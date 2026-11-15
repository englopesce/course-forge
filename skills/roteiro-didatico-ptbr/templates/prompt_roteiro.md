# Pedido de roteiro didático (pt-BR) — preencher roteiro.json

Você é o redator de uma mini-aula. Escreva **um arquivo JSON** em `{{SAIDA}}` seguindo
`references/schema-roteiro.md` (pasta da skill roteiro-didatico-ptbr) e o checklist
`references/checklist-fatos.md`. Depois rode a validação indicada no fim.

## Dados da aula
- Tema: {{TEMA}}
- Público: {{PUBLICO}}
- Nível: {{NIVEL}}
- Tom: {{TOM}}
- Objetivo: {{OBJETIVO}}
{{CONTEXTO}}- Duração-alvo do vídeo: {{DURACAO}} s no total (narração ≈ {{PALAVRAS}} palavras, já descontados os trechos)
- Número de passos/cenas: {{CENAS}}
- Idioma: português do Brasil; {{LINGUAGEM}}.

## Fontes (use SÓ o que está nelas para fatos)
{{FONTES}}

## Trechos do vídeo original que vão entrar (já definidos na configuração)
Cada trecho precisa estar numa cena (`cenas[].trecho.id`). A narração dessa cena deve
**apresentar** o trecho ("Veja no vídeo original...") e terminar antes dele; o trecho toca com o
áudio original e legenda em pt-BR que você escreve em `trecho.legendas` (tempos relativos ao início
do trecho, traduzindo fielmente a fala abaixo, sem inventar).
{{TRECHOS}}

## Regras
1. Fatos só das fontes (transcrições e documentação oficial listadas). Analogias marcadas como analogia.
   Recomendações próprias (orientação) só na última cena ("{{FECHAMENTO}}").
2. `tela`: 2–3 frases de até ~55 caracteres cada. `narracao`: 1–3 frases por cena.
3. Estrutura sugerida: {{ESTRUTURA}}.
4. Preencha `fatos` com cada afirmação e o trecho da fonte que a sustenta.
5. Termos em inglês que a voz pode errar: deixe para `pronuncia` (a etapa de narração ajusta).

{{TECNICO}}## Validar
`python3 {{VALIDADOR}} {{SAIDA}} --config {{CONFIG}}`
Depois retome o pipeline: `{{RETOMAR}}`
