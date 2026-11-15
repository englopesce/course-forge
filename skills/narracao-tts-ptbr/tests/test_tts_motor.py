#!/usr/bin/env python3
"""Seleção de motor, metadado e caminho edge intacto (sem chamar serviços)."""
from __future__ import annotations

import os
import sys
from pathlib import Path
from unittest import mock

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
AULA_RA = Path(__file__).resolve().parents[2] / "aula-ra" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import motor_azure as az  # noqa: E402
import tts_ptbr  # noqa: E402


def test_synth_edge_chama__synth_e_nao_azure():
    async def fake__synth(text, voice, rate, mp3):
        Path(mp3).write_bytes(b"E" * 1500)
        return [(0.0, 0.4, "Oi")]

    with mock.patch.object(tts_ptbr, "_synth", side_effect=fake__synth) as p_edge, \
         mock.patch.object(az, "sintetiza") as p_az:
        import asyncio
        sem = asyncio.Semaphore(1)
        words = asyncio.run(tts_ptbr.synth("Oi.", "pt-BR-FranciscaNeural", "-5%", "/tmp/_nao", sem, motor="edge"))
        assert words == [(0.0, 0.4, "Oi")]
        assert p_edge.await_count == 1
        p_az.assert_not_called()


def test_synth_azure_chama_motor_e_nao_edge(tmp_path):
    dest = tmp_path / "f.mp3"

    def fake_az(text, voice, rate, mp3, cache_dir=None):
        Path(mp3).write_bytes(b"A" * 1500)
        return [(0.0, 0.5, "Oi")]

    with mock.patch.object(az, "sintetiza", side_effect=fake_az) as p_az, \
         mock.patch.object(tts_ptbr, "_synth") as p_edge:
        import asyncio
        sem = asyncio.Semaphore(1)
        words = asyncio.run(tts_ptbr.synth("Oi.", "pt-BR-FranciscaNeural", "-5%", str(dest), sem, motor="azure"))
        assert words == [(0.0, 0.5, "Oi")]
        p_az.assert_called_once()
        p_edge.assert_not_called()


def test_cli_azure_sem_credencial_erro_claro(tmp_path, monkeypatch, capsys):
    monkeypatch.delenv("AZURE_SPEECH_KEY", raising=False)
    monkeypatch.delenv("AZURE_SPEECH_REGION", raising=False)
    monkeypatch.delenv("TTS_MOTOR", raising=False)
    roteiro = tmp_path / "r.json"
    roteiro.write_text('{"cenas":[{"id":"c1","narracao":"Oi."}]}', encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["tts_ptbr.py", str(roteiro), str(tmp_path / "out"), "--motor", "azure"])
    with pytest.raises(az.AzureTtsErro) as ei:
        tts_ptbr.main()
    assert "AZURE_SPEECH_KEY" in str(ei.value)
    # não chegou a criar a pasta de saída (falha cedo)
    # (pode ter sido criada se a ordem mudar; o importante é a mensagem)


def test_cli_motor_via_env(monkeypatch):
    monkeypatch.setenv("TTS_MOTOR", "azure")
    monkeypatch.delenv("AZURE_SPEECH_KEY", raising=False)
    monkeypatch.delenv("AZURE_SPEECH_REGION", raising=False)
    assert az.resolve_motor(cli=None) == "azure"


def test_pipeline_motor_narracao_padrao_edge_env_vence(monkeypatch, tmp_path):
    sys.path.insert(0, str(AULA_RA))
    import pipeline
    # instância mínima: só precisamos do método, então fabricamos um objeto simples
    class P:
        def narracao_cfg(self):
            return {"voz": "pt-BR-FranciscaNeural"}
    P.motor_narracao = pipeline.Pipeline.motor_narracao
    p = P()
    monkeypatch.delenv("TTS_MOTOR", raising=False)
    assert p.motor_narracao() == "edge"
    # yaml
    p.narracao_cfg = lambda: {"motor": "azure"}
    assert p.motor_narracao() == "azure"
    monkeypatch.setenv("TTS_MOTOR", "edge")
    assert p.motor_narracao() == "edge"  # env vence yaml


def test_apara_com_words_vazias_nao_quebra():
    import numpy as np
    x = np.zeros(tts_ptbr.SR, dtype=np.float32)
    x[int(0.2 * tts_ptbr.SR):int(0.6 * tts_ptbr.SR)] = 0.2
    y, desl = tts_ptbr.apara(x, [])
    assert len(y) > 0
    words = az.palavras_por_duracao("Uma frase curta.", len(y) / tts_ptbr.SR)
    assert len(words) == 3


def test_narracao_cfg_hashable_edge_igual_ausente():
    import sys
    sys.path.insert(0, str(AULA_RA))
    import pipeline
    base = {"voz": "pt-BR-FranciscaNeural", "rate": "-5%"}
    assert pipeline.Pipeline.narracao_cfg_hashable(base) == base
    assert pipeline.Pipeline.narracao_cfg_hashable({**base, "motor": "edge"}) == base
    assert pipeline.Pipeline.narracao_cfg_hashable({**base, "motor": ""}) == base
    az = pipeline.Pipeline.narracao_cfg_hashable({**base, "motor": "azure"})
    assert az["motor"] == "azure"
