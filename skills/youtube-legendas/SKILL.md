---
name: youtube-legendas
description: Baixa só as legendas/transcrição e os metadados de um vídeo do YouTube (nunca o vídeo), escolhe vídeo de canal oficial e lida com bloqueio 429/robô com espera progressiva sem cookies. Use quando precisar da transcrição de um vídeo do YouTube como base de roteiro, aula, resumo ou checagem de fatos.
---

# youtube-legendas

Arquivos auxiliares relativos a esta pasta (instalada em `/home/box/agent-data/workflows/youtube-legendas/`).

1. Candidatos: `scripts/search_official.sh "<tema>" 15` → escolha canal oficial (ver `references/selecao-e-bloqueios.md`).
2. Legendas: `python3 scripts/fetch_subs.py <URL> <pasta> [--langs "pt.*,pt,en.*,en"]`
   → `transcript.txt`, `segments.json` (falas com tempo, para achar trechos), `fonte.json` (crédito).
   Baixa os metadados e depois UMA faixa (enviada pelo canal > automática original `-orig`), a partir do info.json
   (`--load-info-json`): pedir `pt.*,en.*` direto puxava dezenas de traduções automáticas e provocava 429.
   Legendas automáticas "rolando" são deduplicadas no `segments.json`.
3. Confira `fonte.json`: `canal_verificado`, `legenda_manual`. Use título, canal e URL no crédito.

Bloqueio 429/robô: `scripts/ytdlp_retry.py` espera e repete (120/300/600 s). Sem cookies, nunca.
Requisitos: `yt-dlp` (PATH ou `~/.local/bin`), Python 3. Node no PATH melhora a extração (`--js-runtimes node`).
