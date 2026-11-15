# Comparação: ementa de IA para financeiro e contábil

Pesquisa feita em 14 de novembro de 2026 (America/Manaus). As URLs da tabela principal responderam HTTP 200 no momento da coleta. Carga horária, preço e tópicos entram aqui só quando a fonte os declara; quando a página não informa horas, está escrito “não encontrado”. Nada foi inventado para preencher lacuna de fonte.

A ementa nossa está em `/workspace/aula-ra/ementa-ia-financeiro-contabil.txt` (e em PDF em `/workspace/aula-ra/entrega/ementa-ia-financeiro-contabil.pdf`): **13 módulos, 104 horas sugeridas, 190 itens** no formato lido pela skill `curso-a-partir-de-ementa`. Destina-se a profissionais e gestores de contabilidade, controladoria, FP&A, tesouraria, fiscal, contas a pagar e a receber e auditoria interna da Rede Amazônica, sem formar programadores.

## Como a pesquisa foi feita

Busca e leitura das páginas de FIPECAFI, IBEF-Rio, BLB Escola de Negócios, ACCA, ICAEW, AICPA & CIMA, CFA Institute, CFC, IBRACON, Insper e menções a cursos da FGV.

O que não entrou como referência principal, e por quê:

- **CFC / CRC-RN, “IA para Contadores e Profissionais de Finanças”.** Há notícia oficial do lançamento, em setembro de 2025, no 14º Encontro Nacional da Mulher Contabilista (https://cfc.org.br/noticias/painel-sobre-inteligencia-artificial-marca-lancamento-de-curso-inedito-para-contadores-no-14o-enmc/, HTTP 200). Nesta busca **não foram encontradas** ementa pública, carga horária nem lista de módulos. Entra abaixo como fonte complementar, não como referência de ementa.
- **IBRACON.** A vitrine https://www.ibracon.com.br/vitrine-ibracon/ (HTTP 200) lista um curso “Ferramentas digitais, automação e IA”. A URL específica do produto de data analytics consultada nesta busca retornou **HTTP 404**. Sem ementa pública verificável, não entra na tabela principal.
- **FGV, “IA Generativa na Gestão Financeira para Empreendedores” (16 horas).** A carga e o nome aparecem em blog de terceiro (Treasy). **Não foi encontrada página oficial da FGV** com essa ementa nesta busca. Trata-se como menção não verificada na origem; não entra na tabela principal.
- **Insper, “IA Aplicada aos Negócios”.** Curso geral de negócios, **32 horas** (https://ee.insper.edu.br/cursos/tecnologia-data-science/ia-aplicada-aos-negocios/, HTTP 200), não específico de financeiro e contábil. Entra só como fonte complementar.

## Referências verificadas (cursos e programas)

| # | Nome | Organização | URL verificada | Formato e carga | Tópicos declarados na fonte |
|---|------|-------------|----------------|------------------|------------------------------|
| 1 | Inteligência Artificial Aplicada à Contabilidade e Finanças | FIPECAFI | https://www.fipecafi.org/Curso-Edux/1322 — matriz: https://fipecafi.org/Matriz/matriz_3579_ee985aa3.pdf | EAD ao vivo, 6 sessões, **18 horas**. Preço declarado: R$ 1.590. Sem exigência de programar; Excel é requisito. Trabalha com base contábil fictícia. | (1) IA e o novo profissional; (2) prompts profissionais e biblioteca de prompts; (3) produtividade e comunicação executiva; (4) análise e decisão, inclusive padrões, inconsistências e cenários; (5) redesenho de processos com human in the loop, indicadores e casos de uso; (6) governança, LGPD, propriedade intelectual, alucinação e políticas. Projeto final: plano de aplicação de IA. |
| 2 | IA Aplicada à Contabilidade e Finanças (On-Line) | IBEF-Rio | https://agenda.ibefrio.org.br/curso/inteligencia-artificial-aplicada-a-contabilidade-e-financas-on-line/ | On-line, **8 horas**. | Fundamentos e aprendizado de máquina; RPA, lançamentos automatizados, conciliação bancária e demonstrações; integração com ERP; painéis de BI; ML para comportamento de cliente e inadimplência; modelos de red flag; gestão da mudança, ética e ROI; roadmap. |
| 3 | IA na Prática para Contabilidade, Tributário e Finanças – EAD | BLB Escola de Negócios | https://blbescoladenegocios.com.br/curso/inteligencia-artificial-na-pratica-para-contabilidade-tributario-e-financas-ead/ | EAD, 2 sessões de 4 horas, **8 horas**. Preço declarado: R$ 945. Reconhecido pelo CFC para PEPC. Centrado no Claude. | ChatGPT versus Claude versus Gemini; janela de contexto; alucinação e LGPD; classificação de despesas; extração estruturada de notas e recibos; indicadores de balanço; conformidade interestadual de ICMS/IPI; conciliação e auditoria preliminar; agentes; o que não delegar. A página afirma “menor taxa de alucinação” do Claude: é alegação do provedor, **não repetida como fato** nesta comparação nem na nossa ementa. |
| 4 | Certificate in Artificial Intelligence for Finance Professionals | ACCA | https://www.accaglobal.com/gb/en/qualifications/glance/certificate-in-artificial-intelligence-for-finance-professionals/certificate-details.html e https://www.accaglobal.com/learning-and-events/acca-learning/certificate-in-artificial-intelligence-for-finance-professionals.html | 10 unidades no próprio ritmo e avaliação de 1 hora. Preço declarado: £ 230 para associados, £ 310 para o público. **Carga horária total: não encontrada.** | História; IA no financeiro hoje; estratégia; implantação e qualidade de dados; riscos; governança de dados (EU AI Act, ISO 42001, GDPR, IESBA); saídas de IA generativa (sycophancy, vieses); engenharia de prompts; armadilhas analíticas (overfitting, correlação versus causalidade); IA agêntica e o modelo das três linhas. |
| 5 | GenAI Accelerator | ICAEW | https://www.icaew.com/learning-and-development/icaew-genai-accelerator-programme | 8 cursos em e-learning. **Carga horária total: não encontrada.** | Fundamentos; operações financeiras (automação, conformidade, detecção de risco, previsão); reporte corporativo e conformidade tributária (auditoria, ESG); estratégia e risco; governança e conselho; prática profissional; setor; implementação e gestão da mudança. |
| 6 | Core Concepts of AI for Accounting Professionals; AI Accelerator Program; Hands-On Generative AI Bootcamp for CPAs | AICPA & CIMA | https://www.aicpa-cima.com/cpe-learning/course/core-concepts-of-artificial-intelligence-for-accounting-professionals — https://www.aicpa-cima.com/cpe-learning/bundle/ai-accelerator-program-bun — https://www.aicpa-cima.com/cpe-learning/conference/hands-on-generative-ai-bootcamp-for-cpas-practical-skills-you-can-use-immediately | Core Concepts: **2,5 créditos CPE**, preço declarado US$ 79–95. Accelerator: três níveis (Operational, Transitional, Strategic); a página do nível Operational declara **12 créditos CPE**. Bootcamp: **3 créditos CPE**, ao vivo on-line em 16 de dezembro de 2026. | Core Concepts: conceitos centrais de IA para profissionais de contabilidade. Bootcamp: ChatGPT, Copilot, Claude e Gemini; revisão de documentos; análise de dados; agentes; governança; citação e validação. |
| 7 | Practical Skills Module “Python, Data Science & AI” (Level II) | CFA Institute | https://www.cfainstitute.org/programs/cfa-program/candidate-resources/practical-skills-modules/python-data-science-and-ai | Módulo prático do programa CFA, **10 a 20 horas**. | Jupyter, pandas, demonstrações financeiras SimFin, previsão de lucro por ação com regressão, random forest, XGBoost e rede neural, PLN (sentimento e nuvem de palavras). Usado aqui como comparável de Python, não como ementa de IA generativa para o dia a dia contábil. |

### Fontes complementares (não são ementas completas e específicas de “IA para financeiro e contábil”, mas informaram o recorte)

| Nome | Organização | URL verificada | O que foi aproveitado | Limite da fonte |
|------|-------------|----------------|------------------------|-----------------|
| Painel e lançamento de curso inédito para contadores | CFC | https://cfc.org.br/noticias/painel-sobre-inteligencia-artificial-marca-lancamento-de-curso-inedito-para-contadores-no-14o-enmc/ | Confirma demanda institucional brasileira por formação de IA para contadores (lançamento em set. 2025, 14º ENMC). | Sem ementa, módulos ou carga pública nesta busca. |
| IA Aplicada aos Negócios | Insper | https://ee.insper.edu.br/cursos/tecnologia-data-science/ia-aplicada-aos-negocios/ | Curso geral de **32 horas** sobre IA em negócios. Útil como contraste de carga e de público amplo. | Não é recorte financeiro-contábil; não entra na tabela de cobertura. |
| Vitrine de cursos | IBRACON | https://www.ibracon.com.br/vitrine-ibracon/ | Há oferta de “Ferramentas digitais, automação e IA” no catálogo da entidade de auditoria. | Produto específico consultado retornou 404; sem ementa verificável. |
| Menção a “IA Generativa na Gestão Financeira para Empreendedores” (16 h) | Atribuída à FGV em blog de terceiro (Treasy) | Página oficial da FGV: **não encontrada** nesta busca | Só registra que circula a menção a um curso de 16 horas. | Sem URL oficial verificada; não usada como fonte de tópicos nem de carga. |

## Cobertura de temas

Legenda: **sim** = a fonte declara o tema com clareza; **parcial** = aparece de forma breve, genérica ou só num recorte (por exemplo, tributário sem SPED ou reforma brasileira); **não** = não foi encontrado na descrição pública consultada. “Nossa ementa” é a de `/workspace/aula-ra/ementa-ia-financeiro-contabil.txt`. Nas colunas da AICPA, o Bootcamp e o Core Concepts foram lidos em conjunto.

| Tema | Nossa | FIPECAFI | IBEF-Rio | BLB | ACCA | ICAEW | AICPA | CFA PSM |
|------|:-----:|:--------:|:--------:|:---:|:----:|:-----:|:-----:|:-------:|
| Fundamentos de IA, limites e alucinação | sim | sim | sim | sim | sim | sim | sim | parcial (ciência de dados, não o recorte de LLM) |
| Comparar Claude, Gemini, ChatGPT e Grok | sim | não | não | parcial (ChatGPT, Claude e Gemini; sem Grok) | não | não | parcial (ChatGPT, Copilot, Claude e Gemini; sem Grok) | não |
| Gemini Enterprise, segurança e Workspace | sim | não | não | não | não | não | não | não |
| Prompts com método e biblioteca | sim | sim | não encontrado | parcial | sim | não encontrado | parcial (Bootcamp prático) | não |
| Conciliação bancária e rotinas contábeis | sim | parcial (casos de uso e processos, sem detalhar conciliação) | sim | sim | não encontrado | parcial (operações financeiras) | parcial (revisão de documentos) | não |
| Extração de NF-e/XML e documentos fiscais | sim | não encontrado | não encontrado | sim (notas e recibos) | não | não encontrado | parcial (revisão de documentos) | não |
| SPED (ECD, ECF, EFD) e obrigações acessórias | sim | não | não | não | não | não | não | não |
| Reforma tributária (EC 132/2023, CBS/IBS) | sim | não | não | parcial (ICMS/IPI interestadual; reforma não declarada) | não | parcial (tax compliance, recorte internacional) | não | não |
| Auditoria, anomalias, red flags e fraude | sim | parcial (padrões e inconsistências) | sim | sim (auditoria preliminar) | parcial (riscos) | sim | parcial | não |
| Relatórios à diretoria, DRE e comunicação | sim | sim (comunicação executiva) | parcial (demonstrações e BI) | parcial (indicadores de balanço) | não encontrado | sim (reporte e conselho) | não encontrado | não |
| Orçamento, FP&A e previsão de caixa | sim | parcial (cenários) | não encontrado | não | não encontrado | sim (forecasting) | não encontrado | sim (previsão de EPS com ML) |
| Dados, planilhas, BI e armadilhas analíticas | sim | parcial | sim (ERP e BI) | não encontrado | sim (overfitting, correlação) | parcial | parcial (análise de dados) | sim (pandas, Jupyter) |
| Ética, LGPD/privacidade e governança | sim (LGPD, Código de Ética do Contador, política da área) | sim (LGPD, PI, políticas) | sim (ética) | sim (LGPD) | sim (GDPR, EU AI Act, ISO 42001, IESBA) | sim (governança e conselho) | sim (governança) | não encontrado |
| Agentes, automação e human in the loop | sim | sim | sim (RPA e roadmap) | sim | sim (IA agêntica e três linhas) | sim | sim | não |
| Pipelines em Python: o LLM só quando for necessário | sim (módulo 12) | não | não | não | não | não | não | parcial (Python e ML; não declara a regra do LLM só no passo de linguagem) |
| Registro de tokens/custo e cache por etapa | sim | não | não | não | não | não | não | não |
| Skills reutilizáveis e avaliação segura no GitHub | sim | não | não | não | não | não | não | não |
| Recorte de empresa de mídia (PI, anunciantes, praças) | sim | não (base fictícia genérica) | não | não | não | não | não | não (SimFin, recorte de mercado) |
| Projeto final aplicado à própria área | sim | sim (plano de aplicação) | parcial (roadmap) | não encontrado | avaliação de certificado | parcial (implementação) | não encontrado | exercício do módulo CFA |
| Treinar modelos de ML (random forest, XGBoost, redes) | não (fora do recorte) | não | parcial (ML para inadimplência; treino não detalhado) | não | não | não | não | sim |

## O que só a nossa ementa tem (ou trata com profundidade que as outras não declaram)

- **Comparação metódica dos quatro assistentes, com Gemini Enterprise e Grok.** BLB e o Bootcamp da AICPA comparam ChatGPT, Claude e Gemini (a AICPA inclui ainda o Copilot). Nenhuma das ementas públicas encontradas declara Grok nem a segurança do Gemini Enterprise com o cuidado de apontar só o que a documentação oficial descreve (criptografia, controles e opções administrativas, a conferir no contrato da empresa).
- **SPED e reforma tributária brasileira (CBS/IBS), com a norma oficial como fonte.** O tributário da BLB cobre ICMS/IPI interestadual; o ICAEW trata de tax compliance no recorte internacional. Nenhum dos cursos verificados declara SPED (ECD, ECF, EFD) nem a Emenda Constitucional 132/2023 e o período de transição. A nossa ementa trata o texto do modelo como pista, nunca como fonte.
- **Pipelines em Python em que o LLM só entra quando a linguagem ou o julgamento são necessários.** O comparável de Python é o módulo do CFA Institute (10 a 20 horas), voltado a Jupyter, pandas e treino de modelos de previsão — formação de ciência de dados, não o método “conta e soma no código; modelo só no texto”. Nenhuma referência declara registro de tokens e custo, cache por etapa, o caso interno aula-ra nem a avaliação segura de skills no GitHub.
- **Recorte de grupo de mídia e TV no Norte do Brasil.** Faturamento de publicidade, pedido de inserção, conciliação de anunciantes, intercompany entre empresas do grupo e previsão de caixa com sazonalidade de datas comerciais, eleições e eventos esportivos. As demais ementas usam base fictícia genérica, recorte internacional ou dados SimFin.
- **Carga e profundidade para quem opera o processo, não só uma introdução.** FIPECAFI tem 18 horas; IBEF-Rio e BLB têm 8 horas cada; os programas da ACCA, da ICAEW e da AICPA ou não declaram horas totais ou se organizam em créditos CPE curtos. A nossa ementa sugere 104 horas em 13 módulos, com projeto final aplicado e trilha de conferência de cada número.

## Lacunas das referências que valia incorporar — e o que mudou na nossa ementa

| O que a referência traz e valia absorver | Onde entrou na nossa ementa |
|------------------------------------------|------------------------------|
| A FIPECAFI estrutura **biblioteca de prompts**, **human in the loop**, **governança, LGPD e políticas**, e fecha com um **plano de aplicação**. | Módulos 3, 10, 11 e 13. |
| O IBEF-Rio separa **RPA e regras** de aprendizado de máquina, e declara **conciliação bancária**, **ERP/BI**, **red flags**, **ética, ROI e roadmap**. | Módulos 1, 4, 6, 9 e 11. A distinção RPA versus IA generativa abre o módulo 1. |
| A BLB compara **ChatGPT, Claude e Gemini**, trata **extração estruturada de notas**, **conciliação e auditoria preliminar**, **agentes** e **o que não delegar**. | Módulos 2, 4, 6 e 11. Não absorvemos a alegação de “menor taxa de alucinação” do Claude. |
| A ACCA trata **armadilhas analíticas** (overfitting, correlação versus causalidade), **sycophancy e vieses**, **IA agêntica** e o **modelo das três linhas**, além de referenciais de governança (EU AI Act, ISO 42001, GDPR, IESBA). | Armadilhas no módulo 9 e no 8; vieses e adulação no módulo 1 e no 10; agentes no 11; governança no 10, no recorte brasileiro (LGPD e Código de Ética do Contador), com menção a conferir referenciais internacionais quando couber — sem transformar o curso num certificado ACCA. |
| O ICAEW cobre **operações, forecasting, reporte, auditoria, ESG, conselho e gestão da mudança**. | Módulos 7, 8, 6 e 10. ESG não virou módulo próprio; entra só quando o relatório à diretoria o exigir, com dado da origem, não gerado pelo modelo. |
| A AICPA, no Bootcamp, insiste em **citação, validação** e uso prático de **vários assistentes**, inclusive Copilot. | Conferência de fonte e de número nos módulos 3, 7 e 13. Copilot pode aparecer como ferramenta do pacote Office já existente na empresa, sem ocupar o lugar do Gemini Enterprise contratado. |
| O CFA Institute mostra que **Python, notebooks e previsão com dados** já são formação reconhecida no financeiro. | Módulo 12 (notebooks para quem não programa, conferência de código) e módulo 8 (modelos simples primeiro, incerteza explícita). Não absorvemos o treino de random forest, XGBoost ou redes neurais. |

## O que deliberadamente não absorvemos

- **Treinar modelos de aprendizado de máquina** (random forest, XGBoost, redes neurais do módulo do CFA). O recorte é usar IA com método na rotina, não formar cientistas de dados.
- **Certificação profissional internacional e prova** (certificado ACCA, créditos CPE da AICPA, programa CFA). A ementa é formação interna da Rede Amazônica.
- **A alegação de “menor taxa de alucinação” do Claude**, publicada na página da BLB. É reivindicação de provedor, não fato verificado aqui.
- **Parecer tributário ou jurídico gerado por IA.** O módulo 5 ensina a estudar a norma com o texto oficial carregado no assistente; a opinião continua do tributarista responsável.
- **Curso longo de quem vai construir sistemas financeiros.** O módulo 12 ensina o bastante para desenhar, acompanhar e auditar um pipeline, não para substituir a TI.

## Síntese

Há oferta real e recente de IA para financeiro e contábil, no Brasil (FIPECAFI, IBEF-Rio, BLB) e no exterior (ACCA, ICAEW, AICPA & CIMA, CFA Institute), sobretudo em fundamentos, prompts, ética, governança, conciliação introdutória e, no caso do CFA, ciência de dados com Python. Os cursos brasileiros verificados são curtos (8 ou 18 horas). Nenhum deles, nas ementas públicas encontradas, reúne os quatro assistentes com Gemini Enterprise, o SPED e a reforma tributária (CBS/IBS) com disciplina de fonte oficial, o recorte de um grupo de mídia, e um método explícito de pipeline em que o modelo só entra quando a linguagem é necessária — com conferência de cada número, controle de custo e avaliação segura de skills no GitHub. Essa é a diferença central da nossa ementa, desenhada para o financeiro e a contabilidade da Rede Amazônica e no formato que a skill `curso-a-partir-de-ementa` já consegue ler.
