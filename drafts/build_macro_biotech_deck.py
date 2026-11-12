#!/usr/bin/env python3
"""Build the Dialectic A+ presentation with Macro External R&D strategic context.

Preserves `drafts/Dialectic_Presentation_09.04.26_A_PLUS_REFINED.pptx` unchanged
and outputs `drafts/Dialectic_Presentation_A_PLUS_MACRO_EXTERNAL_RD.pptx` (36 slides):
- Updates Slide 3 (`Presentation Overview`) for the 36-slide sequence.
- Inserts Slide 6 (`macro_external_rd_slide`) right after Slide 5 (RVMD precedent).
- Inserts Slide 7 (`proc_deal_seam_slide`) right after Slide 6.
- Updates internal slide cross-references (Slide 17 -> Slide 36 bibliography) and
  renumbers all 36 slides consistently via `set_page_numbers`.
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_aplus_deck as base


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "drafts" / "Dialectic_Presentation_09.04.26_A_PLUS_REFINED.pptx"
DST = ROOT / "drafts" / "Dialectic_Presentation_A_PLUS_MACRO_EXTERNAL_RD.pptx"

TEAL = RGBColor(0x00, 0xA9, 0x98)
DEEP_TEAL = RGBColor(0x00, 0x72, 0x69)
NAVY = RGBColor(0x1F, 0x4E, 0x79)
DARK = RGBColor(0x1F, 0x29, 0x33)
MID = RGBColor(0x4D, 0x5B, 0x66)
LIGHT = RGBColor(0xF3, 0xF6, 0xF7)
PALE_TEAL = RGBColor(0xE8, 0xF5, 0xF3)
PALE_BLUE = RGBColor(0xEA, 0xF0, 0xF6)
PALE_RED = RGBColor(0xFA, 0xEE, 0xED)
PALE_GOLD = RGBColor(0xFB, 0xF5, 0xE8)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
RED = RGBColor(0xA7, 0x35, 0x35)
GOLD = RGBColor(0xB5, 0x78, 0x19)
GREEN = RGBColor(0x2C, 0x7B, 0x63)
LINE = RGBColor(0xCF, 0xD8, 0xDC)
FONT = "Aptos"
FONT_DISPLAY = "Aptos Display"


def textbox(*args, **kwargs):
    kwargs.setdefault("font", FONT)
    return base.textbox(*args, **kwargs)


def add_title(slide, title: str, *, size: float = 22):
    return textbox(
        slide,
        1.12,
        0.10,
        11.55,
        0.50,
        title,
        size=size,
        bold=True,
        color=WHITE,
        font=FONT_DISPLAY,
        valign=MSO_ANCHOR.MIDDLE,
    )


def panel(slide, x: float, y: float, w: float, h: float, *, fill=WHITE, line=LINE, line_pt: float = 1.0):
    shape = base.add_panel(slide, x, y, w, h, fill=fill, line=line, radius=False)
    shape.line.width = Pt(line_pt)
    return shape


def add_label(slide, x: float, y: float, w: float, text: str, *, fill=NAVY, color=WHITE, size: float = 10.0):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(x),
        Inches(y),
        Inches(w),
        Inches(0.32),
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = fill
    textbox(
        slide,
        x,
        y,
        w,
        0.32,
        text.upper(),
        size=size,
        bold=True,
        color=color,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    return shape


def add_rich_textbox(
    slide,
    x: float,
    y: float,
    w: float,
    h: float,
    runs: list[tuple[str, bool, RGBColor]],
    *,
    size: float = 12.5,
    align=PP_ALIGN.LEFT,
    valign=MSO_ANCHOR.TOP,
    margin: float = 0.03,
):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = shape.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = Inches(margin)
    frame.margin_right = Inches(margin)
    frame.margin_top = Inches(margin)
    frame.margin_bottom = Inches(margin)
    frame.vertical_anchor = valign
    paragraph = frame.paragraphs[0]
    paragraph.alignment = align
    paragraph.space_after = Pt(0)
    for text, is_bold, color in runs:
        run = paragraph.add_run()
        base.set_run(run, text, size=size, bold=is_bold, color=color, font=FONT)
    return shape


def add_multiline_centered(
    slide,
    x: float,
    y: float,
    w: float,
    h: float,
    lines: list[str],
    *,
    size: float = 12.0,
    bold: bool = True,
    color=WHITE,
    font: str = FONT,
):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = shape.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = Inches(0.01)
    frame.margin_right = Inches(0.01)
    frame.margin_top = Inches(0.01)
    frame.margin_bottom = Inches(0.01)
    frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    for idx, line in enumerate(lines):
        paragraph = frame.paragraphs[0] if idx == 0 else frame.add_paragraph()
        paragraph.alignment = PP_ALIGN.CENTER
        paragraph.space_after = Pt(0)
        run = paragraph.add_run()
        base.set_run(run, line, size=size, bold=bold, color=color, font=font)
    return shape


def add_footer(slide, source: str, status: str = "", *, source_size: float = 8.5):
    # Keep status <= 11.0" (clear of page-number chevron at x=11.64") and
    # source <= 9.62" (clear of DIALECTIC logo at x=10.18", y=6.98").
    if status:
        textbox(slide, 0.50, 6.75, 10.95, 0.22, status, size=8.6, color=RED, italic=True)
    textbox(slide, 0.50, 7.00, 9.62, 0.24, source, size=source_size, color=MID, italic=True)


def overview_macro_slide(prs: Presentation, blank):
    """Updated Slide 3 Table of Contents reflecting the 36-slide deck structure."""
    slide = prs.slides.add_slide(blank)
    add_title(slide, "Presentation Overview", size=22)

    entries = [
        ("01", "Investment proposition", "Slide 4", False),
        ("02", "External R&D and strategic context", "Slides 5-9", True),
        ("03", "Why BCL-XL and why degradation", "Slides 10-16", False),
        ("04", "Ovarian combination and preclinical data", "Slides 17-27", False),
        ("05", "Human evidence and active trials", "Slides 28-32", False),
        ("06", "Key risks, IP and publications", "Slides 33-36", False),
    ]
    for index, (number, text, slide_range, highlight) in enumerate(entries):
        column = index // 3
        row = index % 3
        x = 0.72 + column * 6.12
        y = 1.24 + row * 1.56
        card_fill = PALE_TEAL if highlight else WHITE
        card_line = TEAL if highlight else LINE
        panel(slide, x, y, 5.72, 1.16, fill=card_fill, line=card_line, line_pt=1.4 if highlight else 1.0)
        accent = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(x),
            Inches(y),
            Inches(0.08),
            Inches(1.16),
        )
        accent.fill.solid()
        accent.fill.fore_color.rgb = DEEP_TEAL if highlight else TEAL
        accent.line.color.rgb = accent.fill.fore_color.rgb

        textbox(
            slide,
            x + 0.22,
            y + 0.20,
            0.68,
            0.76,
            number,
            size=22,
            bold=True,
            color=DEEP_TEAL if highlight else TEAL,
            font=FONT_DISPLAY,
            valign=MSO_ANCHOR.MIDDLE,
        )
        textbox(
            slide,
            x + 0.96,
            y + 0.14,
            3.56,
            0.88,
            text,
            size=15.6,
            bold=True,
            color=NAVY,
            valign=MSO_ANCHOR.MIDDLE,
        )
        textbox(
            slide,
            x + 4.54,
            y + 0.34,
            1.02,
            0.48,
            slide_range,
            size=12.2,
            bold=highlight,
            color=DEEP_TEAL if highlight else MID,
            align=PP_ALIGN.RIGHT,
            valign=MSO_ANCHOR.MIDDLE,
        )

    textbox(
        slide,
        0.75,
        6.22,
        11.80,
        0.44,
        "The ovarian combination is the primary clinical and investment thesis.",
        size=15.5,
        bold=True,
        color=DEEP_TEAL,
        align=PP_ALIGN.CENTER,
    )
    return slide


def macro_external_rd_slide(prs: Presentation, blank):
    """Slide 6 (Slide A): External innovation supplies ~two-thirds of Big Pharma pipeline & revenue."""
    slide = prs.slides.add_slide(blank)
    add_title(
        slide,
        "External innovation supplies roughly two-thirds of Big Pharma product revenue",
        size=19.0,
    )

    # --- Top-Left Panel: EY 2026 Top-25 Biopharma Product Revenue Origin ---
    panel(slide, 0.50, 1.02, 6.15, 3.60, fill=WHITE, line=LINE)
    add_label(slide, 0.72, 1.18, 2.86, "Top-25 pharma revenue origin", fill=NAVY, size=9.6)

    # Compact legend in top-right of left panel
    legend_items = [
        (3.72, DEEP_TEAL, DEEP_TEAL, "M&A"),
        (4.52, TEAL, TEAL, "Alliances"),
        (5.54, PALE_BLUE, NAVY, "Organic"),
    ]
    for lx, lfill, lborder, ltext in legend_items:
        swatch = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(lx), Inches(1.26), Inches(0.16), Inches(0.16))
        swatch.fill.solid()
        swatch.fill.fore_color.rgb = lfill
        swatch.line.color.rgb = lborder
        textbox(slide, lx + 0.19, 1.19, 0.85, 0.30, ltext, size=12.0, bold=True, color=lborder, valign=MSO_ANCHOR.MIDDLE)

    # Headline metric row
    textbox(
        slide,
        0.72,
        1.58,
        1.22,
        0.56,
        "68%",
        size=30,
        bold=True,
        color=TEAL,
        font=FONT_DISPLAY,
        valign=MSO_ANCHOR.MIDDLE,
    )
    textbox(
        slide,
        1.98,
        1.60,
        4.46,
        0.54,
        "of 2025 Top-25 product revenue ($524B of $775B) came from M&A and alliances",
        size=13.0,
        bold=True,
        color=DARK,
        valign=MSO_ANCHOR.MIDDLE,
    )

    # Stacked horizontal bars: 2015 ($412B) vs 2025 ($775B)
    bar_x = 1.92
    bar_w = 4.50
    bar_rows = [
        (
            2.28,
            ["2015", "$412B"],
            [
                (0.44, DEEP_TEAL, DEEP_TEAL, WHITE, ["44%", "($181B)"]),
                (0.17, TEAL, TEAL, WHITE, ["17%", "($70B)"]),
                (0.39, PALE_BLUE, NAVY, NAVY, ["39%", "($162B)"]),
            ],
        ),
        (
            3.02,
            ["2025", "$775B"],
            [
                (0.44, DEEP_TEAL, DEEP_TEAL, WHITE, ["44%", "($340B)"]),
                (0.24, TEAL, TEAL, WHITE, ["24%", "($184B)"]),
                (0.32, PALE_BLUE, NAVY, NAVY, ["32%", "($252B)"]),
            ],
        ),
    ]
    for ry, row_lines, segments in bar_rows:
        add_multiline_centered(
            slide,
            0.70,
            ry,
            1.14,
            0.58,
            row_lines,
            size=12.4,
            bold=True,
            color=NAVY,
        )
        cursor_x = bar_x
        for share, sfill, sline, scolor, slines in segments:
            seg_w = bar_w * share
            seg = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE,
                Inches(cursor_x),
                Inches(ry),
                Inches(seg_w),
                Inches(0.58),
            )
            seg.fill.solid()
            seg.fill.fore_color.rgb = sfill
            seg.line.color.rgb = sline
            seg.line.width = Pt(1.0)
            add_multiline_centered(
                slide,
                cursor_x,
                ry,
                seg_w,
                0.58,
                slines,
                size=12.0,
                bold=True,
                color=scolor,
            )
            cursor_x += seg_w

    panel(slide, 0.72, 3.76, 5.70, 0.70, fill=LIGHT, line=LINE)
    textbox(
        slide,
        0.84,
        3.80,
        5.46,
        0.62,
        "Organic internal revenue fell from 39% (2015) to 32% (2025); alliance revenue grew fastest at 10.2% CAGR vs. 4.5% organic.",
        size=12.2,
        bold=True,
        color=NAVY,
        valign=MSO_ANCHOR.MIDDLE,
    )

    # --- Top-Right Panel: IQVIA Emerging Biopharma R&D Pipeline & Launches ---
    panel(slide, 6.83, 1.02, 5.97, 3.60, fill=PALE_TEAL, line=RGBColor(0xB6, 0xDB, 0xD6))
    add_label(slide, 7.05, 1.18, 3.05, "Emerging biopharma R&D share", fill=DEEP_TEAL, size=9.6)
    textbox(
        slide,
        7.05,
        1.56,
        5.58,
        0.32,
        "Emerging biopharma (EBP): <$200M R&D spend and <$500M revenue",
        size=12.2,
        italic=True,
        color=MID,
        valign=MSO_ANCHOR.MIDDLE,
    )

    track_x = 9.22
    track_w = 3.36
    # Row 1: 2002 active pipeline (33%)
    textbox(slide, 7.05, 1.96, 2.12, 0.38, "2002 active pipeline", size=12.3, bold=True, color=DARK, valign=MSO_ANCHOR.MIDDLE)
    panel(slide, track_x, 1.98, track_w, 0.34, fill=WHITE, line=LINE)
    w_2002 = track_w * 0.33
    panel(slide, track_x, 1.98, w_2002, 0.34, fill=TEAL, line=TEAL)
    textbox(slide, track_x + w_2002 + 0.08, 1.96, 1.80, 0.38, "33% EBP", size=12.2, bold=True, color=DEEP_TEAL, valign=MSO_ANCHOR.MIDDLE)

    # Row 2: 2022-2023 pipeline / starts (67% / 65%)
    textbox(slide, 7.05, 2.45, 2.12, 0.38, "2022-23 R&D / starts", size=12.3, bold=True, color=DARK, valign=MSO_ANCHOR.MIDDLE)
    panel(slide, track_x, 2.47, track_w, 0.34, fill=WHITE, line=LINE)
    w_2223 = track_w * 0.66
    panel(slide, track_x, 2.47, w_2223, 0.34, fill=TEAL, line=TEAL)
    textbox(slide, track_x, 2.47, w_2223, 0.34, "67% / 65% EBP", size=12.0, bold=True, color=WHITE, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    # Row 3: 2025 clinical trial starts (68% EBP vs 26% Large Pharma vs 6% Other)
    textbox(slide, 7.05, 2.94, 2.12, 0.42, "2025 trial starts", size=12.4, bold=True, color=NAVY, valign=MSO_ANCHOR.MIDDLE)
    w_ebp = track_w * 0.68
    w_lp = track_w * 0.26
    w_oth = track_w * 0.06
    panel(slide, track_x, 2.96, w_ebp, 0.38, fill=DEEP_TEAL, line=DEEP_TEAL)
    textbox(slide, track_x, 2.96, w_ebp, 0.38, "68% EBP", size=12.2, bold=True, color=WHITE, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
    panel(slide, track_x + w_ebp, 2.96, w_lp, 0.38, fill=NAVY, line=NAVY)
    textbox(slide, track_x + w_ebp, 2.96, w_lp, 0.38, "26%", size=12.0, bold=True, color=WHITE, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE, margin=0.01)
    panel(slide, track_x + w_ebp + w_lp, 2.96, w_oth, 0.38, fill=LIGHT, line=LINE)

    # Bottom NAS origination callout inside right panel
    panel(slide, 7.05, 3.52, 5.53, 0.94, fill=WHITE, line=TEAL, line_pt=1.2)
    textbox(
        slide,
        7.18,
        3.60,
        1.56,
        0.76,
        "61%-85%",
        size=21,
        bold=True,
        color=DEEP_TEAL,
        font=FONT_DISPLAY,
        valign=MSO_ANCHOR.MIDDLE,
    )
    textbox(
        slide,
        8.78,
        3.56,
        3.72,
        0.86,
        "Novel active substances originated by EBPs (85% of 2024 U.S. launches; 61% of 2025 global launches; large pharma = 26% of trial starts).",
        size=12.1,
        color=DARK,
        valign=MSO_ANCHOR.MIDDLE,
    )

    # --- Bottom Structural Drivers Row ---
    panel(slide, 0.50, 4.78, 6.15, 1.84, fill=PALE_GOLD, line=GOLD, line_pt=1.2)
    add_label(slide, 0.72, 4.92, 2.78, "2025-2030 patent cliff (LOE)", fill=GOLD, size=9.6)
    textbox(
        slide,
        3.58,
        4.90,
        2.84,
        0.36,
        "~$220B to $300B+ at risk",
        size=15.0,
        bold=True,
        color=GOLD,
        font=FONT_DISPLAY,
        align=PP_ALIGN.RIGHT,
        valign=MSO_ANCHOR.MIDDLE,
    )
    textbox(
        slide,
        0.72,
        5.34,
        5.70,
        1.18,
        "Branded sales facing loss of exclusivity (~$220B in 2025-2029 per IQVIA; $300B+ through 2030 per Evaluate), including Keytruda, Opdivo, Darzalex, Ibrance and Xtandi, outpace 10 to 14 year internal R&D timelines.",
        size=12.5,
        color=DARK,
        valign=MSO_ANCHOR.MIDDLE,
    )

    panel(slide, 6.83, 4.78, 5.97, 1.84, fill=PALE_BLUE, line=NAVY, line_pt=1.2)
    add_label(slide, 7.05, 4.92, 3.05, "Division of biopharma R&D labor", fill=NAVY, size=9.6)
    textbox(
        slide,
        7.05,
        5.34,
        5.53,
        1.18,
        "Focused biotechs specialize in novel modalities (such as VHL-recruiting degraders and precision combinations) to absorb early target and modality risk; Big Pharma deploys scale at registrational Phase 2/3 and global launch.",
        size=12.5,
        color=DARK,
        valign=MSO_ANCHOR.MIDDLE,
    )

    add_footer(
        slide,
        "Sources: EY Biotech Beyond Borders 2026 Databook; IQVIA Global Trends in R&D 2023, 2025 & 2026; IQVIA Global Use of Medicines 2025; Evaluate.",
        "Sector external-R&D and LOE figures describe industry structure and do not predict partner interest, deal terms or clinical success for Dialectic.",
    )
    return slide


def proc_deal_seam_slide(prs: Presentation, blank):
    """Slide 7 (Slide B): Phase 1b/2 clinical proof is the principal pharma BD/M&A seam & Dialectic fit."""
    slide = prs.slides.add_slide(blank)
    add_title(
        slide,
        "Phase 1b/2 clinical proof is a primary pharma partnership and acquisition seam",
        size=18.8,
    )

    # --- Top 3-Stage R&D Inflection Architecture ---
    panel(slide, 0.50, 1.00, 3.68, 1.32, fill=PALE_BLUE, line=NAVY)
    textbox(
        slide,
        0.68,
        1.08,
        3.32,
        0.32,
        "1. Modality & Phase 1a safety",
        size=13.0,
        bold=True,
        color=NAVY,
        valign=MSO_ANCHOR.MIDDLE,
    )
    textbox(
        slide,
        0.68,
        1.42,
        3.32,
        0.82,
        "Human RP2D, systemic target engagement and manageable safety established by biotech",
        size=12.3,
        color=DARK,
        valign=MSO_ANCHOR.MIDDLE,
    )

    panel(slide, 4.46, 1.00, 4.42, 1.32, fill=PALE_TEAL, line=DEEP_TEAL, line_pt=2.0)
    add_label(slide, 4.66, 1.08, 4.02, "2. Phase 1b/2 clinical proof (primary seam)", fill=DEEP_TEAL, size=9.4)
    textbox(
        slide,
        4.66,
        1.44,
        4.02,
        0.80,
        "Mechanism-matched combination PoC triggers co-funded trials, alliances or early M&A",
        size=12.4,
        bold=True,
        color=DARK,
        valign=MSO_ANCHOR.MIDDLE,
    )

    panel(slide, 9.16, 1.00, 3.64, 1.32, fill=LIGHT, line=MID)
    textbox(
        slide,
        9.32,
        1.08,
        3.34,
        0.32,
        "3. Phase 2/3 & global launch",
        size=13.0,
        bold=True,
        color=NAVY,
        valign=MSO_ANCHOR.MIDDLE,
    )
    textbox(
        slide,
        9.32,
        1.42,
        3.34,
        0.82,
        "Global registrational trials, commercial scale or post-approval bolt-on M&A",
        size=12.3,
        color=DARK,
        valign=MSO_ANCHOR.MIDDLE,
    )

    for x1, x2 in ((4.18, 4.46), (8.88, 9.16)):
        conn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(1.66), Inches(x2), Inches(1.66))
        conn.line.color.rgb = TEAL
        conn.line.width = Pt(2.2)

    # --- Middle-Left Panel: Recent PROC Acquisition Precedents ---
    panel(slide, 0.50, 2.46, 5.82, 3.54, fill=WHITE, line=LINE)
    add_label(slide, 0.72, 2.60, 3.22, "Recent PROC acquisition precedents", fill=NAVY, size=9.6)

    # Precedent 1: Genmab / ProfoundBio ($1.8B)
    panel(slide, 0.72, 3.04, 5.38, 1.36, fill=PALE_TEAL, line=TEAL, line_pt=1.2)
    textbox(
        slide,
        0.86,
        3.12,
        1.32,
        0.48,
        "$1.8B",
        size=22,
        bold=True,
        color=DEEP_TEAL,
        font=FONT_DISPLAY,
        valign=MSO_ANCHOR.MIDDLE,
    )
    textbox(slide, 0.86, 3.62, 1.32, 0.34, "Apr 2024", size=12.2, bold=True, color=MID, valign=MSO_ANCHOR.MIDDLE)
    textbox(slide, 0.86, 3.94, 1.32, 0.34, "Phase 1/2", size=12.2, bold=True, color=DEEP_TEAL, valign=MSO_ANCHOR.MIDDLE)
    add_rich_textbox(
        slide,
        2.24,
        3.10,
        3.76,
        1.24,
        [
            ("Genmab / ProfoundBio (Rina-S, FRα ADC): ", True, DEEP_TEAL),
            (
                "All-cash buyout following Phase 1/2 ovarian readout (RAINFOL-01) prior to Phase 3 initiation.",
                False,
                DARK,
            ),
        ],
        size=12.4,
        valign=MSO_ANCHOR.MIDDLE,
    )

    # Precedent 2: AbbVie / ImmunoGen ($10.1B)
    panel(slide, 0.72, 4.50, 5.38, 1.38, fill=PALE_BLUE, line=NAVY, line_pt=1.2)
    textbox(
        slide,
        0.86,
        4.58,
        1.32,
        0.48,
        "$10.1B",
        size=20.5,
        bold=True,
        color=NAVY,
        font=FONT_DISPLAY,
        valign=MSO_ANCHOR.MIDDLE,
    )
    textbox(slide, 0.86, 5.08, 1.32, 0.34, "Nov 2023-24", size=12.0, bold=True, color=MID, valign=MSO_ANCHOR.MIDDLE)
    textbox(slide, 0.86, 5.40, 1.32, 0.34, "Approved", size=12.2, bold=True, color=NAVY, valign=MSO_ANCHOR.MIDDLE)
    add_rich_textbox(
        slide,
        2.24,
        4.56,
        3.76,
        1.26,
        [
            ("AbbVie / ImmunoGen (Elahere, FRα ADC): ", True, NAVY),
            (
                "31.7% to 41.9% ORR in FRα-high PROC; restricted to ~36% of PROC patients with boxed ocular warning.",
                False,
                DARK,
            ),
        ],
        size=12.4,
        valign=MSO_ANCHOR.MIDDLE,
    )

    # --- Middle-Right Panel: Dialectic Position at the Seam ---
    panel(slide, 6.50, 2.46, 6.30, 3.54, fill=PALE_TEAL, line=DEEP_TEAL, line_pt=1.2)
    add_label(slide, 6.72, 2.60, 3.56, "Dialectic position at the inflection seam", fill=DEEP_TEAL, size=9.6)

    position_rows = [
        (
            3.04,
            0.94,
            NAVY,
            "Established: ",
            "Phase 1a completed (0.40 mg/kg IV 2x/wk RP2D; sustained leukocyte BCL-XL degradation; transient thrombocytopenia; Mahadevan 2025) + 7/8 HGSOC PDX synergy & DF83 regressions (Qin 2026).",
        ),
        (
            4.06,
            0.88,
            TEAL,
            "Active inflection: ",
            "Recruiting DFCI Phase 1b trial (NCT06964009; DT2216 + weekly paclitaxel, BOIN n=30) in biomarker-unrestricted PROC beyond the ~36% FRα-high subset.",
        ),
        (
            5.02,
            0.88,
            DEEP_TEAL,
            "BD & combo breadth: ",
            "Preclinical mitotic-arrest / free ADC payload (DM4, MMAE, MMAF), KRAS G12C (Lv 2022) and SERD data support co-funded study or gated CDA partner paths.",
        ),
    ]
    for ry, rh, bar_color, lead, copy in position_rows:
        panel(slide, 6.72, ry, 5.86, rh, fill=WHITE, line=LINE)
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.72), Inches(ry), Inches(0.08), Inches(rh))
        bar.fill.solid()
        bar.fill.fore_color.rgb = bar_color
        bar.line.color.rgb = bar_color
        add_rich_textbox(
            slide,
            6.90,
            ry + 0.03,
            5.58,
            rh - 0.06,
            [(lead, True, bar_color), (copy, False, DARK)],
            size=12.1,
            valign=MSO_ANCHOR.MIDDLE,
        )

    # --- Mandatory Claim-Ledger Qualification Banner ---
    panel(slide, 0.50, 6.10, 12.30, 0.52, fill=PALE_RED, line=RED, line_pt=1.2)
    add_multiline_centered(
        slide,
        0.66,
        6.12,
        11.98,
        0.48,
        [
            "Historical PROC deals do not predict DT2216 clinical outcomes, partnership terms or valuation;",
            "human combination efficacy and tumor BCL-XL degradation remain to be established in NCT06964009.",
        ],
        size=12.1,
        bold=True,
        color=RED,
    )

    add_footer(
        slide,
        "Sources: AbbVie/ImmunoGen & Genmab/ProfoundBio (2023-24); Matulonis JCO 2023; St. Laurent & Liu JCO 2023; Mahadevan JHO 2025; Lv JHO 2022; Qin 2026; NCT06964009.",
        "Qin et al. July 2026 manuscript data are confidential and not peer reviewed; free DM4/MMAE/MMAF payloads were tested in vitro, not intact ADCs.",
        source_size=8.5,
    )
    return slide


def update_cross_references(prs: Presentation) -> None:
    """Update hardcoded slide cross-references shifted by the 2-slide insertion."""
    for slide in prs.slides:
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            for paragraph in shape.text_frame.paragraphs:
                for run in paragraph.runs:
                    if "listed on slide 34" in run.text:
                        run.text = run.text.replace("listed on slide 34", "listed on slide 36")


def verify_deck(prs: Presentation) -> None:
    """Run structural, numbering, font-size, and claim-qualification checks on all 36 slides."""
    if len(prs.slides) != 36:
        raise RuntimeError(f"Expected 36 slides, found {len(prs.slides)}")

    for number, slide in enumerate(prs.slides, 1):
        found = []
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            compact = re.sub(r"\s+", " ", shape.text_frame.text).strip()
            if compact.isdigit() and shape.left > Inches(11.35) and shape.top > Inches(6.50):
                found.append(compact)
        if found != [str(number)]:
            raise RuntimeError(f"Slide {number} page number mismatch: {found}")

    for target_slide_num in (3, 6, 7):
        slide = prs.slides[target_slide_num - 1]
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            txt = shape.text_frame.text
            if "\u2014" in txt:
                raise RuntimeError(f"Em-dash found on Slide {target_slide_num}: {txt!r}")
            norm = re.sub(r"\s+", " ", txt).strip()
            if not norm or norm.isdigit():
                continue
            if shape.top < Inches(0.78) or shape.top > Inches(6.65):
                continue
            if norm.isupper() and len(norm) <= 45:
                continue
            for paragraph in shape.text_frame.paragraphs:
                for run in paragraph.runs:
                    if run.text.strip() and run.font.size is not None:
                        pts = run.font.size / Pt(1)
                        if pts < 12.0:
                            raise RuntimeError(
                                f"Slide {target_slide_num} has {pts:.1f} pt body text (<12 pt): {run.text!r}"
                            )


def build() -> Path:
    if not SRC.exists():
        raise FileNotFoundError(f"Base presentation not found: {SRC}")

    shutil.copy2(SRC, DST)
    prs = Presentation(str(DST))
    if len(prs.slides) != 34:
        raise RuntimeError(f"Expected 34 slides in base deck, found {len(prs.slides)}")

    blank = prs.slide_layouts[7]

    overview_macro_slide(prs, blank)     # index 34 -> replaces index 2 (Slide 3)
    macro_external_rd_slide(prs, blank)  # index 35 -> inserted as Slide 6
    proc_deal_seam_slide(prs, blank)     # index 36 -> inserted as Slide 7

    all_entries = list(prs.slides._sldIdLst)
    idx_overview = 34
    idx_macro_a = 35
    idx_macro_b = 36

    # Final 36-slide sequence:
    # Slides 1-2 (indices 0,1), Slide 3 (idx_overview), Slides 4-5 (indices 3,4),
    # Slides 6-7 (idx_macro_a, idx_macro_b), Slides 8-36 (indices 5..33).
    order = [0, 1, idx_overview, 3, 4, idx_macro_a, idx_macro_b] + list(range(5, 34))
    if len(order) != 36 or len(set(order)) != 36:
        raise RuntimeError(f"Invalid 36-slide order: {order}")

    keep = set(order)
    for index, entry in enumerate(all_entries):
        if index not in keep:
            prs.part.drop_rel(entry.get(qn("r:id")))

    slide_list = prs.slides._sldIdLst
    for entry in list(slide_list):
        slide_list.remove(entry)
    for index in order:
        slide_list.append(all_entries[index])

    update_cross_references(prs)
    base.set_page_numbers(prs)
    prs.save(str(DST))

    saved = Presentation(str(DST))
    verify_deck(saved)
    print(f"Saved: {DST}")
    print(f"Total slides: {len(saved.slides)} (verified page numbers 1..36 and >=12pt body copy)")
    return DST


if __name__ == "__main__":
    build()
