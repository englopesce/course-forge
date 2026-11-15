# Esquema do roteiro.json

```json
{
  "titulo": "Título da aula",
  "subtitulo": "Uma aula rápida para ...",
  "publico": "diretores, não técnicos | programadores, nível intermediário",
  "fonte": {"titulo": "...", "canal": "...", "url": "https://www.youtube.com/watch?v=ID", "titulo_curto": "..."},
  "fontes_extras": [{"titulo": "...", "canal": "...", "url": "..."}],
  "pronuncia": {"Termo": "grafia-fonética-só-para-a-voz"},
  "cenas": [
    {
      "id": "kebab-case-unico",
      "titulo": "Título da tela",
      "tela": ["frase curta 1", "frase curta 2", "frase curta 3"],
      "narracao": "Texto falado em pt-BR.",
      "icone": "🎯",
      "layout": "lista | fluxo",
      "trecho": {
        "id": "id-do-trecho-na-config",
        "legendas": [{"de": 0.0, "ate": 3.2, "texto": "tradução pt-BR da fala"}]
      },
      "codigo": {
        "arquivo": "src/index.ts", "linhas": "9-27", "linguagem": "ts (opcional, pelo sufixo)", "titulo": "opcional",
        "destaques": [{"linhas": "11-14", "nota": "nota curta (≤ ~50 caracteres)"}]
      }
    }
  ],
  "exercicios": [
    {"id": "ex1", "titulo": "...", "enunciado": "...", "dica": "...", "arquivo": "src/x.ts (opcional)",
     "checagem": "nome de um comando de exemplo.checagem (opcional)"}
  ],
  "fatos": [{"afirmacao": "...", "fonte": "trecho literal da transcrição (com tempo mm:ss)"}]
}
```

- `fonte` = vídeo principal (crédito geral). Créditos de cada trecho vêm da etapa de trechos.
- `fontes_extras` (opcional) = outros vídeos/documentos usados como base; entram no crédito final da página e do vídeo
  (os vídeos dos trechos entram automaticamente).
- `pronuncia` (opcional) soma-se ao mapa padrão `narracao-tts-ptbr/references/pronuncia-padrao.json`
  (o do roteiro vence; `"pronuncia_padrao": false` desliga o padrão).
- `trecho` é opcional; no máximo um por cena. A narração da cena acontece **antes** do trecho.
- `layout: "fluxo"` desenha cartões com setas (bom para etapas); padrão é lista.
- 5 a 8 cenas. A última deve ser "Para lembrar" (recomendações próprias, não atribuídas à fonte).
  O nome da última cena vem de `roteiro.fechamento` na config (ex.: "Na prática" para programadores).

## Parâmetros do pedido (aula.yaml)
`aula.publico`, `aula.nivel`, `aula.tom`, `aula.linguagem`, `aula.contexto` (lista: curso, módulo, aula anterior/
próxima…) e `roteiro.estrutura`, `roteiro.fechamento`, `roteiro.cenas`, `roteiro.duracao_alvo`, `roteiro.palavras_max`,
`roteiro.documentacao` ([{titulo, url, arquivo?}] — documentação oficial que vira fonte de fatos, como as transcrições).
Padrão (sem nada na config): público não técnico, tom didático, fechamento "Para lembrar".

## Aulas técnicas (com `exemplo` na config — skill codigo-exemplo-aula)
- `codigo` (opcional, por cena): trecho do **repositório de exemplo testado** (`arquivo` relativo a `exemplo.dir`,
  `linhas` "a-b" ≤ 22 linhas). `destaques` (1–4) dentro da faixa, na ordem da fala; no vídeo dividem o tempo da cena.
  Cena com código: 1–2 itens de `tela`. Não ponha `trecho` e `codigo` na mesma cena (o HTML mostraria só o trecho).
- `exercicios` (opcional): viram `exercicios.md` e a seção "Exercícios práticos" do HTML. `checagem` = nome de um
  comando de `exemplo.checagem` que prova a solução (ex.: `solucao`); sem checagem = exercício aberto.
- Narre a ideia, não a sintaxe; identificadores longos (camelCase) ficam na tela, não na voz.
