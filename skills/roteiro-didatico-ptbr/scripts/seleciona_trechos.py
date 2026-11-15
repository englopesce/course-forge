#!/usr/bin/env python3
"""Seleciona só os trechos relevantes das transcrições para o pedido de roteiro (economia de tokens).

Janelas de ~janela_s segundos (falas consecutivas de segments.json, com timestamps) são pontuadas por BM25 contra
uma consulta montada da config: tema, objetivo, tópicos do contexto, termos de checagem, trechos (mostra/título),
`_busca_videos` e `roteiro.selecao.palavras_chave`, expandida pt→en (references/glossario-pt-en.json) porque muitas
fontes estão em inglês. Entram sempre as janelas em volta de cada trecho da config (± contexto_trecho_s); depois as
de maior nota, até `max_tokens` (contados com tiktoken). Saída: JSON com as janelas e um .md pronto para o pedido.

Config (aula.yaml): roteiro.selecao: {modo: bm25 | completo, max_tokens: 2500, janela_s: 45, contexto_trecho_s: 30,
                                       min_nota: 0.0, palavras_chave: [..]}
Uso: python seleciona_trechos.py --config aula.yaml --legendas pasta_legendas/ --saida selecao.json
"""
import argparse, json, math, os, re, sys, unicodedata
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "aula-ra", "scripts"))
try:
    from uso_tokens import contar
except Exception:  # skill usada sozinha
    def contar(t): return (len(t) + 3) // 4, "aprox. 4 caracteres/token"

PADRAO = {"modo": "bm25", "max_tokens": 2500, "janela_s": 45, "contexto_trecho_s": 30, "min_nota": 0.0, "palavras_chave": []}
STOP = set("""a o e é de da do das dos em no na nos nas um uma uns umas para por com sem que se como mais mas ou ao aos à às
seu sua seus suas ele ela eles elas isso esse essa este esta aquilo the a an and or of to in on for with is are was were be
been it this that these those you we they i he she his her its their our your as at by from not no so if then than there
here what which who how when where why can will would should could do does did have has had just also very really about
into out up down over more most some any all each every one two like get got going know think thing things right okay
aula aulas curso módulo modulo tópicos topicos ementa cobertos anterior próxima proxima vista não antecipe explicar
relacionar programadores outros exemplos exemplo""".split())


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def toks(s):
    out = []
    for w in re.findall(r"[a-zA-ZÀ-ÿ0-9]+", s.lower()):
        if w in STOP or len(w) < 3: continue
        w = sem_acento(w)
        if len(w) > 4 and w.endswith("s"): w = w[:-1]  # plural simples (tokens -> token)
        out.append(w)
    return out


def tsec(x):
    if isinstance(x, (int, float)): return float(x)
    s = 0
    for v in str(x).split(":"): s = s * 60 + float(v)
    return s


def mmss(t):
    return f"{int(t // 60)}:{t % 60:04.1f}"


def consulta(cfg):
    au, ro = cfg.get("aula", {}), cfg.get("roteiro", {})
    sel = {**PADRAO, **(ro.get("selecao") or {})}
    partes = [au.get("tema", ""), au.get("objetivo", "")]
    ctx = au.get("contexto") or []
    for c in (ctx if isinstance(ctx, list) else [ctx]):
        if "Tópicos" in str(c) or "Topicos" in str(c): partes.append(str(c).split(":", 1)[-1])
    partes += (cfg.get("narracao") or {}).get("termos_checagem") or []
    for t in cfg.get("trechos", []): partes += [t.get("mostra", ""), t.get("titulo_curto", "")]
    b = cfg.get("_busca_videos") or []
    partes += b if isinstance(b, list) else [b]
    partes += sel.get("palavras_chave") or []
    q = toks(" ".join(map(str, partes)))
    glos = {k: v for k, v in json.load(open(os.path.join(HERE, "..", "references", "glossario-pt-en.json"), encoding="utf-8")).items()
            if not k.startswith("_")}
    extra = [w for t in q for k, ws in glos.items() if t.startswith(k) for w in toks(" ".join(ws))]
    return q + extra, sel


def janelas(segs, vid, janela_s):
    out, cur = [], []
    for s in segs:
        cur.append(s)
        if cur[-1]["fim"] - cur[0]["ini"] >= janela_s:
            out.append(cur); cur = []
    if cur: out.append(cur)
    return [{"video": vid, "ini": round(c[0]["ini"], 1), "fim": round(c[-1]["fim"], 1),
             "texto": " ".join(x["texto"].strip() for x in c)} for c in out]


def bm25(docs, q, k1=1.4, b=0.75):
    N = len(docs); tk = [toks(d["texto"]) for d in docs]
    avg = sum(map(len, tk)) / max(1, N); df = Counter(w for t in tk for w in set(t)); qc = Counter(q)
    notas = []
    for t in tk:
        tf = Counter(t); s = 0.0
        for w, qn in qc.items():
            if w not in tf: continue
            idf = math.log(1 + (N - df[w] + 0.5) / (df[w] + 0.5))
            s += idf * tf[w] * (k1 + 1) / (tf[w] + k1 * (1 - b + b * len(t) / avg)) * (1 + 0.2 * (qn - 1))
        notas.append(round(s, 3))
    return notas


def selecionar(cfg, legendas, modo=None):
    q, sel = consulta(cfg)
    if modo: sel["modo"] = modo
    fontes = sorted(d for d in os.listdir(legendas) if os.path.exists(os.path.join(legendas, d, "segments.json")))
    docs = []
    for vid in fontes:
        docs += janelas(json.load(open(os.path.join(legendas, vid, "segments.json"), encoding="utf-8")), vid, sel["janela_s"])
    for d, n in zip(docs, bm25(docs, q)): d["nota"] = n; d["tokens"] = contar(d["texto"])[0]
    total = sum(d["tokens"] for d in docs)
    if sel["modo"] == "completo":
        escolha = list(range(len(docs)))
    else:
        obrig = set()
        for t in cfg.get("trechos", []):
            i0, i1 = tsec(t["inicio"]) - sel["contexto_trecho_s"], tsec(t["fim"]) + sel["contexto_trecho_s"]
            obrig |= {i for i, d in enumerate(docs) if d["video"] == t["video"] and d["fim"] > i0 and d["ini"] < i1}
        escolha, usado = [], 0
        for i in sorted(obrig, key=lambda i: -docs[i]["nota"]):
            escolha.append(i); usado += docs[i]["tokens"]
        for i in sorted(range(len(docs)), key=lambda i: -docs[i]["nota"]):
            if i in obrig or docs[i]["nota"] <= sel["min_nota"]: continue
            if usado + docs[i]["tokens"] > sel["max_tokens"]: continue
            escolha.append(i); usado += docs[i]["tokens"]
    for i in escolha: docs[i]["obrigatoria"] = sel["modo"] != "completo" and i in (obrig if sel["modo"] != "completo" else set())
    escolhidas = sorted((docs[i] for i in escolha), key=lambda d: (fontes.index(d["video"]), d["ini"]))
    return {"modo": sel["modo"], "max_tokens": sel["max_tokens"], "consulta": sorted(set(q)),
            "tokens_transcricoes": total, "tokens_selecionados": sum(d["tokens"] for d in escolhidas),
            "janelas_total": len(docs), "janelas": escolhidas}


def markdown(res):
    out = [f"## Trechos relevantes das transcrições (seleção {res['modo']}: {res['tokens_selecionados']} de "
           f"{res['tokens_transcricoes']} tokens, {len(res['janelas'])} de {res['janelas_total']} janelas)",
           "Use estes trechos como base (tempos no vídeo original). Abra a transcrição inteira só se faltar algo essencial.", ""]
    vid = None
    for d in res["janelas"]:
        if d["video"] != vid:
            vid = d["video"]; out.append(f"### [{vid}]")
        out.append(f"- [{mmss(d['ini'])}–{mmss(d['fim'])}]{' (trecho)' if d.get('obrigatoria') else ''} {d['texto']}")
    return "\n".join(out) + "\n"


def main():
    import yaml
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", required=True); ap.add_argument("--legendas", required=True); ap.add_argument("--saida", required=True)
    ap.add_argument("--modo", choices=["bm25", "completo"], help="sobrepõe roteiro.selecao.modo")
    a = ap.parse_args()
    res = selecionar(yaml.safe_load(open(a.config, encoding="utf-8")), a.legendas, a.modo)
    json.dump(res, open(a.saida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(os.path.splitext(a.saida)[0] + ".md", "w", encoding="utf-8").write(markdown(res))
    print(f"seleção {res['modo']}: {res['tokens_selecionados']}/{res['tokens_transcricoes']} tokens, "
          f"{len(res['janelas'])}/{res['janelas_total']} janelas -> {a.saida}")


if __name__ == "__main__":
    main()
