#!/usr/bin/env python3
"""Ponto único de uso de LLM do aula-ra: registra tokens por aula em <pasta da aula>/uso-tokens.json.

Hoje as etapas de LLM (roteiro da aula; estrutura do curso) são feitas pelo AGENTE que roda o pipeline, não por uma
chamada de API dentro do script: o pipeline escreve o pedido (PEDIDO_*.md) e o agente responde com o arquivo.
Nesses casos o uso é ESTIMADO com tokenizer (tiktoken o200k_base; sem tiktoken, ~4 caracteres por token) a partir
do que o agente precisa ler (pedido + arquivos que o pedido manda abrir) e do que ele escreve, e o registro sai com
"estimado": true. Quando uma etapa chamar um modelo por API, use `chamar()` (ou `uso_tokens.py chamar`): ele chama um
endpoint compatível com OpenAI (/chat/completions) e registra o uso REAL devolvido em `usage` ("estimado": false).

Registro: {"etapa", "modelo", "entrada", "saida", "cache" (true = etapa pulada pelo cache: 0 gastos),
           "evitados" (tokens que a etapa teria gastado), "estimado", "fonte", "quando", "detalhes"}.

CLI:
  python uso_tokens.py estimar --pasta AULA --etapa roteiro --entrada a.md b.txt --saida roteiro.json [--modelo agente]
  python uso_tokens.py chamar  --pasta AULA --etapa X --prompt pedido.md --saida resposta.txt   # precisa de LLM_API_BASE,
                                                       # LLM_API_KEY e LLM_MODEL no ambiente (nada é lido de outro lugar)
  python uso_tokens.py resumo  uso-tokens.json [...]
"""
import argparse, json, os, sys, time
from urllib import request as _rq

ARQ = "uso-tokens.json"
_ENC = None


def contar(texto):
    """(tokens, fonte). tiktoken o200k_base quando instalado; senão ~4 caracteres/token."""
    global _ENC
    try:
        import tiktoken
        if _ENC is None: _ENC = tiktoken.get_encoding("o200k_base")
        return len(_ENC.encode(texto, disallowed_special=())), "tiktoken o200k_base"
    except Exception:
        return (len(texto) + 3) // 4, "aprox. 4 caracteres/token"


def contar_arquivos(paths):
    tot, fonte, det = 0, "", {}
    for p in paths:
        if not p or not os.path.isfile(p): continue
        n, fonte = contar(open(p, encoding="utf-8", errors="replace").read())
        nome = os.path.basename(p)
        if nome in ("transcript.txt", "segments.json"): nome = f"{os.path.basename(os.path.dirname(p))}/{nome}"  # um por vídeo
        det[nome] = n; tot += n
    return tot, fonte, det


def carregar(pasta):
    p = os.path.join(pasta, ARQ)
    if os.path.exists(p):
        try: return json.load(open(p, encoding="utf-8"))
        except Exception: pass
    return {"registros": []}


def registrar(pasta, etapa, modelo, entrada, saida, cache=False, estimado=True, fonte="", evitados=0, detalhes=None):
    os.makedirs(pasta, exist_ok=True)
    d = carregar(pasta)
    d["registros"].append({"etapa": etapa, "modelo": modelo, "entrada": int(entrada), "saida": int(saida), "cache": bool(cache),
                           "evitados": int(evitados), "estimado": bool(estimado), "fonte": fonte,
                           "quando": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "detalhes": detalhes or {}})
    d["total"] = somar(d["registros"])
    json.dump(d, open(os.path.join(pasta, ARQ), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return d["registros"][-1]


def somar(regs):
    t = {"entrada": 0, "saida": 0, "evitados": 0, "chamadas": 0, "do_cache": 0, "estimados": 0}
    for r in regs:
        t["entrada"] += r.get("entrada", 0); t["saida"] += r.get("saida", 0); t["evitados"] += r.get("evitados", 0)
        t["do_cache"] += 1 if r.get("cache") else 0
        t["chamadas"] += 0 if r.get("cache") else 1
        t["estimados"] += 1 if (r.get("estimado") and not r.get("cache")) else 0
    return t


def estimar(pasta, etapa, entradas, saida, modelo="agente", detalhes=None):
    ne, fonte, de = contar_arquivos(entradas)
    ns, _, ds = contar_arquivos([saida] if isinstance(saida, str) else saida)
    return registrar(pasta, etapa, modelo, ne, ns, estimado=True, fonte=fonte,
                     detalhes={"entrada_por_arquivo": de, "saida_por_arquivo": ds, **(detalhes or {})})


def chamar(pasta, etapa, mensagens, modelo=None, base=None, chave=None, timeout=600, **params):
    """Chamada real (OpenAI-compatível). Registra usage.prompt_tokens/completion_tokens (e cached_tokens, se vier)."""
    base = base or os.environ.get("LLM_API_BASE"); chave = chave or os.environ.get("LLM_API_KEY")
    modelo = modelo or os.environ.get("LLM_MODEL")
    if not (base and chave and modelo):
        raise SystemExit("chamar(): defina LLM_API_BASE, LLM_API_KEY e LLM_MODEL (ou faça a etapa pelo agente e use estimar)")
    body = json.dumps({"model": modelo, "messages": mensagens, **params}).encode()
    req = _rq.Request(base.rstrip("/") + "/chat/completions", data=body,
                      headers={"Content-Type": "application/json", "Authorization": f"Bearer {chave}"})
    r = json.load(_rq.urlopen(req, timeout=timeout))
    u = r.get("usage") or {}
    cached = (u.get("prompt_tokens_details") or {}).get("cached_tokens", 0)
    registrar(pasta, etapa, r.get("model", modelo), u.get("prompt_tokens", 0), u.get("completion_tokens", 0),
              estimado=False, fonte="usage da API", detalhes={"prompt_cache_tokens": cached, "id": r.get("id")})
    return r["choices"][0]["message"]["content"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("estimar"); e.add_argument("--pasta", required=True); e.add_argument("--etapa", required=True)
    e.add_argument("--entrada", nargs="+", default=[]); e.add_argument("--saida", nargs="*", default=[]); e.add_argument("--modelo", default="agente")
    c = sub.add_parser("chamar"); c.add_argument("--pasta", required=True); c.add_argument("--etapa", required=True)
    c.add_argument("--prompt", required=True); c.add_argument("--saida", required=True)
    r = sub.add_parser("resumo"); r.add_argument("arquivos", nargs="+")
    a = ap.parse_args()
    if a.cmd == "estimar":
        print(json.dumps(estimar(a.pasta, a.etapa, a.entrada, a.saida, a.modelo), ensure_ascii=False))
    elif a.cmd == "chamar":
        txt = chamar(a.pasta, a.etapa, [{"role": "user", "content": open(a.prompt, encoding="utf-8").read()}])
        open(a.saida, "w", encoding="utf-8").write(txt)
    else:
        tot = somar([x for f in a.arquivos for x in carregar(os.path.dirname(os.path.abspath(f)) if f.endswith(ARQ) else f)["registros"]])
        print(json.dumps(tot, ensure_ascii=False))


if __name__ == "__main__":
    main()
