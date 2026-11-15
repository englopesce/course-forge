---
name: video-hyperframes
description: Renderiza um vídeo MP4 explicativo (1920×1080 e/ou vertical 1080×1920 com layout próprio) com HyperFrames a partir de roteiro.json + narração (timings), com cores/fontes da marca, trechos de vídeo original inseridos com o próprio áudio e legendas pt-BR gravadas com ffmpeg. Cenas com código ganham painel de código animado (linhas entram uma a uma; cada destaque escurece o resto e mostra sua nota). Use quando precisar transformar um roteiro narrado em vídeo curto animado sem Remotion.
---

# video-hyperframes

Arquivos auxiliares relativos a esta pasta (instalada em `/home/box/agent-data/workflows/video-hyperframes/`).
Leia `references/hyperframes-notas.md`.

1. Projeto: `npx -y hyperframes@0.9.43 init hf --example blank --resolution landscape --non-interactive --skip-skills`
   e copie `narracao.wav` → `hf/assets/`, `gsap.min.js` → `hf/`.
2. Composição: `python3 scripts/build_hyperframes.py roteiro.json timings.json hf/ [--tema tema.json] [--clips clips/clips.json] [--formato 16x9|9x16]
   [--codigo saida/codigo/snippets.json]` (timings/SRT da skill narracao-tts-ptbr; clips da skill
   trechos-youtube-credito; snippets da skill codigo-exemplo-aula). Cena com código: 16:9 texto à esquerda e painel
   à direita, 9:16 empilhado; a fonte se ajusta ao nº de linhas e à maior linha (14–30 px; ≤ 22 linhas e ≤ 72
   caracteres ficam legíveis); os destaques dividem o tempo da fala da cena. Fonte mono: JetBrains Mono
   (`fc-match "JetBrains Mono"`; instale se faltar), sem ligaduras.
3. Render + legenda: `scripts/render.sh hf/ narracao.srt saida/aula.mp4 Inter 18`
   (ou `npx hyperframes render` e `scripts/burn_subs.sh entrada.mp4 legendas.srt saida.mp4`).
   Vertical 9:16: projeto separado (`init hf-9x16 --resolution portrait`), `--formato 9x16` (template
   `templates/hyperframes_index_9x16.html`, usa `clips/<id>_9x16.mp4` da skill trechos-youtube-credito),
   `scripts/rewrap_srt.py narracao.srt aula-9x16.srt --max 26` e `SUB_MARGINV=48 scripts/render.sh hf-9x16/ aula-9x16.srt aula-9x16.mp4 Inter 9`.
4. Conferir: `ffprobe` (duração, streams), quadros PNG em momentos de texto, legenda e trecho.
