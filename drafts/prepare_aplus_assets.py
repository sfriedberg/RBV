#!/usr/bin/env python3
"""Render and crop the manuscript panels used in the A+ investor deck."""

from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "sources" / "kris-forward-2026-09-03"
ASSET_DIR = SOURCE_DIR / "aplus-assets"
MANUSCRIPT = SOURCE_DIR / "BCLXL Chemoresistance Text (2026-07-21)Template.pdf"
FIGURE4 = SOURCE_DIR / "Qin Figure 4 (2026-07-21).pdf"


def render_page(pdf: Path, page: int, output: Path, dpi: int) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "pdftoppm",
            "-png",
            "-r",
            str(dpi),
            "-f",
            str(page),
            "-l",
            str(page),
            "-singlefile",
            str(pdf),
            str(output.with_suffix("")),
        ],
        check=True,
    )
    return output


def crop_fraction(source: Path, output: Path, box: tuple[float, float, float, float]) -> None:
    image = Image.open(source).convert("RGB")
    width, height = image.size
    crop = (
        round(box[0] * width),
        round(box[1] * height),
        round(box[2] * width),
        round(box[3] * height),
    )
    image.crop(crop).save(output, optimize=True)


def make_contact_sheet(files: list[tuple[str, Path]]) -> None:
    cells: list[Image.Image] = []
    for label, path in files:
        image = Image.open(path).convert("RGB")
        image.thumbnail((560, 330))
        cell = Image.new("RGB", (590, 380), "white")
        cell.paste(image, ((590 - image.width) // 2, 12))
        ImageDraw.Draw(cell).text((16, 350), label, fill="black")
        cells.append(ImageOps.expand(cell, border=1, fill=(190, 190, 190)))

    rows = (len(cells) + 1) // 2
    sheet = Image.new("RGB", (1180, rows * 380), (225, 225, 225))
    for index, cell in enumerate(cells):
        sheet.paste(cell, ((index % 2) * 590, (index // 2) * 380))
    sheet.save(ASSET_DIR / "contact-sheet.jpg", quality=92)


def main() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)

    figure3 = render_page(MANUSCRIPT, 43, ASSET_DIR / "figure3-full.png", 300)
    figure6 = render_page(MANUSCRIPT, 49, ASSET_DIR / "figure6-full.png", 300)
    figure8 = render_page(MANUSCRIPT, 53, ASSET_DIR / "figure8-full.png", 300)
    figure4 = render_page(FIGURE4, 1, ASSET_DIR / "figure4-full.png", 360)

    crops = [
        (
            "Figure 3F: DT2216 plus paclitaxel breadth",
            figure3,
            ASSET_DIR / "figure3F-paclitaxel-breadth.png",
            (0.37, 0.19, 0.98, 0.48),
        ),
        (
            "Figure 4E: BCL-XL specificity with MMAF",
            figure4,
            ASSET_DIR / "figure4E-specificity.png",
            (0.02, 0.49, 0.48, 0.75),
        ),
        (
            "Figure 4F: DM4, MMAE and MMAF payloads",
            figure4,
            ASSET_DIR / "figure4F-adc-payloads.png",
            (0.49, 0.49, 0.98, 0.75),
        ),
        (
            "Figure 6D: eight HGSOC PDX models",
            figure6,
            ASSET_DIR / "figure6D-pdx-breadth.png",
            (0.03, 0.36, 0.98, 0.93),
        ),
        (
            "Figure 8F: DF83 flank tumor volume",
            figure8,
            ASSET_DIR / "figure8F-flank-volume.png",
            (0.03, 0.28, 0.45, 0.43),
        ),
        (
            "Figure 8H: DF83 flank survival",
            figure8,
            ASSET_DIR / "figure8H-flank-survival.png",
            (0.61, 0.28, 0.98, 0.43),
        ),
        (
            "Figure 8Q: disseminated DF83 tumor burden",
            figure8,
            ASSET_DIR / "figure8Q-ip-burden.png",
            (0.03, 0.79, 0.44, 0.96),
        ),
        (
            "Figure 8S: disseminated DF83 survival",
            figure8,
            ASSET_DIR / "figure8S-ip-survival.png",
            (0.58, 0.81, 0.82, 0.98),
        ),
    ]

    for _, source, output, box in crops:
        crop_fraction(source, output, box)

    make_contact_sheet([(label, output) for label, _, output, _ in crops])

    for label, _, output, _ in crops:
        image = Image.open(output)
        print(f"{label}: {image.width}x{image.height} -> {output}")


if __name__ == "__main__":
    main()
