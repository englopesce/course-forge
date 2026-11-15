---
name: curso-a-partir-de-ementa
description: Transforma uma ementa (texto livre com módulos, unidades e tópicos) num curso inteiro em vídeo — módulos → aulas com objetivos, tipo e duração, CURSO.md/curso.json legíveis e um aula.yaml por aula — e roda o pipeline aula-ra nas aulas escolhidas, com cache, checagem de cobertura de todos os tópicos e público/nível/tom como parâmetros. Use quando pedirem um curso, trilha ou série de aulas completa a partir de uma ementa, plano de ensino ou programa de disciplina.
---

# curso-a-partir-de-ementa

Arquivos auxiliares relativos a esta pasta (instalada em `/home/box/agent-data/workflows/curso-a-partir-de-ementa/`).
Usa as skills irmãs da aula-ra (pipeline por aula) e codigo-exemplo-aula (aulas com código).
Python do venv com PyYAML (o mesmo da aula-ra).

## Passos
1. Copie `templates/curso_exemplo.yaml` para a pasta do curso como `curso.yaml` e ajuste: `curso.ementa` (arquivo
   de texto), `publico`, `nivel`, `tom`, `linguagem` (vão para todo roteiro), `estrutura` (aulas por módulo,
   duração, `cobertura: erro|aviso`), `padrao_aula` (base de todo aula.yaml: formatos, marca, `narracao: {motor, voz, rate, pausa_frase_ms, pausa_paragrafo_ms,
   pausa_cena_ms, termos_ingles, pronuncia}` — repassados a todas as aulas). **Motor (v1.5.1):** o template vem com
   `narracao.motor: edge` — padrão de TODOS os cursos, novos inclusive (decisão do Carlos, 15/11/2026). O motor
   `azure` existe na narracao-tts-ptbr mas não deve ser usado; não re-narrar aulas prontas. Voz padrão
   `pt-BR-FranciscaNeural`, rate `-5%`, `termos_ingles.modo: ingles_mesma_voz`.
   Demais chaves sem valor caem nos padrões do pipeline aula-ra / narracao-tts-ptbr)
   e `por_tipo`.
2. `python scripts/curso.py estrutura curso.yaml` → lê a ementa (`ementa.json`: módulos, unidades, itens com ids
   `mNN.iNNN`/`mNN.uNN`) e, sem `estrutura.json`, escreve `PEDIDO_ESTRUTURA.md` (de `templates/prompt_estrutura.md`)
   e **para com código 10**.
3. **Julgamento do agente:** leia o pedido e escreva `estrutura.json` (esquema em `references/schema-estrutura.md`):
   divisão em aulas rápidas, objetivos (1–4, verbos observáveis), `tipo`, `duracao_video_s`, tópicos da ementa
   cobertos, `busca_videos` e `documentacao` oficial. Pode ser gerado por um script seu (versione-o junto).
4. Rode de novo `estrutura`: valida esquema e **cobertura de todos os itens da ementa** e gera `CURSO.md`
   (legível), `curso.json` e `aulas/<id>.yaml` (id `mNN-aNN`). Os yaml gerados não se editam: ajustes de cada
   aula (vídeos verificados por oEmbed, trechos, `exemplo` com checagem, `termos_checagem`, cenas, duração,
   documentação) vão em `aulas/<id>.extra.yaml`, mesclado por cima (listas substituem) e nunca sobrescrito.
5. Para cada aula a produzir: escolha vídeos de canais oficiais/confiáveis (busca sugerida no yaml,
   `_busca_videos`), confira canal/título por oEmbed, escreva o `.extra.yaml` e, se for de código, o repositório
   `exemplos/<id>/` (detectado sozinho) — veja codigo-exemplo-aula.
6. `python scripts/curso.py aulas curso.yaml --ids m01-a03,m03-a04` (ou `--tipo codigo`, `--modulo m03`) roda o
   pipeline aula-ra **em sequência** (evita 429). Aula sem vídeos: `precisa_videos` (código 10). Na 1ª vez cada
   aula para no roteiro (código 10): escreva `roteiro.json` e repita com `--from roteiro`. Repassa
   `--from/--to/--stage/--force`. Log em `_trabalho/<id>/pipeline.log`; resultado em `status.json`.
7. `python scripts/curso.py status curso.yaml` → tabela por aula (yaml, extra, roteiro, HTML, 16x9, 9x16, WER, código,
   tokens de LLM de entrada/saída/evitados) e o total do curso (soma dos `uso-tokens.json` das aulas + o do curso, que
   registra a etapa `estrutura`). Contagens do agente são estimadas (tiktoken); as de API, reais.
8. Repassa ao pipeline `--refazer-pedido`, `--manter-roteiro` e `--selecao-modo` (ver aula-ra, economia de tokens).

## Cache e versões
- Vídeos compartilhados: cada aula.yaml ganha `cache_videos` (padrão `<curso>/_cache/videos`; `cache_videos: false` no
  curso.yaml desliga). Um vídeo usado por várias aulas é baixado uma vez (por id e versão da skill de legendas).
- `estrutura` só refaz se mudar ementa, curso.yaml, estrutura.json, algum `.extra.yaml`, templates ou scripts
  (`.cache/estrutura.json`); `--force` refaz. Cada aula usa o cache da aula-ra (por etapa).
- Versione a pasta do curso (git local): curso.yaml, estrutura.json (ou o script que o gera), extras, exemplos.

## Regras
- Aulas rápidas (≈ 90–150 s de vídeo; `palavras_max` derivado da duração). Uma ideia central por aula.
- Fatos só de transcrição ou documentação oficial (`roteiro.documentacao` entra nas fontes do pedido de roteiro);
  recomendações marcadas como orientação. Vídeos: trechos curtos creditados, nunca cookies, espera progressiva no 429.
- Ementas reais têm defeitos (tópicos repetidos entre módulos, numeração quebrada): registre no relatório em vez de
  "corrigir" a ementa em silêncio. Marque as aulas afetadas com `aviso_duplicacao: "<texto>"` no `.extra.yaml`: o aviso
  vai para o CURSO.md (seção "Avisos da ementa" e na aula) e o `status` mostra `⚠dup`.
