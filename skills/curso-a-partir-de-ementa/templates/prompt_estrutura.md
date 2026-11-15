# Pedido de estrutura de curso — preencher estrutura.json

Você é o designer instrucional do curso. Transforme a ementa em **módulos → aulas curtas** e escreva
**um arquivo JSON** em `{{SAIDA}}` no formato de `{{ESQUEMA}}`. Depois rode a validação do fim.

## Curso
- Título: {{TITULO}}
- Público: {{PUBLICO}}
- Nível: {{NIVEL}}
- Tom: {{TOM}}
- Objetivo geral: {{OBJETIVO}}
- Ementa original: `{{EMENTA_TXT}}`
- Ementa estruturada (USE OS IDS DAQUI): `{{EMENTA_JSON}}` — cada item tem `id` (ex.: `m01.i006`), `nivel`, `pai`, `unidade`.

## Módulos encontrados
{{MODULOS}}

## Regras
1. Mantenha os módulos da ementa (mesmos ids `m01`…, mesma ordem). Não invente conteúdo fora da ementa.
2. Cada aula = **uma ideia central** que cabe em um vídeo curto de {{DURACAO_VIDEO}} s, mais prática fora do vídeo.
   Módulos com {{AULAS_POR_MODULO}} aulas (junte itens pequenos e parecidos; divida itens grandes).
3. **Cobertura total**: todo item da ementa precisa estar em `topicos` de alguma aula (o id do item, de um ancestral
   dele ou da unidade `mNN.uNN`). O validador recusa se faltar item.
4. `tipo`: `conceitual` (explica como algo funciona), `codigo` (escreve/roda código: exige repositório de exemplo
   testado), `ferramenta` (configura/usa uma ferramenta), `pratica`/`projeto` (laboratório ou entrega guiada),
   `carreira` (soft skills, mercado).
5. `objetivos`: 1–3 por aula, verbos observáveis ("implementar", "explicar", "configurar", "comparar"), do ponto de vista
   do aluno. `duracao_estudo_min` = tempo de prática/leitura além do vídeo.
6. Ordem didática dentro do módulo: base antes de aplicação; práticas da ementa ("Prática N", "Hands-on", "Projeto")
   viram aulas `pratica`/`projeto` com `pratica` descrevendo a entrega.
7. `busca_videos`: 1–2 termos de busca em inglês para achar vídeo de canal **oficial/confiável** (o vídeo é escolhido
   depois, por aula, e verificado via oEmbed). `documentacao`: URLs de documentação oficial, quando houver.
{{REGRAS}}

## Validar e gerar os aula.yaml
`{{VALIDAR}}`
(ERRO = corrija o JSON; AVISO = revise. Sem erros, o comando gera CURSO.md, curso.json e aulas/<id>.yaml.)
