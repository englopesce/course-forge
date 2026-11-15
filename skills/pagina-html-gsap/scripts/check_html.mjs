// Confere a página no Chrome headless: sem internet, coleta erros de JS, navega pelos
// passos com o botão "Próximo" e salva PNGs. Uso:
//   npm i puppeteer-core   (uma vez, na pasta de trabalho)
//   CHROME=/usr/bin/google-chrome node check_html.mjs aula.html saida_png/ 1,3,6,8
// Para passos com <video>, confere se o MP4 local carregou (metadados, dimensões) e as legendas.
import puppeteer from "puppeteer-core";
import fs from "node:fs";
import path from "node:path";

const [file, outDir = ".", stepsArg = "1,2"] = process.argv.slice(2);
const steps = stepsArg.split(",").map(Number);
fs.mkdirSync(outDir, { recursive: true });
const browser = await puppeteer.launch({ executablePath: process.env.CHROME || "/usr/bin/google-chrome",
  headless: true, args: ["--no-sandbox"] });
const page = await browser.newPage();
await page.setViewport({ width: 1600, height: 900 });
const errors = [];
page.on("pageerror", (e) => errors.push("pageerror: " + e.message));
page.on("console", (m) => { if (m.type() === "error") errors.push("console: " + m.text()); });
page.on("requestfailed", (r) => {
  const why = (r.failure() && r.failure().errorText) || "";
  // trocar de passo interrompe o download parcial do <video> (ERR_ABORTED): não é erro; o carregamento é checado abaixo
  if (/\.(mp4|webm)$/i.test(r.url()) && /ERR_ABORTED/.test(why)) return;
  errors.push("requestfailed: " + r.url() + " " + why);
});
await page.setOfflineMode(true); // prova que funciona sem internet
await page.goto("file://" + path.resolve(file), { waitUntil: "load" });
const info = await page.evaluate(() => ({ gsap: !!window.gsap, version: window.gsap && gsap.version, total: AULA.cenas.length }));
let cur = 1;
for (const s of steps) {
  while (cur < s) { await page.click("#next"); cur++; }
  await new Promise((r) => setTimeout(r, 2500)); // espera a animação terminar
  const txt = await page.$eval("#step h1", (e) => e.textContent.trim());
  const vid = await page.evaluate(async () => {
    const v = document.querySelector("#step video");
    if (!v) return null;
    if (v.readyState < 1) await new Promise((r) => { v.onloadedmetadata = r; v.onerror = r; setTimeout(r, 8000); });
    const t = v.textTracks[0];
    if (t) { t.mode = "showing"; await new Promise((r) => setTimeout(r, 500)); }
    return { src: v.currentSrc.split("/").slice(-2).join("/"), readyState: v.readyState, duration: v.duration,
      w: v.videoWidth, h: v.videoHeight, erro: v.error && v.error.code, legendas: t ? (t.cues ? t.cues.length : 0) : null };
  });
  if (vid) { console.log(`passo ${s} vídeo:`, JSON.stringify(vid)); if (!(vid.readyState >= 1 && vid.w > 0)) errors.push("vídeo não carregou: " + vid.src); }
  const out = path.join(outDir, `html_passo_${s}.png`);
  await page.screenshot({ path: out });
  console.log(`passo ${s}: "${txt}" -> ${out}`);
}
// volta um passo para testar o botão Anterior
await page.click("#prev");
const back = await page.$eval("#cont", (e) => e.textContent);
console.log(JSON.stringify({ ...info, aposAnterior: back, erros: errors }));
await browser.close();
process.exit(errors.length ? 1 : 0);
