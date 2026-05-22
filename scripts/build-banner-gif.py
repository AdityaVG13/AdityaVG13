#!/usr/bin/env python3
"""Build profile-banner-workbench.gif for the profile README."""
from __future__ import annotations
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
W, H = 1200, 280
TERM_X, TERM_Y, TERM_W, TERM_H = 32, 28, 700, 224
LINES = [
    ("cortex ingest session", "ok", "#c4b5fd"),
    ("gpr check artifacts", "pass", "#fdb927"),
    ("projects loading", "...", "#94a3b8"),
    ("compress context window", "done", "#86efac"),
]


def render_svg(svg_path: Path, png_path: Path) -> None:
    subprocess.run(
        ["qlmanage", "-t", "-s", "1200", str(svg_path), "-o", str(png_path.parent)],
        check=True,
        capture_output=True,
    )
    thumb = png_path.parent / f"{svg_path.name}.png"
    if thumb != png_path:
        thumb.rename(png_path)
    subprocess.run(
        ["magick", str(png_path), "-crop", f"{W}x{H}+0+0", "+repage", str(png_path)],
        check=True,
        capture_output=True,
    )


def terminal_svg(visible: int) -> str:
    line_ys = [112, 136, 160, 184]
    rows = []
    for i, (cmd, status, color) in enumerate(LINES):
        if i >= visible:
            break
        y = line_ys[i]
        rows.append(
            f'<text x="56" y="{y}" font-family="ui-monospace, Menlo, Consolas, monospace" '
            f'font-size="14" fill="#e6edf3">'
            f'<tspan fill="#552583">&gt;</tspan> {cmd}  '
            f'<tspan fill="{color}">{status}</tspan></text>'
        )
    cursor = ""
    if visible < len(LINES):
        cy = line_ys[visible]
        cursor = f'<rect x="56" y="{cy - 12}" width="10" height="16" fill="#552583" opacity="0.9"/>'

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2b3038"/>
      <stop offset="100%" stop-color="#3d4450"/>
    </linearGradient>
  </defs>
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect x="{TERM_X}" y="{TERM_Y}" width="{TERM_W}" height="{TERM_H}" rx="14" fill="#252a31" stroke="#4b5563" stroke-width="1"/>
  <circle cx="{TERM_X + 24}" cy="{TERM_Y + 22}" r="6" fill="#ef4444" opacity="0.85"/>
  <circle cx="{TERM_X + 46}" cy="{TERM_Y + 22}" r="6" fill="#f59e0b" opacity="0.85"/>
  <circle cx="{TERM_X + 68}" cy="{TERM_Y + 22}" r="6" fill="#22c55e" opacity="0.85"/>
  <text x="56" y="{TERM_Y + 56}" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="13" fill="#552583">agent loop</text>
  {''.join(rows)}
  {cursor}
  <text x="1168" y="58" text-anchor="end" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="14" fill="#94a3b8">aditya @ workbench</text>
  <text x="1168" y="156" text-anchor="end" font-family="system-ui, -apple-system, sans-serif" font-size="64" font-weight="700" fill="#552583">AdityaG</text>
</svg>"""


def build_terminal_gif() -> None:
    specs: list[int] = []
    for n in range(1, len(LINES) + 1):
        specs.extend([n] * 4)
    specs.extend([len(LINES)] * 6)
    specs.extend([0] * 3)

    out = ASSETS / "profile-banner-workbench.gif"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        pngs: list[Path] = []
        for idx, vis in enumerate(specs):
            sp = tmp_path / f"f{idx:02d}.svg"
            pp = tmp_path / f"f{idx:02d}.png"
            sp.write_text(terminal_svg(vis), encoding="utf-8")
            render_svg(sp, pp)
            pngs.append(pp)
        subprocess.run(
            ["magick", "-delay", "12", "-loop", "0", *[str(p) for p in pngs], str(out)],
            check=True,
        )
        subprocess.run(
            ["magick", str(out), "-layers", "Optimize", "-colors", "48", str(out)],
            check=True,
        )
    print(f"terminal gif: {out}")


def main() -> None:
    build_terminal_gif()


if __name__ == "__main__":
    main()
