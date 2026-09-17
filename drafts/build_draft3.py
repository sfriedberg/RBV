#!/usr/bin/env python3
"""vDRAFT3: paste Sarosiek figures, drop commercial bake-off, add trial bar."""
from __future__ import annotations

import shutil
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

SRC = Path(
    "/Users/stephenfriedberg/Rockbrook-Diligence-Workstreams/"
    "Dialectic-Therapeutics/drafts/"
    "Dialectic_Presentation_09.03.26_vDRAFT2.pptx"
)
DST_DRAFTS = Path(
    "/Users/stephenfriedberg/Rockbrook-Diligence-Workstreams/"
    "Dialectic-Therapeutics/drafts/"
    "Dialectic_Presentation_09.03.26_vDRAFT3.pptx"
)
DST_DROPBOX = Path(
    "/Users/stephenfriedberg/Library/CloudStorage/Dropbox/"
    "Dialectic Therapeutics/Company Presentations/"
    "Dialectic Presentation_09.03.26_vDRAFT3.pptx"
)
FIGS = Path(
    "/Users/stephenfriedberg/Rockbrook-Diligence-Workstreams/"
    "Dialectic-Therapeutics/sources/sarosiek-figures"
)

NAVY = RGBColor(0x1F, 0x4E, 0x79)
TEXT_DARK = RGBColor(0x20, 0x20, 0x20)
MUTED = RGBColor(0x55, 0x55, 0x55)
FONT = "Segoe UI"
FONT_LIGHT = "Segoe UI Semilight"


def set_run(run, text, **kw):
    run.text = text
    run.font.name = kw.get("name", FONT_LIGHT)
    if kw.get("size") is not None:
        run.font.size = Pt(kw["size"])
    if kw.get("bold") is not None:
        run.font.bold = kw["bold"]
    if kw.get("italic") is not None:
        run.font.italic = kw["italic"]
    if kw.get("color") is not None:
        run.font.color.rgb = kw["color"]


def add_title(slide, text, subtitle=None):
    tb = slide.shapes.add_textbox(Inches(0.4), Inches(0.18), Inches(12.5), Inches(0.42))
    r = tb.text_frame.paragraphs[0].add_run()
    set_run(r, text, bold=True, size=20, name=FONT_LIGHT, color=NAVY)
    if subtitle:
        sb = slide.shapes.add_textbox(Inches(0.4), Inches(0.56), Inches(12.5), Inches(0.32))
        sr = sb.text_frame.paragraphs[0].add_run()
        set_run(sr, subtitle, size=12, italic=True, color=TEXT_DARK)
    line = slide.shapes.add_connector(1, Inches(0.4), Inches(0.92), Inches(12.9), Inches(0.92))
    line.line.color.rgb = NAVY
    line.line.width = Pt(1.15)


def add_footer(slide, text):
    tb = slide.shapes.add_textbox(Inches(0.4), Inches(7.18), Inches(12.5), Inches(0.26))
    r = tb.text_frame.paragraphs[0].add_run()
    set_run(r, text, size=9, italic=True, color=MUTED)


def add_full_figure(slide, png, top=1.00, max_h=6.05):
    # Source pages are 1760x1360. Fit height so they stay on a 16:9 slide.
    height = Inches(max_h)
    width = Inches(max_h * 1760 / 1360)
    left = Inches((13.333 - (max_h * 1760 / 1360)) / 2)
    slide.shapes.add_picture(str(png), left, Inches(top), width=width, height=height)


def add_two_figures(slide, left_png, right_png, top=1.05):
    # Width-constrained; native 1760x1360 keeps aspect (~4.8" tall).
    slide.shapes.add_picture(str(left_png), Inches(0.35), Inches(top), width=Inches(6.2))
    slide.shapes.add_picture(str(right_png), Inches(6.75), Inches(top), width=Inches(6.2))


def delete_slide(prs, index):
    sld_id = prs.slides._sldIdLst[index]
    prs.part.drop_rel(sld_id.get(qn("r:id")))
    prs.slides._sldIdLst.remove(sld_id)


def reorder_slides(prs, order):
    lst = prs.slides._sldIdLst
    entries = list(lst)
    for el in list(lst):
        lst.remove(el)
    for i in order:
        lst.append(entries[i])


def main():
    shutil.copy2(SRC, DST_DRAFTS)
    prs = Presentation(str(DST_DRAFTS))
    blank = prs.slide_layouts[7]

    # Trial-bar footnote on PROC design (vDRAFT2 slide 25, index 24)
    proc = prs.slides[24]
    box = proc.shapes.add_textbox(Inches(0.4), Inches(6.95), Inches(12.4), Inches(0.42))
    tf = box.text_frame
    tf.word_wrap = True
    r = tf.paragraphs[0].add_run()
    set_run(
        r,
        "Efficacy bar, not a competitive bake-off: historical weekly paclitaxel ORR ~13–20%; Elahere 32–42% in FRα-high; pembrolizumab + weekly paclitaxel approved Feb 2026. DT2216 has no PROC ORR yet.",
        size=11,
        name=FONT,
        color=TEXT_DARK,
    )

    young = prs.slides.add_slide(blank)
    add_title(
        young,
        "Young platelets are less primed — why a pulsed degrader can be tolerated",
        "This is the navitoclax answer. Not a Dialectic claim: Grozovsky / Fraser / Qin, Cell Death & Disease 2026, and Khan, Nat Med 2019.",
    )
    add_two_figures(young, FIGS / "p24-24.png", FIGS / "p25-25.png")
    add_footer(young, "Sources: Grozovsky, Fraser, Qin et al., Cell Death & Disease 2026; Khan et al., Nat Med 2019. Sarosiek AACR 2026 slides 24–25.")

    bh3 = prs.slides.add_slide(blank)
    add_title(
        bh3,
        "HGSOC cell lines are BCL-XL dependent by BH3 profiling",
        "KURAMOCHI, OVCAR3, OVCAR4, OVSAHO. HRK and BAD separate at p<0.0001. MS1 (MCL-1) does not. Qin et al., bioRxiv 2025.",
    )
    add_full_figure(bh3, FIGS / "p15-15.png")
    add_footer(bh3, "Source: Sarosiek AACR 2026, “BH3 Profiling HGSOC cell lines – BCL-XL dependence.” Single preprint: Qin et al., bioRxiv 2025.")

    pac = prs.slides.add_slide(blank)
    add_title(
        pac,
        "Why paclitaxel: mitotic arrest collapses MCL-1 onto BCL-XL",
        "Left: paclitaxel phosphorylates BCL-XL and drops MCL-1. Right: only mitotically arrested cells read as BCL-XL dependent.",
    )
    add_two_figures(pac, FIGS / "p28-28.png", FIGS / "p29-29.png")
    add_footer(pac, "Source: Qin et al., bioRxiv 2025; Sarosiek AACR 2026 slides 28–29. Mechanism: APC/C-Cdc20 → MCL-1 → 26S proteasome.")

    coip = prs.slides.add_slide(blank)
    add_title(
        coip,
        "DT2216 releases BIM, BAX and BAK from BCL-XL",
        "The co-IP. Untreated HGSOC: BCL-XL holds the pro-apoptotic proteins. After DT2216, they are free.",
    )
    add_full_figure(coip, FIGS / "p31-31.png")
    add_footer(coip, "Source: Qin et al., bioRxiv 2025; Sarosiek AACR 2026 slide 31. Same single preprint as DF83.")

    # Delete TAM / landscape / acquisitions (indices 28, 29, 30) from the back.
    for idx in (30, 29, 28):
        delete_slide(prs, idx)

    # After delete: 0-27 original through risk; 28 IP, 29 collab, 30 pubs;
    # 31 young, 32 bh3, 33 pac, 34 coip.
    order = (
        list(range(0, 12))
        + [31]
        + list(range(12, 16))
        + [32, 33, 34]
        + list(range(16, 31))
    )
    if len(order) != 35 or sorted(order) != list(range(35)):
        raise RuntimeError(f"bad order len={len(order)} {order}")
    reorder_slides(prs, order)

    # TOC: drop any commercial line if present; keep mechanism line.
    toc = prs.slides[2]
    for s in toc.shapes:
        if s.has_text_frame and "Company Overview" in s.text_frame.text:
            items = [
                "Company Overview",
                "Scientific Foundation: BCL-XL as a Target",
                "Why Paclitaxel: Mechanism of Combination",
                "Preclinical Efficacy Overview",
                "Phase 1 Clinical Trial Summary",
                "Phase 1b/2 Clinical Trial Design",
                "What Still Has to Be Proven",
                "Intellectual Property",
                "Publications",
            ]
            tf = s.text_frame
            while len(tf.paragraphs) > 1:
                tf.paragraphs[-1]._p.getparent().remove(tf.paragraphs[-1]._p)
            for i, item in enumerate(items):
                p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                if p.runs:
                    p.runs[0].text = item
                    for extra in p.runs[1:]:
                        extra._r.getparent().remove(extra._r)
                else:
                    r = p.add_run()
                    r.text = item
                    r.font.size = Pt(20)
                    r.font.name = FONT_LIGHT

    prs.save(str(DST_DRAFTS))
    shutil.copy2(DST_DRAFTS, DST_DROPBOX)
    print("saved", DST_DRAFTS)
    print("slides", len(Presentation(str(DST_DRAFTS)).slides))


if __name__ == "__main__":
    main()
