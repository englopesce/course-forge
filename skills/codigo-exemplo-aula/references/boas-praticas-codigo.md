# Código em aula curta — boas práticas (orientação)

## Repositório de exemplo
- Mínimo que roda: um conceito por aula, sem framework extra. README com "como rodar" em 3 comandos.
- Teste automático que exercita o que a aula ensina (ex.: um client que chama a ferramenta do server).
  Teste que falha não pode travar: feche conexões/processos em `finally`.
- `package-lock.json` versionado e `npm ci` na checagem (instalação reprodutível); versões fixadas por faixa (`^`/`~`).
- Exercício com checagem: a resposta fica em `solucao/` e um script (`test:solucao`, `checar:solucao`) a testa.
  Assim a aula garante que o exercício tem solução que roda.
- Linhas ≤ ~72 caracteres, nomes em português quando forem do domínio da aula; APIs como na documentação oficial.
- Node 24: `node --test "build/test/*.test.js"` (glob entre aspas; diretório puro falha).

## Cenas com código
- Até 22 linhas por cena; prefira 8–16. Corte o que não é o ponto (imports óbvios, boilerplate).
- 1 a 4 destaques por cena, na ordem da fala; cada `nota` em até ~50 caracteres.
  No vídeo os destaques dividem o tempo da fala da cena; no HTML viram botões.
- Narre a ideia, não a sintaxe: "registramos a ferramenta com nome, descrição e esquema", não "server ponto registerTool".
  Identificadores camelCase longos soam mal no TTS — deixe-os na tela.
- Trecho do YouTube e código em cenas separadas (se houver os dois, o HTML mostra o trecho).
- Cite a documentação oficial da versão usada (SDKs mudam: confira a página no dia da aula).
