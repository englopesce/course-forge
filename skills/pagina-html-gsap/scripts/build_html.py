#!/usr/bin/env python3
"""Gera a página HTML única (passo a passo, GSAP embutido) a partir de roteiro.json.

Uso: python build_html.py roteiro.json saida/aula.html [--gsap gsap.min.js] [--tema tema.json]
        [--clips clips/clips.json --clips-dir clips/] [--codigo codigo/snippets.json]
- Sem --gsap (ou arquivo ausente) carrega o GSAP da CDN; offline funciona sem animação.
- Com --clips, as cenas com "trecho" mostram o MP4 local (pasta irmã, caminho relativo
  --clips-dir), legenda pt-BR embutida (Blob, funciona em file://), crédito e link com tempo.
  Os MP4 NÃO são embutidos no HTML (ficariam pesados); copie a pasta clips/ junto.
- Com --codigo (etapa "codigo", skill codigo-exemplo-aula), as cenas com "codigo" mostram o código do
  repositório de exemplo com números de linha, realce de sintaxe e botões de destaque; `exercicios` do
  roteiro viram a seção "Exercícios práticos" (com o comando de conferência de codigo/checagem.json).
tema.json: {"cores": {"fundo","fundo2","texto","suave","destaque1","destaque2","destaque3"},
            "fonte_titulo": "Poppins", "fonte_texto": "Inter"}
"""
import argparse, html, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
REALCE_CSS = (".tk-kw{color:#c792ea}.tk-str{color:#c3e88d}.tk-com{color:#7f8ca3;font-style:italic}.tk-num{color:#f78c6c}"
              ".tk-fn{color:#82aaff}.tk-typ{color:#ffcb6b}.tk-key{color:#89ddff}.tk-punct{color:#a6accd}")
CDN = "https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"
PADRAO = {"cores": {"fundo": "#0b1d3a", "fundo2": "#12305e", "texto": "#ffffff", "suave": "#b9c7e0",
                    "destaque1": "#4285f4", "destaque2": "#34a853", "destaque3": "#fbbc04"},
          "fonte_titulo": "Poppins", "fonte_texto": "Inter"}


def root_vars(tema):
    c = {**PADRAO["cores"], **(tema.get("cores") or {})}
    ft = tema.get("fonte_titulo") or PADRAO["fonte_titulo"]; fx = tema.get("fonte_texto") or PADRAO["fonte_texto"]
    return (f"--bg:{c['fundo']}; --bg2:{c['fundo2']}; --ink:{c['texto']}; --muted:{c['suave']}; "
            f"--a1:{c['destaque1']}; --a2:{c['destaque2']}; --a3:{c['destaque3']}; "
            f"--font-display:\"{ft}\", \"{fx}\", sans-serif; --font-body:\"{fx}\", \"Segoe UI\", \"Noto Sans\", Roboto, Arial, sans-serif;")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("roteiro"); ap.add_argument("saida")
    ap.add_argument("--gsap", default=""); ap.add_argument("--tema", default="")
    ap.add_argument("--clips", default=""); ap.add_argument("--clips-dir", default="clips/")
    ap.add_argument("--codigo", default="")
    ap.add_argument("--template", default=os.path.join(HERE, "..", "templates", "aula_template.html"))
    a = ap.parse_args()
    rot = json.load(open(a.roteiro, encoding="utf-8"))
    tema = json.load(open(a.tema, encoding="utf-8")) if a.tema else {}
    tpl = open(a.template, encoding="utf-8").read()
    gs = open(a.gsap, encoding="utf-8").read() if a.gsap and os.path.exists(a.gsap) else f'document.write(\'<script src="{CDN}"><\\/script>\');'
    clips = {}
    if a.clips:
        base = os.path.dirname(a.clips)
        for c in json.load(open(a.clips, encoding="utf-8")):
            if c.get("vtt"):
                c["vtt_text"] = open(os.path.join(base, c["vtt"]), encoding="utf-8").read()
            clips[c["id"]] = c
    codigo = json.load(open(a.codigo, encoding="utf-8")) if a.codigo and os.path.exists(a.codigo) else {}
    chk_p = os.path.join(os.path.dirname(a.codigo), "checagem.json") if a.codigo else ""
    checagem = json.load(open(chk_p, encoding="utf-8")) if chk_p and os.path.exists(chk_p) else {}
    checagem = {"comandos": [{k: c[k] for k in ("nome", "cmd", "ok")} for c in checagem.get("comandos", [])]}
    js = lambda o: json.dumps(o, ensure_ascii=False).replace("</", "<\\/")
    out = (tpl.replace("{{GSAP}}", gs.replace("</script", "<\\/script"))
              .replace("{{DATA_JSON}}", js(rot)).replace("{{CLIPS_JSON}}", js(clips))
              .replace("{{CODIGO_JSON}}", js(codigo)).replace("{{CHECAGEM_JSON}}", js(checagem)).replace("{{REALCE_CSS}}", REALCE_CSS)
              .replace("{{CLIPS_DIR}}", js(a.clips_dir.rstrip("/") + "/"))
              .replace("{{ROOT_VARS}}", root_vars(tema))
              .replace("{{TITULO}}", html.escape(rot["titulo"]))
              .replace("{{SUBTITULO}}", html.escape(rot.get("subtitulo", ""))))
    os.makedirs(os.path.dirname(os.path.abspath(a.saida)), exist_ok=True)
    open(a.saida, "w", encoding="utf-8").write(out)
    print("ok:", a.saida, f"{len(out)//1024} KB, GSAP {'embutido' if 'GreenSock' in gs else 'via CDN'}, {len(clips)} trecho(s), {len(codigo)} cena(s) com código")


if __name__ == "__main__":
    main()
