#!/usr/bin/env bash
# Renderiza um projeto HyperFrames e grava as legendas. Uso:
#   render.sh projeto_hf/ legendas.srt saida.mp4 [fonte] [tamanho] [versao_hyperframes]
set -euo pipefail
PROJ="$1"; SRT="$2"; OUT="$3"; FONT="${4:-Inter}"; SIZE="${5:-18}"; HFV="${6:-0.9.43}"
HERE="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)/sem_legenda.mp4"
( cd "$PROJ" && npx -y "hyperframes@${HFV}" check ) | grep -E "Check (passed|failed)|✗|error\(s\)" || true
# a captura paralela às vezes cancela os workers no meio ("Parallel worker cancelled"): tenta de novo até 2 vezes
for tentativa in 1 2 3; do
  ( cd "$PROJ" && npx -y "hyperframes@${HFV}" render -q standard -o "$TMP" ) | grep -E "Render complete|rendered in|rror" || true
  [ -s "$TMP" ] && break
  echo "render falhou (tentativa $tentativa)"; sleep 5
done
[ -s "$TMP" ] || { echo "render falhou"; exit 1; }
"$HERE/burn_subs.sh" "$TMP" "$SRT" "$OUT" "$FONT" "$SIZE"
