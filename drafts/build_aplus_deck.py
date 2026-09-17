#!/usr/bin/env python3
"""Build the confidential A+ Dialectic investor presentation."""

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


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "drafts" / "Dialectic_Presentation_09.03.26_vDRAFT5.pptx"
DST = ROOT / "drafts" / "Dialectic_Presentation_09.03.26_A_PLUS_DRAFT.pptx"
ASSETS = ROOT / "sources" / "kris-forward-2026-09-03" / "aplus-assets"
AACR = ROOT / "sources" / "sarosiek-figures"

TEAL = RGBColor(0x00, 0xB3, 0x9F)
DEEP_TEAL = RGBColor(0x00, 0x7D, 0x73)
NAVY = RGBColor(0x1F, 0x4E, 0x79)
DARK = RGBColor(0x1F, 0x29, 0x33)
MID = RGBColor(0x4D, 0x5B, 0x66)
LIGHT = RGBColor(0xF1, 0xF5, 0xF6)
PALE_TEAL = RGBColor(0xE5, 0xF5, 0xF2)
PALE_BLUE = RGBColor(0xE8, 0xF0, 0xF7)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
RED = RGBColor(0xB8, 0x42, 0x42)
GOLD = RGBColor(0xC8, 0x8B, 0x2B)
FONT = "Aptos"
FONT_DISPLAY = "Aptos Display"


def set_run(run, text: str, *, size=14, bold=False, color=DARK, italic=False, font=FONT):
    run.text = text
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color


def textbox(
    slide,
    x,
    y,
    w,
    h,
    text="",
    *,
    size=14,
    bold=False,
    color=DARK,
    italic=False,
    font=FONT,
    align=PP_ALIGN.LEFT,
    valign=MSO_ANCHOR.TOP,
    margin=0.03,
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
    run = paragraph.add_run()
    set_run(run, text, size=size, bold=bold, color=color, italic=italic, font=font)
    return shape


def add_title(slide, title: str, subtitle: str | None = None, *, size=23):
    textbox(
        slide,
        1.12,
        0.10,
        10.65,
        0.50,
        title,
        size=size,
        bold=True,
        color=WHITE,
        font=FONT_DISPLAY,
        valign=MSO_ANCHOR.MIDDLE,
    )
    if subtitle:
        textbox(slide, 0.45, 0.76, 12.35, 0.38, subtitle, size=12.5, color=MID, italic=True)


def add_footer(slide, text: str):
    textbox(slide, 0.45, 7.10, 11.35, 0.25, text, size=8.2, color=MID, italic=True)


def add_paragraphs(slide, x, y, w, h, paragraphs, *, size=14, color=DARK, bullet=False):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = shape.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = Inches(0.04)
    frame.margin_right = Inches(0.04)
    frame.margin_top = Inches(0.03)
    frame.margin_bottom = Inches(0.03)
    for index, item in enumerate(paragraphs):
        paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        paragraph.space_after = Pt(7)
        paragraph.level = 0
        if bullet:
            paragraph.text = ""
            paragraph._p.get_or_add_pPr().insert(0, paragraph._p._new_buChar())
        if isinstance(item, str):
            runs = [(item, False)]
        else:
            runs = item
        for text, is_bold in runs:
            run = paragraph.add_run()
            set_run(run, text, size=size, bold=is_bold, color=color)
    return shape


def add_panel(slide, x, y, w, h, *, fill=LIGHT, line=None, radius=True):
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE
    shape = slide.shapes.add_shape(shape_type, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = line or fill
    if radius and hasattr(shape, "adjustments") and len(shape.adjustments):
        shape.adjustments[0] = 0.08
    return shape


def add_metric(slide, x, y, w, value, label, *, color=TEAL, value_size=28):
    textbox(slide, x, y, w, 0.46, value, size=value_size, bold=True, color=color, font=FONT_DISPLAY)
    textbox(slide, x, y + 0.46, w, 0.52, label, size=11.5, color=MID)


def add_picture_contain(slide, path: Path, x, y, w, h):
    with Image.open(path) as image:
        aspect = image.width / image.height
    box_aspect = w / h
    if aspect >= box_aspect:
        width = w
        height = w / aspect
    else:
        height = h
        width = h * aspect
    left = x + (w - width) / 2
    top = y + (h - height) / 2
    return slide.shapes.add_picture(
        str(path),
        Inches(left),
        Inches(top),
        width=Inches(width),
        height=Inches(height),
    )


def add_lane(slide, y, label, middle, result, *, highlight=False, result_color=DARK):
    fill = PALE_TEAL if highlight else LIGHT
    line = TEAL if highlight else RGBColor(0xD5, 0xDD, 0xE1)
    add_panel(slide, 0.48, y, 12.25, 1.24, fill=fill, line=line)
    textbox(slide, 0.72, y + 0.18, 2.65, 0.78, label, size=15, bold=True, color=NAVY, valign=MSO_ANCHOR.MIDDLE)
    textbox(slide, 3.70, y + 0.18, 5.35, 0.78, middle, size=14, color=DARK, valign=MSO_ANCHOR.MIDDLE)
    textbox(
        slide,
        9.35,
        y + 0.18,
        3.05,
        0.78,
        result,
        size=14,
        bold=True,
        color=result_color,
        valign=MSO_ANCHOR.MIDDLE,
    )
    for x in (3.35, 9.00):
        chevron = slide.shapes.add_shape(MSO_SHAPE.CHEVRON, Inches(x), Inches(y + 0.43), Inches(0.22), Inches(0.32))
        chevron.fill.solid()
        chevron.fill.fore_color.rgb = TEAL if highlight else RGBColor(0xA6, 0xB2, 0xB8)
        chevron.line.color.rgb = chevron.fill.fore_color.rgb


def investment_summary(prs, blank):
    slide = prs.slides.add_slide(blank)
    add_title(slide, "Investment Summary")
    textbox(
        slide,
        0.55,
        0.95,
        7.55,
        0.62,
        "DT2216 plus weekly paclitaxel in platinum-resistant ovarian cancer",
        size=21,
        bold=True,
        color=NAVY,
        font=FONT_DISPLAY,
    )
    add_paragraphs(
        slide,
        0.58,
        1.68,
        7.45,
        4.65,
        [
            [
                ("Clinical foundation. ", True),
                ("Phase 1 established 0.40 mg/kg IV twice weekly as the recommended Phase 2 dose and showed rapid BCL-XL reduction in peripheral leukocytes. Monotherapy activity in advanced solid tumors was limited.", False),
            ],
            [
                ("Combination rationale. ", True),
                ("Paclitaxel-induced mitotic arrest reduces MCL-1 and increases dependence on BCL-XL, which DT2216 is designed to degrade.", False),
            ],
            [
                ("Preclinical evidence. ", True),
                ("Seven of eight patient-derived ovarian models showed ex-vivo synergy. DT2216 plus paclitaxel produced durable control in both flank and disseminated DF83 PDX models.", False),
            ],
            [
                ("Clinical value inflection. ", True),
                ("The ongoing Phase 1b/2 study will test combination safety, dose, response rate, durability and tumor pharmacodynamics. Human combination efficacy has not yet been reported.", False),
            ],
        ],
        size=14.3,
    )
    add_panel(slide, 8.42, 1.02, 4.27, 5.65, fill=PALE_BLUE, line=RGBColor(0xC8, 0xD8, 0xE5))
    add_metric(slide, 8.75, 1.40, 3.55, "0.40 mg/kg", "IV twice weekly Phase 1 RP2D", color=NAVY)
    add_metric(slide, 8.75, 2.72, 3.55, "7 of 8", "HGSOC PDX models showed ex-vivo combination synergy", color=TEAL)
    add_metric(slide, 8.75, 4.12, 3.55, "35 days", "Median-survival extension versus paclitaxel in the disseminated DF83 PDX model (preclinical)", color=DEEP_TEAL)
    textbox(
        slide,
        8.75,
        5.62,
        3.55,
        0.66,
        "The central risk is clinical translation of the combination effect.",
        size=12.5,
        bold=True,
        color=RED,
    )
    add_footer(
        slide,
        "Sources: Mahadevan et al., J Hematol Oncol 2025; Qin et al., submitted manuscript, July 2026. Manuscript data are confidential and not peer reviewed.",
    )
    return slide


def platelet_slide(prs, blank):
    slide = prs.slides.add_slide(blank)
    add_title(slide, "Platelet recovery supports intermittent BCL-XL degradation", size=21)
    textbox(
        slide,
        1.08,
        0.76,
        11.45,
        0.38,
        "Recently produced platelets are less primed and less dependent on BCL-XL; megakaryocytes have low VHL expression.",
        size=12.7,
        color=MID,
    )
    add_picture_contain(slide, AACR / "p24-24.png", 0.40, 1.18, 6.12, 5.05)
    add_picture_contain(slide, AACR / "p25-25.png", 6.80, 1.18, 6.10, 5.05)
    textbox(
        slide,
        0.62,
        6.22,
        12.00,
        0.50,
        "The biology supports platelet recovery between doses rather than continuous BCL-XL inhibition.",
        size=13.5,
        bold=True,
        color=NAVY,
        align=PP_ALIGN.CENTER,
    )
    add_footer(
        slide,
        "Sources: Grozovsky, Fraser, Qin et al., Cell Death Dis 2026; Khan et al., Nat Med 2019; Sarosiek AACR 2026.",
    )
    return slide


def science_design_slide(prs, blank):
    slide = prs.slides.add_slide(blank)
    add_title(slide, "DT2216 plus paclitaxel targets complementary survival pathways", size=21)
    textbox(slide, 1.08, 0.76, 11.45, 0.34, "The combination functionally co-targets BCL-XL and MCL-1 without administering a direct MCL-1 inhibitor.", size=13, color=MID)

    add_panel(slide, 0.55, 1.30, 8.25, 4.95, fill=WHITE, line=RGBColor(0xC8, 0xD2, 0xD7), radius=False)
    textbox(slide, 0.85, 1.58, 2.15, 0.48, "Paclitaxel", size=18, bold=True, color=DEEP_TEAL, align=PP_ALIGN.CENTER)
    textbox(slide, 3.25, 1.58, 2.15, 0.48, "Mitotic arrest", size=16, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    textbox(slide, 5.75, 1.58, 2.25, 0.48, "MCL-1 decreases", size=16, bold=True, color=NAVY, align=PP_ALIGN.CENTER)

    textbox(slide, 0.85, 3.24, 2.15, 0.48, "DT2216", size=18, bold=True, color=DEEP_TEAL, align=PP_ALIGN.CENTER)
    textbox(slide, 3.25, 3.17, 2.15, 0.62, "VHL-mediated\ndegradation", size=15, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    textbox(slide, 5.75, 3.24, 2.25, 0.48, "BCL-XL decreases", size=16, bold=True, color=NAVY, align=PP_ALIGN.CENTER)

    for y in (1.66, 3.32):
        for x in (2.90, 5.40):
            chevron = slide.shapes.add_shape(MSO_SHAPE.CHEVRON, Inches(x), Inches(y), Inches(0.24), Inches(0.30))
            chevron.fill.solid()
            chevron.fill.fore_color.rgb = TEAL
            chevron.line.color.rgb = TEAL

    line1 = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(6.88), Inches(2.12), Inches(5.43), Inches(5.02))
    line2 = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(6.88), Inches(3.84), Inches(5.43), Inches(5.02))
    for line in (line1, line2):
        line.line.color.rgb = TEAL
        line.line.width = Pt(2)

    add_panel(slide, 3.40, 4.83, 4.10, 0.82, fill=PALE_TEAL, line=TEAL, radius=False)
    textbox(slide, 3.62, 5.02, 3.66, 0.42, "Apoptosis in ovarian PDX models", size=16, bold=True, color=DEEP_TEAL, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    add_panel(slide, 9.05, 1.30, 3.68, 4.95, fill=LIGHT, line=RGBColor(0xD5, 0xDD, 0xE1), radius=False)
    textbox(slide, 9.35, 1.60, 3.05, 0.43, "Why the combination is needed", size=15.5, bold=True, color=NAVY)
    add_paragraphs(
        slide,
        9.35,
        2.18,
        3.03,
        3.55,
        [
            "BCL-XL targeting alone induces compensatory pro-survival signaling, including MCL-1.",
            "Direct BCL-XL and MCL-1 inhibition produced synergistic apoptosis in 88.6% of 132 tested lines, but was not tolerated in vivo.",
            "Paclitaxel supplies the MCL-1 effect in the current clinical combination.",
        ],
        size=13.0,
    )
    textbox(
        slide,
        0.62,
        6.40,
        12.0,
        0.38,
        "This is the biological basis for the current ovarian clinical program.",
        size=14.5,
        bold=True,
        color=NAVY,
        align=PP_ALIGN.CENTER,
    )
    add_footer(
        slide,
        "Source: Qin et al., submitted manuscript, July 2026, Figs. 1–3. Direct dual-inhibitor data are mechanistic context, not the clinical regimen. Confidential; not peer reviewed.",
    )
    return slide


def mechanism_slide(prs, blank):
    slide = prs.slides.add_slide(blank)
    add_title(slide, "Paclitaxel moves surviving HGSOC cells onto BCL-XL", size=22)
    textbox(
        slide,
        1.08,
        0.78,
        11.45,
        0.34,
        "MCL-1 falls during mitotic arrest, while BCL-XL dependence rises in the same cells.",
        size=13,
        color=MID,
    )
    add_picture_contain(slide, AACR / "p28-28.png", 0.35, 1.15, 6.25, 4.95)
    add_picture_contain(slide, AACR / "p29-29.png", 6.73, 1.15, 6.22, 4.95)
    textbox(slide, 0.48, 6.07, 5.95, 0.50, "Paclitaxel reduced MCL-1 and produced the BCL-XL phospho-shift.", size=12.3, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    textbox(slide, 6.88, 6.07, 5.85, 0.50, "Mitotically arrested cells showed greater BCL-XL dependence by BH3 profiling.", size=12.3, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    add_footer(slide, "Source: Qin et al., submitted manuscript, July 2026, Figs. 3 and 5; Sarosiek AACR 2026. Confidential; not peer reviewed.")
    return slide


def pdx_breadth_slide(prs, blank):
    slide = prs.slides.add_slide(blank)
    add_title(slide, "Seven of eight patient-derived ovarian models showed combination synergy ex vivo", size=19.5)
    add_picture_contain(slide, ASSETS / "figure6D-pdx-breadth.png", 0.35, 1.02, 8.95, 5.88)
    add_panel(slide, 9.48, 1.12, 3.25, 5.55, fill=PALE_BLUE, line=RGBColor(0xC8, 0xD8, 0xE5))
    add_metric(slide, 9.78, 1.52, 2.68, "7 of 8", "PDX models showed synergy at one or more tested dose combinations", color=TEAL, value_size=30)
    add_metric(slide, 9.78, 3.05, 2.68, "0 to 7", "Prior chemotherapy lines represented across the models", color=NAVY, value_size=27)
    add_metric(slide, 9.78, 4.58, 2.68, "5 of 8", "Met the manuscript threshold for DT2216 single-agent sensitivity", color=DEEP_TEAL, value_size=27)
    add_footer(
        slide,
        "Source: Qin et al., submitted manuscript, July 2026, Fig. 6D. Short-term ex-vivo assay; one biological replicate shown and reproduced in a second. Confidential; not peer reviewed.",
    )
    return slide


def df83_slide(prs, blank):
    slide = prs.slides.add_slide(blank)
    add_title(slide, "DT2216 plus paclitaxel produced durable control in two DF83 PDX settings", size=20)

    add_panel(slide, 0.45, 0.95, 6.10, 4.50, fill=WHITE, line=RGBColor(0xD5, 0xDD, 0xE1), radius=False)
    textbox(slide, 0.70, 1.18, 5.60, 0.30, "Flank PDX", size=15, bold=True, color=NAVY)
    add_picture_contain(slide, ASSETS / "figure8F-flank-volume.png", 0.72, 1.56, 5.55, 2.75)
    textbox(
        slide,
        0.72,
        4.42,
        5.55,
        0.72,
        "Complete regression. DT2216 stopped at day 138, with no regrowth during the following 100 days.",
        size=13.0,
        bold=True,
        color=DARK,
    )

    add_panel(slide, 6.77, 0.95, 6.10, 4.50, fill=WHITE, line=RGBColor(0xD5, 0xDD, 0xE1), radius=False)
    textbox(slide, 7.02, 1.18, 5.60, 0.30, "Disseminated intraperitoneal PDX", size=15, bold=True, color=NAVY)
    add_picture_contain(slide, ASSETS / "figure8Q-ip-burden.png", 7.02, 1.56, 5.55, 2.75)
    textbox(
        slide,
        7.02,
        4.42,
        5.55,
        0.72,
        "Tumor signal reached background levels by day 40. Median survival increased 35 days versus paclitaxel.",
        size=13.0,
        bold=True,
        color=DARK,
    )

    add_panel(slide, 0.50, 5.76, 12.20, 0.92, fill=PALE_TEAL, line=RGBColor(0xB6, 0xDE, 0xD8), radius=False)
    textbox(
        slide,
        0.78,
        5.94,
        11.45,
        0.52,
        "The intraperitoneal model more closely reproduces disseminated ovarian growth and ascites. Both studies remain preclinical.",
        size=13.4,
        bold=True,
        color=DARK,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_footer(
        slide,
        "Source: Qin et al., submitted manuscript, July 2026, Fig. 8F–H and 8P–S. Confidential and not peer reviewed.",
    )
    return slide


def breadth_slide(prs, blank):
    slide = prs.slides.add_slide(blank)
    add_title(slide, "DT2216 plus paclitaxel showed in-vitro synergy across 55 cell lines and 12 tumor types", size=18.5)
    add_picture_contain(slide, ASSETS / "figure3F-paclitaxel-breadth.png", 0.35, 1.02, 8.70, 5.90)
    add_panel(slide, 9.26, 1.15, 3.43, 5.47, fill=PALE_BLUE, line=RGBColor(0xC8, 0xD8, 0xE5))
    add_metric(slide, 9.58, 1.52, 2.85, "55 of 55", "Cell lines showed synergy at one or more tested dose combinations", color=TEAL, value_size=28)
    add_metric(slide, 9.58, 3.02, 2.85, "12", "Tumor types represented", color=NAVY, value_size=30)
    add_metric(slide, 9.58, 4.34, 2.85, "10.7", "Average excess over Bliss; range -19.1 to 68.0", color=DEEP_TEAL, value_size=28)
    textbox(
        slide,
        9.58,
        5.62,
        2.82,
        0.78,
        "Non-ovarian evidence is in vitro. Some tested dose combinations were antagonistic.",
        size=10.8,
        bold=True,
        color=RED,
        align=PP_ALIGN.CENTER,
    )
    add_footer(
        slide,
        "Source: Qin et al., submitted manuscript, July 2026, Fig. 3F and Fig. S3H. Both wild-type and mutant TP53 cell lines were included. Confidential; not peer reviewed.",
    )
    return slide


def adc_payload_slide(prs, blank):
    slide = prs.slides.add_slide(blank)
    add_title(slide, "DT2216 increased apoptosis with three microtubule ADC payloads in OVCAR8", size=19)
    textbox(
        slide,
        1.08,
        0.76,
        11.45,
        0.40,
        "The current clinical program remains DT2216 plus weekly paclitaxel.",
        size=12.7,
        bold=True,
        color=NAVY,
    )
    add_picture_contain(slide, ASSETS / "figure4F-adc-payloads.png", 0.38, 1.16, 7.45, 4.95)
    textbox(slide, 0.52, 6.02, 7.15, 0.45, "DT2216 combined with DM4, MMAE and MMAF increased apoptosis in OVCAR8 cells.", size=12.5, bold=True, color=NAVY, align=PP_ALIGN.CENTER)

    add_picture_contain(slide, ASSETS / "figure4E-specificity.png", 8.05, 1.20, 4.72, 3.20)
    textbox(
        slide,
        8.15,
        4.37,
        4.48,
        1.55,
        "MMAF-induced apoptosis increased with BCL-XL inhibition or degradation. Selective BCL-2 or MCL-1 inhibition did not produce the same effect.",
        size=13.1,
        color=DARK,
    )
    textbox(
        slide,
        8.15,
        5.95,
        4.48,
        0.70,
        "DM4 is the payload used by mirvetuximab soravtansine (Elahere). Free payload was tested; the intact ADC was not.",
        size=12.0,
        bold=True,
        color=RED,
    )
    add_footer(
        slide,
        "Source: Qin et al., submitted manuscript, July 2026, Fig. 4E–F. Fig. 4E n=3; Fig. 4F DM4/MMAE n=3 and MMAF n=1 biological replicate. In vitro. Confidential; not peer reviewed.",
    )
    return slide


def phase1_slide(prs, blank):
    slide = prs.slides.add_slide(blank)
    add_title(slide, "Phase 1 established a human dose and systemic target engagement", size=21)
    add_metric(slide, 0.65, 1.16, 3.15, "20", "Heavily pretreated patients enrolled", color=NAVY, value_size=34)
    add_metric(slide, 4.10, 1.16, 3.80, "0.40 mg/kg", "IV twice weekly recommended Phase 2 dose", color=TEAL, value_size=30)
    add_metric(slide, 8.35, 1.16, 4.15, "Rapid reduction", "BCL-XL in peripheral leukocytes at the RP2D", color=DEEP_TEAL, value_size=25)

    add_panel(slide, 0.55, 2.62, 6.05, 3.72, fill=PALE_TEAL, line=RGBColor(0xB6, 0xDE, 0xD8))
    textbox(slide, 0.85, 2.94, 5.45, 0.38, "Safety and pharmacology", size=16, bold=True, color=DEEP_TEAL)
    add_paragraphs(
        slide,
        0.85,
        3.42,
        5.38,
        2.45,
        [
            "Thrombocytopenia occurred in 9 of 20 patients. One dose-limiting grade 4 event resolved within 48 hours.",
            "No major bleeding events, treatment-related deaths or platelet transfusions were reported.",
            "Plasma exposure was dose proportional, with no accumulation on twice-weekly dosing.",
        ],
        size=13.3,
    )

    add_panel(slide, 6.78, 2.62, 5.95, 3.72, fill=PALE_BLUE, line=RGBColor(0xC8, 0xD8, 0xE5))
    textbox(slide, 7.08, 2.94, 5.35, 0.38, "Antitumor activity", size=16, bold=True, color=NAVY)
    add_paragraphs(
        slide,
        7.08,
        3.42,
        5.28,
        2.45,
        [
            "DT2216 did not demonstrate single-agent activity in advanced solid tumors.",
            "Stable disease was the best RECIST response in 4 of 20 patients, with a median duration of 107 days.",
            "The Phase 1 result supports development with a mechanism-matched combination rather than monotherapy.",
        ],
        size=13.3,
    )
    add_footer(slide, "Source: Mahadevan et al., J Hematol Oncol 2025; NCT04886622.")
    return slide


def translation_slide(prs, blank):
    slide = prs.slides.add_slide(blank)
    add_title(slide, "Phase 1 established systemic pharmacodynamics; Phase 1b will test tumor pharmacodynamics", size=18.5)

    add_panel(slide, 0.55, 1.05, 5.95, 4.75, fill=LIGHT, line=RGBColor(0xD5, 0xDD, 0xE1))
    textbox(slide, 0.88, 1.38, 5.35, 0.40, "Preclinical efficacy exposure", size=16, bold=True, color=NAVY)
    add_paragraphs(
        slide,
        0.88,
        1.95,
        5.32,
        2.75,
        [
            [("DF83 regimen: ", True), ("DT2216 15 mg/kg IP every four days with paclitaxel.", False)],
            [("Current manuscript: ", True), ("Flank treatment stopped at day 138, followed by 100 days without regrowth.", False)],
            [("Limitation: ", True), ("The mouse dose and route cannot be converted directly into the human RP2D.", False)],
        ],
        size=14,
    )

    add_panel(slide, 6.82, 1.05, 5.95, 4.75, fill=PALE_TEAL, line=RGBColor(0xB6, 0xDE, 0xD8))
    textbox(slide, 7.15, 1.38, 5.35, 0.40, "Human Phase 1 pharmacodynamics", size=16, bold=True, color=DEEP_TEAL)
    add_paragraphs(
        slide,
        7.15,
        1.95,
        5.30,
        2.75,
        [
            [("Human regimen: ", True), ("DT2216 0.40 mg/kg IV twice weekly.", False)],
            [("Measured effect: ", True), ("Rapid and persistent BCL-XL reduction in peripheral leukocytes in four patients at the RP2D.", False)],
            [("Remaining question: ", True), ("Tumor exposure and BCL-XL degradation have not been demonstrated in patients.", False)],
        ],
        size=14,
    )

    add_panel(slide, 1.05, 6.02, 11.22, 0.78, fill=PALE_BLUE, line=RGBColor(0xC8, 0xD8, 0xE5))
    textbox(
        slide,
        1.30,
        6.19,
        10.72,
        0.42,
        "The ovarian study measures BCL-XL in PBMCs and evaluates tumor genetics and pro- and anti-apoptotic proteins.",
        size=14,
        bold=True,
        color=NAVY,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_footer(slide, "Sources: Qin et al., submitted manuscript, July 2026; Mahadevan et al., J Hematol Oncol 2025; company Phase 1b/2 protocol. Manuscript confidential; not peer reviewed.")
    return slide


def ovarian_trial_slide(prs, blank):
    slide = prs.slides.add_slide(blank)
    add_title(slide, "The Phase 1b/2 study directly tests DT2216 plus weekly paclitaxel in PROC", size=20)
    textbox(slide, 1.08, 0.80, 11.45, 0.34, "Lead site: Dana-Farber Cancer Institute", size=13, color=MID)

    add_panel(slide, 0.48, 1.22, 12.28, 2.18, fill=PALE_TEAL, line=RGBColor(0xB6, 0xDE, 0xD8))
    textbox(slide, 0.75, 1.48, 1.72, 0.52, "Phase 1b", size=20, bold=True, color=DEEP_TEAL, valign=MSO_ANCHOR.MIDDLE)
    textbox(slide, 2.42, 1.43, 2.55, 0.82, "Approximately 30 patients\nBOIN dose escalation", size=13.5, bold=True, color=DARK, valign=MSO_ANCHOR.MIDDLE)
    textbox(slide, 5.10, 1.37, 3.50, 1.20, "DT2216: 0.32 or 0.40 mg/kg IV twice weekly\nPaclitaxel: 70 or 80 mg/m² IV weekly", size=13.2, color=DARK, valign=MSO_ANCHOR.MIDDLE)
    textbox(slide, 8.92, 1.37, 3.43, 1.20, "Primary endpoint: recommended combination dose\nSecondary: safety, ORR, duration and PFS", size=13.2, color=DARK, valign=MSO_ANCHOR.MIDDLE)

    add_panel(slide, 0.48, 3.72, 12.28, 2.38, fill=PALE_BLUE, line=RGBColor(0xC8, 0xD8, 0xE5))
    textbox(slide, 0.75, 4.02, 1.72, 0.52, "Phase 2", size=20, bold=True, color=NAVY, valign=MSO_ANCHOR.MIDDLE)
    textbox(slide, 2.42, 3.96, 2.55, 0.92, "Approximately 40–60 patients\nSimon two-stage design", size=13.5, bold=True, color=DARK, valign=MSO_ANCHOR.MIDDLE)
    textbox(slide, 5.10, 3.89, 3.50, 1.35, "High-grade epithelial ovarian cancer\nUp to four prior cytotoxic lines\nNo prior weekly paclitaxel", size=13.0, color=DARK, valign=MSO_ANCHOR.MIDDLE)
    textbox(slide, 8.92, 3.89, 3.43, 1.35, "Primary endpoint: ORR by RECIST v1.1\nSecondary: safety, duration, PFS and OS\nTumor and PBMC pharmacodynamics", size=13.0, color=DARK, valign=MSO_ANCHOR.MIDDLE)

    textbox(
        slide,
        0.62,
        6.32,
        12.00,
        0.52,
        "The single-arm design will be judged against historical weekly-paclitaxel activity. No DT2216 combination response rate has been reported.",
        size=13.0,
        bold=True,
        color=RED,
        align=PP_ALIGN.CENTER,
    )
    add_footer(slide, "Source: Company protocol. Historical weekly-paclitaxel ORR in PROC is approximately 13–20%; cross-trial comparisons are descriptive.")
    return slide


def questions_slide(prs, blank):
    slide = prs.slides.add_slide(blank)
    add_title(slide, "Key questions for the ovarian program")
    questions = [
        (
            "Does the human regimen reproduce tumor BCL-XL degradation?",
            "Phase 1 showed peripheral-leukocyte pharmacodynamics. The Phase 1b tumor assays are intended to test the remaining translation question.",
        ),
        (
            "Does the combination improve meaningfully on weekly paclitaxel?",
            "The Phase 2 study is single arm. Response rate, durability and PFS will be interpreted against historical experience rather than a randomized control.",
        ),
        (
            "Can dose intensity be maintained through repeated cycles?",
            "DT2216 caused transient thrombocytopenia in Phase 1. Combination tolerability and recovery kinetics remain central clinical endpoints.",
        ),
        (
            "Is the preclinical effect reproducible in patients?",
            "The submitted manuscript includes multiple ovarian models, but the durable regressions remain preclinical and the manuscript is not yet peer reviewed.",
        ),
    ]
    y = 1.12
    for number, (question, answer) in enumerate(questions, 1):
        add_panel(slide, 0.55, y, 12.18, 1.24, fill=WHITE if number % 2 else LIGHT, line=RGBColor(0xD5, 0xDD, 0xE1), radius=False)
        textbox(slide, 0.77, y + 0.18, 0.45, 0.45, str(number), size=19, bold=True, color=TEAL, align=PP_ALIGN.CENTER)
        textbox(slide, 1.35, y + 0.16, 4.65, 0.78, question, size=14.0, bold=True, color=NAVY, valign=MSO_ANCHOR.MIDDLE)
        textbox(slide, 6.17, y + 0.16, 6.18, 0.78, answer, size=12.8, color=DARK, valign=MSO_ANCHOR.MIDDLE)
        y += 1.38
    add_footer(slide, "Sources: Mahadevan et al., J Hematol Oncol 2025; Qin et al., submitted manuscript, July 2026; company Phase 1b/2 protocol. Manuscript confidential; not peer reviewed.")
    return slide


def set_page_numbers(prs):
    for number, slide in enumerate(prs.slides, 1):
        found = False
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            compact = shape.text_frame.text.replace("\n", "").replace(" ", "").strip()
            if compact.isdigit() and shape.left > Inches(11.4) and shape.top > Inches(6.55):
                shape.text_frame.text = str(number)
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        run.font.name = FONT
                        run.font.size = Pt(11)
                        run.font.bold = False
                        run.font.color.rgb = WHITE
                found = True
        if not found and number > 1:
            textbox(slide, 12.18, 7.10, 0.38, 0.22, str(number), size=10.5, color=WHITE, align=PP_ALIGN.CENTER)


def update_toc(prs):
    slide = prs.slides[2]
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        for paragraph in shape.text_frame.paragraphs:
            for run in paragraph.runs:
                if "What Still Has to Be Proven" in run.text:
                    run.text = run.text.replace("What Still Has to Be Proven", "Key Questions for the Ovarian Program")


def update_legacy_text(prs):
    replacements = {
        "Qin X et al. bioRxiv 2025": "Qin et al., submitted manuscript, July 2026",
        "Qin et al. bioRxiv 2025": "Qin et al., submitted manuscript, July 2026",
        "Dosing stopped day 130; no tumor detectable day 236": (
            "Current submitted manuscript: DT2216 stopped at day 138; no regrowth was observed during the following 100 days"
        ),
        "DT2216 is effective against a wide variety of cancers, particularly in combination with other chemotherapeutics, indicating the potential for broad clinical application. It was approved by the FDA as an IND in 2021 to treat relapsed/refractory malignancies.": (
            "Preclinical studies have evaluated DT2216 across multiple cancer models, most often in combination. The DT2216 IND became effective in 2021 for relapsed or refractory malignancies."
        ),
        "Paclitaxel exposure induces BCL-XL dependence in chemoresistant HGSOC; DT2216 synergizes only after that exposure (BH3 profiling, Sarosiek lab)": (
            "Paclitaxel exposure increases BCL-XL dependence in chemoresistant HGSOC and enhances apoptosis with DT2216 (BH3 profiling, Sarosiek lab)"
        ),
        "Strong IP in the BCL family of proteins and proven safety superiority related to conventional inhibitors (e.g., Navitoclax": (
            "Licensed patent estate covering DT2216, DT5321 and related BCL-family degraders"
        ),
        "Licensed patent estate covering DT2216, DT5321 and related BCL-family degraders)": (
            "Licensed patent estate covering DT2216, DT5321 and related BCL-family degraders"
        ),
        "IP Strategy: Own the Entire APTaD Selection/Degradation Platform and Maintain Leadership Position in this Class of Therapeutic": (
            "IP strategy: extend protection through successive APTaD generations, analogs and internally developed IP"
        ),
    }
    for slide in prs.slides:
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            for paragraph in shape.text_frame.paragraphs:
                full_text = paragraph.text
                for old, new in replacements.items():
                    if old in full_text and not any(old in run.text for run in paragraph.runs):
                        if paragraph.runs:
                            paragraph.runs[0].text = full_text.replace(old, new)
                            for extra in paragraph.runs[1:]:
                                extra._r.getparent().remove(extra._r)
                        break
                for run in paragraph.runs:
                    for old, new in replacements.items():
                        if old in run.text:
                            run.text = run.text.replace(old, new)


def main():
    shutil.copy2(SRC, DST)
    prs = Presentation(str(DST))
    if len(prs.slides) != 34:
        raise RuntimeError(f"Expected 34-slide vDRAFT5, found {len(prs.slides)}")
    blank = prs.slide_layouts[7]

    new_slides = {
        "summary": investment_summary(prs, blank),
        "s13": platelet_slide(prs, blank),
        "s17": science_design_slide(prs, blank),
        "s18": mechanism_slide(prs, blank),
        "s19": pdx_breadth_slide(prs, blank),
        "s20": df83_slide(prs, blank),
        "s21": breadth_slide(prs, blank),
        "s22": adc_payload_slide(prs, blank),
        "s26": phase1_slide(prs, blank),
        "s27": translation_slide(prs, blank),
        "s28": ovarian_trial_slide(prs, blank),
        "s31": questions_slide(prs, blank),
    }

    entries = list(prs.slides._sldIdLst)
    # Appended slides begin at entry 34 in insertion order.
    appended = {name: 34 + i for i, name in enumerate(new_slides)}

    order = (
        [0, 1, 2, appended["summary"]]
        + list(range(4, 12))
        + [appended["s13"]]
        + list(range(13, 16))
        + [appended[f"s{n}"] for n in range(17, 23)]
        + list(range(22, 25))
        + [appended["s26"], appended["s27"], appended["s28"]]
        + [28, 29, appended["s31"], 31, 32, 33]
    )
    if len(order) != 34 or len(set(order)) != 34:
        raise RuntimeError(f"Bad final order: {order}")

    keep = set(order)
    slide_list = prs.slides._sldIdLst
    for index, entry in enumerate(entries):
        if index not in keep:
            prs.part.drop_rel(entry.get(qn("r:id")))
    for entry in list(slide_list):
        slide_list.remove(entry)
    for index in order:
        slide_list.append(entries[index])

    update_toc(prs)
    update_legacy_text(prs)
    set_page_numbers(prs)
    prs.save(str(DST))
    print(f"saved {DST}")
    print(f"slides {len(Presentation(str(DST)).slides)}")


if __name__ == "__main__":
    main()
