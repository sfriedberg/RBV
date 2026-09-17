#!/usr/bin/env python3
"""Build the source-audited, fully polished Dialectic presentation."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

import build_aplus_deck as base
from refined_deck_content import SLIDES


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "drafts" / "Dialectic_Presentation_09.03.26_A_PLUS_DRAFT.pptx"
DST = ROOT / "drafts" / "Dialectic_Presentation_09.04.26_A_PLUS_REFINED.pptx"
RENDERS = ROOT / "drafts" / "qa-aplus-final3"
ASSET_DIR = ROOT / "drafts" / "refined-assets"

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


def add_footer(slide, source: str, status: str = ""):
    if status:
        textbox(slide, 0.50, 6.77, 11.55, 0.23, status, size=8.8, color=RED, italic=True)
    textbox(slide, 0.50, 7.02, 11.50, 0.24, source, size=8.5, color=MID, italic=True)


def add_bullets(slide, x, y, w, items, *, size=15, color=DARK, gap=0.78, accent=TEAL):
    for index, item in enumerate(items):
        top = y + index * gap
        marker = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(x),
            Inches(top + 0.11),
            Inches(0.08),
            Inches(0.25),
        )
        marker.fill.solid()
        marker.fill.fore_color.rgb = accent
        marker.line.color.rgb = accent
        textbox(
            slide,
            x + 0.22,
            top,
            w - 0.22,
            gap - 0.05,
            item,
            size=size,
            color=color,
            valign=MSO_ANCHOR.TOP,
        )


def add_label(slide, x, y, w, text, *, fill=NAVY, color=WHITE, size=12.5):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(x),
        Inches(y),
        Inches(w),
        Inches(0.34),
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = fill
    textbox(
        slide,
        x,
        y,
        w,
        0.34,
        text.upper(),
        size=size,
        bold=True,
        color=color,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )


def add_stat(slide, x, y, w, value, label, *, color=TEAL, size=30):
    textbox(slide, x, y, w, 0.52, value, size=size, bold=True, color=color, font=FONT_DISPLAY)
    textbox(slide, x, y + 0.54, w, 0.58, label, size=13.5, color=MID)


def add_picture_contain(slide, path: Path, x, y, w, h):
    return base.add_picture_contain(slide, path, x, y, w, h)


def crop_fraction(source: Path, output: Path, box: tuple[float, float, float, float]):
    image = Image.open(source).convert("RGB")
    width, height = image.size
    crop = (
        round(box[0] * width),
        round(box[1] * height),
        round(box[2] * width),
        round(box[3] * height),
    )
    image.crop(crop).save(output, quality=95)


def prepare_assets():
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    crops = {
        "slide09-specificity.jpg": (9, (0.76, 0.15, 0.985, 0.71)),
        "slide10-duration-top.jpg": (10, (0.19, 0.20, 0.76, 0.55)),
        "slide10-duration-bottom.jpg": (10, (0.18, 0.64, 0.79, 0.91)),
        "slide23-flc.jpg": (23, (0.13, 0.16, 0.985, 0.76)),
        "slide24-ctcl.jpg": (24, (0.12, 0.16, 0.985, 0.86)),
        "slide25-erbc.jpg": (25, (0.02, 0.14, 0.985, 0.90)),
    }
    for name, (slide_number, box) in crops.items():
        crop_fraction(RENDERS / f"slide-{slide_number:02d}.jpg", ASSET_DIR / name, box)


def overview_slide(prs, blank):
    slide = prs.slides.add_slide(blank)
    add_title(slide, SLIDES[3].title)
    entries = [
        ("01", "Investment proposition"),
        ("02", "Why BCL-XL and why degradation"),
        ("03", "Why paclitaxel in ovarian cancer"),
        ("04", "Preclinical evidence"),
        ("05", "Human evidence and active trials"),
        ("06", "Key risks, intellectual property and supporting work"),
    ]
    for index, (number, text) in enumerate(entries):
        column = index // 3
        row = index % 3
        x = 0.75 + column * 6.15
        y = 1.25 + row * 1.58
        panel(slide, x, y, 5.65, 1.15, fill=WHITE, line=LINE)
        textbox(slide, x + 0.25, y + 0.22, 0.70, 0.52, number, size=22, bold=True, color=TEAL)
        textbox(
            slide,
            x + 1.05,
            y + 0.18,
            4.25,
            0.70,
            text,
            size=16.5,
            bold=True,
            color=NAVY,
            valign=MSO_ANCHOR.MIDDLE,
        )
    textbox(
        slide,
        0.78,
        6.25,
        11.7,
        0.46,
        "The ovarian combination is the primary clinical and investment thesis.",
        size=15.5,
        bold=True,
        color=DEEP_TEAL,
        align=PP_ALIGN.CENTER,
    )
    return slide


def summary_slide(prs, blank):
    spec = SLIDES[4]
    slide = prs.slides.add_slide(blank)
    add_title(slide, spec.title, size=20.5)
    textbox(slide, 0.58, 0.78, 7.3, 0.42, spec.subtitle, size=14.5, color=MID, italic=True)
    labels = ("Human foundation", "Combination evidence", "Clinical inflection")
    for index, (label, text) in enumerate(zip(labels, spec.body)):
        y = 1.42 + index * 1.46
        add_label(slide, 0.58, y, 1.72, label, fill=DEEP_TEAL if index == 2 else NAVY, size=10.2)
        textbox(slide, 0.58, y + 0.46, 7.15, 0.82, text, size=14.7, color=DARK)
    panel(slide, 8.16, 1.05, 4.55, 5.42, fill=PALE_BLUE, line=RGBColor(0xC6, 0xD6, 0xE3))
    add_stat(slide, 8.55, 1.48, 3.75, "0.40 mg/kg", "IV twice-weekly Phase 1 recommended dose", color=NAVY, size=27)
    add_stat(slide, 8.55, 2.85, 3.75, "7 of 8", "Patient-derived ovarian models showed ex-vivo synergy", color=TEAL, size=31)
    add_stat(slide, 8.55, 4.22, 3.75, "Recruiting", "Registered ovarian Phase 1b study; estimated enrollment 30", color=DEEP_TEAL, size=25)
    textbox(
        slide,
        8.55,
        5.72,
        3.75,
        0.48,
        "Central risk: clinical translation of the preclinical combination effect.",
        size=12.6,
        bold=True,
        color=RED,
        align=PP_ALIGN.CENTER,
    )
    add_footer(slide, spec.source, spec.status_note)
    return slide


def rvmd_slide(prs, blank):
    spec = SLIDES[5]
    slide = prs.slides.add_slide(blank)
    add_title(slide, spec.title, size=20.2)
    textbox(slide, 0.62, 0.79, 11.8, 0.40, spec.subtitle, size=14.2, color=MID, italic=True)

    panel(slide, 0.55, 1.35, 6.65, 4.85, fill=WHITE, line=LINE)
    add_label(slide, 0.82, 1.63, 1.72, "Design lesson", fill=NAVY, size=10.8)
    textbox(slide, 0.82, 2.18, 5.98, 0.70, "Active RAS lacked a conventional small-molecule binding pocket.", size=18, bold=True, color=NAVY)
    textbox(
        slide,
        0.82,
        3.06,
        5.98,
        1.08,
        "Daraxonrasib uses tri-complex pharmacology to create a druggable surface and inhibit active RAS signaling across multiple variants.",
        size=15,
        color=DARK,
    )
    textbox(
        slide,
        0.82,
        4.60,
        5.98,
        0.92,
        "Relevance to Dialectic: molecular design can change the therapeutic index of a validated target.",
        size=15.5,
        bold=True,
        color=DEEP_TEAL,
    )

    panel(slide, 7.47, 1.35, 5.25, 4.85, fill=PALE_TEAL, line=RGBColor(0xB9, 0xDC, 0xD7))
    add_label(slide, 7.78, 1.63, 1.92, "Phase 3 result", fill=DEEP_TEAL, size=10.8)
    add_stat(slide, 7.85, 2.22, 2.05, "13.2 mo", "Median overall survival with daraxonrasib", color=DEEP_TEAL, size=28)
    add_stat(slide, 10.12, 2.22, 2.05, "6.7 mo", "Median overall survival with chemotherapy", color=NAVY, size=28)
    add_stat(slide, 7.85, 4.10, 2.10, "0.40", "Overall-survival hazard ratio", color=TEAL, size=31)
    textbox(
        slide,
        10.10,
        4.15,
        2.15,
        1.10,
        "Different target, disease and development risk. This precedent does not predict DT2216 success.",
        size=12.4,
        bold=True,
        color=RED,
    )
    add_footer(slide, spec.source)
    return slide


def leadership_slide(prs, blank):
    spec = SLIDES[6]
    slide = prs.slides.add_slide(blank)
    add_title(slide, spec.title)
    columns = [
        (
            "BOARD",
            [
                ("John Harkey, Jr., JD, MBA", "Executive Chairman; Co-Founder"),
                ("Robert Hromas, MD", "Director; SAB Chair"),
                ("Daohong Zhou, MD", "Director; Scientific Co-Founder"),
                ("David Hitt, JD, MTax", "Board Observer; IP Strategist"),
            ],
        ),
        (
            "MANAGEMENT",
            [
                ("Joshua Sills", "Chief Operating Officer"),
                ("Stephen Friedberg", "Chief Financial Officer"),
                ("James Strauss, MD", "Chief Medical Officer"),
                ("Larry Tremaine, PhD", "Chief Scientific Officer"),
                ("Guangrong Zheng, PhD", "Medicinal Chemistry; Scientific Co-Founder"),
                ("Eric Rasmussen", "Controller"),
            ],
        ),
        (
            "SCIENTIFIC ADVISORS",
            [
                ("Jonathan Licht, MD", "Hematologic oncology"),
                ("Joan Brugge, PhD", "Cancer biology"),
            ],
        ),
    ]
    for col, (heading, people) in enumerate(columns):
        x = 0.52 + col * 4.24
        panel(slide, x, 1.05, 3.98, 5.62, fill=WHITE if col != 1 else PALE_TEAL, line=LINE)
        add_label(slide, x + 0.24, 1.30, 1.90, heading, fill=DEEP_TEAL if col == 1 else NAVY, size=10.2)
        y = 1.92
        for name, role in people:
            textbox(slide, x + 0.28, y, 3.38, 0.28, name, size=14.5, bold=True, color=NAVY)
            textbox(slide, x + 0.28, y + 0.32, 3.38, 0.42, role, size=12.0, color=MID)
            y += 0.80
    add_footer(slide, spec.source, spec.status_note)
    return slide


def pipeline_slide(prs, blank):
    spec = SLIDES[7]
    slide = prs.slides.add_slide(blank)
    add_title(slide, spec.title, size=20)
    headers = ("Program", "Regimen or asset", "Current status", "Evidence basis")
    widths = (2.20, 3.10, 3.30, 3.25)
    xs = (0.62, 2.86, 6.02, 9.38)
    for x, w, heading in zip(xs, widths, headers):
        add_label(slide, x, 1.03, w - 0.08, heading, fill=NAVY, size=9.8)
    rows = [
        ("Ovarian cancer", "DT2216 + weekly paclitaxel", "Recruiting Phase 1b", "Submitted ovarian package"),
        ("Fibrolamellar carcinoma", "DT2216 + irinotecan", "Suspended", "Published FLC PDX work"),
        ("CTCL / ER+ breast cancer", "DT2216 programs", "Proposed", "Published CTCL / unpublished ER+"),
        ("Next generation", "DT5321 / oral degraders", "Preclinical research", "Company programs"),
    ]
    status_colors = (GREEN, RED, GOLD, NAVY)
    status_fills = (PALE_TEAL, PALE_RED, PALE_GOLD, PALE_BLUE)
    for row_index, row in enumerate(rows):
        y = 1.55 + row_index * 1.18
        panel(slide, 0.55, y, 12.18, 0.94, fill=WHITE if row_index % 2 == 0 else LIGHT, line=LINE)
        textbox(slide, 0.75, y + 0.19, 1.92, 0.54, row[0], size=14.3, bold=True, color=NAVY, valign=MSO_ANCHOR.MIDDLE)
        textbox(slide, 2.98, y + 0.19, 2.86, 0.54, row[1], size=13.6, color=DARK, valign=MSO_ANCHOR.MIDDLE)
        badge = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.15), Inches(y + 0.19), Inches(2.92), Inches(0.54))
        badge.fill.solid()
        badge.fill.fore_color.rgb = status_fills[row_index]
        badge.line.color.rgb = status_colors[row_index]
        textbox(
            slide,
            6.15,
            y + 0.19,
            2.92,
            0.54,
            row[2],
            size=13.1,
            bold=True,
            color=status_colors[row_index],
            align=PP_ALIGN.CENTER,
            valign=MSO_ANCHOR.MIDDLE,
        )
        textbox(slide, 9.50, y + 0.19, 2.92, 0.54, row[3], size=12.8, color=MID, valign=MSO_ANCHOR.MIDDLE)
    textbox(
        slide,
        0.68,
        6.32,
        11.85,
        0.36,
        "ClinicalTrials.gov lists NCT06620302 as suspended for unacceptable toxicity; status verified August 2026.",
        size=12.8,
        bold=True,
        color=RED,
        align=PP_ALIGN.CENTER,
    )
    add_footer(slide, spec.source)
    return slide


def target_slide(prs, blank):
    spec = SLIDES[8]
    slide = prs.slides.add_slide(blank)
    add_title(slide, spec.title, size=19.2)
    panel(slide, 0.52, 1.08, 7.15, 5.35, fill=WHITE, line=LINE)
    add_label(slide, 0.82, 1.36, 2.18, "Validated biology", fill=NAVY, size=10.5)
    center_x, center_y = 4.05, 3.22
    center = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(center_x - 0.75), Inches(center_y - 0.75), Inches(1.50), Inches(1.50))
    center.fill.solid()
    center.fill.fore_color.rgb = TEAL
    center.line.color.rgb = DEEP_TEAL
    textbox(slide, center_x - 0.63, center_y - 0.28, 1.26, 0.56, "BCL-XL", size=18, bold=True, color=WHITE, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
    nodes = [
        (1.05, 2.15, "Tumor-cell\nsurvival"),
        (5.55, 2.15, "Treatment\nresistance"),
        (1.05, 4.15, "Senescent-cell\nsurvival"),
        (5.55, 4.15, "Platelet\nsurvival"),
    ]
    for x, y, text in nodes:
        box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(1.75), Inches(0.86))
        box.fill.solid()
        box.fill.fore_color.rgb = PALE_BLUE
        box.line.color.rgb = NAVY
        textbox(slide, x, y, 1.75, 0.86, text, size=14, bold=True, color=NAVY, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    panel(slide, 7.92, 1.08, 4.82, 5.35, fill=PALE_RED, line=RGBColor(0xE4, 0xC1, 0xBF))
    add_label(slide, 8.25, 1.36, 2.24, "Therapeutic constraint", fill=RED, size=10.5)
    textbox(
        slide,
        8.28,
        2.12,
        4.08,
        0.68,
        "The same survival protein is present in tumor cells and platelets.",
        size=18,
        bold=True,
        color=RED,
        align=PP_ALIGN.CENTER,
    )
    textbox(
        slide,
        8.34,
        3.12,
        3.98,
        1.18,
        "Direct BCL-XL inhibition can therefore cause on-target, dose-limiting thrombocytopenia.",
        size=15.5,
        color=DARK,
        align=PP_ALIGN.CENTER,
    )
    textbox(
        slide,
        8.34,
        4.75,
        3.98,
        0.72,
        "The development problem is therapeutic index, not target relevance.",
        size=15.5,
        bold=True,
        color=NAVY,
        align=PP_ALIGN.CENTER,
    )
    add_footer(slide, spec.source)
    return slide


def mechanism_slide(prs, blank):
    spec = SLIDES[9]
    slide = prs.slides.add_slide(blank)
    add_title(slide, spec.title, size=20)
    panel(slide, 0.50, 1.05, 8.15, 5.42, fill=WHITE, line=LINE)
    add_label(slide, 0.82, 1.34, 1.92, "Mechanism", fill=NAVY, size=10.8)
    boxes = [
        (0.88, 2.18, 1.72, "BCL-XL", NAVY),
        (3.22, 2.18, 1.72, "DT2216", TEAL),
        (5.56, 2.18, 1.72, "VHL", DEEP_TEAL),
    ]
    for x, y, w, text, color in boxes:
        shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(w), Inches(0.92))
        shape.fill.solid()
        shape.fill.fore_color.rgb = color
        shape.line.color.rgb = color
        textbox(slide, x, y, w, 0.92, text, size=17, bold=True, color=WHITE, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
    for x1, x2 in ((2.60, 3.22), (4.94, 5.56)):
        connector = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(2.64), Inches(x2), Inches(2.64))
        connector.line.color.rgb = TEAL
        connector.line.width = Pt(2.2)
    textbox(
        slide,
        1.05,
        3.55,
        6.92,
        0.62,
        "Ternary-complex formation promotes BCL-XL ubiquitination and proteasomal degradation.",
        size=16,
        bold=True,
        color=NAVY,
        align=PP_ALIGN.CENTER,
    )
    textbox(
        slide,
        1.05,
        4.55,
        6.92,
        0.78,
        "Preclinical proteomic and complex-formation experiments support the intended degradation specificity.",
        size=15,
        color=DARK,
        align=PP_ALIGN.CENTER,
    )
    panel(slide, 8.90, 1.05, 3.82, 5.42, fill=LIGHT, line=LINE)
    add_label(slide, 9.18, 1.34, 1.92, "Specificity evidence", fill=DEEP_TEAL, size=10.2)
    add_picture_contain(slide, ASSET_DIR / "slide09-specificity.jpg", 9.20, 1.94, 3.20, 2.85)
    textbox(
        slide,
        9.18,
        5.05,
        3.22,
        0.86,
        "Specific degradation supports the intended mechanism. It does not establish the absence of off-target toxicity.",
        size=12.2,
        bold=True,
        color=RED,
        align=PP_ALIGN.CENTER,
    )
    add_footer(slide, spec.source, spec.status_note)
    return slide


def duration_slide(prs, blank):
    spec = SLIDES[10]
    slide = prs.slides.add_slide(blank)
    add_title(slide, spec.title, size=18.5)
    panel(slide, 0.45, 1.03, 8.10, 5.67, fill=WHITE, line=LINE)
    add_picture_contain(slide, ASSET_DIR / "slide10-duration-top.jpg", 0.68, 1.25, 7.62, 2.28)
    add_picture_contain(slide, ASSET_DIR / "slide10-duration-bottom.jpg", 0.68, 3.78, 7.62, 2.38)
    panel(slide, 8.80, 1.03, 3.93, 5.67, fill=PALE_BLUE, line=RGBColor(0xC8, 0xD7, 0xE2))
    add_label(slide, 9.10, 1.34, 1.75, "What it shows", fill=NAVY, size=10.5)
    add_bullets(slide, 9.12, 2.02, 3.22, spec.body, size=14.0, gap=1.20, accent=TEAL)
    add_footer(slide, spec.source)
    return slide


def pkpd_slide(prs, blank):
    spec = SLIDES[11]
    slide = prs.slides.add_slide(blank)
    add_title(slide, spec.title, size=20)
    steps = [
        ("PLASMA", "Concentrations decline after dosing", NAVY, PALE_BLUE),
        ("TISSUE", "Drug can remain within tumor and cells", TEAL, PALE_TEAL),
        ("PHARMACOLOGY", "Target degradation can persist", DEEP_TEAL, PALE_TEAL),
    ]
    for index, (heading, text, color, fill) in enumerate(steps):
        x = 0.62 + index * 4.22
        panel(slide, x, 1.48, 3.70, 2.38, fill=fill, line=color)
        textbox(slide, x + 0.28, 1.83, 3.14, 0.40, heading, size=15.5, bold=True, color=color, align=PP_ALIGN.CENTER)
        textbox(slide, x + 0.34, 2.48, 3.02, 0.86, text, size=16, bold=True, color=DARK, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        if index < 2:
            connector = slide.shapes.add_connector(
                MSO_CONNECTOR.STRAIGHT,
                Inches(x + 3.70),
                Inches(2.67),
                Inches(x + 4.22),
                Inches(2.67),
            )
            connector.line.color.rgb = MID
            connector.line.width = Pt(2)
            connector.line.end_arrowhead = True
    panel(slide, 1.20, 4.35, 10.85, 1.70, fill=WHITE, line=LINE)
    textbox(
        slide,
        1.55,
        4.72,
        10.15,
        0.94,
        "For DT2216, this is a preclinical explanation for the observed PK/PD disconnect. Human tumor retention and BCL-XL degradation have not been established.",
        size=16,
        color=DARK,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_footer(slide, spec.source)
    return slide


def comparison_slide(prs, blank):
    spec = SLIDES[12]
    slide = prs.slides.add_slide(blank)
    add_title(slide, spec.title, size=20.5)
    columns = [
        (
            0.55,
            "NAVITOCLAX",
            NAVY,
            PALE_BLUE,
            (
                "Directly inhibits BCL-XL while drug is present",
                "Daily exposure can maintain platelet inhibition",
                "On-target thrombocytopenia constrained dosing",
            ),
        ),
        (
            6.75,
            "DT2216",
            DEEP_TEAL,
            PALE_TEAL,
            (
                "Uses VHL to degrade BCL-XL",
                "No plasma accumulation with twice-weekly Phase 1 dosing",
                "Preclinical platelet liability reduced, not eliminated",
            ),
        ),
    ]
    for x, heading, color, fill, points in columns:
        panel(slide, x, 1.15, 5.95, 4.75, fill=fill, line=color)
        textbox(slide, x + 0.35, 1.52, 5.25, 0.50, heading, size=21, bold=True, color=color, align=PP_ALIGN.CENTER)
        add_bullets(slide, x + 0.48, 2.35, 4.98, points, size=15, gap=1.00, accent=color)
    panel(slide, 1.15, 6.10, 10.98, 0.58, fill=PALE_RED, line=RGBColor(0xE4, 0xC1, 0xBF))
    textbox(
        slide,
        1.38,
        6.19,
        10.52,
        0.38,
        "Phase 1: thrombocytopenia in 9 of 20 patients; one dose-limiting grade 4 event resolved within 48 hours.",
        size=13.3,
        bold=True,
        color=RED,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_footer(slide, spec.source)
    return slide


def tissue_slide(prs, blank):
    spec = SLIDES[14]
    slide = prs.slides.add_slide(blank)
    add_title(slide, spec.title, size=20.5)
    panel(slide, 0.62, 1.15, 12.05, 4.92, fill=WHITE, line=LINE)
    stages = [
        ("After dosing", "Plasma exposure falls", NAVY),
        ("Tumor tissue", "DT2216 remains detectable", TEAL),
        ("Target effect", "BCL-XL degradation persists", DEEP_TEAL),
    ]
    for index, (heading, text, color) in enumerate(stages):
        x = 0.98 + index * 4.03
        circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x + 0.95), Inches(1.70), Inches(1.25), Inches(1.25))
        circle.fill.solid()
        circle.fill.fore_color.rgb = color
        circle.line.color.rgb = color
        textbox(slide, x + 1.02, 2.02, 1.11, 0.46, str(index + 1), size=24, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        textbox(slide, x + 0.20, 3.20, 2.75, 0.38, heading, size=16, bold=True, color=color, align=PP_ALIGN.CENTER)
        textbox(slide, x + 0.20, 3.72, 2.75, 0.82, text, size=16, color=DARK, align=PP_ALIGN.CENTER)
        if index < 2:
            connector = slide.shapes.add_connector(
                MSO_CONNECTOR.STRAIGHT,
                Inches(x + 2.35),
                Inches(2.33),
                Inches(x + 4.00),
                Inches(2.33),
            )
            connector.line.color.rgb = LINE
            connector.line.width = Pt(2)
    textbox(
        slide,
        1.15,
        5.28,
        11.00,
        0.50,
        "Company preclinical data support intermittent dosing. Human tumor exposure remains an open question.",
        size=15.2,
        bold=True,
        color=NAVY,
        align=PP_ALIGN.CENTER,
    )
    add_footer(slide, spec.source)
    return slide


def evidence_map_slide(prs, blank):
    spec = SLIDES[15]
    slide = prs.slides.add_slide(blank)
    add_title(slide, spec.title, size=18.2)
    columns = [
        (
            "PUBLISHED\nSINGLE AGENT",
            NAVY,
            PALE_BLUE,
            ("T-ALL", "Cutaneous T-cell lymphoma"),
        ),
        (
            "PUBLISHED\nCOMBINATIONS",
            GOLD,
            PALE_GOLD,
            ("AML and SCLC", "KRAS G12C cancers", "Pancreatic and breast cancer", "Fibrolamellar carcinoma"),
        ),
        (
            "SUBMITTED\nOVARIAN PACKAGE",
            DEEP_TEAL,
            PALE_TEAL,
            ("Mechanism in HGSOC", "Patient-derived models", "Flank and disseminated PDX", "Pan-cancer in-vitro breadth"),
        ),
    ]
    for index, (heading, color, fill, items) in enumerate(columns):
        x = 0.52 + index * 4.24
        panel(slide, x, 1.15, 3.98, 5.27, fill=fill, line=color)
        textbox(slide, x + 0.30, 1.50, 3.38, 0.72, heading, size=17, bold=True, color=color, align=PP_ALIGN.CENTER)
        add_bullets(slide, x + 0.38, 2.58, 3.20, items, size=14.6, gap=0.77, accent=color)
        if index == 2:
            textbox(slide, x + 0.38, 5.70, 3.20, 0.40, "Most complete current evidence package", size=12.6, bold=True, color=DEEP_TEAL, align=PP_ALIGN.CENTER)
    add_footer(slide, spec.source, spec.status_note)
    return slide


def portfolio_slide(prs, blank):
    spec = SLIDES[16]
    slide = prs.slides.add_slide(blank)
    add_title(slide, spec.title, size=19.3)
    rows = [
        ("OVARIAN", "Recruiting Phase 1b", "Most complete current mechanism, patient-derived and in-vivo package", GREEN, PALE_TEAL),
        ("FLC", "Suspended", "Published PDX rationale; registered study suspended for unacceptable toxicity", RED, PALE_RED),
        ("CTCL", "Proposed", "Published xenograft evidence; company-planned clinical program", GOLD, PALE_GOLD),
        ("ER+ BREAST", "Proposed", "Unpublished preclinical evidence; company-planned clinical program", NAVY, PALE_BLUE),
    ]
    for index, (program, status, evidence, color, fill) in enumerate(rows):
        y = 1.25 + index * 1.30
        panel(slide, 0.58, y, 12.08, 1.02, fill=fill, line=color)
        textbox(slide, 0.86, y + 0.25, 1.65, 0.48, program, size=15, bold=True, color=color, valign=MSO_ANCHOR.MIDDLE)
        textbox(slide, 2.72, y + 0.25, 2.12, 0.48, status, size=15, bold=True, color=color, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        textbox(slide, 5.12, y + 0.18, 7.10, 0.64, evidence, size=14.3, color=DARK, valign=MSO_ANCHOR.MIDDLE)
    add_footer(slide, spec.source)
    return slide


def evidence_image_slide(prs, blank, number: int, asset: str, image_w: float):
    spec = SLIDES[number]
    slide = prs.slides.add_slide(blank)
    add_title(slide, spec.title, size=18.2 if number != 24 else 17.8)
    panel(slide, 0.38, 1.05, image_w, 5.68, fill=WHITE, line=LINE)
    add_picture_contain(slide, ASSET_DIR / asset, 0.57, 1.26, image_w - 0.38, 5.18)
    x = 0.38 + image_w + 0.24
    w = 12.82 - x
    panel(slide, x, 1.05, w, 5.68, fill=PALE_BLUE if number != 25 else PALE_GOLD, line=LINE)
    add_label(slide, x + 0.25, 1.35, min(1.80, w - 0.50), "Evidence", fill=NAVY, size=10.5)
    add_bullets(slide, x + 0.28, 2.02, w - 0.55, spec.body, size=13.5, gap=1.28, accent=TEAL)
    add_footer(slide, spec.source, spec.status_note)
    return slide


def ovarian_trial_slide(prs, blank):
    spec = SLIDES[28]
    slide = prs.slides.add_slide(blank)
    add_title(slide, spec.title, size=21)
    textbox(slide, 0.60, 0.79, 11.95, 0.38, spec.subtitle, size=14.2, color=MID, italic=True)
    panel(slide, 0.52, 1.33, 7.58, 4.95, fill=PALE_TEAL, line=RGBColor(0xB6, 0xDB, 0xD6))
    add_label(slide, 0.82, 1.62, 2.02, "Registered study", fill=DEEP_TEAL, size=10.5)
    add_stat(slide, 0.86, 2.16, 2.10, "30", "Estimated enrollment", color=DEEP_TEAL, size=31)
    add_stat(slide, 3.18, 2.16, 2.08, "BOIN", "Dose-escalation design", color=TEAL, size=27)
    add_stat(slide, 5.46, 2.16, 2.12, "Recruiting", "Status in current registry", color=GREEN, size=22)
    textbox(
        slide,
        0.88,
        3.78,
        6.85,
        1.28,
        "Company protocol dose levels\nDT2216 0.32 or 0.40 mg/kg IV twice weekly\nPaclitaxel 70 or 80 mg/m² IV weekly",
        size=15,
        color=DARK,
        align=PP_ALIGN.CENTER,
    )
    textbox(
        slide,
        0.88,
        5.38,
        6.85,
        0.45,
        "Primary registered outcome: combination maximum tolerated dose.",
        size=14.0,
        bold=True,
        color=NAVY,
        align=PP_ALIGN.CENTER,
    )
    panel(slide, 8.35, 1.33, 4.38, 4.95, fill=PALE_BLUE, line=LINE)
    add_label(slide, 8.67, 1.62, 2.05, "Later expansion", fill=NAVY, size=10.5)
    textbox(
        slide,
        8.72,
        2.28,
        3.62,
        1.25,
        "A Phase 2 expansion remains a company plan.",
        size=19,
        bold=True,
        color=NAVY,
        align=PP_ALIGN.CENTER,
    )
    textbox(
        slide,
        8.72,
        3.93,
        3.62,
        1.25,
        "It is not included in the current ClinicalTrials.gov record. No human combination response rate has been reported.",
        size=14.6,
        color=DARK,
        align=PP_ALIGN.CENTER,
    )
    add_footer(slide, spec.source)
    return slide


def flc_trial_slide(prs, blank):
    spec = SLIDES[29]
    slide = prs.slides.add_slide(blank)
    add_title(slide, spec.title, size=22)
    panel(slide, 0.58, 0.98, 12.10, 0.82, fill=PALE_RED, line=RED)
    textbox(
        slide,
        0.90,
        1.14,
        11.46,
        0.46,
        "ClinicalTrials.gov lists NCT06620302 as suspended for “Unacceptable Toxicity”; status verified August 2026.",
        size=15.2,
        bold=True,
        color=RED,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    panel(slide, 0.58, 2.08, 5.92, 4.28, fill=WHITE, line=LINE)
    add_label(slide, 0.88, 2.39, 1.92, "Registered design", fill=NAVY, size=10.5)
    add_bullets(
        slide,
        0.92,
        3.08,
        5.18,
        (
            "Phase 1 dose escalation in recurrent or refractory solid tumors",
            "Phase 2 feasibility cohort restricted to molecularly confirmed FLC",
            "DT2216 combined with irinotecan in 21-day cycles",
        ),
        size=14.4,
        gap=0.94,
        accent=NAVY,
    )
    panel(slide, 6.77, 2.08, 5.91, 4.28, fill=PALE_BLUE, line=LINE)
    add_label(slide, 7.08, 2.39, 1.92, "Current reading", fill=RED, size=10.5)
    add_bullets(
        slide,
        7.10,
        3.08,
        5.18,
        (
            "Enrollment and dosing are not presented as active",
            "No assumption is made about cause beyond the registry wording",
            "No restart timing or future readout is assumed",
        ),
        size=14.4,
        gap=0.94,
        accent=RED,
    )
    add_footer(slide, spec.source)
    return slide


def catalyst_slide(prs, blank):
    spec = SLIDES[30]
    slide = prs.slides.add_slide(blank)
    add_title(slide, spec.title, size=20.0)
    rows = [
        ("COMPLETED", "First-in-human dose escalation; 0.40 mg/kg twice-weekly recommended dose; Phase 1 publication", GREEN, PALE_TEAL),
        ("ACTIVE", "Ovarian Phase 1b recruiting; estimated primary completion December 30, 2026", TEAL, PALE_TEAL),
        ("SUSPENDED", "FLC Phase 1/2; registry reason: unacceptable toxicity", RED, PALE_RED),
        ("PLANNED", "CTCL, ER-positive breast cancer and next-generation degraders; timing is a company estimate", GOLD, PALE_GOLD),
    ]
    for index, (status, text, color, fill) in enumerate(rows):
        y = 1.23 + index * 1.34
        panel(slide, 0.62, y, 12.02, 1.05, fill=fill, line=color)
        textbox(slide, 0.88, y + 0.27, 1.82, 0.48, status, size=14.4, bold=True, color=color, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        textbox(slide, 3.05, y + 0.19, 9.12, 0.65, text, size=14.4, color=DARK, valign=MSO_ANCHOR.MIDDLE)
    add_footer(slide, spec.source)
    return slide


def questions_slide(prs, blank):
    spec = SLIDES[31]
    slide = prs.slides.add_slide(blank)
    add_title(slide, spec.title)
    answers = (
        "Phase 1 measured peripheral-leukocyte pharmacodynamics. Tumor exposure and degradation remain unproven.",
        "Transient thrombocytopenia was observed in Phase 1. Combination tolerability and recovery kinetics are central.",
        "The registered study is single arm. Activity will be interpreted against prior weekly-paclitaxel experience.",
        "The submitted manuscript includes several ovarian models, but durable regressions remain preclinical.",
    )
    for index, (question, answer) in enumerate(zip(spec.body, answers), 1):
        y = 1.10 + (index - 1) * 1.38
        panel(slide, 0.54, y, 12.18, 1.15, fill=WHITE if index % 2 else LIGHT, line=LINE)
        textbox(slide, 0.76, y + 0.22, 0.52, 0.48, str(index), size=20, bold=True, color=TEAL, align=PP_ALIGN.CENTER)
        textbox(slide, 1.40, y + 0.16, 4.72, 0.72, question, size=14.0, bold=True, color=NAVY, valign=MSO_ANCHOR.MIDDLE)
        textbox(slide, 6.32, y + 0.16, 5.98, 0.72, answer, size=12.8, color=DARK, valign=MSO_ANCHOR.MIDDLE)
    add_footer(slide, spec.source, "Submitted-manuscript data are confidential and not peer reviewed.")
    return slide


def ip_slide(prs, blank):
    spec = SLIDES[32]
    slide = prs.slides.add_slide(blank)
    add_title(slide, spec.title, size=19.5)
    columns = [
        ("DT2216", "UAMS", spec.body[0], NAVY, PALE_BLUE),
        ("DT5321", "University of Florida", spec.body[1], TEAL, PALE_TEAL),
        ("PATENT STRATEGY", "Company report", spec.body[2], DEEP_TEAL, LIGHT),
    ]
    for index, (heading, owner, text, color, fill) in enumerate(columns):
        x = 0.52 + index * 4.24
        panel(slide, x, 1.20, 3.98, 5.02, fill=fill, line=color)
        textbox(slide, x + 0.30, 1.58, 3.38, 0.46, heading, size=19, bold=True, color=color, align=PP_ALIGN.CENTER)
        textbox(slide, x + 0.30, 2.15, 3.38, 0.40, owner, size=13.5, bold=True, color=MID, align=PP_ALIGN.CENTER)
        textbox(slide, x + 0.38, 2.95, 3.22, 1.88, text.split(" | ", 1)[-1], size=14.2, color=DARK, align=PP_ALIGN.CENTER)
        if index == 2:
            textbox(
                slide,
                x + 0.38,
                5.22,
                3.22,
                0.52,
                "Subject to legal diligence",
                size=12.4,
                bold=True,
                color=RED,
                align=PP_ALIGN.CENTER,
            )
    add_footer(slide, spec.source, spec.status_note)
    return slide


def collaboration_slide(prs, blank):
    spec = SLIDES[33]
    slide = prs.slides.add_slide(blank)
    add_title(slide, spec.title, size=20.2)
    groups = [
        (
            "DT2216",
            DEEP_TEAL,
            PALE_TEAL,
            (
                "Ovarian and endometrial cancer",
                "Fibrolamellar carcinoma",
                "Cutaneous T-cell lymphoma",
                "Pancreatic and other BCL-XL-dependent settings",
            ),
        ),
        (
            "DT5321",
            NAVY,
            PALE_BLUE,
            (
                "Leukemia and Richter transformation",
                "Prostate cancer",
                "Myeloproliferative neoplasms",
            ),
        ),
        (
            "THIRD GENERATION",
            GOLD,
            PALE_GOLD,
            (
                "Oral degrader research",
                "Broader BCL-family targeting",
                "Additional solid and hematologic indications",
            ),
        ),
    ]
    for index, (heading, color, fill, items) in enumerate(groups):
        x = 0.52 + index * 4.24
        panel(slide, x, 1.20, 3.98, 5.02, fill=fill, line=color)
        textbox(slide, x + 0.30, 1.58, 3.38, 0.48, heading, size=18, bold=True, color=color, align=PP_ALIGN.CENTER)
        add_bullets(slide, x + 0.38, 2.45, 3.20, items, size=14.2, gap=0.80, accent=color)
    add_footer(slide, spec.source, spec.status_note)
    return slide


def publications_slide(prs, blank):
    spec = SLIDES[34]
    slide = prs.slides.add_slide(blank)
    add_title(slide, spec.title)
    sections = [
        (
            "CLINICAL",
            DEEP_TEAL,
            PALE_TEAL,
            (
                "Mahadevan et al. | Journal of Hematology & Oncology | 2025",
                "First-in-human Phase 1 study of DT2216",
            ),
        ),
        (
            "OVARIAN MECHANISM",
            NAVY,
            PALE_BLUE,
            (
                "Qin et al. | bioRxiv preprint | 2025",
                "Qin et al. | confidential submitted manuscript | July 2026",
            ),
        ),
        (
            "PLATFORM FOUNDATION",
            GOLD,
            PALE_GOLD,
            (
                "Khan et al. | Nature Medicine | 2019",
                "He et al. | Journal of Hematology & Oncology | 2020",
                "Shebl et al. | JCI Insight | 2022",
                "Lv et al. | Journal of Hematology & Oncology | 2022",
            ),
        ),
    ]
    heights = (1.25, 1.55, 2.05)
    y = 1.15
    for (heading, color, fill, items), height in zip(sections, heights):
        panel(slide, 0.65, y, 12.0, height, fill=fill, line=color)
        textbox(slide, 0.95, y + 0.28, 2.25, 0.48, heading, size=14.5, bold=True, color=color, valign=MSO_ANCHOR.MIDDLE)
        textbox(slide, 3.45, y + 0.22, 8.78, height - 0.36, "\n".join(items), size=13.5, color=DARK, valign=MSO_ANCHOR.MIDDLE)
        y += height + 0.28
    add_footer(slide, spec.source)
    return slide


def update_cover_date(prs):
    for shape in prs.slides[0].shapes:
        if not shape.has_text_frame:
            continue
        for paragraph in shape.text_frame.paragraphs:
            for run in paragraph.runs:
                run.text = run.text.replace("September 3, 2026", "September 4, 2026")
                run.text = run.text.replace(
                    "Creating Innovative and New Technologies to Treat Cancer",
                    "Creating Innovative Technologies to Treat Cancer",
                )


def update_preserved_text(prs):
    replacements = {
        "company Phase 1b/2 protocol": "company Phase 1b protocol",
    }
    clear_text = {
        "A mechanism-matched ovarian combination is now being tested in patients.",
        "The RAS precedent illustrates the potential value of changing how a difficult target is engaged.",
        "Recently produced platelets are less primed and less dependent on BCL-XL; megakaryocytes have low VHL expression.",
        "The combination functionally co-targets BCL-XL and MCL-1 without administering a direct MCL-1 inhibitor.",
        "MCL-1 falls during mitotic arrest, while BCL-XL dependence rises in the same cells.",
        "The current clinical program remains DT2216 plus weekly paclitaxel.",
        "NCT06964009 is testing DT2216 with weekly paclitaxel in recurrent platinum-resistant ovarian cancer.",
    }
    for slide in prs.slides:
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            if shape.text_frame.text.strip() in clear_text:
                shape.text_frame.clear()
                continue
            for paragraph in shape.text_frame.paragraphs:
                for run in paragraph.runs:
                    for old, new in replacements.items():
                        run.text = run.text.replace(old, new)


def set_page_numbers(prs):
    base.set_page_numbers(prs)


def build() -> Path:
    if not SRC.exists():
        raise FileNotFoundError(SRC)
    prepare_assets()
    shutil.copy2(SRC, DST)
    prs = Presentation(str(DST))
    if len(prs.slides) != 34:
        raise RuntimeError(f"Expected 34 slides, found {len(prs.slides)}")
    blank = prs.slide_layouts[7]

    builders = {
        3: overview_slide,
        4: summary_slide,
        5: rvmd_slide,
        6: leadership_slide,
        7: pipeline_slide,
        8: target_slide,
        9: mechanism_slide,
        10: duration_slide,
        11: pkpd_slide,
        12: comparison_slide,
        14: tissue_slide,
        15: evidence_map_slide,
        16: portfolio_slide,
        23: lambda p, b: evidence_image_slide(p, b, 23, "slide23-flc.jpg", 8.45),
        24: lambda p, b: evidence_image_slide(p, b, 24, "slide24-ctcl.jpg", 8.55),
        25: lambda p, b: evidence_image_slide(p, b, 25, "slide25-erbc.jpg", 8.68),
        28: ovarian_trial_slide,
        29: flc_trial_slide,
        30: catalyst_slide,
        31: questions_slide,
        32: ip_slide,
        33: collaboration_slide,
        34: publications_slide,
    }

    original_entries = list(prs.slides._sldIdLst)
    appended_indices: dict[int, int] = {}
    for number, builder in builders.items():
        builder(prs, blank)
        appended_indices[number] = len(prs.slides) - 1

    all_entries = list(prs.slides._sldIdLst)
    order = []
    for number in range(1, 35):
        order.append(appended_indices.get(number, number - 1))
    if len(order) != 34 or len(set(order)) != 34:
        raise RuntimeError(f"Invalid final order: {order}")

    keep = set(order)
    for index, entry in enumerate(all_entries):
        if index not in keep:
            prs.part.drop_rel(entry.get(qn("r:id")))
    slide_list = prs.slides._sldIdLst
    for entry in list(slide_list):
        slide_list.remove(entry)
    for index in order:
        slide_list.append(all_entries[index])

    update_cover_date(prs)
    update_preserved_text(prs)
    set_page_numbers(prs)
    prs.save(str(DST))
    check = Presentation(str(DST))
    if len(check.slides) != 34:
        raise RuntimeError(f"Saved deck has {len(check.slides)} slides")
    print(f"saved {DST}")
    print("slides 34")
    print(f"replaced {len(builders)} slides")
    return DST


if __name__ == "__main__":
    build()

