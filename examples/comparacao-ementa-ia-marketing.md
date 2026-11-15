# Comparação: ementa de IA para marketing

Pesquisa feita em 14 de novembro de 2026 (America/Manaus). As URLs da tabela principal responderam HTTP 200 no momento da coleta (exceções sinalizadas). Carga horária e tópicos entram só quando a fonte os declara; quando não informa, está escrito “não encontrado”. Nada foi inventado.

A ementa nossa está em `/workspace/aula-ra/ementa-ia-marketing.txt` (PDF em `/workspace/aula-ra/entrega/ementa-ia-marketing.pdf`): **13 módulos, 104 horas sugeridas**, no formato lido pela skill `curso-a-partir-de-ementa`.

## O que não entrou como referência principal

- Páginas da ESPM “IA aplicada ao Marketing Digital” e pós de 390 h: curl retornou **403**; a pós não entra na tabela. O curso presencial do Rio foi lido via fetch (sem horas declaradas).
- HubSpot Academy “AI for Marketers”: conteúdo não carregou; duração de terceiros não confirmada.
- Google Skillshop: não foi encontrado curso específico de IA para marketing.

## Referências verificadas

| # | Nome | Organização | URL verificada | Formato e carga | Tópicos declarados na fonte |
|---|---|---|---|---|---|
| 1 | Formação em Marketing Digital e Growth com IA | ESPM (Atualização SP) | https://atualizacaosp.espm.br/formacao-em-marketing-digital-e-growth-com-ia/ | Online ao vivo, **18 horas** (abr. 2026) | Growth, CRO, testes A/B, SEO com IA, Meta e Google Ads, e-mail, copywriting com IA, analytics. |
| 2 | Inteligência Artificial em Marketing Digital | ESPM (Rio de Janeiro) | https://www.espm.br/cursos/dynamic/inteligencia-artificial-em-marketing-digital-espm/ | Presencial, 4 aulas aos sábados; **horas não encontradas** | ML e DL, criação de conteúdo (ChatGPT, DALL-E), SEO com IA, automação, análise de dados, personalização, chatbots, recomendação. |
| 3 | Inteligência Artificial para Marketing Digital | Senac Santa Catarina | https://portal.sc.senac.br/curso/153685/inteligencia-artificial-para-marketing-digital | **20 horas** | Análise de dados, comportamento do consumidor, segmentação, personalização, ML, automação, cuidados éticos e legais. |
| 4 | IA: campanhas de Marketing Digital | Alura | https://www.alura.com.br/curso-online-inteligencia-artificial-campanhas-marketing-digital | Online, **8 horas** | SEO com IA, produção e impulsionamento de conteúdo, segmentação, automação, ética. |
| 5 | Aplicação prática de ferramentas de IA para publicidade digital | IAB Brasil | https://iabbrasil.com.br/cursos/aplicacao-pratica-de-ferramentas-de-ia-para-publicidade-digital/ | On-line ao vivo, 9h–12h; **total não encontrado** | IA generativa, ideação e produção, segmentação e otimização de mídia, modelos preditivos e mensuração. |
| 6 | IA Generativa para Agências de Publicidade | ABAP com Templo | https://www.abap.com.br/curso-ia-agencias-publicidade-associadas-abap/ | Gravado, **mais de 6 horas**, 4 módulos (exclusivo associadas) | Prompts, produtividade, criatividade (imagem e vídeo), agentes, ética e governança. |

### Fontes complementares e normas citadas

| Fonte | URL verificada | Uso na ementa |
|---|---|---|
| CONAR — Guia de influenciadores atualizado (2026, inclui IA) | https://www.conar.org.br/noticias/guia-de-marketing-e-publicidade-por-influenciadores-digitais | Princípios e módulos 6 e 10. |
| IAB Brasil — Guia de Uso da IA na Publicidade Digital 2026 e Manual de Conformidade | https://iabbrasil.com.br/guia-de-uso-da-inteligencia-artificial-na-publicidade-digital-2026/ | Leitura complementar recomendada. |
| Resolução TSE n. 23.732/2024 | https://www.tse.jus.br/legislacao/compilada/res/2024/resolucao-no-23-732-de-27-de-fevereiro-de-2024 (curl 403; texto lido via busca) | Módulo 10. |

## O que só a nossa ementa tem (ou trata com profundidade que as outras não declaram)

- Comparação metódica de Gemini Enterprise (segurança conforme documentação oficial), Claude, ChatGPT e Grok, com teste lado a lado no mesmo pacote fictício.
- Audiência TV e digital lida em conjunto, com fonte, período e metodologia — as referências tratam de digital/performance, não de audiência de TV e rádio.
- GEO (ser citado por motores de resposta) além de SEO; só a ESPM e a Alura tratam SEO com IA.
- Rotulagem de conteúdo sintético com CONAR (guia 2026) e TSE no mesmo módulo; nenhuma referência cita as regras.
- Pipelines em Python com o LLM só no passo de linguagem, registro de tokens e custo, cache por etapa, caso aula-ra e avaliação segura de skills no GitHub (módulo 12): nenhuma referência verificada declara esse método. Inclui versões 16:9/9:16 e legendas por ffmpeg.

## O que incorporamos das referências

| Referência | Onde entrou |
|---|---|
| ESPM Growth: testes A/B, CRO e analytics | Módulos 4 e 9. |
| IAB: ideação, otimização de mídia e mensuração | Módulos 6, 7 e 9. |
| ABAP: biblioteca de prompts e agentes | Módulos 3 e 11. |
| Senac SC: cuidados éticos e legais | Módulo 10. |

## O que deliberadamente não absorvemos

- Gestão de tráfego pago em profundidade (Google/Meta Ads), que é outra formação.
- Machine learning para recomendação personalizada.
