---
name: codigo-exemplo-aula
description: Etapa "codigo" de uma aula técnica (aula-ra) — roda o repositório de exemplo da aula numa cópia limpa (install, build, testes, solução dos exercícios), extrai do próprio repositório os trechos de código citados nas cenas do roteiro (com realce de sintaxe offline e destaques por linha) e gera exercicios.md; falha se o código não rodar. Use quando uma aula para programadores precisar mostrar código na tela (vídeo e HTML), ter exercícios e um repositório executável conferido automaticamente.
---

# codigo-exemplo-aula

Arquivos auxiliares relativos a esta pasta (instalada em `/home/box/agent-data/workflows/codigo-exemplo-aula/`).
Leia `references/boas-praticas-codigo.md` antes de escrever o repositório e as cenas com código.

**Fonte única de verdade:** o código que aparece na tela sai do repositório testado, nunca de texto colado no roteiro.

1. Repositório da aula (escrito pelo agente): pasta pequena e executável (ex.: `exemplos/<id-da-aula>/`) com
   README, testes automáticos e `solucao/` para cada exercício que tiver checagem. Linhas ≤ ~72 caracteres.
2. No `aula.yaml`:
   ```yaml
   exemplo:
     dir: ../exemplos/m03-a04            # relativo ao yaml
     checagem:                           # rodados em <trabalho>/exemplo-run (cópia sem node_modules/dist/build/.git)
       - {nome: instalar, cmd: npm ci}
       - {nome: build, cmd: npm run build}
       - {nome: teste, cmd: npm test, timeout: 180}
       - {nome: solucao, cmd: npm run test:solucao}
   ```
3. No `roteiro.json` (skill roteiro-didatico-ptbr): `cenas[].codigo = {arquivo, linhas "a-b", destaques [{linhas, nota}],
   linguagem?, titulo?}` (≤ 22 linhas; 1–2 itens de `tela` nessa cena; trecho do YouTube em outra cena) e
   `exercicios = [{id, titulo, enunciado, dica, arquivo?, checagem?}]` (`checagem` = nome de um comando acima).
4. Rodar: o pipeline aula-ra faz sozinho (etapa `codigo`, entre `roteiro` e `narracao`; pulada se a aula não tem
   `exemplo`, código nem exercícios). Manual:
   `python3 scripts/etapa_codigo.py --config aula.yaml --roteiro roteiro.json --saida <saida> --trabalho <trabalho>`.
5. Saídas: `<saida>/codigo/snippets.json` (linhas realçadas + destaques, usado por pagina-html-gsap e
   video-hyperframes com `--codigo`), `<saida>/codigo/checagem.json` e `log_NN_<nome>.txt`, `<saida>/exemplo/`
   (cópia do repositório para o aluno) e `<saida>/exercicios.md`. Código de saída 1 = algo não rodou: corrija o
   repositório antes de seguir (a verificação final da aula também falha se `checagem.json` não estiver ok).

Realce: `scripts/realce.py` (offline, sem dependências) para ts/js/json/bash/yaml/md/mdc/py/txt; avisa linha > 72
caracteres ou trecho > 22 linhas. Não use `console.log` em servidor stdio de exemplo (vai para o protocolo).
