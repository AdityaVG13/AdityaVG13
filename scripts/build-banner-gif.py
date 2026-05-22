#!/usr/bin/env python3
"""Build profile-banner-workbench.gif with typewriter terminal animation."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
W, H = 1200, 360
BRAND_W = 520
BRAND_X = W - BRAND_W
TERM_X, TERM_Y, TERM_W, TERM_H = 24, 24, 680, 232
LINE_YS = [96, 126, 156, 186]
FRAME_DELAY_CS = 32
LINE_HOLD_FRAMES = 10
END_HOLD_FRAMES = 16
LINES = [
    ("cortex ingest session", "ok", "#c4b5fd"),
    ("gpr check artifacts", "pass", "#fdb927"),
    ("projects loading", "...", "#94a3b8"),
]
BRAND_SVG = ASSETS / "banner-brand-strip.svg"
BRAND_PNG = ASSETS / "banner-brand-strip.png"


def ensure_brand_strip() -> Path:
    """Right column is a separate SVG; Quick Look skips it in the full banner."""
    brand_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{BRAND_W}" height="{H}" viewBox="0 0 {BRAND_W} {H}">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2b3038"/>
      <stop offset="100%" stop-color="#3d4450"/>
    </linearGradient>
  </defs>
  <rect width="{BRAND_W}" height="{H}" fill="url(#bg)"/>
  <text x="{BRAND_W - 24}" y="56" text-anchor="end" font-family="Menlo, monospace" font-size="14" fill="#94a3b8">aditya @ workbench</text>
  <text x="{BRAND_W - 24}" y="168" text-anchor="end" font-family="Menlo, monospace" font-size="88" font-weight="bold" fill="#552583">AdityaG</text>
  <text x="{BRAND_W - 24}" y="202" text-anchor="end" font-family="Menlo, monospace" font-size="14" fill="#94a3b8">BUILDING AI SYSTEMS</text>
</svg>"""
    BRAND_SVG.write_text(brand_svg, encoding="utf-8")
    subprocess.run(
        ["qlmanage", "-t", "-s", str(BRAND_W), str(BRAND_SVG), "-o", str(ASSETS)],
        check=True,
        capture_output=True,
    )
    thumb = ASSETS / f"{BRAND_SVG.name}.png"
    subprocess.run(
        ["magick", str(thumb), "-crop", f"{BRAND_W}x{H}+0+0", "+repage", str(BRAND_PNG)],
        check=True,
        capture_output=True,
    )
    return BRAND_PNG


def render_svg(svg_path: Path, png_path: Path, brand_png: Path) -> None:
    subprocess.run(
        ["qlmanage", "-t", "-s", "1200", str(svg_path), "-o", str(png_path.parent)],
        check=True,
        capture_output=True,
    )
    thumb = png_path.parent / f"{svg_path.name}.png"
    if thumb != png_path:
        thumb.rename(png_path)
    subprocess.run(
        [
            "magick",
            str(png_path),
            "-crop",
            f"{W}x{H}+0+0",
            "+repage",
            "-background",
            "#2b3038",
            "-gravity",
            "northwest",
            "-extent",
            f"{W}x{H}",
            str(brand_png),
            "-geometry",
            f"+{BRAND_X}+0",
            "-composite",
            str(png_path),
        ],
        check=True,
        capture_output=True,
    )


def terminal_svg(
    done: list[tuple[str, str, str]],
    current: str | None,
    status: str,
    color: str,
    show_cursor: bool,
) -> str:
    rows = []
    for i, (cmd, st, col) in enumerate(done):
        y = LINE_YS[i]
        rows.append(
            f'<text x="44" y="{y}" font-family="ui-monospace, Menlo, Consolas, monospace" '
            f'font-size="14" fill="#e6edf3">'
            f'<tspan fill="#552583">&gt;</tspan> {cmd}  '
            f'<tspan fill="{col}">{st}</tspan></text>'
        )

    if current is not None:
        y = LINE_YS[len(done)]
        body = current.removeprefix("> ").strip()
        cmd_part = body
        st_part = status
        if st_part and cmd_part.endswith(st_part):
            cmd_part = cmd_part[: -len(st_part)].rstrip()
        rows.append(
            f'<text x="44" y="{y}" font-family="ui-monospace, Menlo, Consolas, monospace" '
            f'font-size="14" fill="#e6edf3">'
            f'<tspan fill="#552583">&gt;</tspan> {cmd_part}'
            + (f'  <tspan fill="{color}">{st_part}</tspan>' if st_part else "")
            + "</text>"
        )
        if show_cursor:
            cx = 44 + 8 + len(f"> {cmd_part}" + (f"  {st_part}" if st_part else "")) * 8
            rows.append(
                f'<rect x="{cx}" y="{y - 13}" width="9" height="15" fill="#552583" opacity="0.95"/>'
            )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2b3038"/>
      <stop offset="100%" stop-color="#3d4450"/>
    </linearGradient>
  </defs>
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect x="{TERM_X}" y="{TERM_Y}" width="{TERM_W}" height="{TERM_H}" rx="14" fill="#252a31" stroke="#4b5563" stroke-width="1"/>
  <circle cx="{TERM_X + 22}" cy="{TERM_Y + 18}" r="5.5" fill="#ef4444" opacity="0.9"/>
  <circle cx="{TERM_X + 42}" cy="{TERM_Y + 18}" r="5.5" fill="#f59e0b" opacity="0.9"/>
  <circle cx="{TERM_X + 62}" cy="{TERM_Y + 18}" r="5.5" fill="#22c55e" opacity="0.9"/>
  <text x="44" y="{TERM_Y + 44}" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="13" fill="#552583">agent loop</text>
  {''.join(rows)}
</svg>"""


def build_frame_states() -> list[dict]:
    states: list[dict] = []
    done: list[tuple[str, str, str]] = []

    states.append({"done": [], "current": "> ", "status": "", "color": LINES[0][2], "cursor": True})

    for cmd, status, color in LINES:
        text = f"> {cmd}"
        for n in range(1, len(text) + 1, 2):
            partial = text[:n]
            st = status if n >= len(text) else ""
            states.append(
                {
                    "done": list(done),
                    "current": partial,
                    "status": st,
                    "color": color,
                    "cursor": True,
                }
            )
        states.append(
            {
                "done": list(done),
                "current": text,
                "status": status,
                "color": color,
                "cursor": True,
            }
        )
        done.append((cmd, status, color))
        for _ in range(LINE_HOLD_FRAMES):
            states.append(
                {
                    "done": list(done),
                    "current": None,
                    "status": "",
                    "color": color,
                    "cursor": False,
                }
            )
        if len(done) < len(LINES):
            states.append(
                {
                    "done": list(done),
                    "current": "> ",
                    "status": "",
                    "color": LINES[len(done)][2],
                    "cursor": True,
                }
            )

    for _ in range(END_HOLD_FRAMES):
        states.append(
            {
                "done": list(done),
                "current": None,
                "status": "",
                "color": LINES[-1][2],
                "cursor": False,
            }
        )

    return states




def build_terminal_gif() -> None:
    out = ASSETS / "profile-banner-workbench.gif"
    brand_png = ensure_brand_strip()
    states = build_frame_states()
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        pngs: list[Path] = []
        for idx, state in enumerate(states):
            sp = tmp_path / f"f{idx:04d}.svg"
            pp = tmp_path / f"f{idx:04d}.png"
            sp.write_text(
                terminal_svg(
                    state["done"],
                    state["current"],
                    state["status"],
                    state["color"],
                    state["cursor"],
                ),
                encoding="utf-8",
            )
            render_svg(sp, pp, brand_png)
            pngs.append(pp)
        subprocess.run(
            [
                "magick",
                "-delay",
                str(FRAME_DELAY_CS),
                "-loop",
                "0",
                *[str(p) for p in pngs],
                str(out),
            ],
            check=True,
        )
    print(f"wrote {out} ({len(states)} frames, {out.stat().st_size // 1024} KB)")


def main() -> None:
    build_terminal_gif()


if __name__ == "__main__":
    main()
