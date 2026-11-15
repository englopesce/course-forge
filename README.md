# course-forge

Skills de agente da [L4Tec](https://l4tec.com) para transformar uma ementa num curso inteiro em vídeo, em português do Brasil: plano de estudo, roteiro didático, código de exemplo testado com exercícios, narração, trechos de vídeo com crédito, página HTML animada e vídeo MP4 em 16:9 e 9:16.

## Skills

| Skill | O que faz |
|---|---|
| [`aula-ra`](skills/aula-ra) | Orquestra a produção de uma mini-aula com um pipeline único (`scripts/pipeline.py aula.yaml`) |
| [`curso-a-partir-de-ementa`](skills/curso-a-partir-de-ementa) | Transforma uma ementa em módulos, aulas, `curso.json` e um `aula.yaml` por aula |
| [`plano-de-estudo`](skills/plano-de-estudo) | Planeja trilhas e sessões com vídeos verificados |
| [`youtube-legendas`](skills/youtube-legendas) | Baixa só a transcrição e os metadados de um vídeo do YouTube |
| [`roteiro-didatico-ptbr`](skills/roteiro-didatico-ptbr) | Escreve e valida o `roteiro.json` da aula |
| [`codigo-exemplo-aula`](skills/codigo-exemplo-aula) | Roda o repositório de exemplo, extrai os trechos de código e gera exercícios |
| [`narracao-tts-ptbr`](skills/narracao-tts-ptbr) | Gera a narração pt-BR, a legenda SRT e confere a voz por transcrição reversa |
| [`trechos-youtube-credito`](skills/trechos-youtube-credito) | Recorta trechos curtos com crédito gravado na imagem |
| [`pagina-html-gsap`](skills/pagina-html-gsap) | Gera a página HTML animada (GSAP), offline |
| [`video-hyperframes`](skills/video-hyperframes) | Renderiza o vídeo MP4 com HyperFrames e legendas gravadas |

Cada skill tem um `SKILL.md` com instruções para o agente e, quando aplicável, `scripts/`, `templates/` e `references/`.

## Exemplos

A pasta [`examples/`](examples) traz ementas, configurações de aula (`aula-*.yaml`) e os manifestos de dois cursos (`curso-ia-jornalismo` e `curso-eng-software-ia`).

## Instalação

Copie cada pasta de `skills/` para a pasta de skills do seu agente (por padrão `/home/box/agent-data/workflows/<slug>/`). A `aula-ra` encontra as skills irmãs pela pasta-mãe, por `$AULA_SKILLS_DIR` ou por `skills_dir` no YAML. Veja os detalhes em [`skills/aula-ra/README.md`](skills/aula-ra/README.md).

## Licença

O código deste repositório está sob a [Apache License 2.0](LICENSE). Use, modifique e redistribua à vontade, mantendo os avisos de copyright e o arquivo [`NOTICE`](NOTICE). A marca L4Tec não está incluída na licença.

Vídeos, narrações e trechos de terceiros gerados com estas skills não fazem parte deste repositório e seguem os direitos de seus autores.
