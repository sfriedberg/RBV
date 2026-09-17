#!/usr/bin/env python3
"""vDRAFT5: Qin Fig 7 BH3 on DF83, inserted after the DF83 result."""
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
    "Dialectic_Presentation_09.03.26_vDRAFT4.pptx"
)
DST_DRAFTS = Path(
    "/Users/stephenfriedberg/Rockbrook-Diligence-Workstreams/"
    "Dialectic-Therapeutics/drafts/"
    "Dialectic_Presentation_09.03.26_vDRAFT5.pptx"
)
DST_DROPBOX = Path(
    "/Users/stephenfriedberg/Library/CloudStorage/Dropbox/"
    "Dialectic Therapeutics/Company Presentations/"
    "Dialectic Presentation_09.03.26_vDRAFT5.pptx"
)
FIGS = Path(
    "/Users/stephenfriedberg/Rockbrook-Diligence-Workstreams/"
    "Dialectic-Therapeutics/sources/qin-figures"
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
    slide = prs.slides.add_slide(blank)

    tb = slide.shapes.add_textbox(Inches(0.4), Inches(0.16), Inches(12.5), Inches(0.40))
    r = tb.text_frame.paragraphs[0].add_run()
    set_run(
        r,
        "DF83 after paclitaxel: the dependence that was cured",
        bold=True,
        size=20,
        name=FONT_LIGHT,
        color=NAVY,
    )
    sb = slide.shapes.add_textbox(Inches(0.4), Inches(0.54), Inches(12.5), Inches(0.34))
    sr = sb.text_frame.paragraphs[0].add_run()
    set_run(
        sr,
        "Same recurrent, 4-line PDX as the day-236 result. Paclitaxel raised priming and BCL-XL dependence in the dish and in the mouse.",
        size=13,
        italic=True,
        color=TEXT_DARK,
    )
    line = slide.shapes.add_connector(1, Inches(0.4), Inches(0.92), Inches(12.9), Inches(0.92))
    line.line.color.rgb = NAVY
    line.line.width = Pt(1.15)

    # Stacked, height-constrained so both BH3 plates fit under the title.
    # C–D native 1100x450; H–I native 1485x330.
    cd_h = 2.55
    cd_w = cd_h * 1100 / 450
    slide.shapes.add_picture(
        str(FIGS / "fig7-CD.png"),
        Inches((13.333 - cd_w) / 2),
        Inches(1.02),
        height=Inches(cd_h),
    )
    cap1 = slide.shapes.add_textbox(Inches(0.4), Inches(3.60), Inches(12.5), Inches(0.28))
    c1 = cap1.text_frame.paragraphs[0].add_run()
    set_run(
        c1,
        "Fig 7C–D. DF83 cells, 24 h. Paclitaxel 5 nM or carboplatin 50 µM. n = 3. HRK = BCL-XL dependence.",
        size=12,
        color=TEXT_DARK,
        name=FONT,
    )

    hi_h = 2.20
    hi_w = hi_h * 1485 / 330
    if hi_w > 12.6:
        hi_w = 12.6
        hi_h = 12.6 * 330 / 1485
    slide.shapes.add_picture(
        str(FIGS / "fig7-HI.png"),
        Inches((13.333 - hi_w) / 2),
        Inches(3.92),
        height=Inches(hi_h),
    )
    cap2 = slide.shapes.add_textbox(Inches(0.4), Inches(6.22), Inches(12.5), Inches(0.42))
    cap2.text_frame.word_wrap = True
    c2 = cap2.text_frame.paragraphs[0].add_run()
    set_run(
        c2,
        "Fig 7H–I. DF83 tumors harvested after in-vivo treatment. n = 3–5. Paclitaxel moved the same model onto BCL-XL.",
        size=12,
        color=TEXT_DARK,
        name=FONT,
    )

    ft = slide.shapes.add_textbox(Inches(0.4), Inches(7.18), Inches(12.5), Inches(0.24))
    fr = ft.text_frame.paragraphs[0].add_run()
    set_run(
        fr,
        "Source: Qin et al., bioRxiv 2025.06.24.661170, Figure 7. Single preprint. Not the 2011 treatment-naïve BH3 series.",
        size=9,
        italic=True,
        color=MUTED,
    )

    # New slide is last (index 33). Park it after DF83 (index 19 = slide 20).
    n = len(prs.slides)
    new_idx = n - 1
    if new_idx != 33:
        raise RuntimeError(f"expected 34 slides after add, got {n}")
    order = list(range(20)) + [new_idx] + list(range(20, new_idx))
    if len(order) != n or sorted(order) != list(range(n)):
        raise RuntimeError(f"bad order {order}")
    reorder_slides(prs, order)

    prs.save(str(DST_DRAFTS))
    shutil.copy2(DST_DRAFTS, DST_DROPBOX)
    print("saved", DST_DRAFTS)
    print("slides", len(Presentation(str(DST_DRAFTS)).slides))


if __name__ == "__main__":
    main()
