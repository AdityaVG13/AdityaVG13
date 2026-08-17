#!/usr/bin/env python3
"""Profile hero: emath compiles, ZeroStack refs light. First frame is the finished poster."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
OUT = ASSETS / "profile-banner.gif"
PREVIEW = ASSETS / "profile-banner-preview.png"

W, H = 1200, 300
BG = (18, 20, 26)
CARD = (30, 34, 42)
STROKE = (58, 64, 76)
PURPLE = (85, 37, 131)
PURPLE_LIT = (167, 139, 250)
GOLD = (253, 185, 39)
INK = (236, 239, 244)
MUTED = (156, 168, 184)
DIM = (88, 96, 110)

MENLO = "/System/Library/Fonts/Menlo.ttc"
FRAME_MS = 360
HOLD_POSTER = 10
HOLD_END = 16


def fnt(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(MENLO, size=size, index=1 if bold else 0)


def pill(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str, ref: str, on: bool) -> None:
    fill = (48, 36, 68) if on else (26, 29, 36)
    outline = PURPLE_LIT if on else STROKE
    draw.rounded_rectangle(box, radius=10, fill=fill, outline=outline, width=1)
    x, y = box[0] + 16, box[1] + 11
    draw.text((x, y), title, font=fnt(13, bold=True), fill=INK if on else DIM)
    draw.text((x, y + 22), ref, font=fnt(12), fill=GOLD if on else DIM)


def frame(stage: int) -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Brand column
    draw.text((W - 36, 24), "aditya", font=fnt(13), fill=MUTED, anchor="ra")
    draw.text((W - 36, 148), "AdityaG", font=fnt(64, bold=True), fill=PURPLE, anchor="rm")
    draw.line((W - 292, 188, W - 36, 188), fill=PURPLE, width=2)

    # emath card: Gauss packed on one line
    draw.rounded_rectangle((24, 24, 760, 168), radius=14, fill=CARD, outline=STROKE, width=1)
    draw.text((44, 38), "emath", font=fnt(15, bold=True), fill=PURPLE_LIT)

    math = fnt(36, bold=True)
    x = 44
    y_math = 78
    gap = 10
    left = "Σ k" if stage >= 1 else "Σ"
    draw.text((x, y_math), left, font=math, fill=INK if stage >= 1 else DIM)
    x += draw.textlength(left, font=math) + gap
    if stage >= 2:
        draw.text((x, y_math), "=", font=math, fill=PURPLE_LIT)
        x += draw.textlength("=", font=math) + gap
    if stage >= 3:
        draw.text((x, y_math), "n(n + 1) / 2", font=math, fill=INK)
    if stage >= 4:
        draw.text((44, 128), "verified", font=fnt(18, bold=True), fill=GOLD)

    # ZeroStack hub row
    draw.text((24, 188), "ZeroStack", font=fnt(12, bold=True), fill=MUTED if stage >= 5 else DIM)
    y = 210
    w, h, gap = 232, 66, 14
    x0 = 24
    pill(draw, (x0, y, x0 + w, y + h), "TokenZero", "tz://", stage >= 5)
    pill(draw, (x0 + w + gap, y, x0 + 2 * w + gap, y + h), "GraphZero", "gz://", stage >= 6)
    pill(draw, (x0 + 2 * (w + gap), y, x0 + 3 * w + 2 * gap, y + h), "FSZero", "fz://", stage >= 7)

    return img


def sequence() -> list[int]:
    """Poster first so GitHub's static first-frame still looks finished."""
    seq = [7] * HOLD_POSTER
    for s in range(1, 8):
        seq.extend([s] * (2 if s < 5 else 3))
    seq.extend([7] * HOLD_END)
    return seq


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    frames = [frame(s) for s in sequence()]
    frames[0].save(PREVIEW)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        paths: list[Path] = []
        for i, im in enumerate(frames):
            p = tmp_path / f"f{i:03d}.png"
            im.save(p)
            paths.append(p)
        subprocess.run(
            [
                "magick",
                "-delay",
                str(FRAME_MS // 10),
                "-loop",
                "0",
                *[str(p) for p in paths],
                "-colors",
                "64",
                "-layers",
                "optimize",
                str(OUT),
            ],
            check=True,
        )
    print(f"wrote {OUT} ({len(frames)} frames, {OUT.stat().st_size // 1024} KB)")
    print(f"preview {PREVIEW}")


if __name__ == "__main__":
    main()
