# Comparação: ementa de IA para recursos humanos

Pesquisa feita em 14 de novembro de 2026 (America/Manaus). As URLs da tabela principal responderam HTTP 200 no momento da coleta (exceções sinalizadas). Carga horária e tópicos entram só quando a fonte os declara; quando não informa, está escrito “não encontrado”. Nada foi inventado.

A ementa nossa está em `/workspace/aula-ra/ementa-ia-rh.txt` (PDF em `/workspace/aula-ra/entrega/ementa-ia-rh.pdf`): **13 módulos, 104 horas sugeridas**, no formato lido pela skill `curso-a-partir-de-ementa`.

## O que não entrou como referência principal

- Curso IEL-RS “Inteligência Artificial no RH” (10 h, set. 2025): página de evento antigo; usado só como contexto, não na tabela.
- FGV In Company “RH: criando organizações do futuro” (64 h): in company, sem turma aberta verificada; não usado.
- SHRM AI+HI: o PDF oficial não declara horas totais; a cifra de 18 h vista em busca **não foi confirmada** na fonte.

## Referências verificadas

| # | Nome | Organização | URL verificada | Formato e carga | Tópicos declarados na fonte |
|---|---|---|---|---|---|
| 1 | IA para decisões estratégicas em RH | Insper | https://ee.insper.edu.br/cursos/recursos-humanos/ia-para-decisoes-estrategicas-em-rh/ | Presencial, **18 horas** (30 nov.–1 dez. 2026) | Fundamentos, aplicações nos processos de RH, benefícios, limites e riscos, requisitos para implantação, priorização de investimentos, ética, regulação e governança. |
| 2 | Inteligência artificial aplicada ao RH | Integração Escola de Negócios | https://integracao.com.br/curso/inteligencia-artificial-aplicada-ao-rh/ | Presencial ou online ao vivo, **16 horas** | ChatGPT, Gemini e Copilot; Big Five; documentos automatizados; triagem e chatbot de candidatos; vieses algorítmicos; análise preditiva; PDI; dashboards; clima com análise de sentimento; turnover. |
| 3 | IA Aplicada aos Processos de RH | Senac São Paulo | https://www.sp.senac.br/cursos-livres/curso-de-inteligencia-artificial-aplicada-aos-processos-de-rh | Presencial, **20 horas** | Conceitos e ética, prompts, impactos na gestão de pessoas, uso em subsistemas de RH. |
| 4 | IA no RH: criando agentes com ChatGPT | Alura | https://www.alura.com.br/curso-online-inteligencia-artificial-rh-impactando-dia-a-dia-area-cuida-pessoas | Online, **8 horas** | Agente para avaliação de desempenho, instruções, simulador de devolutivas, dados, ética e LGPD. |
| 5 | IA para RH na Prática | IA no RH (curso independente) | https://www.ianorh.com/curso/ementa | Online, 12 módulos, **cerca de 10h40 de vídeo** | Fundamentos, prompts, checklist “posso colar isso na IA?”, recrutamento sem viés, T&D, desempenho (IA editora, nunca autora), people analytics, DP, Skills e agente, chatbot RAG, LGPD, viés, política, plano de 90 dias. |
| 6 | AI for HR: fundamentals | CIPD (Reino Unido) | https://shop.cipd.org/product?catalog=AI-for-Human-Resources-Fundamentals | Online, meio período: **3 h ao vivo + cerca de 6 h de estudo** | IA e GenAI, impacto no RH, riscos e oportunidades, política de IA, CVs gerados por IA. |
| 7 | SHRM AI+HI Specialty Credential | SHRM (EUA) | https://www.shrm.org/content/dam/en/shrm/credentials/specialty-credentials/ai-hi-specialty-credential-outline.pdf | 3 labs ao vivo, 5 podcasts, 3 verificações e capstone; **30 PDCs**; horas totais não encontradas | Letramento e prompts, IA responsável (viés, transparência, supervisão), ROI, gestão da mudança, capstone. |

## O que só a nossa ementa tem (ou trata com profundidade que as outras não declaram)

- Comparação metódica de Gemini Enterprise (segurança conforme documentação oficial), Claude, ChatGPT e Grok, com teste lado a lado no mesmo pacote fictício.
- Proteção explícita contra decisão automatizada sobre pessoas e menção ao direito de revisão (LGPD, art. 20) com teste de viés documentado.
- Rotinas de DP e eSocial com validação no sistema oficial, não no chat.
- Recorte de grupo de mídia, rádio e TV no Norte (AM, RO, RR, AC, AP). Equipes de externa, plantão e cinco praças, convenções coletivas diferentes.
- Pipelines em Python com o LLM só no passo de linguagem, registro de tokens e custo, cache por etapa, caso aula-ra e avaliação segura de skills no GitHub (módulo 12): nenhuma referência verificada declara esse método.

## O que incorporamos das referências

| Referência | Onde entrou |
|---|---|
| Integração/IA no RH: vieses e chatbot de triagem | Módulos 4 e 10. |
| IA no RH: “editora, nunca autora”, checklist de dados, RAG e plano de 90 dias | Módulos 3, 6, 11 e 13. |
| Insper/SHRM: priorização, ROI e gestão da mudança | Módulos 11 e 13. |
| CIPD: CVs gerados por IA | Módulo 4. |

## O que deliberadamente não absorvemos

- Testes de personalidade (Big Five) interpretados por IA como base de decisão.
- Análise preditiva de “sucesso de contratação” sem validação estatística e jurídica.
- Certificação internacional (SHRM/CIPD).
