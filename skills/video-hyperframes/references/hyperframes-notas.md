# Notas HyperFrames (v0.9.43, testado em nov/2026)

- Licença Apache-2.0; requer Node ≥ 22, FFmpeg, Chrome (`npx hyperframes doctor`).
- Projeto: `npx -y hyperframes@0.9.43 init <pasta> --example blank --resolution landscape --non-interactive --skip-skills`.
- Regras: todo elemento com tempo tem `data-start` + `data-duration` e `class="clip"`; uma timeline GSAP
  pausada registrada em `window.__timelines["main"]`; nada de `Date.now()`/`Math.random()`/rede.
- Áudio: `<audio src="assets/narracao.wav">`; trecho com som: `<video data-has-audio="true">` (sem `muted`).
- `npx hyperframes check` (lint + runtime + layout + contraste) e `snapshot --at 5,30` antes de renderizar.
- Avisos esperados com este template: `nested_structure_needs_subcomposition`, `timeline_track_too_dense`
  (organização do Studio) e `line_unread` no crédito final.
- Render local ~45 s para 90 s de vídeo 1080p30 (8 núcleos, sem GPU).
- Legendas são gravadas depois com ffmpeg (`burn_subs.sh`); o template deixa ~260 px livres embaixo.
- Não usar Remotion (licença paga para empresas do porte da Rede Amazônica).
- No 9:16, `#credit`, `.trecho-tag` e `#avisos` têm placa `rgba(0,0,0,.85)` e z-index acima do `.trecho-video` (tela cheia). Sem isso, o crédito da fonte fica atrás do clipe e a tag teal some no fundo claro do FIT.
- A barra de avisos fixa nunca fica escondida: `#avisos` e `#credit` vão numa faixa `#topo` (flex, z-index 10, acima do clipe). A altura é medida em `layoutTopo()` (e de novo quando as fontes carregam) e posiciona tag e, no 16:9, o cartão do clipe. Offsets fixos (1.2.3) não bastavam quando o aviso jurídico passava de 3 linhas: o check falhava com `content_overlap` / `text_occluded` e o fim do aviso sumia sob a placa do crédito.
