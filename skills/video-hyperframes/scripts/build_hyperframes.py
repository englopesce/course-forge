#!/usr/bin/env python3
"""Gera o index.html de um projeto HyperFrames a partir de roteiro.json + timings.json.

Uso: python build_hyperframes.py roteiro.json timings.json projeto_hf/ [--tema tema.json]
        [--clips clips/clips.json]   # copia os MP4 para projeto_hf/assets/clips/ e os põe na linha do tempo
        [--formato 16x9|9x16]        # 9x16: template vertical próprio e clipes <id>_9x16.mp4 (FIT, tela cheia)
        [--codigo codigo/snippets.json]  # cenas com "codigo": painel de código realçado, linhas "digitadas" e destaques
Pré: projeto criado com `npx hyperframes init`; narracao.wav em projeto_hf/assets/; gsap.min.js em projeto_hf/.
Cada cena vira <section class="clip"> no tempo da fala; um trecho original entra logo depois
da fala da cena (clip_start/clip_end do timings.json), com o áudio próprio (data-has-audio).
"""
import argparse, html, json, os, re, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
PADRAO = {"fundo": "#0b1d3a", "fundo2": "#12305e", "texto": "#ffffff", "suave": "#b9c7e0",
          "destaque1": "#4285f4", "destaque2": "#34a853", "destaque3": "#fbbc04"}


def root_vars(tema):
    c = {**PADRAO, **(tema.get("cores") or {})}
    ft = tema.get("fonte_titulo") or "Poppins"; fx = tema.get("fonte_texto") or "Inter"
    return (f"--ground:{c['fundo']}; --ground2:{c['fundo2']}; --ink:{c['texto']}; --muted:{c['suave']}; "
            f"--accent2:{c['destaque1']}; --accent:{c['destaque2']}; --warn:{c['destaque3']}; "
            f"--font-display:\"{ft}\", \"{fx}\", sans-serif; --font-body:\"{fx}\", \"Noto Sans\", sans-serif;")


def esc_txt(t):
    """Escapa texto visível; "*" vira &#42; para "**/*.ts" não parecer comentário /* */ ao StaticGuard do HyperFrames."""
    return html.escape(t).replace("*", "&#42;")


def painel_codigo(sid, cod, vert, start, t_ini, t_fim):
    """HTML do painel de código + tweens: linhas entram uma a uma; depois cada destaque acende suas linhas
    (as outras escurecem) com a nota embaixo, dividindo o tempo restante da fala da cena."""
    n = len(cod["html"]); mx = max(10, cod.get("max_chars", 40))
    w, h = (880, 640) if vert else (1000, 600)
    fs = max(14, min(30, int(h / (1.5 * n)), int(w / (0.6 * mx + 3.9))))
    ids = [f"{sid}l{k}" for k in range(n)]
    linhas = "".join(f'<span class="ln" id="{ids[k]}"><i>{cod["inicio"] + k}</i>{hl.replace("*", "&#42;") or " "}</span>' for k, hl in enumerate(cod["html"]))
    notas = "".join(f'<div class="nota" id="{sid}n{j}">{j + 1}. {"linha " + str(d["de"]) if d["de"] == d["ate"] else f"linhas {d['de']}–{d['ate']}"}{": " + esc_txt(d["nota"]) if d.get("nota") else ""}</div>'
                    for j, d in enumerate(cod["destaques"]))
    h_ = (f'<div class="codepanel" id="{sid}cp"><div class="arq"><span>📄 {esc_txt(cod["titulo"])}</span>'
          f'<span>linhas {cod["inicio"]}–{cod["fim"]} · código testado</span></div>'
          f'<pre style="font-size:{fs}px">{linhas}</pre><div class="notas">{notas}</div></div>')
    tw = [f'      tl.fromTo("#{sid}cp", {{opacity: 0, y: 30}}, {{opacity: 1, y: 0, duration: 0.5, ease: "power2.out"}}, {start + 0.3:.3f});']
    step = min(0.08, 1.8 / max(1, n)); t0 = start + 0.6
    sel = lambda ks: ", ".join(f"#{ids[k]}" for k in ks)
    tw.append(f'      tl.fromTo("{sel(range(n))}", {{opacity: 0, x: -16}}, {{opacity: 1, x: 0, duration: 0.25, stagger: {step:.3f}, ease: "power1.out"}}, {t0:.3f});')
    dest = cod["destaques"]
    if dest:
        a = max(t0 + n * step + 0.4, t_ini + 1.0); b = max(a + 1.0 * len(dest), t_fim - 0.3)
        slot = (b - a) / len(dest)
        for j, d in enumerate(dest):
            tj = a + j * slot
            on = [k for k in range(n) if d["de"] <= cod["inicio"] + k <= d["ate"]]
            off = [k for k in range(n) if k not in on]
            if off: tw.append(f'      tl.to("{sel(off)}", {{opacity: 0.32, backgroundColor: "rgba(0,0,0,0)", duration: 0.3}}, {tj:.3f});')
            if on: tw.append(f'      tl.to("{sel(on)}", {{opacity: 1, backgroundColor: "rgba(251,188,4,0.18)", duration: 0.3}}, {tj:.3f});')
            tw.append(f'      tl.fromTo("#{sid}n{j}", {{opacity: 0}}, {{opacity: 1, duration: 0.3}}, {tj:.3f});')
            if j < len(dest) - 1: tw.append(f'      tl.to("#{sid}n{j}", {{opacity: 0, duration: 0.2}}, {tj + slot - 0.2:.3f});')
    return h_, tw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("roteiro"); ap.add_argument("timings"); ap.add_argument("projeto")
    ap.add_argument("--tema", default=""); ap.add_argument("--clips", default="")
    ap.add_argument("--formato", default="16x9", choices=["16x9", "9x16"])
    ap.add_argument("--template", default=""); ap.add_argument("--codigo", default="")
    a = ap.parse_args()
    vert = a.formato == "9x16"
    a.template = a.template or os.path.join(HERE, "..", "templates", "hyperframes_index_9x16.html" if vert else "hyperframes_index.html")
    rot = json.load(open(a.roteiro, encoding="utf-8"))
    tm = json.load(open(a.timings, encoding="utf-8"))
    tema = json.load(open(a.tema, encoding="utf-8")) if a.tema else {}
    codigo = json.load(open(a.codigo, encoding="utf-8")) if a.codigo and os.path.exists(a.codigo) else {}
    clips = {}
    if a.clips:
        os.makedirs(os.path.join(a.projeto, "assets", "clips"), exist_ok=True)
        for c in json.load(open(a.clips, encoding="utf-8")):
            if vert:
                if not c.get("arquivo_9x16"):
                    raise SystemExit(f"trecho {c['id']}: falta a versão 9x16 (rode a etapa de trechos com --formatos ...,9x16)")
                c = {**c, "arquivo": c["arquivo_9x16"]}
            shutil.copy2(os.path.join(os.path.dirname(a.clips), c["arquivo"]), os.path.join(a.projeto, "assets", "clips", c["arquivo"]))
            clips[c["id"]] = c
    total = tm["total"]; cenas = rot["cenas"]; f = rot["fonte"]
    esc = esc_txt
    scenes, tweens = [], []
    n = len(cenas)
    for k, (c, t) in enumerate(zip(cenas, tm["cenas"])):
        start = 0 if k == 0 else round(t["start"] - 0.2, 3)
        nxt = total if k == n - 1 else round(tm["cenas"][k + 1]["start"] - 0.2, 3)
        has_clip = "clip_start" in t and t.get("clip_id") in clips
        end = round(t["clip_start"] - 0.1, 3) if has_clip else nxt
        dur = round(end - start, 3)
        sid = f"s{k}"
        lis = "\n".join(
            f'          <li class="bullet" id="{sid}b{i}"><span class="num">{i+1}</span><span>{esc(b)}</span></li>'
            for i, b in enumerate(c["tela"]))
        extra = ""
        if k == n - 1:
            outras = []  # outras fontes: roteiro.fontes_extras + vídeos dos trechos (crédito também no fim)
            for cl in list(rot.get("fontes_extras", [])) + list(clips.values()):
                if cl["url"] != f["url"] and all(cl["url"] != o["url"] for o in outras): outras.append(cl)
            def curto(u):
                u = u or ""
                return re.sub(r"^https?://(www\.)?(youtube\.com/watch\?v=|youtu\.be/)", "youtu.be/", u)
            def eh_youtube(o):
                return bool(re.search(r"youtu(\.be|be\.com)", o.get("url") or ""))
            def linha(o, com_url=True):
                # fontes_extras pode ser lei/docs (sem canal), não só vídeo do YouTube
                titulo = esc(o.get("titulo_curto") or o.get("titulo") or "")
                url = esc(curto(o.get("url") or ""))
                canal = o.get("canal")
                if com_url and eh_youtube(o) and canal and url:
                    return f'{esc(canal)} · “{titulo}” · {url}'
                if canal:
                    return f'{esc(canal)} · “{titulo}”'
                return f'“{titulo}” · {url}' if (com_url and url) else f'“{titulo}”'
            gera = esc((rot.get("credito_geracao") or "").replace("https://github.com/englopesce/course-forge", "github.com/englopesce/course-forge"))
            if eh_youtube(f) and (not outras or all(eh_youtube(o) for o in outras)):
                final = ("Roteiro original em português, narrado por voz sintética"
                         + ("; trechos curtos dos vídeos originais usados com crédito, para treinamento interno." if clips else
                            "; nenhum trecho do vídeo original foi usado."))
            else:
                final = ("Roteiro original em português, a partir de documentos oficiais, narrado por voz sintética"
                         + ("; inclui trechos curtos de vídeo com crédito." if clips else
                            "; nenhum trecho de vídeo foi usado."))
            if gera:
                final += " " + gera
            if outras or not eh_youtube(f):
                so_docs = not eh_youtube(f) and all(not eh_youtube(o) for o in outras)
                rotulo = "Fontes (YouTube):" if eh_youtube(f) and outras and all(eh_youtube(o) for o in [f, *outras]) else "Fontes:"
                extra = (f'\n        <div class="endcredit compacto" id="{sid}cr">{rotulo}<br>{linha(f, com_url=not so_docs)}'
                         + "".join(f"<br>{linha(o, com_url=not so_docs)}" for o in outras) + f"<br>{final}</div>")
            else:
                extra = (f'\n        <div class="endcredit" id="{sid}cr">Baseado no vídeo “{esc(f["titulo"])}”, canal {esc(f["canal"])} '
                         f'(YouTube), {esc(f["url"])}.<br>{final}</div>')
        cod = codigo.get(c.get("id"))
        if cod:  # cena com código: texto (título + itens) e painel de código lado a lado (16:9) ou empilhados (9:16)
            painel, tw_cod = painel_codigo(sid, cod, vert, start, t["start"], end)
            scenes.append(
                f'      <section class="clip scene cena-codigo" id="{sid}" data-start="{start}" data-duration="{dur}" data-track-index="{1 + k % 2}">\n'
                f'        <div class="texto"><div class="kicker">Passo {k+1} de {n}</div>\n'
                f'        <h2 class="title" id="{sid}t">{esc(c["titulo"])}</h2>\n'
                f'        <ul class="bullets">\n{lis}\n        </ul>{extra}</div>\n        {painel}\n      </section>')
        else:
            tw_cod = []
            scenes.append(
                f'      <section class="clip scene" id="{sid}" data-start="{start}" data-duration="{dur}" data-track-index="{1 + k % 2}">\n'
                + (f'        <div class="icon">{esc(c.get("icone", ""))}</div>\n' if vert and c.get("icone") else "")
                + f'        <div class="kicker">Passo {k+1} de {n}</div>\n'
                f'        <h2 class="title" id="{sid}t">{esc(c["titulo"])}</h2>\n'
                f'        <ul class="bullets">\n{lis}\n        </ul>{extra}\n      </section>')
        tweens.extend(tw_cod)
        speak = max(1.5, t["end"] - t["start"])
        tweens.append(f'      tl.fromTo("#{sid}t", {{opacity: 0, y: 40}}, {{opacity: 1, y: 0, duration: 0.6, ease: "power3.out"}}, {start + 0.15:.3f});')
        nb = len(c["tela"])
        for i in range(nb):
            at = t["start"] + 0.5 + i * (speak * 0.8 / max(1, nb))
            tweens.append(f'      tl.fromTo("#{sid}b{i}", {{opacity: 0, x: -60}}, {{opacity: 1, x: 0, duration: 0.5, ease: "power2.out"}}, {at:.3f});')
        if extra:
            tweens.append(f'      tl.fromTo("#{sid}cr", {{opacity: 0}}, {{opacity: 1, duration: 0.6}}, {t["start"] + 1.0:.3f});')
        if k < n - 1:
            tweens.append(f'      tl.to("#{sid}", {{opacity: 0, duration: 0.3}}, {end - 0.3:.3f});')
        if has_clip:
            cl = clips[t["clip_id"]]
            cs = round(t["clip_start"] - 0.1, 3); cdur = round(nxt - cs, 3)
            vdur = round(min(cl["duracao"], t["clip_end"] - t["clip_start"]), 3)
            scenes.append(
                f'      <div class="clip trecho-tag" id="{sid}tag" data-start="{cs}" data-duration="{cdur}" data-track-index="3">'
                f'Exemplo no vídeo original</div>\n'
                f'      <video class="clip trecho-video" id="{sid}v" src="assets/clips/{esc(cl["arquivo"])}" data-start="{t["clip_start"]}" '
                f'data-duration="{vdur}" data-has-audio="true" data-volume="1" playsinline data-track-index="4"></video>')
            tweens.append(f'      tl.fromTo("#{sid}tag", {{opacity: 0}}, {{opacity: 1, duration: 0.3}}, {cs:.3f});')
    if re.search(r"youtu(\.be|be\.com)", f.get("url") or ""):
        credit = f'Fonte: {esc(f["canal"])} (YouTube) · “{esc(f.get("titulo_curto", f["titulo"]))}”'
    else:
        canal = f.get("canal") or ""
        tit = f.get("titulo_curto") or f.get("titulo") or ""
        credit = f'Fonte: {esc(canal)} · “{esc(tit)}”' if canal else f'Fonte: “{esc(tit)}”'
    avisos = [x for x in (rot.get("avisos") or []) if x]
    avisos_bar = esc(" · ".join(avisos))
    avisos_class = "com-avisos" if avisos else ""
    out = open(a.template, encoding="utf-8").read()
    out = (out.replace("{{ROOT_VARS}}", root_vars(tema)).replace("{{TOTAL}}", f"{total}").replace("{{SCENES}}", "\n".join(scenes))
           .replace("{{TWEENS}}", "\n".join(tweens)).replace("{{CREDIT_SHORT}}", credit)
           .replace("{{AVISOS_BAR}}", avisos_bar).replace("{{AVISOS_CLASS}}", avisos_class))
    open(os.path.join(a.projeto, "index.html"), "w", encoding="utf-8").write(out)
    print("ok:", os.path.join(a.projeto, "index.html"), f"{total}s, {n} cenas, {len(clips)} trecho(s), {sum(1 for c in cenas if c.get("id") in codigo)} cena(s) com código")


if __name__ == "__main__":
    main()
