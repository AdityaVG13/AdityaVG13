#!/usr/bin/env python3
"""Build profile-banner.png (static) and profile-banner-terminal.gif."""
from __future__ import annotations
import math, shutil, subprocess, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
W, H = 1200, 280
LINES = [
    ("cortex ingest session", "ok", "#c4b5fd"),
    ("gpr check artifacts", "pass", "#fdb927"),
    ("route model", "qwen2.5-local", "#94a3b8"),
    ("compress context window", "done", "#86efac"),
]


def render_svg(svg_path: Path, png_path: Path) -> None:
    subprocess.run(["qlmanage", "-t", "-s", "1200", str(svg_path), "-o", str(png_path.parent)], check=True, capture_output=True)
    thumb = png_path.parent / f"{svg_path.name}.png"
    if thumb != png_path:
        thumb.rename(png_path)
    subprocess.run(["magick", str(png_path), "-crop", f"{W}x{H}+0+0", "+repage", str(png_path)], check=True, capture_output=True)


def terminal_svg(visible: int) -> str:
    line_ys = [118, 142, 166, 190]
    rows = []
    for i, (cmd, status, color) in enumerate(LINES):
        if i >= visible:
            break
        y = line_ys[i]
        rows.append(
            f'<text x="88" y="{y}" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="15" fill="#e6edf3">'
            f'<tspan fill="#552583">&gt;</tspan> {cmd}  <tspan fill="{color}">{status}</tspan></text>'
        )
    cursor = ""
    if visible < len(LINES):
        cy = line_ys[visible]
        cursor = f'<rect x="88" y="{cy-12}" width="10" height="16" fill="#552583" opacity="0.85"/>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs><linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#2b3038"/><stop offset="100%" stop-color="#3d4450"/></linearGradient></defs>
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect x="48" y="36" width="1104" height="208" rx="14" fill="#252a31" stroke="#4b5563" stroke-width="1"/>
  <circle cx="76" cy="58" r="6" fill="#ef4444" opacity="0.85"/><circle cx="98" cy="58" r="6" fill="#f59e0b" opacity="0.85"/><circle cx="120" cy="58" r="6" fill="#22c55e" opacity="0.85"/>
  <text x="600" y="62" text-anchor="middle" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="13" fill="#94a3b8">aditya @ workbench</text>
  <text x="88" y="96" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="14" fill="#552583">agent loop</text>
  {''.join(rows)}{cursor}
  <text x="600" y="262" text-anchor="middle" font-family="system-ui, sans-serif" font-size="22" font-weight="700" fill="#e6edf3">AdityaG</text>
</svg>'''


def build_terminal_gif() -> None:
    specs = []
    for n in range(1, len(LINES) + 1):
        specs.extend([n] * 4)
    specs.extend([len(LINES)] * 6 + [0] * 3)
    out = ASSETS / "profile-banner-terminal.gif"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        pngs = []
        for idx, vis in enumerate(specs):
            sp, pp = tmp_path / f"f{idx:02d}.svg", tmp_path / f"f{idx:02d}.png"
            sp.write_text(terminal_svg(vis), encoding="utf-8")
            render_svg(sp, pp)
            pngs.append(pp)
        subprocess.run(["magick", "-delay", "12", "-loop", "0", *[str(p) for p in pngs], str(out)], check=True)
        subprocess.run(["magick", str(out), "-layers", "Optimize", "-colors", "48", str(out)], check=True)
    print(f"terminal gif: {out}")


def build_static_png() -> None:
    src = ASSETS / "profile-banner.svg"
    dst = ASSETS / "profile-banner.png"
    render_svg(src, dst)
    print(f"static png: {dst}")


def main() -> None:
    build_static_png()
    build_terminal_gif()


if __name__ == "__main__":
    main()
