# aula-ra — pipeline de mini-aulas (pt-BR)

Transforma vídeos do YouTube (e documentação oficial) em **uma página HTML animada** e **um MP4 curto
narrado**, para o público da config — de diretores não técnicos a programadores (aulas com código real,
exercícios e repositório testado). Um comando, uma configuração. Curso inteiro a partir de uma ementa:
skill irmã `curso-a-partir-de-ementa` (gera um aula.yaml por aula e chama este pipeline).

```bash
python scripts/pipeline.py aula.yaml                    # tudo, pulando o que não mudou
python scripts/pipeline.py aula.yaml --list             # etapas e última execução
python scripts/pipeline.py aula.yaml --stage narracao   # só uma etapa
python scripts/pipeline.py aula.yaml --from trechos --to video
python scripts/pipeline.py aula.yaml --force --stage video
```

## Etapas

| Etapa | Skill (pasta irmã) | Entrada | Saída |
|---|---|---|---|
| `legendas` | youtube-legendas | `videos[].url` | `<trabalho>/legendas/<id>/{transcript.txt,segments.json,fonte.json}` |
| `roteiro` | roteiro-didatico-ptbr | transcrições + `aula`, `roteiro`, `trechos` | `<saida>/roteiro.json` (**agente**) |
| `codigo` | codigo-exemplo-aula | `exemplo` (repositório + comandos) + `cenas[].codigo` + `exercicios` | `<saida>/codigo/{snippets.json,checagem.json,log_*.txt}`, `<saida>/exemplo/`, `<saida>/exercicios.md` (pulada sem `exemplo`/código/exercícios) |
| `narracao` | narracao-tts-ptbr | roteiro + `narracao` + durações dos trechos | `<trabalho>/narracao/{narracao.wav,narracao.srt,timings.json,voz.json}` |
| `trechos` | trechos-youtube-credito | `trechos` + roteiro (legendas pt-BR) | `<saida>/clips/{<id>.mp4,<id>.vtt,clips.json}` |
| `html` | pagina-html-gsap | roteiro + clips + snippets + `marca` | `<saida>/aula.html` |
| `video` | video-hyperframes | roteiro + narração + clips + snippets + `marca` + `video` (+ `video_9x16`) | por formato: `aula.mp4`/`aula.srt` (16x9), `aula-9x16.mp4`/`aula-9x16.srt` (9x16) |
| `verificacao` | (aula-ra) | MP4(s) + HTML + `codigo/checagem.json` | `<saida>/frames/*.png`, `<saida>/verificacao.json` (falha se o código da aula não rodou) |

## Aulas técnicas (código na tela)
Com `exemplo: {dir, checagem: [{nome, cmd, timeout?}]}` no yaml, a etapa `codigo` roda o repositório numa cópia
limpa e extrai o código citado em `cenas[].codigo` (a tela mostra exatamente o que foi testado). No HTML a cena
vira texto + painel de código com números de linha e botões de destaque; no vídeo (16:9 lado a lado, 9:16
empilhado) as linhas entram uma a uma e cada destaque escurece o resto e mostra sua nota. Exercícios
(`exercicios` no roteiro) viram `exercicios.md` e a seção "Exercícios práticos" do HTML; os que têm
`checagem` são provados por um comando do repositório (ex.: `npm run test:solucao`).
Público/nível/tom: `aula.publico`, `aula.nivel`, `aula.tom`, `aula.linguagem`, `aula.contexto`;
estrutura e fechamento: `roteiro.estrutura`, `roteiro.fechamento`; docs oficiais: `roteiro.documentacao`.

## Formatos (16:9 e 9:16)
`formatos: [16x9, 9x16]` no `aula.yaml` (padrão: só `16x9`, compatível com as aulas antigas).
- **16x9** → `aula.mp4` 1920×1080 (como antes).
- **9x16** → `aula-9x16.mp4` 1080×1920, com **layout vertical próprio** para as cenas animadas
  (`video-hyperframes/templates/hyperframes_index_9x16.html`: ícone, título e itens empilhados; faixa de baixo para legendas)
  e trechos em **FIT**: o quadro 16:9 inteiro, sem corte, centralizado; fundo = o próprio trecho desfocado e
  escurecido (`trechos_opcoes.fundo_9x16: blur`) ou uma cor (`"#0b1d3a"`); crédito (canal, título, link com tempo)
  na área livre de cima; legendas requebradas (`rewrap_srt.py`) logo abaixo do quadro.
  Reenquadramento: `trechos-youtube-credito/scripts/reframe_9x16.py` (também usável sozinho).
- Opções do vertical: `video_9x16: {legenda_tamanho: 9, legenda_margem: 48, legenda_max_chars: 26}`.
- Cache por formato (`.cache/video.json`, `.cache/video-9x16.json`), projeto HyperFrames por formato (`hf/`, `hf-9x16/`).
  Ex.: `--stage video` refaz só o formato cujas entradas mudaram.
- A verificação confere dimensões, áudio e duração de cada formato e salva quadros de cena animada e de
  trecho de cada um (`frames/video_*.png`, `frames/video9x16_*.png`).

## Cache / idempotência
Cada etapa calcula um hash de: seções da config que usa + arquivos de entrada + pastas `scripts/` e
`templates/` da própria skill. Guardado em `<trabalho>/.cache/<etapa>.json`. Se o hash é igual e as
saídas existem, a etapa é pulada; `--force` refaz. Downloads também são cacheados
(`<trabalho>/legendas`, `<trabalho>/cache_trechos`), para não repetir chamadas ao YouTube.
Observação: a etapa `narracao` gera e confere a voz juntas; o edge-tts não gera bytes idênticos a cada
chamada, então refazer a narração faz o vídeo ser renderizado de novo.

## Etapa do agente (roteiro)
Sem `roteiro.json`, o pipeline cria `<saida>/PEDIDO_ROTEIRO.md` (prompt preenchido com tema, público,
caminhos das transcrições e as falas originais de cada trecho), mostra o esquema e para com código 10.
O agente escreve `roteiro.json`, valida com
`python ../roteiro-didatico-ptbr/scripts/validate_roteiro.py roteiro.json --config aula.yaml` e retoma com
`--from roteiro`. Se a config mudar depois, o pipeline avisa e atualiza o pedido.

## Requisitos
- Python 3.11+ com venv: `pip install edge-tts faster-whisper pyyaml`
- `yt-dlp` (PATH ou `~/.local/bin`), `ffmpeg`/`ffprobe` (com drawtext), `fc-match`
- Node ≥ 22 + `npx` (HyperFrames 0.9.43 via npx; `puppeteer-core` é instalado em `<trabalho>/node`)
- Google Chrome (`/usr/bin/google-chrome`) para a verificação do HTML
- Internet: YouTube (legendas/trechos), Microsoft edge-tts, jsDelivr (GSAP, uma vez)

## Exemplo
`templates/aula.yaml` — piloto "Agentes de IA no Gemini Enterprise" (vídeo oficial Google Workspace,
3 trechos). Resultado em `/workspace/aula-ra/piloto-v2/`.
Curso para programadores (85 aulas geradas de uma ementa; 3 produzidas, uma com MCP server em TypeScript):
`/workspace/aula-ra/curso-eng-software-ia/` (`curso.yaml`, `aulas/*.yaml`, `exemplos/`).
Sessão 2 (Deep Research e Gemini Notebook, vários vídeos, 16:9 + 9:16): `/workspace/aula-ra/aula-sessao-2-deep-research-notebook.yaml`
→ `/workspace/aula-ra/sessao-2/`.

## Pronúncia
O mapa `pronuncia` fica no `roteiro.json` (só a voz usa a grafia fonética; a legenda mantém a original).
Sugestões testadas com pt-BR-FranciscaNeural estão em `narracao-tts-ptbr/references/pronuncia-padrao.json`.

## Instalação como skills
Copie cada pasta para `/home/box/agent-data/workflows/<slug>/` (aula-ra, youtube-legendas,
roteiro-didatico-ptbr, narracao-tts-ptbr, trechos-youtube-credito, pagina-html-gsap, video-hyperframes,
codigo-exemplo-aula, curso-a-partir-de-ementa).
Todos os caminhos internos são relativos à pasta da skill.
