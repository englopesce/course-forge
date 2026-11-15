#!/usr/bin/env python3
"""Confere a narração sem ouvir: transcreve o áudio de volta (faster-whisper, pt)
e compara com o roteiro (WER), lista trocas palavra a palavra e checa termos-chave.

Uso: python check_voice.py roteiro.json audio_ou_video [--model small] [--terms "Termo A,Termo B"]
         [--timings timings.json]  # silencia os intervalos dos trechos originais (clip_start/clip_end)
         [--json relatorio.json]
Requer: pip install faster-whisper (baixa o modelo na 1ª vez).
"""
import argparse, difflib, json, os, re, subprocess

import numpy as np

from faster_whisper import WhisperModel


NUM = {"0": "zero", "1": "um", "2": "dois", "3": "três", "4": "quatro", "5": "cinco", "6": "seis", "7": "sete",
       "8": "oito", "9": "nove", "10": "dez", "11": "onze", "12": "doze", "13": "treze", "14": "catorze",
       "15": "quinze", "16": "dezesseis", "17": "dezessete", "18": "dezoito", "19": "dezenove", "20": "vinte",
       "30": "trinta", "40": "quarenta", "50": "cinquenta", "60": "sessenta", "70": "setenta", "80": "oitenta",
       "90": "noventa", "100": "cem", "200": "duzentos", "300": "trezentos", "400": "quatrocentos",
       "500": "quinhentos", "600": "seiscentos", "700": "setecentos", "800": "oitocentos", "900": "novecentos",
       "1000": "mil"}
EQUIV = {"uma": "um", "duas": "dois"}  # "1"/"2" do Whisper valem para um/uma, dois/duas
EQUIV.update({w[:-2] + "as": w for w in NUM.values() if w.endswith("entos")})  # quinhentas = quinhentos


_EQ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references", "equivalencias-whisper.json")
WHISPER_EQ = {k: v for k, v in json.load(open(_EQ, encoding="utf-8")).items() if not k.startswith("_")} if os.path.exists(_EQ) else {}


try:
    from num2words import num2words as _n2w
except ImportError:  # sem num2words: fica só a tabela NUM (números pequenos)
    _n2w = None


def numeros_por_extenso(s):
    """Algarismos e números por extenso contam como iguais: "28 x 28" = "vinte e oito por vinte e oito",
    "784" = "setecentos e oitenta e quatro", "1.000" = "mil", "10%" = "dez por cento", "18,99" = "dezoito vírgula 99".
    Assim a grafia que o Whisper escolhe não conta como erro de voz."""
    s = re.sub(r"(?<=\d)\s*[x×]\s*(?=\d)", " por ", s)          # 28x28, 28 × 28
    s = re.sub(r"(?<=\d)\.(?=\d{3}(?!\d))", "", s)               # 1.000 -> 1000
    s = re.sub(r"(?<=\d),(?=\d)", " vírgula ", s)                 # 18,9998
    s = re.sub(r"(?<=\d)\s*%", " por cento", s)
    if _n2w:
        s = re.sub(r"\d+", lambda m: " " + _n2w(int(m.group()), lang="pt_BR") + " ", s)
    return s


def norm(s):
    s = numeros_por_extenso(s.lower()).replace("-", " ")
    for k, v in WHISPER_EQ.items():  # grafia brasileira do Whisper para o termo dito certo ("comit" = commit)
        s = re.sub(rf"(?<!\w){re.escape(k)}(?!\w)", v, s)
    s = re.sub(r"intelig[eê]ncia artificial", "ia", s)  # a voz lê "IA" por extenso; o Whisper escreve as duas formas
    s = re.sub(r"[^\w\s]", " ", s)
    # números: o Whisper escreve "2", o roteiro diz "dois" -> não é erro de voz
    return [EQUIV.get(NUM.get(w, w), NUM.get(w, w)) for w in s.split()]


def conta(toks, alvo):
    """Ocorrências do termo como palavras inteiras (1 a 4 palavras coladas: "Service Now" = "ServiceNow").
    Antes contava substring e "SSO" achava "pessoa"."""
    n = i = 0
    while i < len(toks):
        for k in range(1, 5):
            if "".join(toks[i:i + k]) == alvo:
                n += 1; i += k - 1; break
        i += 1
    return n



def junta_compostos(ref, hyp):
    """Junta 2 palavras ouvidas quando, coladas, formam uma palavra do roteiro que nenhuma das duas é
    (ex.: "type script" -> "typescript", "std out" -> "stdout") e o par não aparece separado no roteiro:
    é grafia do Whisper, não erro da voz."""
    vocab = set(ref); pares = set(zip(ref, ref[1:])); out = []; i = 0
    while i < len(hyp):
        if i + 1 < len(hyp) and hyp[i] + hyp[i + 1] in vocab and (hyp[i], hyp[i + 1]) not in pares:
            out.append(hyp[i] + hyp[i + 1]); i += 2
        else:
            out.append(hyp[i]); i += 1
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("roteiro"); ap.add_argument("audio")
    ap.add_argument("--model", default="small")
    ap.add_argument("--terms", default="")
    ap.add_argument("--timings", default="")
    ap.add_argument("--json", default="")
    ap.add_argument("--de-json", default="", help="recalcula o WER com a transcrição já salva nesse relatório (não roda o Whisper)")
    a = ap.parse_args()
    cenas_rot = json.load(open(a.roteiro, encoding="utf-8"))["cenas"]
    ref_txt = " ".join(c["narracao"] for c in cenas_rot)
    ref_cena = {c.get("id"): c["narracao"] for c in cenas_rot}
    a.motor = None
    if a.timings and os.path.exists(a.timings):
        a.motor = json.load(open(a.timings, encoding="utf-8")).get("motor")
        if a.motor:
            print(f"Motor: {a.motor}")
    if a.de_json:
        velho = json.load(open(a.de_json, encoding="utf-8"))
        if velho.get("motor") and not getattr(a, "motor", None):
            a.motor = velho["motor"]
            print(f"Motor: {a.motor}")
        return relatorio(a, ref_txt, velho["transcricao"], None, velho.get("palavras_min"))
    m = WhisperModel(a.model, device="cpu", compute_type="int8")
    # decodifica com ffmpeg (evita incompatibilidade de versões do PyAV)
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", a.audio, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"])
    audio = np.frombuffer(raw, dtype=np.float32).copy()
    clip_total = 0.0
    janelas = []
    if a.timings:
        for c in json.load(open(a.timings, encoding="utf-8"))["cenas"]:
            if "clip_start" in c:
                audio[int(c["clip_start"] * 16000):int(c["clip_end"] * 16000)] = 0.0
                clip_total += c["clip_end"] - c["clip_start"]
            if "start" in c and "end" in c:
                janelas.append((max(0.0, c["start"] - 0.25), c["end"] + 0.35, ref_cena.get(c.get("id"), "")))
    opts = dict(language="pt", beam_size=5, word_timestamps=True,
                vad_filter=True, condition_on_previous_text=False)  # VAD evita "alucinação" no silêncio
    if janelas:
        # cena a cena: na faixa inteira o Whisper às vezes "pula" um trecho de fala (salto de janela de 30 s).
        # O Whisper também oscila de uma rodada para outra (fallback de temperatura, CPU com várias threads):
        # às vezes devolve frase vazia ou em laço para um áudio bom. Por isso cada cena é transcrita até
        # 3 vezes e vale a melhor; a voz só é dada como ruim se as 3 leituras falharem.
        segs, words, speech_dur = [], [], 0.0
        for t0, t1, rtxt in janelas:
            best = None
            for _ in range(3):
                ss, _i = m.transcribe(audio[int(t0 * 16000):int(t1 * 16000)], **opts)
                ss = list(ss)
                r, h = norm(rtxt), norm(" ".join(s_.text.strip() for s_ in ss))
                sm_ = difflib.SequenceMatcher(a=r, b=h, autojunk=False)
                err = (len(r) + len(h) - 2 * sum(b.size for b in sm_.get_matching_blocks())) / max(1, len(r))
                if best is None or err < best[0]:
                    best = (err, ss)
                if err <= 0.05 or not rtxt:
                    break
            ss = best[1]; segs += ss
            words += [w for s_ in ss for w in s_.words]
            speech_dur += t1 - t0
        dur = speech_dur
    else:
        segs, info = m.transcribe(audio, **opts)
        segs = list(segs)
        words = [w for s in segs for w in s.words]
        dur = (segs[-1].end - clip_total) if segs else 0  # tempo de fala, sem os trechos
    hyp_txt = " ".join(s.text.strip() for s in segs)
    relatorio(a, ref_txt, hyp_txt, dur, None)


def relatorio(a, ref_txt, hyp_txt, dur, ritmo):
    ref, hyp = norm(ref_txt), norm(hyp_txt)
    hyp = junta_compostos(ref, hyp)
    sm = difflib.SequenceMatcher(a=ref, b=hyp, autojunk=False)
    S = D = I = 0; diffs = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        if op == "replace":
            S += min(i2 - i1, j2 - j1); D += max(0, (i2 - i1) - (j2 - j1)); I += max(0, (j2 - j1) - (i2 - i1))
        elif op == "delete":
            D += i2 - i1
        else:
            I += j2 - j1
        diffs.append((" ".join(ref[i1:i2]), " ".join(hyp[j1:j2])))
    wer = (S + D + I) / len(ref)
    print(f"WER: {wer:.1%}  (S={S} D={D} I={I}, {len(ref)} palavras de referência)")
    if dur:
        ritmo = round(len(hyp) / (dur / 60), 1)
        print(f"Ritmo: {ritmo:.0f} palavras/min no áudio ({dur:.1f}s até a última fala)")
    print("Trocas (roteiro -> ouvido pelo Whisper):")
    for r, h in diffs:
        print(f"  '{r}' -> '{h}'")
    termos = {}
    for t in [x.strip() for x in a.terms.split(",") if x.strip()]:
        # compara sem espaços: "Service Now" conta como "ServiceNow"
        alvo = "".join(norm(t))
        n_ref = conta(ref, alvo); n_hyp = conta(hyp, alvo)
        n_hyp = min(n_hyp, n_ref)  # não conta acima do esperado (ex.: "serveStdio" ouvido "serve stdio")
        termos[t] = [n_hyp, n_ref]
        print(f"Termo '{t}': {n_hyp}/{n_ref} reconhecidos")
    if a.json:
        rel = {"wer": round(wer, 4), "S": S, "D": D, "I": I, "palavras_ref": len(ref),
               "palavras_min": ritmo, "trocas": diffs,
               "termos": termos, "transcricao": hyp_txt}
        if getattr(a, "motor", None):
            rel["motor"] = a.motor
        json.dump(rel, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\nTranscrição:\n" + hyp_txt)


if __name__ == "__main__":
    main()
