# Changelog — narracao-tts-ptbr

## 1.8.0 — 2026-11-15

- Motor `azure` (Azure Speech, licença comercial), recomendado para conteúdo monetizado (YouTube e afins).
  Mesmas vozes Neural pt-BR, mesmo ritmo (`<prosody rate>`), mesmas pausas, mesmo modo `ingles_mesma_voz`,
  mesma SRT/timings e mesma conferência por Whisper. Saída nos mesmos arquivos do motor `edge`, para
  video-hyperframes, pagina-html-gsap e aula-ra não precisarem mudar o consumo.
- Seleção: `--motor azure|edge`, `narracao.motor` no yaml, ou variável `TTS_MOTOR`. Sem `motor` no yaml,
  o script e o pipeline assumem `edge` (caminho edge-tts idêntico ao da v1.7). **Azure só em cursos novos**
  (decisão de 2026-11-15): o template de curso-a-partir-de-ementa 1.5.0 já vem com `narracao.motor: azure`
  e falha com mensagem clara se faltarem `AZURE_SPEECH_KEY`/`AZURE_SPEECH_REGION`. Cursos já renderizados
  (IA para Jornalismo, Eng. Software IA) ficam com `motor: edge` explícito e não são re-narrados.
  `motor: edge` (ou ausente) não entra no hash de cache.
- Credenciais somente por `AZURE_SPEECH_KEY` e `AZURE_SPEECH_REGION` no ambiente. Nunca no repositório,
  em yaml, em logs ou em metadados; erro claro se faltarem. `timings.json` (e `voz.json`) passam a registrar
  o campo `motor`. `check_voice.py` relata o motor.
- SDK (`azure-cognitiveservices-speech`) quando instalado, com WordBoundary; senão, REST TTS e tempos
  estimados pela duração da frase. Retry com backoff em 429/5xx. Cache opcional de frases por hash
  (motor+voz+rate+texto). O pipeline aula-ra (1.4.1) encaminha `--motor` e só inclui o motor no hash de
  cache quando não é `edge`.

## 1.7.0 — 2026-11-14

- Padrão `termos_ingles = ingles_mesma_voz` (decisão do Carlos); mapa `diff = díf`; “context window” → “janela de contexto”.
