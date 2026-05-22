#!/usr/bin/env python3
"""Render assets/profile-banner.gif from animated glow frames. Requires qlmanage + magick."""
from __future__ import annotations
import math, shutil, subprocess, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
FRAMES, FRAME_DELAY_CS = 24, 6

def frame_svg(glow_left, glow_right, corner, bar_shift):
    bar_x1, bar_x2 = bar_shift, 100 - bar_shift
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="280" viewBox="0 0 1200 280">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#15181d"/><stop offset="50%" stop-color="#1a1f26"/><stop offset="100%" stop-color="#262b33"/>
    </linearGradient>
    <linearGradient id="accentBar" x1="{bar_x1}%" y1="0%" x2="{bar_x2}%" y2="0%">
      <stop offset="0%" stop-color="#57d6a3" stop-opacity="0"/>
      <stop offset="35%" stop-color="#57d6a3" stop-opacity="0.55"/>
      <stop offset="65%" stop-color="#87a7bd" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#f2bc66" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="glowLeft" cx="18%" cy="72%" r="28%">
      <stop offset="0%" stop-color="#57d6a3" stop-opacity="{glow_left:.3f}"/><stop offset="100%" stop-color="#57d6a3" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glowRight" cx="82%" cy="28%" r="26%">
      <stop offset="0%" stop-color="#87a7bd" stop-opacity="{glow_right:.3f}"/><stop offset="100%" stop-color="#87a7bd" stop-opacity="0"/>
    </radialGradient>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#30363d" stroke-width="0.5" opacity="0.35"/>
    </pattern>
  </defs>
  <rect width="1200" height="280" fill="url(#bg)"/><rect width="1200" height="280" fill="url(#grid)"/>
  <rect width="1200" height="280" fill="url(#glowLeft)"/><rect width="1200" height="280" fill="url(#glowRight)"/>
  <path d="M 48 220 L 120 220" stroke="#57d6a3" stroke-width="2" opacity="{corner:.3f}" stroke-linecap="round"/>
  <path d="M 48 220 L 48 148" stroke="#57d6a3" stroke-width="2" opacity="{corner:.3f}" stroke-linecap="round"/>
  <path d="M 1152 60 L 1080 60" stroke="#87a7bd" stroke-width="2" opacity="{corner * 0.85:.3f}" stroke-linecap="round"/>
  <path d="M 1152 60 L 1152 132" stroke="#87a7bd" stroke-width="2" opacity="{corner * 0.85:.3f}" stroke-linecap="round"/>
  <text x="600" y="118" text-anchor="middle" font-family="system-ui, sans-serif" font-size="58" font-weight="700" fill="#57d6a3">AdityaG</text>
  <text x="600" y="154" text-anchor="middle" font-family="system-ui, sans-serif" font-size="17" font-weight="500" fill="#c9d1d9" letter-spacing="0.14em">BUILDING AI SYSTEMS</text>
  <rect x="360" y="276" width="480" height="3" fill="url(#accentBar)"/>
  <g font-family="ui-monospace, Menlo, Consolas, monospace" font-size="12" font-weight="600">
    <rect x="352" y="188" width="148" height="28" rx="14" fill="#262b33" stroke="#57d6a3" stroke-width="1"/>
    <text x="426" y="206" text-anchor="middle" fill="#57d6a3">agent memory</text>
    <rect x="516" y="188" width="118" height="28" rx="14" fill="#262b33" stroke="#87a7bd" stroke-width="1"/>
    <text x="575" y="206" text-anchor="middle" fill="#87a7bd">spec loops</text>
    <rect x="650" y="188" width="156" height="28" rx="14" fill="#262b33" stroke="#f2bc66" stroke-width="1"/>
    <text x="728" y="206" text-anchor="middle" fill="#f2bc66">model routing</text>
  </g>
</svg>"""

def render_frame(svg_path: Path, png_path: Path) -> None:
    subprocess.run(["qlmanage", "-t", "-s", "1200", str(svg_path), "-o", str(png_path.parent)], check=True, capture_output=True)
    thumb = png_path.parent / f"{svg_path.name}.png"
    if thumb != png_path:
        thumb.rename(png_path)
    subprocess.run(["magick", str(png_path), "-crop", "1200x280+0+0", "+repage", str(png_path)], check=True, capture_output=True)

def main() -> None:
    out_gif = ASSETS / "profile-banner.gif"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        pngs = []
        for i in range(FRAMES):
            t = (2 * math.pi * i) / FRAMES
            svg_path = tmp_path / f"frame-{i:02d}.svg"
            png_path = tmp_path / f"frame-{i:02d}.png"
            svg_path.write_text(frame_svg(
                0.08 + 0.06 * (0.5 + 0.5 * math.sin(t)),
                0.07 + 0.05 * (0.5 + 0.5 * math.sin(t + 1.2)),
                0.2 + 0.25 * (0.5 + 0.5 * math.sin(t + 0.6)),
                8 * math.sin(t),
            ), encoding="utf-8")
            render_frame(svg_path, png_path)
            pngs.append(png_path)
        subprocess.run(["magick", "-delay", str(FRAME_DELAY_CS), "-loop", "0", *[str(p) for p in pngs], str(out_gif)], check=True)
        subprocess.run(["magick", str(out_gif), "-layers", "Optimize", "-colors", "64", str(out_gif)], check=True)
        shutil.copy2(pngs[FRAMES // 2], ASSETS / "profile-banner.png")
    print(f"Wrote {out_gif}")

if __name__ == "__main__":
    main()
