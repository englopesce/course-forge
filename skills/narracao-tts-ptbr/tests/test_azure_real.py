#!/usr/bin/env python3
"""Teste real curto do Azure Speech + conferência Whisper. Pulado se não houver chave."""
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

TEM_CHAVE = bool(os.environ.get("AZURE_SPEECH_KEY") and os.environ.get("AZURE_SPEECH_REGION"))
pytestmark = pytest.mark.skipif(not TEM_CHAVE, reason="AZURE_SPEECH_KEY/REGION ausentes; teste real pendente")

FRASE = "Esta é uma frase curta de teste da voz Francisca."


def test_azure_uma_frase_e_whisper():
    import motor_azure as az
    sys.path.insert(0, str(SCRIPTS))
    # sintetiza uma frase e confere com check_voice
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        roteiro = {"cenas": [{"id": "c1", "narracao": FRASE}]}
        (td / "roteiro.json").write_text(json.dumps(roteiro, ensure_ascii=False), encoding="utf-8")
        saida = td / "saida"
        saida.mkdir()
        # usa o fluxo completo do tts_ptbr (pausa, wav, srt, timings)
        import subprocess
        cmd = [sys.executable, str(SCRIPTS / "tts_ptbr.py"), str(td / "roteiro.json"), str(saida),
               "--motor", "azure", "--voice", "pt-BR-FranciscaNeural", "--rate=-5%",
               "--pausa-frase-ms", "400", "--paralelo", "1"]
        subprocess.check_call(cmd)
        timings = json.loads((saida / "timings.json").read_text(encoding="utf-8"))
        assert timings["motor"] == "azure"
        assert timings["voice"] == "pt-BR-FranciscaNeural"
        assert timings["rate"] == "-5%"
        assert "AZURE_SPEECH_KEY" not in json.dumps(timings)
        assert os.environ["AZURE_SPEECH_REGION"] not in json.dumps(timings)
        assert (saida / "narracao.wav").is_file()
        assert (saida / "narracao.srt").is_file()
        rel = saida / "voz.json"
        subprocess.check_call([
            sys.executable, str(SCRIPTS / "check_voice.py"),
            str(td / "roteiro.json"), str(saida / "narracao.wav"),
            "--timings", str(saida / "timings.json"),
            "--model", "small", "--json", str(rel),
        ])
        voz = json.loads(rel.read_text(encoding="utf-8"))
        assert voz.get("motor") == "azure"
        # frase curta e limpa: WER deve ser baixo; não falhamos o teste por um
        # escorregão do Whisper, só registramos.
        print(f"WER real Azure: {voz['wer']:.1%}  transcrição: {voz['transcricao']!r}")
        assert voz["wer"] <= 0.25, f"WER alto demais no teste real: {voz['wer']}"
