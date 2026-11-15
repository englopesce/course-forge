#!/usr/bin/env python3
"""Executa o yt-dlp com espera progressiva quando o YouTube responde 429 / verificação de robô.
Nunca usa cookies de conta. Importável (run_ytdlp) ou via linha de comando:
  python ytdlp_retry.py -- <argumentos do yt-dlp>
Variáveis: YTDLP (caminho do binário), YT_BACKOFF="120,300,600" (segundos entre tentativas),
YT_EJS_REMOTO=0 desliga o 2º recurso abaixo.
Desafio JS ("n challenge solving failed" / 403 nos fragmentos): tenta de novo, na hora, com
`--remote-components ejs:github` (script oficial de solução do yt-dlp baixado do GitHub; sem cookies).
Watchdog de travamento (0% CPU e arquivos parados, inclusive sem `.part`): YT_HANG_SECS (padrão 90;
0 desliga), YT_HANG_TENTATIVAS (padrão 4), YT_HANG_BACKOFF (padrão 15,30,60), YT_HANG_POLL (padrão 2).
Se não houver progresso, encerra só aquele yt-dlp/ffmpeg (não o pipeline) e tenta de novo, passando
a usar ejs:github. Baixa só o que os argumentos pedirem (nas aulas: --download-sections).
"""
import os, shutil, signal, subprocess, sys, tempfile, time

BLOCK_MARKERS = ("HTTP Error 429", "Too Many Requests", "confirm you", "not a bot")
EJS_MARKERS = ("n challenge solving failed", "403 Forbidden", "Requested format is not available")


class HangError(Exception):
    """yt-dlp/ffmpeg ficou sem progresso (CPU e arquivos parados) pelo prazo do watchdog."""

    def __init__(self, seconds, output=""):
        super().__init__(f"sem progresso há {seconds}s")
        self.seconds = seconds
        self.output = output


def ytdlp_bin():
    return os.environ.get("YTDLP") or shutil.which("yt-dlp") or os.path.expanduser("~/.local/bin/yt-dlp")


def _ints(env, default):
    raw = os.environ.get(env, default)
    return [int(x) for x in raw.split(",") if str(x).strip()]


def _watch_dirs(args):
    dirs = []
    i = 0
    while i < len(args):
        a = args[i]
        path = None
        if a in ("-o", "--output", "-P", "--paths", "--output-template") and i + 1 < len(args):
            path = args[i + 1]
            i += 2
        elif a.startswith("-o") and len(a) > 2:
            path = a[2:]
            i += 1
        else:
            i += 1
        if path:
            d = os.path.dirname(path)
            dirs.append(os.path.abspath(d) if d else os.getcwd())
    # únicos, estáveis
    out, seen = [], set()
    for d in dirs:
        if d not in seen:
            seen.add(d)
            out.append(d)
    return out or [os.getcwd()]


def _descendants(root):
    kids = {}
    try:
        names = os.listdir("/proc")
    except OSError:
        return [root]
    for name in names:
        if not name.isdigit():
            continue
        try:
            with open(f"/proc/{name}/stat", "r", encoding="utf-8", errors="replace") as f:
                st = f.read()
            rest = st[st.rfind(")") + 2:].split()
            ppid = int(rest[1])
            kids.setdefault(ppid, []).append(int(name))
        except (OSError, ValueError, IndexError):
            continue
    out, stack, seen = [], [root], set()
    while stack:
        p = stack.pop()
        if p in seen:
            continue
        seen.add(p)
        out.append(p)
        stack.extend(kids.get(p, []))
    return out


def _cpu_jiffies(pids):
    total = 0
    for pid in pids:
        try:
            with open(f"/proc/{pid}/stat", "r", encoding="utf-8", errors="replace") as f:
                st = f.read()
            rest = st[st.rfind(")") + 2:].split()
            total += int(rest[11]) + int(rest[12])
        except (OSError, ValueError, IndexError):
            continue
    return total


def _io_bytes(pids):
    r = w = 0
    for pid in pids:
        try:
            with open(f"/proc/{pid}/io", "r", encoding="utf-8", errors="replace") as f:
                data = f.read()
            for line in data.splitlines():
                if line.startswith("read_bytes:"):
                    r += int(line.split()[1])
                elif line.startswith("write_bytes:"):
                    w += int(line.split()[1])
        except (OSError, ValueError, IndexError):
            continue
    return r, w


def _dir_sizes(dirs):
    items = []
    for d in dirs:
        if not os.path.isdir(d):
            continue
        try:
            for root, _, files in os.walk(d):
                for fn in files:
                    fp = os.path.join(root, fn)
                    try:
                        st = os.stat(fp)
                        items.append((fp, st.st_size, int(getattr(st, "st_mtime_ns", st.st_mtime))))
                    except OSError:
                        continue
        except OSError:
            continue
    items.sort()
    return tuple(items)


def _progress_key(pid, dirs):
    pids = _descendants(pid)
    return (_cpu_jiffies(pids), _io_bytes(pids), _dir_sizes(dirs))


def _kill_group(pid):
    try:
        os.killpg(pid, signal.SIGTERM)
    except (ProcessLookupError, PermissionError, OSError):
        pass
    deadline = time.time() + 3
    while time.time() < deadline:
        try:
            os.killpg(pid, 0)
        except (ProcessLookupError, PermissionError, OSError):
            return
        time.sleep(0.15)
    try:
        os.killpg(pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError, OSError):
        pass


def _cleanup_incomplete(dirs, before):
    """Remove só temporários novos desta tentativa (.part/.ytdl/.temp/.tmp), nunca cache já existente."""
    known = {fp for fp, _, _ in before}
    suffixes = (".part", ".ytdl", ".temp", ".tmp")
    for d in dirs:
        if not os.path.isdir(d):
            continue
        for root, _, files in os.walk(d):
            for fn in files:
                if not fn.endswith(suffixes):
                    continue
                fp = os.path.join(root, fn)
                if fp in known:
                    continue
                try:
                    os.remove(fp)
                except OSError:
                    pass


def _run_once(cmd, args, hang_secs, poll, log):
    dirs = _watch_dirs(args)
    before = _dir_sizes(dirs)
    # Evita deadlock no pipe (progresso do yt-dlp pode encher o buffer).
    def _read_out(fh):
        fh.seek(0)
        return fh.read().decode("utf-8", errors="replace")

    with tempfile.TemporaryFile() as outf:
        p = subprocess.Popen(
            cmd,
            stdout=outf,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        last = None
        last_change = time.time()
        try:
            while p.poll() is None:
                if hang_secs > 0:
                    try:
                        key = _progress_key(p.pid, dirs)
                    except Exception:
                        key = last
                    now = time.time()
                    if key != last:
                        last = key
                        last_change = now
                    elif now - last_change >= hang_secs:
                        log(
                            f"[yt-dlp {time.strftime('%H:%M:%S')}] sem progresso há {hang_secs}s "
                            f"(CPU e arquivos parados). Encerrando só este yt-dlp/ffmpeg.",
                            flush=True,
                        )
                        _kill_group(p.pid)
                        try:
                            p.wait(timeout=5)
                        except subprocess.TimeoutExpired:
                            _kill_group(p.pid)
                            p.wait(timeout=3)
                        output = _read_out(outf)
                        _cleanup_incomplete(dirs, before)
                        raise HangError(hang_secs, output)
                time.sleep(poll)
            rc = p.returncode
            return rc, _read_out(outf)
        except HangError:
            raise
        except Exception:
            if p.poll() is None:
                _kill_group(p.pid)
            raise


def run_ytdlp(args, backoff=None, log=print):
    if any(a.startswith("--cookies") for a in args):
        raise SystemExit("Política: não usar cookies de conta com o yt-dlp.")
    waits = backoff or _ints("YT_BACKOFF", "120,300,600")
    hang_secs = int(os.environ.get("YT_HANG_SECS", "90"))
    hang_tries = int(os.environ.get("YT_HANG_TENTATIVAS", "4"))
    hang_backoff = _ints("YT_HANG_BACKOFF", "15,30,60") or [15, 30, 60]
    poll = float(os.environ.get("YT_HANG_POLL", "2"))
    base = [ytdlp_bin()]
    if shutil.which("node"):
        base += ["--js-runtimes", "node"]
    ejs = False
    n = 0
    hang_n = 0
    while True:
        cmd = base + list(args)
        try:
            rc, out = _run_once(cmd, args, hang_secs, poll, log)
        except HangError as e:
            hang_n += 1
            out = e.output or ""
            if hang_n >= hang_tries:
                sys.stderr.write(out[-3000:])
                raise SystemExit(
                    f"yt-dlp travou sem progresso ({e.seconds}s) após {hang_n} tentativa(s)."
                )
            if not ejs and os.environ.get("YT_EJS_REMOTO", "1") != "0":
                log(
                    f"[yt-dlp {time.strftime('%H:%M:%S')}] nova tentativa com --remote-components ejs:github",
                    flush=True,
                )
                base += ["--remote-components", "ejs:github"]
                ejs = True
            wait = hang_backoff[min(hang_n - 1, len(hang_backoff) - 1)]
            log(
                f"[yt-dlp {time.strftime('%H:%M:%S')}] retentando download da seção após travamento "
                f"({hang_n}/{hang_tries - 1}) em {wait}s (sem cookies)...",
                flush=True,
            )
            time.sleep(wait)
            continue
        if rc == 0:
            return out
        if not ejs and os.environ.get("YT_EJS_REMOTO", "1") != "0" and any(m in out for m in EJS_MARKERS):
            log(
                f"[yt-dlp {time.strftime('%H:%M:%S')}] desafio JS/403: tentando com --remote-components ejs:github",
                flush=True,
            )
            base += ["--remote-components", "ejs:github"]
            ejs = True
            continue
        if any(m in out for m in BLOCK_MARKERS) and n < len(waits):
            log(
                f"[yt-dlp {time.strftime('%H:%M:%S')}] YouTube bloqueou (429/robô). Esperando {waits[n]}s "
                f"e tentando de novo ({n + 1}/{len(waits)})...",
                flush=True,
            )
            time.sleep(waits[n])
            n += 1
            continue
        sys.stderr.write(out[-3000:])
        raise SystemExit(f"yt-dlp falhou (código {rc}).")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--":
        a = a[1:]
    print(run_ytdlp(a)[-2000:])
