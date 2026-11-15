#!/usr/bin/env python3
"""Baixa SÓ legendas + metadados de um vídeo do YouTube (nunca o vídeo).

Uso: python fetch_subs.py URL pasta_saida [--langs "pt.*,pt,en.*,en"]
Gera na pasta: <id>.info.json, <id>*.vtt, transcript.txt (texto corrido),
segments.json ([{"ini":s,"fim":s,"texto":...}]), fonte.json (título, canal, URL, data, verificado).
Prioriza a legenda enviada pelo canal; cai para a automática. Reaproveita arquivos já baixados.
"""
import argparse, glob, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ytdlp_retry import run_ytdlp  # noqa: E402


def secs(x):
    h, m, r = x.split(":")
    return int(h) * 3600 + int(m) * 60 + float(r)


def parse_vtt(path):
    """Lê o VTT em segmentos. Legendas automáticas do YouTube vêm "rolando" (cada cue repete a linha
    anterior e acrescenta a nova, com cues-relâmpago de ~10 ms): aqui cada segmento fica só com o texto novo.
    1) descarta linhas iniciais iguais às linhas do cue anterior; 2) remove sobreposição de palavras (>= 3)."""
    segs, acc, prev_lines = [], [], []
    for blk in open(path, encoding="utf-8").read().split("\n\n"):
        m = re.search(r"(\d+:\d\d:\d\d\.\d+) --> (\d+:\d\d:\d\d\.\d+)", blk)
        if not m:
            continue
        ini, fim = secs(m.group(1)), secs(m.group(2))
        lines = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", l)).strip() for l in blk.splitlines()
                 if "-->" not in l and l.strip() and not l.strip().isdigit()]
        lines = [l for l in lines if l]
        if not lines or fim - ini < 0.05:
            if lines: prev_lines = lines
            continue
        cur = list(lines)
        while cur and cur[0] in prev_lines:
            cur.pop(0)
        prev_lines = lines
        ws = " ".join(cur).split()
        ov = 0
        for k in range(min(len(ws), len(acc)), 0, -1):
            if acc[-k:] == ws[:k] and (k >= 3 or k == len(ws)):
                ov = k; break
        novo = ws[ov:]
        if not novo:
            continue
        acc += novo
        segs.append({"ini": round(ini, 2), "fim": round(fim, 2), "texto": " ".join(novo)})
    return segs


def pick_track(info, langs):
    """Escolhe UMA faixa: enviada pelo canal (na ordem de --langs) > automática original (-orig) > automática."""
    pats = [p.strip() for p in langs.split(",") if p.strip()]
    manual = [k for k in (info.get("subtitles") or {}) if k != "live_chat"]
    autos = list((info.get("automatic_captions") or {}).keys())
    for p in pats:
        for k in sorted(manual):
            if re.fullmatch(p, k): return k, False
    orig = [k for k in autos if k.endswith("-orig")]
    for p in pats:
        for k in orig:
            if re.fullmatch(p, k[:-5]): return k, True
    for p in pats:
        base = p.replace(".*", "")
        if base in autos: return base, True
        for k in sorted(autos):
            if re.fullmatch(p, k): return k, True
    return None, None


def video_id(url):
    m = re.search(r"(?:v=|youtu\.be/|shorts/)([\w-]{11})", url)
    return m.group(1) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url"); ap.add_argument("out")
    ap.add_argument("--langs", default="pt.*,pt,en.*,en")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    vid = video_id(a.url)
    info_p = os.path.join(a.out, f"{vid}.info.json")
    if not glob.glob(os.path.join(a.out, f"{vid}*.vtt")):
        # 1) só os metadados (1 requisição). 2) UMA faixa de legenda escolhida aqui, a partir do info.json
        #    (--load-info-json: não busca a página de novo). Pedir "pt.*,en.*" direto baixava dezenas de
        #    faixas (traduções automáticas) e provocava 429.
        if not os.path.exists(info_p):
            run_ytdlp(["--skip-download", "--write-info-json", "-o", os.path.join(a.out, "%(id)s.%(ext)s"), a.url])
        info = json.load(open(info_p, encoding="utf-8"))
        lang, auto = pick_track(info, a.langs)
        if not lang:
            raise SystemExit(f"sem legenda compatível com {a.langs}")
        print(f"[legendas] faixa escolhida: {lang} ({'automática' if auto else 'enviada pelo canal'})", flush=True)
        run_ytdlp(["--load-info-json", info_p, "--skip-download", "--write-auto-sub" if auto else "--write-sub",
                   "--sub-langs", lang, "--sub-format", "vtt",
                   "-o", os.path.join(a.out, "%(id)s.%(ext)s")])
    info = json.load(open(os.path.join(a.out, f"{vid}.info.json"), encoding="utf-8"))
    subs = info.get("subtitles") or {}
    vtts = sorted(glob.glob(os.path.join(a.out, f"{vid}*.vtt")))
    base = lambda p: os.path.basename(p)
    manual = [v for v in vtts if any(base(v).startswith(f"{vid}.{k}.") for k in subs) and "-orig" not in v]
    # entre manuais, prefere pt
    manual.sort(key=lambda v: (0 if ".pt" in base(v) else 1, v))
    src = (manual or vtts)[0]
    segs = parse_vtt(src)
    open(os.path.join(a.out, "transcript.txt"), "w", encoding="utf-8").write(" ".join(s["texto"] for s in segs))
    json.dump(segs, open(os.path.join(a.out, "segments.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    fonte = {"id": vid, "titulo": info["title"], "canal": info.get("channel"), "url": f"https://www.youtube.com/watch?v={vid}",
             "publicado": info.get("upload_date"), "canal_verificado": info.get("channel_is_verified"),
             "canal_url": info.get("channel_url"), "duracao": info.get("duration"),
             "legenda_usada": base(src), "legenda_manual": bool(manual)}
    json.dump(fonte, open(os.path.join(a.out, "fonte.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(fonte, ensure_ascii=False))


if __name__ == "__main__":
    main()
