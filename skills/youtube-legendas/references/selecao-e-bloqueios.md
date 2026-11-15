# Escolha do vídeo oficial e bloqueios do YouTube

## Escolher a fonte
1. Buscar: `scripts/search_official.sh "<tema> <produto>" 15`.
2. Preferir canal **oficial do fabricante** (ex.: Google Cloud, Google Cloud Tech, Google Workspace,
   Microsoft, AWS). Confirmar `canal_verificado: true` em `fonte.json`.
3. Preferir vídeo com **legenda enviada pelo canal** (`legenda_manual: true`), recente e de 3–10 min
   com demonstração na tela (bom para trechos).
4. Validar título/canal também por oEmbed se houver dúvida:
   `https://www.youtube.com/oembed?url=<URL>&format=json`.

## 429 / "Sign in to confirm you're not a bot"
- `ytdlp_retry.py` espera 120 s, 300 s e 600 s (ajuste por `YT_BACKOFF`) e tenta de novo.
- **Nunca** usar `--cookies` / `--cookies-from-browser` de conta pessoal — o script recusa.
- Reaproveitar arquivos já baixados (o script não repete download se `.info.json` e `.vtt` existem).
- Agrupar pedidos: um único `yt-dlp` com várias `--download-sections` em vez de várias chamadas.
- Idioma: use padrões com curinga (`en.*`), pois a legenda manual pode ter sufixo (`en-j3PyPqV-e1s`).
