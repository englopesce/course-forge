#!/usr/bin/env bash
# Grava (burn-in) legendas SRT num MP4 com ffmpeg/libass, estilo legível para TV/projetor.
# Uso: burn_subs.sh entrada.mp4 legendas.srt saida.mp4 [fonte] [tamanho]
# Posição: SUB_MARGINV (padrão 22, na escala PlayResY=288 do libass). No 9:16 o pipeline usa ≈48
# (legenda logo abaixo do trecho, na área livre) e tamanho ≈9.
# A fonte precisa existir no sistema (fc-list) e ter acentos (Inter, Noto Sans, Open Sans...).
set -euo pipefail
IN="$1"; SRT="$2"; OUT="$3"; FONT="${4:-Inter}"; SIZE="${5:-18}"; MV="${SUB_MARGINV:-22}"
# FontSize do libass é relativo a PlayResY=288 (padrão do SRT); 18 ≈ 67 px em 1080p.
STYLE="FontName=${FONT},FontSize=${SIZE},Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BackColour=&H99000000,BorderStyle=3,Outline=2,Shadow=0,MarginV=${MV},Alignment=2"
# escapa o caminho para o filtro subtitles
SRT_ESC=$(printf '%s' "$SRT" | sed "s/\\\\/\\\\\\\\/g; s/:/\\\\:/g; s/'/\\\\'/g")
ffmpeg -y -loglevel error -i "$IN" \
  -vf "subtitles='${SRT_ESC}':charenc=UTF-8:force_style='${STYLE}'" \
  -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart "$OUT"
echo "ok: $OUT"
