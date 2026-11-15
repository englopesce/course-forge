#!/usr/bin/env bash
# Lista vozes Neural em português.
# Padrão: edge-tts. Com TTS_MOTOR=azure (ou --azure): lista do Azure Speech
# (exige AZURE_SPEECH_KEY e AZURE_SPEECH_REGION; a chave não é impressa).
# Uso: list_voices.sh [prefixo] [--azure]   (padrão de prefixo: pt-)
set -euo pipefail
PREFIX="${1:-pt-}"
AZURE=0
for a in "$@"; do
  [ "$a" = "--azure" ] && AZURE=1
  case "$a" in pt-|pt-*) PREFIX="$a" ;; esac
done
if [ "${TTS_MOTOR:-}" = "azure" ] || [ "$AZURE" = 1 ]; then
  if [ -z "${AZURE_SPEECH_KEY:-}" ] || [ -z "${AZURE_SPEECH_REGION:-}" ]; then
    echo "Motor Azure exige as variáveis de ambiente AZURE_SPEECH_KEY e AZURE_SPEECH_REGION." >&2
    exit 2
  fi
  python3 - << 'PY' "$PREFIX"
import json, os, sys, urllib.request
prefix = sys.argv[1]
key, region = os.environ["AZURE_SPEECH_KEY"], os.environ["AZURE_SPEECH_REGION"]
url = f"https://{region}.tts.speech.microsoft.com/cognitiveservices/voices/list"
req = urllib.request.Request(url)
req.add_header("Ocp-Apim-Subscription-Key", key)
with urllib.request.urlopen(req, timeout=30) as resp:
    voices = json.loads(resp.read().decode("utf-8"))
for v in voices:
    short = v.get("ShortName") or v.get("Name") or ""
    if short.lower().startswith(prefix.lower()):
        locale = v.get("Locale", "")
        gender = v.get("Gender", "")
        print(f"{short:40} {locale:8} {gender}")
PY
else
  EDGE="${EDGE_TTS:-$(command -v edge-tts || echo ./venv/bin/edge-tts)}"
  "$EDGE" --list-voices | grep -i "^${PREFIX}"
fi
