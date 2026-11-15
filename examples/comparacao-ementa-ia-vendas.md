# Comparação: ementa de IA para vendas

Pesquisa feita em 14 de novembro de 2026 (America/Manaus). As URLs da tabela principal responderam HTTP 200 no momento da coleta (exceções sinalizadas). Carga horária e tópicos entram só quando a fonte os declara; quando não informa, está escrito “não encontrado”. Nada foi inventado.

A ementa nossa está em `/workspace/aula-ra/ementa-ia-vendas.txt` (PDF em `/workspace/aula-ra/entrega/ementa-ia-vendas.pdf`): **13 módulos, 104 horas sugeridas**, no formato lido pela skill `curso-a-partir-de-ementa`.

## O que não entrou como referência principal

- HubSpot Academy “AI for Sales”: a página oficial respondeu 200, mas o conteúdo não carregou sem JavaScript; a duração (~36 min) vem de terceiros e **não foi confirmada**.
- QI 360 (12 h): plataforma de terceiros com o mesmo texto do curso ESPM; usamos a ESPM como fonte.

## Referências verificadas

| # | Nome | Organização | URL verificada | Formato e carga | Tópicos declarados na fonte |
|---|---|---|---|---|---|
| 1 | IA Aplicada a Vendas | Senac São Paulo | https://www.sp.senac.br/cursos-livres/curso-de-inteligencia-artificial-aplicada-a-vendas | Presencial, **20 horas** | Ética, prompts, IA preditiva e generativa, prospecção e qualificação de leads, roteiros, negociação, pós-venda e fidelização. |
| 2 | IA Aplicada às Vendas: da Prospecção à Fidelização | Senac MS | https://www.ms.senac.br/Curso/Detalhe/127352 | Presencial, **8 horas** | Automação do funil, chatbots, e-mails personalizados, segmentação de leads, previsão de comportamento, BI, pós-venda. |
| 3 | IA: personalize estratégias de vendas com ChatGPT | Alura | https://www.alura.com.br/curso-online-inteligencia-artificial-estrategias-vendas-chatgpt | Online, **6 horas** | ChatGPT nas etapas de venda, dores e objeções, prompts de prospecção e proposta, playbooks, negociação. |
| 4 | Inteligência comercial e Gemini | Alura | https://www.alura.com.br/curso-online-inteligencia-comercial-gemini | Online, **2 horas** | Gems, dashboards, análises no Colab com Gemini sem código, Google Opal. |
| 5 | IA na Prática para Marketing, Vendas e Serviços | ESPM | https://www.espm.br/cursos/dynamic/inteligencia-artificial-aplicada-a-marketing-vendas-e-servicos/ | Online ao vivo, **12 horas** (declarado no texto) | Lead scoring, chatbots, previsão de vendas, atendimento, ferramentas, ética e privacidade. |
| 6 | Como vender rádio e digital | ACERT (Associação Cearense de Emissoras de Rádio e TV) | https://acert.org.br/media-training/ | Online, 8 encontros de 1h30 (**12 horas**) | Prospecção de anunciantes de rádio e TV, venda consultiva, objeções, carteira, mídia kit, plano de mídia, precificação de rádio e digital, IA para vendas e prospecção. |
| 7 | Curso de Vendas para Rádio e TV | Estúdio Escola Comunica (Sympla) | https://www.sympla.com.br/play/lgc/1220001 | Gravado; **carga não encontrada** | Prospecção, venda consultiva de mídia, pitch, negociação. Sem IA declarada. |

## O que só a nossa ementa tem (ou trata com profundidade que as outras não declaram)

- Comparação metódica de Gemini Enterprise (segurança conforme documentação oficial), Claude, ChatGPT e Grok, com teste lado a lado no mesmo pacote fictício.
- Fluxo completo de venda de mídia — tabela de preços, proposta, **PI**, grade, comprovação e faturamento — com regra de que preço e desconto vêm da tabela e do sistema, nunca do modelo. Só a ACERT trata venda de radiodifusão, sem PI nem pipeline.
- Audiência e alcance só com fonte, período e metodologia; CONAR e período eleitoral no pós-venda.
- Recorte de grupo de mídia, rádio e TV no Norte (AM, RO, RR, AC, AP). Anunciantes regionais e sazonalidade local.
- Pipelines em Python com o LLM só no passo de linguagem, registro de tokens e custo, cache por etapa, caso aula-ra e avaliação segura de skills no GitHub (módulo 12): nenhuma referência verificada declara esse método. Inclui conferência automática de PI contra proposta e grade.

## O que incorporamos das referências

| Referência | Onde entrou |
|---|---|
| ACERT: mídia kit, carteira e precificação de rádio e digital | Módulos 4, 5 e 6. |
| Senac SP: roteiros, negociação e pós-venda | Módulos 7 e 9. |
| Alura Gemini: Gems e análises sem código | Módulos 2 e 8. |
| ESPM: lead scoring e previsão de vendas | Módulo 8, com premissas explícitas. |

## O que deliberadamente não absorvemos

- Chatbots de venda automática ao consumidor final (não é o modelo de negócio).
- Persuasão assistida por IA sem limite ético.
