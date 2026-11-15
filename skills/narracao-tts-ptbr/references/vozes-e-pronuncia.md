# Vozes pt-BR, ritmo e pronúncia (edge-tts 7.3.1, faster-whisper small, nov/2026)

## v1.3.0 — feedback do Carlos (sotaque inglês nos termos; frases emendadas)
Trecho de teste com 30 termos em inglês (4 cenas, 103 palavras; `trecho_termos.json` em
`curso-eng-software-ia/_comparacao-vozes/`), uma rodada por combinação, pausas 400/700/950 ms.

Mapa de pronúncia v1.2 (antes):
| Voz | +8% | +0% | -5% |
|---|---|---|---|
| Francisca | 7,8% · 26/32 | 4,9% · 27/32 | 7,8% · 25/32 |
| Antonio | 12,6% · 23/32 | 14,6% · 22/32 | 14,6% · 22/32 |
| ThalitaMultilingual | 5,8% · 27/32 | 5,8% · 27/32 | 6,8% · 27/32 |

Mapa v1.3.0 (depois):
| Voz | +0% | -5% |
|---|---|---|
| **Francisca** | 3,9% · 29/32 | **3,9% · 30/32** (135 palavras/min) |
| Antonio | 7,8% · 27/32 | 6,8% · 27/32 |
| ThalitaMultilingual | 3,9% · 29/32 | 8,7% · 26/32 |

Escolha: **Francisca -5%** (melhor em termos, empate em WER, mais lenta como pedido). Thalita é "Multilingual":
tende a ler o termo em inglês com sotaque inglês — o oposto do pedido — e caiu muito a -5%. Antonio é o pior.

## Pausas
SSML `<break>` não funciona (o edge-tts escapa e lê "break time..."). Pausa natural do serviço entre frases ≈ 0,24 s.
Agora: frase a frase + silêncio exato (400 ms frase, 700 ms parágrafo, 950 ms cena, 500 ms antes/depois de trecho).

## Pronúncia (Francisca -5%, frases reais, acertos do termo na transcrição)
Rodada 1 (2 frases) e 2 (3 frases); entre parênteses o total. Escolhida em negrito.
- token: **tôu-ken** (2/5; as outras 0/5, viram "toque em") · tokens: **tôkens** (2/2)
- prompt: **prômpt** (1/3, = original; "prómpti" 0/2) · deploy: **diplói** (5/5)
- globs: **glóbis** (2/5; Whisper escreve "globes") · framework: **freimuórqui** (2/2)
- context window: **cóntéksti uíndou** (2/5) · rules: **rúlis** (1/3; "rúls"/"rúlz" viram "ruas")
- LLM: **éle éle ême** (2/2) · SDK: **ésse dê cá** (2/2) · MCP: **ême cê pê** (1/2, = original)
- server: **sérver** (2/2) · TypeScript: **táipi-scrípti** (2/2) · Cursor: sem grafia (original 2/2 e 3/3 na aula; "Kérsor" 2/2 em frases soltas, mas na aula m01-a08 o Whisper escreveu "kersor" 3/3 — retirado)
- npm: **ene pê ême** (2/2) · build: **bíld** (2/2) · test: **tést** (2/5; Whisper escreve "teste")
- commit: **comíti** (Whisper escreve "comit" 5/5 → equivalência) · embedding: **embédingui** (3/3; original 1/5)
- handler: **rândler** (3/3; "rêndler" vira "render") · install: **instól** (2/2) · frontmatter: **front-máter** (2/2)
- description: **discrípchon** (2/2) · Agent: **Êidjent** (2/5) · client: **cláient** (3/5)
- git: **guíti** (3/5) · Zod: **Zód** (Whisper "Zode") · Anthropic: **Antrópic** (Whisper "Antropiq")
- Claude: **Clôd** · host: **rôust** (3/3) · chat: **tchét** (2/2) · script: **scrípti** (2/2) · softmax: **sóft-méx** (2/2)
- query: sem grafia (as grafias pioram).

## Armadilhas
- "IA" é lido como "inteligência artificial" (a legenda continua "IA").
- "agente é ..." pode ser ouvido "a gente é ..."; reescreva.
- Serviço online da Microsoft (sem chave): precisa de internet; às vezes responde sem áudio (o script repete).
- A conferência é automática: **ninguém ouviu**. Recomende escuta humana (amostras em `_comparacao-vozes/`).

## Histórico (piloto, +8%)
Francisca 4,7% (3,0% com mapa), Thalita 7,8%, Antonio 9,1% numa narração de 232 palavras sem termos de programação.

## v1.4.2 (2026-11-14) — vibe coding, diff, arrays
Francisca -5%, faster-whisper small, 3 frases × 2 repetições por grafia (script: work/pron/teste6.py).

| termo | grafias testadas (acertos) | escolhida |
|---|---|---|
| vibe coding | sem grafia 0/6 ("VibeCode"); váibe côding 0/6; váib côdin 1/6; vaibi côudin 4/6 e 5/6; vaibi côdin 2/6; váibi cóudin 1/6; váibi côding 0/6; vaibi côuding 4/6 | **vaibi côudin** |
| diff | sem grafia 2/6 e 1/6 ("gif", "Difantes"); díf 2/6; dife 4/6 e 5/6; difi 2/6; díff 2/6; díffi 6/6 | **díffi** |
| arrays | sem grafia 0/6 ("a raiz"); arrêis, arreis, a-rêis 0/6 (sempre "a reis"/"arrei"); erêis 0/6 ("heres") | **arrêis** + equivalência no check_voice |

Conferência: algarismos e números por extenso agora contam como iguais (num2words pt_BR): "28 x 28" = "vinte e oito por vinte e oito",
"784" = "setecentos e oitenta e quatro", "1.000" = "mil", "10%" = "dez por cento". `--de-json relatorio.json` recalcula o WER sem rodar o Whisper.

## v1.4.3 (2026-11-14) — wrapper, Y Combinator, Perplexity, Hugging Face, retry, OpenAI, Gemini, JSON Schema
Francisca -5%, faster-whisper small, 3 frases × 2 repetições por grafia; 3 rodadas, a 3ª com frases novas para confirmar
(script: work/pron/teste7.py, com nova tentativa quando o edge-tts dá timeout). Só entrou no mapa o que melhorou também na 3ª rodada.

| termo | rodadas 1–2 (acertos) | confirmação (3ª rodada) | decisão |
|---|---|---|---|
| OpenAI | sem grafia 1/6; Ôupen ei ai 6/6; Ôupen êi ai 6/6; Open êi ái 0/6 | sem grafia 0/6 ("OPA"); Ôupen ei ai 5/6 | **Ôupen ei ai** |
| Perplexity | sem grafia 0/6; perpléxiti 4/6; perplékssiti 4/6; perpléksiti 1/6 | sem grafia 0/6; perpléxiti 2/6 | **perpléxiti** |
| JSON Schema | sem grafia 0/6; djêison squima, jêison isquíma, jêisson esquema 0/6 ("Jason schema") | com a equivalência jason→json: sem grafia 0/6 ("João Sema"); djêison squima 6/6 | **djêison squima** + equivalência |
| retry | sem grafia e 5 grafias 0/6 (o Whisper escreve "retrai"/"ritrai") | com a equivalência retrai→retry: sem grafia 0/6 ("rétrico"); retrai 6/6 | **retrai** + equivalência |
| Gemini | sem grafia 0/6; Dgémini 4/6; Djémini 4/6; Jêmini 0/6 | sem grafia 0/6 ("Xemini"); Dgémini 4/6 | mantém **Dgémini** (+ equivalência gêmini) |
| wrapper | sem grafia 0/6; uréper 4/6; répper, rápper, rrépper 0/6 | empate: sem grafia 2/6; uréper 2/6 | não entrou: prefira "camada sobre a API" |
| Y Combinator | sem grafia 2/6; uai combinêitor 4/6; uai cômbinêitor 4/6; uái cômbineitor 0/6 | sem grafia 6/6; uai combinêitor 4/6 | não entrou (sem grafia é melhor) |
| Hugging Face | 7 grafias (râguin feice, háguin feis, rágguin fêis, Háguin Feis, rráguin fêice, Hugging Feice, sem grafia): todas 0/6 | todas 0/6 | não entrou: cite na tela/legenda |

Equivalências novas no check_voice (grafias foneticamente iguais): gêmini/gémini → gemini, jason → json, retrai/ritrai → retry.

## v1.5.0 (2026-11-14): termos em inglês com pronúncia inglesa (pedido do Carlos)
Comparação completa, com tabela, áudios e amostra:
`/workspace/aula-ra/curso-eng-software-ia/_comparacao-ingles/LEIAME.md`.

Resumo:
- SSML `<lang>`, `<voice>` aninhada e `<phoneme>` são recusados pelo serviço (NoAudioReceived).
- Thalita Multilingual na frase inteira: português limpo (WER pt 5,9%), mas os termos com sotaque (10/20).
- Emenda com termo en-US: 16–18/20 termos.
  - O salto de volume e de tom fica no nível da variação natural (1,7 dB e 2,8 st).
  - Custo: o WER pt sobe para cerca de 11% (o Whisper ouve sílabas a mais nas junções).
- Melhor nas métricas: `emendar_en` com `en-US-AvaNeural`. **O Carlos ouviu a amostra e recusou (2026-11-14):
  o padrão é `aportuguesar`** (o mapa aprovado); os outros modos ficam como opção.


## v1.6.0 (2026-11-14) — modo opcional `ingles_mesma_voz`

Padrão do pipeline **permanece `aportuguesar`** (mapa aprovado pelo Carlos). O modo novo é opcional:
`narracao.termos_ingles.modo: ingles_mesma_voz`. A frase sai **inteira** na `pt-BR-FranciscaNeural` a −5%,
sem emenda e sem voz en-US ou Multilingual. Mapa: `references/pronuncia-ingles-francisca.json`.

Teste no mesmo trecho de 4 parágrafos / 20 ocorrências (`_comparacao-ingles/`), 3 a 5 grafias por termo,
frase real inteira, Whisper small (`language=pt` e `language=None`) e, quando deu, idioma no recorte do termo.
Hífen evitado quando gerava micro-pausa; no mapa `aportuguesar` o hífen de "tôu-ken" e "táipi-scrípti" foi
conferido e **não** alterado: os vales de ~80 ms aparecem também sem o hífen (sílaba da voz), e os silêncios
≥ 150 ms dentro de frase são de pontuação do texto (`git:`, `padrão:`, `;`, vírgulas).

Amostras para o Carlos ouvir (conferência só automática; ninguém ouviu):
`curso-eng-software-ia/_comparacao-ingles/amostra-francisca-aportuguesar.mp3` (43,0 s) e
`amostra-francisca-ingles-mesma-voz.mp3` (42,5 s). Relatório: `relatorio-francisca.json`.

Na amostra final (Whisper small, pt, frase a frase, melhor tentativa):

| modo | WER | WER pt | termos grafia inglesa | com equivalências |
|---|---|---|---|---|
| aportuguesar (padrão) | 9,3% | 3,5% | 11/20 | 13/20 |
| ingles_mesma_voz | 11,2% | 3,5% | 11/20 | 13/20 |

O modo novo acertou **token** (2/2, "token a token"), que o aportuguesar perdeu ("toquem"). Perdeu **diff**
(Whisper escreveu "GIF") e **context window** ("contextuíndo"). O português em volta ficou igual (WER pt 3,5%).

Grafias escolhidas (reconhecimento na frase de teste, grafia inglesa original): token `tôuquen` (pt sim / auto não, recorte en "token and token");
prompt `prômpt` (pt+auto, recorte en "prompt"); deploy `deplóy`; framework `frêimwôrk`; commit `comítt`;
TypeScript `táipiskript`; MCP `MCP` (a própria sigla); rules `rúuless` (só no auto); Agent `Êijent`;
diff `díffe`; OpenAI `Ôupen ei ai`; Claude `Clôd`. Sem reconhecimento estável da grafia original:
context window `kóntekst uíndow`; vibe coding `váib códing` (sai "VibeCode"); arrays `arráys` (sai "reis");
Hugging Face `Râguin Fêice` (auto chegou em "Hangin Face"); Anthropic fica na grafia original (auto: "Anthropique").

## v1.7.0 (2026-11-14): padrão `ingles_mesma_voz`
Decisão do Carlos: o padrão passa a ser `termos_ingles.modo: ingles_mesma_voz`, só com a pt-BR-FranciscaNeural a -5%.
Pausas sem mudança. Correções no mapa `pronuncia-ingles-francisca.json` (frases reais, Whisper small pt, 2 rodadas;
números na `_nota` do arquivo): `diff` = "díf" (antes "díffe", que saía "drift"/"GIF"). Para "context window", nenhuma
grafia testada passou: diga "janela de contexto" no roteiro. Checagem automática, ninguém ouviu.
