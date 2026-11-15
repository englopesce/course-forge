#!/usr/bin/env python3
"""Lê uma ementa em texto (copiada de PDF/Docs) e devolve uma estrutura com ids estáveis.

Uso: python ementa.py ementa.txt [saida.json]
Reconhece: módulos "N - Título" / "N- Título" no começo da linha; unidades "Unidade N: ..." / "UNIDADE IV - ...";
itens com marcadores ● ○ ■ - (nível 1/2/3/1), numerados "1.2." e "Prática N:"; linhas de continuação (sem marcador)
são somadas ao item anterior. Remove caracteres invisíveis (U+200B) e o rodapé repetido de propaganda ("Dúvidas? ...",
telefone). Ids: m01, m01.u02, m01.i007 (sequencial no módulo). O texto original do item é mantido.
"""
import json, re, sys

RUIDO = [re.compile(r"^Dúvidas\?"), re.compile(r"^\+?\(?\d{2}\)?\s*\d{2}\s*\d{4}-\d{4}$")]
MOD = re.compile(r"^(\d{1,2})\s*-\s*(\S.+)$")
UNI = re.compile(r"^(Unidade|UNIDADE)\s+([0-9IVXL]+)\s*[:\-–—]?\s*(.*)$")
MARC = {"●": 1, "○": 2, "■": 3, "-": 1, "–": 1}
NUM = re.compile(r"^(\d+\.\d+)\.?\s+(.+)$")
PRAT = re.compile(r"^(Prática\s*\d+\s*:.*|Projeto\s+(final|integrador).*)$", re.I)


def limpar(t):
    return t.replace("\u200b", "").replace("\ufeff", "").rstrip()


def parse(texto):
    linhas = [limpar(l) for l in texto.splitlines()]
    titulo = next((l.strip() for l in linhas if l.strip()), "")
    mods, mod, uni, ult = [], None, None, None
    for bruto in linhas:
        l = bruto.strip()
        if not l or any(r.search(l) for r in RUIDO): continue
        m = MOD.match(bruto) if not bruto.startswith(" ") else None
        if m and not NUM.match(l):
            mod = {"id": f"m{int(m.group(1)):02d}", "n": int(m.group(1)), "titulo": m.group(2).strip(), "unidades": [], "itens": []}
            mods.append(mod); uni = None; ult = None; continue
        if mod is None: continue
        m = UNI.match(l)
        if m:
            uni = {"id": f"{mod['id']}.u{len(mod['unidades']) + 1:02d}", "rotulo": f"Unidade {m.group(2)}", "titulo": m.group(3).strip(" —–-")}
            mod["unidades"].append(uni); ult = None; continue
        nivel, txt, pratica = None, None, False
        if l[0] in MARC and (len(l) == 1 or l[1] in " \t"):
            nivel, txt = MARC[l[0]], l[1:].strip()
        elif NUM.match(l):
            nivel, txt = 1, l
        elif PRAT.match(l):
            nivel, txt, pratica = 1, l, True
        if txt is not None:
            if not txt: continue
            ult = {"id": f"{mod['id']}.i{len(mod['itens']) + 1:03d}", "nivel": nivel, "texto": txt,
                   "unidade": uni["id"] if uni else None}
            if pratica: ult["pratica"] = True
            # pai = item anterior de nível menor
            for ant in reversed(mod["itens"]):
                if ant["nivel"] < nivel: ult["pai"] = ant["id"]; break
            mod["itens"].append(ult); continue
        if ult is not None:  # continuação
            ult["texto"] = (ult["texto"] + " " + l).strip()
        elif uni is not None:
            uni["titulo"] = (uni["titulo"] + " " + l).strip()
    return {"titulo": titulo, "modulos": mods}


def main():
    e = parse(open(sys.argv[1], encoding="utf-8").read())
    out = json.dumps(e, ensure_ascii=False, indent=1)
    if len(sys.argv) > 2: open(sys.argv[2], "w", encoding="utf-8").write(out)
    else: print(out)
    print(f"{len(e['modulos'])} módulos, {sum(len(m['itens']) for m in e['modulos'])} itens", file=sys.stderr)


if __name__ == "__main__":
    main()
