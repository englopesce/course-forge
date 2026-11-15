#!/usr/bin/env python3
"""Narração pt-BR a partir de um roteiro.json (campo cenas[].narracao).

Motores: --motor edge (padrão, edge-tts) ou --motor azure (Azure Speech, licença comercial;
recomendado para conteúdo monetizado). Também vale a variável TTS_MOTOR. O caminho edge
permanece idêntico ao da v1.7.

Gera: <out>/cena_XX.wav (fala da cena, já com as pausas entre frases), <out>/narracao.wav (todas as
cenas + pausas + silêncio dos trechos), <out>/timings.json (início/fim de cada cena e de cada frase) e
<out>/narracao.srt (legendas curtas a partir dos limites de palavra do próprio TTS, nos tempos novos).

Pausas: o edge-tts (7.x) escapa SSML próprio (um <break> é lido em voz alta), então cada FRASE é
sintetizada à parte, o silêncio de borda que o serviço põe é aparado e as frases são unidas com
silêncio exato: --pausa-frase-ms entre frases, --pausa-paragrafo-ms entre parágrafos (linha em branco
ou quebra de linha na narração), --pausa-cena-ms entre cenas e --pausa-trecho-ms antes/depois de um
trecho original. Sem as pausas a voz emenda as frases (~0,24 s natural do serviço).

Uso: python tts_ptbr.py roteiro.json saida/ [--motor edge|azure] [--voice pt-BR-FranciscaNeural] [--rate -5%]
         [--pausa-frase-ms 400] [--pausa-paragrafo-ms 700] [--pausa-cena-ms 950] [--pausa-trecho-ms 500]
         [--pronuncia extra.json]        # {"termo": "grafia falada"} somado ao mapa padrão (o roteiro vence)
         [--termos-ingles-modo emendar_en|multilingual|original|aportuguesar|ssml_lang|ingles_mesma_voz] [--voz-en en-US-AvaNeural]
         [--termos-ingles extra.json]    # {"termos": [...], "sem_ingles": [...]}: soma/tira da lista padrão
         [--trechos duracoes.json]       # {"id-do-trecho": segundos}: abre um silêncio na narração
                                         # para o trecho original tocar logo após a fala da cena
Campos de timings.json por cena: start/end (fala), frases [[início, fim], ...] e, se houver,
clip_id/clip_start/clip_end. As legendas pt-BR do trecho (cenas[].trecho.legendas) entram no mesmo SRT.
Requer: pip install edge-tts numpy ; ffmpeg/ffprobe no PATH. Precisa de internet.
Motor azure: AZURE_SPEECH_KEY e AZURE_SPEECH_REGION no ambiente; pacote opcional
azure-cognitiveservices-speech (WordBoundary); sem ele, usa o REST. timings.json
registra o campo motor (edge|azure). Chave e região nunca vão a log nem a metadado.
"""
import argparse, asyncio, json, os, re, subprocess, wave

import edge_tts
import numpy as np

import termos_ingles as ti
import motor_azure as az

MAX_CHARS = 42  # por linha de legenda
MAX_LINES = 2
SR = 48000
PADRAO = {"voice": "pt-BR-FranciscaNeural", "rate": "-5%", "pausa_frase_ms": 400, "pausa_paragrafo_ms": 700,
          "pausa_cena_ms": 950, "pausa_trecho_ms": 500,
          # v1.5: termos técnicos em inglês com pronúncia inglesa (ver termos_ingles.py e references/vozes-e-pronuncia.md)
          # v1.7: padrão "ingles_mesma_voz" (Francisca -5%, grafias de som inglês, decisão do Carlos em 2026-11-14); aportuguesar segue opcional; emendar_en foi testado e recusado na escuta (2026-11-14)
          "termos_ingles_modo": "ingles_mesma_voz", "voz_en": "en-US-AvaNeural", "voz_multilingual": "pt-BR-ThalitaMultilingualNeural"}


def norm_rate(r):
    r = str(r).strip()
    if not r.endswith("%"): r += "%"
    if r[0] not in "+-": r = "+" + r
    return r


async def synth(text, voice, rate, mp3, sem, tries=4, motor="edge", cache_dir=None):
    async with sem:
        if motor == "azure":
            # retry/backoff (429/5xx) fica em motor_azure.sintetiza
            return await asyncio.to_thread(az.sintetiza, text, voice, rate, mp3, cache_dir)
        for n in range(tries):
            try:
                return await _synth(text, voice, rate, mp3)
            except Exception as e:  # serviço às vezes responde sem áudio; tenta de novo
                if n == tries - 1:
                    raise
                print(f"  tentativa {n+1} falhou ({type(e).__name__}); repetindo...")
                await asyncio.sleep(2 * (n + 1))


async def _synth(text, voice, rate, mp3):
    comm = edge_tts.Communicate(text, voice, rate=rate, boundary="WordBoundary")
    words = []
    with open(mp3, "wb") as f:
        async for ch in comm.stream():
            if ch["type"] == "audio":
                f.write(ch["data"])
            elif ch["type"] == "WordBoundary":
                words.append((ch["offset"] / 1e7, (ch["offset"] + ch["duration"]) / 1e7, ch["text"]))
    if not words or os.path.getsize(mp3) < 1000:
        raise RuntimeError("sem áudio")
    return words


def decode(mp3):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", mp3, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"])
    return np.frombuffer(raw, dtype=np.float32).copy()


def apara(x, words, limiar_db=-50.0):
    """Corta o silêncio de borda do serviço (energia em janelas de 10 ms): guarda 30 ms antes da 1ª
    janela com voz e 90 ms depois da última. Devolve (áudio, deslocamento em s a subtrair das palavras)."""
    hop = SR // 100
    n = len(x) // hop
    if n == 0: return x, 0.0
    rms = np.sqrt(np.mean(x[:n * hop].reshape(n, hop) ** 2, axis=1) + 1e-12)
    voz = np.where(20 * np.log10(rms) > limiar_db)[0]
    if len(voz) == 0: return x, 0.0
    a = max(0, voz[0] * hop - int(0.03 * SR))
    b = min(len(x), (voz[-1] + 1) * hop + int(0.09 * SR))
    if words:  # sem WordBoundary (REST Azure) vale só a energia; com words o corte é idêntico ao do edge
        a = min(a, max(0, int((words[0][0] - 0.02) * SR)))  # nunca corta o começo da 1ª palavra
        b = max(b, min(len(x), int((words[-1][1] + 0.05) * SR)))
    return x[a:b], a / SR


def ts(t):
    h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}"


def chunk_words(words, text, prefixos=frozenset()):
    """Agrupa palavras em blocos de legenda. Usa o texto original (com pontuação)
    mapeando palavra a palavra, porque o WordBoundary vem sem pontuação.
    `prefixos`: começos de grafias de várias palavras ("ponto ême" de "ponto ême dê cê"): não quebra o bloco no meio
    delas, senão a legenda não volta para a grafia original (".mdc")."""
    toks = text.split()
    out, cur, i = [], [], 0
    for (a, b, w) in words:
        tok = w
        while i < len(toks):
            if w.lower().strip('.,:;!?“”"') in toks[i].lower():
                tok = toks[i]; i += 1; break
            i += 1
        cur.append((a, b, tok))
        line = " ".join(x[2] for x in cur)
        meio = any(" ".join(x[2] for x in cur[-k:]).rstrip(",;:") in prefixos for k in range(1, min(len(cur), 6) + 1)) \
            and not tok.endswith(('.', '?', '!'))
        if (len(line) > MAX_CHARS * MAX_LINES - 10 or tok.endswith(('.', ':', '?', '!', ';'))) and not meio:
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    fix = []  # evita "palavra órfã" (bloco de 1 palavra) juntando ao bloco anterior da mesma frase
    for blk in out:
        if fix and len(blk) == 1 and not fix[-1][-1][2].endswith(('.', ':', '?', '!', ';')):
            fix[-1] = fix[-1] + blk
        else:
            fix.append(blk)
    return fix


def wrap(s):
    if len(s) <= MAX_CHARS:
        return s
    ws = s.split(); best = None
    for k in range(1, len(ws)):
        l1, l2 = " ".join(ws[:k]), " ".join(ws[k:])
        sc = max(len(l1), len(l2))
        if best is None or sc < best[0]:
            best = (sc, l1 + "\n" + l2)
    return best[1]


def frases(narracao):
    """[(parágrafo, frase)]: parágrafo = bloco separado por quebra de linha; frase termina em . ! ? …
    seguido de espaço (".mdc", "console.log", "3.5" não quebram)."""
    out = []
    for p, par in enumerate(x for x in re.split(r"\s*\n\s*", narracao.strip()) if x.strip()):
        for f in re.split(r"(?<=[.!?…])\s+(?=\S)", par.strip()):
            if f.strip(): out.append((p, f.strip()))
    return out


def carrega_pron(rot, extra_path, modo="ingles_mesma_voz"):
    """Mapa de grafias para a voz. Base: pronuncia-padrao.json (modo aportuguesar).
    No modo ingles_mesma_voz, as entradas de pronuncia-ingles-francisca.json substituem as do padrão
    (a frase continua inteira na Francisca; não há emenda nem troca de voz)."""
    pron = {}
    ref = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references")
    padrao = os.path.join(ref, "pronuncia-padrao.json")
    ingles = os.path.join(ref, "pronuncia-ingles-francisca.json")
    if rot.get("pronuncia_padrao", True) and os.path.exists(padrao):
        pron = {k: v for k, v in json.load(open(padrao, encoding="utf-8")).items() if not k.startswith("_")}
    if modo == "ingles_mesma_voz" and os.path.exists(ingles):
        pron.update({k: v for k, v in json.load(open(ingles, encoding="utf-8")).items() if not k.startswith("_")})
    if extra_path:
        pron.update({k: v for k, v in json.load(open(extra_path, encoding="utf-8")).items() if not k.startswith("_")})
    pron.update(rot.get("pronuncia", {}))  # o do roteiro vence
    return dict(sorted(pron.items(), key=lambda kv: -len(kv[0])))  # mais longos primeiro ("NotebookLM" antes de "Notebook")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("roteiro"); ap.add_argument("out")
    ap.add_argument("--voice", default=PADRAO["voice"])
    ap.add_argument("--rate", default=PADRAO["rate"])
    ap.add_argument("--pausa-frase-ms", type=int, default=PADRAO["pausa_frase_ms"])
    ap.add_argument("--pausa-paragrafo-ms", type=int, default=PADRAO["pausa_paragrafo_ms"])
    ap.add_argument("--pausa-cena-ms", type=int, default=PADRAO["pausa_cena_ms"])
    ap.add_argument("--pausa-trecho-ms", type=int, default=PADRAO["pausa_trecho_ms"])
    ap.add_argument("--gap", type=float, default=None, help="(antigo) pausa entre cenas em s; use --pausa-cena-ms")
    ap.add_argument("--lead", type=float, default=0.6, help="silêncio inicial (s)")
    ap.add_argument("--pronuncia", default="", help="JSON {termo: grafia} extra (config da aula)")
    ap.add_argument("--trechos", default="", help="JSON {id: duração} dos trechos originais")
    ap.add_argument("--paralelo", type=int, default=4, help="frases sintetizadas ao mesmo tempo")
    ap.add_argument("--termos-ingles-modo", default=PADRAO["termos_ingles_modo"],
                    choices=["emendar_en", "multilingual", "original", "aportuguesar", "ssml_lang", "ingles_mesma_voz"])
    ap.add_argument("--voz-en", default=PADRAO["voz_en"], help="voz en-US que diz os termos (modo emendar_en)")
    ap.add_argument("--voz-multilingual", default=PADRAO["voz_multilingual"], help="voz do modo multilingual")
    ap.add_argument("--termos-ingles", default="", help='JSON {"termos": [...], "sem_ingles": [...]} da aula')
    ap.add_argument("--motor", default="", help="edge (padrão) ou azure (Azure Speech, licença comercial)")
    ap.add_argument("--cache", default="", help="pasta de cache por hash (motor+voz+rate+texto); também TTS_CACHE_DIR")
    a = ap.parse_args()
    a.rate = norm_rate(a.rate)
    a.motor = az.resolve_motor(cli=a.motor or None)
    a.cache = a.cache or os.environ.get("TTS_CACHE_DIR") or ""
    gap_cena = a.gap if a.gap is not None else a.pausa_cena_ms / 1000
    gap_trecho = a.pausa_trecho_ms / 1000
    if a.motor == "azure":
        az.credenciais()  # falha cedo, mensagem clara, sem vazar segredo
    os.makedirs(a.out, exist_ok=True)
    rot = json.load(open(a.roteiro, encoding="utf-8"))
    cenas = rot["cenas"]
    # "pronuncia": {"Gemini": "Dgémini"} -> só a voz usa a grafia fonética; a legenda mantém a original
    modo = a.termos_ingles_modo
    if modo == "ssml_lang":  # o serviço recusa <lang>/<voice>/<phoneme> (NoAudioReceived): usa a emenda
        print("aviso: ssml_lang não é aceito pelo serviço do edge-tts; usando emendar_en"); modo = "emendar_en"
    pron = carrega_pron(rot, a.pronuncia, modo=modo)
    termos_en = []
    # aportuguesar e ingles_mesma_voz: a frase sai inteira na voz pt-BR, com o mapa de grafias.
    # os outros modos tiram esses termos do mapa para a voz ler a grafia original (e emendar/trocar voz).
    if modo not in ("aportuguesar", "ingles_mesma_voz"):
        extra = json.load(open(a.termos_ingles, encoding="utf-8")) if a.termos_ingles else {}
        tira = {t.lower() for t in extra.get("sem_ingles", [])}
        termos_en = [t for t in ti.termos_padrao() + list(extra.get("termos", [])) if t.lower() not in tira]
        en_low = {t.lower() for t in termos_en}
        pron = {k: v for k, v in pron.items() if k.lower() not in en_low}  # o termo vai na grafia original
    if modo == "multilingual":
        a.voice = a.voz_multilingual
    volta = sorted(pron.items(), key=lambda kv: -len(kv[1]))

    # uma passada só, alternativas da mais longa para a mais curta: texto já trocado não é trocado de novo
    # (".cursor/rules" -> "ponto cursor barra rules" não vira "... rúlis"). (?<!\w)/(?!\w) em vez de \b:
    # funciona também para chaves que começam/terminam com símbolo (".mdc", "C#")
    ida = re.compile("|".join(rf"(?<!\w){re.escape(k)}(?!\w)" for k in pron)) if pron else None
    vinda = {}
    for k, v in pron.items(): vinda.setdefault(v, k)
    volta_re = re.compile("|".join(re.escape(v) for _, v in volta)) if volta else None

    prefixos = frozenset(" ".join(v.split()[:i]) for v in pron.values() for i in range(1, len(v.split())))

    def falado(t):
        return ida.sub(lambda m: pron[m.group(0)], t) if ida else t

    def escrito(t):
        return volta_re.sub(lambda m: vinda[m.group(0)], t) if volta_re else t

    # 1) sintetiza todas as frases (em paralelo, limitado)
    jobs = []
    for k, c in enumerate(cenas):
        for j, (par, fr) in enumerate(frases(c["narracao"])):
            jobs.append((k, j, par, falado(fr)))

    async def todas():
        sem = asyncio.Semaphore(max(1, a.paralelo))
        return await asyncio.gather(*[synth(f, a.voice, a.rate, os.path.join(a.out, f"cena_{k:02d}_f{j:02d}.mp3"), sem,
                                              motor=a.motor, cache_dir=(a.cache or None))
                                      for k, j, _, f in jobs])
    res = asyncio.run(todas())
    aud_en, emendas = {}, []
    presentes = {}
    if modo == "emendar_en":
        for _, _, _, f in jobs:
            for t in ti.agrupa(f, termos_en): presentes.setdefault(t.lower(), t)
    por_cena = {}
    brutos = [decode(os.path.join(a.out, f"cena_{k:02d}_f{j:02d}.mp3")) for k, j, _, _ in jobs]
    f0_pt = f0_en = None; pitch_en = "+0Hz"
    if modo == "emendar_en" and presentes:
        f0_pt = ti.f0_de(brutos[:12], SR)
        aud, f0_en, pitch_en = asyncio.run(ti.audios_termos(list(presentes.values()), a.voz_en, a.rate, f0_pt))
        aud_en = {t.lower(): x for t, x in aud.items()}
    for (k, j, par, fala), words, x in zip(jobs, res, brutos):
        if aud_en:
            aqui = {t: aud_en[t.lower()] for t in ti.agrupa(fala, termos_en)}
            if aqui:
                x, words, rel = ti.emendar(x, words, aqui, sr=SR, ajusta_tom=False)
                emendas += [{"cena": k, "frase": j, **r} for r in rel]
        x, desl = apara(x, words)
        if words:
            words = [(max(0.0, s0 - desl), max(0.0, s1 - desl), w) for s0, s1, w in words]
        else:
            # REST do Azure não traz WordBoundary: estima pela duração já aparada
            words = az.palavras_por_duracao(fala, len(x) / SR)
        por_cena.setdefault(k, []).append((par, fala, x, words))

    # 2) monta a linha do tempo
    t = a.lead; timings = []; srt = []; trilha = []
    durs = json.load(open(a.trechos, encoding="utf-8")) if a.trechos else {}

    def poe(x, inicio):
        trilha.append((int(round(inicio * SR)), x))

    for k, c in enumerate(cenas):
        start = t; fr_t = []; cena_buf = []; prev_par = None
        for par, fala, x, words in por_cena.get(k, []):
            if prev_par is not None:
                p = (a.pausa_paragrafo_ms if par != prev_par else a.pausa_frase_ms) / 1000
                cena_buf.append(np.zeros(int(round(p * SR)), dtype=np.float32)); t += p
            prev_par = par
            poe(x, t); cena_buf.append(x)
            for blk in chunk_words(words, fala, prefixos):
                s0, s1 = t + blk[0][0], t + blk[-1][1] + 0.15
                srt.append((s0, s1, wrap(escrito(" ".join(z[2] for z in blk)))))
            fr_t.append([round(t, 3), round(t + len(x) / SR, 3)])
            t += len(x) / SR
        end = t
        if cena_buf:
            write_wav(os.path.join(a.out, f"cena_{k:02d}.wav"), np.concatenate(cena_buf))
        tm = {"id": c.get("id", str(k)), "start": round(start, 3), "end": round(end, 3), "frases": fr_t}
        tr = c.get("trecho")
        if tr and tr.get("id") in durs:
            cs = end + gap_trecho; ce = cs + durs[tr["id"]]
            tm.update(clip_id=tr["id"], clip_start=round(cs, 3), clip_end=round(ce, 3))
            for lg in tr.get("legendas", []):
                srt.append((cs + lg["de"], min(ce, cs + lg["ate"]), wrap(lg["texto"])))
            t = ce + gap_trecho
            # depois do trecho, completa até a pausa de cena (mín.) antes da próxima fala
            t = max(t, ce + gap_cena * 0.5)
        else:
            t = end + gap_cena
        timings.append(tm)
    ultimo = timings[-1]
    total = max(ultimo["end"], ultimo.get("clip_end", 0)) + 1.5
    buf = np.zeros(int(round(total * SR)) + 1, dtype=np.float32)
    for i0, x in trilha:
        buf[i0:i0 + len(x)] += x[:max(0, len(buf) - i0)]
    wav = os.path.join(a.out, "narracao.wav")
    write_wav(wav, buf, canais=2)
    srt.sort(key=lambda z: z[0])
    for i in range(len(srt) - 1):  # evita sobreposição de legendas
        if srt[i][1] > srt[i + 1][0]:
            srt[i] = (srt[i][0], srt[i + 1][0] - 0.02, srt[i][2])
    with open(os.path.join(a.out, "narracao.srt"), "w", encoding="utf-8") as f:
        for i, (s0, s1, txt) in enumerate(srt, 1):
            f.write(f"{i}\n{ts(s0)} --> {ts(s1)}\n{txt}\n\n")
    json.dump({"modo": modo, "voz_en": a.voz_en if modo == "emendar_en" else None, "f0_pt": f0_pt, "f0_en": f0_en,
               "pitch_en": pitch_en, "emendas": emendas},
              open(os.path.join(a.out, "termos_ingles.json"), "w"), ensure_ascii=False, indent=1)
    meta = {"voice": a.voice, "rate": a.rate, "motor": a.motor, "termos_ingles_modo": modo, "pausa_frase_ms": a.pausa_frase_ms, "pausa_paragrafo_ms": a.pausa_paragrafo_ms,
            "pausa_cena_ms": int(round(gap_cena * 1000)), "pausa_trecho_ms": a.pausa_trecho_ms,
            "total": round(total, 3), "cenas": timings}
    az.garante_metadado_limpo(meta)
    json.dump(meta, open(os.path.join(a.out, "timings.json"), "w"), indent=1)
    for f in os.listdir(a.out):  # mp3 por frase são intermediários
        if re.match(r"cena_\d+_f\d+\.mp3$", f) or re.match(r"cena_\d+\.mp3$", f): os.remove(os.path.join(a.out, f))
    print(f"ok: {len(cenas)} cenas, {len(jobs)} frases, {total:.1f}s, motor {a.motor}, voz {a.voice} {a.rate}, termos em inglês: {modo}"
          f"{f' ({len(emendas)} emendas, voz {a.voz_en})' if modo == 'emendar_en' else ''}, "
          f"pausas frase/parágrafo/cena {a.pausa_frase_ms}/{a.pausa_paragrafo_ms}/{int(round(gap_cena * 1000))} ms")


def write_wav(path, x, canais=1):
    pcm = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    if canais == 2: pcm = np.repeat(pcm[:, None], 2, axis=1).reshape(-1)
    with wave.open(path, "wb") as w:
        w.setnchannels(canais); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())


if __name__ == "__main__":
    main()
