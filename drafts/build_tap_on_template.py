#!/usr/bin/env python3
"""Build the TAP CTCL inquiry deck on the existing Dialectic slide master."""

from __future__ import annotations

import shutil
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

import build_aplus_deck as base

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "Dialectic_Presentation_09.04.26_A_PLUS_REFINED.pptx"
DST = ROOT / "Dialectic_TAP_Inquiry_CTCL_091426.pptx"

TEAL = RGBColor(0x00, 0xA9, 0x98)
DEEP_TEAL = RGBColor(0x00, 0x72, 0x69)
NAVY = RGBColor(0x1F, 0x4E, 0x79)
DARK = RGBColor(0x1F, 0x29, 0x33)
MID = RGBColor(0x4D, 0x5B, 0x66)
LIGHT = RGBColor(0xF3, 0xF6, 0xF7)
PALE_TEAL = RGBColor(0xE8, 0xF5, 0xF3)
PALE_RED = RGBColor(0xFA, 0xEE, 0xED)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
RED = RGBColor(0xA7, 0x35, 0x35)
LINE = RGBColor(0xCF, 0xD8, 0xDC)
FONT = "Aptos"
FONT_DISPLAY = "Aptos Display"

textbox = base.textbox
add_title = base.add_title


def panel(slide, x, y, w, h, *, fill=WHITE, line=LINE):
    return base.add_panel(slide, x, y, w, h, fill=fill, line=line, radius=False)


def add_footer(slide, source: str):
    textbox(slide, 0.50, 7.02, 11.50, 0.24, source, size=8.5, color=MID, italic=True, font=FONT)


def add_label(slide, x, y, w, text, *, fill=NAVY):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(0.32))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = fill
    textbox(slide, x, y, w, 0.32, text.upper(), size=11.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE, font=FONT)


def set_runs(shape, replacements: dict[str, str]) -> None:
    for paragraph in shape.text_frame.paragraphs:
        for run in paragraph.runs:
            for old, new in replacements.items():
                if old in run.text:
                    run.text = run.text.replace(old, new)


def replace_cover(slide) -> None:
    replacements = {
        "Creating Innovative Technologies to Treat Cancer": "Creating Innovative Technologies to Treat Cancer",
        "CONFIDENTIAL |": "NON-CONFIDENTIAL  |  TAP INQUIRY",
        "CONFIDENTIAL": "NON-CONFIDENTIAL",
        "Company Presentation": "DT2216 for cutaneous T-cell lymphoma",
        "September 4, 2026": "September 14, 2026",
        "September 3, 2026": "September 14, 2026",
    }
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        set_runs(shape, replacements)
        compact = shape.text_frame.text.strip()
        if compact in {"CONFIDENTIAL |", "CONFIDENTIAL", "NON-CONFIDENTIAL", "NON-CONFIDENTIAL\n"}:
            for paragraph in shape.text_frame.paragraphs:
                if paragraph.runs:
                    paragraph.runs[0].text = "NON-CONFIDENTIAL  |  TAP INQUIRY"
                    for extra in paragraph.runs[1:]:
                        extra.text = ""
                    break
        if "Company Presentation" in compact and "DT2216" not in compact:
            for paragraph in shape.text_frame.paragraphs:
                for run in paragraph.runs:
                    if "Company Presentation" in run.text:
                        run.text = run.text.replace("Company Presentation", "DT2216 for cutaneous T-cell lymphoma")


def keep_slides(prs, keep: list[int]) -> None:
    entries = list(prs.slides._sldIdLst)
    slide_list = prs.slides._sldIdLst
    keep_set = set(keep)
    for index, entry in enumerate(entries):
        if index not in keep_set:
            prs.part.drop_rel(entry.get(qn("r:id")))
    for entry in list(slide_list):
        slide_list.remove(entry)
    for index in keep:
        slide_list.append(entries[index])


def content(prs):
    return prs.slides.add_slide(prs.slide_layouts[7])


def slide_scope(prs):
    s = content(prs)
    add_title(s, "The TAP ask is the first DT2216 cohort in CTCL")
    panel(s, 0.50, 1.12, 7.55, 5.55, fill=LIGHT, line=LINE)
    add_label(s, 0.70, 1.28, 1.55, "In scope", fill=DEEP_TEAL)
    textbox(
        s, 0.70, 1.76, 7.15, 4.70,
        "Lead indication: relapsed/refractory CTCL, after approved agents.\n\n"
        "Asset: DT2216, a VHL-based BCL-XL PROTAC from the APTaD® platform.\n\n"
        "Starting point: Phase 1a RP2D of 0.40 mg/kg IV twice weekly.\n\n"
        "Site path: trial-design discussions with MD Anderson (Drs. Iyer and Akkad).\n\n"
        "Clock: initiation targeted for 2027, after protocol lock.\n\n"
        "Why TAP: fund the first heme cohort, not another solid-tumor monotherapy study.",
        size=14.5, color=DARK,
    )
    panel(s, 8.20, 1.12, 4.65, 5.55, fill=PALE_TEAL, line=TEAL)
    add_label(s, 8.40, 1.28, 2.55, "Out of scope", fill=NAVY)
    textbox(
        s, 8.40, 1.76, 4.25, 4.70,
        "Platinum-resistant ovarian cancer (NCT06964009)\n\n"
        "COG / PEP-CTN solid-tumor and FLC study (NCT06620302)\n\n"
        "DT5321 dual degrader (next heme asset)\n\n"
        "Investigator-initiated myeloid expansion (MF, post-MPN AML)\n\n"
        "Confidential unpublished combination figures",
        size=14, color=DARK,
    )
    add_footer(s, "Aligned to Dialectic TAP Initial Inquiry Form, 1 September 2026.")


def slide_mechanism(prs):
    s = content(prs)
    add_title(s, "BCL-XL is validated. Continuous inhibition was not doseable.")
    blocks = [
        ("01", "The target", "BCL-XL is the most commonly overexpressed anti-apoptotic protein in human cancer. Many T-cell lymphomas re-express it after normal mature T cells have dropped it."),
        ("02", "Why inhibitors stalled", "Navitoclax, AZD0466, and pelcitoclax ran into on-target thrombocytopenia. Platelets depend on BCL-XL. Continuous inhibition could not be dosed as a heme drug."),
        ("03", "What DT2216 changes", "DT2216 recruits VHL E3 ligase to degrade BCL-XL in tumor cells. Platelets express very little VHL, so they are relatively spared. The target becomes usable."),
        ("04", "What this is not", "Not a claim that platelets are untouched. Phase 1a still saw transient thrombocytopenia. Not a claim that CTCL patients have been treated."),
    ]
    for i, (n, title, body) in enumerate(blocks):
        col, row = i % 2, i // 2
        x, y = 0.50 + col * 6.40, 1.12 + row * 2.80
        fill = PALE_RED if i == 3 else LIGHT
        panel(s, x, y, 6.20, 2.62, fill=fill, line=LINE)
        textbox(s, x + 0.20, y + 0.14, 1.10, 0.36, n, size=16, bold=True, color=TEAL, font=FONT_DISPLAY)
        textbox(s, x + 0.20, y + 0.50, 5.80, 0.38, title, size=16, bold=True, color=DEEP_TEAL, font=FONT_DISPLAY)
        textbox(s, x + 0.20, y + 0.96, 5.80, 1.45, body, size=13.5, color=DARK)
    add_footer(s, "Khan et al., Nat Med 2019; company Fast Track PR, 5 April 2022; TAP 1-pager §1.")


def slide_preclinical(prs):
    s = content(prs)
    add_title(s, "Published heme models show single-agent activity versus navitoclax")
    panel(s, 0.50, 1.12, 6.20, 4.55, fill=WHITE, line=LINE)
    add_label(s, 0.70, 1.28, 2.35, "CTCL  ·  He 2020", fill=DEEP_TEAL)
    textbox(
        s, 0.70, 1.76, 5.80, 3.70,
        "MyLa cutaneous T-cell lymphoma xenografts.\n\n"
        "DT2216 monotherapy inhibited growth and outperformed navitoclax in the reported model.\n\n"
        "BCL-XL was degraded. The paper did not show BCL-2 or MCL-1 compensation.\n\n"
        "Less platelet toxicity than navitoclax, with a survival benefit in the model.",
        size=14.5, color=DARK,
    )
    panel(s, 6.90, 1.12, 5.95, 4.55, fill=WHITE, line=LINE)
    add_label(s, 7.10, 1.28, 2.45, "T-ALL  ·  Khan 2019", fill=NAVY)
    textbox(
        s, 7.10, 1.76, 5.55, 3.70,
        "MOLT-4 T-ALL. Foundational DT2216 paper.\n\n"
        "Weekly DT2216 produced near-complete growth inhibition versus daily navitoclax in the reported experiment.\n\n"
        "Same pattern: BCL-XL degradation, no compensatory BCL-2 / MCL-1, reduced platelet liability versus continuous inhibition.\n\n"
        "Supports intermittent degradation as the heme dosing idea later used in Phase 1a (BIW).",
        size=14, color=DARK,
    )
    panel(s, 0.50, 5.80, 12.35, 0.95, fill=PALE_TEAL, line=TEAL)
    textbox(
        s, 0.70, 5.92, 11.95, 0.72,
        "These papers are why Fast Track exists. They are not a substitute for a treated CTCL patient.",
        size=15, bold=True, color=DEEP_TEAL, valign=MSO_ANCHOR.MIDDLE,
    )
    add_footer(s, "Khan et al., Nat Med 2019; He et al., J Hematol Oncol 2020. Preclinical only.")


def slide_phase1(prs):
    s = content(prs)
    add_title(s, "Phase 1a set a human dose. It did not enroll CTCL.")
    metrics = [
        ("20", "Patients. Solid tumors only."),
        ("0.40", "mg/kg IV BIW recommended Phase 2 dose"),
        ("1", "DLT — grade 4 platelets, resolved <48 h"),
        ("4 / 20", "Best RECIST: stable disease. No responses."),
    ]
    for i, (val, lab) in enumerate(metrics):
        x = 0.50 + i * 3.20
        panel(s, x, 1.12, 3.05, 1.85, fill=PALE_TEAL, line=TEAL)
        textbox(s, x, 1.22, 3.05, 0.70, val, size=26, bold=True, color=DEEP_TEAL, align=PP_ALIGN.CENTER, font=FONT_DISPLAY)
        textbox(s, x + 0.10, 1.95, 2.85, 0.85, lab, size=12.5, color=MID, align=PP_ALIGN.CENTER)
    panel(s, 0.50, 3.15, 12.35, 3.55, fill=WHITE, line=LINE)
    textbox(
        s, 0.70, 3.32, 11.95, 3.20,
        "BCL-XL in peripheral leukocytes fell rapidly at 0.40 mg/kg and stayed down. Human tumor BCL-XL degradation has not been shown.\n\n"
        "Thrombocytopenia was transient and manageable. The paper reported recovery above 50k in four days and above 75k in one week. No bleeding events or treatment-emergent deaths.\n\n"
        "The 1-pager states there were no related SAEs, discontinuations, or deaths.\n\n"
        "Authors: monotherapy lacked single-agent activity in these solid tumors. That is why the TAP indication is a BCL-XL-dependent lymphoid population.",
        size=14.5, color=DARK,
    )
    add_footer(s, "Mahadevan et al., J Hematol Oncol 2025; NCT04886622. n = 20 advanced solid tumors.")


def slide_regulatory(prs):
    s = content(prs)
    add_title(s, "Designations and prior Texas funding are in hand. A CTCL dataset is not.")
    rows = [
        ("Orphan drug", "DT2216 for T-cell lymphoma", "Company designation. Not efficacy."),
        ("Fast Track", "Adult relapsed/refractory PTCL and CTCL", "Expedites FDA interaction. Not approval."),
        ("IND / Phase 1a", "NCT04886622 completed", "Solid-tumor dose escalation. RP2D set."),
        ("CPRIT TXCO", "DP210005  ·  $14.45M contracted", "Record includes T-cell lymphoma and SCLC."),
        ("MDA path", "Iyer and Akkad — design discussions", "CTCL Phase 2 targeted for 2027. Not a locked protocol."),
    ]
    for i, (k, v, n) in enumerate(rows):
        y = 1.12 + i * 1.10
        panel(s, 0.50, y, 12.35, 1.00, fill=LIGHT, line=LINE)
        shape = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.50), Inches(y), Inches(0.10), Inches(1.00))
        shape.fill.solid()
        shape.fill.fore_color.rgb = TEAL
        shape.line.color.rgb = TEAL
        textbox(s, 0.80, y, 2.45, 1.00, k, size=15, bold=True, color=DEEP_TEAL, valign=MSO_ANCHOR.MIDDLE)
        textbox(s, 3.35, y, 4.70, 1.00, v, size=14.5, color=DARK, valign=MSO_ANCHOR.MIDDLE)
        textbox(s, 8.15, y, 4.50, 1.00, n, size=13.5, color=MID, valign=MSO_ANCHOR.MIDDLE)
    add_footer(s, "Orphan PR; Fast Track PR, 5 April 2022; CPRIT DP210005; TAP 1-pager §2.")


def slide_design(prs):
    s = content(prs)
    add_title(s, "Proposed CTCL Phase 2: use the dose already in hand")
    rows = [
        ("Population", "Relapsed/refractory CTCL after approved targeted therapy. Not front-line."),
        ("Regimen", "DT2216 at 0.40 mg/kg IV twice weekly. Steroid combination to be locked with MDA."),
        ("Site / PI", "MD Anderson. Trial-design discussions with Drs. Iyer and Akkad."),
        ("Purpose", "First human CTCL dataset: safety in a heme population, activity by mSWAT, go/no-go on expansion."),
        ("Clock", "Protocol lock, then initiation targeted for 2027. TAP diligence is typically 3–6 months to committee."),
        ("What TAP funds", "The first heme cohort — drug, CRO, site, and the work to open it. Not PROC. Not COG."),
    ]
    for i, (k, v) in enumerate(rows):
        y = 1.12 + i * 0.90
        panel(s, 0.50, y, 12.35, 0.82, fill=LIGHT if i % 2 == 0 else WHITE, line=LINE)
        textbox(s, 0.70, y, 2.35, 0.82, k, size=13.5, bold=True, color=DEEP_TEAL, valign=MSO_ANCHOR.MIDDLE)
        textbox(s, 3.15, y, 9.50, 0.82, v, size=13.5, color=DARK, valign=MSO_ANCHOR.MIDDLE)
    add_footer(s, "Working design from the 1 September 2026 inquiry form. Not a protocol. Not submitted.")
    s.notes_slide.notes_text_frame.text = (
        "Josh 1 Sep: PROC/FLC are Phase 1b; CTCL should be framed as direct-to-Phase 2 single agent. "
        "1-pager still says plus dexamethasone. n, IND amendment, and dollar ask remain open."
    )


def slide_other_trials(prs):
    s = content(prs)
    add_title(s, "Two solid-tumor trials are visible. They are not this ask.")
    panel(s, 0.50, 1.12, 6.20, 5.55, fill=WHITE, line=LINE)
    add_label(s, 0.70, 1.28, 1.85, "What exists", fill=RED)
    textbox(
        s, 0.70, 1.76, 5.80, 4.70,
        "PROC: DT2216 plus weekly paclitaxel at DFCI / BIDMC (NCT06964009). Phase 1b/2. First efficacy expected 2027.\n\n"
        "COG / PEP-CTN: DT2216 plus irinotecan in relapsed/refractory solid tumors and fibrolamellar carcinoma (NCT06620302).\n\n"
        "The inquiry form treats these as the studies that extend the RP2D and the drug-supply path hematology will use.\n\n"
        "If TAP diligence reaches ClinicalTrials.gov, both records will be there. We are not hiding them.",
        size=14.5, color=DARK,
    )
    panel(s, 6.90, 1.12, 5.95, 5.55, fill=PALE_TEAL, line=TEAL)
    add_label(s, 7.10, 1.28, 2.85, "What TAP funds", fill=DEEP_TEAL)
    textbox(
        s, 7.10, 1.76, 5.55, 4.70,
        "The first CTCL Phase 2 cohort in a BCL-XL-dependent T-cell lymphoma population.\n\n"
        "A protocol that uses the published heme models, Fast Track, orphan designation, and the human dose already established.\n\n"
        "Myelofibrosis, post-MPN AML, and DT5321 remain follow-on heme options. They are not the check TAP is being asked to write.",
        size=14.5, color=DARK,
    )
    add_footer(s, "NCT06964009; NCT06620302. Confidential ovarian manuscript is omitted on purpose.")


def slide_plan(prs):
    s = content(prs)
    add_title(s, "Dose, supply, and a 2027 CTCL start are the operating facts")
    steps = [
        ("Now", "Phase 1a complete. RP2D 0.40 mg/kg IV BIW. Two solid-tumor combination trials on the register."),
        ("Supply", "GMP drug substance on hand through Phase 2. Lyophilized drug product developed, with FDA alignment."),
        ("2026–27", "Lock the CTCL protocol with MD Anderson. TAP diligence in parallel (typically 3–6 months to committee)."),
        ("2027", "Target CTCL Phase 2 initiation. First heme safety and activity read. Go/no-go on expansion."),
    ]
    for i, (when, body) in enumerate(steps):
        y = 1.16 + i * 1.38
        oval = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.58), Inches(y + 0.38), Inches(0.38), Inches(0.38))
        oval.fill.solid()
        oval.fill.fore_color.rgb = TEAL
        oval.line.color.rgb = TEAL
        textbox(s, 0.58, y + 0.38, 0.38, 0.38, str(i + 1), size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        if i < 3:
            bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.74), Inches(y + 0.78), Inches(0.06), Inches(0.96))
            bar.fill.solid()
            bar.fill.fore_color.rgb = TEAL
            bar.line.color.rgb = TEAL
        textbox(s, 1.20, y, 2.10, 1.22, when, size=18, bold=True, color=DEEP_TEAL, valign=MSO_ANCHOR.MIDDLE, font=FONT_DISPLAY)
        textbox(s, 3.40, y, 9.40, 1.22, body, size=15, color=DARK, valign=MSO_ANCHOR.MIDDLE)
    add_footer(s, "TAP 1-pager §4. Company-reported supply language. Not a CMC package.")


def slide_team(prs):
    s = content(prs)
    add_title(s, "Texas company. Operators who already ran first-in-human.")
    people = [
        ("John D. Harkey, Jr.", "Executive Chairman", "Co-founder and Executive Chairman of AveXis, acquired by Novartis for $8.7B."),
        ("Joshua Sills", "COO  ·  TAP contact", "Twenty years of biotech and technology operations. Also operates Cessation Therapeutics."),
        ("James Strauss, MD", "Chief Medical Officer", "Hematologist and medical oncologist, Texas Oncology. Phase 1–2 investigator, Mary Crowley."),
        ("Larry Tremaine, PhD", "Chief Scientific Officer", "Thirty-five years at Pfizer PDM. Led DT2216 preclinical development."),
        ("Stephen Friedberg", "Chief Financial Officer", "Business operations at Alphabet / Google. Principal investing and operating experience."),
        ("Zhou  ·  Zheng  ·  Hromas", "Scientific co-founders", "DT2216 inventors. Hromas chairs the board. SAB includes Joan Brugge and Jonathan Licht (LLS SCOR)."),
    ]
    for i, (name, role, note) in enumerate(people):
        col, row = i % 3, i // 3
        x, y = 0.50 + col * 4.20, 1.12 + row * 2.80
        panel(s, x, y, 4.05, 2.62, fill=WHITE, line=LINE)
        bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(4.05), Inches(0.08))
        bar.fill.solid()
        bar.fill.fore_color.rgb = TEAL
        bar.line.color.rgb = TEAL
        textbox(s, x + 0.16, y + 0.22, 3.74, 0.48, name, size=15, bold=True, color=DEEP_TEAL, font=FONT_DISPLAY)
        textbox(s, x + 0.16, y + 0.72, 3.74, 0.34, role, size=12.5, italic=True, color=NAVY)
        textbox(s, x + 0.16, y + 1.12, 3.74, 1.30, note, size=12.5, color=MID)
    add_footer(s, "TAP 1-pager §5. TAP operating contact: Joshua Sills, COO.")


def slide_landscape(prs):
    s = content(prs)
    add_title(s, "The unmet need is after approved CTCL agents, not instead of them")
    panel(s, 0.50, 1.12, 6.20, 5.55, fill=WHITE, line=LINE)
    add_label(s, 0.70, 1.28, 2.15, "Already available", fill=NAVY)
    textbox(
        s, 0.70, 1.76, 5.80, 4.70,
        "Mogamulizumab (CCR4) in CTCL.\n\n"
        "Brentuximab vedotin in CD30-expressing disease.\n\n"
        "Denileukin diftitox-cxdl (Lymphir) in relapsed/refractory CTCL.\n\n"
        "Skin-directed therapy, HDAC inhibitors, chemotherapy, and transplant in selected patients.\n\n"
        "A TAP reviewer will not accept “no options.” Response rates and durability are still the gap.",
        size=14.5, color=DARK,
    )
    panel(s, 6.90, 1.12, 5.95, 5.55, fill=PALE_TEAL, line=TEAL)
    add_label(s, 7.10, 1.28, 2.55, "Where DT2216 sits", fill=DEEP_TEAL)
    textbox(
        s, 7.10, 1.76, 5.55, 4.70,
        "Different mechanism: BCL-XL degradation, not CCR4, CD30, or IL-2 receptor targeting.\n\n"
        "Natural first use: after those agents, or in patients who are not candidates for them.\n\n"
        "Platelet recovery between doses is the therapeutic-index argument versus navitoclax — still to be shown in a heme cohort.\n\n"
        "Do not position DT2216 as front-line CTCL therapy in this inquiry.",
        size=14.5, color=DARK,
    )
    add_footer(s, "Landscape TAP already knows. Not a market model.")


def slide_close(prs):
    s = content(prs)
    add_title(s, "A CTCL partnership, not a platform tour")
    points = [
        ("A first heme Phase 2", "CTCL at MD Anderson, Fast Track and orphan already granted, RP2D 0.40 mg/kg IV BIW, GMP drug substance through Phase 2."),
        ("A defined use of proceeds", "Open and run the first CTCL cohort. PROC and COG stay on their own tickets."),
        ("What TAP already sells", "KOL network, trial-support credibility, and a signal other capital recognizes. We want that, not only the dollars."),
        ("Milestones, not slides", "Protocol lock. First patient. Heme safety and activity. A go/no-go on expansion."),
    ]
    for i, (t, b) in enumerate(points):
        y = 1.16 + i * 1.38
        panel(s, 0.50, y, 12.35, 1.26, fill=LIGHT, line=LINE)
        bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.50), Inches(y), Inches(0.10), Inches(1.26))
        bar.fill.solid()
        bar.fill.fore_color.rgb = TEAL
        bar.line.color.rgb = TEAL
        textbox(s, 0.80, y + 0.10, 11.85, 0.38, t, size=16, bold=True, color=DEEP_TEAL, font=FONT_DISPLAY)
        textbox(s, 0.80, y + 0.50, 11.85, 0.64, b, size=14, color=DARK)
    add_footer(s, "Dialectic Therapeutics  ·  1220 N. Stemmons Freeway, Suite 100, Dallas, TX 75234  ·  dtsciences.com")
    s.notes_slide.notes_text_frame.text = (
        "Board still picks strategic ($2–10M) vs opportunistic (~$500k). "
        "Do not send until Josh locks regimen, n/IND, and one study-conduct sentence or omit."
    )


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"Missing Dialectic template: {SRC}")
    shutil.copy2(SRC, DST)
    prs = Presentation(str(DST))
    replace_cover(prs.slides[0])

    builders = [
        slide_scope,
        slide_mechanism,
        slide_preclinical,
        slide_phase1,
        slide_regulatory,
        slide_design,
        slide_other_trials,
        slide_plan,
        slide_team,
        slide_landscape,
        slide_close,
    ]
    start = len(prs.slides)
    for build in builders:
        build(prs)

    keep = [0] + list(range(start, start + len(builders)))
    keep_slides(prs, keep)
    base.set_page_numbers(prs)
    prs.core_properties.title = "DT2216 — TAP Inquiry — CTCL Phase 2"
    prs.core_properties.subject = "Blood Cancer United Therapy Acceleration Program"
    prs.core_properties.comments = "Non-confidential. Built on Dialectic September 2026 slide master. Not sent."
    prs.save(str(DST))
    print(DST)
    print("slides", len(Presentation(str(DST)).slides))


if __name__ == "__main__":
    main()
