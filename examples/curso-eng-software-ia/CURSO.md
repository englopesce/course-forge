# Engenharia de Software em IA Aplicada

Curso prático para programadores: do funcionamento dos LLMs a agentes, MCP, DevOps, arquitetura, fine-tuning, governança e carreira, com um projeto integrador (Micro-SaaS).

- **Público:** Programadores (back-end, front-end, full-stack) que já trabalham com JavaScript/TypeScript ou Python
- **Nível:** intermediário — sabe programar, usar git, npm e APIs HTTP; pouca ou nenhuma experiência com IA
- **Tom:** técnico e direto, de dev para dev; mostra o código real e o porquê de cada decisão
- **Ementa:** `/workspace/aula-ra/ementa-eng-software-ia.txt` (367 itens; 367 cobertos pelas aulas)
- **Tamanho:** 12 módulos, 85 aulas, 174 min de vídeo + 72.5 h de prática/estudo estimadas

**Pré-requisitos do curso:** JavaScript/TypeScript ou Python; git e terminal; APIs HTTP/JSON

## 1. Fundamentos de IA e LLMs para Programadores

*Dar ao dev o modelo mental de como LLMs funcionam e o kit de ferramentas de IA do dia a dia.*

12 aulas · 23.2 min de vídeo · 365 min de prática/estudo

| Aula | Título | Tipo | Vídeo | Prática | Objetivos |
|---|---|---|---|---|---|
| m01-a01 | De Turing aos LLMs: a linha do tempo da IA | conceitual | 1:40 | 10 min | Situar ML, deep learning e LLMs numa linha do tempo<br>Explicar por que os LLMs surgiram agora |
| m01-a02 | ML, deep learning, tensores e redes neurais em 2 minutos | conceitual | 2:00 | 20 min | Diferenciar IA, ML e deep learning<br>Explicar tensores e como uma rede neural aprende (gradiente) |
| m01-a03 | Como um LLM funciona: tokens, embeddings e attention | conceitual | 1:50 | 25 min | Explicar o caminho token → embedding → attention → próximo token<br>Relacionar a attention ao uso de contexto em ChatGPT, Gemini e outros |
| m01-a04 | Sua primeira rede neural em JavaScript | codigo | 2:20 | 45 min | Treinar uma rede pequena em JavaScript<br>Percorrer o ciclo dados → treino → validação → inferência |
| m01-a05 | ML no navegador: vídeo, jogos e deep learning na prática | pratica | 2:00 | 60 min | Rodar um modelo pré-treinado no browser sobre vídeo da webcam<br>Identificar usos de ML em jogos |
| m01-a06 | Prompt engineering para codar, debugar e documentar | ferramenta | 1:50 | 30 min | Escrever prompts com contexto, formato e critérios de aceite<br>Aplicar padrões de prompt para código, debug e docs |
| m01-a07 | Cursor, VS Code e Windsurf: IDEs com IA e vibe coding | ferramenta | 1:50 | 20 min | Comparar Cursor, VS Code e Windsurf<br>Avaliar o que é vibe coding e seus limites |
| m01-a08 | Cursor rules: a IA programando do jeito do seu time | ferramenta | 1:50 | 30 min | Criar regras de projeto em .cursor/rules com o tipo de aplicação certo<br>Escolher entre Always, Auto Attached (globs), Agent Requested e Manual |
| m01-a09 | MCPs e automação: IA que testa, lê docs e navega | conceitual | 1:50 | 20 min | Explicar o que um MCP conecta<br>Usar IA para gerar testes, consultar docs e navegar sites; orquestrar fluxos com n8n |
| m01-a10 | RAG, embeddings e busca semântica com JavaScript e Postgres | codigo | 2:20 | 60 min | Explicar RAG e similarity search<br>Montar um RAG mínimo com embeddings e pgvector |
| m01-a11 | Modelos abertos x fechados: OpenRouter e Ollama | ferramenta | 1:50 | 30 min | Comparar modelos abertos e proprietários<br>Chamar vários modelos via OpenRouter e rodar um modelo local com Ollama |
| m01-a12 | Agentes de IA: decisões em etapas e agentes que programam | conceitual | 1:50 | 15 min | Explicar o loop de um agente<br>Reconhecer agentes de código reais e seus limites |

<details><summary>m01-a01 — tópicos da ementa e prática</summary>

- História e contexto da IA

Config: `aulas/m01-a01.yaml` · saída: `m01-fundamentos-ia-llms/m01-a01-historia-da-ia/`

</details>

<details><summary>m01-a02 — tópicos da ementa e prática</summary>

- Revisão de ML, DL e AI para preparar o terreno
- Fundamentos de Web Machine Learning

Config: `aulas/m01-a02.yaml` · saída: `m01-fundamentos-ia-llms/m01-a02-ml-dl-redes-neurais/`

</details>

<details><summary>m01-a03 — tópicos da ementa e prática</summary>

- Como funcionam LLMs: transformers, embeddings, attention
- Exemplos de LLMs: ChatGPT, Gemini e outros

**Prática:** Exercício: calcular à mão uma attention de 3 tokens (Q·K, softmax, soma ponderada de V).

Config: `aulas/m01-a03.yaml` · saída: `m01-fundamentos-ia-llms/m01-a03-como-funcionam-llms/`

</details>

<details><summary>m01-a04 — tópicos da ementa e prática</summary>

- Criando sua primeira IA do zero

Config: `aulas/m01-a04.yaml` · saída: `m01-fundamentos-ia-llms/m01-a04-primeira-rede-neural-js/`

</details>

<details><summary>m01-a05 — tópicos da ementa e prática</summary>

- Projetos práticos com ML na Web

**Prática:** Detectar pose/objetos na webcam com um modelo pré-treinado.

Config: `aulas/m01-a05.yaml` · saída: `m01-fundamentos-ia-llms/m01-a05-ml-na-web/`

</details>

<details><summary>m01-a06 — tópicos da ementa e prática</summary>

- Prompt Engineering na prática

Config: `aulas/m01-a06.yaml` · saída: `m01-fundamentos-ia-llms/m01-a06-prompt-engineering-dev/`

</details>

<details><summary>m01-a07 — tópicos da ementa e prática</summary>

- História e visão geral do Cursor
- Comparando VSCode, Windsurf e Cursor
- Conceito de Vibe Coding e o case do levelsio (microSaaS com +100k/mês usando AI)

Config: `aulas/m01-a07.yaml` · saída: `m01-fundamentos-ia-llms/m01-a07-cursor-e-ides-com-ia/`

</details>

<details><summary>m01-a08 — tópicos da ementa e prática</summary>

- Como usar .cursor rules para deixar a IA “do seu jeito”

**Prática:** Criar 3 regras (.mdc) para um projeto e validar o frontmatter.

Config: `aulas/m01-a08.yaml` · saída: `m01-fundamentos-ia-llms/m01-a08-cursor-rules/`

</details>

<details><summary>m01-a09 — tópicos da ementa e prática</summary>

- MCPs e automação para devs

Config: `aulas/m01-a09.yaml` · saída: `m01-fundamentos-ia-llms/m01-a09-mcp-e-automacao/`

</details>

<details><summary>m01-a10 — tópicos da ementa e prática</summary>

- RAG, embeddings e busca semântica

Config: `aulas/m01-a10.yaml` · saída: `m01-fundamentos-ia-llms/m01-a10-rag-embeddings/`

</details>

<details><summary>m01-a11 — tópicos da ementa e prática</summary>

- Modelos open-source vs. proprietários

Config: `aulas/m01-a11.yaml` · saída: `m01-fundamentos-ia-llms/m01-a11-modelos-abertos-openrouter-ollama/`

</details>

<details><summary>m01-a12 — tópicos da ementa e prática</summary>

- Agents e automação avançada

Config: `aulas/m01-a12.yaml` · saída: `m01-fundamentos-ia-llms/m01-a12-agentes-de-ia/`

</details>

## 2. APIs de IA Generativa e Prompt Engineering

*Integrar APIs de modelos em produtos reais com custo, previsibilidade e observabilidade.*

8 aulas · 16.8 min de vídeo · 360 min de prática/estudo

| Aula | Título | Tipo | Vídeo | Prática | Objetivos |
|---|---|---|---|---|---|
| m02-a01 | IA como serviço: wrappers, oportunidades e onde o dev entra | conceitual | 1:40 | 15 min | Analisar o mercado de 'wrappers' de LLM<br>Identificar oportunidades reais para devs |
| m02-a02 | OpenAI, Anthropic, Hugging Face e Gemini: APIs comparadas | ferramenta | 2:00 | 30 min | Comparar APIs e modelos dos principais provedores<br>Escolher provedor por cenário de uso |
| m02-a03 | Prompt chaining, templates e menos alucinação | codigo | 2:10 | 40 min | Encadear prompts para tarefas complexas<br>Padronizar prompts com templates e reduzir alucinações |
| m02-a04 | Custo e previsibilidade: tokens, cache e contexto | codigo | 2:00 | 30 min | Desenhar chamadas pensando em custo<br>Aplicar cache de prompt e redução de tokens |
| m02-a05 | RAG avançado: orquestração, retries e observabilidade | codigo | 2:20 | 45 min | Orquestrar fluxos com LangChain ou similares<br>Tratar erros, re-tentativas e logging em apps de IA |
| m02-a06 | Mão na massa: LLM da OpenAI num back-end existente | projeto | 2:30 | 90 min | Integrar um LLM a um back-end com autenticação e versionamento<br>Testar o fluxo de requisições |
| m02-a07 | Modelos multimodais: texto, imagem, áudio e vídeo | conceitual | 1:50 | 20 min | Escolher a modalidade certa por problema<br>Conhecer OpenAI Vision, Whisper e Gemini multimodal |
| m02-a08 | OCR inteligente, análise de mídia e bots multimodais | projeto | 2:20 | 90 min | Construir um OCR inteligente com LLM<br>Esboçar um bot multimodal |

<details><summary>m02-a01 — tópicos da ementa e prática</summary>

- Panorama do mercado de IA como serviço

Config: `aulas/m02-a01.yaml` · saída: `m02-apis-ia-generativa/m02-a01-mercado-ia-como-servico/`

</details>

<details><summary>m02-a02 — tópicos da ementa e prática</summary>

- Principais provedores de modelos de IA

Config: `aulas/m02-a02.yaml` · saída: `m02-apis-ia-generativa/m02-a02-provedores-de-modelos/`

</details>

<details><summary>m02-a03 — tópicos da ementa e prática</summary>

- Engenharia de prompts avançada

Config: `aulas/m02-a03.yaml` · saída: `m02-apis-ia-generativa/m02-a03-prompts-avancados/`

</details>

<details><summary>m02-a04 — tópicos da ementa e prática</summary>

- Boas práticas de consistência e custo-eficiência

Config: `aulas/m02-a04.yaml` · saída: `m02-apis-ia-generativa/m02-a04-custo-e-previsibilidade/`

</details>

<details><summary>m02-a05 — tópicos da ementa e prática</summary>

- RAG avançado na prática

Config: `aulas/m02-a05.yaml` · saída: `m02-apis-ia-generativa/m02-a05-rag-avancado-orquestracao/`

</details>

<details><summary>m02-a06 — tópicos da ementa e prática</summary>

- Mão na massa: integrando IA ao back-end

**Prática:** Adicionar um endpoint de resumo com LLM a uma API existente, com testes.

Config: `aulas/m02-a06.yaml` · saída: `m02-apis-ia-generativa/m02-a06-llm-no-back-end/`

</details>

<details><summary>m02-a07 — tópicos da ementa e prática</summary>

- Modelos multimodais (texto, imagem, áudio, vídeo)

Config: `aulas/m02-a07.yaml` · saída: `m02-apis-ia-generativa/m02-a07-multimodal/`

</details>

<details><summary>m02-a08 — tópicos da ementa e prática</summary>

- Aplicações práticas com foco em APIs

**Prática:** OCR de notas fiscais com extração estruturada em JSON.

Config: `aulas/m02-a08.yaml` · saída: `m02-apis-ia-generativa/m02-a08-apps-multimodais/`

</details>

## 3. MCP – Model Context Protocol

*Construir, proteger e operar servidores MCP que conectam LLMs aos sistemas da empresa.*

9 aulas · 17.8 min de vídeo · 335 min de prática/estudo

| Aula | Título | Tipo | Vídeo | Prática | Objetivos |
|---|---|---|---|---|---|
| m03-a01 | O que é MCP e por que ele acabou com as integrações sob medida | conceitual | 1:50 | 15 min | Explicar o problema N×M que o MCP resolve<br>Descrever host, client e server |
| m03-a02 | Tools, resources e prompts: a integração padronizada | conceitual | 1:50 | 20 min | Mapear APIs, bancos e serviços para primitivas MCP<br>Explicar a padronização de entrada/saída |
| m03-a03 | MCP x tools/plugins de cada provedor | conceitual | 1:40 | 15 min | Comparar MCP com function calling proprietário<br>Decidir quando usar MCP |
| m03-a04 | Criando um MCP server em TypeScript do zero | codigo | 2:20 | 60 min | Implementar um MCP server com o SDK oficial (tool com schema Zod, transporte stdio)<br>Consumir o server com um client MCP e testar automaticamente |
| m03-a05 | Organizando um projeto MCP: módulos, testes e versionamento | codigo | 1:50 | 30 min | Aplicar uma estrutura de pastas para tools/resources<br>Separar lógica de negócio do transporte |
| m03-a06 | Sua empresa como MCP: CRM, billing e suporte expostos para IA | conceitual | 1:50 | 20 min | Desenhar uma camada AI-ready sobre serviços internos |
| m03-a07 | Segurança em MCP: tokens, rate limiting e WAF | codigo | 2:10 | 40 min | Proteger um MCP remoto com tokens de serviço<br>Aplicar rate limiting e WAF |
| m03-a08 | MCP no mundo real: legados, copilots e IDEs | conceitual | 1:50 | 15 min | Analisar casos de MCP em empresas<br>Identificar cenários: agentes, IDEs, ERP/CRM |
| m03-a09 | Hands-on: do MCP local à produção com front, back e vários clients | projeto | 2:30 | 120 min | Integrar o MCP a front-end e back-end<br>Testar em diferentes clients e compor com outros MCPs |

<details><summary>m03-a01 — tópicos da ementa e prática</summary>

- Visão geral de MCP (Model Context Protocol)

Config: `aulas/m03-a01.yaml` · saída: `m03-mcp/m03-a01-o-que-e-mcp/`

</details>

<details><summary>m03-a02 — tópicos da ementa e prática</summary>

- Integração padronizada de LLMs com MCP

Config: `aulas/m03-a02.yaml` · saída: `m03-mcp/m03-a02-integracao-padronizada/`

</details>

<details><summary>m03-a03 — tópicos da ementa e prática</summary>

- MCPs vs Tools tradicionais

Config: `aulas/m03-a03.yaml` · saída: `m03-mcp/m03-a03-mcp-vs-tools/`

</details>

<details><summary>m03-a04 — tópicos da ementa e prática</summary>

- Como criar e consumir MCPs usando JavaScript/TypeScript
- Criação de um MCP server do zero

**Prática:** Adicionar uma nova tool ao server e cobri-la no teste com o client.

Config: `aulas/m03-a04.yaml` · saída: `m03-mcp/m03-a04-mcp-server-typescript/`

</details>

<details><summary>m03-a05 — tópicos da ementa e prática</summary>

- Boas práticas de organização de código e estrutura de projeto

Config: `aulas/m03-a05.yaml` · saída: `m03-mcp/m03-a05-estrutura-projeto-mcp/`

</details>

<details><summary>m03-a06 — tópicos da ementa e prática</summary>

- Transformando sua empresa em um “MCP”

Config: `aulas/m03-a06.yaml` · saída: `m03-mcp/m03-a06-empresa-como-mcp/`

</details>

<details><summary>m03-a07 — tópicos da ementa e prática</summary>

- Segurança e governança em MCPs

Config: `aulas/m03-a07.yaml` · saída: `m03-mcp/m03-a07-seguranca-mcp/`

</details>

<details><summary>m03-a08 — tópicos da ementa e prática</summary>

- Casos de uso reais em empresas
- Cenários práticos de aplicação

Config: `aulas/m03-a08.yaml` · saída: `m03-mcp/m03-a08-mcp-casos-e-cenarios/`

</details>

<details><summary>m03-a09 — tópicos da ementa e prática</summary>

- Integração desse MCP com front-end (UI) e back-end
- Testando o MCP em diferentes LLM clients e compondo com outros MCPs

**Prática:** Publicar o MCP por HTTP e testá-lo em dois clients.

Config: `aulas/m03-a09.yaml` · saída: `m03-mcp/m03-a09-mcp-em-producao/`

</details>

## 4. Criação de Agentes Autônomos

*Projetar, implementar e observar agentes autônomos e sistemas multiagente.*

9 aulas · 19.0 min de vídeo · 460 min de prática/estudo

| Aula | Título | Tipo | Vídeo | Prática | Objetivos |
|---|---|---|---|---|---|
| m04-a01 | Arquitetura de agentes: o agent loop | conceitual | 1:50 | 20 min | Explicar percepção → raciocínio → ação → feedback<br>Identificar planner, executor, memória e toolbox |
| m04-a02 | ReAct, Plan-and-Execute e Reflection | codigo | 2:10 | 40 min | Comparar padrões de raciocínio<br>Implementar ReAct e Plan-Execute |
| m04-a03 | Function calling e tool use com schemas JSON | codigo | 2:10 | 40 min | Desenhar schemas JSON de funções<br>Conectar um agente a APIs e bancos |
| m04-a04 | Memória e reflexão em agentes | codigo | 2:00 | 35 min | Escolher tipos de memória<br>Implementar um reflection loop |
| m04-a05 | Gerenciamento de contexto: pruning e compressão | conceitual | 1:50 | 25 min | Aplicar context pruning/compression<br>Equilibrar contexto global e local |
| m04-a06 | LangGraph: grafos, roteamento e fallback | codigo | 2:20 | 45 min | Construir um grafo de execução<br>Depurar agentes complexos |
| m04-a07 | Observabilidade, guardrails e limites de autonomia | codigo | 2:00 | 30 min | Instrumentar agentes<br>Aplicar guardrails e human-in-the-loop |
| m04-a08 | Projeto: agente que automatiza tarefas complexas | projeto | 2:30 | 180 min | Construir um agente com planejamento, APIs, logs e memória |
| m04-a09 | Sistemas multiagente: supervisor, hierárquico e group chat | codigo | 2:10 | 45 min | Comparar padrões multiagente<br>Implementar um mini sistema cooperativo |

<details><summary>m04-a01 — tópicos da ementa e prática</summary>

- m04.u01

Config: `aulas/m04-a01.yaml` · saída: `m04-agentes-autonomos/m04-a01-arquitetura-de-agentes/`

</details>

<details><summary>m04-a02 — tópicos da ementa e prática</summary>

- m04.u02

Config: `aulas/m04-a02.yaml` · saída: `m04-agentes-autonomos/m04-a02-react-plan-execute-reflection/`

</details>

<details><summary>m04-a03 — tópicos da ementa e prática</summary>

- m04.u03

Config: `aulas/m04-a03.yaml` · saída: `m04-agentes-autonomos/m04-a03-function-calling/`

</details>

<details><summary>m04-a04 — tópicos da ementa e prática</summary>

- m04.u04

Config: `aulas/m04-a04.yaml` · saída: `m04-agentes-autonomos/m04-a04-memoria-e-reflexao/`

</details>

<details><summary>m04-a05 — tópicos da ementa e prática</summary>

- m04.u05

Config: `aulas/m04-a05.yaml` · saída: `m04-agentes-autonomos/m04-a05-gerenciamento-de-contexto/`

</details>

<details><summary>m04-a06 — tópicos da ementa e prática</summary>

- m04.u06

Config: `aulas/m04-a06.yaml` · saída: `m04-agentes-autonomos/m04-a06-langgraph/`

</details>

<details><summary>m04-a07 — tópicos da ementa e prática</summary>

- m04.u07

Config: `aulas/m04-a07.yaml` · saída: `m04-agentes-autonomos/m04-a07-observabilidade-e-limites/`

</details>

<details><summary>m04-a08 — tópicos da ementa e prática</summary>

- m04.u08

Config: `aulas/m04-a08.yaml` · saída: `m04-agentes-autonomos/m04-a08-projeto-agente/`

</details>

<details><summary>m04-a09 — tópicos da ementa e prática</summary>

- m04.u09

Config: `aulas/m04-a09.yaml` · saída: `m04-agentes-autonomos/m04-a09-multiagentes/`

</details>

## 5. Ferramentas de IA para UX & UI

*Usar IA para prototipar, gerar e testar interfaces e levar IA ao front-end.*

5 aulas · 10.2 min de vídeo · 200 min de prática/estudo

| Aula | Título | Tipo | Vídeo | Prática | Objetivos |
|---|---|---|---|---|---|
| m05-a01 | A revolução da IA no design de interfaces | conceitual | 1:40 | 15 min | Explicar AI-driven UX<br>Mapear ferramentas por etapa do design |
| m05-a02 | Prototipação e geração de UI com IA (Firebase Studio) | ferramenta | 2:10 | 45 min | Gerar wireframes a partir de texto<br>Prototipar com Firebase Studio e validar fluxos |
| m05-a03 | Agentes de código e Gemini CLI no front-end | ferramenta | 2:00 | 40 min | Usar Gemini CLI para scaffolding<br>Definir um fluxo com agentes de código |
| m05-a04 | Testes E2E e interação inteligente com a UI | codigo | 2:00 | 40 min | Automatizar testes E2E com IA |
| m05-a05 | IA no cliente e no servidor com Firebase AI Logic | codigo | 2:20 | 60 min | Consumir APIs de IA no front-end com segurança<br>Construir uma feature inteligente |

<details><summary>m05-a01 — tópicos da ementa e prática</summary>

- m05.u01

Config: `aulas/m05-a01.yaml` · saída: `m05-ia-ux-ui/m05-a01-ia-no-design/`

</details>

<details><summary>m05-a02 — tópicos da ementa e prática</summary>

- m05.u02

Config: `aulas/m05-a02.yaml` · saída: `m05-ia-ux-ui/m05-a02-prototipacao-com-ia/`

</details>

<details><summary>m05-a03 — tópicos da ementa e prática</summary>

- m05.u03

Config: `aulas/m05-a03.yaml` · saída: `m05-ia-ux-ui/m05-a03-agentes-cli-front-end/`

</details>

<details><summary>m05-a04 — tópicos da ementa e prática</summary>

- m05.u04

Config: `aulas/m05-a04.yaml` · saída: `m05-ia-ux-ui/m05-a04-testes-e2e-com-ia/`

</details>

<details><summary>m05-a05 — tópicos da ementa e prática</summary>

- m05.u05

Config: `aulas/m05-a05.yaml` · saída: `m05-ia-ux-ui/m05-a05-ia-no-cliente-e-servidor/`

</details>

## 6. Ferramentas de IA para DevOps

*Aplicar IA generativa e agentes à infraestrutura, operação, segurança e custos.*

10 aulas · 22.3 min de vídeo · 610 min de prática/estudo

| Aula | Título | Tipo | Vídeo | Prática | Objetivos |
|---|---|---|---|---|---|
| m06-a01 | IA generativa para infraestrutura: fundamentos e limites | conceitual | 2:00 | 20 min | Relacionar LLMs, APIs, agentes e RAG à infraestrutura<br>Validar respostas e evitar alucinações |
| m06-a02 | IaC Copilot: Terraform validado gerado por IA | codigo | 2:20 | 60 min | Gerar Terraform a partir de linguagem natural<br>Validar com plan/validate e Policy-as-Code |
| m06-a03 | Agentes para Kubernetes: deploy, autoscaling e GitOps | codigo | 2:20 | 60 min | Gerar manifests e HPA/VPA<br>Integrar rollout com Argo CD/Flux |
| m06-a04 | Troubleshooting assistido: ReAct para pods quebrados | codigo | 2:10 | 50 min | Diagnosticar CrashLoopBackOff e OOMKilled com IA<br>Correlacionar logs e traces |
| m06-a05 | AIOps: PromQL por linguagem natural e anomalias | codigo | 2:10 | 50 min | Gerar PromQL/LogQL<br>Detectar anomalias com ML |
| m06-a06 | ChatOps com aprovação humana e RBAC | codigo | 2:10 | 50 min | Construir comandos seguros<br>Auditar ações com aprovação |
| m06-a07 | Segurança, compliance e CI/CD com copilots | codigo | 2:20 | 50 min | Automatizar scans e AI fix<br>Gerar pipelines com gates inteligentes |
| m06-a08 | FinOps com IA: Infracost, rightsizing e forecasting | codigo | 2:00 | 40 min | Estimar custos em PRs<br>Detectar recursos ociosos |
| m06-a09 | RAG de runbooks, post-mortem e auto-remediação segura | codigo | 2:20 | 50 min | Montar RAG de runbooks<br>Auto-remediar com dry-run e human-in-the-loop |
| m06-a10 | Projeto integrador DevOps com IA | projeto | 2:30 | 180 min | Entregar um copilot/agente DevOps com guardrails e ROI |

<details><summary>m06-a01 — tópicos da ementa e prática</summary>

- m06.u01

Config: `aulas/m06-a01.yaml` · saída: `m06-ia-devops/m06-a01-ia-generativa-infra/`

</details>

<details><summary>m06-a02 — tópicos da ementa e prática</summary>

- m06.u02

Config: `aulas/m06-a02.yaml` · saída: `m06-ia-devops/m06-a02-iac-copilot/`

</details>

<details><summary>m06-a03 — tópicos da ementa e prática</summary>

- m06.u03

Config: `aulas/m06-a03.yaml` · saída: `m06-ia-devops/m06-a03-agentes-kubernetes/`

</details>

<details><summary>m06-a04 — tópicos da ementa e prática</summary>

- m06.u04

Config: `aulas/m06-a04.yaml` · saída: `m06-ia-devops/m06-a04-troubleshooting-assistido/`

</details>

<details><summary>m06-a05 — tópicos da ementa e prática</summary>

- m06.u05

Config: `aulas/m06-a05.yaml` · saída: `m06-ia-devops/m06-a05-aiops-observabilidade/`

</details>

<details><summary>m06-a06 — tópicos da ementa e prática</summary>

- m06.u06

Config: `aulas/m06-a06.yaml` · saída: `m06-ia-devops/m06-a06-chatops-com-aprovacao/`

</details>

<details><summary>m06-a07 — tópicos da ementa e prática</summary>

- m06.u07
- m06.u08

Config: `aulas/m06-a07.yaml` · saída: `m06-ia-devops/m06-a07-seguranca-e-cicd/`

</details>

<details><summary>m06-a08 — tópicos da ementa e prática</summary>

- m06.u09

Config: `aulas/m06-a08.yaml` · saída: `m06-ia-devops/m06-a08-finops-com-ia/`

</details>

<details><summary>m06-a09 — tópicos da ementa e prática</summary>

- m06.u10
- m06.u11

Config: `aulas/m06-a09.yaml` · saída: `m06-ia-devops/m06-a09-runbooks-e-auto-remediacao/`

</details>

<details><summary>m06-a10 — tópicos da ementa e prática</summary>

- m06.u12

Config: `aulas/m06-a10.yaml` · saída: `m06-ia-devops/m06-a10-projeto-integrador-devops/`

</details>

## 7. Ferramentas de IA para Gestão de Projetos

*Usar IA para escopo, backlog, cronograma, riscos, comunicação e automação de gestão.*

8 aulas · 15.5 min de vídeo · 260 min de prática/estudo

| Aula | Título | Tipo | Vídeo | Prática | Objetivos |
|---|---|---|---|---|---|
| m07-a01 | Requirements copilot: escopo e histórias com IA | ferramenta | 1:50 | 30 min | Converter descrições em histórias e critérios de aceite |
| m07-a02 | Priorização inteligente de backlog | ferramenta | 1:50 | 30 min | Aplicar frameworks de priorização com IA |
| m07-a03 | Cronograma, capacidade e estimativas com IA (Monte Carlo) | codigo | 2:10 | 40 min | Gerar cronogramas com dependências<br>Estimar prazos com simulação |
| m07-a04 | Riscos e mitigação com AIOps de projeto | conceitual | 1:50 | 25 min | Detectar riscos com dados do projeto |
| m07-a05 | Reuniões turbinadas e status reports automáticos | ferramenta | 2:00 | 30 min | Extrair decisões e ações de reuniões<br>Gerar relatórios por público |
| m07-a06 | Governança, compliance e qualidade com IA | conceitual | 1:50 | 25 min | Automatizar checklists e trilhas de auditoria |
| m07-a07 | Automação em Jira, Notion e Slack com bots em JavaScript | codigo | 2:20 | 60 min | Criar um bot que transforma linguagem natural em workflow |
| m07-a08 | Portfólio e OKRs com IA | conceitual | 1:40 | 20 min | Alinhar projetos a OKRs com métricas de outcome |

<details><summary>m07-a01 — tópicos da ementa e prática</summary>

- m07.u01

Config: `aulas/m07-a01.yaml` · saída: `m07-ia-gestao-projetos/m07-a01-requirements-copilot/`

</details>

<details><summary>m07-a02 — tópicos da ementa e prática</summary>

- m07.u02

Config: `aulas/m07-a02.yaml` · saída: `m07-ia-gestao-projetos/m07-a02-backlog-inteligente/`

</details>

<details><summary>m07-a03 — tópicos da ementa e prática</summary>

- m07.u03
- m07.u04

Config: `aulas/m07-a03.yaml` · saída: `m07-ia-gestao-projetos/m07-a03-cronograma-e-estimativas/`

</details>

<details><summary>m07-a04 — tópicos da ementa e prática</summary>

- m07.u05

Config: `aulas/m07-a04.yaml` · saída: `m07-ia-gestao-projetos/m07-a04-riscos-aiops-projeto/`

</details>

<details><summary>m07-a05 — tópicos da ementa e prática</summary>

- m07.u06
- m07.u07

Config: `aulas/m07-a05.yaml` · saída: `m07-ia-gestao-projetos/m07-a05-reunioes-e-status/`

</details>

<details><summary>m07-a06 — tópicos da ementa e prática</summary>

- m07.u08

Config: `aulas/m07-a06.yaml` · saída: `m07-ia-gestao-projetos/m07-a06-governanca-qualidade/`

</details>

<details><summary>m07-a07 — tópicos da ementa e prática</summary>

- m07.u09

Config: `aulas/m07-a07.yaml` · saída: `m07-ia-gestao-projetos/m07-a07-automacao-jira-slack/`

</details>

<details><summary>m07-a08 — tópicos da ementa e prática</summary>

- m07.u10

Config: `aulas/m07-a08.yaml` · saída: `m07-ia-gestao-projetos/m07-a08-portfolio-e-okrs/`

</details>

## 8. Arquitetura de Sistemas com IA

*Escolher e combinar padrões arquiteturais AI-first, de single-agent a enterprise.*

5 aulas · 10.3 min de vídeo · 170 min de prática/estudo

| Aula | Título | Tipo | Vídeo | Prática | Objetivos |
|---|---|---|---|---|---|
| m08-a01 | Arquitetura AI-first: 5 padrões e trade-offs | conceitual | 2:00 | 25 min | Comparar padrões arquiteturais com IA<br>Decidir por latência, custo e precisão |
| m08-a02 | Arquiteturas single-agent | codigo | 2:00 | 40 min | Prototipar agentes reativos e deliberativos |
| m08-a03 | Arquiteturas multi-agent em JavaScript | codigo | 2:10 | 45 min | Implementar orquestração multiagente |
| m08-a04 | Padrões de design de IA: RAG, roteamento, cache e HITL | conceitual | 2:00 | 30 min | Aplicar roteamento de modelos e caching semântico |
| m08-a05 | Arquitetura enterprise: do API gateway à observabilidade | conceitual | 2:10 | 30 min | Mapear o stack completo de IA enterprise |

<details><summary>m08-a01 — tópicos da ementa e prática</summary>

- m08.u01

Config: `aulas/m08-a01.yaml` · saída: `m08-arquitetura-ia/m08-a01-arquitetura-ai-first/`

</details>

<details><summary>m08-a02 — tópicos da ementa e prática</summary>

- m08.u02

Config: `aulas/m08-a02.yaml` · saída: `m08-arquitetura-ia/m08-a02-single-agent/`

</details>

<details><summary>m08-a03 — tópicos da ementa e prática</summary>

- m08.u03

Config: `aulas/m08-a03.yaml` · saída: `m08-arquitetura-ia/m08-a03-multi-agent/`

</details>

<details><summary>m08-a04 — tópicos da ementa e prática</summary>

- m08.u04

Config: `aulas/m08-a04.yaml` · saída: `m08-arquitetura-ia/m08-a04-padroes-ia/`

</details>

<details><summary>m08-a05 — tópicos da ementa e prática</summary>

- m08.u05

Config: `aulas/m08-a05.yaml` · saída: `m08-arquitetura-ia/m08-a05-arquitetura-enterprise/`

</details>

## 9. Processamento de Dados e Fine-Tuning de Modelos

*Decidir quando fazer fine-tuning, preparar dados, treinar, avaliar e integrar modelos customizados.*

6 aulas · 12.7 min de vídeo · 360 min de prática/estudo

| Aula | Título | Tipo | Vídeo | Prática | Objetivos |
|---|---|---|---|---|---|
| m09-a01 | Quando fazer fine-tuning (e quando não) | conceitual | 1:50 | 20 min | Aplicar um decision framework: prompt, RAG ou fine-tuning |
| m09-a02 | Preparando datasets JSONL para fine-tuning | codigo | 2:10 | 45 min | Limpar, balancear e estruturar dados em JSONL |
| m09-a03 | Fine-tuning via API da OpenAI | codigo | 2:10 | 45 min | Subir dataset, treinar e versionar com scripts JavaScript |
| m09-a04 | LoRA e PEFT na prática | conceitual | 2:00 | 30 min | Explicar LoRA e comparar custo x desempenho |
| m09-a05 | Avaliando modelos fine-tunados (A/B e métricas) | codigo | 2:00 | 40 min | Medir precisão e consistência<br>Comparar modelos com testes A/B |
| m09-a06 | Projeto: modelo customizado para um domínio | projeto | 2:30 | 180 min | Entregar um modelo fine-tunado integrado a um fluxo |

<details><summary>m09-a01 — tópicos da ementa e prática</summary>

- m09.u01

Config: `aulas/m09-a01.yaml` · saída: `m09-dados-fine-tuning/m09-a01-quando-fazer-fine-tuning/`

</details>

<details><summary>m09-a02 — tópicos da ementa e prática</summary>

- m09.u02

Config: `aulas/m09-a02.yaml` · saída: `m09-dados-fine-tuning/m09-a02-datasets-jsonl/`

</details>

<details><summary>m09-a03 — tópicos da ementa e prática</summary>

- m09.u03

Config: `aulas/m09-a03.yaml` · saída: `m09-dados-fine-tuning/m09-a03-fine-tuning-openai/`

</details>

<details><summary>m09-a04 — tópicos da ementa e prática</summary>

- m09.u04

Config: `aulas/m09-a04.yaml` · saída: `m09-dados-fine-tuning/m09-a04-lora-peft/`

</details>

<details><summary>m09-a05 — tópicos da ementa e prática</summary>

- m09.u05

Config: `aulas/m09-a05.yaml` · saída: `m09-dados-fine-tuning/m09-a05-avaliar-fine-tuning/`

</details>

<details><summary>m09-a06 — tópicos da ementa e prática</summary>

- m09.u06

Config: `aulas/m09-a06.yaml` · saída: `m09-dados-fine-tuning/m09-a06-projeto-modelo-customizado/`

</details>

## 10. Segurança e Governança em IA

*Governar riscos técnicos, éticos, legais e financeiros de sistemas com IA.*

3 aulas · 5.8 min de vídeo · 75 min de prática/estudo

| Aula | Título | Tipo | Vídeo | Prática | Objetivos |
|---|---|---|---|---|---|
| m10-a01 | Governança, explicabilidade e vieses | conceitual | 2:00 | 25 min | Explicar governança em IA<br>Reconhecer vieses e limites de explicabilidade |
| m10-a02 | Riscos de IA: humanos, segurança, dados e regulação | conceitual | 2:10 | 30 min | Classificar riscos de IA<br>Relacionar riscos a controles e regulação |
| m10-a03 | Custos financeiros de IA | conceitual | 1:40 | 20 min | Estimar e controlar custos de IA |

<details><summary>m10-a01 — tópicos da ementa e prática</summary>

- O que é Governança em IA
- Interpretabilidade e Explicabilidade em Modelos de IA
- Vieses e Responsabilidade em Modelos de IA

Config: `aulas/m10-a01.yaml` · saída: `m10-seguranca-governanca/m10-a01-governanca-explicabilidade/`

</details>

<details><summary>m10-a02 — tópicos da ementa e prática</summary>

- Gerenciamento de Riscos em Inteligência Artificial - Aspectos Humanos e Éticos
- Gerenciamento de Riscos em Inteligência Artificial - Segurança e Dados
- Gerenciamento de Riscos em Inteligência Artificial - Aspectos Legais e Regulatórios

Config: `aulas/m10-a02.yaml` · saída: `m10-seguranca-governanca/m10-a02-riscos-de-ia/`

</details>

<details><summary>m10-a03 — tópicos da ementa e prática</summary>

- Custos Financeiros em Inteligência Artificial

Config: `aulas/m10-a03.yaml` · saída: `m10-seguranca-governanca/m10-a03-custos-de-ia/`

</details>

## 11. Projeto Integrador – Capstone Project

*Construir e defender um Micro-SaaS com RAG, agentes e MCP, do escopo ao deploy.*

5 aulas · 10.8 min de vídeo · 960 min de prática/estudo

| Aula | Título | Tipo | Vídeo | Prática | Objetivos |
|---|---|---|---|---|---|
| m11-a01 | Ideação e arquitetura do Micro-SaaS | projeto | 2:00 | 120 min | Definir problema, proposta de valor e arquitetura |
| m11-a02 | Core: RAG, vector database e agente principal | projeto | 2:20 | 240 min | Entregar protótipo RAG com CLI (Entrega 1) |
| m11-a03 | Back-end, MCP e orquestração com ADK | projeto | 2:20 | 240 min | Entregar API documentada e app com MCP (Entrega 2) |
| m11-a04 | Front-end Angular, validação do MCP e deploy | projeto | 2:20 | 240 min | Entregar solução implantada com agente via MCP (Entrega 3) |
| m11-a05 | Apresentação final e defesa técnica | projeto | 1:50 | 120 min | Defender decisões de arquitetura e documentar |

<details><summary>m11-a01 — tópicos da ementa e prática</summary>

- m11.u01

Config: `aulas/m11-a01.yaml` · saída: `m11-capstone/m11-a01-ideacao-arquitetura/`

</details>

<details><summary>m11-a02 — tópicos da ementa e prática</summary>

- m11.u02

Config: `aulas/m11-a02.yaml` · saída: `m11-capstone/m11-a02-rag-e-agentes/`

</details>

<details><summary>m11-a03 — tópicos da ementa e prática</summary>

- m11.u03

Config: `aulas/m11-a03.yaml` · saída: `m11-capstone/m11-a03-backend-mcp-orquestracao/`

</details>

<details><summary>m11-a04 — tópicos da ementa e prática</summary>

- m11.u04

Config: `aulas/m11-a04.yaml` · saída: `m11-capstone/m11-a04-front-end-e-deploy/`

</details>

<details><summary>m11-a05 — tópicos da ementa e prática</summary>

- m11.u05

Config: `aulas/m11-a05.yaml` · saída: `m11-capstone/m11-a05-apresentacao-defesa/`

</details>

## 12. Carreira e Entrevistas para Engenheiros de IA Aplicada

*Posicionar-se, passar em entrevistas e negociar como engenheiro de IA aplicada.*

5 aulas · 9.7 min de vídeo · 195 min de prática/estudo

| Aula | Título | Tipo | Vídeo | Prática | Objetivos |
|---|---|---|---|---|---|
| m12-a01 | LinkedIn, networking e marca pessoal | carreira | 1:50 | 30 min | Otimizar perfil e rede para vagas de IA |
| m12-a02 | Portfólio no GitHub e expectativas por nível | carreira | 1:50 | 45 min | Montar um portfólio de projetos de IA<br>Entender o que cada nível exige |
| m12-a03 | Entrevistas de RH (STAR) e proposta de valor | carreira | 1:50 | 30 min | Responder com STAR<br>Pesquisar e justificar expectativa salarial |
| m12-a04 | Entrevistas técnicas: live coding, system design e perguntas de IA | carreira | 2:20 | 60 min | Praticar live coding pensando em voz alta<br>Desenhar um sistema de IA na entrevista |
| m12-a05 | Negociação, promoção e diferenciação | carreira | 1:50 | 30 min | Negociar ofertas e pedir promoção com dados |

<details><summary>m12-a01 — tópicos da ementa e prática</summary>

- Otimização de LinkedIn para Recrutadores - Palavras-chave de IA, SSI alto, headline impactante, seção "Sobre" com projetos
- Networking Estratégico - Conectar com recrutadores e tech leads, participar de comunidades de IA, engajamento consistente
- Marca Pessoal e Posicionamento - Compartilhar aprendizados, artigos técnicos, projetos, posicionar-se como especialista em IA aplicada

Config: `aulas/m12-a01.yaml` · saída: `m12-carreira/m12-a01-linkedin-networking-marca/`

</details>

<details><summary>m12-a02 — tópicos da ementa e prática</summary>

- Portfólio GitHub Profissional - Projetos deployados, READMEs detalhados, código limpo, demonstrações ao vivo acessíveis
- Expectativas por Nível (Junior → Principal) - O que cada nível exige: escopo, autonomia, impacto, liderança técnica

Config: `aulas/m12-a02.yaml` · saída: `m12-carreira/m12-a02-portfolio-e-niveis/`

</details>

<details><summary>m12-a03 — tópicos da ementa e prática</summary>

- Preparação para Entrevistas de RH - Metodologia STAR, storytelling efetivo, alinhamento cultural, responder pontos fracos estrategicamente
- Expectativas Salariais e Proposta de Valor - Pesquisa de mercado, como justificar seu valor, quando mencionar números

Config: `aulas/m12-a03.yaml` · saída: `m12-carreira/m12-a03-entrevistas-rh-e-salario/`

</details>

<details><summary>m12-a04 — tópicos da ementa e prática</summary>

- Live Coding e Problem Solving - Prática de coding interviews, pensar em voz alta, testar casos edge, otimização
- System Design para Sistemas de IA - Arquitetar sistemas completos, justificar trade-offs, escalabilidade, custos, resiliência
- Explicar Decisões Técnicas - Comunicar escolhas arquiteturais, por que escolheu determinado padrão, alternativas consideradas
- Perguntas Técnicas Específicas de IA - RAG vs fine-tuning, quando usar agents, otimização de custos, handling de failures

Config: `aulas/m12-a04.yaml` · saída: `m12-carreira/m12-a04-entrevistas-tecnicas-ia/`

</details>

<details><summary>m12-a05 — tópicos da ementa e prática</summary>

- Negociação Salarial Efetiva - Timing correto, âncoras salariais, múltiplas ofertas como leverage, pacote completo além do salário
- Pedido de Aumento/Promoção - Documentar impacto, timing estratégico, construir caso com métricas, apresentação profissional
- Técnicas de Diferenciação - Demonstrar projetos ao vivo, case studies de resultados, contributions open source, presença técnica

Config: `aulas/m12-a05.yaml` · saída: `m12-carreira/m12-a05-negociacao-e-diferenciacao/`

</details>
