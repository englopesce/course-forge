# IA para Jornalismo

Curso prático para jornalistas, editores, chefes de reportagem e analistas de audiência da Rede Amazônica usarem inteligência artificial com método jornalístico: apurar, escutar o público, monitorar diários oficiais, cruzar dados, verificar conteúdo, montar pipelines em que o modelo só entra quando a linguagem ou o julgamento são necessários, e decidir com responsabilidade editorial. Não forma programadores.

- **Público:** Jornalistas, editores, chefes de reportagem e analistas de audiência da Rede Amazônica (TV e plataformas digitais no Norte do Brasil). Não é um curso de formação de programadores.
- **Nível:** introdutório a intermediário — parte das rotinas de apuração, edição e escuta do público; quem já trabalha com dados avança nos módulos 6 a 8 e no de pipelines, sem deixar o restante do grupo para trás
- **Tom:** claro e direto, de redação para redação; analogias do jornalismo do dia a dia; a IA auxilia, a responsabilidade editorial é sempre humana
- **Ementa:** `/workspace/aula-ra/ementa-ia-jornalismo.txt` (284 itens; 284 cobertos pelas aulas)
- **Tamanho:** 13 módulos, 124 aulas, 244 min de vídeo + 58.6 h de prática/estudo estimadas

**Pré-requisitos do curso:** Rotina de apuração, edição ou escuta do público numa redação (TV ou plataformas digitais); Não é exigido saber programar; o módulo de pipelines ensina o suficiente para desenhar etapas, pedir trechos à IA, rodar e conferir

## 1. Fundamentos de IA e limites no jornalismo

*Dar à redação o vocabulário e os limites da IA: o que o modelo faz, onde ajuda, onde não se confia e quais riscos nomear desde o primeiro dia.*

11 aulas · 20.8 min de vídeo · 220 min de prática/estudo

| Aula | Título | Tipo | Vídeo | Prática | Objetivos |
|---|---|---|---|---|---|
| m01-a01 | IA, aprendizado de máquina e IA generativa: o que muda para a redação | conceitual | 1:50 | 15 min | Diferenciar inteligência artificial, aprendizado de máquina e IA generativa<br>Dizer, em uma frase, o que cada uma dessas ideias implica na rotina da pauta |
| m01-a02 | O modelo prevê texto: fluência não é apuração | conceitual | 2:00 | 20 min | Explicar que um modelo de linguagem prevê a continuação mais provável de um texto, e não 'sabe' ou 'apura'<br>Relacionar a fluência da resposta com o risco de alucinação |
| m01-a03 | Gerar conteúdo não é o mesmo que analisar ou buscar dados | conceitual | 1:50 | 15 min | Distinguir ferramentas que geram conteúdo das que analisam, buscam ou organizam dados<br>Reconhecer multimodalidade em termos jornalísticos: texto, imagem, áudio e vídeo como entrada e como saída |
| m01-a04 | Onde a IA costuma ajudar na redação | conceitual | 1:50 | 20 min | Listar usos em que a IA costuma ajudar: transcrição, triagem, síntese, acervo, extração preliminar, tradução de apoio e rascunho de estrutura<br>Separar esses apoios de uma apuração pronta para ir ao ar |
| m01-a05 | Onde não se pode confiar sem validação humana | conceitual | 2:00 | 20 min | Identificar o que exige validação humana: atribuição, números, citações, nexo causal, identificação de pessoas e fatos sem fonte rastreável<br>Aplicar a regra: nada disso vai ao ar só porque a IA afirmou |
| m01-a06 | Defina o problema editorial antes de escolher a ferramenta | conceitual | 1:40 | 20 min | Formular o que a pauta precisa resolver, com qual prazo e qual risco, antes de abrir um chat<br>Justificar a escolha da ferramenta a partir do problema, não do hábito |
| m01-a07 | Acertos e fracassos documentados no uso de IA no jornalismo | conceitual | 2:00 | 25 min | Citar exemplos reais de uso de IA no jornalismo com acerto ou fracasso documentado<br>Extrair uma lição prática de cada caso, sem generalizar além da fonte |
| m01-a08 | O que muda — e o que não muda — no método jornalístico | conceitual | 1:50 | 15 min | Recorrer a pauta, apuração, checagem, edição e publicação como etapas que a IA não substitui<br>Dizer o que pode mudar na execução de cada etapa sem abrir mão da responsabilidade editorial |
| m01-a09 | Alucinação, viés, desatualização e o tom seguro da resposta | conceitual | 1:50 | 20 min | Nomear alucinação, viés, desatualização e confiança excessiva no tom seguro da resposta<br>Reconhecer o tom seguro como um risco, não como um sinal de acerto |
| m01-a10 | O que o modelo conhece mal sobre a Amazônia e o interior | conceitual | 2:00 | 25 min | Explicar o viés de treino e de recorte regional: Amazônia, povos indígenas, cidades do interior e línguas locais<br>Adotar a conferência em fonte local como regra quando o tema for territorial ou indígena |
| m01-a11 | O que não colar na nuvem — e o custo de um erro no ar | conceitual | 2:00 | 25 min | Identificar o que não deve ser colado em ferramentas na nuvem (fonte em risco, sigilo, dado pessoal desnecessário)<br>Relacionar uso opaco ou erro da IA no ar com o impacto na confiança do público |

<details><summary>m01-a01 — tópicos da ementa e prática</summary>

- Diferença entre inteligência artificial, aprendizado de máquina e IA generativa

Config: `aulas/m01-a01.yaml` · saída: `m01-fundamentos-ia-limites/m01-a01-ia-ml-e-ia-generativa/`

</details>

<details><summary>m01-a02 — tópicos da ementa e prática</summary>

- O que um modelo de linguagem faz de fato: prever a continuação mais provável de um texto, não "saber" ou "apurar"
- Por que o texto sai fluente mesmo quando o conteúdo está errado (alucinação)

Config: `aulas/m01-a02.yaml` · saída: `m01-fundamentos-ia-limites/m01-a02-o-modelo-preve-texto/`

</details>

<details><summary>m01-a03 — tópicos da ementa e prática</summary>

- Ferramentas que geram conteúdo versus ferramentas que analisam, buscam ou organizam dados (distinção útil para escolher o instrumento certo)
- Multimodalidade em termos jornalísticos: texto, imagem, áudio e vídeo como entrada e como saída

Config: `aulas/m01-a03.yaml` · saída: `m01-fundamentos-ia-limites/m01-a03-gerar-versus-analisar/`

</details>

<details><summary>m01-a04 — tópicos da ementa e prática</summary>

- Onde costuma ajudar: transcrição, triagem, síntese, organização de acervo, extração preliminar, tradução de apoio, rascunho de estrutura

Config: `aulas/m01-a04.yaml` · saída: `m01-fundamentos-ia-limites/m01-a04-onde-a-ia-ajuda/`

</details>

<details><summary>m01-a05 — tópicos da ementa e prática</summary>

- Onde não se pode confiar sem validação humana: atribuição, números, citações, nexo causal, identificação de pessoas, "fatos" sem fonte rastreável

Config: `aulas/m01-a05.yaml` · saída: `m01-fundamentos-ia-limites/m01-a05-onde-nao-confiar/`

</details>

<details><summary>m01-a06 — tópicos da ementa e prática</summary>

- Definir o problema editorial antes de escolher a ferramenta (o que a pauta precisa resolver, com qual prazo e qual risco)

Config: `aulas/m01-a06.yaml` · saída: `m01-fundamentos-ia-limites/m01-a06-problema-editorial-primeiro/`

</details>

<details><summary>m01-a07 — tópicos da ementa e prática</summary>

- Exemplos reais de uso de IA no jornalismo, com acertos e fracassos documentados em reportagens e treinamentos de referência

Config: `aulas/m01-a07.yaml` · saída: `m01-fundamentos-ia-limites/m01-a07-acertos-e-fracassos/`

</details>

<details><summary>m01-a08 — tópicos da ementa e prática</summary>

- O que muda (e o que não muda) no método jornalístico: pauta, apuração, checagem, edição e publicação

Config: `aulas/m01-a08.yaml` · saída: `m01-fundamentos-ia-limites/m01-a08-o-metodo-nao-muda/`

</details>

<details><summary>m01-a09 — tópicos da ementa e prática</summary>

- Alucinação, viés, desatualização e confiança excessiva no tom seguro da resposta

Config: `aulas/m01-a09.yaml` · saída: `m01-fundamentos-ia-limites/m01-a09-riscos-do-primeiro-dia/`

</details>

<details><summary>m01-a10 — tópicos da ementa e prática</summary>

- Viés nos dados de treino e no recorte regional: o que um modelo "conhece" mal sobre a Amazônia, povos indígenas, cidades do interior e línguas locais

Config: `aulas/m01-a10.yaml` · saída: `m01-fundamentos-ia-limites/m01-a10-vies-sobre-a-amazonia/`

</details>

<details><summary>m01-a11 — tópicos da ementa e prática</summary>

- Privacidade e segurança: o que não deve ser colado em ferramentas na nuvem
- Impacto na confiança do público quando o uso é opaco ou quando um erro da IA vai ao ar

Config: `aulas/m01-a11.yaml` · saída: `m01-fundamentos-ia-limites/m01-a11-privacidade-e-confianca/`

</details>

## 2. Uso comparado de Claude, Gemini, Grok e ChatGPT

*Comparar assistentes com método (não com propaganda), sabendo quando cada um faz sentido e o que conferir na documentação vigente.*

12 aulas · 23.5 min de vídeo · 325 min de prática/estudo

| Aula | Título | Tipo | Vídeo | Prática | Objetivos |
|---|---|---|---|---|---|
| m02-a01 | Critérios para comparar assistentes sem cair em propaganda | conceitual | 2:00 | 20 min | Listar critérios práticos: tipo de tarefa, citação de fontes, multimodalidade, trabalho em equipe, custo, limite de uso, retenção de dados e o que a casa já contrata<br>Montar uma ficha de comparação reutilizável pela editoria |
| m02-a02 | Teste lado a lado: a mesma pauta, o mesmo pacote, dois relógios | pratica | 2:00 | 40 min | Rodar o mesmo pacote de documentos e a mesma pauta em mais de um assistente, anotando acertos, invenções e recusas<br>Registrar velocidade e precisão em separado, sem tratar uma como prova da outra |
| m02-a03 | Conta da casa versus conta pessoal — e a comparação não é um ranking | conceitual | 1:50 | 20 min | Explicar o que muda em sigilo, histórico e conformidade entre plano, conta corporativa e conta pessoal<br>Tratar a comparação como método revisável, não como ranking permanente, porque as capacidades mudam |
| m02-a04 | ChatGPT: o que o plano contratado liga — e os GPTs da editoria | ferramenta | 2:00 | 30 min | Conferir, no plano contratado, quais ferramentas estão ligadas (pesquisa, arquivos, voz, imagem)<br>Configurar um GPT personalizado com instruções fixas, arquivos de apoio e formato de saída para uma tarefa repetida |
| m02-a05 | Quando o ChatGPT faz sentido — e o limite da apuração | conceitual | 1:50 | 20 min | Indicar usos cabíveis: rascunho de estrutura, brainstorm de ângulos e apoio a tarefas gerais, sempre com revisão editorial<br>Recusar tratar a resposta como apuração pronta; conferir fontes e números fora do chat |
| m02-a06 | Claude: documentos longos e a janela de contexto vigente | ferramenta | 2:00 | 25 min | Explicar por que o Claude é frequentemente usado para ler documentos longos<br>Conferir na documentação oficial da Anthropic o tamanho vigente da janela de contexto, sem decorar um número que pode mudar |
| m02-a07 | Projetos no Claude: quando usar e o que a janela longa não dispensa | ferramenta | 2:00 | 30 min | Organizar o material de uma pauta ou de uma editoria em Projetos e espaços de trabalho<br>Usar o Claude para leitura de processos, relatórios e transcrições longas, com checagem humana de cifras, nomes e trechos |
| m02-a08 | Gemini, NotebookLM e Pinpoint no acervo da casa | ferramenta | 2:10 | 35 min | Descrever a integração do Gemini com o Google Workspace quando a administração da casa habilita o acesso<br>Distinguir NotebookLM (caderno ancorado nos arquivos enviados) de Pinpoint (organização, busca, OCR e transcrição em coleções grandes) |
| m02-a09 | Fact Check Explorer, Gems e o risco da pesquisa longa | ferramenta | 2:00 | 30 min | Localizar o Fact Check Explorer e outras ferramentas Google de verificação quando couberem à pauta<br>Usar Gems e pesquisa longa (Deep Research) com o alerta, já documentado em treinamentos jornalísticos, de fontes fabricadas ou mal atribuídas |
| m02-a10 | Quando o ecossistema Google faz sentido na pauta | conceitual | 1:40 | 15 min | Indicar o uso quando a pauta já vive no Workspace da empresa, em acervos documentais ou em pesquisa ancorada nos arquivos da própria equipe<br>Evitar escolher o Gemini só por ser o da empresa, se a tarefa não se beneficia dessa âncora |
| m02-a11 | Grok e a busca no X: escuta com conferência do post original | ferramenta | 2:10 | 30 min | Localizar o Grok nos produtos da xAI e no X, sabendo que o que cada interface oferece depende do plano e da conta<br>Usar a busca no X (palavra-chave, significado, usuários e fios, com recorte de contas e datas) para escutar o que circula, citando e conferindo o post original — sem tratar tendência no X como tendência da audiência da TV |
| m02-a12 | Planilhas, ferramenta especializada e o registro da comparação | pratica | 1:50 | 30 min | Organizar extrações em tabela ou CSV com planilhas (incluindo Gemini ou complementos no Google Sheets)<br>Decidir quando vale uma ferramenta especializada em vez do chat genérico e registrar o que foi usado, conferido e descartado |

<details><summary>m02-a01 — tópicos da ementa e prática</summary>

- Critérios práticos: tipo de tarefa, qualidade da citação de fontes, multimodalidade, trabalho em equipe, custo, limite de uso, política de retenção de dados e o que a organização já contrata

Config: `aulas/m02-a01.yaml` · saída: `m02-uso-comparado-assistentes/m02-a01-criterios-para-comparar/`

</details>

<details><summary>m02-a02 — tópicos da ementa e prática</summary>

- Teste lado a lado com a mesma pauta e o mesmo pacote de documentos, anotando acertos, invenções e recusas
- Velocidade não é o mesmo que precisão: como registrar os dois no teste

**Prática:** Testar a mesma pauta e o mesmo pacote de documentos em dois assistentes; anotar acertos, invenções, recusas, tempo e precisão.

Config: `aulas/m02-a02.yaml` · saída: `m02-uso-comparado-assistentes/m02-a02-teste-lado-a-lado/`

</details>

<details><summary>m02-a03 — tópicos da ementa e prática</summary>

- Planos, contas corporativas e contas pessoais: o que muda em sigilo, histórico e conformidade
- Capacidades mudam com frequência; a comparação desta ementa é um método, não um ranking permanente

Config: `aulas/m02-a03.yaml` · saída: `m02-uso-comparado-assistentes/m02-a03-conta-corporativa-e-metodo/`

</details>

<details><summary>m02-a04 — tópicos da ementa e prática</summary>

- Assistente de uso geral, muito presente na rotina de redações; conferir no plano contratado quais ferramentas estão ligadas (pesquisa, arquivos, voz, imagem)
- GPTs personalizados: instruções fixas, arquivos de apoio e formato de saída para tarefas repetidas da editoria

**Prática:** Rascunhar as instruções de um GPT da editoria (tarefa, formato de saída e o que ele deve admitir que não encontrou).

Config: `aulas/m02-a04.yaml` · saída: `m02-uso-comparado-assistentes/m02-a04-chatgpt-plano-e-gpts/`

</details>

<details><summary>m02-a05 — tópicos da ementa e prática</summary>

- Quando faz sentido: rascunho de estrutura, brainstorm de ângulos, apoio a tarefas gerais — sempre com revisão editorial
- Limite: não tratar a resposta como apuração pronta; conferir fontes e números fora do chat

Config: `aulas/m02-a05.yaml` · saída: `m02-uso-comparado-assistentes/m02-a05-quando-usar-chatgpt/`

</details>

<details><summary>m02-a06 — tópicos da ementa e prática</summary>

- Família de modelos frequentemente usada para ler e analisar documentos longos; a janela de contexto vigente deve ser conferida na documentação oficial da Anthropic

Config: `aulas/m02-a06.yaml` · saída: `m02-uso-comparado-assistentes/m02-a06-claude-janela-de-contexto/`

</details>

<details><summary>m02-a07 — tópicos da ementa e prática</summary>

- Projetos (Projects) e espaços de trabalho para reunir o material de uma pauta ou de uma editoria
- Quando faz sentido: leitura de processos, relatórios, transcrições longas e revisão cuidadosa de texto, com checagem humana dos trechos usados
- Limite: contexto longo não dispensa a leitura jornalística nem a conferência de cifras e nomes

Config: `aulas/m02-a07.yaml` · saída: `m02-uso-comparado-assistentes/m02-a07-projetos-no-claude/`

</details>

<details><summary>m02-a08 — tópicos da ementa e prática</summary>

- Integração com serviços do Google Workspace (por exemplo Gmail, Drive e Documentos), quando a conta e a administração da organização habilitam esse acesso — conforme a documentação de suporte do Google
- NotebookLM: cadernos ancorados nos arquivos que a equipe envia, úteis para síntese, roteiros e perguntas sobre um acervo delimitado
- Pinpoint (Google News Initiative): organização, busca, OCR e transcrição em coleções grandes de documentos

Config: `aulas/m02-a08.yaml` · saída: `m02-uso-comparado-assistentes/m02-a08-gemini-workspace-e-acervo/`

</details>

<details><summary>m02-a09 — tópicos da ementa e prática</summary>

- Fact Check Explorer e outras ferramentas Google de verificação, quando couberem à pauta
- Gems (assistentes personalizados), Deep Research e o risco, já documentado em treinamentos jornalísticos, de fontes fabricadas ou mal atribuídas

Config: `aulas/m02-a09.yaml` · saída: `m02-uso-comparado-assistentes/m02-a09-fact-check-gems-deep-research/`

</details>

<details><summary>m02-a10 — tópicos da ementa e prática</summary>

- Quando faz sentido: pauta que já vive no Workspace da empresa, acervos documentais e pesquisa ancorada em arquivos da própria equipe

Config: `aulas/m02-a10.yaml` · saída: `m02-uso-comparado-assistentes/m02-a10-quando-o-google-faz-sentido/`

</details>

<details><summary>m02-a11 — tópicos da ementa e prática</summary>

- O Grok está disponível em produtos da xAI e no X; o que cada interface oferece depende do plano e da conta
- A documentação oficial da xAI descreve a ferramenta X Search: busca por palavra-chave e por significado, busca de usuários e recuperação de fios (threads) no X, com recorte por contas e por datas
- Quando faz sentido: escuta do que circula no X sobre um tema, uma pauta ou uma conta, com citação e conferência do post original
- Limite: isso não é acesso automático a todas as redes, nem substitui busca no YouTube, em comentários do site ou em grupos fechados; tendência no X não é tendência da audiência da TV

Config: `aulas/m02-a11.yaml` · saída: `m02-uso-comparado-assistentes/m02-a11-grok-e-busca-no-x/`

</details>

<details><summary>m02-a12 — tópicos da ementa e prática</summary>

- Planilhas (incluindo o uso de Gemini ou complementos no Google Sheets) para organizar extrações em tabela ou CSV
- Quando vale um modelo ou ferramenta especializada em vez do chat genérico
- Registro simples da comparação: qual ferramenta usamos, para quê, o que conferimos e o que descartamos

**Prática:** Preencher um registro simples: ferramenta, tarefa, o que conferiu, o que descartou.

Config: `aulas/m02-a12.yaml` · saída: `m02-uso-comparado-assistentes/m02-a12-planilhas-e-registro/`

</details>

## 3. Prompts e apuração com método

*Escrever comandos reutilizáveis para o ciclo da pauta, ancorados em fonte, com proibição de invenção e biblioteca da editoria.*

9 aulas · 17.8 min de vídeo · 265 min de prática/estudo

| Aula | Título | Tipo | Vídeo | Prática | Objetivos |
|---|---|---|---|---|---|
| m03-a01 | Anatomia de um prompt que presta para jornalismo | conceitual | 2:00 | 25 min | Montar um comando com papel, tarefa, recorte, fonte obrigatória, formato da saída e o que o modelo deve admitir que não encontrou<br>Reconhecer um prompt vago como risco editorial, não só como resultado ruim |
| m03-a02 | Peça tabela com origem — e proíba inventar página, link ou entrevista | ferramenta | 2:00 | 30 min | Pedir tabela ou CSV com colunas de origem, data, valor, nome e grau de certeza, pronto para a planilha<br>Exigir citação do trecho ou do documento de origem e proibir invenção de página, link, processo ou entrevista |
| m03-a03 | Mostre o padrão de saída e itere o que funcionou | pratica | 1:50 | 30 min | Incluir poucos exemplos bons do padrão de saída desejado, em vez de um parágrafo vago<br>Testar, ver o erro, corrigir o comando e guardar o que funcionou |
| m03-a04 | Ângulos, roteiro de entrevista e triagem do malote | ferramenta | 2:10 | 35 min | Levantar ângulos e perguntas a partir de um dossiê, sem aceitar fatos que não estejam no material<br>Tirar roteiro de entrevista e omissões do entrevistado de uma transcrição, e triar malotes, PDFs e e-mails entre pauta, rotina e olho humano imediato |
| m03-a05 | Síntese com trecho literal — e apoio à edição, com a decisão na editoria | ferramenta | 2:00 | 30 min | Sintetizar processo, relatório ou lei em linguagem clara, com trechos literais entre aspas e página ou seção<br>Usar a IA para cortes, títulos e sugestão de passagem de VT ou de texto digital, deixando a decisão com a editoria |
| m03-a06 | Pesquisa longa é ponto de partida — confira se o link existe | conceitual | 2:00 | 25 min | Tratar relatórios de modos de pesquisa longa (Deep Research e equivalentes) como ponto de partida, nunca como fonte final<br>Conferir se o link existe, se o título bate e se o trecho está lá, diante da armadilha das fontes fabricadas |
| m03-a07 | Ancorar a resposta no acervo da pauta reduz — e não elimina — o erro | ferramenta | 2:00 | 30 min | Usar NotebookLM e Pinpoint no fluxo: subir o acervo, buscar, transcrever, extrair entidades e só então sintetizar<br>Explicar busca ancorada em documentos (RAG) em linguagem de redação: reduz, mas não elimina, o risco de erro |
| m03-a08 | Arquivos sensíveis: conta da casa, anonimizar ou não enviar | conceitual | 1:50 | 20 min | Preferir ferramentas e contas corporativas para arquivos da pauta<br>Decidir anonimizar ou não enviar quando houver fonte em risco |
| m03-a09 | Biblioteca de prompts da editoria, versionada e auditável | pratica | 2:00 | 40 min | Montar modelos de prompt reutilizáveis por editoria (política, cidades, economia, meio ambiente, esportes, agronegócio)<br>Versionar o que funcionou, com exemplo de entrada e de saída revisada, e documentar o que a IA fez em cada etapa |

<details><summary>m03-a01 — tópicos da ementa e prática</summary>

- Papel, tarefa, recorte, fonte obrigatória, formato da saída e o que o modelo deve admitir que não encontrou

Config: `aulas/m03-a01.yaml` · saída: `m03-prompts-e-apuracao/m03-a01-anatomia-do-prompt/`

</details>

<details><summary>m03-a02 — tópicos da ementa e prática</summary>

- Pedir tabela ou CSV para ir direto à planilha, com colunas de origem, data, valor, nome e grau de certeza
- Obrigatoriedade de citar o trecho ou o documento de origem; proibir invenção de página, link, processo ou entrevista

Config: `aulas/m03-a02.yaml` · saída: `m03-prompts-e-apuracao/m03-a02-csv-e-proibir-invencao/`

</details>

<details><summary>m03-a03 — tópicos da ementa e prática</summary>

- Exemplos poucos e bons valem mais do que um parágrafo vago: mostrar o padrão de saída desejado
- Iterar: testar, ver o erro, corrigir o comando, guardar o que funcionou

**Prática:** Iterar um prompt três vezes a partir do erro observado e guardar a versão que funcionou.

Config: `aulas/m03-a03.yaml` · saída: `m03-prompts-e-apuracao/m03-a03-exemplos-e-iteracao/`

</details>

<details><summary>m03-a04 — tópicos da ementa e prática</summary>

- Levantamento de ângulos e perguntas a partir de um dossiê, sem aceitar "fatos" que não estejam no material
- Roteiro de entrevistas e lista de omissões do entrevistado, a partir da transcrição
- Triagem de malotes, PDFs e e-mails: o que parece pauta, o que é rotina, o que exige olho humano imediato

Config: `aulas/m03-a04.yaml` · saída: `m03-prompts-e-apuracao/m03-a04-angulos-entrevistas-triagem/`

</details>

<details><summary>m03-a05 — tópicos da ementa e prática</summary>

- Síntese de processo, relatório ou lei em linguagem clara, com trechos literais entre aspas e página ou seção
- Apoio a edição: cortes, títulos e sugestão de passagem de VT ou de texto para digital — a decisão permanece da editoria

Config: `aulas/m03-a05.yaml` · saída: `m03-prompts-e-apuracao/m03-a05-sintese-e-edicao/`

</details>

<details><summary>m03-a06 — tópicos da ementa e prática</summary>

- Uso responsável de modos de pesquisa longa (por exemplo Deep Research e equivalentes): tratar o relatório como ponto de partida, nunca como fonte final
- Armadilha das fontes fabricadas: conferir se o link existe, se o título bate e se o trecho está lá

Config: `aulas/m03-a06.yaml` · saída: `m03-prompts-e-apuracao/m03-a06-pesquisa-longa-e-fontes-fabricadas/`

</details>

<details><summary>m03-a07 — tópicos da ementa e prática</summary>

- NotebookLM e Pinpoint no fluxo: subir o acervo, buscar, transcrever, extrair entidades e só então sintetizar
- RAG em linguagem de redação: ancorar a resposta nos documentos da pauta reduz, mas não elimina, o risco de erro

Config: `aulas/m03-a07.yaml` · saída: `m03-prompts-e-apuracao/m03-a07-notebooklm-pinpoint-e-rag/`

</details>

<details><summary>m03-a08 — tópicos da ementa e prática</summary>

- Arquivos sensíveis: preferir ferramentas e contas corporativas; anonimizar ou não enviar quando houver fonte em risco

Config: `aulas/m03-a08.yaml` · saída: `m03-prompts-e-apuracao/m03-a08-arquivos-sensiveis/`

</details>

<details><summary>m03-a09 — tópicos da ementa e prática</summary>

- Modelos de prompt reutilizáveis por editoria (política, cidades, economia, meio ambiente, esportes, agronegócio)
- Versionar e compartilhar o que funcionou, com exemplo de entrada e de saída revisada
- Documentar o que a IA fez em cada etapa, para a apuração continuar auditável quando o editor perguntar

**Prática:** Guardar um prompt da sua editoria com exemplo de entrada, saída revisada e o que a IA fez em cada etapa.

Config: `aulas/m03-a09.yaml` · saída: `m03-prompts-e-apuracao/m03-a09-biblioteca-da-editoria/`

</details>

## 4. Análise de comentários das matérias

*Escutar quem comenta com método, sem transformar volume em opinião pública, e levar à editoria só o que passa por revisão humana.*

10 aulas · 19.3 min de vídeo · 245 min de prática/estudo

| Aula | Título | Tipo | Vídeo | Prática | Objetivos |
|---|---|---|---|---|---|
| m04-a01 | Cada canal de comentário representa um recorte diferente | conceitual | 1:50 | 15 min | Mapear comentários no site, no aplicativo, no YouTube, no X e em outras redes da reportagem<br>Dizer o que cada canal representa — e o que ele não representa |
| m04-a02 | Comentário não é enquete — e não autoriza 'o público acha que' | conceitual | 2:00 | 20 min | Reconhecer viés de quem comenta: ruído, campanha organizada, ironia, recorte partidário e ausência de quem não fala<br>Recusar a frase do tipo 'o público acha que' a partir de comentários |
| m04-a03 | O que a redação pode aprender com quem comenta | conceitual | 1:50 | 20 min | Separar aprendizados úteis: dúvidas recorrentes, correções apontadas, temas que a matéria não cobriu, tom da recepção e sinais de assédio à equipe<br>Levar esses sinais à reunião de pauta com método, não com impressão solta |
| m04-a04 | Limpeza, frequência e agrupamento por tema — sem virar dado científico | ferramenta | 2:00 | 30 min | Fazer a limpeza mínima do texto: repetição, spam, links e variações da mesma palavra<br>Usar frequência, nuvem de palavras e agrupamento por tema na reunião de pauta, sem tratar o resultado como dado científico |
| m04-a05 | Menções, recortes amazônicos e o que muda depois de uma correção | ferramenta | 2:00 | 30 min | Separar menção à reportagem, a personagens e a assuntos laterais<br>Aplicar recortes úteis à Rede Amazônica (municípios, rios, povos, órgãos, temas) e observar séries no tempo depois de correção, segundo capítulo ou coletiva |
| m04-a06 | Classificar o tom só com amostra revisada por humano | ferramenta | 1:50 | 30 min | Fazer classificação preliminar de tom (apoio, crítica, dúvida, ataque)<br>Revisar uma amostra humana antes de qualquer relato à editoria |
| m04-a07 | Toxicidade, assédio e o que escala para a editoria ou à segurança | conceitual | 2:00 | 25 min | Identificar toxicidade, discurso de ódio, ameaça e assédio a jornalistas, entrevistados e comunidades<br>Aplicar o protocolo interno: o que escala para a editoria, o que vai para a segurança da equipe e o que não se responde |
| m04-a08 | Ironia e português regional quebram a medição automática de tom | conceitual | 1:50 | 20 min | Explicar por que ironia, português regional e código local geram erro na classificação automática<br>Tornar a amostra revisada obrigatória antes de qualquer número de sentimento |
| m04-a09 | Alertas: correção, denúncia, ataque e dúvida repetida | pratica | 2:00 | 30 min | Montar alertas para correção factual apontada por leitor, denúncia nova com indício, coordenação de ataque e dúvida repetida que pede FAQ ou matéria-explicação<br>Separar o que pode virar pauta, o que vira ajuste de linguagem e o que deve ser ignorado |
| m04-a10 | Comentário visível não autoriza expor dado pessoal — e o relato tem método | conceitual | 2:00 | 25 min | Aplicar LGPD e ética: comentário visível não autoriza expor dado pessoal, menor de idade ou alvo de ódio em reportagem posterior sem critério<br>Produzir um relato periódico à editoria com o que foi ouvido, com que método e com que limites |

<details><summary>m04-a01 — tópicos da ementa e prática</summary>

- Comentários no site, no aplicativo, no YouTube, no X e em outras redes da reportagem: o que cada canal representa

Config: `aulas/m04-a01.yaml` · saída: `m04-analise-de-comentarios/m04-a01-canais-de-comentario/`

</details>

<details><summary>m04-a02 — tópicos da ementa e prática</summary>

- Viés de quem comenta: ruído, campanha organizada, ironia, recorte partidário e ausência de quem não fala
- Comentário não é enquete e não autoriza frase do tipo "o público acha que"

Config: `aulas/m04-a02.yaml` · saída: `m04-analise-de-comentarios/m04-a02-comentario-nao-e-enquete/`

</details>

<details><summary>m04-a03 — tópicos da ementa e prática</summary>

- O que a redação pode aprender: dúvidas recorrentes, correções apontadas, temas que a matéria não cobriu, tom da recepção, sinais de assédio à equipe

Config: `aulas/m04-a03.yaml` · saída: `m04-analise-de-comentarios/m04-a03-o-que-aprender-com-comentarios/`

</details>

<details><summary>m04-a04 — tópicos da ementa e prática</summary>

- Limpeza mínima do texto: repetição, spam, links, variações da mesma palavra
- Frequência, nuvem de palavras e agrupamento por tema: o que mostrar na reunião de pauta e o que não transforma em "dado científico"

Config: `aulas/m04-a04.yaml` · saída: `m04-analise-de-comentarios/m04-a04-limpeza-frequencia-e-temas/`

</details>

<details><summary>m04-a05 — tópicos da ementa e prática</summary>

- Separar menção à reportagem, menção a personagens e menção a assuntos laterais
- Recortes úteis à Rede Amazônica: municípios, rios, povos, órgãos e temas (saúde, energia, queimadas, transporte, segurança)
- Séries no tempo: o que mudou nos comentários depois de uma correção, de um segundo capítulo ou de uma coletiva

Config: `aulas/m04-a05.yaml` · saída: `m04-analise-de-comentarios/m04-a05-mencoes-recortes-e-series/`

</details>

<details><summary>m04-a06 — tópicos da ementa e prática</summary>

- Classificação preliminar de tom (apoio, crítica, dúvida, ataque) com revisão humana de uma amostra

Config: `aulas/m04-a06.yaml` · saída: `m04-analise-de-comentarios/m04-a06-tom-e-amostra-revisada/`

</details>

<details><summary>m04-a07 — tópicos da ementa e prática</summary>

- Toxicidade, discurso de ódio, ameaça e assédio a jornalistas, entrevistados e comunidades
- Protocolo interno: o que escala para a editoria, o que vai para segurança da equipe, o que não se responde

Config: `aulas/m04-a07.yaml` · saída: `m04-analise-de-comentarios/m04-a07-toxicidade-e-protocolo/`

</details>

<details><summary>m04-a08 — tópicos da ementa e prática</summary>

- Armadilha de "medir sentimento" com IA: ironia, português regional e código local geram erro; a amostra revisada é obrigatória

Config: `aulas/m04-a08.yaml` · saída: `m04-analise-de-comentarios/m04-a08-ironia-e-portugues-regional/`

</details>

<details><summary>m04-a09 — tópicos da ementa e prática</summary>

- Alertas: correção factual apontada por leitor, denúncia nova com indício, coordenação de ataque, dúvida repetida que pede FAQs ou matéria-explicação
- O que pode virar pauta, o que vira ajuste de linguagem e o que deve ser ignorado

**Prática:** Classificar 15 comentários de uma matéria em: pauta, ajuste de linguagem ou ignorar, com uma linha de justificativa.

Config: `aulas/m04-a09.yaml` · saída: `m04-analise-de-comentarios/m04-a09-alertas-e-o-que-vira-pauta/`

</details>

<details><summary>m04-a10 — tópicos da ementa e prática</summary>

- LGPD e ética: comentário visível não autoriza expor dado pessoal, menor de idade ou alvo de ódio em reportagem posterior sem critério
- Relato periódico para a editoria: o que foi ouvido, com que método, com que limites

Config: `aulas/m04-a10.yaml` · saída: `m04-analise-de-comentarios/m04-a10-lgpd-nos-comentarios-e-relato/`

</details>

## 5. Agência de escuta (social listening)

*Desenhar uma escuta jornalística territorial da Rede Amazônica, com dicionário regional, alertas e ética, sem confundir volume com opinião pública.*

10 aulas · 19.5 min de vídeo · 260 min de prática/estudo

| Aula | Título | Tipo | Vídeo | Prática | Objetivos |
|---|---|---|---|---|---|
| m05-a01 | Escuta jornalística não é monitoramento de marca nem pesquisa de opinião | conceitual | 2:00 | 20 min | Diferenciar monitoramento de menções à marca, escuta jornalística e pesquisa de opinião<br>Definir a função: temas emergentes, desinformação em circulação, demandas locais e sinais de pauta antes de 'todo mundo está falando' |
| m05-a02 | Recorte Norte e governança: quem monitora, quem valida, quem decide | conceitual | 2:00 | 25 min | Recortar a escuta em Amazonas, Rondônia, Roraima, Acre e Amapá, com atenção a municípios do interior e a comunidades pouco visíveis no volume nacional<br>Definir quem monitora, quem valida, quem decide se vira pauta, com que prazo e com que registro |
| m05-a03 | Escuta no X com Grok — sempre conferindo o post original | ferramenta | 1:50 | 25 min | Usar busca e fios no X com apoio do Grok e da ferramenta de busca, quando disponíveis no plano<br>Conferir sempre o post original antes de qualquer alerta |
| m05-a04 | YouTube, comentários da casa e outras redes — com limite no que é privado | ferramenta | 2:00 | 25 min | Monitorar comentários, títulos em alta e lives de interesse regional no YouTube, além dos comentários das próprias matérias e programas<br>Incluir outras redes e grupos abertos de interesse público com respeito a termos de uso, à LGPD e ao que é espaço privado |
| m05-a05 | Alertas oficiais dialogam com a escuta — e não se misturam com ela | conceitual | 1:40 | 15 min | Incluir sinais oficiais e de serviço (órgãos, clima, saúde, trânsito) no radar da escuta<br>Evitar misturar alerta oficial e conversa em rede como se fossem a mesma evidência |
| m05-a06 | Dicionário de escuta e consultas com variações da mesma pauta | pratica | 2:00 | 40 min | Montar um dicionário com nomes, siglas, apelidos, topônimos, povos, rios, obras, eleições e desastres recorrentes da área de cobertura<br>Usar consultas booleanas e variações (queimada/fogo/focos, estiagem/rio baixo, PEC/proposta) |
| m05-a07 | Separe volume, alcance e confiabilidade — e defina o limiar do alerta | conceitual | 2:00 | 25 min | Separar volume, alcance aparente e confiabilidade da fonte<br>Definir o limiar: o que merece aviso imediato à chefia e o que entra no boletim do dia |
| m05-a08 | A tendência de São Paulo não pode apagar Porto Velho ou o interior | conceitual | 2:00 | 20 min | Distinguir tendência regional e tendência nacional<br>Evitar que o recorte de São Paulo ou do X global apague o que importa em Porto Velho, Boa Vista, Macapá, Rio Branco ou no interior do Amazonas |
| m05-a09 | Padrão coordenado, não amplificar o falso e o que não se coleta | conceitual | 2:00 | 25 min | Reconhecer padrão de publicação coordenada sem transformar suspeita em denúncia pronta<br>Não amplificar conteúdo falso ao rebater sem verificação, e não coletar dado sensível de particular, conversa claramente privada ou conteúdo de menor |
| m05-a10 | O boletim de escuta: fato, fonte, recorte, o conferido e a hipótese | pratica | 2:00 | 40 min | Redigir um boletim com fato observado, fonte, recorte, o que já foi conferido e o que ainda é hipótese<br>Integrar o boletim à reunião de pauta e à editoria de verificação |

<details><summary>m05-a01 — tópicos da ementa e prática</summary>

- Diferença entre monitoramento de menções à marca, escuta jornalística e pesquisa de opinião
- Função: detectar temas emergentes, desinformação em circulação, demandas locais e sinais de pauta antes que virem "todo mundo está falando"

Config: `aulas/m05-a01.yaml` · saída: `m05-agencia-de-escuta/m05-a01-escuta-nao-e-pesquisa-de-opiniao/`

</details>

<details><summary>m05-a02 — tópicos da ementa e prática</summary>

- Recorte territorial: Amazonas, Rondônia, Roraima, Acre e Amapá, com atenção a municípios do interior e a comunidades que pouco aparecem no volume nacional
- Governança: quem monitora, quem valida, quem decide se vira pauta, com que prazo e com que registro

Config: `aulas/m05-a02.yaml` · saída: `m05-agencia-de-escuta/m05-a02-recorte-territorial-e-governanca/`

</details>

<details><summary>m05-a03 — tópicos da ementa e prática</summary>

- X: busca e fios com apoio do Grok e da ferramenta de busca no X, quando disponível no plano, sempre conferindo o post original

Config: `aulas/m05-a03.yaml` · saída: `m05-agencia-de-escuta/m05-a03-escuta-no-x-com-grok/`

</details>

<details><summary>m05-a04 — tópicos da ementa e prática</summary>

- YouTube: comentários, títulos em alta e lives de interesse regional
- Comentários das próprias matérias e programas da Rede Amazônica (ligação com o módulo 4)
- Outras redes e grupos abertos de interesse público, com respeito a termos de uso, à LGPD e ao que é espaço privado

Config: `aulas/m05-a04.yaml` · saída: `m05-agencia-de-escuta/m05-a04-youtube-comentarios-e-outras-redes/`

</details>

<details><summary>m05-a05 — tópicos da ementa e prática</summary>

- Sinais oficiais e de serviço: alertas de órgãos, clima, saúde e trânsito, que dialogam com a escuta nas redes — sem misturar os dois como se fossem a mesma coisa

Config: `aulas/m05-a05.yaml` · saída: `m05-agencia-de-escuta/m05-a05-sinais-oficiais-versus-redes/`

</details>

<details><summary>m05-a06 — tópicos da ementa e prática</summary>

- Dicionário de escuta: nomes, siglas, apelidos, topônimos, povos, rios, obras, eleições e desastres recorrentes na área de cobertura
- Consultas booleanas e variações (queimada/fogo/focos, estiagem/rio baixo, PEC/proposta)

**Prática:** Rascunhar o dicionário de escuta de um tema da cobertura (10 a 15 termos e variações).

Config: `aulas/m05-a06.yaml` · saída: `m05-agencia-de-escuta/m05-a06-dicionario-e-consultas/`

</details>

<details><summary>m05-a07 — tópicos da ementa e prática</summary>

- Separar volume, alcance aparente e confiabilidade da fonte
- Alertas com limiar: o que merece aviso imediato à chefia e o que entra no boletim do dia

Config: `aulas/m05-a07.yaml` · saída: `m05-agencia-de-escuta/m05-a07-volume-alcance-e-alertas/`

</details>

<details><summary>m05-a08 — tópicos da ementa e prática</summary>

- Tendência regional versus tendência nacional: como evitar que o recorte de São Paulo ou do X global apague o que importa em Porto Velho, Boa Vista, Macapá, Rio Branco ou no interior do Amazonas

Config: `aulas/m05-a08.yaml` · saída: `m05-agencia-de-escuta/m05-a08-tendencia-regional-versus-nacional/`

</details>

<details><summary>m05-a09 — tópicos da ementa e prática</summary>

- Reconhecer padrão de publicação coordenada sem transformar suspeita em denúncia pronta
- Não amplificar conteúdo falso ao "rebater" sem verificação
- O que não se coleta: dado sensível de particular, conversa claramente privada, conteúdo de menor

Config: `aulas/m05-a09.yaml` · saída: `m05-agencia-de-escuta/m05-a09-desinformacao-e-o-que-nao-coletar/`

</details>

<details><summary>m05-a10 — tópicos da ementa e prática</summary>

- Boletim de escuta: fato observado, fonte, recorte, o que já foi conferido e o que ainda é hipótese
- Integração com a reunião de pauta e com a editoria de verificação

**Prática:** Escrever um boletim de uma página sobre um tema da cobertura, com o que foi conferido e o que ainda é hipótese.

Config: `aulas/m05-a10.yaml` · saída: `m05-agencia-de-escuta/m05-a10-boletim-de-escuta-e-pauta/`

</details>

## 6. Diários oficiais da área de cobertura e documentos públicos

*Mapear diários da União, dos estados da cobertura e dos municípios, extrair atos com método e transformar publicação em pauta auditável.*

10 aulas · 19.3 min de vídeo · 270 min de prática/estudo

| Aula | Título | Tipo | Vídeo | Prática | Objetivos |
|---|---|---|---|---|---|
| m06-a01 | O que é um diário oficial e o que costuma sair nele | conceitual | 1:50 | 15 min | Explicar o que é um diário oficial<br>Listar o que costuma sair nele: leis, decretos, nomeações, licitações, contratos, homologações e prestações de contas |
| m06-a02 | DOU e os diários dos cinco estados da cobertura | ferramenta | 2:00 | 30 min | Consultar o Diário Oficial da União no portal oficial<br>Localizar os diários oficiais de Amazonas, Rondônia, Roraima, Acre e Amapá nos portais oficiais de cada estado |
| m06-a03 | Diários municipais, PDFs difíceis e a LAI como complemento | ferramenta | 2:00 | 25 min | Enfrentar a dificuldade prática dos PDFs pouco acessíveis dos diários municipais (capitais e interior)<br>Usar a Lei de Acesso à Informação como complemento do que o diário não detalha |
| m06-a04 | Querido Diário: busca aberta — e a cobertura que falta conferir | ferramenta | 2:00 | 30 min | Usar o Querido Diário, da Open Knowledge Brasil, para buscar diários do Executivo municipal em formato aberto, inclusive pela API quando houver apoio de dados<br>Conferir a cobertura vigente na plataforma oficial antes de afirmar que não saiu no diário |
| m06-a05 | Busca avançada, API e o Diário do Clima na cobertura ambiental | ferramenta | 1:50 | 25 min | Fazer busca avançada com recorte por município, palavra-chave e período, e usar a API com apoio de dados, sem exigir programação de toda a turma<br>Relacionar o Diário do Clima ao monitoramento de atos ambientais relevantes para a cobertura amazônica |
| m06-a06 | OCR e busca em lotes de PDFs baixados dos portais oficiais | ferramenta | 1:50 | 30 min | Usar NotebookLM, Pinpoint e equivalentes para OCR, transcrição e busca em lotes de PDFs oficiais<br>Manter o PDF original como referência da conferência |
| m06-a07 | O que extrair de um ato — e a tabela padronizada da pauta | pratica | 2:00 | 35 min | Extrair tipo, órgão, data de publicação, vigência, nomes, cargos, CNPJ, valores, objeto, prazos e número do processo ou da licitação<br>Usar tabelas padronizadas para contratos, licitações, nomeações, exonerações, decretos e convênios |
| m06-a08 | Extenso versus número, retificação, OCR que falha e o acervo da pauta | conceitual | 2:00 | 25 min | Conferir valores por extenso versus numéricos, retificações posteriores e atos que revogam atos anteriores<br>Tratar falha de OCR e troca de dígitos pela IA como regra de risco: a conferência no PDF original é obrigatória, e o acervo leva pasta, nome, origem e data da coleta |
| m06-a09 | Sinais de reportagem no diário: emergência, aditivo, familiar, dispensa | conceitual | 2:00 | 25 min | Reconhecer sinais de reportagem: contratação emergencial recorrente, valor atípico, nomeação de familiar já noticiado, aditivo sucessivo, dispensa de licitação e convênio com OSC pouco conhecida<br>Tratar o sinal como pista, não como furo pronto |
| m06-a10 | Agenda pública, o que não é notícia e o registro para o colega retomar | pratica | 1:50 | 30 min | Localizar e processar em volume, com supervisão humana, agenda pública, discursos e legislações<br>Separar rotina administrativa do que é notícia e registrar a fonte de forma que outro colega retome a apuração |

<details><summary>m06-a01 — tópicos da ementa e prática</summary>

- O que é um diário oficial e o que costuma sair nele: leis, decretos, nomeações, licitações, contratos, homologações, prestações de contas

Config: `aulas/m06-a01.yaml` · saída: `m06-diarios-oficiais/m06-a01-o-que-e-um-diario-oficial/`

</details>

<details><summary>m06-a02 — tópicos da ementa e prática</summary>

- Diário Oficial da União (DOU) e a consulta no portal oficial
- Diários oficiais dos estados da área de cobertura (Amazonas, Rondônia, Roraima, Acre e Amapá), nos portais oficiais de cada estado

Config: `aulas/m06-a02.yaml` · saída: `m06-diarios-oficiais/m06-a02-dou-e-diarios-estaduais/`

</details>

<details><summary>m06-a03 — tópicos da ementa e prática</summary>

- Diários municipais: captais e interior; a dificuldade prática dos PDFs pouco acessíveis
- Lei de Acesso à Informação (LAI) como complemento do que o diário não detalha

Config: `aulas/m06-a03.yaml` · saída: `m06-diarios-oficiais/m06-a03-diarios-municipais-e-lai/`

</details>

<details><summary>m06-a04 — tópicos da ementa e prática</summary>

- O projeto Querido Diário, da Open Knowledge Brasil: diários do Executivo municipal em formato aberto, com plataforma de busca e API
- Cobertura variável: nem todo município está na base; conferir a cobertura vigente na plataforma oficial antes de afirmar que "não saiu no diário"

Config: `aulas/m06-a04.yaml` · saída: `m06-diarios-oficiais/m06-a04-querido-diario/`

</details>

<details><summary>m06-a05 — tópicos da ementa e prática</summary>

- Busca avançada, recorte por município, palavra-chave e período; uso da API por quem tiver apoio de dados, sem exigir programação de toda a turma
- Relação com o Diário do Clima e o monitoramento de atos ambientais — relevante para a cobertura amazônica

Config: `aulas/m06-a05.yaml` · saída: `m06-diarios-oficiais/m06-a05-busca-e-diario-do-clima/`

</details>

<details><summary>m06-a06 — tópicos da ementa e prática</summary>

- NotebookLM, Pinpoint e equivalentes para OCR, transcrição e busca em lotes de PDFs baixados dos portais oficiais

Config: `aulas/m06-a06.yaml` · saída: `m06-diarios-oficiais/m06-a06-ocr-com-notebooklm-e-pinpoint/`

</details>

<details><summary>m06-a07 — tópicos da ementa e prática</summary>

- O que extrair de um ato: tipo, órgão, data de publicação, vigência, nomes, cargos, CNPJ, valores, objeto, prazos e número do processo ou da licitação
- Tabelas padronizadas para contratos, licitações, nomeações, exonerações, decretos e convênios

**Prática:** Preencher uma tabela padronizada a partir de um ato real da área de cobertura.

Config: `aulas/m06-a07.yaml` · saída: `m06-diarios-oficiais/m06-a07-o-que-extrair-e-tabelas/`

</details>

<details><summary>m06-a08 — tópicos da ementa e prática</summary>

- Atenção a valores por extenso versus numéricos, retificações posteriores e atos que revogam atos anteriores
- OCR falha em diário antigo, scan ruim e carimbo; a IA também troca dígitos — a conferência no PDF original é obrigatória
- Organização do acervo da pauta: pastas, nome de arquivo, origem e data da coleta

Config: `aulas/m06-a08.yaml` · saída: `m06-diarios-oficiais/m06-a08-retificacoes-ocr-e-acervo/`

</details>

<details><summary>m06-a09 — tópicos da ementa e prática</summary>

- Sinais de reportagem: contratação emergencial recorrente, valor atípico, nomeação de familiar já noticiado, aditivo sucessivo, dispensa de licitação, convênio com OSC pouco conhecida

Config: `aulas/m06-a09.yaml` · saída: `m06-diarios-oficiais/m06-a09-sinais-de-reportagem/`

</details>

<details><summary>m06-a10 — tópicos da ementa e prática</summary>

- Agenda pública, discursos e legislações: onde encontrar e como processar em volume, com supervisão humana (lição também presente em formações da Abraji sobre dados públicos)
- O que é só rotina administrativa e não é notícia
- Como registrar a fonte de forma que outro colega retome a apuração

**Prática:** Registrar a fonte de um ato (URL, data da coleta, trecho e o que falta checar) para um colega retomar.

Config: `aulas/m06-a10.yaml` · saída: `m06-diarios-oficiais/m06-a10-agenda-rotina-e-registro/`

</details>

## 7. Inconsistências, cruzamentos e transparência

*Reconhecer o que conta como inconsistência, cruzar com bases oficiais e usar a IA só para apontar o que deve ser checado — nunca para confirmar irregularidade.*

8 aulas · 16.0 min de vídeo · 215 min de prática/estudo

| Aula | Título | Tipo | Vídeo | Prática | Objetivos |
|---|---|---|---|---|---|
| m07-a01 | Divergência entre atos: valor, data, prazo, objeto e quantidade | conceitual | 1:50 | 20 min | Identificar divergência de valores, datas, prazos, objetos ou quantidades entre um ato e outro<br>Tratar a divergência como inconsistência a checar, não ainda como furo |
| m07-a02 | CNPJ que não confere, empresa inexistente e sócios em comum | conceitual | 2:00 | 25 min | Reconhecer CNPJ que não confere com a razão social, empresa inexistente, CNAE incompatível ou sócios em comum em várias contratações<br>Levar cada um desses sinais à fonte oficial, não à conclusão pronta |
| m07-a03 | Grafias, CPF mascarado, cargo inexistente e o processo que não aparece | conceitual | 2:00 | 25 min | Detectar nome com grafias diferentes, CPF/CNPJ mascarado e cargo que não existe no organograma publicado<br>Checar o ato que cita um processo, um contrato ou uma lei que não aparece onde deveria |
| m07-a04 | Retificação silenciosa: o que mudou entre a versão original e a corrigida | conceitual | 1:50 | 25 min | Comparar a versão original e a retificada de um ato<br>Registrar o que mudou e o que a retificação silenciou |
| m07-a05 | Portal da Transparência e a situação cadastral na Receita | ferramenta | 2:00 | 30 min | Consultar o Portal da Transparência da União e os portais estaduais e municipais da área de cobertura<br>Conferir CNPJ e situação cadastral em fontes oficiais da Receita Federal |
| m07-a06 | Licitações, LAI quando uma ponta não fecha, e Tribunais de Contas | ferramenta | 2:10 | 30 min | Buscar licitações e contratos em portais de compras e em bases estaduais ou municipais, quando existirem e estiverem atualizados<br>Quando uma ponta não fecha, pedir acesso pela LAI, registrar o pedido e não preencher o buraco com a IA; usar Tribunais de Contas como fonte e contexto, sem transformar o acórdão em sentença jornalística automática |
| m07-a07 | A IA sugere pares a conferir — e não confirma irregularidade | conceitual | 2:00 | 20 min | Usar a IA para sugerir pares a conferir, montar a planilha e apontar divergências possíveis<br>Aplicar a proibição explícita: a IA não confirma irregularidade, superfaturamento ou parentesco; ela aponta o que deve ser checado |
| m07-a08 | Célula a célula, sinal versus prova, e o dossiê para o jurídico | pratica | 2:10 | 40 min | Conferir célula a célula os valores e identificadores usados na reportagem<br>Escrever o que se sabe, o que se perguntou ao poder público e o que ainda não se pode afirmar, organizando a apuração para o jurídico e para o direito de resposta |

<details><summary>m07-a01 — tópicos da ementa e prática</summary>

- Divergência de valores, datas, prazos, objetos ou quantidades entre um ato e outro

Config: `aulas/m07-a01.yaml` · saída: `m07-inconsistencias-e-cruzamentos/m07-a01-divergencias-entre-atos/`

</details>

<details><summary>m07-a02 — tópicos da ementa e prática</summary>

- CNPJ que não confere com a razão social, empresa inexistente, empresa com CNAE incompatível ou com sócios em comum em várias contratações

Config: `aulas/m07-a02.yaml` · saída: `m07-inconsistencias-e-cruzamentos/m07-a02-cnpj-e-empresas/`

</details>

<details><summary>m07-a03 — tópicos da ementa e prática</summary>

- Nome de pessoa com grafias diferentes, CPF/CNPJ mascarado, cargo que não existe no organograma publicado
- Ato que cita um processo, um contrato ou uma lei que não aparece onde deveria

Config: `aulas/m07-a03.yaml` · saída: `m07-inconsistencias-e-cruzamentos/m07-a03-nomes-cargos-e-atos-sem-processo/`

</details>

<details><summary>m07-a04 — tópicos da ementa e prática</summary>

- Retificação silenciosa: o que mudou entre a versão original e a corrigida

Config: `aulas/m07-a04.yaml` · saída: `m07-inconsistencias-e-cruzamentos/m07-a04-retificacao-silenciosa/`

</details>

<details><summary>m07-a05 — tópicos da ementa e prática</summary>

- Portal da Transparência da União e portais de transparência estaduais e municipais da área de cobertura
- Consulta de CNPJ e situação cadastral em fontes oficiais da Receita Federal

Config: `aulas/m07-a05.yaml` · saída: `m07-inconsistencias-e-cruzamentos/m07-a05-transparencia-e-receita/`

</details>

<details><summary>m07-a06 — tópicos da ementa e prática</summary>

- Licitações e contratos em portais de compras e em bases estaduais ou municipais, quando existirem e estiverem atualizados
- Diários, transparência e LAI: o que fazer quando uma ponta não fecha — pedir acesso, registrar o pedido e não preencher o buraco com a IA
- Tribunais de Contas e outros órgãos de controle como fonte e como contexto, sem transformar o acórdão em sentença jornalística automática

Config: `aulas/m07-a06.yaml` · saída: `m07-inconsistencias-e-cruzamentos/m07-a06-licitacoes-lai-e-tribunais/`

</details>

<details><summary>m07-a07 — tópicos da ementa e prática</summary>

- Uso da IA para sugerir pares a conferir, montar a planilha e apontar divergências possíveis
- Proibição explícita: a IA não "confirma" fraude, superfaturamento ou parentesco; ela aponta o que deve ser checado

Config: `aulas/m07-a07.yaml` · saída: `m07-inconsistencias-e-cruzamentos/m07-a07-ia-sugere-nao-confirma/`

</details>

<details><summary>m07-a08 — tópicos da ementa e prática</summary>

- Conferência célula a célula dos valores e identificadores usados na reportagem
- Red flags versus prova: como escrever o que se sabe, o que se perguntou ao poder público e o que ainda não se pode afirmar
- Organização da apuração para o jurídico e para o direito de resposta

**Prática:** Montar um dossiê curto de uma inconsistência: o que foi conferido, o que foi perguntado e o que ainda não se pode afirmar.

Config: `aulas/m07-a08.yaml` · saída: `m07-inconsistencias-e-cruzamentos/m07-a08-conferencia-red-flags-e-juridico/`

</details>

## 8. Jornalismo de dados e previsões com cuidado

*Usar dados para apurar, não para enfeitar; distinguir tendência, cenário e previsão; e publicar número só depois de origem, conta e responsável pela checagem.*

10 aulas · 19.3 min de vídeo · 240 min de prática/estudo

| Aula | Título | Tipo | Vídeo | Prática | Objetivos |
|---|---|---|---|---|---|
| m08-a01 | A pergunta jornalística vem antes da base de dados | conceitual | 1:40 | 15 min | Formular a pergunta jornalística antes de escolher a base<br>Recusar o dado que entra na reportagem só para enfeitar |
| m08-a02 | Tendência, sazonalidade e o ruído de um mês atípico | conceitual | 2:00 | 25 min | Distinguir tendência, sazonalidade e ruído de um mês atípico numa série temporal<br>Evitar transformar um ponto fora da curva em manchete de recorde sem contexto |
| m08-a03 | Bases recorrentes da cobertura amazônica — na fonte e na metodologia | ferramenta | 2:00 | 30 min | Localizar bases recorrentes: queimadas e focos de calor, nível dos rios, saúde, educação, orçamento, segurança e eleições<br>Ir sempre à fonte oficial e à documentação da metodologia |
| m08-a04 | Cruze na planilha antes do modelo — e visualize com eixo, recorte e exclusão | pratica | 2:00 | 35 min | Fazer o cruzamento simples em planilha antes de qualquer modelo sofisticado<br>Produzir visualização honesta: eixo, recorte, período e o que foi excluído |
| m08-a05 | Projeção, cenário, estimativa oficial — e previsão apresentada como fato | conceitual | 1:50 | 20 min | Diferenciar projeção exploratória, cenário, estimativa oficial e previsão apresentada como fato<br>Escolher a palavra certa antes de ir ao ar ou ao digital |
| m08-a06 | Eleições: pesquisa registrada, margem de erro e o que a IA não pode inventar | conceitual | 2:00 | 25 min | Usar apenas pesquisas registradas e informar a margem de erro<br>Recusar que a IA invente intenção de voto ou que a redação preveja resultado |
| m08-a07 | Clima, queimadas e orçamento: fonte especializada, não modelo caseiro | conceitual | 2:00 | 25 min | Usar dados e alertas de fontes especializadas em clima e queimadas, sem transformar exercício de modelo caseiro em forecast<br>Distinguir projetar ritmo de gasto de afirmar desvio no orçamento |
| m08-a08 | Incerteza, intervalo e hipótese: como falar sem superlativo indevido | conceitual | 1:50 | 20 min | Levar incerteza, intervalo e hipótese para o texto no ar e no digital<br>Evitar superlativo indevido quando o dado não comporta certeza |
| m08-a09 | Correlação não é causalidade — e o recorte muda a conclusão | conceitual | 2:00 | 20 min | Aplicar a regra: correlação não é causalidade<br>Mostrar como recorte geográfico e recorte temporal mudam a conclusão |
| m08-a10 | Atraso, buraco no interior, quando pedir ajuda e a revisão do número | conceitual | 2:00 | 25 min | Avaliar qualidade da base: atraso, sub-registro, mudança de metodologia e buracos em município do interior<br>Saber quando a equipe de dados precisa entrar e revisar, antes de publicar, origem, data, conta e responsável pela checagem |

<details><summary>m08-a01 — tópicos da ementa e prática</summary>

- Pergunta jornalística primeiro, base de dados depois

Config: `aulas/m08-a01.yaml` · saída: `m08-jornalismo-de-dados/m08-a01-pergunta-primeiro/`

</details>

<details><summary>m08-a02 — tópicos da ementa e prática</summary>

- Séries temporais: o que é tendência, o que é sazonalidade, o que é ruído de um mês atípico

Config: `aulas/m08-a02.yaml` · saída: `m08-jornalismo-de-dados/m08-a02-series-temporais/`

</details>

<details><summary>m08-a03 — tópicos da ementa e prática</summary>

- Bases recorrentes na cobertura amazônica: queimadas e focos de calor, nível dos rios, saúde, educação, orçamento, segurança e eleições — sempre na fonte oficial e na documentação da metodologia

Config: `aulas/m08-a03.yaml` · saída: `m08-jornalismo-de-dados/m08-a03-bases-da-cobertura-amazonica/`

</details>

<details><summary>m08-a04 — tópicos da ementa e prática</summary>

- Cruce simples em planilha antes de qualquer modelo sofisticado
- Visualização honesta: eixo, recorte, período e o que foi excluído

**Prática:** Cruzar duas colunas de uma base oficial da cobertura e anotar eixo, período e o que ficou de fora do gráfico.

Config: `aulas/m08-a04.yaml` · saída: `m08-jornalismo-de-dados/m08-a04-cruzamento-e-visualizacao/`

</details>

<details><summary>m08-a05 — tópicos da ementa e prática</summary>

- Diferença entre projeção exploratória, cenário, estimativa oficial e "previsão" apresentada como fato

Config: `aulas/m08-a05.yaml` · saída: `m08-jornalismo-de-dados/m08-a05-projecao-cenario-e-previsao/`

</details>

<details><summary>m08-a06 — tópicos da ementa e prática</summary>

- Eleições: pesquisas registradas, margem de erro, o que a IA não pode inventar em intenção de voto e o risco ético de "prever resultado"

Config: `aulas/m08-a06.yaml` · saída: `m08-jornalismo-de-dados/m08-a06-eleicoes-e-ia/`

</details>

<details><summary>m08-a07 — tópicos da ementa e prática</summary>

- Clima e queimadas: usar dados e alertas de fontes especializadas; não transformar um exercício de modelo caseiro em forecast no jornalismo
- Orçamento e execução: projetar ritmo de gasto é diferente de afirmar desvio

Config: `aulas/m08-a07.yaml` · saída: `m08-jornalismo-de-dados/m08-a07-clima-queimadas-e-orcamento/`

</details>

<details><summary>m08-a08 — tópicos da ementa e prática</summary>

- Incerteza, intervalo e hipótese: como falar no ar e no digital sem superlativo indevido

Config: `aulas/m08-a08.yaml` · saída: `m08-jornalismo-de-dados/m08-a08-incerteza-no-ar/`

</details>

<details><summary>m08-a09 — tópicos da ementa e prática</summary>

- Correlação não é causalidade
- Recorte geográfico e recorte temporal que mudam a conclusão

Config: `aulas/m08-a09.yaml` · saída: `m08-jornalismo-de-dados/m08-a09-correlacao-e-recorte/`

</details>

<details><summary>m08-a10 — tópicos da ementa e prática</summary>

- Qualidade da base: atraso, sub-registro, mudança de metodologia, buracos em município do interior
- Quando a equipe de dados precisa entrar e quando o jornalista para e pede ajuda
- Revisão antes de publicar número: origem, data, conta, responsável pela checagem

Config: `aulas/m08-a10.yaml` · saída: `m08-jornalismo-de-dados/m08-a10-qualidade-da-base-e-revisao/`

</details>

## 9. Verificação, checagem e mídia sintética

*Tratar tudo que a IA entregou como pista, checar na fonte primária e aplicar protocolo a imagem, áudio e vídeo sintéticos, inclusive em eleição e crise.*

8 aulas · 15.7 min de vídeo · 185 min de prática/estudo

| Aula | Título | Tipo | Vídeo | Prática | Objetivos |
|---|---|---|---|---|---|
| m09-a01 | Tudo que a IA entregou vira pista: confira na fonte primária | conceitual | 2:00 | 20 min | Tratar toda entrega da IA como pista a conferir na fonte primária<br>Exigir dupla checagem de números, nomes, cargos, datas, citações e links |
| m09-a02 | Quem gerou o texto não é a prova de que o texto está certo | conceitual | 1:50 | 20 min | Recusar usar a própria ferramenta que gerou o texto como única prova de que o texto está certo<br>Manter o fact-checking clássico: a IA não substitui o método de agências e mesas de verificação |
| m09-a03 | Fact Check Explorer e bases publicadas — com leitura da peça original | ferramenta | 1:50 | 25 min | Usar o Fact Check Explorer e bases de checagens publicadas como apoio<br>Ler a peça original, não só o recorte que a ferramenta devolve |
| m09-a04 | Imagem, áudio e vídeo sintéticos — e a edição enganosa tradicional | conceitual | 2:00 | 20 min | Diferenciar mídia sintética (imagem gerada, voz clonada, vídeo fabricado) e edição enganosa tradicional<br>Nomear cada tipo com precisão antes de qualquer protocolo |
| m09-a05 | Artefato não prova origem — e a ausência de artefato não prova autenticidade | ferramenta | 2:10 | 30 min | Usar sinais de alerta conhecendo os limites: artefato visual não prova origem, e ausência de artefato não prova autenticidade<br>Seguir a origem do arquivo, metadados quando existirem, busca reversa, contato com a fonte e contexto de publicação |
| m09-a06 | Sintético em campanha e o selo quando a própria redação gera a imagem | conceitual | 2:00 | 25 min | Equilibrar velocidade da redação e risco de amplificar o falso em campanha e em crises, inclusive no ciclo eleitoral<br>Aplicar a política de uso de imagem, áudio ou vídeo gerados pela própria redação: ilustração, engano e selo explícito |
| m09-a07 | De onde saiu, quem impulsionou e o que muda em ano eleitoral | conceitual | 2:00 | 25 min | Mapear a cadeia de circulação: de onde saiu, quem impulsionou e o que já foi desmentido<br>Ajustar o protocolo em ano eleitoral, conforme formações de referência no Brasil sobre integridade da informação |
| m09-a08 | Como corrigir no ar quando o erro teve origem na IA | conceitual | 1:50 | 20 min | Corrigir no ar e no digital quando a redação erra, inclusive se o erro teve origem em ferramenta de IA<br>Colaborar com mesas de verificação e com o jornalismo de dados da casa, quando houver |

<details><summary>m09-a01 — tópicos da ementa e prática</summary>

- Tudo que a IA entregou vira pista: conferir na fonte primária
- Números, nomes, cargos, datas, citações e links exigem dupla checagem

Config: `aulas/m09-a01.yaml` · saída: `m09-verificacao-e-midia-sintetica/m09-a01-ia-entrega-pista/`

</details>

<details><summary>m09-a02 — tópicos da ementa e prática</summary>

- Não usar a própria ferramenta que gerou o texto como única prova de que o texto está certo
- Fact-checking clássico continua valendo; a IA não substitui o método de agências e mesas de verificação

Config: `aulas/m09-a02.yaml` · saída: `m09-verificacao-e-midia-sintetica/m09-a02-nao-usar-a-propria-ferramenta-como-prova/`

</details>

<details><summary>m09-a03 — tópicos da ementa e prática</summary>

- Ferramentas de apoio (por exemplo Fact Check Explorer e bases de checagens publicadas), com leitura da peça original

Config: `aulas/m09-a03.yaml` · saída: `m09-verificacao-e-midia-sintetica/m09-a03-ferramentas-de-apoio-a-checagem/`

</details>

<details><summary>m09-a04 — tópicos da ementa e prática</summary>

- O que são deepfake, voz clonada, imagem gerada e edição enganosa "tradicional"

Config: `aulas/m09-a04.yaml` · saída: `m09-verificacao-e-midia-sintetica/m09-a04-o-que-e-midia-sintetica/`

</details>

<details><summary>m09-a05 — tópicos da ementa e prática</summary>

- Sinais de alerta e os limites desses sinais: artefato visual não prova origem, e ausência de artefato não prova autenticidade
- Procedimentos: origem do arquivo, metadados quando existirem, busca reversa, contato com a fonte, contexto de publicação

Config: `aulas/m09-a05.yaml` · saída: `m09-verificacao-e-midia-sintetica/m09-a05-sinais-limites-e-procedimentos/`

</details>

<details><summary>m09-a06 — tópicos da ementa e prática</summary>

- Conteúdo sintético em campanha e em crises (inclusive no ciclo eleitoral): velocidade da redação versus risco de amplificar o falso
- Política de uso de imagem, áudio ou vídeo gerados pela própria redação: quando é ilustração, quando é enganoso, quando precisa de selo explícito

Config: `aulas/m09-a06.yaml` · saída: `m09-verificacao-e-midia-sintetica/m09-a06-campanha-crise-e-politica-de-uso/`

</details>

<details><summary>m09-a07 — tópicos da ementa e prática</summary>

- Cadeia de circulação: de onde saiu, quem impulsionou, o que já foi desmentido
- Eleições e integridade da informação: o que muda no protocolo em ano eleitoral (formação de referência no Brasil trata especificamente desse cenário)

Config: `aulas/m09-a07.yaml` · saída: `m09-verificacao-e-midia-sintetica/m09-a07-cadeia-de-circulacao-e-eleicoes/`

</details>

<details><summary>m09-a08 — tópicos da ementa e prática</summary>

- Como corrigir no ar e no digital quando a redação erra, inclusive se o erro teve origem em ferramenta de IA
- Colaboração com mesas de verificação e com o jornalismo de dados da casa, quando houver

Config: `aulas/m09-a08.yaml` · saída: `m09-verificacao-e-midia-sintetica/m09-a08-correcao-e-colaboracao/`

</details>

## 10. Ética, LGPD, transparência e política editorial de IA

*Aplicar ética jornalística e LGPD ao uso de IA, declarar o uso com clareza e rascunhar uma política editorial aplicável à Rede Amazônica.*

10 aulas · 19.3 min de vídeo · 265 min de prática/estudo

| Aula | Título | Tipo | Vídeo | Prática | Objetivos |
|---|---|---|---|---|---|
| m10-a01 | Independência, precisão, honestidade com o público e dever de minimizar dano | conceitual | 1:50 | 15 min | Reafirmar independência, precisão, honestidade com o público e dever de minimizar dano no uso de IA<br>Usar esses princípios como teste de qualquer atalho que a ferramenta ofereça |
| m10-a02 | Teste de viés — e o juízo sobre suspeito, vítima e interesse público não se terceiriza | pratica | 2:00 | 30 min | Testar respostas da IA com os mesmos fatos em recortes diferentes (gênero, raça, território, afiliação política, povos indígenas)<br>Recusar terceirizar para o modelo o juízo sobre quem é suspeito, quem é vítima e o que é de interesse público |
| m10-a03 | Crédito, risco de plágio e o debate sobre treinar modelos com jornalismo | conceitual | 2:00 | 20 min | Citar com crédito e reconhecer o risco de plágio ou de reaproveitar texto de terceiro via modelo<br>Explicar o debate sobre uso de conteúdo jornalístico para treinar modelos e o que isso implica para o veículo e para a reportagem |
| m10-a04 | LGPD: base legal, minimização e dado de criança | conceitual | 2:00 | 25 min | Aplicar base legal, minimização e finalidade: comentários, documentos, planilhas e entrevistas não entram na ferramenta porque é mais fácil<br>Distinguir dado pessoal, dado sensível e dado de criança e adolescente |
| m10-a05 | Fonte em risco não vai à nuvem — leia os termos da conta que você usa | conceitual | 2:00 | 25 min | Aplicar a regra padrão: fonte em risco, off e material sob segredo de Justiça não se enviam à nuvem<br>Ler os termos vigentes de contas pessoais versus corporativas, histórico, treino do modelo e política de retenção do provedor |
| m10-a06 | Golpe com tema de IA, extensões duvidosas e chave compartilhada | conceitual | 1:50 | 20 min | Reconhecer golpe com tema de IA, extensões duvidosas e o risco de compartilhar chaves ou acessos<br>Adotar práticas mínimas de segurança digital na redação |
| m10-a07 | Quando declarar o uso de IA — em linguagem clara, em todos os meios | conceitual | 1:50 | 20 min | Decidir quando declarar o uso de IA (apoio à apuração, geração de imagem, síntese, tradução, transcrição) e quando a menção é dispensável<br>Fazer essa declaração em linguagem clara, sem jargão, em TV, rádio, site e redes |
| m10-a08 | O erro é da redação, não da IA — e como responder ao público | conceitual | 1:50 | 20 min | Recusar atribuir à IA a responsabilidade por um erro editorial<br>Responder pergunta de audiência ou de entrevistado sobre o uso de IA na reportagem com clareza |
| m10-a09 | Os componentes mínimos da política editorial de IA da casa | conceitual | 2:00 | 30 min | Listar componentes mínimos: usos permitidos e proibidos, checagem obrigatória, proteção de fontes, transparência, responsabilidade da chefia e canal de dúvida<br>Adaptar modelos de referência (Abraji, Poynter, JournalismAI) ao contexto da casa, definindo quem aprova exceções e como se registra o uso em pautas sensíveis |
| m10-a10 | A política envelhece — rascunhe a da Rede Amazônica | projeto | 2:00 | 60 min | Prever formação contínua porque a política envelhece quando a ferramenta muda<br>Rascunhar uma política aplicável à Rede Amazônica, para revisão da direção e da editoria-chefe |

<details><summary>m10-a01 — tópicos da ementa e prática</summary>

- Independência, precisão, honestidade com o público e dever de minimizar dano

Config: `aulas/m10-a01.yaml` · saída: `m10-etica-lgpd-politica/m10-a01-independencia-precisao-e-dano/`

</details>

<details><summary>m10-a02 — tópicos da ementa e prática</summary>

- Viés: como testar respostas da IA com os mesmos fatos em recortes diferentes (gênero, raça, território, afiliação política, povos indígenas)
- Não terceirizar para o modelo o juízo sobre quem é suspeito, quem é vítima e o que é de interesse público

**Prática:** Rodar o mesmo conjunto de fatos em dois recortes (por território ou por grupo) e anotar diferenças de tom ou de juízo.

Config: `aulas/m10-a02.yaml` · saída: `m10-etica-lgpd-politica/m10-a02-vies-e-juizo-nao-terceirizado/`

</details>

<details><summary>m10-a03 — tópicos da ementa e prática</summary>

- Crédito, citação e o risco de plágio ou de reaproveitar texto de terceiro via modelo
- Propriedade intelectual: o debate sobre uso de conteúdo jornalístico para treinar modelos e o que isso implica para o veículo e para a reportagem

Config: `aulas/m10-a03.yaml` · saída: `m10-etica-lgpd-politica/m10-a03-credito-plagio-e-propriedade/`

</details>

<details><summary>m10-a04 — tópicos da ementa e prática</summary>

- Base legal, minimização e finalidade: comentários, documentos, planilhas e entrevistas não entram na ferramenta "porque é mais fácil"
- Dados pessoais, dados sensíveis e dado de criança e adolescente

Config: `aulas/m10-a04.yaml` · saída: `m10-etica-lgpd-politica/m10-a04-lgpd-minimizacao-e-dados-sensiveis/`

</details>

<details><summary>m10-a05 — tópicos da ementa e prática</summary>

- Fonte em risco, off e material sob segredo de Justiça: regra padrão é não enviar à nuvem
- Contas pessoais versus contas corporativas, histórico, treino do modelo e política de retenção do provedor — ler os termos vigentes

Config: `aulas/m10-a05.yaml` · saída: `m10-etica-lgpd-politica/m10-a05-fonte-em-risco-e-contas/`

</details>

<details><summary>m10-a06 — tópicos da ementa e prática</summary>

- Segurança digital básica: phishing com tema de IA, extensões duvidosas e compartilhamento de chaves ou de acessos

Config: `aulas/m10-a06.yaml` · saída: `m10-etica-lgpd-politica/m10-a06-seguranca-digital-basica/`

</details>

<details><summary>m10-a07 — tópicos da ementa e prática</summary>

- Quando declarar o uso de IA (apoio à apuração, geração de imagem, síntese, tradução, transcrição) e quando a menção é dispensável
- Linguagem clara, sem jargão, em TV, rádio, site e redes

Config: `aulas/m10-a07.yaml` · saída: `m10-etica-lgpd-politica/m10-a07-quando-declarar-o-uso-de-ia/`

</details>

<details><summary>m10-a08 — tópicos da ementa e prática</summary>

- O que não se deve fazer: atribuir à IA a responsabilidade por um erro editorial
- Como responder pergunta de audiência ou de entrevistado sobre o uso de IA na reportagem

Config: `aulas/m10-a08.yaml` · saída: `m10-etica-lgpd-politica/m10-a08-responsabilidade-e-perguntas-do-publico/`

</details>

<details><summary>m10-a09 — tópicos da ementa e prática</summary>

- Componentes mínimos: usos permitidos, usos proibidos, checagem obrigatória, proteção de fontes, transparência, responsabilidade da chefia e canal de dúvida
- Modelos e guias de referência (por exemplo formações da Abraji, do Poynter e do JournalismAI) para adaptar, não para copiar sem contexto
- Quem aprova exceções e como se registra o uso em pautas sensíveis

Config: `aulas/m10-a09.yaml` · saída: `m10-etica-lgpd-politica/m10-a09-componentes-da-politica/`

</details>

<details><summary>m10-a10 — tópicos da ementa e prática</summary>

- Formação contínua: a política envelhece quando a ferramenta muda
- Exercício: rascunho de política aplicável à Rede Amazônica, para revisão da direção e da editoria-chefe

**Prática:** Entregar um rascunho de política de IA da casa (usos permitidos e proibidos, checagem, fontes, transparência e canal de dúvida) para revisão da chefia.

Config: `aulas/m10-a10.yaml` · saída: `m10-etica-lgpd-politica/m10-a10-formacao-continua-e-rascunho/`

</details>

## 11. Automação, agentes e fluxo da redação

*Mapear o fluxo da casa, automatizar primeiro o que é alto volume e baixo risco, e manter trava humana antes de publicar ou de acusar.*

6 aulas · 11.8 min de vídeo · 155 min de prática/estudo

| Aula | Título | Tipo | Vídeo | Prática | Objetivos |
|---|---|---|---|---|---|
| m11-a01 | Mapeie o fluxo atual: onde a IA reduz trabalho e onde ela cria risco | conceitual | 2:00 | 25 min | Mapear o fluxo atual: pauta, apuração, edição, publicação, escuta e correção<br>Marcar onde a IA reduz trabalho repetitivo e onde ela cria retrabalho ou risco |
| m11-a02 | GPTs, Gems e Projetos do Claude com instruções, acervo e teste | ferramenta | 2:00 | 30 min | Configurar assistentes personalizados da redação (GPTs, Gems, Projetos do Claude e equivalentes) com instruções, acervo e formato de saída<br>Testar o assistente antes de liberar para o plantão |
| m11-a03 | Encadeie etapas — e trave o humano antes de publicar ou de acusar | conceitual | 2:00 | 25 min | Descrever agentes e encadeamento de etapas (triagem, extração, planilha, alerta) com trava humana antes de publicar ou de acusar<br>Automatizar primeiro tarefas de alto volume e baixo risco (transcrição, recorte de diário, boletim de escuta), não a reportagem investigativa completa |
| m11-a04 | Quem olha o alerta no fim de semana — e como medir erro evitado e erro introduzido | conceitual | 2:00 | 25 min | Definir filas, plantão e fim de semana: quem olha o alerta e com que prazo<br>Acompanhar indicadores simples: tempo economizado, erros evitados, erros introduzidos e pautas geradas com qualidade |
| m11-a05 | Documente o fluxo para um colega novo repetir o método | pratica | 1:50 | 30 min | Escrever a documentação do fluxo de forma que um colega novo consiga repetir o método<br>Incluir ferramentas, travas humanas e o que fazer quando o alerta falha |
| m11-a06 | Ser citado com crédito — sem deixar o SEO de IA guiar a pauta | conceitual | 2:00 | 20 min | Identificar o que a redação pode fazer para o jornalismo original ser citado com crédito em mecanismos de resposta com IA (GEO), sem deixar que essa otimização guide a pauta<br>Fixar o limite ético: o que nunca sai no automático |

<details><summary>m11-a01 — tópicos da ementa e prática</summary>

- Mapa do fluxo atual: pauta, apuração, edição, publicação, escuta e correção
- Onde a IA reduz trabalho repetitivo e onde ela cria retrabalho ou risco

Config: `aulas/m11-a01.yaml` · saída: `m11-automacao-e-fluxo/m11-a01-mapa-do-fluxo-atual/`

</details>

<details><summary>m11-a02 — tópicos da ementa e prática</summary>

- Assistentes personalizados da redação (GPTs, Gems, Projetos do Claude e equivalentes): instruções, acervo, formato de saída e teste

Config: `aulas/m11-a02.yaml` · saída: `m11-automacao-e-fluxo/m11-a02-assistentes-personalizados/`

</details>

<details><summary>m11-a03 — tópicos da ementa e prática</summary>

- Agentes e encadeamento de etapas (triagem → extração → planilha → alerta), sempre com trava humana antes de publicar ou de acusar
- O que automatizar primeiro: tarefas de alto volume e baixo risco (transcrição, recorte de diário, boletim de escuta), não a reportagem investigativa completa

Config: `aulas/m11-a03.yaml` · saída: `m11-automacao-e-fluxo/m11-a03-agentes-com-trava-humana/`

</details>

<details><summary>m11-a04 — tópicos da ementa e prática</summary>

- Filas, plantão e fim de semana: quem olha o alerta e com que prazo
- Indicadores simples: tempo economizado, erros evitados, erros introduzidos, pautas geradas com qualidade

Config: `aulas/m11-a04.yaml` · saída: `m11-automacao-e-fluxo/m11-a04-plantao-e-indicadores/`

</details>

<details><summary>m11-a05 — tópicos da ementa e prática</summary>

- Documentação do fluxo para um colega novo conseguir repetir o método

**Prática:** Documentar em uma página o fluxo de um alerta (quem olha, prazo, trava e o que registrar).

Config: `aulas/m11-a05.yaml` · saída: `m11-automacao-e-fluxo/m11-a05-documentacao-do-fluxo/`

</details>

<details><summary>m11-a06 — tópicos da ementa e prática</summary>

- SEO e visibilidade em mecanismos de resposta com IA (GEO): o que a redação pode fazer para o jornalismo original ser citado com crédito, sem deixar que essa otimização guide a pauta
- Limite ético da automação de publicação: o que nunca sai no automático

Config: `aulas/m11-a06.yaml` · saída: `m11-automacao-e-fluxo/m11-a06-geo-e-limite-da-publicacao-automatica/`

</details>

## 12. Pipelines em Python: o LLM só quando for necessário

*Desenhar pipelines reexecutáveis em que etapas determinísticas ficam no código e o modelo entra só onde há linguagem ou julgamento, com registro de custo e trava humana.*

12 aulas · 25.0 min de vídeo · 395 min de prática/estudo

| Aula | Título | Tipo | Vídeo | Prática | Objetivos |
|---|---|---|---|---|---|
| m12-a01 | Pipeline é etapa reexecutável — o modelo entra só na linguagem | conceitual | 2:00 | 20 min | Definir pipeline como sequência de etapas reexecutáveis, com entrada, saída e regra claras — não um papo longo num chat<br>Separar etapas determinísticas em código (coleta, limpeza, recorte, contagem, cruzamento, validação) do ponto em que o modelo entra só para linguagem ou julgamento e sai de novo para o código gravar o resultado |
| m12-a02 | Tudo no chat versus pipeline: custo, erro, repetição e auditoria | conceitual | 2:00 | 25 min | Comparar, na mesma pauta, o caminho tudo no chat e o caminho do pipeline em tokens, tempo, erro, capacidade de repetir e de auditar<br>Usar cache e reexecução por etapa: se a coleta não mudou, não se paga de novo a transcrição nem o roteiro |
| m12-a03 | Configuração em arquivo, registro de tokens e a trava antes de ir ao ar | conceitual | 2:00 | 25 min | Colocar vozes, pastas, limites e fontes num arquivo de configuração (YAML ou equivalente), sem embutir decisão no meio do código ou do prompt<br>Registrar tokens e custo por etapa e no total, com meta de reduzir o que o modelo lê, e manter trava humana quando o resultado vira pauta, número publicado, acusação ou conteúdo no ar |
| m12-a04 | Python para jornalistas: planilha, texto e pasta, começando no notebook | ferramenta | 2:00 | 40 min | Explicar por que o Python aparece tanto em redação de dados: lê planilha, texto e pasta de arquivos com pouca cerimônia<br>Começar num notebook no navegador (Jupyter ou Google Colab), para ver o resultado linha a linha |
| m12-a05 | Peça o código à IA, rode, leia o erro e confira a amostra | codigo | 2:20 | 60 min | Pedir o código à IA com o problema, o formato da entrada e o formato da saída, recusando código mágico que a pessoa não consegue explicar<br>Rodar, ler a mensagem de erro, mandar o erro de volta e conferir o resultado numa amostra — o jornalista permanece responsável pelo que o script faz |
| m12-a06 | O que não colar no notebook da nuvem — e quando pedir ajuda a quem já trabalha com dados | conceitual | 1:50 | 20 min | Não colar no chat ou no notebook na nuvem fonte em risco, dado pessoal desnecessário, chave de API, senha ou material sob sigilo<br>Saber quando pedir ajuda a quem já trabalha com dados na casa, em vez de insistir sozinho |
| m12-a07 | O pipeline interno de aulas como método — e a queda estimada de tokens | conceitual | 2:10 | 25 min | Descrever o pipeline interno de criação de aulas (aula-ra) como exemplo de método, não como produto a copiar inteiro: cada etapa tem script, cache e ponto de parada<br>Relatar a cadeia típica (legendas, roteiro só com trechos relevantes, narração, crédito, HTML, vídeo 16:9 e 9:16) e a estimativa de que, no teste das aulas de amostra, os tokens caíram cerca de 54 por cento ao enviar só trechos relevantes e reaproveitar o cache — número estimado por tokenizer, não medido numa API de provedor; e a reexecução seletiva (só a voz ou só o vídeo) quando a entrada não mudou |
| m12-a08 | Três pipelines da redação: diários, comentários e escuta | pratica | 2:10 | 50 min | Traduzir o método para diários oficiais (baixar, extrair, filtrar, modelo só para classificar ou resumir o que restou), comentários (contar no código; modelo só na amostra ou no boletim) e escuta (busca e alerta no código; o modelo redige o resumo do que já foi filtrado, nunca inventa que algo está em alta)<br>Desenhar no papel, depois num YAML, as etapas de um desses três pipelines, marcando onde o modelo entra, onde não entra e onde a pessoa revisa |
| m12-a09 | FFmpeg em lote: corte, legenda, 16:9 e o vertical em FIT | ferramenta | 2:10 | 35 min | Listar o que o FFmpeg faz bem em lote: cortar, juntar, redimensionar, gravar legenda na imagem e gerar versão 16:9 e 9:16<br>Explicar o enquadramento FIT no vertical (quadro inteiro centralizado sobre fundo desfocado), para não cortar crédito nem informação |
| m12-a10 | Legenda, narração sintética, crédito na imagem e o que não se automatiza | conceitual | 2:10 | 25 min | Revisar nomes, toponímia amazônica e termos técnicos em legenda automática (Whisper ou equivalente) antes de publicar, e decidir quando a narração sintética exige selo, autorização e decisão editorial<br>Gravar crédito de trechos de terceiros na própria imagem (canal, título, link e tempo), respeitar o limite jurídico de obra alheia, e não automatizar escolha do furo, montagem que altera o sentido ou publicação no ar sem revisão — vídeo gerado ou narrado por IA segue a política de transparência e de rotulagem da casa (módulo 9) |
| m12-a11 | Skill é pacote reutilizável — e as regras do que o agente sempre faz ou nunca faz | conceitual | 2:00 | 25 min | Definir skill como pacote reutilizável de instruções (e, às vezes, de scripts) que um agente segue numa tarefa, distinto de um truque de prompt solto no chat<br>Descrever, conforme a documentação oficial da Anthropic, Agent Skills como pasta com SKILL.md (metadados em YAML e instruções) e as regras de projeto em ambientes de agentes (por exemplo regras do Cursor), conforme a documentação vigente |
| m12-a12 | Buscar no GitHub com ficha de risco — e versionar as skills da casa | pratica | 2:10 | 45 min | Buscar skills e repositórios no GitHub olhando licença, data da última atualização, questões abertas, estrelas só como sinal fraco, README e testes visíveis, sem rodar código baixado sem ler e sem colar chave nem dado da redação em repositório alheio<br>Reutilizar, adaptar e versionar as skills da própria casa, com registro de mudança; avaliar um repositório público com uma ficha e rascunhar o SKILL.md de uma tarefa da editoria |

<details><summary>m12-a01 — tópicos da ementa e prática</summary>

- Pipeline, neste curso, é uma sequência de etapas reexecutáveis, com entrada, saída e regra claras — não um papo longo num chat
- Etapas determinísticas em código, sem LLM: coleta, limpeza, recorte de data, contagem, frequência, expressões regulares, cruzamento de planilhas e CNPJ, validação de formato
- O modelo entra só onde a tarefa é linguagem ou julgamento (classificar tema, redigir boletim, resumir um ato, sugerir ângulo) e sai de novo para o código gravar o resultado

Config: `aulas/m12-a01.yaml` · saída: `m12-pipelines-em-python/m12-a01-o-que-e-um-pipeline/`

</details>

<details><summary>m12-a02 — tópicos da ementa e prática</summary>

- Comparar, na mesma pauta, o caminho "tudo no chat" e o caminho do pipeline: custo em tokens, tempo, erro, capacidade de repetir e de auditar
- Cache e reexecução por etapa: se a coleta não mudou, não se paga de novo a transcrição nem o roteiro

Config: `aulas/m12-a02.yaml` · saída: `m12-pipelines-em-python/m12-a02-chat-versus-pipeline/`

</details>

<details><summary>m12-a03 — tópicos da ementa e prática</summary>

- Configuração em arquivo (YAML ou equivalente): vozes, pastas, limites, fontes — para não embutir decisão no meio do código ou do prompt
- Registro de tokens e de custo por etapa e no total; meta de reduzir o que o modelo lê, não só de "escrever um prompt melhor"
- Trava humana nos pontos em que o resultado vira pauta, número publicado, acusação ou conteúdo no ar

Config: `aulas/m12-a03.yaml` · saída: `m12-pipelines-em-python/m12-a03-config-custo-e-trava-humana/`

</details>

<details><summary>m12-a04 — tópicos da ementa e prática</summary>

- Por que Python aparece tanto em redação de dados: lê planilha, texto e pasta de arquivos com pouca cerimônia
- Onde rodar no começo: notebook no navegador (Jupyter ou Google Colab), para ver o resultado linha a linha

**Prática:** Abrir um notebook e ler uma planilha pequena, conferindo as primeiras linhas.

Config: `aulas/m12-a04.yaml` · saída: `m12-pipelines-em-python/m12-a04-python-para-jornalistas/`

</details>

<details><summary>m12-a05 — tópicos da ementa e prática</summary>

- Pedir o código à IA com o problema, o formato da entrada e o formato da saída; recusar "código mágico" que a pessoa não consegue explicar
- Rodar, ler a mensagem de erro, mandar o erro de volta, conferir o resultado numa amostra — o jornalista permanece responsável pelo que o script faz

**Prática:** Pedir um script que leia um CSV, rode, corrija o erro e confira três linhas na mão.

Config: `aulas/m12-a05.yaml` · saída: `m12-pipelines-em-python/m12-a05-pedir-rodar-e-conferir-codigo/`

</details>

<details><summary>m12-a06 — tópicos da ementa e prática</summary>

- O que não colar no chat ou no notebook na nuvem: fonte em risco, dado pessoal desnecessário, chave de API, senha ou material sob sigilo
- Quando pedir ajuda a quem já trabalha com dados na casa, em vez de insistir sozinho

Config: `aulas/m12-a06.yaml` · saída: `m12-pipelines-em-python/m12-a06-o-que-nao-colar-e-quando-pedir-ajuda/`

</details>

<details><summary>m12-a07 — tópicos da ementa e prática</summary>

- O pipeline interno de criação de aulas (aula-ra) como exemplo de método, não como produto a copiar inteiro: cada etapa tem script, cache e ponto de parada
- Cadeia típica: baixar só as legendas de um vídeo do YouTube; o modelo escreve o roteiro a partir de trechos relevantes (não da transcrição inteira); narração com síntese de voz (edge-tts); recorte de trechos com crédito na imagem; página HTML com animação; renderização do vídeo com HyperFrames e ffmpeg, em 16:9 e 9:16
- No teste das aulas de amostra de um curso interno, a estimativa de tokens caiu cerca de 54% ao enviar ao modelo só os trechos relevantes e ao reaproveitar o cache; o número foi estimado por tokenizer, não medido numa API de provedor
- Reexecução seletiva: refazer só a voz ou só o vídeo, sem gastar de novo o roteiro, quando a entrada não mudou

Config: `aulas/m12-a07.yaml` · saída: `m12-pipelines-em-python/m12-a07-caso-aula-ra-e-economia-de-tokens/`

</details>

<details><summary>m12-a08 — tópicos da ementa e prática</summary>

- Traduzir o mesmo método para a redação: pipeline de diários oficiais (baixar, extrair texto, filtrar por palavra e município, LLM só para classificar ou resumir o que restou, planilha para checagem)
- Pipeline de comentários: coletar, limpar, contar palavras e temas no código; LLM só para classificar uma amostra ou redigir o boletim
- Pipeline de escuta: busca e alerta no código; o modelo ajuda a redigir o resumo do que já foi filtrado, nunca a "inventar" que algo está em alta
- Exercício: desenhar no papel (depois num YAML) as etapas de um desses três pipelines, marcando onde o LLM entra, onde não entra e onde a pessoa revisa

**Prática:** Desenhar no papel e depois num YAML as etapas de um pipeline (diários, comentários ou escuta), com o ponto do modelo e o ponto de revisão humana.

Config: `aulas/m12-a08.yaml` · saída: `m12-pipelines-em-python/m12-a08-pipelines-da-redacao/`

</details>

<details><summary>m12-a09 — tópicos da ementa e prática</summary>

- O que o ffmpeg faz bem em lote: cortar, juntar, redimensionar, gravar legenda na imagem, gerar versão 16:9 e versão 9:16
- No vertical 9:16, um recorte a partir de um original 16:9 pode usar o enquadramento FIT (o quadro inteiro centralizado sobre fundo desfocado), para não cortar crédito nem informação

Config: `aulas/m12-a09.yaml` · saída: `m12-pipelines-em-python/m12-a09-ffmpeg-e-formatos/`

</details>

<details><summary>m12-a10 — tópicos da ementa e prática</summary>

- Legenda automática com transcrição (por exemplo Whisper ou equivalente): sempre revisar nomes, toponímia amazônica e termos técnicos antes de publicar
- Narração sintética: quando ajuda (acessibilidade, aula interna, versão rápida) e quando exige selo, autorização e decisão editorial
- Crédito de trechos de terceiros na própria imagem (canal, título, link e tempo), em material interno ou publicado, e o limite jurídico de usar obra alheia
- O que não se automatiza: escolha do furo, montagem que altera o sentido, publicação no ar sem revisão
- Ligação com o módulo 9: vídeo gerado ou narrado por IA segue a política de transparência e de rotulagem da casa

Config: `aulas/m12-a10.yaml` · saída: `m12-pipelines-em-python/m12-a10-legendas-narracao-credito-e-limite/`

</details>

<details><summary>m12-a11 — tópicos da ementa e prática</summary>

- Skill, neste sentido, é um pacote reutilizável de instruções (e, às vezes, de scripts) que um agente segue numa tarefa — distinto de um "truque de prompt" solto no chat
- Exemplo verificável: a documentação oficial da Anthropic descreve Agent Skills como uma pasta com um arquivo SKILL.md (metadados em YAML, com nome e descrição, e instruções em Markdown), que o agente carrega quando a tarefa combina com a descrição
- Regras de projeto em ambientes de agentes (por exemplo regras do Cursor ou arquivos equivalentes, conforme a documentação vigente da ferramenta): o que a casa quer que o assistente sempre faça ou nunca faça

Config: `aulas/m12-a11.yaml` · saída: `m12-pipelines-em-python/m12-a11-skills-e-regras-de-projeto/`

</details>

<details><summary>m12-a12 — tópicos da ementa e prática</summary>

- Como buscar skills e repositórios no GitHub: licença, data da última atualização, questões abertas, número de estrelas como sinal fraco (não como garantia), README e testes visíveis
- Segurança: não rodar código baixado sem ler; não colar chave nem dado da redação em repositório alheio; desconfiar de pedido de permissão ampla ou de instalação opaca
- Reutilizar, adaptar e versionar as skills da própria casa (o que deu certo nos módulos de diário, de escuta, de comentários ou de aula), com registro de mudança
- Exercício: avaliar um repositório público com uma ficha (licença, manutenção, risco, o que reaproveitar) e rascunhar o SKILL.md de uma tarefa da editoria

**Prática:** Preencher uma ficha (licença, manutenção, risco, o que reaproveitar) de um repositório público e rascunhar o SKILL.md de uma tarefa da editoria.

Config: `aulas/m12-a12.yaml` · saída: `m12-pipelines-em-python/m12-a12-buscar-no-github-e-seguranca/`

</details>

## 13. Projeto final — aplicação na Rede Amazônica

*Aplicar o método numa pauta ou num território real da cobertura, com produto mínimo conferido, registro de checagem e proposta de continuidade.*

8 aulas · 16.2 min de vídeo · 475 min de prática/estudo

| Aula | Título | Tipo | Vídeo | Prática | Objetivos |
|---|---|---|---|---|---|
| m13-a01 | Escolha o caminho — de preferência ligado a uma pauta real | projeto | 1:50 | 30 min | Escolher, individualmente ou em dupla, um dos caminhos do projeto, de preferência ligado a uma pauta ou a um território real da cobertura<br>Registrar a escolha e o recorte territorial ou temático |
| m13-a02 | Caminho A: agência de escuta de um tema da cobertura | projeto | 2:00 | 60 min | Desenhar dicionário regional, canais, boletim e protocolo de alerta para um tema (queimadas, saúde, eleições ou obra pública)<br>Deixar explícito o que é fato observado e o que ainda é hipótese |
| m13-a03 | Caminho B: monitoramento de diários oficiais com lista de inconsistências | projeto | 2:00 | 60 min | Recortar um estado ou município, extrair atos, cruzar com transparência e montar a lista de inconsistências a checar<br>Manter cada item como pista, não como acusação |
| m13-a04 | Caminho C: comentários e audiência de uma série ou de um programa | projeto | 2:00 | 60 min | Definir método de coleta, temas, riscos e recomendações editoriais a partir dos comentários de uma série ou de um programa<br>Evitar transformar volume em 'o público acha que' |
| m13-a05 | Caminho D: pipeline reexecutável, com o modelo só onde a linguagem entra | projeto | 2:10 | 70 min | Desenhar um pipeline reexecutável (diários, comentários, escuta ou recorte de vídeo) com etapas em código, modelo só onde a linguagem for necessária, registro de custo e ponto de revisão humana<br>Marcar com clareza onde o modelo entra, onde não entra e quem revisa |
| m13-a06 | Documento de partida: problema, fontes, riscos e o que não será automatizado | projeto | 2:00 | 45 min | Redigir o documento de partida com problema editorial, público afetado, fontes, ferramentas, riscos (ética, LGPD, alucinação) e o que não será automatizado<br>Usar esse documento como contrato da execução supervisionada |
| m13-a07 | Execute com amostra conferida, produto mínimo e plano de continuidade | projeto | 2:10 | 90 min | Montar o fluxo com as ferramentas escolhidas (entre Claude, Gemini, Grok, ChatGPT e o estojo complementar)<br>Conferir uma amostra com registro do que a IA acertou e do que errou; entregar um produto mínimo (boletim, planilha auditável, protocolo ou protótipo de alerta) e o plano de continuidade (quem opera, com que frequência, com que revisão) |
| m13-a08 | Apresente à editoria: problema, método, achado, limite e pedido de decisão | projeto | 2:00 | 60 min | Fazer uma apresentação curta à editoria com problema, método, achado, limite e pedido de decisão<br>Atender aos critérios de relevância jornalística, rigor da checagem, cuidado ético e de dados, clareza do método e viabilidade na rotina, incorporando lições à política de IA e à biblioteca de prompts, e entregando o produto, o registro de checagem e a proposta de política ou de protocolo |

<details><summary>m13-a01 — tópicos da ementa e prática</summary>

- O participante (ou a dupla) escolhe um de três caminhos, preferencialmente ligado a uma pauta ou a um território real da cobertura:

**Prática:** Registrar o caminho escolhido, o território ou a pauta e o porquê da escolha. (A ementa fala em três caminhos e em seguida lista quatro, A a D: use os quatro descritos.)

Config: `aulas/m13-a01.yaml` · saída: `m13-projeto-final/m13-a01-escolher-o-caminho/`

</details>

<details><summary>m13-a02 — tópicos da ementa e prática</summary>

- Caminho A — Agência de escuta: dicionário regional, canais, boletim e protocolo de alerta para um tema (por exemplo queimadas, saúde, eleições ou obra pública)

**Prática:** Entregar o dicionário, a lista de canais, o modelo de boletim e o protocolo de alerta do tema escolhido.

Config: `aulas/m13-a02.yaml` · saída: `m13-projeto-final/m13-a02-caminho-agencia-de-escuta/`

</details>

<details><summary>m13-a03 — tópicos da ementa e prática</summary>

- Caminho B — Monitoramento de diários oficiais: recorte de um estado ou município, extração, cruzamento com transparência e lista de inconsistências a checar

**Prática:** Entregar o recorte, a tabela de extração e a lista de inconsistências a checar, com fonte de cada linha.

Config: `aulas/m13-a03.yaml` · saída: `m13-projeto-final/m13-a03-caminho-diarios-oficiais/`

</details>

<details><summary>m13-a04 — tópicos da ementa e prática</summary>

- Caminho C — Comentários e audiência de uma série ou de um programa: método de coleta, temas, riscos e recomendações editoriais

**Prática:** Entregar método, temas encontrados, riscos e recomendações editoriais, com os limites da amostra.

Config: `aulas/m13-a04.yaml` · saída: `m13-projeto-final/m13-a04-caminho-comentarios/`

</details>

<details><summary>m13-a05 — tópicos da ementa e prática</summary>

- Caminho D — Pipeline reexecutável: diários, comentários, escuta ou recorte de vídeo, com etapas em código, LLM só onde a linguagem for necessária, registro de custo e ponto de revisão humana

**Prática:** Entregar o desenho das etapas (papel e YAML), o registro de custo previsto e o ponto de revisão humana.

Config: `aulas/m13-a05.yaml` · saída: `m13-projeto-final/m13-a05-caminho-pipeline/`

</details>

<details><summary>m13-a06 — tópicos da ementa e prática</summary>

- Documento de partida: problema editorial, público afetado, fontes, ferramentas, riscos (ética, LGPD, alucinação) e o que não será automatizado

**Prática:** Entregar o documento de partida do projeto escolhido.

Config: `aulas/m13-a06.yaml` · saída: `m13-projeto-final/m13-a06-documento-de-partida/`

</details>

<details><summary>m13-a07 — tópicos da ementa e prática</summary>

- Montagem do fluxo com as ferramentas escolhidas (entre Claude, Gemini, Grok, ChatGPT e o estojo complementar)
- Amostra conferida por humano, com registro do que a IA acertou e do que errou
- Produto mínimo: boletim, planilha auditável, protocolo ou protótipo de alerta — não um discurso sobre IA
- Plano de continuidade na redação: quem opera, com que frequência, com que revisão

**Prática:** Entregar o produto mínimo, o registro da amostra conferida e o plano de continuidade na redação.

Config: `aulas/m13-a07.yaml` · saída: `m13-projeto-final/m13-a07-execucao-supervisionada/`

</details>

<details><summary>m13-a08 — tópicos da ementa e prática</summary>

- Apresentação curta à editoria: problema, método, achado, limite e pedido de decisão
- Critérios: relevância jornalística, rigor da checagem, cuidado ético e de dados, clareza do método e viabilidade na rotina
- Lições a incorporar na política de IA e na biblioteca de prompts da casa
- Projeto final: entrega do produto, do registro de checagem e da proposta de política ou de protocolo associada

**Prática:** Apresentar à editoria e entregar o pacote final: produto, registro de checagem e proposta de política ou de protocolo associada.

Config: `aulas/m13-a08.yaml` · saída: `m13-projeto-final/m13-a08-apresentacao-e-avaliacao/`

</details>
