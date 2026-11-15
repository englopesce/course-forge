#!/usr/bin/env bash
# Copia os arquivos auxiliares (não o SKILL.md) da cópia de trabalho para as skills instaladas.
set -euo pipefail
SRC=/workspace/aula-ra/skills; DST=/home/box/agent-data/workflows
for d in aula-ra youtube-legendas roteiro-didatico-ptbr narracao-tts-ptbr trechos-youtube-credito pagina-html-gsap video-hyperframes codigo-exemplo-aula curso-a-partir-de-ementa; do
  ( cd "$SRC/$d" && find . -type f ! -name SKILL.md ! -path '*/__pycache__/*' -print0 ) | while IFS= read -r -d '' f; do
    mkdir -p "$DST/$d/$(dirname "$f")"; cp -p "$SRC/$d/$f" "$DST/$d/$f"; done
done
diff -rq --exclude __pycache__ --exclude SKILL.md --exclude .git "$SRC" "$DST" 2>&1 | grep -v "^Only in $DST" | grep -v "^Only in $SRC: \.git" || echo "sincronizado"
