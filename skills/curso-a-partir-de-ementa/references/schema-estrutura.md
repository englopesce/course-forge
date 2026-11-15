# Esquema do estrutura.json (escrito pelo agente)

```json
{
  "curso": {"titulo": "...", "resumo": "2–3 frases", "pre_requisitos": ["..."]},
  "modulos": [
    {
      "id": "m01", "slug": "fundamentos-ia-llms", "titulo": "Fundamentos de IA e LLMs", "objetivo": "1 frase",
      "aulas": [
        {
          "slug": "como-funcionam-llms",
          "titulo": "Como um LLM funciona: tokens, embeddings e attention",
          "tipo": "conceitual",
          "objetivos": ["Explicar ...", "Relacionar ..."],
          "topicos": ["m01.i006"],
          "duracao_video_s": 120,
          "duracao_estudo_min": 20,
          "pratica": "exercício/entrega fora do vídeo (opcional)",
          "pre_requisitos": ["opcional"],
          "busca_videos": ["3blue1brown attention transformers"],
          "documentacao": [{"titulo": "...", "url": "https://..."}]
        }
      ]
    }
  ]
}
```

- Id da aula = `<módulo>-a<NN>` pela posição (ex.: `m01-a03`); não escreva o id, ele é derivado (reordenar muda os ids).
- `topicos`: ids da `ementa.json` (`mNN.iNNN` item, `mNN.uNN` unidade inteira). Item coberto = ele, um ancestral ou a
  unidade citada; um item-pai também conta como coberto se todos os filhos estiverem cobertos.
- `tipo` ∈ conceitual | codigo | ferramenta | pratica | projeto | carreira. `por_tipo` no curso.yaml muda a config da aula
  por tipo (ex.: aulas de código com mais cenas e duração).
- `duracao_video_s`: 60–180 recomendado (aulas rápidas). `palavras_max` do roteiro é derivado (≈ 2 palavras/s).
