#!/usr/bin/env python3
"""Recorta trechos curtos de vídeos do YouTube com crédito gravado na imagem.

Baixa SÓ as seções necessárias (yt-dlp --download-sections, formato modesto ≤720p H.264),
com folga de --pad s, reaproveitando o cache; corta com precisão no ffmpeg, grava o crédito
(canal, título, link com tempo) e normaliza o áudio.

Uso: python cut_clips.py --trechos trechos.json --fontes pasta_legendas/ --cache cache_raw/ --out clips/
        [--roteiro roteiro.json] [--pad 1] [--font Inter] [--altura 720] [--formatos 16x9,9x16] [--fundo-9x16 blur]
trechos.json: [{"id","video","inicio","fim","mostra"}]   (inicio/fim em s ou "mm:ss")
fontes: pasta com <video_id>/fonte.json (gerado por youtube-legendas/fetch_subs.py)
Saída: clips/<id>.mp4, clips/<id>.vtt (legenda pt-BR do roteiro, se houver), clips/clips.json
Com 9x16 em --formatos: também clips/<id>_9x16.mp4 (1080x1920, FIT: quadro inteiro sem corte, fundo
desfocado do próprio trecho, crédito na área livre de cima; ver reframe_9x16.py) e "arquivo_9x16" no clips.json.
"""
import time, argparse, glob, json, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ytdlp_retry import run_ytdlp  # noqa: E402
from reframe_9x16 import filtro_9x16  # noqa: E402

FMT = "bv*[height<={h}][vcodec^=avc1]+ba[ext=m4a]/b[height<={h}]"


def tsec(x):
    if isinstance(x, (int, float)): return float(x)
    s = 0
    for v in str(x).split(":"): s = s * 60 + float(v)
    return s


def mmss(s):
    return f"{int(s // 60):02d}:{s % 60:05.2f}"


def font_file(name):
    try:
        return subprocess.check_output(["fc-match", "-f", "%{file}", f"{name}:bold"]).decode().strip()
    except Exception:
        return ""


def cached(cache, vid, a, b):
    for p in glob.glob(os.path.join(cache, f"{vid}_*-*.mp4")):
        m = re.search(r"_(\d+)-(\d+)\.mp4$", p)
        if m and int(m.group(1)) <= a and int(m.group(2)) >= b:
            return p, int(m.group(1))
    return None, None


def esc_dt(s):  # escape para drawtext
    return s.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\u2019").replace("%", "\\%")


def vtt_ts(t):
    return f"{int(t // 3600):02d}:{int(t % 3600 // 60):02d}:{t % 60:06.3f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trechos", required=True); ap.add_argument("--fontes", required=True)
    ap.add_argument("--cache", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--roteiro", default=""); ap.add_argument("--pad", type=float, default=1.0)
    ap.add_argument("--font", default="Inter"); ap.add_argument("--altura", type=int, default=720)
    ap.add_argument("--formatos", default="16x9"); ap.add_argument("--fundo-9x16", dest="fundo9", default="blur")
    a = ap.parse_args()
    os.makedirs(a.cache, exist_ok=True); os.makedirs(a.out, exist_ok=True)
    trechos = json.load(open(a.trechos, encoding="utf-8"))
    leg = {}
    if a.roteiro and os.path.exists(a.roteiro):
        for c in json.load(open(a.roteiro, encoding="utf-8"))["cenas"]:
            if c.get("trecho"): leg[c["trecho"]["id"]] = c["trecho"].get("legendas", [])
    def tem_video(p):
        return "video" in subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type", "-of", "csv=p=0", p],
                                         capture_output=True, text=True).stdout
    # 1) baixar o que falta, agrupado por vídeo (uma chamada por vídeo)
    falta = {}
    for t in trechos:
        i0, i1 = tsec(t["inicio"]), tsec(t["fim"])
        wa, wb = int(max(0, i0 - a.pad)), int(i1 + a.pad + 0.999)
        p, _ = cached(a.cache, t["video"], int(i0), int(i1 + 0.999))
        if p and not tem_video(p): os.remove(p); p = None  # cache antigo só com áudio
        if not p: falta.setdefault(t["video"], []).append((wa, wb))
    for tentativa, espera in enumerate([0, 30, 90]):  # seção às vezes vem só com áudio: apaga e baixa de novo
        if not falta: break
        if espera: print(f"[trechos] seção sem vídeo; nova tentativa em {espera}s"); time.sleep(espera)
        for vid, wins in falta.items():
            args = ["-f", FMT.format(h=a.altura), "--force-keyframes-at-cuts", "--merge-output-format", "mp4",
                    "-o", os.path.join(a.cache, "%(id)s_%(section_start)d-%(section_end)d.%(ext)s")]
            for wa, wb in wins: args += ["--download-sections", f"*{wa}-{wb}"]
            print(f"[trechos] baixando {len(wins)} seção(ões) de {vid}: {wins}")
            run_ytdlp(args + [f"https://www.youtube.com/watch?v={vid}"])
        ruins = {}
        for vid, wins in falta.items():
            for t in trechos:
                if t["video"] != vid: continue
                p, _ = cached(a.cache, vid, int(tsec(t["inicio"])), int(tsec(t["fim"]) + 0.999))
                if p and not tem_video(p):
                    os.remove(p); ruins.setdefault(vid, []).extend(w for w in wins if w not in ruins.get(vid, []))
        falta = ruins
    # 2) cortar com crédito
    ff = font_file(a.font)
    out_meta = []
    for t in trechos:
        vid = t["video"]; i0, i1 = tsec(t["inicio"]), tsec(t["fim"]); dur = round(i1 - i0, 3)
        fonte = json.load(open(os.path.join(a.fontes, vid, "fonte.json"), encoding="utf-8"))
        raw, base = cached(a.cache, vid, int(i0), int(i1 + 0.999))
        if not raw: raise SystemExit(f"trecho {t['id']}: seção não encontrada no cache")
        link = f"youtu.be/{vid}?t={int(i0)}"
        titulo = t.get("titulo_curto") or fonte["titulo"]
        l1 = esc_dt(f"Trecho do vídeo original · {fonte['canal']} (YouTube)")
        l2 = esc_dt(f"“{titulo}” · {link}")
        fnt = f"fontfile='{ff}':" if ff else ""
        H = a.altura; W = H * 16 // 9; fs1 = round(H * 0.036); fs2 = round(H * 0.031)
        vf = (f"scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30,"
              f"drawbox=x=0:y=0:w=iw:h={round(H*0.125)}:color=black@0.62:t=fill,"
              f"drawtext={fnt}text='{l1}':x={round(H*0.03)}:y={round(H*0.016)}:fontsize={fs1}:fontcolor=white,"
              f"drawtext={fnt}text='{l2}':x={round(H*0.03)}:y={round(H*0.016)+fs1+round(H*0.008)}:fontsize={fs2}:fontcolor=0xDDE6F5")
        out = os.path.join(a.out, f"{t['id']}.mp4")
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{i0 - base:.3f}", "-i", raw, "-t", f"{dur}",
                               "-vf", vf, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,afade=t=in:d=0.15,afade=t=out:st=%.3f:d=0.3" % (dur - 0.3),
                               "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-g", "30", "-keyint_min", "30", "-pix_fmt", "yuv420p",
                               "-c:a", "aac", "-b:a", "128k", "-ac", "2", "-movflags", "+faststart", out])
        real = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out]).decode())
        out9 = None
        if "9x16" in a.formatos.split(","):
            out9 = os.path.join(a.out, f"{t['id']}_9x16.mp4")
            # mesmo quadro 16:9 do trecho, mas SEM o crédito gravado (o crédito vai para a área livre)
            fc = ("[0:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1[src];"
                  + filtro_9x16(fonte["canal"], titulo, link, a.font, a.fundo9, entrada="[src]"))
            subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{i0 - base:.3f}", "-i", raw, "-t", f"{dur}",
                                   "-filter_complex", fc, "-map", "[v]", "-map", "0:a",
                                   "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,afade=t=in:d=0.15,afade=t=out:st=%.3f:d=0.3" % (dur - 0.3),
                                   "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-g", "30", "-keyint_min", "30", "-pix_fmt", "yuv420p",
                                   "-c:a", "aac", "-b:a", "128k", "-ac", "2", "-movflags", "+faststart", out9])
        vtt = None
        if leg.get(t["id"]):
            vtt = os.path.join(a.out, f"{t['id']}.vtt")
            with open(vtt, "w", encoding="utf-8") as f:
                f.write("WEBVTT\n\n")
                for k, lg in enumerate(leg[t["id"]], 1):
                    f.write(f"{k}\n{vtt_ts(lg['de'])} --> {vtt_ts(lg['ate'])}\n{lg['texto']}\n\n")
        out_meta.append({"id": t["id"], "arquivo": os.path.basename(out), "vtt": os.path.basename(vtt) if vtt else None,
                         "arquivo_9x16": os.path.basename(out9) if out9 else None,
                         "video": vid, "inicio": i0, "fim": i1, "duracao": round(real, 3), "mostra": t.get("mostra", ""),
                         "canal": fonte["canal"], "titulo": fonte["titulo"], "url": fonte["url"],
                         "link_tempo": f"https://youtu.be/{vid}?t={int(i0)}", "inicio_mmss": mmss(i0), "fim_mmss": mmss(i1)})
        print(f"[trechos] {t['id']}: {mmss(i0)}–{mmss(i1)} ({real:.2f}s) -> {out}")
    json.dump(out_meta, open(os.path.join(a.out, "clips.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
