---
name: roteiro-didatico-ptbr
description: >-
  Escreve e valida o roteiro.json de uma mini-aula em pt-BR para o público
  definido na config (de diretores não técnicos a programadores), com cenas de
  telas curtas, narração, analogias, fechamento ("Para lembrar"/"Na prática"),
  legendas pt-BR dos trechos e, em aulas técnicas, cenas com código do
  repositório de exemplo e exercícios; fatos ancorados em transcrição ou
  documentação oficial. Use quando precisar transformar transcrição(ões) de
  vídeo e docs em roteiro didático para página HTML e/ou vídeo narrado, sobre
  qualquer tema.
---
# roteiro-didatico-ptbr

Arquivos auxiliares relativos a esta pasta (instalada em `/home/box/agent-data/workflows/roteiro-didatico-ptbr/`).

Esta é a etapa que **o agente escreve** (não é automática).

1. Gerar o pedido com as entradas: `python3 scripts/make_request.py --config aula.yaml --legendas <pasta_legendas> --saida roteiro.json --pedido PEDIDO_ROTEIRO.md`
   (o pipeline aula-ra faz isso sozinho e para, dizendo o caminho).
   Público, nível, tom, linguagem, contexto do curso, estrutura das cenas, fechamento e documentação oficial vêm
   da config (`aula.*`, `roteiro.*`; ver `references/schema-roteiro.md`). Com `exemplo.dir` o pedido ganha a seção
   técnica: arquivos do repositório (com nº de linhas), comandos de checagem e o formato de `codigo`/`exercicios`.
   Seleção (v1.4.0, economia de tokens): `python3 scripts/seleciona_trechos.py --config aula.yaml --legendas <pasta> --saida selecao.json`
   escolhe por BM25 as janelas (~45 s, com tempos) relevantes ao tema/objetivo/tópicos/termos/trechos, até
   `roteiro.selecao.max_tokens` (padrão 2500), sempre com as janelas em volta dos trechos; `make_request.py --selecao selecao.md`
   põe só elas no pedido. `modo: completo` volta ao comportamento antigo. Palavras em inglês da fonte: `palavras_chave`
   na config ou o glossário `references/glossario-pt-en.json`.
2. Ler `PEDIDO_ROTEIRO.md` (feito de `templates/prompt_roteiro.md`), os trechos selecionados que ele já traz (a transcrição inteira só se faltar algo essencial) e os docs citados e escrever
   `roteiro.json` no formato de `references/schema-roteiro.md`, seguindo `references/checklist-fatos.md`.
3. Validar: `python3 scripts/validate_roteiro.py roteiro.json --config aula.yaml` (precisa de PyYAML para `--config`).
   Confere também: arquivo e faixa de linhas do `codigo`, destaques dentro da faixa, trecho > 22 linhas (aviso),
   repositório sem nenhuma cena com código (aviso), `checagem` dos exercícios existente.

Boas práticas: uma ideia por tela; 2–3 frases curtas; verbo no início; exemplo concreto do vídeo; fechar com 3
lembretes acionáveis. Público não técnico: analogia do cotidiano. Programadores: mostrar o código real (do
repositório testado), dizer o porquê de cada decisão, erros comuns; identificadores longos ficam na tela, não na voz.
Exemplo completo: `templates/roteiro_exemplo.json`.
