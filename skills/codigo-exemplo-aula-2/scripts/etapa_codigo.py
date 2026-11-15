#!/usr/bin/env python3
"""Etapa "codigo" da aula técnica: roda o repositório de exemplo, extrai o código das cenas e gera os exercícios.

Uso: python etapa_codigo.py --config aula.yaml --roteiro roteiro.json --saida <pasta_saida> --trabalho <pasta_trabalho>

Config (aula.yaml):
  exemplo:
    dir: exemplos/mcp-server-ts          # relativo ao yaml; repositório executável da aula
    checagem:                            # comandos rodados numa CÓPIA LIMPA (sem node_modules/dist) do repositório
      - {nome: instalar, cmd: npm install --no-audit --no-fund}
      - {nome: build, cmd: npm run build}
      - {nome: teste, cmd: npm test, timeout: 180}
    ignorar: [node_modules, dist, .git]  # não copiados (padrão)
Roteiro (roteiro.json):
  cenas[].codigo = {"arquivo": "src/server.ts", "linhas": "1-24", "destaques": [{"linhas": "8-14", "nota": "..."}],
                    "linguagem": "ts" (opcional, pelo sufixo), "titulo": "src/server.ts" (opcional)}
  exercicios = [{"id": "ex1", "titulo": "...", "enunciado": "...", "dica": "...", "arquivo": "src/x.ts",
                 "checagem": "nome-de-um-comando-da-checagem"}]
Saídas: <saida>/codigo/snippets.json (linhas já realçadas), <saida>/codigo/checagem.json (+ logs),
        <saida>/exemplo/ (cópia do repositório, sem node_modules) e <saida>/exercicios.md.
Sai com código 1 se um comando falhar, se o código citado não existir ou se um exercício citar checagem inexistente/falha.
"""
import argparse, json, os, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from realce import realcar, lang_of  # noqa: E402

IGNORAR = ["node_modules", "dist", "build", ".git", ".turbo", "coverage"]


def faixa(s, total=None):
    if isinstance(s, int): return s, s
    a, _, b = str(s).partition("-")
    a = int(a); b = int(b) if b else a
    return a, b


def copiar(src, dst, ignorar):
    if os.path.exists(dst): shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(*ignorar))


def main():
    import yaml
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True); ap.add_argument("--roteiro", required=True)
    ap.add_argument("--saida", required=True); ap.add_argument("--trabalho", required=True)
    ap.add_argument("--sem-checagem", action="store_true", help="só extrai o código (não roda os comandos)")
    a = ap.parse_args()
    cfg = yaml.safe_load(open(a.config, encoding="utf-8")) or {}
    base = os.path.dirname(os.path.abspath(a.config))
    rot = json.load(open(a.roteiro, encoding="utf-8"))
    ex = cfg.get("exemplo") or {}
    out_dir = os.path.join(a.saida, "codigo"); os.makedirs(out_dir, exist_ok=True)
    erros, res = [], {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "comandos": [], "ok": True}
    repo = None
    if ex.get("dir"):
        repo = ex["dir"] if os.path.isabs(ex["dir"]) else os.path.normpath(os.path.join(base, ex["dir"]))
        if not os.path.isdir(repo): raise SystemExit(f"exemplo.dir não existe: {repo}")
        ign = ex.get("ignorar") or IGNORAR
        res["repositorio"] = repo
        # 1) roda a checagem numa cópia limpa
        if not a.sem_checagem and ex.get("checagem"):
            run_dir = os.path.join(a.trabalho, "exemplo-run"); copiar(repo, run_dir, ign)
            env = {**os.environ, "CI": "1", "NO_COLOR": "1", "npm_config_update_notifier": "false"}
            for i, c in enumerate(ex["checagem"]):
                c = c if isinstance(c, dict) else {"nome": f"cmd{i+1}", "cmd": c}
                t0 = time.time(); log = os.path.join(out_dir, f"log_{i+1:02d}_{c['nome']}.txt")
                try:
                    p = subprocess.run(c["cmd"], shell=True, cwd=run_dir, capture_output=True, text=True,
                                       timeout=c.get("timeout", 300), env=env)
                    rc, saida = p.returncode, p.stdout + p.stderr
                except subprocess.TimeoutExpired as e:
                    rc, saida = 124, f"TIMEOUT após {c.get('timeout', 300)} s\n{e.stdout or ''}{e.stderr or ''}"
                open(log, "w", encoding="utf-8").write(f"$ {c['cmd']}\n{saida}")
                linhas = saida.strip().splitlines()
                item = {"nome": c["nome"], "cmd": c["cmd"], "codigo": rc, "ok": rc == 0, "segundos": round(time.time() - t0, 1),
                        "log": os.path.relpath(log, a.saida), "fim_saida": linhas[-12:]}
                res["comandos"].append(item)
                print(f"[codigo] {'OK ' if rc == 0 else 'FALHOU'} {c['nome']}: {c['cmd']} ({item['segundos']} s)")
                if rc != 0:
                    erros.append(f"comando '{c['nome']}' falhou (código {rc}); ver {log}")
                    print("\n".join(linhas[-25:])); break
        # 2) cópia do repositório para a entrega
        copiar(repo, os.path.join(a.saida, "exemplo"), ign)
    # 3) código das cenas
    snippets = {}
    for c in rot.get("cenas", []):
        cd = c.get("codigo")
        if not cd: continue
        if not repo: erros.append(f"cena {c['id']}: tem 'codigo' mas a config não tem exemplo.dir"); continue
        arq = os.path.join(repo, cd["arquivo"])
        if not os.path.isfile(arq): erros.append(f"cena {c['id']}: arquivo {cd['arquivo']} não existe no exemplo"); continue
        texto = open(arq, encoding="utf-8").read().rstrip("\n").split("\n")
        i0, i1 = faixa(cd.get("linhas", f"1-{len(texto)}"))
        if not (1 <= i0 <= i1 <= len(texto)):
            erros.append(f"cena {c['id']}: linhas {cd.get('linhas')} fora do arquivo ({len(texto)} linhas)"); continue
        lg = cd.get("linguagem") or lang_of(cd["arquivo"])
        # realça o arquivo inteiro (estado de comentários de bloco) e recorta
        hl = realcar("\n".join(texto), lg)[i0 - 1:i1]
        dest = []
        for d in cd.get("destaques", []):
            d = d if isinstance(d, dict) else {"linhas": d}
            a0, a1 = faixa(d["linhas"])
            if not (i0 <= a0 <= a1 <= i1): erros.append(f"cena {c['id']}: destaque {d['linhas']} fora de {i0}-{i1}"); continue
            dest.append({"de": a0, "ate": a1, "nota": d.get("nota", "")})
        maxc = max(len(x) for x in texto[i0 - 1:i1])
        if i1 - i0 + 1 > 22: print(f"[codigo] AVISO cena {c['id']}: {i1 - i0 + 1} linhas (máx. recomendado 22 no vídeo)")
        if maxc > 72: print(f"[codigo] AVISO cena {c['id']}: linha com {maxc} caracteres (fonte vai diminuir; ideal ≤ 72)")
        snippets[c["id"]] = {"arquivo": cd["arquivo"], "titulo": cd.get("titulo", cd["arquivo"]), "linguagem": lg,
                             "inicio": i0, "fim": i1, "max_chars": maxc, "texto": texto[i0 - 1:i1], "html": hl, "destaques": dest}
    json.dump(snippets, open(os.path.join(out_dir, "snippets.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # 4) exercícios
    exs = rot.get("exercicios", [])
    nomes = {c["nome"]: c for c in res["comandos"]}
    todos = {(c if isinstance(c, dict) else {"nome": ""})["nome"] for c in ex.get("checagem", [])}
    if exs:
        md = [f"# Exercícios — {rot['titulo']}", ""]
        if repo: md += ["Repositório de exemplo: pasta `exemplo/` (ao lado deste arquivo). Rode `npm install` antes.", ""]
        for k, e in enumerate(exs, 1):
            md += [f"## {k}. {e['titulo']}", "", e["enunciado"], ""]
            if e.get("arquivo"): md += [f"- Arquivo: `exemplo/{e['arquivo']}`"]
            if e.get("dica"): md += [f"- Dica: {e['dica']}"]
            ck = e.get("checagem")
            if ck:
                if ck not in todos: erros.append(f"exercício {e.get('id', k)}: checagem '{ck}' não existe em exemplo.checagem")
                elif ck in nomes and not nomes[ck]["ok"]: erros.append(f"exercício {e.get('id', k)}: checagem '{ck}' falhou")
                cmd = next(c for c in ex["checagem"] if isinstance(c, dict) and c["nome"] == ck)["cmd"] if ck in todos else "?"
                st = "verificado automaticamente (passou)" if ck in nomes and nomes[ck]["ok"] else "não rodado"
                md += [f"- Como conferir: `{cmd}` — {st}"]
            md += [""]
        open(os.path.join(a.saida, "exercicios.md"), "w", encoding="utf-8").write("\n".join(md))
    res["snippets"] = len(snippets); res["exercicios"] = len(exs); res["erros"] = erros; res["ok"] = not erros
    json.dump(res, open(os.path.join(out_dir, "checagem.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"[codigo] {len(res['comandos'])} comando(s), {len(snippets)} cena(s) com código, {len(exs)} exercício(s)")
    for e in erros: print("ERRO:", e)
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main()
