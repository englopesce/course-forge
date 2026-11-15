#!/usr/bin/env bash
# Lista vozes Neural em português do edge-tts. Uso: list_voices.sh [prefixo]   (padrão pt-)
EDGE="${EDGE_TTS:-$(command -v edge-tts || echo ./venv/bin/edge-tts)}"
"$EDGE" --list-voices | grep -i "^${1:-pt-}"
