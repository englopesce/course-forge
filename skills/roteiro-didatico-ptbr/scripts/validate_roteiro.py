#!/usr/bin/env python3
"""Valida roteiro.json (esquema, tamanhos, trechos x configuração).
Uso: python validate_roteiro.py roteiro.json [--config aula.yaml] [--palavras-max 230]
Sai com código 1 se houver erro; avisos não bloqueiam.
"""
import argparse, json, os, re, sys


def faixa(x):
    a, _, b = str(x).partition("-")
    return int(a), int(b or a)


def load_cfg(p):
    if not p:
        return {}
    import yaml
    return yaml.safe_load(open(p, encoding="utf-8")) or {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("roteiro"); ap.add_argument("--config"); ap.add_argument("--palavras-max", type=int)
    a = ap.parse_args()
    r = json.load(open(a.roteiro, encoding="utf-8"))
    cfg = load_cfg(a.config)
    err, warn = [], []
    ex = cfg.get("exemplo") or {}
    repo = None
    if ex.get("dir"):
        repo = ex["dir"] if os.path.isabs(ex["dir"]) else os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(a.config)), ex["dir"]))
    for k in ("titulo", "fonte", "cenas"):
        if k not in r: err.append(f"falta '{k}'")
    f = r.get("fonte", {})
    for k in ("titulo", "canal", "url"):
        if not f.get(k): err.append(f"fonte.{k} vazio")
    cenas = r.get("cenas", [])
    if not 5 <= len(cenas) <= 8: warn.append(f"{len(cenas)} cenas (recomendado 5–8)")
    ids = set()
    clips = {c["id"]: c for c in cfg.get("trechos", [])}
    usados = set()
    for i, c in enumerate(cenas):
        tag = f"cena {i+1} ({c.get('id')})"
        if not re.fullmatch(r"[a-z0-9-]+", c.get("id", "")): err.append(f"{tag}: id inválido (kebab-case)")
        if c.get("id") in ids: err.append(f"{tag}: id repetido")
        ids.add(c.get("id"))
        if not c.get("narracao"): err.append(f"{tag}: sem narracao")
        tela = c.get("tela", [])
        if not 1 <= len(tela) <= 3: err.append(f"{tag}: tela precisa de 1–3 itens")
        for t in tela:
            if len(t) > 60: warn.append(f"{tag}: item de tela longo ({len(t)} car.)")
        t = c.get("trecho")
        if t:
            if clips and t.get("id") not in clips: err.append(f"{tag}: trecho '{t.get('id')}' não existe na config")
            usados.add(t.get("id"))
            if t.get("id") in clips:
                cl = clips[t["id"]]
                dur = tsec(cl["fim"]) - tsec(cl["inicio"])
                for lg in t.get("legendas", []):
                    if lg["ate"] > dur + 0.05 or lg["de"] < 0 or lg["de"] >= lg["ate"]:
                        err.append(f"{tag}: legenda fora do trecho ({lg})")
            if not t.get("legendas"): warn.append(f"{tag}: trecho sem legendas pt-BR")
        cd = c.get("codigo")
        if cd:
            if not cd.get("arquivo"): err.append(f"{tag}: codigo sem 'arquivo'")
            elif repo:
                arq = os.path.join(repo, cd["arquivo"])
                if not os.path.isfile(arq): err.append(f"{tag}: codigo.arquivo não existe no exemplo ({cd['arquivo']})")
                else:
                    nl = len(open(arq, encoding="utf-8").read().rstrip("\n").split("\n"))
                    i0, i1 = faixa(cd.get("linhas", f"1-{nl}"))
                    if not 1 <= i0 <= i1 <= nl: err.append(f"{tag}: codigo.linhas {cd.get('linhas')} fora do arquivo ({nl} linhas)")
                    elif i1 - i0 + 1 > 22: warn.append(f"{tag}: {i1 - i0 + 1} linhas de código (recomendado até ~18)")
                    for d in cd.get("destaques", []):
                        d0, d1 = faixa(d["linhas"] if isinstance(d, dict) else d)
                        if not i0 <= d0 <= d1 <= i1: err.append(f"{tag}: destaque {d0}-{d1} fora de {i0}-{i1}")
            else: err.append(f"{tag}: tem 'codigo' mas a config não tem exemplo.dir")
            if len(tela) > 2: warn.append(f"{tag}: cena com código: prefira 1–2 itens de tela")
    if repo and not any(c.get("codigo") for c in cenas): warn.append("config tem exemplo mas nenhuma cena mostra código")
    nomes_chk = {x["nome"] for x in (cfg.get("exemplo") or {}).get("checagem", []) if isinstance(x, dict)}
    for e in r.get("exercicios", []):
        for k in ("titulo", "enunciado"):
            if not e.get(k): err.append(f"exercício {e.get('id')}: falta '{k}'")
        if e.get("checagem") and e["checagem"] not in nomes_chk: err.append(f"exercício {e.get('id')}: checagem '{e['checagem']}' não está em exemplo.checagem")
    faltando = set(clips) - usados
    if faltando: err.append(f"trechos da config sem cena: {sorted(faltando)}")
    palavras = sum(len(c.get("narracao", "").split()) for c in cenas)
    pmax = a.palavras_max or cfg.get("roteiro", {}).get("palavras_max")
    if pmax and palavras > pmax: warn.append(f"narração com {palavras} palavras (máx. sugerido {pmax})")
    if not r.get("fatos"): warn.append("sem lista 'fatos' (checagem)")
    print(f"roteiro: {len(cenas)} cenas, {palavras} palavras, {len(usados)} trechos, "
          f"{sum(1 for c in cenas if c.get('codigo'))} cena(s) com código, {len(r.get('exercicios', []))} exercício(s)")
    for w in warn: print("AVISO:", w)
    for e in err: print("ERRO:", e)
    sys.exit(1 if err else 0)


def tsec(x):
    if isinstance(x, (int, float)): return float(x)
    p = [float(v) for v in str(x).split(":")]
    s = 0
    for v in p: s = s * 60 + v
    return s


if __name__ == "__main__":
    main()
