#!/usr/bin/env python3
"""Executa o yt-dlp com espera progressiva quando o YouTube responde 429 / verificação de robô.
Nunca usa cookies de conta. Importável (run_ytdlp) ou via linha de comando:
  python ytdlp_retry.py -- <argumentos do yt-dlp>
Variáveis: YTDLP (caminho do binário), YT_BACKOFF="120,300,600" (segundos entre tentativas).
"""
import os, shutil, subprocess, sys, time

BLOCK_MARKERS = ("HTTP Error 429", "Too Many Requests", "confirm you", "not a bot")


def ytdlp_bin():
    return os.environ.get("YTDLP") or shutil.which("yt-dlp") or os.path.expanduser("~/.local/bin/yt-dlp")


def run_ytdlp(args, backoff=None, log=print):
    if any(a.startswith("--cookies") for a in args):
        raise SystemExit("Política: não usar cookies de conta com o yt-dlp.")
    waits = backoff or [int(x) for x in os.environ.get("YT_BACKOFF", "120,300,600").split(",")]
    base = [ytdlp_bin()]
    if shutil.which("node"):
        base += ["--js-runtimes", "node"]
    for n in range(len(waits) + 1):
        p = subprocess.run(base + args, capture_output=True, text=True)
        out = p.stdout + p.stderr
        if p.returncode == 0:
            return out
        if any(m in out for m in BLOCK_MARKERS) and n < len(waits):
            log(f"[yt-dlp {time.strftime('%H:%M:%S')}] YouTube bloqueou (429/robô). Esperando {waits[n]}s e tentando de novo ({n+1}/{len(waits)})...", flush=True)
            time.sleep(waits[n]); continue
        sys.stderr.write(out[-3000:])
        raise SystemExit(f"yt-dlp falhou (código {p.returncode}).")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--":
        a = a[1:]
    print(run_ytdlp(a)[-2000:])
