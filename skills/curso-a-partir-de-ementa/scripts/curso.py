#!/usr/bin/env python3
"""curso-a-partir-de-ementa: ementa (texto) -> estrutura de curso (módulos -> aulas) -> um aula.yaml por aula -> pipeline aula-ra.

Uso:
  python curso.py estrutura curso.yaml [--force]      # ementa.json; pedido ao agente (código 10) ou valida estrutura.json
                                                      # e gera CURSO.md, curso.json e aulas/<id>.yaml
  python curso.py aulas curso.yaml --ids m01-a03,m03-a05 [--from X --to Y --stage S --force]
                                                      # roda o pipeline aula-ra das aulas escolhidas, em sequência
  python curso.py aulas curso.yaml --tipo codigo | --modulo m03   # seleção por tipo/módulo
  python curso.py status curso.yaml                   # o que já existe de cada aula (roteiro, MP4, HTML, WER, código)
                                                      # e os tokens de LLM (uso-tokens.json de cada aula + do curso), somados

A parte de julgamento (dividir a ementa em aulas, objetivos, tipo, duração) é do agente: o script escreve
PEDIDO_ESTRUTURA.md (de templates/prompt_estrutura.md) e para com código 10 até existir estrutura.json; então
valida (esquema + cobertura de TODOS os itens da ementa) e gera o resto. Ajustes por aula (vídeos, trechos,
repositório de exemplo, termos de checagem, documentação) ficam em aulas/<id>.extra.yaml — nunca sobrescritos.
Cache: <saida>/.cache/estrutura.json (hash de ementa, curso.yaml, estrutura.json, extras, templates e scripts).
"""
import argparse, copy, glob, hashlib, json, os, re, subprocess, sys, time

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ementa import parse as parse_ementa  # noqa: E402

TIPOS = {"conceitual", "codigo", "ferramenta", "pratica", "projeto", "carreira"}
CODIGO_PARAR = 10


def log(m):
    print(f"[curso {time.strftime('%H:%M:%S')}] {m}", flush=True)


def merge(a, b):
    """Mescla b em a (dicts recursivos; listas e valores de b substituem)."""
    out = copy.deepcopy(a)
    for k, v in (b or {}).items():
        out[k] = merge(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else copy.deepcopy(v)
    return out


class Curso:
    def __init__(self, cfg_path, force=False):
        self.cfg_path = os.path.abspath(cfg_path)
        self.cfg = yaml.safe_load(open(cfg_path, encoding="utf-8"))
        self.base = os.path.dirname(self.cfg_path)
        self.rel = lambda p: p if os.path.isabs(p) else os.path.normpath(os.path.join(self.base, p))
        self.out = self.rel(self.cfg.get("saida", "."))
        self.c = self.cfg["curso"]
        self.ementa_txt = self.rel(self.c["ementa"])
        self.skills = os.environ.get("AULA_SKILLS_DIR") or (self.rel(self.cfg["skills_dir"]) if self.cfg.get("skills_dir")
                                                             else os.path.normpath(os.path.join(HERE, "..", "..")))
        self.force = force
        self.p = {k: os.path.join(self.out, v) for k, v in {
            "ementa": "ementa.json", "estrutura": "estrutura.json", "pedido": "PEDIDO_ESTRUTURA.md", "md": "CURSO.md",
            "json": "curso.json", "aulas": "aulas", "cache": ".cache", "status": "status.json"}.items()}
        for d in (self.out, self.p["aulas"], self.p["cache"]): os.makedirs(d, exist_ok=True)

    # ---------- ementa ----------
    def ementa(self):
        e = parse_ementa(open(self.ementa_txt, encoding="utf-8").read())
        e["arquivo"] = self.ementa_txt
        json.dump(e, open(self.p["ementa"], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        log(f"ementa: {len(e['modulos'])} módulos, {sum(len(m['itens']) for m in e['modulos'])} itens -> {self.p['ementa']}")
        return e

    # ---------- pedido ao agente ----------
    def pedido(self, e):
        tpl = open(os.path.join(HERE, "..", "templates", "prompt_estrutura.md"), encoding="utf-8").read()
        est = self.cfg.get("estrutura", {})
        resumo = []
        for m in e["modulos"]:
            resumo.append(f"- **{m['id']} — {m['titulo']}**: {len(m['itens'])} itens" +
                          (f", {len(m['unidades'])} unidades" if m["unidades"] else ""))
        regras = "\n".join(f"- {r}" for r in est.get("regras", []))
        val = f"{sys.executable} {os.path.abspath(__file__)} estrutura {self.cfg_path}"
        s = (tpl.replace("{{SAIDA}}", self.p["estrutura"]).replace("{{EMENTA_TXT}}", self.ementa_txt)
             .replace("{{EMENTA_JSON}}", self.p["ementa"]).replace("{{TITULO}}", self.c.get("titulo", e["titulo"]))
             .replace("{{PUBLICO}}", self.c.get("publico", "")).replace("{{NIVEL}}", self.c.get("nivel", ""))
             .replace("{{TOM}}", self.c.get("tom", "")).replace("{{OBJETIVO}}", self.c.get("objetivo", ""))
             .replace("{{AULAS_POR_MODULO}}", str(est.get("aulas_por_modulo", "3 a 8")))
             .replace("{{DURACAO_VIDEO}}", str(est.get("duracao_video_s", "90 a 150")))
             .replace("{{MODULOS}}", "\n".join(resumo)).replace("{{REGRAS}}", regras or "- (nenhuma além das acima)")
             .replace("{{ESQUEMA}}", os.path.normpath(os.path.join(HERE, "..", "references", "schema-estrutura.md")))
             .replace("{{VALIDAR}}", val))
        open(self.p["pedido"], "w", encoding="utf-8").write(s)

    # ---------- validação ----------
    def validar(self, e, est):
        err, warn = [], []
        itens = {i["id"]: i for m in e["modulos"] for i in m["itens"]}
        unis = {u["id"] for m in e["modulos"] for u in m["unidades"]}
        mods_em = {m["id"] for m in e["modulos"]}
        cobertos, ids, total_s = set(), set(), 0
        mods = est.get("modulos", [])
        if {m.get("id") for m in mods} != mods_em:
            err.append(f"módulos da estrutura {sorted(m.get('id') for m in mods)} ≠ ementa {sorted(mods_em)}")
        for m in mods:
            if not m.get("titulo"): err.append(f"{m.get('id')}: sem título")
            if not m.get("aulas"): err.append(f"{m.get('id')}: sem aulas")
            for k, a in enumerate(m.get("aulas", []), 1):
                tag = f"{m.get('id')}/aula {k}"
                if not re.fullmatch(r"[a-z0-9-]{3,48}", a.get("slug", "")): err.append(f"{tag}: slug inválido (kebab-case, 3–48)")
                aid = f"{m.get('id')}-a{k:02d}"
                if aid in ids: err.append(f"{tag}: id repetido")
                ids.add(aid)
                for f_ in ("titulo", "objetivos", "tipo", "duracao_video_s", "topicos"):
                    if not a.get(f_): err.append(f"{tag}: falta '{f_}'")
                if a.get("tipo") and a["tipo"] not in TIPOS: err.append(f"{tag}: tipo '{a['tipo']}' (use {sorted(TIPOS)})")
                ob = a.get("objetivos") or []
                if not 1 <= len(ob) <= 4: warn.append(f"{tag}: {len(ob)} objetivos (ideal 1–3)")
                d = a.get("duracao_video_s") or 0
                if not 45 <= d <= 300: warn.append(f"{tag}: duracao_video_s={d} (aulas rápidas: 60–180)")
                total_s += d
                for t in a.get("topicos", []):
                    if t in itens: cobertos.add(t)
                    elif t in unis: cobertos.update(i for i, x in itens.items() if x.get("unidade") == t)
                    else: err.append(f"{tag}: tópico '{t}' não existe na ementa")
                    if t in itens and not t.startswith(m.get("id", "") + "."): warn.append(f"{tag}: tópico {t} é de outro módulo")
        # um item conta como coberto se ele ou um ancestral foi citado
        def coberto(i):
            while i:
                if i in cobertos: return True
                i = itens[i].get("pai")
            return False
        # pais sem cobertura direta contam se todos os filhos foram cobertos
        filhos = {}
        for i, x in itens.items():
            if x.get("pai"): filhos.setdefault(x["pai"], []).append(i)
        falta = [i for i in itens if not coberto(i) and not (i in filhos and all(coberto(f) for f in filhos[i]))]
        modo = self.cfg.get("estrutura", {}).get("cobertura", "erro")
        if falta:
            msg = "itens da ementa sem aula: " + ", ".join(f"{i} ({itens[i]['texto'][:50]})" for i in falta[:25]) + (" ..." if len(falta) > 25 else "")
            (err if modo == "erro" else warn).append(msg)
        return err, warn, {"aulas": len(ids), "itens": len(itens), "cobertos": len(itens) - len(falta), "video_total_s": total_s}

    # ---------- geração ----------
    def aulas_lista(self, est):
        lst = []
        for mi, m in enumerate(est["modulos"]):
            for k, a in enumerate(m["aulas"], 1):
                aid = f"{m['id']}-a{k:02d}"
                lst.append({**a, "id": aid, "n": k, "modulo": m["id"], "modulo_titulo": m["titulo"], "modulo_slug": m.get("slug") or m["id"],
                            "total_modulo": len(m["aulas"]), "dir": f"{m['id']}-{m.get('slug', '')}".rstrip("-") + f"/{aid}-{a['slug']}"})
        for i, a in enumerate(lst):  # vizinhas (contexto para o roteiro)
            a["anterior"] = lst[i - 1]["titulo"] if i and lst[i - 1]["modulo"] == a["modulo"] else None
            a["proxima"] = lst[i + 1]["titulo"] if i + 1 < len(lst) and lst[i + 1]["modulo"] == a["modulo"] else None
        return lst

    def aula_yaml(self, a, e, est):
        itens = {i["id"]: i for m in e["modulos"] for i in m["itens"]}
        c = self.c
        pad = merge(self.cfg.get("padrao_aula", {}), (self.cfg.get("por_tipo") or {}).get(a["tipo"], {}))
        d = a["duracao_video_s"]
        topicos = [itens[t]["texto"] if t in itens else t for t in a["topicos"]]
        ctx = [f"Curso: {c.get('titulo', est.get('curso', {}).get('titulo', ''))} — módulo {a['modulo'][1:]} ({a['modulo_titulo']}), aula {a['n']} de {a['total_modulo']}",
               "Tópicos da ementa cobertos: " + "; ".join(topicos)]
        if a.get("anterior"): ctx.append(f"Aula anterior (já vista): {a['anterior']}")
        if a.get("proxima"): ctx.append(f"Próxima aula (não antecipe): {a['proxima']}")
        if a.get("pre_requisitos"): ctx.append("Pré-requisitos: " + "; ".join(a["pre_requisitos"]))
        gerado = {
            "aula": {"slug": f"{a['id']}-{a['slug']}", "tema": a["titulo"], "objetivo": " ".join(f"({i}) {o}" for i, o in enumerate(a["objetivos"], 1)),
                     "publico": c.get("publico", ""), "nivel": c.get("nivel", ""), "tom": c.get("tom", ""), "linguagem": c.get("linguagem", ""),
                     "tipo": a["tipo"], "contexto": ctx, "curso_id": a["id"]},
            "saida": os.path.relpath(os.path.join(self.out, a["dir"]), self.p["aulas"]),
            "trabalho": os.path.relpath(os.path.join(self.out, "_trabalho", a["id"]), self.p["aulas"]),
            "skills_dir": self.skills,
            "roteiro": {"duracao_alvo": d, "palavras_max": int(round(d * 0.85 * 2.4 / 10) * 10)},
        }
        cv = self.cfg.get("cache_videos", "_cache/videos")  # transcrições compartilhadas entre aulas (id do vídeo + versão)
        if cv: gerado["cache_videos"] = os.path.relpath(os.path.join(self.out, cv), self.p["aulas"])
        y = merge(merge(pad, gerado), {})
        if a.get("busca_videos"): y["_busca_videos"] = a["busca_videos"]
        if a.get("documentacao"): y.setdefault("roteiro", {})["documentacao"] = a["documentacao"]
        ex_dir = os.path.join(self.out, "exemplos", a["id"])
        if os.path.isdir(ex_dir): y["exemplo"] = {"dir": os.path.relpath(ex_dir, self.p["aulas"])}
        extra_p = os.path.join(self.p["aulas"], f"{a['id']}.extra.yaml")
        if os.path.exists(extra_p): y = merge(y, yaml.safe_load(open(extra_p, encoding="utf-8")) or {})
        return y, os.path.exists(extra_p)

    def curso_md(self, e, est, lst, stats):
        c = self.c; L = []
        L += [f"# {c.get('titulo', est.get('curso', {}).get('titulo', ''))}", ""]
        if est.get("curso", {}).get("resumo"): L += [est["curso"]["resumo"], ""]
        L += [f"- **Público:** {c.get('publico', '')}", f"- **Nível:** {c.get('nivel', '')}", f"- **Tom:** {c.get('tom', '')}",
              f"- **Ementa:** `{self.ementa_txt}` ({stats['itens']} itens; {stats['cobertos']} cobertos pelas aulas)",
              f"- **Tamanho:** {len(est['modulos'])} módulos, {stats['aulas']} aulas, {stats['video_total_s'] / 60:.0f} min de vídeo + "
              f"{sum(a.get('duracao_estudo_min', 0) for a in lst) / 60:.1f} h de prática/estudo estimadas", ""]
        avisos = [a for a in lst if a.get("aviso_duplicacao")]
        if avisos:  # defeitos da ementa ficam registrados, não "corrigidos" (campo aviso_duplicacao no .extra.yaml)
            L += ["**Avisos da ementa:**"] + [f"- {a['id']} — {a['aviso_duplicacao']}" for a in avisos] + [""]
        if est.get("curso", {}).get("pre_requisitos"):
            L += ["**Pré-requisitos do curso:** " + "; ".join(est["curso"]["pre_requisitos"]), ""]
        itens = {i["id"]: i for m in e["modulos"] for i in m["itens"]}
        for m in est["modulos"]:
            ms = [a for a in lst if a["modulo"] == m["id"]]
            L += [f"## {m['id'][1:].lstrip('0')}. {m['titulo']}", ""]
            if m.get("objetivo"): L += [f"*{m['objetivo']}*", ""]
            L += [f"{len(ms)} aulas · {sum(a['duracao_video_s'] for a in ms) / 60:.1f} min de vídeo · "
                  f"{sum(a.get('duracao_estudo_min', 0) for a in ms)} min de prática/estudo", "",
                  "| Aula | Título | Tipo | Vídeo | Prática | Objetivos |", "|---|---|---|---|---|---|"]
            for a in ms:
                L.append(f"| {a['id']} | {a['titulo']} | {a['tipo']} | {a['duracao_video_s'] // 60}:{a['duracao_video_s'] % 60:02d} | "
                         f"{a.get('duracao_estudo_min', 0)} min | " + "<br>".join(a["objetivos"]) + " |")
            L += [""]
            for a in ms:
                tps = [itens[t]["texto"] if t in itens else t for t in a["topicos"]]
                L += [f"<details><summary>{a['id']} — tópicos da ementa e prática</summary>", "",
                      *(f"- {t}" for t in tps)]
                if a.get("pratica"): L += ["", f"**Prática:** {a['pratica']}"]
                if a.get("aviso_duplicacao"): L += ["", f"> ⚠️ **Aviso da ementa (não corrigido):** {a['aviso_duplicacao']}"]
                L += ["", f"Config: `aulas/{a['id']}.yaml` · saída: `{a['dir']}/`", "", "</details>", ""]
        open(self.p["md"], "w", encoding="utf-8").write("\n".join(L))

    def estrutura(self):
        e = self.ementa()
        if not os.path.exists(self.p["estrutura"]):
            self.pedido(e)
            log("ETAPA DO AGENTE: escreva a estrutura do curso.")
            print(f"  Pedido: {self.p['pedido']}\n  Ementa estruturada: {self.p['ementa']}\n  Escreva em: {self.p['estrutura']}\n"
                  f"  Depois rode de novo: {sys.executable} {os.path.abspath(__file__)} estrutura {self.cfg_path}")
            sys.exit(CODIGO_PARAR)
        est = json.load(open(self.p["estrutura"], encoding="utf-8"))
        err, warn, stats = self.validar(e, est)
        for w in warn: print("AVISO:", w)
        for x in err: print("ERRO:", x)
        if err: sys.exit(1)
        h = hashlib.sha256()
        for f in [self.p["ementa"], self.cfg_path, self.p["estrutura"]] + sorted(glob.glob(os.path.join(self.p["aulas"], "*.extra.yaml"))) \
                + sorted(glob.glob(os.path.join(HERE, "*.py"))) + sorted(glob.glob(os.path.join(HERE, "..", "templates", "*"))):
            h.update(f.encode()); h.update(open(f, "rb").read())
        h.update(json.dumps(sorted(os.listdir(os.path.join(self.out, "exemplos"))) if os.path.isdir(os.path.join(self.out, "exemplos")) else []).encode())
        key = h.hexdigest(); cf = os.path.join(self.p["cache"], "estrutura.json")
        lst = self.aulas_lista(est)
        outs = [self.p["md"], self.p["json"]] + [os.path.join(self.p["aulas"], f"{a['id']}.yaml") for a in lst]
        if not self.force and os.path.exists(cf) and json.load(open(cf))["hash"] == key and all(map(os.path.exists, outs)):
            log(f"estrutura: sem mudança ({stats['aulas']} aulas), pulando")
            return lst
        for a in lst:
            y, tem_extra = self.aula_yaml(a, e, est)
            p = os.path.join(self.p["aulas"], f"{a['id']}.yaml")
            cab = (f"# GERADO por curso-a-partir-de-ementa ({open(os.path.join(HERE, 'VERSION')).read().strip()}) a partir de estrutura.json.\n"
                   f"# NÃO edite: ajustes desta aula vão em {a['id']}.extra.yaml (mesclado por cima; listas substituem).\n")
            ordem = ["aula", "saida", "trabalho", "skills_dir", "cache_videos", "videos", "trechos", "exemplo", "formatos", "roteiro", "narracao"]
            y = {**{k: y[k] for k in ordem if k in y}, **{k: v for k, v in y.items() if k not in ordem}}
            open(p, "w", encoding="utf-8").write(cab + yaml.safe_dump(y, allow_unicode=True, sort_keys=False, width=140))
            a["yaml"] = os.path.relpath(p, self.out); a["extra"] = tem_extra
            if y.get("aviso_duplicacao"): a["aviso_duplicacao"] = y["aviso_duplicacao"]
        self.curso_md(e, est, lst, stats)
        json.dump({"curso": {**self.c, **est.get("curso", {})}, "stats": stats, "aulas": lst}, open(self.p["json"], "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        self.registrar_estrutura(cf)
        json.dump({"hash": key, "quando": time.strftime("%Y-%m-%d %H:%M:%S"), "estrutura_sha": self.sha(self.p["estrutura"])}, open(cf, "w"))
        log(f"estrutura: {stats['aulas']} aulas em {len(est['modulos'])} módulos; cobertura {stats['cobertos']}/{stats['itens']} itens; "
            f"{stats['video_total_s'] / 60:.0f} min de vídeo -> {self.p['md']}, {self.p['aulas']}/")
        return lst

    @staticmethod
    def sha(p):
        return hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.exists(p) else None

    def uso(self):
        sys.path.insert(0, os.path.join(self.skills, "aula-ra", "scripts"))
        import uso_tokens
        return uso_tokens

    def registrar_estrutura(self, cf):
        """Etapa de LLM do curso (estrutura.json escrita pelo agente): estimada com tokenizer, 1 vez por estrutura nova."""
        ant = json.load(open(cf)) if os.path.exists(cf) else {}
        if ant.get("estrutura_sha") == self.sha(self.p["estrutura"]): return
        try:
            schema = os.path.join(HERE, "..", "references", "schema-estrutura.md")
            self.uso().estimar(self.out, "estrutura", [self.p["pedido"], self.p["ementa"], schema], self.p["estrutura"],
                               detalhes={"origem": "estrutura do curso (agente)"})
        except Exception as e:
            log(f"AVISO: não registrou tokens da estrutura ({e})")

    # ---------- execução ----------
    def selecionar(self, lst, ids=None, tipo=None, modulo=None):
        sel = lst
        if ids: sel = [a for a in lst if a["id"] in ids or a["slug"] in ids]
        if tipo: sel = [a for a in sel if a["tipo"] == tipo]
        if modulo: sel = [a for a in sel if a["modulo"] == modulo]
        if ids:
            faltam = set(ids) - {a["id"] for a in sel} - {a["slug"] for a in sel}
            if faltam: raise SystemExit(f"aulas não encontradas: {sorted(faltam)}")
        return sel

    def aulas(self, sel, passa):
        pipe = os.path.join(self.skills, "aula-ra", "scripts", "pipeline.py")
        res = {}
        for a in sel:
            y = os.path.join(self.p["aulas"], f"{a['id']}.yaml")
            cfg = yaml.safe_load(open(y, encoding="utf-8"))
            if not cfg.get("videos"):
                res[a["id"]] = {"estado": "precisa_videos", "codigo": CODIGO_PARAR}
                print(f"\n== {a['id']}: ETAPA DO AGENTE — escolha vídeos (canal oficial/confiável, verificado via oEmbed) e ponha em "
                      f"aulas/{a['id']}.extra.yaml (videos, trechos, exemplo...). Busca sugerida: {cfg.get('_busca_videos', a['titulo'])}")
                continue
            log(f"== {a['id']} {a['titulo']}")
            lg = os.path.join(self.out, "_trabalho", a["id"]); os.makedirs(lg, exist_ok=True)
            with open(os.path.join(lg, "pipeline.log"), "a", encoding="utf-8") as fh:
                p = subprocess.Popen([sys.executable, pipe, y] + passa, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                for linha in p.stdout:
                    sys.stdout.write(linha); fh.write(linha)
                rc = p.wait()
            res[a["id"]] = {"estado": {0: "ok", CODIGO_PARAR: "precisa_roteiro"}.get(rc, "erro"), "codigo": rc}
        st = json.load(open(self.p["status"])) if os.path.exists(self.p["status"]) else {}
        st.update({k: {**v, "quando": time.strftime("%Y-%m-%d %H:%M:%S")} for k, v in res.items()})
        json.dump(st, open(self.p["status"], "w"), ensure_ascii=False, indent=1)
        print("\nresumo:", ", ".join(f"{k}={v['estado']}" for k, v in res.items()))
        return max([v["codigo"] for v in res.values()] + [0])

    def status(self, lst):
        print(f"{'aula':9s} {'tipo':10s} {'yaml':4s} {'extra':5s} {'roteiro':7s} {'html':4s} {'16x9':5s} {'9x16':5s} {'WER':6s} {'código':7s} "
              f"{'tok.ent':>8s} {'tok.sai':>8s} {'evit.':>7s} título")
        U = self.uso(); tot = {"entrada": 0, "saida": 0, "evitados": 0, "chamadas": 0, "do_cache": 0, "estimados": 0}; n_aulas = 0
        for a in lst:
            y = os.path.join(self.p["aulas"], f"{a['id']}.yaml")
            cfg = yaml.safe_load(open(y, encoding="utf-8")) if os.path.exists(y) else {}
            out = os.path.normpath(os.path.join(self.p["aulas"], cfg.get("saida", ""))) if cfg else ""
            ex = lambda f: "sim" if out and os.path.exists(os.path.join(out, f)) else "-"
            wer, cod = "-", "-"
            vj = os.path.join(out, "verificacao.json") if out else ""
            if vj and os.path.exists(vj):
                v = json.load(open(vj, encoding="utf-8"))
                wer = f"{v.get('voz_mp4', {}).get('wer', 0) * 100:.1f}%" if v.get("voz_mp4", {}).get("wer") is not None else "?"
                cod = {True: "rodou", False: "FALHOU", None: "-"}[v.get("codigo", {}).get("ok")] if v.get("codigo") else "-"
            t = U.somar(U.carregar(out)["registros"]) if out and os.path.exists(os.path.join(out, U.ARQ)) else None
            if t:
                n_aulas += 1
                for k in tot: tot[k] += t[k]
            te, ts_, tv = (f"{t['entrada']}", f"{t['saida']}", f"{t['evitados']}") if t else ("-", "-", "-")
            print(f"{a['id']:9s} {a['tipo']:10s} {'sim' if cfg else '-':4s} {'sim' if os.path.exists(y.replace('.yaml', '.extra.yaml')) else '-':5s} "
                  f"{ex('roteiro.json'):7s} {ex('aula.html'):4s} {ex('aula.mp4'):5s} {ex('aula-9x16.mp4'):5s} {wer:6s} {cod:7s} "
                  f"{te:>8s} {ts_:>8s} {tv:>7s} {'⚠dup ' if cfg.get('aviso_duplicacao') else ''}{a['titulo'][:50]}")
        dups = [a["id"] for a in lst if a.get("aviso_duplicacao")]
        if dups: print("\n⚠dup = aviso de duplicação na ementa (não corrigida): " + ", ".join(dups))
        cur = U.somar(U.carregar(self.out)["registros"]) if os.path.exists(os.path.join(self.out, U.ARQ)) else None
        print(f"\ntokens de LLM — {n_aulas} aula(s) com uso-tokens.json: entrada {tot['entrada']}, saída {tot['saida']}, "
              f"{tot['chamadas']} rodada(s) ({tot['estimados']} estimada(s)), {tot['do_cache']} do cache, {tot['evitados']} evitados pelo cache")
        if cur:
            print(f"curso (estrutura): entrada {cur['entrada']}, saída {cur['saida']} ({cur['estimados']} estimada(s))")
            tot["entrada"] += cur["entrada"]; tot["saida"] += cur["saida"]
        print(f"TOTAL: entrada {tot['entrada']} + saída {tot['saida']} = {tot['entrada'] + tot['saida']} tokens "
              "(estimados com tiktoken o200k_base quando a etapa é do agente; reais quando vierem de API)")
        return tot

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("comando", choices=["estrutura", "aulas", "status"]); ap.add_argument("config")
    ap.add_argument("--ids", default=""); ap.add_argument("--tipo"); ap.add_argument("--modulo")
    ap.add_argument("--force", action="store_true", help="estrutura: regera; aulas: repassa --force ao pipeline")
    ap.add_argument("--stage"); ap.add_argument("--from", dest="frm"); ap.add_argument("--to")
    ap.add_argument("--refazer-pedido", action="store_true", help="aulas: repassa ao pipeline (mede o roteiro sem cache)")
    ap.add_argument("--manter-roteiro", action="store_true", help="aulas: repassa ao pipeline")
    ap.add_argument("--selecao-modo", choices=["bm25", "completo"], help="aulas: repassa ao pipeline")
    a = ap.parse_args()
    c = Curso(a.config, force=a.force and a.comando == "estrutura")
    lst = c.estrutura()
    if a.comando == "estrutura": return
    if a.comando == "status": return c.status(lst)
    ids = [x.strip() for x in a.ids.split(",") if x.strip()]
    if not (ids or a.tipo or a.modulo): raise SystemExit("escolha as aulas: --ids, --tipo ou --modulo")
    passa = (["--force"] if a.force else []) + (["--stage", a.stage] if a.stage else []) + \
            (["--from", a.frm] if a.frm else []) + (["--to", a.to] if a.to else []) + \
            (["--refazer-pedido"] if a.refazer_pedido else []) + (["--manter-roteiro"] if a.manter_roteiro else []) + \
            (["--selecao-modo", a.selecao_modo] if a.selecao_modo else [])
    sys.exit(c.aulas(c.selecionar(lst, ids, a.tipo, a.modulo), passa))


if __name__ == "__main__":
    main()
