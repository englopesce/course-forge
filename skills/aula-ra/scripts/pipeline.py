#!/usr/bin/env python3
"""Pipeline aula-ra: config da aula (YAML) -> legendas -> roteiro -> código -> narração -> trechos -> HTML -> MP4 -> verificação.

Uso:
  python pipeline.py aula.yaml                    # roda tudo (pula etapas sem mudança)
  python pipeline.py aula.yaml --stage narracao   # só uma etapa
  python pipeline.py aula.yaml --from trechos --to video
  python pipeline.py aula.yaml --force [--stage html]   # refaz mesmo sem mudança
  python pipeline.py aula.yaml --list             # mostra etapas e estado do cache

Cache: cada etapa guarda em <trabalho>/.cache/<etapa>.json o hash das entradas (trecho da config,
arquivos de entrada e os próprios scripts da etapa). Sem mudança e com as saídas presentes -> pula.
A etapa "roteiro" depende do agente: se roteiro.json não existir, o pipeline escreve o pedido
(PEDIDO_ROTEIRO.md), diz quais arquivos usar e para com código 10. Escreva o roteiro e rode de novo.

Economia de tokens (v1.4.0): o pedido de roteiro leva só as janelas relevantes das transcrições (BM25, limite em
`roteiro.selecao.max_tokens`); o roteiro só é refeito quando muda o hash da entrada (trechos selecionados + config
relevante + prompt/esquema + versão da skill) — se mudar, para com código 10 (ou --manter-roteiro); tokens de cada
etapa de LLM vão para <saida>/uso-tokens.json (uso_tokens.py: real se vier de API, senão estimado com tiktoken);
`cache_videos: <dir>` compartilha transcrições entre aulas (por id do vídeo e versão da skill de legendas).

Etapa "codigo" (aulas técnicas, skill codigo-exemplo-aula): se a config tiver `exemplo` ou o roteiro tiver
cenas com `codigo`/`exercicios`, roda os comandos de `exemplo.checagem` numa cópia limpa do repositório de
exemplo (ex.: npm install, build, teste com cliente MCP), extrai o código citado pelas cenas (realçado) e gera
exercicios.md; falha se algo não rodar. Sem nada disso, a etapa é pulada.

Formatos de vídeo: `formatos: [16x9, 9x16]` na config (padrão só 16x9). 16x9 -> aula.mp4 (1920x1080);
9x16 -> aula-9x16.mp4 (1080x1920, layout vertical próprio; trechos em FIT com fundo desfocado).
Cada formato tem cache próprio (video.json / video-9x16.json) e projeto HyperFrames próprio.

As skills de cada etapa são procuradas na pasta-mãe desta skill (ex.: /home/box/agent-data/workflows/)
ou em $AULA_SKILLS_DIR / config `skills_dir`. Python das etapas: o mesmo que roda este script
(use o venv com edge-tts, faster-whisper e PyYAML; azure-cognitiveservices-speech é opcional, só no motor azure).
"""
import argparse, glob, hashlib, json, os, shutil, subprocess, sys, time

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import uso_tokens  # noqa: E402  ponto único de registro de tokens de LLM
STAGES = ["legendas", "roteiro", "codigo", "narracao", "trechos", "html", "video", "verificacao"]
STAGE_SKILL = {"legendas": "youtube-legendas", "roteiro": "roteiro-didatico-ptbr", "codigo": "codigo-exemplo-aula", "narracao": "narracao-tts-ptbr",
               "trechos": "trechos-youtube-credito", "html": "pagina-html-gsap", "video": "video-hyperframes",
               "verificacao": None}
PY = sys.executable
FORMATOS = {"16x9": {"res": "landscape", "hf": "hf", "mp4": "aula.mp4", "srt": "aula.srt", "cache": "video", "wh": (1920, 1080)},
            "9x16": {"res": "portrait", "hf": "hf-9x16", "mp4": "aula-9x16.mp4", "srt": "aula-9x16.srt", "cache": "video-9x16",
                     "wh": (1080, 1920)}}


# Padrões da narração (v1.3.0, escolhidos por transcrição reversa: ver narracao-tts-ptbr/references/vozes-e-pronuncia.md).
# Na config: narracao: {motor, voz, rate, pausa_frase_ms, pausa_paragrafo_ms, pausa_cena_ms, pausa_trecho_ms, pronuncia: {termo: grafia},
# whisper_modelo, termos_checagem, termos_ingles}. `velocidade` (até v1.2) ainda vale como rate.
# termos_ingles (v1.5/v1.6): {modo: emendar_en|multilingual|original|aportuguesar|ssml_lang|ingles_mesma_voz,
#   voz_en, voz_multilingual, termos: [extras], sem_ingles: [tirar da lista padrão]}.
#   Padrão (v1.7, decisão do Carlos em 2026-11-14): ingles_mesma_voz — mesma Francisca -5%, frase inteira,
#   grafias de som inglês (pronuncia-ingles-francisca.json). aportuguesar (pronuncia-padrao.json) segue opcional.
#   a emenda en-US (emendar_en) foi testada e recusada na escuta em 2026-11-14.
NARRACAO_PADRAO = {"voz": "pt-BR-FranciscaNeural", "rate": "-5%", "pausa_frase_ms": 400, "pausa_paragrafo_ms": 700,
                   "pausa_cena_ms": 950, "pausa_trecho_ms": 500, "whisper_modelo": "small",
                   "termos_ingles": {"modo": "ingles_mesma_voz"}}


class Parar(Exception):
    pass


def log(msg):
    print(f"[aula-ra {time.strftime('%H:%M:%S')}] {msg}", flush=True)


def run(cmd, **kw):
    log("$ " + " ".join(str(c) for c in cmd))
    subprocess.run([str(c) for c in cmd], check=True, **kw)


def tsec(x):
    if isinstance(x, (int, float)): return float(x)
    s = 0
    for v in str(x).split(":"): s = s * 60 + float(v)
    return s


def vid_of(url):
    import re
    m = re.search(r"(?:v=|youtu\.be/|shorts/)([\w-]{11})", url)
    return m.group(1)


def sha_files(paths):
    h = hashlib.sha256()
    for p in sorted(set(paths)):
        if os.path.isdir(p):
            for f in sorted(glob.glob(os.path.join(p, "**", "*"), recursive=True)):
                if os.path.isfile(f) and "__pycache__" not in f:
                    h.update(f.encode()); h.update(open(f, "rb").read())
        elif os.path.isfile(p):
            h.update(p.encode()); h.update(open(p, "rb").read())
        else:
            h.update(f"missing:{p}".encode())
    return h.hexdigest()


class Pipeline:
    def __init__(self, cfg_path, force=False, refazer_pedido=False, manter_roteiro=False, selecao_modo=None):
        self.cfg_path = os.path.abspath(cfg_path)
        self.cfg = yaml.safe_load(open(cfg_path, encoding="utf-8"))
        base = os.path.dirname(self.cfg_path)
        rel = lambda p: p if os.path.isabs(p) else os.path.normpath(os.path.join(base, p))
        self.out = rel(self.cfg["saida"])
        self.work = rel(self.cfg.get("trabalho") or os.path.join(self.cfg["saida"], "_trabalho"))
        self.skills = os.environ.get("AULA_SKILLS_DIR") or (rel(self.cfg["skills_dir"]) if self.cfg.get("skills_dir")
                                                             else os.path.normpath(os.path.join(HERE, "..", "..")))
        self.force = force; self.refazer_pedido = refazer_pedido; self.manter_roteiro = manter_roteiro
        self.selecao_modo = selecao_modo
        self.cache_videos = rel(self.cfg["cache_videos"]) if self.cfg.get("cache_videos") else None
        for d in (self.out, self.work, os.path.join(self.work, ".cache")):
            os.makedirs(d, exist_ok=True)
        self.leg_dir = os.path.join(self.work, "legendas")
        self.roteiro = os.path.join(self.out, self.cfg.get("roteiro", {}).get("arquivo", "roteiro.json"))
        self.tts_dir = os.path.join(self.work, "narracao")
        self.clips_dir = os.path.join(self.out, "clips")
        self.hf_dir = os.path.join(self.work, "hf")
        self.formatos = [str(f).replace(":", "x") for f in (self.cfg.get("formatos") or ["16x9"])]
        for f in self.formatos:
            if f not in FORMATOS: raise SystemExit(f"formato desconhecido: {f} (use 16x9 e/ou 9x16)")
        self.tema_json = os.path.join(self.work, "tema.json")
        json.dump(self.cfg.get("marca", {}), open(self.tema_json, "w", encoding="utf-8"), ensure_ascii=False)

    # ---------- utilidades ----------
    def s(self, stage, *parts):
        return os.path.join(self.skills, STAGE_SKILL[stage], *parts)

    def cache_ok(self, stage, key, outputs):
        f = os.path.join(self.work, ".cache", f"{stage}.json")
        if self.force or not os.path.exists(f):
            return False
        c = json.load(open(f))
        return c.get("hash") == key and all(os.path.exists(o) for o in outputs)

    def cache_save(self, stage, key, outputs):
        json.dump({"hash": key, "outputs": outputs, "quando": time.strftime("%Y-%m-%d %H:%M:%S")},
                  open(os.path.join(self.work, ".cache", f"{stage}.json"), "w"), indent=1)

    @staticmethod
    def narracao_cfg_hashable(n):
        """motor: edge (ou ausente) não entra no hash — pin de cursos antigos não re-narra."""
        if not isinstance(n, dict):
            return n
        n = dict(n)
        if n.get("motor") in (None, "", "edge"):
            n.pop("motor", None)
        return n

    def key(self, stage, cfg_parts, files):
        h = hashlib.sha256()
        cfg = {k: self.cfg.get(k) for k in cfg_parts}
        if "narracao" in cfg:
            cfg["narracao"] = self.narracao_cfg_hashable(cfg.get("narracao"))
        h.update(json.dumps(cfg, sort_keys=True, ensure_ascii=False).encode())
        skill_dir = self.s(stage) if STAGE_SKILL[stage] else os.path.join(HERE, "..")
        # scripts/, templates/ e os .json de references/ (ex.: mapa de pronúncia padrão) da skill da etapa
        h.update(sha_files(files + [os.path.join(skill_dir, "scripts"), os.path.join(skill_dir, "templates")]
                           + glob.glob(os.path.join(skill_dir, "references", "*.json"))).encode())
        return h.hexdigest()

    def trechos_cfg(self):
        return [{**t, "video": vid_of(t["video"]) if "/" in str(t["video"]) else t["video"]} for t in self.cfg.get("trechos", [])]

    # ---------- etapas ----------
    def versao_skill(self, stage):
        f = self.s(stage, "scripts", "VERSION")
        return open(f).read().split()[0] if os.path.exists(f) else "0"

    def legendas(self):
        """Legendas de cada vídeo. Com `cache_videos` (o curso põe <curso>/_cache/videos), cada vídeo é baixado UMA vez para
        <cache>/<id>/<versão da youtube-legendas>-<hash dos idiomas>/ e copiado para a aula: várias aulas com o mesmo vídeo
        reaproveitam a transcrição (e um resumo.md, se existir) sem novo download."""
        videos = self.cfg.get("videos") or []
        if not videos:
            os.makedirs(self.leg_dir, exist_ok=True)
            return log("legendas: nenhum vídeo na config")
        outs = [os.path.join(self.leg_dir, vid_of(v["url"]), "fonte.json") for v in videos]
        k = self.key("legendas", ["videos"], [])
        if self.cache_ok("legendas", k, outs): return log("legendas: sem mudança, pulando")
        ver = self.versao_skill("legendas")
        for v in videos:
            vid = vid_of(v["url"]); dest = os.path.join(self.leg_dir, vid); langs = v.get("idiomas", "pt.*,pt,en.*,en")
            if not self.cache_videos:
                run([PY, self.s("legendas", "scripts", "fetch_subs.py"), v["url"], dest, "--langs", langs]); continue
            cdir = os.path.join(self.cache_videos, vid, f"{ver}-{hashlib.sha256(langs.encode()).hexdigest()[:8]}")
            if os.path.exists(os.path.join(cdir, "fonte.json")):
                log(f"legendas {vid}: do cache do curso ({cdir})")
            elif os.path.exists(os.path.join(dest, "fonte.json")):
                log(f"legendas {vid}: semeando o cache do curso com a cópia desta aula"); shutil.copytree(dest, cdir, dirs_exist_ok=True)
            else:
                run([PY, self.s("legendas", "scripts", "fetch_subs.py"), v["url"], cdir, "--langs", langs])
            shutil.copytree(cdir, dest, dirs_exist_ok=True)
        self.cache_save("legendas", k, outs)

    def selecao(self):
        """Só os trechos relevantes das transcrições (roteiro-didatico-ptbr/seleciona_trechos.py, BM25 + janelas com tempo,
        limite roteiro.selecao.max_tokens). Devolve o .md que entra no pedido (ou None em modo completo)."""
        sj = os.path.join(self.work, "selecao_transcricoes.json")
        run([PY, self.s("roteiro", "scripts", "seleciona_trechos.py"), "--config", self.cfg_path, "--legendas", self.leg_dir, "--saida", sj]
            + (["--modo", self.selecao_modo] if self.selecao_modo else []))
        sel = json.load(open(sj, encoding="utf-8"))
        return (None if sel["modo"] == "completo" else sj[:-5] + ".md"), sel

    def roteiro_entrada(self, sel_md):
        """Hash do que o roteiro depende: trechos selecionados, config relevante, prompt/esquema e versão da skill."""
        h = hashlib.sha256()
        h.update(json.dumps({k: self.cfg.get(k) for k in ("aula", "roteiro", "trechos", "exemplo", "videos")}, sort_keys=True,
                            ensure_ascii=False, default=str).encode())
        fs = [self.s("roteiro", "templates", "prompt_roteiro.md"), self.s("roteiro", "references", "schema-roteiro.md"),
              self.s("roteiro", "scripts", "make_request.py"), self.s("roteiro", "scripts", "VERSION")]
        fs += [sel_md] if sel_md else glob.glob(os.path.join(self.leg_dir, "*", "transcript.txt"))
        h.update(sha_files(fs + self.exemplo_files()).encode())
        return h.hexdigest()

    def pedido_roteiro(self, pedido, retomar, sel_md):
        cmd = [PY, self.s("roteiro", "scripts", "make_request.py"), "--config", self.cfg_path, "--legendas", self.leg_dir,
               "--saida", self.roteiro, "--pedido", pedido, "--retomar", retomar]
        run(cmd + (["--selecao", sel_md] if sel_md else []))

    def leitura_agente(self, pedido, sel_md):
        """O que o agente lê para escrever o roteiro: o pedido, o esquema e — sem seleção — as transcrições inteiras."""
        fs = [pedido, self.s("roteiro", "references", "schema-roteiro.md")]
        return fs if sel_md else fs + sorted(glob.glob(os.path.join(self.leg_dir, "*", "transcript.txt")))

    def roteiro_stage(self):
        pedido = os.path.join(self.out, "PEDIDO_ROTEIRO.md")
        retomar = f"{PY} {os.path.abspath(__file__)} {self.cfg_path} --from roteiro"
        sel_md, sel = self.selecao()
        entrada = self.roteiro_entrada(sel_md)
        cf = os.path.join(self.work, ".cache", "roteiro.json")
        c = json.load(open(cf)) if os.path.exists(cf) else {}
        info = {"selecao": {k: sel[k] for k in ("modo", "max_tokens", "tokens_transcricoes", "tokens_selecionados", "janelas_total")}
                | {"janelas": len(sel["janelas"])}}
        if not os.path.exists(self.roteiro):
            self.pedido_roteiro(pedido, retomar, sel_md)
            json.dump({"pedido_hash": entrada}, open(os.path.join(self.work, ".cache", "roteiro_pedido.json"), "w"))
            raise Parar(
                "ETAPA DO AGENTE: escreva o roteiro.\n"
                f"  Pedido (já traz os trechos relevantes das transcrições): {pedido}\n"
                f"  Esquema: {self.s('roteiro', 'references', 'schema-roteiro.md')}\n"
                f"  Escreva em: {self.roteiro}\n"
                f"  Depois retome: {retomar}")
        rsha = sha_files([self.roteiro])
        if c.get("entrada") == entrada and c.get("roteiro_sha") == rsha and not (self.force or self.refazer_pedido):
            uso_tokens.registrar(self.out, "roteiro", "agente", 0, 0, cache=True, evitados=c.get("tokens", 0),
                                 estimado=True, fonte="cache (hash da entrada igual)", detalhes=info)
            return log("roteiro: entrada igual (trechos, config, prompt, versão), sem refazer")
        if c and c.get("entrada") != entrada and c.get("roteiro_sha") == rsha:
            self.pedido_roteiro(pedido, retomar, sel_md)
            if self.cfg.get("roteiro", {}).get("refazer_se_mudar", True) and not (self.manter_roteiro or self.refazer_pedido):
                raise Parar("A ENTRADA DO ROTEIRO MUDOU (trechos selecionados, config, prompt ou versão da skill).\n"
                            f"  Refaça {self.roteiro} a partir do pedido atualizado: {pedido}\n"
                            f"  Ou mantenha o roteiro atual: {retomar} --manter-roteiro")
            log("roteiro: entrada mudou, mantendo o roteiro atual (--manter-roteiro)")
        elif self.refazer_pedido or not os.path.exists(pedido):
            self.pedido_roteiro(pedido, retomar, sel_md)
        run([PY, self.s("roteiro", "scripts", "validate_roteiro.py"), self.roteiro, "--config", self.cfg_path])
        novo = c.get("roteiro_sha") != rsha or self.refazer_pedido
        tokens = c.get("tokens", 0)
        if novo:  # roteiro novo (ou medição pedida): estima o que o agente leu e escreveu
            origem = ("medição (--refazer-pedido)" if self.refazer_pedido else
                      "roteiro escrito pelo agente" if c else "roteiro já existente (migração v1.4: estimado pelo pedido atual)")
            r = uso_tokens.estimar(self.out, "roteiro", self.leitura_agente(pedido, sel_md), self.roteiro,
                                   detalhes={**info, "origem": origem})
            tokens = r["entrada"] + r["saida"]
        json.dump({"entrada": entrada, "roteiro_sha": rsha, "tokens": tokens, "hash": entrada, "outputs": [self.roteiro],
                   "quando": time.strftime("%Y-%m-%d %H:%M:%S")}, open(cf, "w"), indent=1)

    def exemplo_files(self):
        ex = self.cfg.get("exemplo") or {}
        if not ex.get("dir"): return []
        base = os.path.dirname(self.cfg_path)
        repo = ex["dir"] if os.path.isabs(ex["dir"]) else os.path.normpath(os.path.join(base, ex["dir"]))
        ign = set(ex.get("ignorar") or ["node_modules", "dist", "build", ".git", ".turbo", "coverage"])
        fs = []
        for r, ds, f in os.walk(repo):
            ds[:] = sorted(d for d in ds if d not in ign)
            fs += [os.path.join(r, x) for x in sorted(f)]
        return fs or [repo]

    def codigo(self):
        rot = json.load(open(self.roteiro, encoding="utf-8"))
        cod_dir = os.path.join(self.out, "codigo")
        if not (self.cfg.get("exemplo") or rot.get("exercicios") or any(c.get("codigo") for c in rot["cenas"])):
            if os.path.isdir(cod_dir): shutil.rmtree(cod_dir)  # não deixar código velho na página/vídeo
            return log("codigo: aula sem exemplo/código/exercícios, pulando")
        outs = [os.path.join(cod_dir, "snippets.json"), os.path.join(cod_dir, "checagem.json")]
        if rot.get("exercicios"): outs.append(os.path.join(self.out, "exercicios.md"))
        k = self.key("codigo", ["exemplo"], [self.roteiro] + self.exemplo_files())
        if self.cache_ok("codigo", k, outs): return log("codigo: sem mudança, pulando")
        run([PY, self.s("codigo", "scripts", "etapa_codigo.py"), "--config", self.cfg_path, "--roteiro", self.roteiro,
             "--saida", self.out, "--trabalho", self.work])
        self.cache_save("codigo", k, outs)

    def snippets(self):
        p = os.path.join(self.out, "codigo", "snippets.json")
        return p if os.path.exists(p) else None

    def narracao_cfg(self):
        """Parâmetros da narração: padrões (NARRACAO_PADRAO) + `narracao:` da config. `velocidade` (antigo) vale como `rate`."""
        n = dict(self.cfg.get("narracao") or {})
        if "rate" not in n and "velocidade" in n: n["rate"] = n["velocidade"]
        return {**NARRACAO_PADRAO, **{k: v for k, v in n.items() if v is not None}}

    def motor_narracao(self):
        """TTS_MOTOR (env) vence narracao.motor (yaml); padrão edge. Não entra em NARRACAO_PADRAO:
        assim o hash de cache das aulas já renderizadas no motor edge continua o mesmo."""
        n = self.narracao_cfg()
        m = (os.environ.get("TTS_MOTOR") or n.get("motor") or "edge").strip().lower()
        if m not in ("edge", "azure"):
            raise SystemExit(f"motor de narração desconhecido: {m!r} (use edge ou azure)")
        return m

    def narracao(self):
        n = self.narracao_cfg()
        durs = {t["id"]: round(tsec(t["fim"]) - tsec(t["inicio"]), 3) for t in self.trechos_cfg()}
        dj = os.path.join(self.work, "trechos_duracoes.json"); json.dump(durs, open(dj, "w"))
        outs = [os.path.join(self.tts_dir, x) for x in ("narracao.wav", "narracao.srt", "timings.json", "voz.json")]
        k = self.key("narracao", ["narracao", "trechos"], [self.roteiro])
        motor = self.motor_narracao()
        # motor edge (padrão) não entra no hash, para não invalidar o cache já gravado;
        # azure (ou outro) entra, e a pasta de cache de frases também é por hash com o motor.
        if motor != "edge":
            k = hashlib.sha256((k + "|motor:" + motor).encode()).hexdigest()
        if self.cache_ok("narracao", k, outs): return log("narracao: sem mudança, pulando")
        if os.path.isdir(self.tts_dir): shutil.rmtree(self.tts_dir)  # sem cena_XX velha de outra versão
        cmd = [PY, self.s("narracao", "scripts", "tts_ptbr.py"), self.roteiro, self.tts_dir, "--motor", motor,
               "--voice", n["voz"],
               f"--rate={n['rate']}", "--pausa-frase-ms", n["pausa_frase_ms"], "--pausa-paragrafo-ms", n["pausa_paragrafo_ms"],
               "--pausa-cena-ms", n["pausa_cena_ms"], "--pausa-trecho-ms", n["pausa_trecho_ms"], "--trechos", dj]
        if motor == "azure":
            cmd += ["--cache", os.path.join(self.work, ".cache", "tts-frases")]
        if n.get("pronuncia"):
            os.makedirs(self.tts_dir, exist_ok=True)
            pj = os.path.join(self.work, "pronuncia_extra.json"); json.dump(n["pronuncia"], open(pj, "w", encoding="utf-8"), ensure_ascii=False)
            cmd += ["--pronuncia", pj]
        te = n.get("termos_ingles") or {}
        if te.get("modo"): cmd += ["--termos-ingles-modo", te["modo"]]
        if te.get("voz_en"): cmd += ["--voz-en", te["voz_en"]]
        if te.get("voz_multilingual"): cmd += ["--voz-multilingual", te["voz_multilingual"]]
        if te.get("termos") or te.get("sem_ingles"):
            tj = os.path.join(self.work, "termos_ingles_extra.json")
            json.dump({"termos": te.get("termos") or [], "sem_ingles": te.get("sem_ingles") or []},
                      open(tj, "w", encoding="utf-8"), ensure_ascii=False)
            cmd += ["--termos-ingles", tj]
        run(cmd)
        run([PY, self.s("narracao", "scripts", "check_voice.py"), self.roteiro, os.path.join(self.tts_dir, "narracao.wav"),
             "--model", n["whisper_modelo"], "--terms", ",".join(n.get("termos_checagem") or []),
             "--timings", os.path.join(self.tts_dir, "timings.json"), "--json", os.path.join(self.tts_dir, "voz.json")])
        self.cache_save("narracao", k, outs)

    def trechos(self):
        tr = self.trechos_cfg()
        if not tr: return log("trechos: nenhum na config")
        tj = os.path.join(self.work, "trechos.json"); json.dump(tr, open(tj, "w"), ensure_ascii=False)
        outs = [os.path.join(self.clips_dir, "clips.json")] + [os.path.join(self.clips_dir, f"{t['id']}.mp4") for t in tr]
        if "9x16" in self.formatos:
            outs += [os.path.join(self.clips_dir, f"{t['id']}_9x16.mp4") for t in tr]
        k = self.key("trechos", ["trechos", "videos"] + (["formatos"] if self.formatos != ["16x9"] else []), [self.roteiro])
        if self.cache_ok("trechos", k, outs): return log("trechos: sem mudança, pulando")
        tc = self.cfg.get("trechos_opcoes", {})
        run([PY, self.s("trechos", "scripts", "cut_clips.py"), "--trechos", tj, "--fontes", self.leg_dir,
             "--cache", os.path.join(self.work, "cache_trechos"), "--out", self.clips_dir, "--roteiro", self.roteiro,
             "--pad", tc.get("folga", 1.0), "--font", self.cfg.get("marca", {}).get("fonte_texto", "Inter"), "--altura", tc.get("altura", 720),
             "--formatos", ",".join(self.formatos), "--fundo-9x16", tc.get("fundo_9x16", "blur")])
        self.cache_save("trechos", k, outs)

    def gsap(self):
        ver = self.cfg.get("html", {}).get("gsap_versao", "3.15.0")
        p = os.path.join(self.work, f"gsap-{ver}.min.js")
        if not os.path.exists(p):
            run(["curl", "-sSLf", "-o", p, f"https://cdn.jsdelivr.net/npm/gsap@{ver}/dist/gsap.min.js"])
        return p

    def html(self):
        out = os.path.join(self.out, "aula.html")
        cj = os.path.join(self.clips_dir, "clips.json")
        sn = self.snippets()
        extra = [sn, os.path.join(self.out, "codigo", "checagem.json")] if sn else []
        k = self.key("html", ["html", "marca"], [self.roteiro, cj] + glob.glob(os.path.join(self.clips_dir, "*.vtt")) + extra)
        if self.cache_ok("html", k, [out]): return log("html: sem mudança, pulando")
        cmd = [PY, self.s("html", "scripts", "build_html.py"), self.roteiro, out, "--gsap", self.gsap(), "--tema", self.tema_json]
        if os.path.exists(cj): cmd += ["--clips", cj, "--clips-dir", "clips/"]
        if sn: cmd += ["--codigo", sn]
        run(cmd)
        self.cache_save("html", k, [out])

    def video(self):
        for fmt in self.formatos:
            self.video_fmt(fmt)

    def video_fmt(self, fmt):
        F = FORMATOS[fmt]
        v = self.cfg.get("video", {}); hfv = v.get("hyperframes", "0.9.43")
        out = os.path.join(self.out, F["mp4"])
        cj = os.path.join(self.clips_dir, "clips.json")
        srt_out = os.path.join(self.out, F["srt"])
        hf_dir = os.path.join(self.work, F["hf"])
        files = [self.roteiro, os.path.join(self.tts_dir, "timings.json"), os.path.join(self.tts_dir, "narracao.wav"),
                 os.path.join(self.tts_dir, "narracao.srt"), cj] + glob.glob(os.path.join(self.clips_dir, "*.mp4"))
        sn = self.snippets()
        if sn: files.append(sn)
        # 16x9 mantém a chave antiga (compatível); 9x16 inclui o formato e as opções verticais
        k = self.key("video", ["video", "marca"] + (["video_9x16"] if fmt == "9x16" else []), files + ([fmt] if fmt != "16x9" else []))
        if self.cache_ok(F["cache"], k, [out, srt_out]): return log(f"video {fmt}: sem mudança, pulando")
        if not os.path.exists(os.path.join(hf_dir, "hyperframes.json")):
            os.makedirs(self.work, exist_ok=True)
            res = F["res"] if fmt == "9x16" else v.get("resolucao", "landscape")
            run(["npx", "-y", f"hyperframes@{hfv}", "init", os.path.basename(hf_dir), "--example", "blank",
                 "--resolution", res, "--non-interactive", "--skip-skills"], cwd=self.work)
        os.makedirs(os.path.join(hf_dir, "assets"), exist_ok=True)
        shutil.copy2(os.path.join(self.tts_dir, "narracao.wav"), os.path.join(hf_dir, "assets", "narracao.wav"))
        shutil.copy2(self.gsap(), os.path.join(hf_dir, "gsap.min.js"))
        cmd = [PY, self.s("video", "scripts", "build_hyperframes.py"), self.roteiro, os.path.join(self.tts_dir, "timings.json"),
               hf_dir, "--tema", self.tema_json, "--formato", fmt]
        if os.path.exists(cj): cmd += ["--clips", cj]
        if sn: cmd += ["--codigo", sn]
        run(cmd)
        env = dict(os.environ)
        if fmt == "9x16":
            v9 = self.cfg.get("video_9x16", {})
            run([PY, self.s("video", "scripts", "rewrap_srt.py"), os.path.join(self.tts_dir, "narracao.srt"), srt_out,
                 "--max", v9.get("legenda_max_chars", 26)])
            env["SUB_MARGINV"] = str(v9.get("legenda_margem", 48))
            size = str(v9.get("legenda_tamanho", 9))
        else:
            shutil.copy2(os.path.join(self.tts_dir, "narracao.srt"), srt_out)
            size = str(v.get("legenda_tamanho", 18))
        run([self.s("video", "scripts", "render.sh"), hf_dir, srt_out, out, v.get("legenda_fonte", "Inter"), size, hfv], env=env)
        self.cache_save(F["cache"], k, [out, srt_out])

    def verificacao(self):
        out = os.path.join(self.out, "verificacao.json")
        mp4 = os.path.join(self.out, "aula.mp4"); html = os.path.join(self.out, "aula.html")
        mp4s = {f: os.path.join(self.out, FORMATOS[f]["mp4"]) for f in self.formatos}
        if "16x9" not in mp4s: mp4 = next(iter(mp4s.values()))
        tim = os.path.join(self.tts_dir, "timings.json")
        k = self.key("verificacao", ["narracao", "formatos"], list(mp4s.values()) + [html, tim]
                     + glob.glob(os.path.join(self.out, "codigo", "checagem.json")))
        if self.cache_ok("verificacao", k, [out]): return log("verificacao: sem mudança, pulando")
        frames = os.path.join(self.out, "frames"); os.makedirs(frames, exist_ok=True)
        res = {"formatos": {}}
        t = json.load(open(tim)); cenas = t["cenas"]
        momentos = [("cena1", (cenas[0]["start"] + cenas[0]["end"]) / 2)]
        meio = cenas[len(cenas) // 2]
        momentos.append((f"cena{len(cenas) // 2 + 1}", (meio["start"] + meio["end"]) / 2))
        for c in cenas:
            if "clip_start" in c:
                momentos.append((f"trecho_{c['clip_id']}", (c["clip_start"] + c["clip_end"]) / 2))
        momentos.append(("ultima", cenas[-1]["end"] - 1.0))
        falhas = []
        for fmt, arq in mp4s.items():
            pr = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries",
                  "format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate", "-of", "json", arq]))
            vs = [x for x in pr["streams"] if x["codec_type"] == "video"]
            wh_ok = bool(vs) and (vs[0]["width"], vs[0]["height"]) == FORMATOS[fmt]["wh"]
            tem_audio = any(x["codec_type"] == "audio" for x in pr["streams"])
            if not (wh_ok and tem_audio): falhas.append(f"{fmt}: dimensões/áudio inesperados")
            fr = []
            pref = "video" if fmt == "16x9" else f"video{fmt}"
            for nome, s_ in momentos:
                pth = os.path.join(frames, f"{pref}_{nome}_{s_:.0f}s.png")
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s_:.2f}", "-i", arq, "-frames:v", "1", pth], check=True)
                fr.append(pth)
            res["formatos"][fmt] = {"arquivo": arq, "ffprobe": pr, "dimensoes_ok": wh_ok, "audio": tem_audio, "frames": fr}
            if fmt == "16x9": res["ffprobe"] = pr; res["frames_video"] = fr
        durs = [float(v["ffprobe"]["format"]["duration"]) for v in res["formatos"].values()]
        if max(durs) - min(durs) > 0.5: falhas.append(f"durações diferentes entre formatos: {durs}")
        res["falhas_formatos"] = falhas
        # voz no MP4 final (trechos silenciados)
        n = self.narracao_cfg()
        vj = os.path.join(self.work, "voz_mp4.json")
        run([PY, self.s("narracao", "scripts", "check_voice.py"), self.roteiro, mp4, "--timings", tim,
             "--model", n["whisper_modelo"], "--terms", ",".join(n.get("termos_checagem") or []), "--json", vj])
        res["voz_mp4"] = json.load(open(vj))
        chk = os.path.join(self.out, "codigo", "checagem.json")
        if os.path.exists(chk):  # resultado da etapa codigo (o exemplo rodou?)
            c = json.load(open(chk, encoding="utf-8"))
            res["codigo"] = {"ok": c.get("ok"), "comandos": [{k: x[k] for k in ("nome", "cmd", "codigo", "ok", "segundos")} for x in c.get("comandos", [])],
                             "snippets": c.get("snippets"), "exercicios": c.get("exercicios")}
            if not c.get("ok"): falhas.append("etapa codigo com erro (ver codigo/checagem.json)")
        # HTML no Chrome headless
        node = os.path.join(self.work, "node")
        if not os.path.exists(os.path.join(node, "node_modules", "puppeteer-core")):
            os.makedirs(node, exist_ok=True)
            run(["npm", "init", "-y"], cwd=node, stdout=subprocess.DEVNULL)
            run(["npm", "i", "-s", "puppeteer-core"], cwd=node)
        shutil.copy2(self.s("html", "scripts", "check_html.mjs"), os.path.join(node, "check_html.mjs"))
        rot = json.load(open(self.roteiro, encoding="utf-8"))
        passos = sorted({1, len(rot["cenas"])} | {i + 1 for i, c in enumerate(rot["cenas"]) if c.get("trecho") or c.get("codigo")})
        p = subprocess.run(["node", "check_html.mjs", html, frames, ",".join(map(str, passos))], cwd=node,
                           capture_output=True, text=True, env={**os.environ, "CHROME": shutil.which("google-chrome") or "/usr/bin/google-chrome"})
        print(p.stdout + p.stderr)
        res["html"] = {"codigo": p.returncode, "saida": p.stdout.strip().splitlines()}
        json.dump(res, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        if p.returncode != 0:
            raise SystemExit("verificação do HTML falhou (ver verificacao.json)")
        if falhas:
            raise SystemExit("verificação dos formatos falhou: " + "; ".join(falhas))
        self.cache_save("verificacao", k, [out])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("config")
    ap.add_argument("--stage", choices=STAGES); ap.add_argument("--from", dest="frm", choices=STAGES)
    ap.add_argument("--to", choices=STAGES); ap.add_argument("--force", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--refazer-pedido", action="store_true", help="roteiro: refaz o pedido e registra a estimativa de uma rodada sem cache")
    ap.add_argument("--manter-roteiro", action="store_true", help="roteiro: a entrada mudou, mas fica o roteiro atual")
    ap.add_argument("--selecao-modo", choices=["bm25", "completo"], help="roteiro: sobrepõe roteiro.selecao.modo (medir antes/depois)")
    a = ap.parse_args()
    p = Pipeline(a.config, force=a.force, refazer_pedido=a.refazer_pedido, manter_roteiro=a.manter_roteiro, selecao_modo=a.selecao_modo)
    if a.list:
        for s in STAGES:
            nomes = [FORMATOS[x]["cache"] for x in p.formatos] if s == "video" else [s]
            for nm in nomes:
                f = os.path.join(p.work, ".cache", f"{nm}.json")
                print(f"{nm:12s} {STAGE_SKILL[s] or 'aula-ra':26s} {json.load(open(f))['quando'] if os.path.exists(f) else '-'}")
        return
    sel = [a.stage] if a.stage else STAGES[STAGES.index(a.frm or STAGES[0]):STAGES.index(a.to or STAGES[-1]) + 1]
    fn = {"legendas": p.legendas, "roteiro": p.roteiro_stage, "codigo": p.codigo, "narracao": p.narracao, "trechos": p.trechos,
          "html": p.html, "video": p.video, "verificacao": p.verificacao}
    try:
        for s in sel:
            log(f"== etapa {s} ({STAGE_SKILL[s] or 'aula-ra'})")
            fn[s]()
    except Parar as e:
        print("\n" + str(e)); sys.exit(10)
    log("pronto: " + p.out)


if __name__ == "__main__":
    main()
