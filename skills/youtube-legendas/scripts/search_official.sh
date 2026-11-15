#!/usr/bin/env bash
# Lista candidatos no YouTube (sem baixar nada). Uso: search_official.sh "tema" [n]
# Depois confira o canal (verificado/oficial) com fetch_subs.py -> fonte.json.canal_verificado.
YTDLP="${YTDLP:-$(command -v yt-dlp || echo "$HOME/.local/bin/yt-dlp")}"
"$YTDLP" --flat-playlist --print "%(id)s | %(title)s | %(channel)s | %(duration)ss" "ytsearch${2:-15}:$1"
