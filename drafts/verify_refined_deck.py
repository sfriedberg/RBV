#!/usr/bin/env python3
"""Structural and copy checks for the refined Dialectic presentation."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt

from refined_deck_content import SLIDE_TITLES


REQUIRED = [
    "DT2216 plus weekly paclitaxel",
    "0.40 mg/kg",
    "7 of 8",
    "55",
    "12 tumor types",
    "Free payload was tested; the intact ADC was not",
    "confidential",
    "not peer reviewed",
    "suspended for unacceptable toxicity",
]

BANNED = [
    "Dosing stopped day 130",
    "no tumor detectable day 236",
    "Elahere combination",
    "intact Elahere",
    "all dose combinations were synergistic",
    "no platelet toxicity",
    "proven safety superiority",
    "owns the entire APTaD",
    "H2 2025",
    "upcoming Phase 1b/2 pediatric COG trial",
    "Phase 1b/2 study directly tests",
]

REPLACED_SLIDES = {
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    14,
    15,
    16,
    23,
    24,
    25,
    28,
    29,
    30,
    31,
    32,
    33,
    34,
}


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def slide_text(slide) -> str:
    parts: list[str] = []
    for shape in slide.shapes:
        if shape.has_text_frame:
            text = shape.text_frame.text.strip()
            if text:
                parts.append(text)
    return "\n".join(parts)


def extract_text(prs: Presentation) -> list[str]:
    return [slide_text(slide) for slide in prs.slides]


def check_slide_count(prs: Presentation) -> list[str]:
    return [] if len(prs.slides) == 34 else [f"Expected 34 slides; found {len(prs.slides)}"]


def locate_title(slide, number: int) -> str:
    if number == 1:
        for shape in slide.shapes:
            if shape.has_text_frame and "Creating Innovative" in shape.text_frame.text:
                return normalize(shape.text_frame.text)
        return ""
    candidates = []
    for shape in slide.shapes:
        if not shape.has_text_frame or shape.top > Inches(0.72):
            continue
        text = normalize(shape.text_frame.text)
        if text and not text.isdigit():
            candidates.append((shape.left, text))
    candidates.sort(key=lambda item: item[0])
    return candidates[0][1] if candidates else ""


def check_titles(prs: Presentation) -> list[str]:
    errors = []
    for number, slide in enumerate(prs.slides, 1):
        actual = locate_title(slide, number)
        expected = normalize(SLIDE_TITLES[number])
        if actual != expected:
            errors.append(f"Slide {number} title mismatch: {actual!r} != {expected!r}")
    return errors


def check_page_numbers(prs: Presentation) -> list[str]:
    errors = []
    for number, slide in enumerate(prs.slides, 1):
        found = []
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            text = normalize(shape.text_frame.text)
            if (
                text.isdigit()
                and shape.left > Inches(11.35)
                and shape.top > Inches(6.50)
            ):
                found.append(text)
        if str(number) not in found:
            errors.append(f"Slide {number} missing page number")
        if len(found) > 1:
            errors.append(f"Slide {number} has duplicate page numbers: {found}")
    return errors


def check_required_phrases(text: str) -> list[str]:
    lower = text.lower()
    return [f"Missing required phrase: {phrase}" for phrase in REQUIRED if phrase.lower() not in lower]


def check_banned_phrases(text: str) -> list[str]:
    lower = text.lower()
    return [f"Found banned phrase: {phrase}" for phrase in BANNED if phrase.lower() in lower]


def check_manuscript_labels(slides: list[str]) -> list[str]:
    errors = []
    for number in range(17, 23):
        text = slides[number - 1].lower()
        if "confidential" not in text or "not peer reviewed" not in text:
            errors.append(f"Slide {number} missing manuscript-status wording")
    return errors


def check_minimum_font_sizes(prs: Presentation) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    for number in REPLACED_SLIDES:
        slide = prs.slides[number - 1]
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            text = normalize(shape.text_frame.text)
            if not text or text.isdigit():
                continue
            if shape.top < Inches(0.78) or shape.top > Inches(6.65):
                continue
            if text.isupper() and len(text) <= 24:
                continue
            for paragraph in shape.text_frame.paragraphs:
                for run in paragraph.runs:
                    if not run.text.strip() or run.font.size is None:
                        continue
                    points = run.font.size / Pt(1)
                    if points < 12:
                        errors.append(
                            f"Slide {number} has {points:.1f} pt body text: {normalize(run.text)[:60]}"
                        )
                    elif points < 15:
                        warnings.append(
                            f"Slide {number} has {points:.1f} pt secondary text: {normalize(run.text)[:60]}"
                        )
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("presentation", type=Path)
    args = parser.parse_args()

    prs = Presentation(str(args.presentation))
    slides = extract_text(prs)
    full_text = "\n".join(slides)
    errors: list[str] = []
    errors.extend(check_slide_count(prs))
    errors.extend(check_titles(prs))
    errors.extend(check_page_numbers(prs))
    errors.extend(check_required_phrases(full_text))
    errors.extend(check_banned_phrases(full_text))
    errors.extend(check_manuscript_labels(slides))
    font_errors, font_warnings = check_minimum_font_sizes(prs)
    errors.extend(font_errors)

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        if font_warnings:
            print("WARNINGS")
            for warning in font_warnings:
                print(f"- {warning}")
        return 1

    print("PASS: 34 slides")
    print("PASS: titles and page numbers")
    print("PASS: critical wording")
    print("PASS: manuscript labels")
    print("PASS: no banned wording")
    print("PASS: no body text below 12 pt on rebuilt slides")
    if font_warnings:
        print(f"REVIEW: {len(font_warnings)} secondary text runs below 15 pt")
    return 0


if __name__ == "__main__":
    sys.exit(main())

