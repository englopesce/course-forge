---
name: aula-ra
description: Orquestra a produção de uma mini-aula em pt-BR sobre qualquer tema, para o público da config (de diretores não técnicos a programadores), a partir de vídeos do YouTube e documentação oficial — plano opcional (plano-de-estudo), legendas, roteiro didático, código de exemplo testado com exercícios (aulas técnicas), narração TTS, trechos com crédito, página HTML animada (GSAP) e vídeo MP4 16:9/9:16 (HyperFrames) — com um pipeline único (`scripts/pipeline.py aula.yaml`), cache e etapas re-executáveis. Use quando pedirem uma aula, explicação animada, vídeo curto explicativo ou página passo a passo baseada em vídeo(s) do YouTube; para um curso inteiro a partir de ementa, use curso-a-partir-de-ementa (que chama este pipeline).
---

# aula-ra (orquestradora)

Arquivos auxiliares relativos a esta pasta. Instalação esperada: cada skill em
`/home/box/agent-data/workflows/<slug>/` (irmãs desta). O pipeline acha as outras pela pasta-mãe
(ou `$AULA_SKILLS_DIR` / `skills_dir` no YAML). Detalhes e comandos: `README.md`.

## Etapas e skills (nesta ordem)
0. *(opcional)* **plano-de-estudo** — trilha curta: planejar as sessões e os vídeos verificados (entrega uma Page).
   Curso inteiro a partir de uma ementa: **curso-a-partir-de-ementa** (gera um `aula.yaml` por aula).
1. **youtube-legendas** — vídeo oficial + transcrição (`legendas`).
2. **roteiro-didatico-ptbr** — *o agente escreve* `roteiro.json` (`roteiro`).
3. **codigo-exemplo-aula** — só em aulas técnicas (`exemplo` no yaml): roda o repositório de exemplo numa cópia
   limpa, extrai o código das cenas e gera `exercicios.md` (`codigo`; pulada nas outras aulas).
4. **narracao-tts-ptbr** — voz pt-BR + SRT + conferência por transcrição reversa (`narracao`).
5. **trechos-youtube-credito** — trechos curtos com crédito (`trechos`, opcional).
6. **pagina-html-gsap** — `aula.html` offline, com painel de código e exercícios quando houver (`html`).
7. **video-hyperframes** — `aula.mp4` (16:9) e, se pedido, `aula-9x16.mp4` (9:16), com legendas gravadas e
   painel de código animado (`video`).
8. verificação (desta skill): ffprobe e quadros PNG de cada formato, voz no MP4, Chrome headless e resultado da
   checagem do código (`verificacao`).

## Como rodar
1. Copie `templates/aula.yaml`, ajuste tema, público (`aula.publico`, `nivel`, `tom`, `linguagem`), vídeos,
   trechos, voz, marca, `saida` e `formatos` (`[16x9]` padrão; `[16x9, 9x16]` gera também o vertical).
   Aula técnica: `exemplo: {dir, checagem}` e `roteiro.documentacao` (docs oficiais) — ver codigo-exemplo-aula.
2. `python scripts/pipeline.py aula.yaml` (Python do venv com edge-tts, faster-whisper, PyYAML).
3. Na 1ª vez ele **para na etapa roteiro** (código 10) e mostra o pedido
   (`<saida>/PEDIDO_ROTEIRO.md`, feito de `roteiro-didatico-ptbr/templates/prompt_roteiro.md`, já com os trechos
   relevantes das transcrições) e onde escrever `roteiro.json`. Escreva **lendo só o pedido** (a transcrição inteira
   só se faltar algo), e retome com `--from roteiro`.
4. Refazer partes: `--stage narracao`, `--from trechos --to video`, `--force`. Estado: `--list`.

## Regras fixas
- Sem Remotion. Fatos só da transcrição ou documentação oficial; analogias e recomendações marcadas.
- Código na tela só do repositório testado (a etapa `codigo` e a verificação falham se não rodar).
- Crédito (título, canal, URL) nos dois formatos; trechos só para uso interno (`references/politica-credito-youtube.md`).
- YouTube 429/robô: espera e repete; **nunca** cookies de conta.
- Relatar a voz com honestidade: checagem automática (WER, termos), ninguém ouviu.
- Pronúncia: **padrão `narracao.termos_ingles.modo: ingles_mesma_voz`** (v1.7, decisão do Carlos em 2026-11-14): só a
  `pt-BR-FranciscaNeural` a -5%, frase inteira, termos em inglês com grafias de som inglês
  (`narracao-tts-ptbr/references/pronuncia-ingles-francisca.json` por cima de `pronuncia-padrao.json`). Nenhuma voz en-US
  nem Multilingual. `aportuguesar` (padrão até a v1.6), `emendar_en`, `multilingual` e `original` ficam como opção; a emenda en-US foi testada e recusada pelo Carlos na escuta (2026-11-14). Ordem: mapa padrão < mapa `ingles_mesma_voz` (no modo padrão) < `narracao.pronuncia` < `pronuncia` do roteiro (este vence).

## Economia de tokens de LLM (v1.4.0)
- **Registro:** toda etapa de LLM passa por `scripts/uso_tokens.py` e vai para `<saida>/uso-tokens.json` (etapa, modelo,
  tokens de entrada e saída, `cache`, `evitados`, `estimado`, quando). Hoje o roteiro (e a estrutura do curso) é escrito
  pelo agente, sem API: o uso é **estimado** com tiktoken o200k_base sobre o que o agente lê (pedido + esquema; sem
  seleção, também as transcrições inteiras) e escreve (`roteiro.json`). Etapa que chamar API: use `uso_tokens.chamar()`
  (OpenAI-compatível; `LLM_API_BASE`, `LLM_API_KEY`, `LLM_MODEL` no ambiente) — registra o `usage` real.
- **Só o relevante:** o pedido de roteiro traz só janelas das transcrições (BM25 sobre janelas de ~45 s com tempos,
  consulta = tema, objetivo, tópicos, termos, trechos e `_busca_videos`, expandida pt→en; janelas em volta de cada
  trecho entram sempre). Limite e modo no yaml: `roteiro.selecao: {modo: bm25|completo, max_tokens: 2500, janela_s: 45,
  contexto_trecho_s: 30, palavras_chave: [...]}`. A transcrição inteira fica citada como reserva.
- **Cache de vídeos do curso:** `cache_videos: <dir>` (o curso põe `<curso>/_cache/videos`): cada vídeo é baixado uma
  vez em `<dir>/<id>/<versão youtube-legendas>-<hash dos idiomas>/` e copiado para as aulas que o usam; um `resumo.md`
  nessa pasta (se alguém escrever) entra no pedido de toda aula que usar o vídeo.
- **Roteiro só quando a entrada muda:** hash de trechos selecionados + config relevante (`aula`, `roteiro`, `trechos`,
  `exemplo`, `videos`) + prompt/esquema + versão da skill (`.cache/roteiro.json`). Igual → pula (registra `cache: true`
  e os tokens evitados). Mudou → refaz o pedido e para com código 10 (`--manter-roteiro` mantém o atual;
  `roteiro.refazer_se_mudar: false` só avisa). `--refazer-pedido` mede uma rodada sem cache; `--selecao-modo completo|bm25`
  sobrepõe o modo (comparar antes/depois).

## Narração (v1.3.0) — parâmetros em `narracao:` do yaml (todos opcionais; padrões em `pipeline.py`, `NARRACAO_PADRAO`)
| chave | padrão | o quê |
|---|---|---|
| `motor` | `edge` (se omitido) | v1.4.1 / narracao-tts-ptbr 1.8.0: `edge` ou `azure`. Sem a chave, o pipeline assume `edge` (cursos já existentes não mudam e não re-narram). **Padrão em todos os cursos, novos inclusive: `edge`** (decisão do Carlos, 15/11/2026); o motor `azure` fica disponível mas não é usado. `TTS_MOTOR` (env) vence o yaml. Chave e região do Azure só por `AZURE_SPEECH_KEY` e `AZURE_SPEECH_REGION`, nunca no yaml — erro claro se o motor for `azure` e faltarem. `motor: edge` (ou ausente) não entra no hash de cache. |
| `voz` | `pt-BR-FranciscaNeural` | venceu Antonio e Thalita em WER e termos em inglês |
| `rate` | `-5%` | velocidade da voz (`velocidade`, nome antigo, ainda vale); no Azure vai para `<prosody rate>` |
| `pausa_frase_ms` | 400 | silêncio entre frases (350–500 soa natural) |
| `pausa_paragrafo_ms` | 700 | entre parágrafos (quebra de linha na narração) |
| `pausa_cena_ms` | 950 | entre cenas |
| `pausa_trecho_ms` | 500 | antes e depois de um trecho original |
| `pronuncia` | `{}` | `{termo: grafia falada}` extra desta aula, por cima do mapa do modo |
| `termos_ingles` | `{modo: ingles_mesma_voz}` | v1.7: **padrão `ingles_mesma_voz`** (decisão do Carlos em 2026-11-14): Francisca -5%, frase inteira, grafias de som inglês (`pronuncia-ingles-francisca.json`), sem emenda e sem outra voz; `termos_ingles.json` sai sem emendas. `aportuguesar` foi o padrão até a v1.6. A emenda en-US (`emendar_en`, voz `en-US-AvaNeural`) foi testada e **recusada pelo Carlos na escuta** (2026-11-14); fica como opção. `modo`: `emendar_en` (frase na Francisca, termo dito pela voz en-US e emendado com volume/tom ajustados e crossfade), `multilingual` (frase inteira em `voz_multilingual`, padrão pt-BR-ThalitaMultilingualNeural), `original` (Francisca lê a grafia original), `aportuguesar` (mapa até a v1.4), `ssml_lang` (o serviço recusa: cai para `emendar_en`). `termos: [...]` soma e `sem_ingles: [...]` tira da lista `narracao-tts-ptbr/references/termos-ingles.json` |
| `whisper_modelo`, `termos_checagem` | `small`, `[]` | conferência por transcrição reversa |
As pausas são silêncio real entre frases sintetizadas uma a uma (o edge-tts não aceita SSML); SRT e `timings.json`
saem nos tempos novos, e vídeo e página continuam lendo os mesmos campos.
