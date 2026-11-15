---
name: narracao-tts-ptbr
description: >-
  Gera narração pt-BR a partir de roteiro.json com edge-tts (padrão) ou Azure
  Speech (motor azure, licença comercial, recomendado para conteúdo monetizado),
  mesmas vozes Neural pt-BR, ritmo natural (rate e pausas entre frases,
  parágrafos e cenas configuráveis), termos em inglês com grafias de som inglês
  na mesma voz (padrão ingles_mesma_voz; mapa aportuguesado e emenda en-US
  opcionais), pausas para trechos de vídeo original, legenda SRT sincronizada e
  conferência objetiva da voz por transcrição reversa (faster-whisper, WER e
  termos-chave). Use quando precisar de locução sintética em português para
  vídeo, aula ou apresentação.
---
# narracao-tts-ptbr

Arquivos auxiliares relativos a esta pasta (instalada em `/home/box/agent-data/workflows/narracao-tts-ptbr/`).

Requisitos: `python3 -m venv venv && ./venv/bin/pip install edge-tts faster-whisper numpy`, ffmpeg/ffprobe.
Para o motor `azure` (recomendado em conteúdo monetizado): as variáveis `AZURE_SPEECH_KEY` e
`AZURE_SPEECH_REGION` no ambiente (nunca no repositório, em yaml, em logs ou em metadados) e, para
limites de palavra do serviço, `pip install azure-cognitiveservices-speech` (sem o SDK, o motor usa o REST).

1. Vozes: `scripts/list_voices.sh pt-BR` (existem Francisca, Antonio e ThalitaMultilingual). **Padrão (v1.3.0):
   `pt-BR-FranciscaNeural`, `--rate -5%`** — no trecho de teste com 30 termos em inglês, Francisca -5% teve WER 3,9% e
   30/32 termos; Antonio 6,8–7,8% e 27/32; Thalita 3,9–8,7% e 26–29/32 (ver `references/vozes-e-pronuncia.md`).
   O +8% antigo soava corrido.
2. Narrar: `./venv/bin/python scripts/tts_ptbr.py roteiro.json saida/ [--motor edge|azure] --voice pt-BR-FranciscaNeural --rate=-5%
   --pausa-frase-ms 400 --pausa-paragrafo-ms 700 --pausa-cena-ms 950 --pausa-trecho-ms 500 [--pronuncia extra.json] [--trechos duracoes.json]`
   → `narracao.wav`, `narracao.srt`, `timings.json` (cena: start/end, `frases` [[início, fim]], clip_start/clip_end, campo `motor`), `cena_XX.wav`.
   Use `--rate=-5%` (com `=`: valor negativo). Pausas: o edge-tts 7.x **escapa SSML** (um `<break>` é lido em voz alta),
   então cada frase é sintetizada à parte, a borda de silêncio do serviço é aparada e as frases são unidas com silêncio
   exato (o motor `azure` usa o mesmo esquema; o ritmo vai em `<prosody rate>` no SSML). SRT e timings saem nos tempos
   novos (o vídeo e a página consomem os mesmos campos). Parágrafo = quebra de linha
   na narração. Frase termina em `. ! ? …` seguido de espaço (".mdc", "console.log" não quebram).
3. Conferir sem ouvir: `./venv/bin/python scripts/check_voice.py roteiro.json saida/narracao.wav --timings saida/timings.json --terms "Termo A,Termo B" [--json relatorio.json]`
   (WER, trocas palavra a palavra, ritmo, termos reconhecidos). Meta: WER < 5%, todos os termos.
   Com `--timings` a transcrição é cena a cena, cada cena até 3 vezes valendo a melhor; trechos originais em silêncio;
   serve também para o MP4 final. Termos contam como palavra inteira; "IA" = "inteligência artificial"; algarismos e
   números por extenso contam como iguais (num2words pt_BR: "28 x 28" = "vinte e oito por vinte e oito", "1.000" = "mil",
   "10%" = "dez por cento"); `--de-json relatorio.json` recalcula o WER de um relatório salvo sem rodar o Whisper; compostos separados pelo Whisper ("type script") são juntados. Grafias brasileiras que
   o Whisper usa para o termo dito certo ("comit", "Zode", "Antropique", "globes", "gite", "prompte") valem como o termo
   (`references/equivalencias-whisper.json`; só grafias foneticamente iguais). Não rode vários check_voice em paralelo:
   cada um usa todos os núcleos e juntos ficam dezenas de vezes mais lentos.
4. Mapa padrão: `references/pronuncia-padrao.json` (v1.4.3, ~64 termos; "OpenAI" → "Ôupen ei ai", "JSON Schema" → "djêison squima", "retry" → "retrai", "Perplexity" → "perpléxiti", "vibe coding" → "vaibi côudin", "diff" → "díffi",
   "arrays" → "arrêis" testados em 2026-11-14, ver `references/vozes-e-pronuncia.md`; token, prompt, deploy, globs, framework,
   context window, rules, LLM, SDK, MCP, server, TypeScript, npm, build, test, commit, embedding, handler,
   install, frontmatter, description, Agent, git, Zod, Anthropic, Claude, host, chat, script, softmax, além de Gemini,
   Workbench etc.). Ordem: mapa padrão < `narracao.pronuncia` da config (`--pronuncia`) < `pronuncia` do roteiro
   (`"pronuncia_padrao": false` desliga o padrão). Troca numa passada só (o texto trocado não é trocado de novo); a
   legenda mostra a grafia original. Grafias escolhidas por transcrição reversa (2–3 frases reais × 3–5 grafias, 2
   rodadas); a nota do arquivo lista o que não tem conserto: prefira "regras", "o agente", "janela de contexto" a
   "rules", "Agent", "context window" (e sem grafia boa: "wrapper" → diga "camada sobre a API"; "Hugging Face" → só na
   tela). Termo novo: teste variantes em frases reais, confirme numa rodada com frases novas e só então grave no mapa.
5. Aulas técnicas: identificadores camelCase (registerTool, callTool) e "tool" soam mal — deixe-os na tela e narre a
   ideia ("ferramenta"); use "esquema" (não "schema"), "execute" (não "rode"), "atenção" (não "attention").
6. **Termos em inglês — padrão `ingles_mesma_voz` (v1.7.0, decisão do Carlos em 2026-11-14).** A frase sai inteira na
   `pt-BR-FranciscaNeural` a -5%; os termos em inglês usam `references/pronuncia-ingles-francisca.json` (por cima do mapa
   do item 4), grafias pensadas para soar perto do inglês ("tôuquen", "prômpt", "deplóy", "díf"). Sem emenda e sem
   outra voz: `termos_ingles.json` sai sem emendas e `timings.json` registra `termos_ingles_modo`. "context window" não
   tem grafia que o Whisper reconheça: diga "janela de contexto". `aportuguesar` (mapa do item 4) foi o padrão até a
   v1.6 e segue opcional. Outros opcionais (v1.5):
   `--termos-ingles-modo emendar_en --voz-en en-US-AvaNeural` (`scripts/termos_ingles.py`). **A emenda en-US foi
   testada (melhor nas métricas) e recusada pelo Carlos na escuta em 2026-11-14: não use sem pedido.** A frase sai inteira na Francisca com o termo na grafia original; o trecho do termo
   (limites de palavra do serviço, cortado nos silêncios entre palavras) é trocado pelo termo dito isolado pela voz
   en-US, com tom ajustado no próprio serviço (prosody pitch = F0 Francisca − F0 da voz en, até ±50 Hz), volume igualado
   (RMS das janelas com voz), ritmo ajustado (0,85–1,2×, rubberband) e crossfade de 12 ms; termos vizinhos ("MCP
   server") viram uma emenda só. Lista: `references/termos-ingles.json` (+ `--termos-ingles extra.json` com
   `termos`/`sem_ingles`). Outros modos opcionais: `multilingual` (frase na Thalita Multilingual), `original`.
   `ssml_lang` não existe de fato: o serviço do edge-tts recusa `<lang>`, `<voice>` aninhada e
   `<phoneme>` (NoAudioReceived), então cai para `emendar_en`. `saida/termos_ingles.json` registra cada emenda
   (duração, tom, salto de volume). Teste e números: `references/vozes-e-pronuncia.md` (v1.5). A conferência compara
   com o roteiro, que tem a grafia original: o termo dito em inglês e transcrito na grafia original conta como acerto.
7. Relate com honestidade: a checagem é automática (Whisper), ninguém ouviu. Amostras para escuta humana ajudam.
8. **Motor `azure` (v1.8.0) — recomendado para conteúdo monetizado** (YouTube e afins). O edge-tts não tem licença
   comercial; o Azure Speech, com as mesmas vozes Neural pt-BR (`pt-BR-FranciscaNeural` etc.), tem. O padrão desta
   versão o script/pipeline sem `motor` no yaml continua em `edge` (cursos já existentes não mudam).
   Cursos novos usam `motor: azure` no template.
   - Como escolher: `--motor azure` no `tts_ptbr.py`; na config da aula, `narracao.motor: azure`; ou a variável
     `TTS_MOTOR=azure` (vence o yaml). Ordem no script avulso: `--motor` > `TTS_MOTOR` > `edge`. No pipeline
     aula-ra: `TTS_MOTOR` > `narracao.motor` > `edge`. **Decisão (2026-11-15): Azure só em cursos novos.** O
     template de `curso-a-partir-de-ementa` já vem com `narracao.motor: azure`. Sem `motor` no yaml, o script e
     o pipeline assumem `edge` (aulas antigas não mudam de motor). `motor: edge` (ou ausente) não entra no hash
     de cache, para um pin explícito não re-narrar. Ao usar `azure`, o hash inclui o motor e a narração é refeita.
     Os cursos IA para Jornalismo e Eng. Software IA ficam fixados em `edge` e não devem ser re-narrados.
   - Variáveis (somente no ambiente, nunca no repo, em yaml, em logs ou em `timings.json`/`voz.json`):
     `AZURE_SPEECH_KEY` e `AZURE_SPEECH_REGION`. Se faltarem, o motor para com uma mensagem clara. Há um
     `.gitignore` para `.env`. `scripts/list_voices.sh --azure` lista as vozes da região (a chave não é impressa).
   - Instalação: `pip install azure-cognitiveservices-speech` (SDK; entrega WordBoundary, o mesmo tipo de
     timing do edge-tts). Sem o SDK, o motor usa o REST TTS
     ([documentação](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/rest-text-to-speech))
     e estima os tempos das palavras pela duração da frase. Rate: `<prosody rate="-5%">`
     ([SSML](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-synthesis-markup-voice)).
     Retry com backoff em HTTP 429 e 5xx (`Retry-After` quando houver). Cache opcional de frases
     (`--cache` ou `TTS_CACHE_DIR`), chave = hash(motor+voz+rate+texto).
   - Custo e limites (só fonte oficial): o Azure Speech cobra text-to-speech por caractere; as vozes Neural
     padrão incluem 0,5 milhão de caracteres grátis por mês. Valores pagos e cotas do recurso estão na
     [página oficial de preços](https://azure.microsoft.com/en-us/pricing/details/speech/) (consultada em
     2026-11-15). A skill não grava preço em outro lugar.
   - Diferença prática Azure vs edge: no SDK, o `audio_offset` do WordBoundary vem em ticks (100 ns) e a
     `duration` em `timedelta` — a skill converte para os mesmos `(início, fim, texto)` em segundos do edge.
     No REST, sem WordBoundary, a SRT reparte a duração da frase. A emenda `emendar_en` (recusada pelo Carlos)
     ainda sintetiza o termo en-US pelo edge-tts. `check_voice.py` lê `timings.json` e relata o `motor`
     (também em `voz.json`).

