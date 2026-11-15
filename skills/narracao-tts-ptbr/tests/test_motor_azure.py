#!/usr/bin/env python3
"""Testes unitários do motor Azure (sem chamar o serviço; mocks)."""
from __future__ import annotations

import io
import json
import os
import sys
import time
from datetime import timedelta
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import motor_azure as az  # noqa: E402


CHAVE = "AZUREKEY-unit-test-nao-e-real-abc123"
REGIAO = "westus2-unit-test"


def test_monta_ssml_rate_voz_e_escape():
    ssml = az.monta_ssml('Use A & B, depois <tag> e "aspas".', "pt-BR-FranciscaNeural", "-5%")
    assert 'xml:lang="pt-BR"' in ssml
    assert 'name="pt-BR-FranciscaNeural"' in ssml
    assert '<prosody rate="-5%">' in ssml
    assert "&amp;" in ssml
    assert "&lt;tag&gt;" in ssml
    assert "&quot;aspas&quot;" in ssml
    assert "<tag>" not in ssml
    assert "A & B" not in ssml
    assert ssml.startswith("<speak ") and ssml.endswith("</speak>")


def test_xml_escape_apos():
    assert az.xml_escape("d'água") == "d&apos;água"


def test_idioma_da_voz():
    assert az.idioma_da_voz("pt-BR-FranciscaNeural") == "pt-BR"
    assert az.idioma_da_voz("en-US-AvaNeural") == "en-US"
    assert az.idioma_da_voz("Francisca") == "pt-BR"


def test_resolve_motor_ordem_e_padrao(monkeypatch):
    monkeypatch.delenv("TTS_MOTOR", raising=False)
    assert az.resolve_motor() == "edge"
    assert az.resolve_motor(config="azure") == "azure"
    monkeypatch.setenv("TTS_MOTOR", "azure")
    assert az.resolve_motor(config="edge") == "azure"  # env vence config
    assert az.resolve_motor(cli="edge", config="azure") == "edge"  # cli vence env
    with pytest.raises(SystemExit):
        az.resolve_motor(cli="google")


def test_credenciais_faltando(monkeypatch):
    monkeypatch.delenv("AZURE_SPEECH_KEY", raising=False)
    monkeypatch.delenv("AZURE_SPEECH_REGION", raising=False)
    with pytest.raises(az.AzureTtsErro) as ei:
        az.credenciais()
    msg = str(ei.value)
    assert "AZURE_SPEECH_KEY" in msg and "AZURE_SPEECH_REGION" in msg
    assert "Faltando" in msg


def test_credenciais_ok_e_redige(monkeypatch):
    monkeypatch.setenv("AZURE_SPEECH_KEY", CHAVE)
    monkeypatch.setenv("AZURE_SPEECH_REGION", REGIAO)
    k, r = az.credenciais()
    assert k == CHAVE and r == REGIAO
    bruto = f"falhou em https://{REGIAO}.tts.speech.microsoft.com com {CHAVE}"
    limpo = az.redige(bruto, CHAVE, REGIAO)
    assert CHAVE not in limpo and REGIAO not in limpo
    assert "[AZURE_SPEECH_KEY]" in limpo
    assert "[AZURE_SPEECH_REGION]" in limpo


def test_ticks_e_duration():
    assert az.ticks_para_s(10_000_000) == 1.0
    assert az.ticks_para_s(1_500_000) == 0.15
    assert az.duration_para_s(timedelta(milliseconds=250)) == pytest.approx(0.25)
    assert az.duration_para_s(2_000_000) == pytest.approx(0.2)  # ticks
    assert az.duration_para_s(None) == 0.0


def test_eh_palavra_filtra_pontuacao():
    assert az.eh_palavra("aula") is True
    assert az.eh_palavra(".") is False
    assert az.eh_palavra("...", boundary_type="Punctuation") is False
    assert az.eh_palavra("Fim", boundary_type="Sentence") is False
    assert az.eh_palavra("IA", boundary_type="Word") is True


class _Evt:
    def __init__(self, text, offset_ticks, duration, btype="Word"):
        self.text = text
        self.audio_offset = offset_ticks
        self.duration = duration
        self.boundary_type = btype


def test_palavras_de_eventos_word_boundaries():
    evs = [
        _Evt("A", 1_000_000, timedelta(milliseconds=200)),          # 0.10–0.30
        _Evt(".", 3_000_000, timedelta(milliseconds=50), "Punctuation"),
        _Evt("aula", 4_000_000, timedelta(milliseconds=400)),       # 0.40–0.80
    ]
    words = az.palavras_de_eventos(evs)
    assert len(words) == 2
    assert words[0][0] == pytest.approx(0.1) and words[0][1] == pytest.approx(0.3) and words[0][2] == "A"
    assert words[1][0] == pytest.approx(0.4) and words[1][1] == pytest.approx(0.8) and words[1][2] == "aula"


def test_palavras_por_duracao_soma_e_conta():
    words = az.palavras_por_duracao("Oi, mundo novo", 1.0)
    assert len(words) == 3
    assert words[0][0] == 0.0
    assert words[-1][1] == pytest.approx(1.0)
    assert [w[2] for w in words] == ["Oi,", "mundo", "novo"]
    # palavra maior leva mais tempo
    d0 = words[0][1] - words[0][0]
    d1 = words[1][1] - words[1][0]
    assert d1 > d0


def test_chave_cache_inclui_motor():
    a = az.chave_cache("edge", "pt-BR-FranciscaNeural", "-5%", "Oi.")
    b = az.chave_cache("azure", "pt-BR-FranciscaNeural", "-5%", "Oi.")
    c = az.chave_cache("azure", "pt-BR-FranciscaNeural", "-5%", "Oi!")
    assert a != b != c and a != c


def test_garante_metadado_limpo(monkeypatch):
    monkeypatch.setenv("AZURE_SPEECH_KEY", CHAVE)
    monkeypatch.setenv("AZURE_SPEECH_REGION", REGIAO)
    limpo = {"motor": "azure", "voice": "pt-BR-FranciscaNeural", "rate": "-5%"}
    assert az.garante_metadado_limpo(limpo) is limpo
    with pytest.raises(az.AzureTtsErro, match="chave"):
        az.garante_metadado_limpo({"segredo": CHAVE})
    with pytest.raises(az.AzureTtsErro, match="região"):
        az.garante_metadado_limpo({"onde": REGIAO})


def test_cache_roundtrip(tmp_path):
    mp3 = tmp_path / "fala.mp3"
    mp3.write_bytes(b"M" * 1500)
    words = [(0.0, 0.4, "Oi")]
    az.grava_cache(str(tmp_path / "c"), "azure", "pt-BR-FranciscaNeural", "-5%", "Oi.", str(mp3), words)
    dest = tmp_path / "copia.mp3"
    hit = az.le_cache(str(tmp_path / "c"), "azure", "pt-BR-FranciscaNeural", "-5%", "Oi.")
    assert hit is not None
    src, w, ident = hit
    assert w == words
    # motor diferente = miss
    assert az.le_cache(str(tmp_path / "c"), "edge", "pt-BR-FranciscaNeural", "-5%", "Oi.") is None


class _HTTPError(Exception):
    def __init__(self, code, reason, body=b"", headers=None):
        self.code = code
        self.reason = reason
        self.fp = io.BytesIO(body)
        self.headers = headers or {}

    def read(self):
        return self.fp.read()


def test_sintetiza_rest_sucesso_escreve_mp3_e_ssml(tmp_path, monkeypatch):
    visto = {}

    class _Resp:
        def __enter__(self):
            return self
        def __exit__(self, *a):
            return False
        def read(self):
            return b"ID3FAKEAUDIO" + b"\x00" * 1200

    def fake_urlopen(req, timeout=60):
        visto["url"] = req.full_url
        visto["headers"] = {k: v for k, v in req.header_items()}
        visto["body"] = req.data.decode("utf-8")
        return _Resp()

    monkeypatch.setattr(az.urllib.request, "urlopen", fake_urlopen)
    dest = tmp_path / "out.mp3"
    words = az.sintetiza_rest("A & B.", "pt-BR-FranciscaNeural", "-5%", str(dest), CHAVE, REGIAO)
    assert words == []
    assert dest.is_file() and dest.stat().st_size >= 1000
    assert REGIAO in visto["url"]  # a URL interna usa a região; não vai a log
    assert visto["headers"]["Ocp-apim-subscription-key"] == CHAVE or visto["headers"].get("Ocp-Apim-Subscription-Key") == CHAVE or any(CHAVE in v for v in visto["headers"].values())
    assert "<prosody rate=\"-5%\">" in visto["body"]
    assert "A &amp; B." in visto["body"]
    assert "audio-48khz-192kbitrate-mono-mp3" in str(visto["headers"].values()).lower() or any(
        "audio-48khz-192kbitrate-mono-mp3" in v for v in visto["headers"].values()
    )


def test_sintetiza_rest_429_e_erro_redigido(tmp_path, monkeypatch):
    def boom(req, timeout=60):
        raise az.urllib.error.HTTPError(
            req.full_url, 429, "Too Many Requests",
            {"Retry-After": "7"}, io.BytesIO(f"key={CHAVE} region={REGIAO}".encode()),
        )

    monkeypatch.setattr(az.urllib.request, "urlopen", boom)
    dest = tmp_path / "out.mp3"
    with pytest.raises(az.AzureTtsErro) as ei:
        az.sintetiza_rest("Oi.", "pt-BR-FranciscaNeural", "-5%", str(dest), CHAVE, REGIAO)
    err = ei.value
    assert err.status == 429 and err.retryable is True
    assert err.retry_after == 7.0
    assert CHAVE not in str(err)
    assert REGIAO not in str(err)


def test_sintetiza_retry_backoff_429(tmp_path, monkeypatch):
    chamadas = {"n": 0}

    def fake_sintetiza_rest(texto, voice, rate, dest, key, region, timeout=60):
        chamadas["n"] += 1
        if chamadas["n"] < 3:
            raise az.AzureTtsErro("ocupado", status=429, retryable=True, retry_after=0)
        Path(dest).write_bytes(b"A" * 1500)
        return []

    sleeps = []
    monkeypatch.setattr(az, "sintetiza_rest", fake_sintetiza_rest)
    monkeypatch.setattr(az, "tem_sdk", lambda: False)
    monkeypatch.setattr(az, "_espera", lambda n, ra=None: sleeps.append((n, ra)))
    monkeypatch.setenv("AZURE_SPEECH_KEY", CHAVE)
    monkeypatch.setenv("AZURE_SPEECH_REGION", REGIAO)
    dest = tmp_path / "out.mp3"
    words = az.sintetiza("Oi.", "pt-BR-FranciscaNeural", "-5%", str(dest), forcar="rest")
    assert words == []
    assert chamadas["n"] == 3
    assert dest.is_file()
    assert sleeps  # houve espera entre as falhas


def test_sintetiza_401_nao_retenta(tmp_path, monkeypatch):
    chamadas = {"n": 0}

    def fake_rest(*a, **k):
        chamadas["n"] += 1
        raise az.AzureTtsErro("não autorizado", status=401, retryable=False)

    monkeypatch.setattr(az, "sintetiza_rest", fake_rest)
    monkeypatch.setattr(az, "tem_sdk", lambda: False)
    monkeypatch.setenv("AZURE_SPEECH_KEY", CHAVE)
    monkeypatch.setenv("AZURE_SPEECH_REGION", REGIAO)
    with pytest.raises(az.AzureTtsErro, match="não autorizado"):
        az.sintetiza("Oi.", "pt-BR-FranciscaNeural", "-5%", str(tmp_path / "x.mp3"), forcar="rest")
    assert chamadas["n"] == 1


def test_sintetiza_usa_cache_e_nao_chama_rede(tmp_path, monkeypatch):
    cache = tmp_path / "c"
    src = tmp_path / "orig.mp3"
    src.write_bytes(b"B" * 1500)
    az.grava_cache(str(cache), "azure", "pt-BR-FranciscaNeural", "-5%", "Oi.", str(src), [(0.0, 0.3, "Oi")])

    def boom(*a, **k):
        raise AssertionError("não deveria chamar a rede")

    monkeypatch.setattr(az, "sintetiza_rest", boom)
    monkeypatch.setattr(az, "sintetiza_sdk", boom)
    monkeypatch.setenv("AZURE_SPEECH_KEY", CHAVE)
    monkeypatch.setenv("AZURE_SPEECH_REGION", REGIAO)
    dest = tmp_path / "out.mp3"
    words = az.sintetiza("Oi.", "pt-BR-FranciscaNeural", "-5%", str(dest), cache_dir=str(cache), forcar="rest")
    assert words == [(0.0, 0.3, "Oi")]
    assert dest.read_bytes() == src.read_bytes()


def test_srt_a_partir_de_word_boundaries():
    """Simula o agrupamento de legendas a partir dos limites de palavra (como o tts_ptbr faz)."""
    sys.path.insert(0, str(SCRIPTS))
    import tts_ptbr
    words = [(0.0, 0.2, "Esta"), (0.2, 0.45, "é"), (0.45, 0.9, "uma"), (0.9, 1.4, "frase.")]
    blocos = tts_ptbr.chunk_words(words, "Esta é uma frase.")
    assert blocos
    # a frase inteira cabe num bloco
    texto = " ".join(w[2] for blk in blocos for w in blk)
    assert texto == "Esta é uma frase."
    s0, s1 = blocos[0][0][0], blocos[-1][-1][1]
    assert s0 == 0.0 and s1 == pytest.approx(1.4)
