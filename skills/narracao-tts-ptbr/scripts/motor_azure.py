#!/usr/bin/env python3
"""Motor Azure Speech para narracao-tts-ptbr (v1.8.0).

Sintetiza uma frase com as mesmas vozes Neural pt-BR do edge-tts (ex.:
pt-BR-FranciscaNeural), ritmo via SSML <prosody rate="-5%"> e devolve
limites de palavra no mesmo formato do edge-tts: [(inicio_s, fim_s, texto)].

Credenciais: somente AZURE_SPEECH_KEY e AZURE_SPEECH_REGION no ambiente.
Nunca grave chave ou região no repositório, em yaml, em logs ou em metadados.

Usa o Speech SDK (azure-cognitiveservices-speech) quando instalado, porque
ele entrega WordBoundary; senão cai no REST TTS (áudio) e estima os tempos
das palavras pela duração da frase. Retry com backoff em 429 e 5xx.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.request
from xml.sax.saxutils import escape as _xml_escape

MOTORES = ("edge", "azure")
ENV_KEY = "AZURE_SPEECH_KEY"
ENV_REGION = "AZURE_SPEECH_REGION"
ENV_MOTOR = "TTS_MOTOR"
OUTPUT_FORMAT = "audio-48khz-192kbitrate-mono-mp3"
USER_AGENT = "narracao-tts-ptbr/1.8.0"
TENTATIVAS = 4
# 1 tick = 100 ns = 1e-7 s (documentação do Speech SDK).
TICKS_POR_S = 10_000_000

MSG_CREDENCIAL = (
    "Motor Azure exige as variáveis de ambiente AZURE_SPEECH_KEY e "
    "AZURE_SPEECH_REGION. Não grave a chave nem a região no repositório, "
    "em yaml, em logs ou em metadados."
)


class AzureTtsErro(RuntimeError):
    """Falha no Azure Speech. A mensagem nunca contém a chave nem a região."""

    def __init__(self, msg, status=None, retryable=False, retry_after=None):
        super().__init__(msg)
        self.status = status
        self.retryable = retryable
        self.retry_after = retry_after


def resolve_motor(cli=None, env=None, config=None):
    """Ordem: --motor (cli) > TTS_MOTOR (env) > narracao.motor (config) > edge."""
    for origem in (cli, env if env is not None else os.environ.get(ENV_MOTOR), config):
        if origem is not None and str(origem).strip():
            m = str(origem).strip().lower()
            if m not in MOTORES:
                raise SystemExit(f"motor de narração desconhecido: {m!r} (use edge ou azure)")
            return m
    return "edge"


def credenciais():
    """Lê chave e região do ambiente. Não registre o retorno em log ou arquivo."""
    key = (os.environ.get(ENV_KEY) or "").strip()
    region = (os.environ.get(ENV_REGION) or "").strip()
    if not key or not region:
        faltam = [n for n, v in ((ENV_KEY, key), (ENV_REGION, region)) if not v]
        raise AzureTtsErro(f"{MSG_CREDENCIAL} Faltando: {', '.join(faltam)}.")
    return key, region


def redige(texto, key=None, region=None):
    """Remove chave e região de qualquer texto que vá a log ou exceção."""
    if texto is None:
        return ""
    s = str(texto)
    if key:
        s = s.replace(key, f"[{ENV_KEY}]")
    if region:
        s = s.replace(region, f"[{ENV_REGION}]")
    # URLs regionais comuns do serviço, se a região escapar noutro formato
    s = re.sub(r"https://[a-z0-9-]+\.tts\.speech\.microsoft\.com",
               "https://[AZURE_SPEECH_REGION].tts.speech.microsoft.com", s, flags=re.I)
    s = re.sub(r"https://[a-z0-9-]+\.api\.cognitive\.microsoft\.com",
               "https://[AZURE_SPEECH_REGION].api.cognitive.microsoft.com", s, flags=re.I)
    return s


def idioma_da_voz(voice):
    partes = (voice or "").split("-")
    if len(partes) >= 2 and len(partes[0]) == 2 and len(partes[1]) == 2:
        return f"{partes[0]}-{partes[1]}"
    return "pt-BR"


def xml_escape(texto):
    # quote=True cobre &, <, >, " e '
    return _xml_escape(texto, {"'": "&apos;", '"': "&quot;"})


def monta_ssml(texto, voice, rate, lang=None):
    """SSML com a voz e o ritmo (--rate, ex.: -5%) em <prosody rate>."""
    lang = lang or idioma_da_voz(voice)
    rate = str(rate).strip() or "-5%"
    if not rate.endswith("%") and rate not in {"x-slow", "slow", "medium", "fast", "x-fast"}:
        # multiplicador (0.95) também é válido no Azure; deixamos como veio
        pass
    return (
        f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{xml_escape(lang)}">'
        f'<voice name="{xml_escape(voice)}">'
        f'<prosody rate="{xml_escape(rate)}">{xml_escape(texto)}</prosody>'
        f"</voice></speak>"
    )


def ticks_para_s(ticks):
    return float(ticks) / TICKS_POR_S


def duration_para_s(d):
    if d is None:
        return 0.0
    if hasattr(d, "total_seconds"):
        return float(d.total_seconds())
    # Alguns bindings devolvem ticks (int); valores grandes não são segundos.
    if isinstance(d, (int, float)):
        return float(d) / TICKS_POR_S if d > 10 else float(d)
    return 0.0


def eh_palavra(texto, boundary_type=None):
    t = (texto or "").strip()
    if not t:
        return False
    if re.fullmatch(r"[\W_]+", t, flags=re.UNICODE):
        return False
    if boundary_type is not None:
        nome = str(getattr(boundary_type, "name", boundary_type)).lower()
        if "punctuation" in nome or "sentence" in nome:
            return False
    return True


def evento_para_palavra(evt):
    """Converte um WordBoundary do SDK em (inicio_s, fim_s, texto)."""
    t0 = ticks_para_s(evt.audio_offset)
    dur = duration_para_s(getattr(evt, "duration", None))
    return (t0, t0 + dur, (evt.text or "").strip())


def palavras_de_eventos(eventos):
    out = []
    for ev in eventos:
        texto = getattr(ev, "text", None)
        btype = getattr(ev, "boundary_type", None)
        if not eh_palavra(texto, btype):
            continue
        out.append(evento_para_palavra(ev))
    return out


def palavras_por_duracao(texto, duracao_s):
    """Fallback sem WordBoundary: reparte a duração da frase pelo tamanho das palavras."""
    toks = (texto or "").split()
    if not toks or duracao_s <= 0:
        return []
    pesos = [max(1, len(re.sub(r"[^\wÀ-ÿ]", "", t) or t)) for t in toks]
    total = sum(pesos)
    t = 0.0
    out = []
    for tok, p in zip(toks, pesos):
        d = duracao_s * (p / total)
        out.append((round(t, 6), round(t + d, 6), tok))
        t += d
    return out


def chave_cache(motor, voice, rate, texto):
    h = hashlib.sha256()
    for parte in (motor, voice, rate, texto):
        h.update(b"\0")
        h.update(str(parte).encode("utf-8"))
    return h.hexdigest()


def le_cache(cache_dir, motor, voice, rate, texto):
    if not cache_dir:
        return None
    ident = chave_cache(motor, voice, rate, texto)
    base = os.path.join(cache_dir, ident)
    mp3, meta = base + ".mp3", base + ".json"
    if not (os.path.isfile(mp3) and os.path.isfile(meta) and os.path.getsize(mp3) >= 1000):
        return None
    dados = json.load(open(meta, encoding="utf-8"))
    words = [tuple(w) for w in dados.get("words") or []]
    return mp3, words, ident


def grava_cache(cache_dir, motor, voice, rate, texto, mp3_src, words):
    if not cache_dir:
        return
    os.makedirs(cache_dir, exist_ok=True)
    ident = chave_cache(motor, voice, rate, texto)
    base = os.path.join(cache_dir, ident)
    dest = base + ".mp3"
    if os.path.abspath(mp3_src) != os.path.abspath(dest):
        with open(mp3_src, "rb") as fsrc, open(dest, "wb") as fdst:
            fdst.write(fsrc.read())
    json.dump({"motor": motor, "voice": voice, "rate": rate, "words": words},
              open(base + ".json", "w", encoding="utf-8"), ensure_ascii=False)
    # não inclui o texto completo nem credenciais


def garante_metadado_limpo(obj, key=None, region=None):
    """Garante que um dict/lista a gravar não contém a chave nem a região."""
    key = key or (os.environ.get(ENV_KEY) or "").strip()
    region = region or (os.environ.get(ENV_REGION) or "").strip()
    blob = json.dumps(obj, ensure_ascii=False)
    if key and key in blob:
        raise AzureTtsErro("recusado: a chave do Azure apareceria no metadado da narração")
    if region and region in blob:
        raise AzureTtsErro("recusado: a região do Azure apareceria no metadado da narração")
    return obj


def tem_sdk():
    try:
        import azure.cognitiveservices.speech  # noqa: F401
        return True
    except ImportError:
        return False


def _retry_after(headers):
    if not headers:
        return None
    raw = headers.get("Retry-After") or headers.get("retry-after")
    if not raw:
        return None
    try:
        return max(0.0, float(raw))
    except ValueError:
        return None


def _espera(tentativa, retry_after=None):
    # tentativa é 0-indexada; 2, 4, 8 s (como o edge) ou o Retry-After do 429
    padrao = 2 * (tentativa + 1)
    time.sleep(retry_after if retry_after is not None else padrao)


def sintetiza_rest(texto, voice, rate, dest_mp3, key, region, timeout=60):
    """POST /cognitiveservices/v1 (SSML). Não devolve WordBoundary."""
    ssml = monta_ssml(texto, voice, rate)
    url = f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1"
    req = urllib.request.Request(url, data=ssml.encode("utf-8"), method="POST")
    req.add_header("Ocp-Apim-Subscription-Key", key)
    req.add_header("Content-Type", "application/ssml+xml")
    req.add_header("X-Microsoft-OutputFormat", OUTPUT_FORMAT)
    req.add_header("User-Agent", USER_AGENT)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
    except urllib.error.HTTPError as e:
        corpo = e.read().decode("utf-8", "replace") if e.fp else ""
        retryable = e.code in (429, 500, 502, 503, 504)
        raise AzureTtsErro(
            redige(f"Azure REST TTS HTTP {e.code}: {corpo[:300] or e.reason}", key, region),
            status=e.code, retryable=retryable, retry_after=_retry_after(e.headers),
        ) from None
    except urllib.error.URLError as e:
        raise AzureTtsErro(
            redige(f"Azure REST TTS falhou ao conectar: {e.reason}", key, region),
            retryable=True,
        ) from None
    if not data or len(data) < 1000:
        raise AzureTtsErro("Azure REST TTS devolveu áudio vazio ou curto demais", retryable=True)
    os.makedirs(os.path.dirname(dest_mp3) or ".", exist_ok=True)
    with open(dest_mp3, "wb") as f:
        f.write(data)
    return []  # sem word boundaries; o chamador estima pela duração


def sintetiza_sdk(texto, voice, rate, dest_mp3, key, region):
    """Speech SDK: áudio + WordBoundary (audio_offset em ticks, duration em timedelta)."""
    import azure.cognitiveservices.speech as speechsdk

    ssml = monta_ssml(texto, voice, rate)
    cfg = speechsdk.SpeechConfig(subscription=key, region=region)
    cfg.speech_synthesis_voice_name = voice
    cfg.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Audio48Khz192KBitRateMonoMp3
    )
    eventos = []
    synth = speechsdk.SpeechSynthesizer(speech_config=cfg, audio_config=None)

    def _on_word(evt):
        eventos.append(evt)

    synth.synthesis_word_boundary.connect(_on_word)
    try:
        result = synth.speak_ssml_async(ssml).get()
    finally:
        try:
            synth.synthesis_word_boundary.disconnect_all()
        except Exception:
            pass
        closer = getattr(synth, "close", None)
        if callable(closer):
            try:
                closer()
            except Exception:
                pass

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        data = result.audio_data or b""
        if len(data) < 1000:
            raise AzureTtsErro("Azure Speech SDK devolveu áudio vazio ou curto demais", retryable=True)
        os.makedirs(os.path.dirname(dest_mp3) or ".", exist_ok=True)
        with open(dest_mp3, "wb") as f:
            f.write(data)
        return palavras_de_eventos(eventos)

    detalhe = ""
    status = None
    retryable = True
    if result.reason == speechsdk.ResultReason.Canceled:
        det = result.cancellation_details
        detalhe = getattr(det, "error_details", None) or str(getattr(det, "reason", ""))
        m = re.search(r"\b(429|5\d{2})\b", detalhe or "")
        if m:
            status = int(m.group(1))
        retryable = status in (429, 500, 502, 503, 504) or "429" in (detalhe or "") or not detalhe
    raise AzureTtsErro(
        redige(f"Azure Speech SDK cancelou a síntese: {detalhe or result.reason}", key, region),
        status=status, retryable=retryable,
    )


def sintetiza(texto, voice, rate, dest_mp3, cache_dir=None, tentativas=TENTATIVAS, forcar=None):
    """Sintetiza uma frase. forcar: 'sdk' | 'rest' | None (SDK se instalado, senão REST).

    Devolve lista [(inicio_s, fim_s, texto)] (vazia no REST; o chamador estima).
    """
    key, region = credenciais()
    hit = le_cache(cache_dir, "azure", voice, rate, texto)
    if hit:
        src, words, _ident = hit
        if os.path.abspath(src) != os.path.abspath(dest_mp3):
            os.makedirs(os.path.dirname(dest_mp3) or ".", exist_ok=True)
            with open(src, "rb") as fsrc, open(dest_mp3, "wb") as fdst:
                fdst.write(fsrc.read())
        return words

    modo = forcar or ("sdk" if tem_sdk() else "rest")
    if modo == "sdk" and not tem_sdk():
        raise AzureTtsErro(
            "Motor Azure no modo SDK exige o pacote azure-cognitiveservices-speech "
            "(pip install azure-cognitiveservices-speech). "
            "Sem o SDK, o motor usa o REST automaticamente."
        )
    ultimo = None
    for n in range(tentativas):
        try:
            if modo == "sdk":
                words = sintetiza_sdk(texto, voice, rate, dest_mp3, key, region)
            else:
                words = sintetiza_rest(texto, voice, rate, dest_mp3, key, region)
            grava_cache(cache_dir, "azure", voice, rate, texto, dest_mp3, words)
            return words
        except AzureTtsErro as e:
            ultimo = e
            if not e.retryable or n == tentativas - 1:
                raise
            print(f"  Azure TTS tentativa {n+1} falhou ({e}); repetindo...")
            _espera(n, e.retry_after)
        except Exception as e:
            ultimo = AzureTtsErro(redige(f"{type(e).__name__}: {e}", key, region), retryable=True)
            if n == tentativas - 1:
                raise ultimo from None
            print(f"  Azure TTS tentativa {n+1} falhou ({type(e).__name__}); repetindo...")
            _espera(n)
    raise ultimo
