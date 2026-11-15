#!/usr/bin/env python3
"""Realce de sintaxe offline e determinístico (sem dependências) para mostrar código na aula.

realcar(texto, linguagem) -> lista de linhas em HTML com <span class="tk-..."> (kw, str, com, num, fn, typ, key, punct).
Linguagens: ts, tsx, js, jsx, mjs, json, bash/sh, yaml/yml, md, mdc (Markdown com frontmatter YAML), py, txt.
Uso direto: python realce.py arquivo.ts [ts]  -> imprime HTML.
"""
import html, re, sys

KW = {
    "js": "abstract as async await break case catch class const continue debugger default delete do else enum export extends false "
          "finally for from function get if implements import in instanceof interface let new null of private protected public "
          "readonly return set static super switch this throw true try type typeof undefined var void while with yield satisfies",
    "py": "and as assert async await break class continue def del elif else except False finally for from global if import in is "
          "lambda None nonlocal not or pass raise return True try while with yield",
    "bash": "if then else elif fi for while do done case esac function in export local return set echo cd npm npx node git",
}
TYPES = "string number boolean any unknown never void object Promise Record Array Map Set"
EXT = {"ts": "js", "tsx": "js", "js": "js", "jsx": "js", "mjs": "js", "cjs": "js", "py": "py", "sh": "bash", "bash": "bash",
       "json": "json", "yaml": "yaml", "yml": "yaml", "md": "md", "mdc": "mdc", "txt": "txt"}


def lang_of(name_or_lang):
    k = name_or_lang.rsplit(".", 1)[-1].lower()
    return EXT.get(k, "txt")


def _sp(cls, s):
    return f'<span class="tk-{cls}">{html.escape(s)}</span>' if s else ""


def _code_line(line, fam, state):
    """Tokeniza uma linha de linguagem tipo C/py/bash. state['bloco'] = dentro de /* */."""
    out, i, n = [], 0, len(line)
    kws = set(KW.get(fam, "").split()); tys = set(TYPES.split()) if fam == "js" else set()
    while i < n:
        if state.get("bloco"):
            j = line.find("*/", i)
            if j < 0: out.append(_sp("com", line[i:])); return "".join(out)
            out.append(_sp("com", line[i:j + 2])); i = j + 2; state["bloco"] = False; continue
        ch = line[i]
        if fam == "js" and line.startswith("/*", i): state["bloco"] = True; continue
        if (fam == "js" and line.startswith("//", i)) or (fam in ("py", "bash") and ch == "#"):
            out.append(_sp("com", line[i:])); break
        if ch in "\"'`":
            j = i + 1
            while j < n and line[j] != ch:
                j += 2 if line[j] == "\\" else 1
            out.append(_sp("str", line[i:j + 1])); i = j + 1; continue
        m = re.match(r"\d[\d_.]*(e[+-]?\d+)?", line[i:])
        if m and (i == 0 or not (line[i - 1].isalnum() or line[i - 1] == "_")):
            out.append(_sp("num", m.group(0))); i += len(m.group(0)); continue
        m = re.match(r"[A-Za-z_$][\w$]*", line[i:])
        if m:
            w = m.group(0); rest = line[i + len(w):]
            if w in kws: cls = "kw"
            elif rest.lstrip().startswith("(") and not w[:1].isupper(): cls = "fn"
            elif w in tys or (fam == "js" and w[:1].isupper()): cls = "typ"
            elif fam == "js" and re.match(r"\s*:", rest) and line[:i].rstrip()[-1:] in ("{", ",", ""):
                cls = "key"
            else: cls = ""
            out.append(_sp(cls, w) if cls else html.escape(w)); i += len(w); continue
        if fam == "bash" and ch == "-" and (i == 0 or line[i - 1] == " "):
            m = re.match(r"--?[\w-]+", line[i:])
            if m: out.append(_sp("key", m.group(0))); i += len(m.group(0)); continue
        out.append(_sp("punct", ch) if ch in "{}()[];,.=<>+-*/!?:&|" else html.escape(ch)); i += 1
    return "".join(out)


def _json_line(line):
    out, pos = [], 0
    for m in re.finditer(r'"(?:\\.|[^"\\])*"(\s*:)?|-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?|\btrue\b|\bfalse\b|\bnull\b', line):
        out.append(html.escape(line[pos:m.start()])); t = m.group(0)
        if m.group(1): out.append(_sp("key", t[:-len(m.group(1))]) + html.escape(m.group(1)))
        elif t.startswith('"'): out.append(_sp("str", t))
        elif t[0] in "-0123456789": out.append(_sp("num", t))
        else: out.append(_sp("kw", t))
        pos = m.end()
    out.append(html.escape(line[pos:])); return "".join(out)


def _yaml_line(line):
    m = re.match(r"^(\s*-?\s*)([\w.-]+)(\s*:)(.*)$", line)
    if line.strip().startswith("#"): return _sp("com", line)
    if not m: return html.escape(line)
    v = m.group(4); vs = v.strip()
    if vs in ("true", "false", "null"): vv = html.escape(v[:len(v) - len(v.lstrip())]) + _sp("kw", vs)
    elif re.fullmatch(r"-?\d+(\.\d+)?", vs): vv = html.escape(v[:len(v) - len(v.lstrip())]) + _sp("num", vs)
    elif vs: vv = html.escape(v[:len(v) - len(v.lstrip())]) + _sp("str", vs)
    else: vv = ""
    return html.escape(m.group(1)) + _sp("key", m.group(2)) + html.escape(m.group(3)) + vv


def _md_line(line):
    if re.match(r"^\s*#{1,6}\s", line): return _sp("fn", line)
    if re.match(r"^\s*```", line): return _sp("com", line)
    s = html.escape(line)
    s = re.sub(r"`([^`]+)`", lambda m: f'<span class="tk-str">`{m.group(1)}`</span>', s)
    s = re.sub(r"^(\s*)([-*]|\d+\.)(\s)", lambda m: m.group(1) + f'<span class="tk-punct">{m.group(2)}</span>' + m.group(3), s)
    return s


def realcar(texto, linguagem):
    fam = EXT.get(linguagem.lower(), linguagem.lower())
    linhas = texto.split("\n"); state = {}; out = []
    fm = fam == "mdc" or (fam == "md" and linhas and linhas[0].strip() == "---")
    em_fm = False
    for k, ln in enumerate(linhas):
        if fm and ln.strip() == "---" and (k == 0 or em_fm):
            em_fm = k == 0; out.append(_sp("punct", ln)); continue
        if fm and em_fm: out.append(_yaml_line(ln)); continue
        if fam in ("md", "mdc"): out.append(_md_line(ln))
        elif fam == "json": out.append(_json_line(ln))
        elif fam == "yaml": out.append(_yaml_line(ln))
        elif fam == "txt": out.append(html.escape(ln))
        else: out.append(_code_line(ln, fam, state))
    return out


CSS = """.tk-kw{color:#c792ea}.tk-str{color:#c3e88d}.tk-com{color:#7f8ca3;font-style:italic}.tk-num{color:#f78c6c}
.tk-fn{color:#82aaff}.tk-typ{color:#ffcb6b}.tk-key{color:#89ddff}.tk-punct{color:#a6accd}"""

if __name__ == "__main__":
    p = sys.argv[1]; lg = sys.argv[2] if len(sys.argv) > 2 else lang_of(p)
    print("\n".join(realcar(open(p, encoding="utf-8").read(), lg)))
