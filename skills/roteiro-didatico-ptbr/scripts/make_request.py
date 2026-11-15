#!/usr/bin/env python3
"""Monta o pedido de roteiro para o agente (preenche templates/prompt_roteiro.md).
Uso: python make_request.py --config aula.yaml --legendas pasta_legendas/ --saida roteiro.json --pedido PEDIDO.md [--retomar "cmd"]
Inclui caminhos das transcrições e, para cada trecho da config, as falas originais do intervalo.
Com --selecao (saída .md de seleciona_trechos.py), o pedido traz só as janelas relevantes das transcrições (com tempos)
e a transcrição inteira fica como reserva: é a economia de tokens da v1.4.0.
Público, nível, tom, linguagem, estrutura e fechamento vêm da config (`aula.*` e `roteiro.*`), com padrões
para público não técnico. Com `exemplo.dir` na config, acrescenta a seção técnica: arquivos do repositório de
exemplo (com nº de linhas), o formato de `cenas[].codigo` e de `exercicios`.
"""
import argparse, glob, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
PADRAO = {"nivel": "iniciante, não técnico", "tom": "didático, direto e acolhedor",
          "linguagem": "linguagem simples, frases curtas, sem jargão (explique termos em inglês)",
          "estrutura": "abertura → conceito → como funciona → (analogia) → exemplo/demonstração → riscos/governança → para lembrar",
          "fechamento": "Para lembrar"}
IGNORAR = {"node_modules", "dist", "build", ".git", ".turbo", "coverage"}


def secao_tecnica(cfg, cfg_path):
    ex = cfg.get("exemplo") or {}
    if not ex.get("dir"): return ""
    repo = ex["dir"] if os.path.isabs(ex["dir"]) else os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(cfg_path)), ex["dir"]))
    arqs = []
    for r, ds, fs in os.walk(repo):
        ds[:] = sorted(d for d in ds if d not in IGNORAR)
        for f in sorted(fs):
            p = os.path.join(r, f)
            try: n = sum(1 for _ in open(p, encoding="utf-8"))
            except (UnicodeDecodeError, OSError): continue
            arqs.append(f"  - `{os.path.relpath(p, repo)}` ({n} linhas)")
    cmds = "\n".join(f"  - {c['nome']}: `{c['cmd']}`" if isinstance(c, dict) else f"  - `{c}`" for c in ex.get("checagem", []))
    return f"""## Aula técnica: código na tela e exercícios
Repositório de exemplo (testado automaticamente pela etapa `codigo`): `{repo}`
{chr(10).join(arqs) or '  (vazio)'}
Comandos de checagem (rodam numa cópia limpa; a etapa falha se algum falhar):
{cmds or '  (nenhum)'}

- Mostre código **só deste repositório**: na cena, `"codigo": {{"arquivo": "src/x.ts", "linhas": "1-18",
  "destaques": [{{"linhas": "5-9", "nota": "frase curta"}}]}}`. Até ~18 linhas e ~70 caracteres por linha
  (a fonte diminui se passar). Os destaques acendem na ordem, dividindo o tempo da fala da cena: narre na mesma ordem.
- Na cena com código, `tela` tem 1–2 itens curtos (o código ocupa a maior parte da tela).
- `exercicios` (lista, 1–3): `{{"id", "titulo", "enunciado", "dica", "arquivo", "checagem"}}`; `checagem` = nome de um
  comando acima que confere a solução (opcional). Vão para a página (seção Exercícios) e para `exercicios.md`.
- A narração não lê código símbolo a símbolo: diga o que o trecho faz e por quê.

"""


def tsec(x):
    if isinstance(x, (int, float)): return float(x)
    s = 0
    for v in str(x).split(":"): s = s * 60 + float(v)
    return s


def main():
    import yaml
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True); ap.add_argument("--legendas", required=True)
    ap.add_argument("--saida", required=True); ap.add_argument("--pedido", required=True)
    ap.add_argument("--retomar", default="")
    ap.add_argument("--selecao", default="", help=".md de seleciona_trechos.py: só os trechos relevantes entram no pedido")
    a = ap.parse_args()
    cfg = yaml.safe_load(open(a.config, encoding="utf-8"))
    tpl = open(os.path.join(HERE, "..", "templates", "prompt_roteiro.md"), encoding="utf-8").read()
    fontes = []
    for d in sorted(glob.glob(os.path.join(a.legendas, "*", "fonte.json"))):
        f = json.load(open(d, encoding="utf-8")); pasta = os.path.dirname(d)
        if a.selecao:  # economia de tokens: o agente lê só a seleção abaixo; a transcrição inteira fica de reserva
            fontes.append(f"- [{f['id']}] “{f['titulo']}” — {f['canal']} (verificado: {f.get('canal_verificado')}), {f['url']}\n"
                          f"  (inteira, só se faltar algo essencial: `{os.path.abspath(os.path.join(pasta, 'transcript.txt'))}`)")
            rs = os.path.join(pasta, "resumo.md")
            if os.path.exists(rs):  # resumo do vídeo reaproveitado do cache do curso (escrito uma vez)
                fontes.append("  resumo (reaproveitado): " + open(rs, encoding="utf-8").read().strip().replace("\n", "\n  "))
        else:
            fontes.append(f"- [{f['id']}] “{f['titulo']}” — {f['canal']} (verificado: {f.get('canal_verificado')}), {f['url']}\n"
                          f"  transcrição: `{os.path.abspath(os.path.join(pasta, 'transcript.txt'))}` · falas com tempo: `{os.path.abspath(os.path.join(pasta, 'segments.json'))}`")
    trechos = []
    for t in cfg.get("trechos", []):
        vid = t["video"]
        segs = json.load(open(os.path.join(a.legendas, vid, "segments.json"), encoding="utf-8"))
        i0, i1 = tsec(t["inicio"]), tsec(t["fim"])
        falas = [s for s in segs if s["fim"] > i0 and s["ini"] < i1]
        linhas = "\n".join(f"    - {max(0, s['ini'] - i0):.1f}–{min(i1, s['fim']) - i0:.1f} s: {s['texto']}" for s in falas)
        trechos.append(f"- id `{t['id']}` · vídeo {vid} · {t['inicio']}–{t['fim']} ({i1 - i0:.1f} s) · cena sugerida: `{t.get('cena', '?')}` · mostra: {t.get('mostra', '')}\n{linhas}")
    au = cfg.get("aula", {}); ro = cfg.get("roteiro", {})
    g = lambda k: str(au.get(k) or ro.get(k) or PADRAO[k])
    ctx = au.get("contexto")  # ex.: curso/módulo/aula, pré-requisitos, aulas vizinhas (vem do curso-a-partir-de-ementa)
    ctx = "".join(f"- {x}\n" for x in (ctx if isinstance(ctx, list) else [ctx])) if ctx else ""
    docs = ro.get("documentacao") or au.get("documentacao") or []
    fontes += [f"- documentação oficial: {d['titulo']} — {d['url']}" + (f"\n  cópia local: `{d['arquivo']}`" if d.get("arquivo") else "")
               if isinstance(d, dict) else f"- documentação oficial: {d}" for d in docs]
    if a.selecao and os.path.exists(a.selecao):
        fontes.append("\n" + open(a.selecao, encoding="utf-8").read())
    out = (tpl.replace("{{SAIDA}}", os.path.abspath(a.saida)).replace("{{TEMA}}", au.get("tema", ""))
           .replace("{{PUBLICO}}", au.get("publico", "")).replace("{{OBJETIVO}}", au.get("objetivo", ""))
           .replace("{{NIVEL}}", g("nivel")).replace("{{TOM}}", g("tom")).replace("{{LINGUAGEM}}", g("linguagem"))
           .replace("{{ESTRUTURA}}", g("estrutura")).replace("{{FECHAMENTO}}", g("fechamento")).replace("{{CONTEXTO}}", ctx)
           .replace("{{TECNICO}}", secao_tecnica(cfg, a.config))
           .replace("{{DURACAO}}", str(ro.get("duracao_alvo", 90))).replace("{{PALAVRAS}}", str(ro.get("palavras_max", 200)))
           .replace("{{CENAS}}", str(ro.get("cenas", "5–8"))).replace("{{FONTES}}", "\n".join(fontes) or "(nenhuma)")
           .replace("{{TRECHOS}}", "\n".join(trechos) or "(nenhum)")
           .replace("{{VALIDADOR}}", os.path.join(HERE, "validate_roteiro.py")).replace("{{CONFIG}}", os.path.abspath(a.config))
           .replace("{{RETOMAR}}", a.retomar or "(rode o pipeline de novo)"))
    open(a.pedido, "w", encoding="utf-8").write(out)
    print("pedido:", a.pedido)


if __name__ == "__main__":
    main()
