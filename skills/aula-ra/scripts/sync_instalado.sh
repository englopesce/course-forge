#!/usr/bin/env bash
# Uso: sync_instalado.sh [copia_de_trabalho] [pasta_instalada]
# Copia os arquivos auxiliares (não o SKILL.md) da cópia de trabalho para as skills instaladas.
set -euo pipefail
SRC="${1:-/workspace/aula-ra/skills}"; DST="${2:-/home/box/agent-data/workflows}"
for d in aula-ra youtube-legendas roteiro-didatico-ptbr narracao-tts-ptbr trechos-youtube-credito pagina-html-gsap video-hyperframes; do
  ( cd "$SRC/$d" && find . -type f ! -name SKILL.md ! -path '*/__pycache__/*' -print0 ) | while IFS= read -r -d '' f; do
    mkdir -p "$DST/$d/$(dirname "$f")"; cp -p "$SRC/$d/$f" "$DST/$d/$f"; done
done
diff -rq --exclude __pycache__ --exclude SKILL.md --exclude .git "$SRC" "$DST" 2>&1 | grep -v "^Only in $DST" | grep -v "^Only in $SRC: \.git" || echo "sincronizado"
