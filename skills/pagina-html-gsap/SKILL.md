---
name: pagina-html-gsap
description: Gera uma página HTML única, offline, com animação passo a passo em GSAP (5–8 passos, botões Anterior/Próximo, teclado, crédito), cores e fontes da marca, e opcionalmente trechos de vídeo local com legenda pt-BR e link ao original; confere no Chrome headless (erros de JS, vídeos carregando, PNGs). Também mostra código: cena com painel de código realçado (números de linha, destaques clicáveis com nota, entrada linha a linha) e seção de exercícios práticos com o comando que os confere. Use para explicar conceitos (a público não técnico ou a programadores) em formato de página, a partir de um roteiro.json.
---

# pagina-html-gsap

Arquivos auxiliares relativos a esta pasta (instalada em `/home/box/agent-data/workflows/pagina-html-gsap/`).

1. GSAP local (uma vez): `curl -sSLo gsap.min.js https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js` (licença standard gratuita).
2. Gerar: `python3 scripts/build_html.py roteiro.json saida/aula.html --gsap gsap.min.js [--tema tema.json] [--clips saida/clips/clips.json --clips-dir clips/]`
   - Formato do roteiro: skill roteiro-didatico-ptbr. `layout: "fluxo"` = cartões com setas.
   - Trechos: MP4 ficam em `saida/clips/` (pasta irmã, caminho relativo) — não são embutidos; a legenda VTT é embutida.
   - Código: `--codigo saida/codigo/snippets.json` (skill codigo-exemplo-aula; lê também `checagem.json` ao lado).
     Cena com `codigo` vira texto à esquerda + painel à direita; `exercicios` do roteiro viram a seção
     "🛠️ Exercícios práticos" (com "✔ verificado na geração da aula" quando a checagem passou). Trecho e código na
     mesma cena: mostra o trecho. Fonte mono JetBrains Mono (sem ligaduras), com fallback para DejaVu Sans Mono.
3. Conferir: `npm i puppeteer-core` numa pasta de trabalho e `CHROME=/usr/bin/google-chrome node scripts/check_html.mjs saida/aula.html saida/frames 1,3,5`
   (abre **sem internet**, falha com erro de JS ou vídeo que não carrega, salva `html_passo_N.png`).
   Rode o `.mjs` a partir de uma pasta com `node_modules/puppeteer-core` (copie o script para lá ou use `NODE_PATH`).
