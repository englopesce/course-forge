# Política de trechos do vídeo original (uso interno/educacional)

1. **Só o necessário.** Trechos curtos (4–8 s, no máximo ~3 por aula), escolhidos pela
   transcrição com tempo (`segments.json`) para mostrar o produto/demonstração da cena.
   Baixar **apenas as seções** (`--download-sections "*ini-fim"`), ≤720p; nunca o vídeo inteiro.
2. **Crédito na tela durante todo o trecho:** "Trecho do vídeo original · <canal> (YouTube)" +
   "“<título>” · youtu.be/<id>?t=<s>" (gravado na imagem pelo `cut_clips.py`). Na página HTML,
   repetir o crédito ao lado do vídeo com link para o original no tempo exato.
3. **Áudio original** toca com a narração em pausa; legenda pt-BR fiel à fala (escrita no roteiro).
4. **Uso interno.** Treinamento da empresa, sem publicação aberta (YouTube, redes, site) sem
   autorização do detentor. Não remover marcas d'água/elementos do original, não alterar o sentido.
5. **Sem cookies de conta**; respeitar 429/verificação com espera (ver `ytdlp_retry.py`).
6. Guardar `clips.json` (origem, tempos, link) junto da aula para auditoria.
