#!/usr/bin/env python3
"""Reenquadra um trecho 16:9 para 9:16 (1080x1920) em modo FIT: o quadro 16:9 inteiro, sem corte,
centralizado; o resto da tela é preenchido com uma versão desfocada e escurecida do próprio trecho
(ou com a cor da marca, --fundo "#0b1d3a"); o crédito (canal, título, link com tempo) vai para a
área livre acima do quadro. A área abaixo fica livre para as legendas gravadas depois.

Uso (CLI):  python reframe_9x16.py entrada.mp4 saida.mp4 --canal "Google Workspace" \
               --titulo "NotebookLM ..." --link "youtu.be/ID?t=95" [--font Inter] [--fundo blur|#RRGGBB]
Importável: from reframe_9x16 import filtro_9x16, LAYOUT
A entrada deve ser o trecho SEM crédito gravado (cut_clips.py --formatos ...,9x16 faz isso sozinho).
"""
import argparse, subprocess

W, H = 1080, 1920
FG_H = W * 9 // 16                     # 607 -> par abaixo
FG_H -= FG_H % 2                        # 606
FG_Y = (H - FG_H) // 2                  # topo do quadro original
LAYOUT = {"largura": W, "altura": H, "clip_y": FG_Y, "clip_h": FG_H,
          "credito_y": FG_Y - 250, "legenda_area_y": FG_Y + FG_H}


def esc_dt(s):
    return s.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\u2019").replace("%", "\\%")


def font_file(name):
    try:
        return subprocess.check_output(["fc-match", "-f", "%{file}", f"{name}:bold"]).decode().strip()
    except Exception:
        return ""


def filtro_9x16(canal, titulo, link, font="Inter", fundo="blur", rotulo="Trecho do vídeo original", entrada="[0:v]"):
    """filter_complex de `entrada` (ex.: [0:v]) -> [v] (1080x1920, 30 fps)."""
    ff = font_file(font); fnt = f"fontfile='{ff}':" if ff else ""
    if fundo == "blur":
        bg = (f"{entrada}split[r_a][r_b];[r_a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=40:3,"
              f"eq=brightness=-0.18:saturation=0.85,setsar=1[bg]")
    else:
        bg = f"color=c={fundo.replace('#', '0x')}:s={W}x{H}:r=30,setsar=1[bg];{entrada}null[r_b]"
    cy = LAYOUT["credito_y"]
    lines = [(rotulo.upper(), 30, "0x8AB4F8"), (f"{canal} (YouTube)", 38, "white"),
             (f"“{titulo}”", 32, "0xDDE6F5"), (link, 30, "0xB9C7E0")]
    dt, y = [], cy + 22
    for txt, fs, cor in lines:
        dt.append(f"drawtext={fnt}text='{esc_dt(txt)}':x=(w-text_w)/2:y={y}:fontsize={fs}:fontcolor={cor}")
        y += fs + 16
    fg = f"[r_b]scale={W}:{FG_H},setsar=1[fg]"
    comp = (f"[bg][fg]overlay=0:{FG_Y}:shortest=1,fps=30,"
            f"drawbox=x=40:y={cy}:w={W-80}:h={y - cy + 10}:color=black@0.55:t=fill," + ",".join(dt) + "[v]")
    return ";".join([bg, fg, comp])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entrada"); ap.add_argument("saida")
    ap.add_argument("--canal", required=True); ap.add_argument("--titulo", required=True); ap.add_argument("--link", required=True)
    ap.add_argument("--font", default="Inter"); ap.add_argument("--fundo", default="blur")
    a = ap.parse_args()
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", a.entrada, "-filter_complex",
                           filtro_9x16(a.canal, a.titulo, a.link, a.font, a.fundo), "-map", "[v]", "-map", "0:a?",
                           "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-g", "30", "-pix_fmt", "yuv420p",
                           "-c:a", "copy", "-movflags", "+faststart", a.saida])
    print("ok:", a.saida)


if __name__ == "__main__":
    main()
