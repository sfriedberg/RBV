#!/usr/bin/env python3
"""Build Sept 3 vDRAFT2 from the company deck Stephen just sent.

Edits the live charts in place. Adds three mechanism slides. Does not
overwrite the original Dropbox file.
"""
from __future__ import annotations

import shutil
from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

SRC = Path(
    "/Users/stephenfriedberg/Library/CloudStorage/Dropbox/"
    "Dialectic Therapeutics/Company Presentations/"
    "Dialectic Presentation_09.03.26_vDRAFT.pptx"
)
DST_DRAFTS = Path(
    "/Users/stephenfriedberg/Rockbrook-Diligence-Workstreams/"
    "Dialectic-Therapeutics/drafts/"
    "Dialectic_Presentation_09.03.26_vDRAFT2.pptx"
)
DST_DROPBOX = Path(
    "/Users/stephenfriedberg/Library/CloudStorage/Dropbox/"
    "Dialectic Therapeutics/Company Presentations/"
    "Dialectic Presentation_09.03.26_vDRAFT2.pptx"
)

NAVY = RGBColor(0x1F, 0x4E, 0x79)
NAVY_LIGHT = RGBColor(0xD9, 0xE2, 0xEC)
TEXT_DARK = RGBColor(0x20, 0x20, 0x20)
QUOTE_BG = RGBColor(0xF2, 0xF5, 0xF9)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
MUTED = RGBColor(0x55, 0x55, 0x55)
FONT = "Segoe UI"
FONT_LIGHT = "Segoe UI Semilight"


def set_run(run, text, *, bold=None, size=None, name=None, color=None, italic=None):
    run.text = text
    if name is not None:
        run.font.name = name
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.font.bold = bold
    if italic is not None:
        run.font.italic = italic
    if color is not None:
        run.font.color.rgb = color


def wipe_runs_keep_first(paragraph, text, **font_kw):
    if not paragraph.runs:
        r = paragraph.add_run()
        set_run(r, text, **font_kw)
        return
    set_run(paragraph.runs[0], text, **font_kw)
    for extra in paragraph.runs[1:]:
        extra._r.getparent().remove(extra._r)


def replace_shape_paragraphs(shape, paragraphs):
    """paragraphs: list of (text, bold, size)."""
    tf = shape.text_frame
    tf.word_wrap = True
    while len(tf.paragraphs) > 1:
        el = tf.paragraphs[-1]._p
        el.getparent().remove(el)
    first = True
    for text, bold, size in paragraphs:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        wipe_runs_keep_first(
            p, text, bold=bold, size=size, name=FONT_LIGHT, color=TEXT_DARK
        )


def add_title(slide, text, subtitle=None):
    tb = slide.shapes.add_textbox(Inches(0.45), Inches(0.22), Inches(12.4), Inches(0.62))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run()
    set_run(r, text, bold=True, size=22, name=FONT_LIGHT, color=NAVY)
    if subtitle:
        sb = slide.shapes.add_textbox(Inches(0.45), Inches(0.78), Inches(12.4), Inches(0.38))
        stf = sb.text_frame
        stf.word_wrap = True
        sp = stf.paragraphs[0]
        sr = sp.add_run()
        set_run(sr, subtitle, bold=False, size=13, name=FONT_LIGHT, color=TEXT_DARK, italic=True)
    line = slide.shapes.add_connector(1, Inches(0.45), Inches(1.18), Inches(12.85), Inches(1.18))
    line.line.color.rgb = NAVY
    line.line.width = Pt(1.25)


def add_table(slide, left, top, width, height, headers, rows, header_size=11, body_size=10, col_widths=None):
    tbl_shape = slide.shapes.add_table(len(rows) + 1, len(headers), left, top, width, height)
    tbl = tbl_shape.table
    if col_widths:
        for i, w in enumerate(col_widths):
            tbl.columns[i].width = w
    for ci, h in enumerate(headers):
        cell = tbl.cell(0, ci)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        cell.margin_left = Inches(0.07)
        cell.margin_right = Inches(0.07)
        cell.margin_top = Inches(0.04)
        cell.margin_bottom = Inches(0.04)
        tf = cell.text_frame
        tf.word_wrap = True
        wipe_runs_keep_first(
            tf.paragraphs[0], h, bold=True, size=header_size, name=FONT, color=WHITE
        )
    for ri, row in enumerate(rows, start=1):
        for ci, val in enumerate(row):
            cell = tbl.cell(ri, ci)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if ri % 2 == 1 else QUOTE_BG
            cell.margin_left = Inches(0.07)
            cell.margin_right = Inches(0.07)
            cell.margin_top = Inches(0.03)
            cell.margin_bottom = Inches(0.03)
            tf = cell.text_frame
            tf.word_wrap = True
            wipe_runs_keep_first(
                tf.paragraphs[0], val, bold=False, size=body_size, name=FONT, color=TEXT_DARK
            )
    return tbl_shape


def add_footer(slide, text):
    tb = slide.shapes.add_textbox(Inches(0.45), Inches(7.15), Inches(12.4), Inches(0.28))
    tf = tb.text_frame
    tf.word_wrap = True
    r = tf.paragraphs[0].add_run()
    set_run(r, text, bold=False, size=9, name=FONT_LIGHT, color=MUTED, italic=True)


def add_body(slide, left, top, width, height, paragraphs, size=12):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    first = True
    for para in paragraphs:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_after = Pt(5)
        if isinstance(para, str):
            runs = [(para, False)]
        else:
            runs = para
        for text, bold in runs:
            r = p.add_run()
            set_run(r, text, bold=bold, size=size, name=FONT, color=TEXT_DARK)
    return tb


def delete_slide(prs, index):
    sld_id = prs.slides._sldIdLst[index]
    r_id = sld_id.get(qn("r:id"))
    prs.part.drop_rel(r_id)
    prs.slides._sldIdLst.remove(sld_id)


def reorder_slides(prs, order):
    sld_id_lst = prs.slides._sldIdLst
    entries = list(sld_id_lst)
    for el in list(sld_id_lst):
        sld_id_lst.remove(el)
    for i in order:
        sld_id_lst.append(entries[i])


def find_group_child(slide, group_name, child_name):
    for s in slide.shapes:
        if s.name == group_name and s.shape_type == MSO_SHAPE_TYPE.GROUP:
            for c in s.shapes:
                if c.name == child_name:
                    return c
    return None


def main():
    DST_DRAFTS.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SRC, DST_DRAFTS)
    prs = Presentation(str(DST_DRAFTS))
    blank = prs.slide_layouts[7]

    # --- Slide 1 date ---
    cover = prs.slides[0]
    for s in cover.shapes:
        if s.has_text_frame and "August 12, 2026" in s.text_frame.text:
            wipe_runs_keep_first(
                s.text_frame.paragraphs[0],
                "September 3, 2026",
                size=12,
                name=FONT_LIGHT,
            )

    # --- Slide 3 TOC ---
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
                wipe_runs_keep_first(p, item, size=20, name=FONT_LIGHT)

    # --- Slide 4: recast Sarosiek sentence ---
    exec_sum = prs.slides[3]
    for s in exec_sum.shapes:
        if not s.has_text_frame:
            continue
        for p in s.text_frame.paragraphs:
            if "Research in collaboration with Dr. Sarosiek" in p.text:
                wipe_runs_keep_first(
                    p,
                    "Harvard / Sarosiek lab work (Qin bioRxiv 2025; AACR 2026) established why paclitaxel is the combination partner: mitotic arrest collapses MCL-1 and leaves BCL-XL as the last survival brake. In the DF83 PDX, combination produced durable tumor-free survival after dosing stopped.",
                    bold=False,
                    size=13,
                    name=FONT_LIGHT,
                )

    # --- Slide 12: young-platelet biology ---
    nav = prs.slides[11]
    for s in nav.shapes:
        if s.has_text_frame and "DT2216 is a" in s.text_frame.text:
            p = s.text_frame.add_paragraph()
            wipe_runs_keep_first(
                p,
                "Young platelets are less primed and less BCL-XL-dependent than older circulating platelets (Grozovsky / Fraser / Qin, Cell Death & Disease 2026). Megakaryocytes lack sufficient VHL for a productive ternary complex (Khan, Nat Med 2019). That is the biological reason a pulsed degrader can be tolerated where a continuous inhibitor could not.",
                bold=False,
                size=15,
                name=FONT_LIGHT,
            )

    # --- Slide 16 title ---
    vitro = prs.slides[15]
    for s in vitro.shapes:
        if s.has_text_frame and "Preclinical Efficacy: Ovarian Cancer" in s.text_frame.text:
            wipe_runs_keep_first(
                s.text_frame.paragraphs[0],
                "Preclinical Efficacy: Ovarian Cancer – In Vitro: Paclitaxel collapses MCL-1; DT2216 then removes BCL-XL (OVCAR3)",
                size=20,
                name=FONT_LIGHT,
            )

    # --- Slide 17 title + quotes ---
    df83 = prs.slides[16]
    for s in df83.shapes:
        if s.has_text_frame and s.text_frame.text.startswith("Preclinical Efficacy: Ovarian Cancer"):
            wipe_runs_keep_first(
                s.text_frame.paragraphs[0],
                "Preclinical Efficacy: Ovarian Cancer – In Vivo: DF83 PDX, n=5/arm. Paclitaxel days 0/4/8/12 only; DT2216 through day 130. No tumor at day 236.",
                size=18,
                name=FONT_LIGHT,
            )
    quotes = find_group_child(df83, "Group 88", "object 67")
    if quotes is not None:
        replace_shape_paragraphs(
            quotes,
            [
                ("Investigator roles on this dataset — not endorsements.", True, 11),
                ("", False, 10),
                ("Kristopher Sarosiek, Ph.D. Associate Professor of Radiation Biology and Cell Death, HMS / HSPH. BH3 profiling and the mitotic-arrest / BCL-XL convergence framework (AACR 2026).", False, 10),
                ("", False, 10),
                ("Ursula Matulonis, M.D. Chief, Gynecologic Oncology, DFCI. Prior PI on Immunogen’s Elahere program; PROC trial leadership.", False, 10),
                ("", False, 10),
                ("Joan Brugge, Ph.D. Director, Harvard Ludwig Cancer Center; SAB.", False, 10),
                ("", False, 10),
                ("DF83 is one PDX. Monotherapy delayed tumors. Durable clearance is combination.", True, 10),
            ],
        )

    # --- Slide 26 TAM headline ---
    tam = prs.slides[25]
    for s in tam.shapes:
        if s.has_text_frame and "$45B" in s.text_frame.text:
            wipe_runs_keep_first(
                s.text_frame.paragraphs[0],
                "Commercial Opportunity: PROC is the first wedge. The basket chart on this slide is an illustration, not an underwrite — do not treat $45B as addressable revenue.",
                size=16,
                name=FONT_LIGHT,
            )
        if s.has_text_frame and "This extraordinary commercial opportunity" in s.text_frame.text:
            wipe_runs_keep_first(
                s.text_frame.paragraphs[0],
                "The commercial case rests on three facts, not a basket TAM: (1) BCL-XL is a validated survival target that inhibitors could not dose; (2) existing PROC regimens are non-curative; (3) recent PROC assets have cleared $1B–$10B transactions on clinical signal, not on a $45B model.",
                size=12,
                name=FONT_LIGHT,
            )

    # --- Slide 28 3x claim ---
    acq = prs.slides[27]
    for s in acq.shapes:
        if s.has_text_frame and "3x the market" in s.text_frame.text:
            wipe_runs_keep_first(
                s.text_frame.paragraphs[0],
                "Elahere is restricted to FR-alpha–high tumors (~36% of PROC). DT2216 has no such screen. That is a broader eligible population, not a 3x revenue multiple. Combination use is the clinical path, not an automatic doubling of the market.",
                size=14,
                name=FONT_LIGHT,
            )

    # Add new slides BEFORE deleting anything so python-pptx assigns
    # slide33/34/35 and does not collide with existing slide32.xml (publications).
    why = prs.slides.add_slide(blank)
    add_title(
        why,
        "Why paclitaxel: mechanism, not empiricism",
        "Mitotic arrest converges apoptotic dependence onto BCL-XL. That is why the combination is designed, not observed after the fact.",
    )
    add_table(
        why,
        Inches(0.45),
        Inches(1.32),
        Inches(12.4),
        Inches(4.15),
        ["Step", "What happens", "Evidence"],
        [
            [
                "1. Baseline",
                "HGSOC cells are primed. BCL-XL holds BIM/BAX/BAK; MCL-1 holds BIM/PUMA/NOXA. Two brakes.",
                "BH3 profiling on KURAMOCHI, OVCAR3, OVCAR4, OVSAHO: HRK and BAD p<0.0001. Co-IP: BCL-XL–BIM/BAX/BAK complexes.",
            ],
            [
                "2. Paclitaxel",
                "Mitotic arrest. APC/C-Cdc20 phosphorylates MCL-1; 26S proteasome degrades it.",
                "Western: MCL-1 loss and BCL-XL phospho-shift. BH3 on mitotic vs non-mitotic cells.",
            ],
            [
                "3. Convergence",
                "Dependence collapses onto BCL-XL as the last remaining brake.",
                "Mitotically arrested HGSOC reads as BCL-XL–specific by BH3. That dependence is weaker at baseline.",
            ],
            [
                "4. DT2216",
                "VHL-recruited degradation removes BCL-XL. BIM/BAX/BAK released. Pore. Cytochrome c. Caspase.",
                "Co-IP after DT2216: partners released. Platelets spared: low VHL in megakaryocytes.",
            ],
            [
                "5. Outcome",
                "Synergistic kill under mitotic arrest. Solid tumors need the combination; some heme diseases may not.",
                "DF83 PDX: n=5/arm; paclitaxel days 0/4/8/12; DT2216 through day 130; no tumor day 236.",
            ],
        ],
        header_size=11,
        body_size=10,
        col_widths=[Inches(1.6), Inches(5.2), Inches(5.6)],
    )
    add_body(
        why,
        Inches(0.45),
        Inches(5.55),
        Inches(12.4),
        Inches(1.45),
        [
            [
                ("Platform claim: ", True),
                ("not “DT2216 + chemo.” It is DT2216 plus any agent that collapses MCL-1. The same pattern appears in vitro with paclitaxel or alisertib across GBM, NSCLC, and breast. Solid vs. liquid (Sarosiek, AACR 2026): “targeting BCL-XL alone may be effective in some heme malignancies, but combinations are needed for solid tumors.”", False),
            ]
        ],
        size=13,
    )
    add_footer(why, "Sources: Qin et al., bioRxiv 2025; Sarosiek AACR 2026; Khan et al., Nat Med 2019. Single preprint carries the DF83, co-IP, and BH3-reprogramming data.")

    pd = prs.slides.add_slide(blank)
    add_title(
        pd,
        "Mouse-to-human PD: the missing bridge",
        "The DF83 schedule is not the Phase 1a schedule. Cohort 6 degradation is the current bridge. Tumor PD in PROC is the next one.",
    )
    add_table(
        pd,
        Inches(0.45),
        Inches(1.32),
        Inches(12.4),
        Inches(2.55),
        ["", "DF83 PDX (Qin 2025)", "Human Phase 1a (Mahadevan JHO 2025)"],
        [
            ["Dose / route", "15 mg/kg IP q4d", "0.40 mg/kg IV twice weekly (RP2D)"],
            ["Duration", "DT2216 through day 130; paclitaxel days 0/4/8/12 only", "Cycle = 28 days; 20 patients, 19 completed DLT window"],
            ["PD shown", "Tumor regression; platelets and WBC recovered on schedule", "Complete BCL-XL degradation in WBC, all Cohort 6 patients"],
            ["What is not shown", "Human-equivalent exposure that produced day-236 clearance", "Paired tumor PD at the depth the PDX required"],
        ],
        header_size=11,
        body_size=11,
        col_widths=[Inches(2.2), Inches(5.1), Inches(5.1)],
    )
    add_body(
        pd,
        Inches(0.45),
        Inches(4.05),
        Inches(12.4),
        Inches(2.85),
        [
            [("How the PROC trial is built to close the gap", True)],
            "Phase 1b/2 collects BCL-XL in PBMCs plus tumor assays for pro- and anti-apoptotic proteins. That is the right PD package. It is not yet a completed bridge.",
            "Do not convert 15 mg/kg IP in the mouse to 0.4 mg/kg IV in the patient by arithmetic. Tissue retention and the PK/PD disconnect (slides 11–13) are the qualitative argument; Cohort 6 WBC degradation is the quantitative one we have.",
            "Open items: second PROC PDX; BH3 profiling on platinum-resistant — not treatment-naïve — tumors; Qin 2025 journal path.",
        ],
        size=13,
    )
    add_footer(pd, "Sources: Qin et al., bioRxiv 2025; Mahadevan et al., J Hematol Oncol 2025; company Phase 1b/2 protocol (PBMC and tumor PD).")

    risk = prs.slides.add_slide(blank)
    add_title(
        risk,
        "What still has to be proven",
        "These are the questions a serious reader will ask. Better on the page than in the Q&A.",
    )
    add_table(
        risk,
        Inches(0.45),
        Inches(1.32),
        Inches(12.4),
        Inches(5.55),
        ["Issue", "The fact", "What we have / what we need"],
        [
            [
                "Single preprint",
                "DF83, co-IP, and paclitaxel BH3 reprogramming all cite Qin et al., bioRxiv 2025 — one lab, not yet peer-reviewed.",
                "Khan Nat Med 2019 and Mahadevan JHO 2025 are published. Grozovsky / Fraser / Qin platelet paper is in Cell Death & Disease 2026. Need journal acceptance and a second institution.",
            ],
            [
                "One PDX, combo-dependent",
                "n=5 per arm. Monotherapy delayed tumors. The day-236 clearance is combination.",
                "Mechanistically expected if MCL-1 must fall first. FLC + irinotecan tests a non-taxane backbone. CTCL tests monotherapy in BCL-XL–dependent lymphoma.",
            ],
            [
                "Treatment-naïve vs PROC",
                "The 2011 primary-tumor BH3 work (Ni Chonghaile / Sarosiek / Letai, Science) used treatment-naïve samples. PROC patients have been through selection.",
                "Phase 1b tumor apoptotic-protein assays are designed to test whether BCL-XL dependence survives platinum resistance.",
            ],
            [
                "Mouse vs human dose",
                "15 mg/kg IP q4d × 130 days is not 0.4 mg/kg IV BIW.",
                "Cohort 6: complete WBC degradation at RP2D. PROC trial adds PBMC + tumor PD. That is the bridge, not mg/kg conversion.",
            ],
            [
                "Single-arm trial",
                "Phase 2 is Simon two-stage, no randomized paclitaxel control. Historical weekly-paclitaxel ORR in PROC is ~13–20%.",
                "The bar is a meaningful delta over that history, not a p-value vs a contemporaneous control. Futility interim at ~20–25 patients.",
            ],
        ],
        header_size=11,
        body_size=10,
        col_widths=[Inches(2.15), Inches(5.1), Inches(5.15)],
    )
    add_footer(risk, "Sources: Qin 2025; Ni Chonghaile / Sarosiek / Letai, Science 2011; Mahadevan 2025; company trial design. Historical paclitaxel ORR: Matulonis et al., JCO 2023 range cited on the PROC landscape slide.")

    # After add, before delete: 0-31 original, 32 why, 33 pd, 34 risk.
    delete_slide(prs, 28)

    # After delete of original slide 29: everything after 28 shifts down one.
    # 0-27 original 1-28
    # 28 IP (was 30)
    # 29 collab (was 31)
    # 30 pubs (was 32)
    # 31 why, 32 pd, 33 risk
    order = (
        list(range(0, 15))
        + [31]
        + list(range(15, 22))
        + [32]
        + list(range(22, 25))
        + [33]
        + list(range(25, 28))
        + [28, 29, 30]
    )
    if len(order) != 34 or sorted(order) != list(range(34)):
        raise RuntimeError(f"bad order {order}")
    reorder_slides(prs, order)

    prs.save(str(DST_DRAFTS))
    shutil.copy2(DST_DRAFTS, DST_DROPBOX)
    print("saved", DST_DRAFTS)
    print("saved", DST_DROPBOX)
    print("slides", len(Presentation(str(DST_DRAFTS)).slides))


if __name__ == "__main__":
    main()
