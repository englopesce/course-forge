#!/usr/bin/env python3
"""Termos técnicos em inglês com pronúncia inglesa dentro da narração pt-BR (v1.5).

Modos (narracao.termos_ingles.modo no yaml da aula):
  ingles_mesma_voz (PADRÃO desde v1.7, decisão do Carlos em 2026-11-14)  a frase sai inteira na mesma voz pt-BR (Francisca -5%), com grafias fonéticas
               pensadas para soar perto do inglês (pronuncia-ingles-francisca.json). Sem emenda e
               sem troca de voz.
  aportuguesar o mapa aportuguesado (pronuncia-padrao.json); foi o padrão até a v1.6.
  emendar_en   a frase sai inteira na voz pt-BR (prosódia natural) com o termo na grafia original;
               o trecho do termo (limites de palavra do próprio TTS) é trocado pelo termo dito por uma voz en-US,
               com volume (RMS) e tom (F0, rubberband) ajustados aos da voz pt e crossfade curto nas emendas.
  multilingual a frase inteira na voz pt-BR-ThalitaMultilingualNeural (ou voz_multilingual), grafia original.
  original     a voz pt-BR lê a grafia original (sem mapa para esses termos): linha de base.
  Testado em 2026-11-14 (_comparacao-ingles/LEIAME.md): emendar_en com en-US-AvaNeural foi o melhor nas métricas,
  mas o Carlos ouviu a amostra e recusou; ficou opcional.
  ssml_lang    <lang xml:lang="en-US"> no termo. O serviço do edge-tts recusa SSML além de voice/prosody
               (NoAudioReceived; testado em 2026-11-14 com <lang>, <voice> aninhada e <phoneme>): cai para emendar_en.
"""
import asyncio, os, re, subprocess, tempfile

import numpy as np

SR = 48000
_REF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references")


def termos_padrao():
    import json
    p = os.path.join(_REF, "termos-ingles.json")
    return [t for t in json.load(open(p, encoding="utf-8"))["termos"]] if os.path.exists(p) else []


def acha_termos(texto, termos):
    """Termos presentes no texto (palavra inteira, sem diferenciar maiúsculas), na grafia em que aparecem,
    mais longos primeiro; um termo contido num mais longo já achado ("JSON" em "JSON Schema") não conta de novo."""
    out, low, resto = [], set(), texto
    for t in sorted(set(termos), key=len, reverse=True):
        m = re.search(rf"(?<!\w){re.escape(t)}(?!\w)", resto, re.I)
        if m and m.group(0).lower() not in low:
            out.append(m.group(0)); low.add(m.group(0).lower())
            resto = re.sub(rf"(?<!\w){re.escape(t)}(?!\w)", " ", resto, flags=re.I)
    return out


def agrupa(texto, termos):
    """Como acha_termos, mas termos vizinhos só separados por espaço viram uma expressão só ("MCP server"):
    a voz en diz a expressão inteira (mais natural) e evita duas emendas coladas."""
    achados = acha_termos(texto, termos)
    if len(achados) < 2: return achados
    alt = "|".join(re.escape(t) for t in sorted(achados, key=len, reverse=True))
    out = []
    for m in re.finditer(rf"(?<!\w)(?:{alt})(?:\s+(?:{alt}))+(?!\w)", texto, re.I):
        out.append(m.group(0))
    resto = texto
    for g in out: resto = resto.replace(g, " ")
    return out + [t for t in acha_termos(resto, termos)]


# ---------- medidas ----------
def rms_db(x):
    return float(20 * np.log10(np.sqrt(np.mean(x.astype(np.float64) ** 2)) + 1e-9)) if len(x) else -120.0


def rms_voz_db(x, sr=SR, limiar=-45.0):
    """RMS só das janelas com voz (10 ms), para comparar volume sem contar silêncio."""
    hop = sr // 100; n = len(x) // hop
    if n == 0: return rms_db(x)
    r = 20 * np.log10(np.sqrt(np.mean(x[:n * hop].reshape(n, hop) ** 2, axis=1)) + 1e-9)
    v = r[r > limiar]
    return float(10 * np.log10(np.mean(10 ** (v / 10)))) if len(v) else rms_db(x)


def f0_mediana(x, sr=SR, fmin=75, fmax=400):
    """F0 mediana (Hz) por autocorrelação em janelas de 40 ms; só janelas sonoras. None se não houver."""
    w = int(0.04 * sr); hop = int(0.01 * sr); lo, hi = int(sr / fmax), int(sr / fmin); f0s = []
    for i in range(0, len(x) - w, hop):
        fr = x[i:i + w] - np.mean(x[i:i + w])
        if rms_db(fr) < -38: continue
        ac = np.correlate(fr, fr, "full")[w - 1:]
        if ac[0] <= 0: continue
        ac = ac / ac[0]; k = lo + int(np.argmax(ac[lo:hi]))
        if ac[k] > 0.45: f0s.append(sr / k)
    return float(np.median(f0s)) if len(f0s) >= 3 else None


def centroide(x, sr=SR):
    if len(x) < 512: return None
    sp = np.abs(np.fft.rfft(x * np.hanning(len(x))))
    fr = np.fft.rfftfreq(len(x), 1 / sr)
    return float(np.sum(fr * sp) / (np.sum(sp) + 1e-9))


# ---------- áudio ----------
def decode(path, sr=SR):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"])
    return np.frombuffer(raw, dtype=np.float32).copy()


def apara(x, sr=SR, limiar=-45.0, margem=0.012):
    hop = sr // 200; n = len(x) // hop
    if n == 0: return x
    r = 20 * np.log10(np.sqrt(np.mean(x[:n * hop].reshape(n, hop) ** 2, axis=1)) + 1e-9)
    v = np.where(r > limiar)[0]
    if len(v) == 0: return x
    a = max(0, v[0] * hop - int(margem * sr)); b = min(len(x), (v[-1] + 1) * hop + int(margem * sr))
    return x[a:b]


def rubberband(x, tempo=1.0, pitch=1.0, sr=SR):
    if abs(tempo - 1) < 0.01 and abs(pitch - 1) < 0.005: return x
    with tempfile.TemporaryDirectory() as d:
        i, o = os.path.join(d, "i.f32"), os.path.join(d, "o.f32")
        x.astype(np.float32).tofile(i)
        subprocess.check_call(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(sr), "-ac", "1", "-i", i,
                               "-af", f"rubberband=tempo={tempo:.4f}:pitch={pitch:.4f}:formant=preserved,lowpass=f=11500",
                               "-f", "f32le", "-y", o])
        return np.fromfile(o, dtype=np.float32)


def vale(x, i, raio, sr=SR):
    """Índice de menor energia (janelas de 5 ms) a até `raio` s de i: corta a emenda num ponto quieto."""
    hop = sr // 200; a = max(0, i - int(raio * sr)); b = min(len(x), i + int(raio * sr))
    if b - a < 2 * hop: return i
    n = (b - a) // hop
    e = np.mean(x[a:a + n * hop].reshape(n, hop) ** 2, axis=1)
    return a + int(np.argmin(e)) * hop + hop // 2


def vale_entre(x, lo, hi, sr=SR, prefere="fim"):
    """Ponto mais quieto (janelas de 5 ms) entre lo e hi; empate perto de hi ("fim") ou de lo ("inicio")."""
    hop = sr // 200; lo = max(0, lo); hi = min(len(x), hi)
    if hi - lo < 2 * hop: return (lo + hi) // 2
    n = (hi - lo) // hop
    e = np.mean(x[lo:lo + n * hop].reshape(n, hop) ** 2, axis=1)
    lim = e.min() * 1.5 + 1e-9
    cand = np.where(e <= lim)[0]
    k = cand[-1] if prefere == "fim" else cand[0]
    return lo + int(k) * hop + hop // 2


def limites(x, words, i0, i1, sr=SR):
    """Corte do termo: do silêncio entre a palavra anterior e o termo até o silêncio entre o termo e a próxima.
    Os limites do WordBoundary terminam cedo: a cauda da consoante final ("framewor-k") ficava e soava
    como sílaba a mais ("framework que conhecido"); por isso o fim vai até perto do começo da próxima palavra."""
    t0, t1 = words[i0][0], words[i1][1]
    ant = words[i0 - 1][1] if i0 > 0 else max(0.0, t0 - 0.08)
    prox = words[i1 + 1][0] if i1 + 1 < len(words) else min(len(x) / sr, t1 + 0.25)
    a = vale_entre(x, int((min(ant, t0) - 0.01) * sr), int((t0 + 0.02) * sr), sr, "inicio")
    b = vale_entre(x, int((t1 - 0.02) * sr), int((max(prox, t1) + 0.01) * sr), sr, "fim")
    return a, b


async def sintetiza(texto, voz, rate, pitch="+0Hz", tries=5):
    import edge_tts
    for n in range(tries):
        try:
            fd, mp3 = tempfile.mkstemp(suffix=".mp3"); os.close(fd)
            c = edge_tts.Communicate(texto, voz, rate=rate, pitch=pitch, boundary="WordBoundary")
            words = []
            with open(mp3, "wb") as f:
                async for ch in c.stream():
                    if ch["type"] == "audio": f.write(ch["data"])
                    elif ch["type"] == "WordBoundary":
                        words.append((ch["offset"] / 1e7, (ch["offset"] + ch["duration"]) / 1e7, ch["text"]))
            if os.path.getsize(mp3) < 800: raise RuntimeError("sem áudio")
            x = decode(mp3); os.remove(mp3)
            return x, words
        except Exception as e:
            if n == tries - 1: raise
            await asyncio.sleep(3 * (n + 1))


_CACHE = {}


PORTADORA = ("We use", "every day.")  # frase en neutra: o termo sai com a pronúncia de fala corrida


async def audio_termo(termo, voz, rate, pitch="+0Hz", portadora=False):
    """Termo dito pela voz en, isolado (padrão). `portadora=True` (experimental, pior no teste de 2026-11-14): a voz
    diz "We use <termo> every day." e o termo é recortado; o recorte levou o "z" de "use" junto ("Stoken",
    "Sprunt") e os acertos caíram de 18/20 para 12/20."""
    k = (termo, voz, rate, pitch, portadora)
    if k not in _CACHE:
        if portadora:
            x, w = await sintetiza(f"{PORTADORA[0]} {termo} {PORTADORA[1]}", voz, rate, pitch)
            n0 = len(PORTADORA[0].split()); n1 = n0 + len(termo.split()) - 1
            seg = None
            if len(w) > n1 + 1:
                a, b = limites(x, w, n0, n1)
                seg = x[a:b]
            if seg is None or len(seg) < int(0.1 * SR):
                x, _ = await sintetiza(termo, voz, rate, pitch); seg = apara(x)
            _CACHE[k] = seg.astype(np.float32)
        else:
            x, _ = await sintetiza(termo, voz, rate, pitch)
            _CACHE[k] = apara(x)
    return _CACHE[k]


async def audios_termos(termos, voz, rate, f0_pt):
    """Áudio en de cada termo com o tom já ajustado no próprio serviço (prosody pitch em Hz, mais limpo que
    deslocar depois): 1ª passada mede a F0 da voz en, 2ª sintetiza com +/- (F0 pt - F0 en), até ±50 Hz.
    Devolve ({termo: áudio}, f0_en_original, pitch usado)."""
    base = {t: await audio_termo(t, voz, rate) for t in termos}
    f0_en = f0_de(base.values()) if base else None
    if not (f0_en and f0_pt): return base, f0_en, "+0Hz"
    hz = int(round(max(-50, min(50, f0_pt - f0_en))))
    if abs(hz) < 4: return base, f0_en, "+0Hz"
    p = f"{hz:+d}Hz"
    return {t: await audio_termo(t, voz, rate, p) for t in termos}, f0_en, p


def f0_de(audios, sr=SR):
    """F0 mediana de um conjunto de áudios (a voz como um todo: mais estável que palavra a palavra)."""
    return f0_mediana(np.concatenate(list(audios)), sr) if audios else None


def _tok(s):
    return re.sub(r"[^\w]", "", s.lower())


def spans(words, termos):
    """[(termo, i0, i1, t0, t1)] casando os tokens do termo com os limites de palavra do TTS."""
    toks = [_tok(w[2]) for w in words]; out = []; usados = set()
    for t in sorted(termos, key=len, reverse=True):
        alvo = [_tok(p) for p in t.split()]
        juntos = "".join(alvo)
        for i in range(len(toks)):
            if i in usados: continue
            for k in (len(alvo), 1):  # "vibe coding" em 2 palavras, ou colado num só limite
                cand = toks[i:i + k]
                if (k == len(alvo) and cand == alvo) or (k == 1 and cand and cand[0] == juntos):
                    if not any(j in usados for j in range(i, i + k)):
                        out.append((t, i, i + k - 1, words[i][0], words[i + k - 1][1])); usados.update(range(i, i + k))
                    break
    return sorted(out, key=lambda z: z[3])


def emendar(x, words, termos_audio, xfade=0.012, sr=SR, ajusta_tom=True, ajusta_ritmo=True, f0_en_voz=None, f0_pt_voz=None):
    """Troca cada termo da fala pt (x, words) pelo áudio en correspondente. termos_audio: {termo: áudio}.
    Tom: razão entre a F0 da voz pt e a da voz en (medidas no conjunto, não palavra a palavra), até ±3 semitons.
    Devolve (áudio, words reajustados, relatório por emenda)."""
    sp = spans(words, list(termos_audio))
    if not sp: return x, words, []
    partes, rel, cur, desloc = [], [], 0, 0.0
    novos = list(words); nf = int(xfade * sr)
    f0_pt = f0_pt_voz or f0_mediana(x, sr)
    f0_en = f0_en_voz or f0_de(termos_audio.values(), sr)
    pitch = 1.0
    if ajusta_tom and f0_en and f0_pt:
        pitch = float(np.clip(f0_pt / f0_en, 2 ** (-3 / 12), 2 ** (3 / 12)))
    for termo, i0, i1, t0, t1 in sp:
        a, b = limites(x, words, i0, i1, sr); a = max(cur, a)
        if b - a < int(0.08 * sr): continue
        orig = x[a:b]; en = termos_audio[termo].copy()
        tempo = 1.0
        if ajusta_ritmo:
            tempo = float(np.clip((len(en) / sr) / max(0.12, (b - a) / sr), 0.85, 1.2))
        en = rubberband(en, tempo, pitch, sr)
        alvo_db = rms_voz_db(orig, sr); en_db = rms_voz_db(en, sr)
        en = (en * (10 ** ((alvo_db - en_db) / 20))).astype(np.float32)
        # crossfade (igual potência) com o próprio trecho pt removido, nas duas pontas: sem degrau = sem clique
        k = min(nf, len(en) // 3, len(orig) // 3)
        if k > 8:
            up = np.sin(np.linspace(0, np.pi / 2, k, dtype=np.float32)); dn = np.cos(np.linspace(0, np.pi / 2, k, dtype=np.float32))
            en[:k] = en[:k] * up + orig[:k] * dn
            en[-k:] = en[-k:] * dn + orig[-k:] * up
        partes += [x[cur:a], en]; cur = b
        delta = len(en) / sr - (b - a) / sr
        viz_a = x[max(0, a - int(0.25 * sr)):a]; viz_b = x[b:b + int(0.25 * sr)]
        viz = np.concatenate([viz_a, viz_b])
        rel.append({"termo": termo, "dur_pt": round((b - a) / sr, 3), "dur_en": round(len(en) / sr, 3),
                    "tempo": round(tempo, 3), "pitch": round(pitch, 3),
                    "salto_db": round(rms_voz_db(en, sr) - rms_voz_db(viz, sr), 2),
                    "f0_en": round(f0_mediana(en, sr) or 0, 1), "f0_viz": round(f0_mediana(viz, sr) or 0, 1),
                    "centroide_en": round(centroide(en, sr) or 0), "centroide_viz": round(centroide(viz, sr) or 0)})
        # palavras: o termo ocupa o novo trecho; as seguintes andam delta
        ta, tb = a / sr + desloc, a / sr + desloc + len(en) / sr
        for j in range(len(novos)):
            s0, s1, w = words[j]
            if i0 <= j <= i1:
                novos[j] = (ta + (tb - ta) * (j - i0) / (i1 - i0 + 1), ta + (tb - ta) * (j - i0 + 1) / (i1 - i0 + 1), w)
            elif s0 >= t1:
                novos[j] = (novos[j][0] + delta, novos[j][1] + delta, w)
        desloc += delta
    partes.append(x[cur:])
    return np.concatenate(partes).astype(np.float32), novos, rel


def mede_sem_emenda(x, words, termos, sr=SR):
    """As mesmas medidas da emenda, mas no termo dito pela própria voz pt: a variação natural (referência)."""
    rel = []
    for termo, i0, i1, t0, t1 in spans(words, termos):
        a, b = limites(x, words, i0, i1, sr)
        if b - a < int(0.08 * sr): continue
        en = x[a:b]; viz = np.concatenate([x[max(0, a - int(0.25 * sr)):a], x[b:b + int(0.25 * sr)]])
        rel.append({"termo": termo, "salto_db": round(rms_voz_db(en, sr) - rms_voz_db(viz, sr), 2),
                    "f0_en": round(f0_mediana(en, sr) or 0, 1), "f0_viz": round(f0_mediana(viz, sr) or 0, 1),
                    "centroide_en": round(centroide(en, sr) or 0), "centroide_viz": round(centroide(viz, sr) or 0)})
    return rel
