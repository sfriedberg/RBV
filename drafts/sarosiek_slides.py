#!/usr/bin/env python3
"""New Sarosiek manuscript slides for the Dialectic A+ deck."""

from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_aplus_deck as base

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "drafts" / "Dialectic_Presentation_09.04.26_A_PLUS_REFINED.pptx"
DST = ROOT / "drafts" / "Dialectic_Presentation_09.04.26_A_PLUS_W_SAROSIEK_SLIDES.pptx"

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
    return base.add_title(slide, title, size=size)


def panel(slide, x, y, w, h, *, fill=WHITE, line=LINE):
    return base.add_panel(slide, x, y, w, h, fill=fill, line=line, radius=False)


def add_label(slide, x, y, w, text, *, fill=NAVY, color=WHITE, size=12.5):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(0.34)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = fill
    textbox(
        slide, x, y, w, 0.34, text.upper(), size=size, bold=True, color=color,
        align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE,
    )


def add_bullets(slide, x, y, w, items, *, size=14, color=DARK, gap=0.60, accent=TEAL):
    for index, item in enumerate(items):
        top = y + index * gap
        marker = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(x), Inches(top + 0.09), Inches(0.07), Inches(0.20)
        )
        marker.fill.solid()
        marker.fill.fore_color.rgb = accent
        marker.line.color.rgb = accent
        textbox(slide, x + 0.18, top, w - 0.18, 0.52, item, size=size, color=color, valign=MSO_ANCHOR.TOP)


def add_footer(slide, source: str = "", status: str = ""):
    y = 7.02
    if status:
        textbox(slide, 0.50, 6.77, 11.55, 0.23, status, size=8.8, color=RED, italic=True)
        y = 6.77
    if source:
        textbox(slide, 0.50, y, 11.50, 0.24, source, size=8.5, color=MID, italic=True)



def slide_raa(prs, blank):
    """Slide 1: Rapid Apoptotic Adaptation"""
    slide = prs.slides.add_slide(blank)
    add_title(slide, "Single-agent BCL-XL targeting is limited by rapid apoptotic adaptation", size=17.5)

    # Left panel - timeline data
    panel(slide, 0.50, 1.05, 7.80, 5.45, fill=WHITE, line=LINE)
    add_label(slide, 0.78, 1.34, 2.65, "BCL-XL degradation triggers compensatory MCL-1 upregulation", fill=NAVY, size=9.5)

    # Table
    headers = ["Timepoint", "BCL-XL (target)", "MCL-1 (compensatory)", "HSP27 (driver)"]
    col_widths = [1.20, 1.80, 2.10, 1.80]
    col_starts = [0.85, 2.05, 3.85, 5.95]
    row_data = [
        ["0 hr", "+++", "baseline", "baseline"],
        ["4 hr", "degraded", "elevated", "phosphorylated"],
        ["8 hr", "degraded", "elevated", "phosphorylated"],
        ["24 hr", "degraded", "elevated", "phosphorylated"],
    ]

    for col_idx, (hdr, cx, cw) in enumerate(zip(headers, col_starts, col_widths)):
        textbox(slide, cx, 1.92, cw, 0.30, hdr, size=11.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx), Inches(1.92), Inches(cw), Inches(0.30))
        bg.fill.solid()
        bg.fill.fore_color.rgb = DEEP_TEAL if col_idx == 1 else NAVY
        bg.line.color.rgb = bg.fill.fore_color.rgb
        bg.element.getparent().remove(bg.element)

    for row_idx, row in enumerate(row_data):
        ry = 2.30 + row_idx * 0.60
        for col_idx, (cell, cx, cw) in enumerate(zip(row, col_starts, col_widths)):
            clr = DARK
            if col_idx == 1 and row_idx > 0:
                clr = RED if row_idx == 0 else RED
            textbox(slide, cx, ry, cw, 0.40, cell, size=11.5, bold=(col_idx == 0 or cell == "degraded"), color=clr, align=PP_ALIGN.CENTER)

    # Draw actual table boxes
    for row_idx in range(5):
        ry = 1.92 + row_idx * 0.60
        tbl = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.85), Inches(ry), Inches(6.90), Inches(0.60))
        tbl.fill.solid()
        tbl.fill.fore_color.rgb = LIGHT if row_idx == 0 else WHITE if row_idx % 2 == 1 else LIGHT
        tbl.line.color.rgb = LINE
        tbl.element.getparent().remove(tbl.element)
    for col_idx, (cx, cw) in enumerate(zip(col_starts, col_widths)):
        tbl = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx), Inches(1.92), Inches(cw), Inches(2.40))
        tbl.fill.solid()
        tbl.fill.fore_color.rgb = DEEP_TEAL if col_idx == 1 else NAVY
        tbl.line.color.rgb = tbl.fill.fore_color.rgb
        tbl.element.getparent().remove(tbl.element)

    # Right panel - explanation
    panel(slide, 8.55, 1.05, 4.20, 5.45, fill=PALE_BLUE, line=LINE)
    add_label(slide, 8.85, 1.34, 1.80, "What is RAA?", fill=NAVY, size=10.5)
    raa_items = [
        "Compensatory upregulation of alternative pro-survival proteins when BCL-XL is degraded",
        "Driven by HSP27 Ser82 phosphorylation within 4-8 hours of DT2216 treatment (Fig. 2J, S2J)",
        "HSP27 inhibitor J2 blocks this adaptation and enhances DT2216-induced apoptosis in HSP27-expressing lines (Fig. 2M-N)",
        "The only line without HSP27 (OV90) shows no J2 sensitization (Fig. 2O)",
        "This is why single-agent BCL-XL targeting produces only modest cell death in solid tumors despite strong CRISPR essentiality",
    ]
    add_bullets(slide, 8.90, 1.90, 3.55, raa_items, size=12.8, gap=0.78, accent=NAVY)

    # Takeaway box
    panel(slide, 0.50, 6.20, 12.25, 0.48, fill=PALE_RED, line=RED)
    textbox(slide, 0.80, 6.26, 11.65, 0.38,
            "The combination is not optional. RAA explains why single-agent DT2216 is insufficient and why MCL-1 suppression is required.",
            size=13.5, bold=True, color=RED, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    add_footer(slide, "Source: Qin et al., submitted manuscript, July 2026, Figs. 2J, 2L, 2M-N, 2O, S2J.",
               "Confidential; not peer reviewed.")
    return slide


def slide_paclitaxel_mechanisms(prs, blank):
    """Slide 2: Paclitaxel's three mechanisms"""
    slide = prs.slides.add_slide(blank)
    add_title(slide, "Paclitaxel supplies the missing MCL-1 effect through three parallel mechanisms", size=17.5)

    mechanisms = [
        {
            "title": "Mechanism 1: MCL-1 degradation",
            "fill": PALE_TEAL,
            "color": DEEP_TEAL,
            "bullets": [
                "Paclitaxel at 1/50th Cmax was the only agent among 12 tested that reduced MCL-1 protein in OVCAR3 cells (Fig. 3A)",
                "Mitotically arrested cells show near-complete absence of MCL-1 expression (Fig. 5E)",
                "Remaining MCL-1 continues to bind BIM and BAK, concentrating survival dependence onto BCL-XL (Fig. 5B)",
                "Mechanism: APC/C-Cdc20 phosphorylates MCL-1 during prolonged mitotic arrest, triggering 26S proteasomal degradation",
            ],
        },
        {
            "title": "Mechanism 2: BCL-XL inactivation",
            "fill": PALE_BLUE,
            "color": NAVY,
            "bullets": [
                "Paclitaxel induces BCL-XL phosphorylation at Ser62 — a previously reported inactivating modification (Fig. 3L, S4B)",
                "Phosphorylated BCL-XL has reduced capacity to sequester BAX",
                "DT2216 degrades both phosphorylated and unphosphorylated BCL-XL equally (Fig. 3L)",
            ],
        },
        {
            "title": "Mechanism 3: HSP27 suppression",
            "fill": PALE_GOLD,
            "color": GOLD,
            "bullets": [
                "Paclitaxel treatment decreases HSP27 expression (Fig. 2L)",
                "This further suppresses the RAA machinery, creating a self-reinforcing cycle",
                "Less HSP27 means less compensatory MCL-1 upregulation when DT2216 is present",
            ],
        },
    ]

    y_start = 1.15
    box_height = 1.55
    gap = 0.12
    for idx, m in enumerate(mechanisms):
        y = y_start + idx * (box_height + gap)
        panel(slide, 0.52, y, 12.20, box_height, fill=m["fill"], line=m["color"])
        textbox(slide, 0.82, y + 0.08, 3.40, 0.34, m["title"], size=14, bold=True, color=m["color"])
        add_bullets(slide, 0.82, y + 0.48, 11.55, m["bullets"], size=12.2, gap=0.34, accent=m["color"])

    # Summary at bottom
    panel(slide, 0.52, 5.45, 12.20, 1.05, fill=WHITE, line=LINE)
    textbox(slide, 0.82, 5.55, 11.60, 0.28, "How the mechanisms work together", size=14, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    textbox(slide, 0.82, 5.88, 5.50, 0.48,
            "Without paclitaxel: DT2216 -> BCL-XL degraded -> MCL-1 upregulated via HSP27 -> resistance",
            size=11.8, color=DARK)
    textbox(slide, 6.60, 5.88, 5.80, 0.48,
            "With paclitaxel: MCL-1 degraded + BCL-XL inactivated + HSP27 suppressed -> apoptosis",
            size=11.8, bold=True, color=DEEP_TEAL)

    panel(slide, 0.52, 6.55, 12.20, 0.38, fill=PALE_RED, line=RED)
    textbox(slide, 0.82, 6.58, 11.60, 0.32,
            "Paclitaxel is not just another chemotherapy. It directly counters the resistance mechanism activated by DT2216 alone.",
            size=13.5, bold=True, color=RED, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    add_footer(slide, "Source: Qin et al., submitted manuscript, July 2026, Figs. 2L, 3A, 3K-L, 5B, 5E, S4B.",
               "Confidential; not peer reviewed.")
    return slide


def slide_coip(prs, blank):
    """Slide 3: Co-IP molecular evidence"""
    slide = prs.slides.add_slide(blank)
    add_title(slide, "Pro-apoptotic proteins are physically released only when both drugs are present", size=17.5)

    # Left panel - BCL-XL IP
    panel(slide, 0.50, 1.05, 6.10, 4.55, fill=WHITE, line=LINE)
    add_label(slide, 0.78, 1.34, 2.90, "BCL-XL immunoprecipitation (Fig. 5A)", fill=NAVY, size=9.8)

    ip_headers = ["Condition", "BIM bound?", "BAX bound?", "BAK bound?"]
    ip_cols = [1.40, 1.20, 1.20, 1.20]
    ip_starts = [0.82, 2.22, 3.42, 4.62]
    ip_rows = [
        ["Untreated", "Yes", "Yes", "Yes"],
        ["Paclitaxel alone", "Yes", "Yes", "Yes"],
        ["DT2216 alone", "Mostly released", "Mostly released", "Mostly released"],
        ["Combination", "Minimal", "Released", "Released"],
    ]

    for ci, (hdr, cx, cw) in enumerate(zip(ip_headers, ip_starts, ip_cols)):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx), Inches(1.92), Inches(cw), Inches(0.28))
        bg.fill.solid()
        bg.fill.fore_color.rgb = NAVY
        bg.line.color.rgb = NAVY
        textbox(slide, cx, 1.92, cw, 0.28, hdr, size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    for ri, row in enumerate(ip_rows):
        ry = 2.24 + ri * 0.56
        for ci, (cell, cx, cw) in enumerate(zip(row, ip_starts, ip_cols)):
            clr = DARK
            if "Released" in cell or "Minimal" in cell and ci > 0:
                clr = GREEN if "Released" in cell else GOLD
            bold = (ci > 0 and ("Yes" in cell or "Released" in cell or "Minimal" in cell))
            textbox(slide, cx, ry, cw, 0.40, cell, size=10.5, bold=bold,
                    color=clr, align=PP_ALIGN.CENTER)

    textbox(slide, 0.78, 4.48, 5.40, 0.70,
            "BCL-XL sequesters BIM, BAX and BAK in untreated cells. Paclitaxel alone does not release them. DT2216 degrades BCL-XL, freeing the executioners.",
            size=11.5, bold=True, color=NAVY, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    # Right panel - MCL-1 IP
    panel(slide, 6.85, 1.05, 5.88, 4.55, fill=PALE_TEAL, line=DEEP_TEAL)
    add_label(slide, 7.12, 1.34, 2.90, "MCL-1 immunoprecipitation (Fig. 5B)", fill=DEEP_TEAL, size=9.8)

    mcl_headers = ["Condition", "BIM bound?", "BAK bound?", "BAX bound?"]
    mcl_cols = [1.40, 1.20, 1.20, 1.20]
    mcl_starts = [7.15, 8.55, 9.75, 10.95]
    mcl_rows = [
        ["Untreated", "Yes", "Yes", "No"],
        ["Paclitaxel alone", "Yes (less MCL-1)", "Yes (less)", "No"],
        ["DT2216 alone", "Increased (freed BIM)", "Increased", "No"],
        ["Combination", "Minimal", "Minimal", "No"],
    ]

    for ci, (hdr, cx, cw) in enumerate(zip(mcl_headers, mcl_starts, mcl_cols)):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx), Inches(1.92), Inches(cw), Inches(0.28))
        bg.fill.solid()
        bg.fill.fore_color.rgb = DEEP_TEAL
        bg.line.color.rgb = DEEP_TEAL
        textbox(slide, cx, 1.92, cw, 0.28, hdr, size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    for ri, row in enumerate(mcl_rows):
        ry = 2.24 + ri * 0.56
        for ci, (cell, cx, cw) in enumerate(zip(row, mcl_starts, mcl_cols)):
            clr = DARK
            if ci > 0 and ("Increased" in cell or "Minimal" in cell):
                clr = GOLD if "Increased" in cell else GREEN
            bold = (ci > 0 and ("Yes" in cell or "Increased" in cell or "Minimal" in cell))
            textbox(slide, cx, ry, cw, 0.40, cell, size=10.5, bold=bold,
                    color=clr, align=PP_ALIGN.CENTER)

    textbox(slide, 7.15, 4.48, 5.20, 0.70,
            "When DT2216 degrades BCL-XL, freed BIM lands on MCL-1. That is RAA in molecular terms. Paclitaxel eliminates this safety net by degrading MCL-1.",
            size=11.5, bold=True, color=DEEP_TEAL, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    # Bottom - additional support
    panel(slide, 0.50, 5.75, 12.25, 0.75, fill=WHITE, line=LINE)
    textbox(slide, 0.82, 5.82, 11.60, 0.60,
            "BAX/BAK double knockout eliminates HeLa cell sensitivity to the combination, confirming cell death is BAX/BAK-dependent apoptosis (Fig. 1K, S2D). The combination is not additive; it is mechanistically synergistic: BCL-XL degradation (DT2216) releases the executioners, and MCL-1 loss (paclitaxel) prevents recapture.",
            size=11.8, color=DARK)

    panel(slide, 0.50, 6.55, 12.25, 0.38, fill=PALE_RED, line=RED)
    textbox(slide, 0.80, 6.58, 11.65, 0.32,
            "Both conditions must be met for apoptosis to proceed. This is the molecular logic of the combination.",
            size=13.5, bold=True, color=RED, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    add_footer(slide, "Source: Qin et al., submitted manuscript, July 2026, Figs. 5A, 5B, 1K, S2D.",
               "Confidential; not peer reviewed.")
    return slide


def slide_patient_tumors(prs, blank):
    """Slide 4: Patient tumor BH3 profiling data"""
    slide = prs.slides.add_slide(blank)
    add_title(slide, "BCL-XL dependence is quantifiable in 11 of 12 primary patient tumors", size=18)

    # Left box - primary tumor BH3 data
    panel(slide, 0.50, 1.05, 6.55, 3.60, fill=WHITE, line=LINE)
    add_label(slide, 0.78, 1.34, 2.65, "BH3 profiling of primary tumors (Fig. 5F-G)", fill=NAVY, size=9.8)

    metrics_left = [
        ("11 of 12 (92%)", "Tumors with BCL-XL dependence by HRK peptide"),
        ("12 of 12 (100%)", "Tumors primed for apoptosis by BIM peptide"),
        ("10 of 12 (83%)", "Tumors with MCL-1 dependence by MS1 peptide"),
        ("22.3% avg", "Cytochrome c release with BAD peptide (range 4-68%)"),
        ("28.0% avg", "Cytochrome c release with HRK peptide (range 9-66%)"),
    ]
    for idx, (stat, desc) in enumerate(metrics_left):
        sy = 1.82 + idx * 0.56
        textbox(slide, 0.78, sy, 1.45, 0.30, stat, size=11.5, bold=True, color=NAVY, align=PP_ALIGN.RIGHT)
        textbox(slide, 2.35, sy, 4.35, 0.46, desc, size=11.5, color=DARK)

    # Left box - PDX confirmation
    panel(slide, 0.50, 4.80, 6.55, 1.10, fill=PALE_BLUE, line=NAVY)
    add_label(slide, 0.78, 4.90, 1.92, "PDX confirmation (Fig. 8A-B)", fill=NAVY, size=9.5)
    pdx_items = [
        "4 of 5 PDX models primed for apoptosis",
        "3 of 5 PDX models with BCL-XL dependence by BAD/HRK",
        "Least primed: DF68 (from patient with 5 prior lines of therapy)",
    ]
    add_bullets(slide, 0.90, 5.35, 5.80, pdx_items, size=11.8, gap=0.28, accent=NAVY)

    # Right box - patient characteristics
    panel(slide, 7.30, 1.05, 5.45, 2.60, fill=PALE_TEAL, line=DEEP_TEAL)
    add_label(slide, 7.58, 1.34, 2.60, "Patient specimens (Table S1)", fill=DEEP_TEAL, size=9.8)
    patient_data = [
        ("Treatment-naive", "1"),
        ("Neoadjuvant (on carboplatin/paclitaxel)", "6"),
        ("Recurrent (1-5+ prior lines)", "4"),
        ("Low-grade serous (LGSOC)", "1"),
    ]
    for idx, (desc, count) in enumerate(patient_data):
        py = 1.85 + idx * 0.40
        textbox(slide, 7.65, py, 3.80, 0.30, desc, size=11.5, color=DARK)
        textbox(slide, 11.60, py, 0.60, 0.30, count, size=11.5, bold=True, color=DEEP_TEAL, align=PP_ALIGN.CENTER)

    # Right box - significance
    panel(slide, 7.30, 3.80, 5.45, 2.10, fill=PALE_GOLD, line=GOLD)
    add_label(slide, 7.58, 3.90, 2.65, "What this means", fill=GOLD, size=9.8)
    significance_items = [
        "BCL-XL dependence is not a cell-line artifact. It is present in treatment-naive, neoadjuvant-treated AND recurrent tumors.",
        "Even patients progressing through 5+ prior lines retain BCL-XL dependence.",
        "The single LGSOC specimen was the only tumor without BCL-XL dependence, consistent with its distinct biology (KRAS/BRAF mutations, TP53 wild-type).",
    ]
    add_bullets(slide, 7.65, 4.42, 4.80, significance_items, size=11.8, gap=0.42, accent=GOLD)

    # Takeaway
    panel(slide, 0.50, 6.10, 12.25, 0.42, fill=PALE_RED, line=RED)
    textbox(slide, 0.80, 6.13, 11.65, 0.36,
            "BCL-XL dependence is the dominant apoptotic survival mechanism in patient tumors across all treatment stages. This is the translational basis for the clinical trial.",
            size=13, bold=True, color=RED, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    add_footer(slide, "Source: Qin et al., submitted manuscript, July 2026, Figs. 5F-G, 8A-B, Table S1, S3.",
               "Confidential; not peer reviewed.")
    return slide


def slide_platform(prs, blank):
    """Slide 5: Platform sensitizer for mitotic-arrest agents"""
    slide = prs.slides.add_slide(blank)
    add_title(slide, "DT2216 is a platform sensitizer for mitotic-arrest agents beyond paclitaxel", size=17.5)

    # Upper grid - manuscript in vitro data
    panel(slide, 0.50, 1.05, 12.25, 3.30, fill=WHITE, line=LINE)
    add_label(slide, 0.78, 1.34, 3.70, "DT2216 synergizes with all tested mitotic-arrest agents (Fig. 4A-D)", fill=NAVY, size=9.8)

    grid_headers = ["Drug class", "Agent", "Cancer types", "DT2216 synergy"]
    grid_widths = [1.60, 1.30, 3.80, 1.80]
    grid_starts = [0.85, 2.50, 3.85, 7.75]
    grid_rows = [
        ["AURKA inhibitor", "Alisertib", "GBM, NSCLC, breast, ovarian", "Synergistic"],
        ["PLK1 inhibitor", "BI-2536", "GBM, NSCLC, breast, ovarian", "Synergistic"],
        ["Microtubule disruptor", "Vincristine", "GBM, NSCLC, breast, ovarian", "Synergistic"],
        ["Microtubule stabilizer", "Docetaxel", "GBM, NSCLC, breast, ovarian", "Synergistic"],
        ["ADC payloads", "DM4, MMAE, MMAF", "OVCAR8 (ovarian) -- BCL-XL specific", "Synergistic"],
    ]

    for ci, (hdr, cx, cw) in enumerate(zip(grid_headers, grid_starts, grid_widths)):
        textbox(slide, cx, 1.82, cw, 0.28, hdr, size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx), Inches(1.82), Inches(cw), Inches(0.28))
        bg.fill.solid()
        bg.fill.fore_color.rgb = NAVY
        bg.line.color.rgb = NAVY

    for ri, row in enumerate(grid_rows):
        ry = 2.15 + ri * 0.44
        for ci, (cell, cx, cw) in enumerate(zip(row, grid_starts, grid_widths)):
            if ci == 3:
                textbox(slide, cx, ry, cw, 0.30, cell, size=10, bold=True, color=GREEN, align=PP_ALIGN.CENTER)
            else:
                textbox(slide, cx, ry, cw, 0.30, cell, size=10, color=DARK)

    textbox(slide, 0.85, 4.05, 11.50, 0.20,
            "DM4 is the payload in mirvetuximab soravtansine (Elahere). Free payload was tested, not the intact ADC.",
            size=10.5, italic=True, color=MID)

    # GDSC external validation
    panel(slide, 0.50, 4.55, 12.25, 1.95, fill=PALE_BLUE, line=NAVY)
    add_label(slide, 0.78, 4.65, 3.70, "Independent GDSC database validation (Fig. 3G-J)", fill=NAVY, size=9.8)

    gdsc_rows = [
        ("Breast (52 lines)", "Navitoclax + alisertib", "63% synergy -- strongest of 1,275 combos"),
        ("Breast (52 lines)", "Navitoclax + paclitaxel", "49% synergy -- 2nd strongest"),
        ("Pancreas (29 lines)", "Navitoclax + paclitaxel", "71% -- strongest combination tested"),
        ("Colon (45 lines)", "Navitoclax + vinorelbine", "36% -- strongest combination tested"),
    ]
    for idx, (cancer, drug, result) in enumerate(gdsc_rows):
        gy = 5.04 + idx * 0.35
        textbox(slide, 0.85, gy, 2.80, 0.26, cancer, size=10.5, bold=True, color=NAVY)
        textbox(slide, 3.75, gy, 3.20, 0.26, drug, size=10.5, color=DARK)
        textbox(slide, 7.05, gy, 5.00, 0.26, result, size=10.5, bold=True, color=DEEP_TEAL)

    textbox(slide, 0.85, 6.08, 11.50, 0.30,
            "Navitoclax (BCL-XL/BCL-2/BCL-W inhibitor) most consistently synergizes with agents that cause mitotic arrest -- not with any other drug class. The mitotic-arrest mechanism is independent of tissue of origin and TP53 status.",
            size=11, italic=True, color=MID)

    # Takeaway
    panel(slide, 0.50, 6.55, 12.25, 0.38, fill=PALE_RED, line=RED)
    textbox(slide, 0.80, 6.58, 11.65, 0.32,
            "DT2216 is not just an ovarian drug. The mitotic-arrest vulnerability is a pan-cancer mechanism validated by both the manuscript and the independent GDSC screen.",
            size=13.5, bold=True, color=RED, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    add_footer(slide,
               "Sources: Qin et al., submitted manuscript, July 2026, Figs. 3F-J, 4A-F, S3H-I, S5A-F; GDSC Anchor data (Jaaks et al., Nature 2022).",
               "Confidential; not peer reviewed. GDSC data as reanalyzed in the manuscript.")
    return slide


def build() -> Path:
    """Insert 5 new slides into the A+ refined deck and save."""
    if not SRC.exists():
        raise FileNotFoundError(f"Source deck not found: {SRC}")

    import shutil
    shutil.copy2(SRC, DST)
    prs = Presentation(str(DST))
    blank = prs.slide_layouts[7]

    # Generate the 5 new slides
    builders = [slide_raa, slide_paclitaxel_mechanisms, slide_coip, slide_patient_tumors, slide_platform]
    for builder in builders:
        builder(prs, blank)

    print(f"Generated {len(builders)} new slides")
    print(f"Total slides now: {len(prs.slides)}")
    print(f"Original slides: 34")
    print(f"New slides: {len(builders)}")
    print(f"Expected total: 39")

    prs.save(str(DST))
    verify = Presentation(str(DST))
    print(f"Verified: {len(verify.slides)} slides saved to {DST}")
    return DST


if __name__ == "__main__":
    build()
