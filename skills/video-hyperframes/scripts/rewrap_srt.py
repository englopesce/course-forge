#!/usr/bin/env python3
"""Requebra as linhas de um SRT para uma largura menor (ex.: vídeo vertical 9:16).
Uso: python rewrap_srt.py entrada.srt saida.srt [--max 26]
Mantém tempos e texto; só refaz as quebras, equilibrando o comprimento das linhas."""
import argparse, math, re


def rewrap(txt, mx):
    ws = " ".join(txt.split()).split(" ")
    total = len(" ".join(ws))
    n = max(1, math.ceil(total / mx))
    alvo = total / n; linhas, cur = [], []
    for w in ws:
        if cur and len(" ".join(cur + [w])) > max(alvo + 4, 1) and len(linhas) < n - 1:
            linhas.append(" ".join(cur)); cur = [w]
        else:
            cur.append(w)
    linhas.append(" ".join(cur))
    return "\n".join(linhas)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("entrada"); ap.add_argument("saida"); ap.add_argument("--max", type=int, default=26)
    a = ap.parse_args()
    blocos = re.split(r"\n\s*\n", open(a.entrada, encoding="utf-8").read().strip())
    out = []
    for b in blocos:
        ls = b.splitlines()
        if len(ls) >= 3 and "-->" in ls[1]:
            out.append("\n".join(ls[:2] + [rewrap(" ".join(ls[2:]), a.max)]))
        else:
            out.append(b)
    open(a.saida, "w", encoding="utf-8").write("\n\n".join(out) + "\n")
    print("ok:", a.saida, len(out), "blocos")


if __name__ == "__main__":
    main()
