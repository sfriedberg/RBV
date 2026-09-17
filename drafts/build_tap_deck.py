#!/usr/bin/env python3
"""Build the non-confidential TAP inquiry deck from the 1 Sep 2026 1-pager."""

from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

DST = Path(__file__).resolve().parent / "Dialectic_TAP_CTCL_nonconfidential_091426.pptx"

TEAL = RGBColor(0x00, 0x7D, 0x73)
DEEP = RGBColor(0x0B, 0x3D, 0x3A)
NAVY = RGBColor(0x1F, 0x4E, 0x79)
DARK = RGBColor(0x1F, 0x29, 0x33)
MID = RGBColor(0x4D, 0x5B, 0x66)
LIGHT = RGBColor(0xF1, 0xF5, 0xF6)
PALE = RGBColor(0xE5, 0xF5, 0xF2)
PALE_GOLD = RGBColor(0xFB, 0xF5, 0xE8)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
AMBER = RGBColor(0x8A, 0x5A, 0x12)
RED = RGBColor(0x8B, 0x3A, 0x3A)
LINE = RGBColor(0xD5, 0xDD, 0xE1)
FONT = "Calibri"
DISPLAY = "Calibri"


def rgb_fill(shape, color, line=None):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.color.rgb = line or color


def textbox(slide, x, y, w, h, text, *, size=14, bold=False, color=DARK, italic=False, font=FONT, align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.TOP, margin=0.04):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = shape.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = Inches(margin)
    frame.margin_right = Inches(margin)
    frame.margin_top = Inches(margin)
    frame.margin_bottom = Inches(margin)
    frame.vertical_anchor = valign
    p = frame.paragraphs[0]
    p.alignment = align
    p.space_after = Pt(0)
    run = p.add_run()
    run.text = text
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return shape


def add_runs(slide, x, y, w, h, lines, *, size=13.5, color=DARK, valign=MSO_ANCHOR.TOP):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = shape.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = Inches(0.06)
    frame.margin_right = Inches(0.06)
    frame.margin_top = Inches(0.04)
    frame.margin_bottom = Inches(0.04)
    frame.vertical_anchor = valign
    for i, item in enumerate(lines):
        p = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(6)
        p.level = 0
        runs = [(item, False)] if isinstance(item, str) else item
        for text, is_bold in runs:
            run = p.add_run()
            run.text = text
            run.font.name = FONT
            run.font.size = Pt(size)
            run.font.bold = is_bold
            run.font.color.rgb = color
    return shape


def panel(slide, x, y, w, h, fill=WHITE, line=LINE):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    rgb_fill(shape, fill, line)
    return shape


def bar(slide, x, y, w, h, color):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    rgb_fill(shape, color, color)
    return shape


def footer(slide, page, source):
    bar(slide, 0, 7.22, 13.333, 0.28, LIGHT)
    textbox(slide, 0.45, 7.22, 9.6, 0.28, source, size=10, color=MID, italic=True, valign=MSO_ANCHOR.MIDDLE)
    textbox(slide, 11.4, 7.22, 1.5, 0.28, f"{page}  /  12", size=10, color=MID, align=PP_ALIGN.RIGHT, valign=MSO_ANCHOR.MIDDLE)


def header(slide, title):
    bar(slide, 0, 0, 13.333, 0.72, DEEP)
    bar(slide, 0, 0, 0.14, 7.5, TEAL)
    textbox(slide, 0.45, 0.12, 12.4, 0.50, title, size=22, bold=True, color=WHITE, font=DISPLAY, valign=MSO_ANCHOR.MIDDLE)


def content_slide(prs, page, title, source):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    header(slide, title)
    footer(slide, page, source)
    return slide


def build():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    prs.core_properties.author = "Dialectic Therapeutics"
    prs.core_properties.title = "DT2216 TAP inquiry — non-confidential"
    prs.core_properties.subject = "Blood Cancer United Therapy Acceleration Program"
    prs.core_properties.comments = (
        "Non-confidential. Aligned to Dialectic TAP 1-pager Draft_09.01.2026-js_LMT. Not sent."
    )

    # 1 — Ask
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bar(s, 0, 0, 13.333, 7.5, DEEP)
    bar(s, 0, 0, 0.14, 7.5, TEAL)
    textbox(s, 0.55, 0.28, 12.2, 0.28, "NON-CONFIDENTIAL  ·  TAP INQUIRY  ·  ALIGNED TO 1 SEP 2026 ONE-PAGER", size=11, color=TEAL, bold=True)
    textbox(s, 0.55, 0.68, 12.2, 0.85, "Fund the first DT2216 Phase 2 cohort in CTCL", size=30, bold=True, color=WHITE, font=DISPLAY)
    textbox(
        s,
        0.55,
        1.58,
        12.2,
        1.15,
        "DT2216 is a clinical-stage BCL-XL PROTAC from Dialectic’s APTaD® platform. FDA granted orphan designation in T-cell lymphoma and Fast Track covering T-cell lymphoma. Published CTCL and T-ALL models show single-agent activity versus navitoclax. Solid-tumor Phase 1a set a human dose. It did not enroll CTCL. TAP would underwrite the first blood-cancer cohort.",
        size=16,
        color=WHITE,
    )
    boxes = [
        ("0.40 mg/kg IV BIW", "Phase 1a RP2D\nSolid tumors — not CTCL"),
        ("CTCL  ·  2027 start", "MDA trial-design talks\nIyer and Akkad"),
        ("[BOARD: $ ask]", "Strategic $2–10M vs\nopportunistic ~$500k"),
    ]
    for i, (val, lab) in enumerate(boxes):
        x = 0.55 + i * 4.15
        panel(s, x, 3.05, 3.95, 2.05, fill=RGBColor(0x0F, 0x4C, 0x48), line=TEAL)
        textbox(s, x + 0.18, 3.18, 3.60, 0.70, val, size=18, bold=True, color=WHITE, font=DISPLAY)
        textbox(s, x + 0.18, 3.88, 3.60, 1.05, lab, size=13, color=RGBColor(0xC9, 0xE8, 0xE4))
    textbox(
        s,
        0.55,
        5.30,
        12.2,
        0.70,
        "Contact on the inquiry form: Joshua Sills, COO  ·  sills@dtsciences.com  ·  Dallas. One-pager says DT2216 plus dexamethasone. Josh comment 1 Sep: frame CTCL as direct-to-Phase 2 single agent. Resolve before send.",
        size=13,
        color=RGBColor(0xC9, 0xE8, 0xE4),
    )
    textbox(s, 0.55, 6.95, 12.2, 0.30, "Dialectic Therapeutics  ·  1220 N. Stemmons Freeway, Ste. 100, Dallas, TX 75234  ·  1  /  12", size=12, color=RGBColor(0x9B, 0xC4, 0xC0))

    # 2 — Platform
    s = content_slide(prs, 2, "DT2216 makes BCL-XL druggable by degrading it where platelets cannot", "Source: TAP 1-pager §1; Khan et al., Nat Med 2019; company Fast Track PR, 5 Apr 2022.")
    panel(s, 0.45, 0.95, 6.15, 4.70, LIGHT, LINE)
    textbox(s, 0.65, 1.10, 5.75, 0.40, "The 1-pager’s platform sentence", size=16, bold=True, color=NAVY)
    add_runs(
        s,
        0.60,
        1.55,
        5.80,
        3.90,
        [
            [("DT2216 recruits VHL E3 ligase to destroy BCL-XL in tumor cells and restore apoptosis.", False)],
            [("Platelets express very little VHL, so DT2216 spares them.", False)],
            [("That is the on-target thrombocytopenia that stopped navitoclax and AZD0466 and has stalled pelcitoclax.", False)],
            [("A validated target becomes druggable for the first time.", True)],
            [("Asset family: APTaD®. Next heme asset is DT5321 (subcutaneous BCL-XL/BCL-2 dual degrader), IND-enabling for CLL and resistant AML — not this TAP ask.", False)],
        ],
        size=14.5,
    )
    panel(s, 6.80, 0.95, 6.05, 4.70, PALE, TEAL)
    textbox(s, 7.00, 1.10, 5.65, 0.40, "Why this is a heme thesis first", size=16, bold=True, color=DEEP)
    add_runs(
        s,
        6.95,
        1.55,
        5.70,
        3.90,
        [
            [("Mature T cells drop BCL-XL after thymic selection; many T-cell lymphomas re-express it.", False)],
            [("Solid-tumor Phase 1a showed no single-agent activity. That is expected. It is not the TAP indication.", False)],
            [("Do not claim CTCL patients have been treated. They have not.", True)],
        ],
        size=15,
    )
    panel(s, 0.45, 5.80, 12.40, 1.10, PALE, TEAL)
    textbox(
        s,
        0.65,
        5.95,
        12.00,
        0.80,
        "TAP implication: first cohort is a BCL-XL-dependent lymphoid population. The 1-pager names CTCL.",
        size=15,
        color=DEEP,
        valign=MSO_ANCHOR.MIDDLE,
    )

    # 3 — Preclinical
    s = content_slide(prs, 3, "Published heme models: single-agent regressions versus navitoclax, less platelet toxicity", "Sources: TAP 1-pager §3; Khan et al., Nat Med 2019; He et al., J Hematol Oncol 2020; Blood 2025 post-MPN AML.")
    panel(s, 0.45, 0.95, 6.15, 4.70, WHITE, LINE)
    bar(s, 0.45, 0.95, 6.15, 0.12, TEAL)
    textbox(s, 0.65, 1.20, 5.75, 0.35, "CTCL xenograft — He 2020", size=16, bold=True, color=NAVY)
    add_runs(
        s,
        0.60,
        1.65,
        5.80,
        3.80,
        [
            [("MyLa cutaneous T-cell lymphoma xenografts.", False)],
            [("DT2216 monotherapy inhibited growth and beat navitoclax in the reported model.", False)],
            [("BCL-XL degraded. The paper did not show BCL-2 / MCL-1 compensation.", False)],
            [("Less platelet toxicity than navitoclax. Survival benefit in the model.", False)],
            [("Preclinical activity in a selected CTCL model. Not clinical safety or efficacy.", True)],
        ],
        size=14.5,
    )
    panel(s, 6.80, 0.95, 6.05, 4.70, WHITE, LINE)
    bar(s, 6.80, 0.95, 6.05, 0.12, NAVY)
    textbox(s, 7.00, 1.20, 5.65, 0.35, "T-ALL — Khan 2019, plus later heme", size=16, bold=True, color=NAVY)
    add_runs(
        s,
        6.95,
        1.65,
        5.70,
        3.80,
        [
            [("MOLT-4 T-ALL. Foundational DT2216 paper.", False)],
            [("Weekly DT2216 produced near-complete growth inhibition versus daily navitoclax in the reported experiment.", False)],
            [("1-pager also cites azacitidine synergy in JAK2-mutated post-MPN AML (Blood 2025).", False)],
            [("1-pager cites Harvard/DFCI chemo synergy, including durable ovarian PDX eradication. That supports combination biology. It is not the TAP indication.", False)],
        ],
        size=14.5,
    )
    panel(s, 0.45, 5.80, 12.40, 1.10, PALE, TEAL)
    textbox(
        s,
        0.65,
        5.95,
        12.00,
        0.80,
        "These papers are why Fast Track exists. They are not a substitute for a CTCL patient.",
        size=15,
        color=DEEP,
        valign=MSO_ANCHOR.MIDDLE,
    )

    # 4 — Regulatory
    s = content_slide(prs, 4, "Designations are real. CTCL Phase 2 is in design, not enrolled.", "Sources: TAP 1-pager §2; orphan and Fast Track PRs; CPRIT DP210005.")
    items = [
        ("Orphan", "DT2216 for T-cell lymphoma", "1-pager and company PR. Designation only."),
        ("Fast Track", "1-pager: covering T-cell lymphoma", "Public PR 5 Apr 2022 specifies adult r/r PTCL and CTCL."),
        ("MDA / CTCL", "Iyer and Akkad — trial-design discussions", "DT2216 ± dexamethasone. Target initiation 2027. Not a protocol."),
        ("CPRIT TXCO", "DP210005 · $14.45M contracted", "Record includes T-cell lymphoma. [TO CONFIRM: spent / remaining]"),
    ]
    for i, (k, v, n) in enumerate(items):
        y = 0.95 + i * 1.45
        gold = "TO CONFIRM" in n
        panel(s, 0.45, y, 12.40, 1.32, PALE_GOLD if gold else LIGHT, RGBColor(0xE0, 0xD0, 0xA8) if gold else LINE)
        bar(s, 0.45, y, 0.12, 1.32, TEAL)
        textbox(s, 0.80, y + 0.14, 2.40, 1.00, k, size=18, bold=True, color=DEEP, valign=MSO_ANCHOR.MIDDLE)
        textbox(s, 3.30, y + 0.14, 4.60, 1.00, v, size=16, color=DARK, valign=MSO_ANCHOR.MIDDLE)
        textbox(s, 8.00, y + 0.14, 4.60, 1.00, n, size=13.5, color=AMBER if gold else MID, valign=MSO_ANCHOR.MIDDLE)

    # 5 — Phase 1
    s = content_slide(prs, 5, "Phase 1a set the human dose and showed peripheral BCL-XL degradation", "Source: TAP 1-pager §3; Mahadevan et al., J Hematol Oncol 2025; NCT04886622. n=20 solid tumors.")
    metrics = [
        ("20", "Patients. Solid tumors only."),
        ("0.40", "mg/kg IV twice weekly RP2D"),
        ("Complete", "Sustained BCL-XL loss in PBMCs"),
        ("0", "Related SAEs, discontinuations, or deaths"),
    ]
    for i, (val, lab) in enumerate(metrics):
        x = 0.45 + i * 3.20
        panel(s, x, 0.95, 3.05, 1.85, PALE, TEAL)
        textbox(s, x + 0.12, 1.08, 2.80, 0.70, val, size=26, bold=True, color=DEEP, font=DISPLAY, align=PP_ALIGN.CENTER)
        textbox(s, x + 0.12, 1.80, 2.80, 0.80, lab, size=13, color=MID, align=PP_ALIGN.CENTER)
    panel(s, 0.45, 3.00, 12.40, 3.90, WHITE, LINE)
    add_runs(
        s,
        0.55,
        3.15,
        12.10,
        3.55,
        [
            [("1-pager: well tolerated to RP2D. Only significant related AE was transient, manageable thrombocytopenia.", False)],
            [("Paper detail (keep in diligence, not as a CTCL claim): one DLT grade 4 platelets, resolved <48 h; counts recovered; no bleeding events reported.", False)],
            [("Authors: monotherapy lacked single-agent activity in these solid tumors. That is why TAP is a heme ask.", True)],
            [("Do not describe Phase 1a as a CTCL or PTCL trial. It was not.", True)],
        ],
        size=14.5,
    )

    # 6 — Proposed design from 1-pager
    s = content_slide(prs, 6, "CTCL Phase 2 as written on the 1-pager — gold is still unresolved", "Aligned to TAP 1-pager §2 and §4. Josh/Larry comments from 1–2 Sep 2026. Not a protocol. Not submitted.")
    rows = [
        ("Population", "CTCL is the lead hematology indication. After approved CTCL agents, not instead of them."),
        ("Regimen", "1-pager: DT2216 plus dexamethasone. Josh 1 Sep: “CTCL will be direct to Phase 2 single agent.” [RESOLVE]"),
        ("Site / PI", "Trial-design discussions with MD Anderson (Drs. Iyer and Akkad). Not a named contracted PI yet."),
        ("n / IND", "[TO CONFIRM] first-cohort n, 1–2 sites, and whether this enrolls under the existing IND or needs an amendment."),
        ("Endpoints", "[TO CONFIRM] safety in heme; ORR by mSWAT as applicable; RP2D confirmation if combo."),
        ("Clock", "1-pager target: initiation in 2027. TAP diligence is typically 3–6 months to committee."),
    ]
    for i, (k, v) in enumerate(rows):
        y = 0.92 + i * 0.98
        gold = "TO CONFIRM" in v or "RESOLVE" in v
        panel(s, 0.45, y, 12.40, 0.90, PALE_GOLD if gold else LIGHT, RGBColor(0xE0, 0xD0, 0xA8) if gold else LINE)
        textbox(s, 0.65, y, 2.40, 0.90, k, size=14, bold=True, color=AMBER if gold else DEEP, valign=MSO_ANCHOR.MIDDLE)
        textbox(s, 3.15, y, 9.50, 0.90, v, size=13.5, color=DARK, valign=MSO_ANCHOR.MIDDLE)

    # 7 — Not ovarian
    s = content_slide(prs, 7, "TAP is not being asked to fund PROC or the COG/FLC study", "Sources: TAP 1-pager §2–4; NCT06964009; NCT06620302. Confidential ovarian manuscript is not in this pack.")
    panel(s, 0.45, 0.95, 6.15, 5.95, WHITE, LINE)
    textbox(s, 0.65, 1.15, 5.75, 0.40, "What exists (not this ask)", size=16, bold=True, color=RED)
    add_runs(
        s,
        0.60,
        1.65,
        5.80,
        4.90,
        [
            [("PROC: DT2216 + weekly paclitaxel at DFCI/BIDMC (NCT06964009). 1-pager: Phase 1b/2, first efficacy 2027.", False)],
            [("COG/PEP-CTN: DT2216 + irinotecan in r/r solid tumors and fibrolamellar carcinoma (NCT06620302).", False)],
            [("1-pager use of these trials: they extend the established RP2D and drug supply that hematology will build on.", False)],
            [("Josh 1 Sep: PROC/FLC are Phase 1b and 1b/2. CTCL is the Phase 2 heme door.", True)],
        ],
        size=14.5,
    )
    panel(s, 6.80, 0.95, 6.05, 5.95, PALE, TEAL)
    textbox(s, 7.00, 1.15, 5.65, 0.40, "What TAP is asked to fund", size=16, bold=True, color=DEEP)
    add_runs(
        s,
        6.95,
        1.65,
        5.70,
        4.90,
        [
            [("First CTCL Phase 2 cohort in a BCL-XL-dependent T-cell lymphoma population.", False)],
            [("Uses published heme models, Fast Track / orphan, and the human dose already in hand.", False)],
            [("If diligence reaches ClinicalTrials.gov, PROC and COG will be visible. We are not hiding them. We are not asking TAP to pay for them.", True)],
        ],
        size=15,
    )

    # 8 — CMC from 1-pager
    s = content_slide(prs, 8, "Supply language already on the 1-pager; hold/site sentence still needs Josh", "TAP 1-pager §4. Gold lines were not answered on the form. Default for send: leave gold or omit.")
    rows = [
        ("Drug substance", "1-pager: GMP drug substance is on hand through Phase 2."),
        ("Drug product", "1-pager: a stable lyophilized drug product is developed, with FDA alignment."),
        ("Heme-ready start", "[TO CONFIRM] can a 1–2 site CTCL cohort start from current inventory?"),
        ("Study-conduct sentence", "[TO CONFIRM] one agreed sentence on any hold, amendment, or site status — or write “omit.” Do not invent."),
    ]
    for i, (k, v) in enumerate(rows):
        y = 0.95 + i * 1.45
        gold = "TO CONFIRM" in v
        panel(s, 0.45, y, 12.40, 1.32, PALE_GOLD if gold else LIGHT, RGBColor(0xE0, 0xD0, 0xA8) if gold else LINE)
        textbox(s, 0.70, y + 0.18, 3.20, 0.96, k, size=16, bold=True, color=AMBER if gold else DEEP, valign=MSO_ANCHOR.MIDDLE)
        textbox(s, 4.00, y + 0.18, 8.55, 0.96, v, size=15, color=DARK, valign=MSO_ANCHOR.MIDDLE)

    # 9 — IP
    s = content_slide(prs, 9, "Composition rights on DT2216 are company-reported; legal diligence still applies", "High level only. Not on the 1-pager. Same public wording as the Sept investor file.")
    panel(s, 0.45, 0.95, 12.40, 5.95, LIGHT, LINE)
    add_runs(
        s,
        0.65,
        1.15,
        12.00,
        5.50,
        [
            [("Company reports an exclusive worldwide UAMS license covering first-generation BCL-XL degraders and analogs, including DT2216.", False)],
            [("Company reports two issued U.S. drug-substance patents for DT2216 with a 2037 expiry, plus additional analog and platform filings.", False)],
            [("University of Florida license is reported for second-generation compounds, including DT5321. That is not the TAP asset.", False)],
            [("License scope, claim coverage, and term remain subject to legal diligence. This slide is not a freedom-to-operate opinion.", True)],
            [("[TO CONFIRM] if counsel wants narrower public wording before the inquiry goes out.", False)],
        ],
        size=16,
    )

    # 10 — Team from 1-pager
    s = content_slide(prs, 10, "Team as written on the 1-pager — TAP contact is Josh", "Source: TAP 1-pager §5. Do not invent other titles.")
    people = [
        ("John D. Harkey, Jr.", "Executive Chairman", "Co-founder and Executive Chairman of AveXis, acquired by Novartis for $8.7B."),
        ("Joshua Sills", "COO  ·  TAP contact", "20+ years biotech/tech operations. Also operates Cessation Therapeutics."),
        ("James Strauss, MD", "CMO", "Hematologist/oncologist, Texas Oncology. Phase 1–2 investigator, Mary Crowley."),
        ("Larry Tremaine, PhD", "CSO", "35 years Pfizer PDM. Led DT2216 preclinical development."),
        ("Stephen Friedberg", "CFO", "Business operations at Alphabet/Google. Principal investing and operating."),
        ("Zhou / Zheng / Hromas", "Scientific co-founders", "DT2216 inventors. Hromas: Board Chair; Dean, Long SOM. SAB: Brugge (Harvard Ludwig) and Licht (UF; LLS SCOR)."),
    ]
    for i, (name, role, note) in enumerate(people):
        col = i % 3
        row = i // 3
        x = 0.45 + col * 4.25
        y = 0.95 + row * 3.05
        panel(s, x, y, 4.10, 2.85, WHITE, LINE)
        bar(s, x, y, 4.10, 0.10, TEAL)
        textbox(s, x + 0.15, y + 0.22, 3.80, 0.55, name, size=16, bold=True, color=DEEP)
        textbox(s, x + 0.15, y + 0.78, 3.80, 0.40, role, size=13, italic=True, color=NAVY)
        textbox(s, x + 0.15, y + 1.22, 3.80, 1.40, note, size=13, color=MID)

    # 11 — Competition + Larry expansion comment
    s = content_slide(prs, 11, "Unmet need is after approved CTCL agents; other heme is a follow-on, not the ask", "Approved-agent list is landscape TAP already knows. Larry 2 Sep comment is not yet a company sentence.")
    panel(s, 0.45, 0.95, 6.15, 5.95, WHITE, LINE)
    textbox(s, 0.65, 1.15, 5.75, 0.40, "Already on the market", size=16, bold=True, color=NAVY)
    add_runs(
        s,
        0.60,
        1.65,
        5.80,
        4.90,
        [
            [("Mogamulizumab (CCR4) in CTCL.", False)],
            [("Brentuximab vedotin in CD30-expressing disease.", False)],
            [("Denileukin diftitox-cxdl (Lymphir) in relapsed/refractory CTCL.", False)],
            [("Skin-directed therapy, HDAC / chemo, transplant in selected patients.", False)],
            [("A TAP reviewer will not accept “no options.” Durability is still the gap.", False)],
        ],
        size=14.5,
    )
    panel(s, 6.80, 0.95, 6.05, 5.95, PALE, TEAL)
    textbox(s, 7.00, 1.15, 5.65, 0.40, "Follow-on heme — not this check", size=16, bold=True, color=DEEP)
    add_runs(
        s,
        6.95,
        1.65,
        5.70,
        4.90,
        [
            [("1-pager: MF and post-MPN AML via IITs; DT5321 Phase 1 in r/r heme ~2028.", False)],
            [("Collaborators named on the form: Konopleva, Stahl, Jain, Mato, Iacobucci, Sampath / Woyach / Mercher.", False)],
            [("Larry 2 Sep: add that CTCL success opens AML, T-ALL, MCL, MM — and ask Daohong to write the sentence.", False)],
            [("[DO NOT SEND] until Daohong writes it. Do not put an AI heme table in the TAP pack.", True)],
        ],
        size=14.5,
    )

    # 12 — What TAP gets
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bar(s, 0, 0, 13.333, 7.5, DEEP)
    bar(s, 0, 0, 0.14, 7.5, TEAL)
    textbox(s, 0.55, 0.32, 12.2, 0.35, "WHAT TAP GETS", size=12, bold=True, color=TEAL)
    textbox(s, 0.55, 0.70, 12.2, 0.70, "A CTCL partnership, not a platform tour", size=26, bold=True, color=WHITE, font=DISPLAY)
    points = [
        ("Equity / structured capital", "TAP’s published models: opportunistic ~$500k or strategic $2–10M. [BOARD picks the door.] The 1-pager does not name a dollar figure."),
        ("A first heme Phase 2", "CTCL at MDA, Fast Track and orphan already in hand, RP2D 0.40 mg/kg IV BIW, GMP DS through Phase 2. Gold fields still block a send."),
        ("What TAP already sells", "KOL network, trial-support credibility, and a signal other investors recognize. We want that, not only dollars."),
        ("Milestones, not slides", "Protocol lock, first-patient in 2027, heme safety/ORR, go/no-go on expansion. PROC and COG stay off this ticket."),
    ]
    for i, (t, b) in enumerate(points):
        y = 1.60 + i * 1.15
        textbox(s, 0.55, y, 12.2, 0.35, t, size=16, bold=True, color=WHITE)
        textbox(s, 0.55, y + 0.35, 12.2, 0.65, b, size=14, color=RGBColor(0xC9, 0xE8, 0xE4))
    textbox(s, 0.55, 6.95, 12.2, 0.30, "Not sent. Internal draft aligned to js_LMT 1-pager.  12  /  12", size=12, color=RGBColor(0x9B, 0xC4, 0xC0))

    prs.save(DST)
    print(DST)


if __name__ == "__main__":
    build()
