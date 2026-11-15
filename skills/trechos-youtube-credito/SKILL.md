---
name: trechos-youtube-credito
description: >-
  Recorta trechos curtos (4–8 s) de vídeos do YouTube baixando só as seções
  necessárias, grava crédito na imagem (canal, título, link com tempo),
  normaliza o áudio, gera metadados e legendas pt-BR dos trechos e, se pedido, a
  versão vertical 9:16 em FIT (quadro inteiro, fundo desfocado, crédito na área
  livre). Use quando uma aula, página ou vídeo interno precisar mostrar exemplos
  do vídeo original com crédito, sem baixar o vídeo inteiro.
---
# trechos-youtube-credito

Arquivos auxiliares relativos a esta pasta (instalada em `/home/box/agent-data/workflows/trechos-youtube-credito/`).
Leia antes `references/politica-trechos.md`.

1. Escolha os momentos pela transcrição com tempo (`segments.json` da skill youtube-legendas):
   procure falas que descrevem a demonstração ("type", "agent gallery", "table"...), baixe uma vez e
   confira um mosaico de quadros (`ffmpeg -i x.mp4 -vf "fps=1,scale=320:-1,tile=4x4" -frames:v 1 mosaico.png`).
2. `trechos.json`: `[{"id":"exemplo","video":"<ID>","inicio":"05:15.5","fim":"05:24","mostra":"..."}]`.
3. `python3 scripts/cut_clips.py --trechos trechos.json --fontes <pasta_legendas> --cache <cache> --out clips/ [--roteiro roteiro.json]`
   → `clips/<id>.mp4` (1280×720, H.264/AAC, crédito gravado), `clips/<id>.vtt` (pt-BR), `clips/clips.json`.
   Com `--formatos 16x9,9x16` também `clips/<id>_9x16.mp4` (1080×1920, FIT: quadro 16:9 inteiro sem corte, fundo =
   o próprio trecho desfocado e escurecido ou `--fundo-9x16 "#0b1d3a"`, crédito acima do quadro, área de baixo livre
   para legendas). Reenquadrar um MP4 qualquer: `scripts/reframe_9x16.py entrada.mp4 saida.mp4 --canal ... --titulo ... --link ...`.
4. 429/robô: espera automática 120/300/600 s; sem cookies. O cache evita baixar de novo.
   "n challenge solving failed" / 403 / formato indisponível: `scripts/ytdlp_retry.py` repete uma vez com
   `--remote-components ejs:github` (script oficial do yt-dlp para o desafio do YouTube; não usa conta nem cookies).
   `YT_EJS_REMOTO=0` desliga.
   Travamento no download da seção (0% CPU e arquivos parados, inclusive sem `.part`): o mesmo `ytdlp_retry.py`
   encerra só aquele yt-dlp/ffmpeg (não o pipeline) depois de `YT_HANG_SECS` sem progresso (padrão 90 s; `0` desliga)
   e tenta de novo com espera progressiva (`YT_HANG_BACKOFF`, padrão 15,30,60) até `YT_HANG_TENTATIVAS` (padrão 4),
   passando a usar `ejs:github`. Continua baixando só a seção (`--download-sections`), sem cookies.
Requisitos: yt-dlp, ffmpeg (com drawtext/libfreetype), fontconfig (`fc-match`).
