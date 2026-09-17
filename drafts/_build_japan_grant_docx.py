#!/usr/bin/env python3
"""Dialectic Japan grant memo in AHSI Saturday Word layout."""

from pathlib import Path

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

OUT = Path(
    "/Users/stephenfriedberg/Rockbrook-Diligence-Workstreams/"
    "Dialectic-Therapeutics/drafts/"
    "Japan_Grant_Landscape_DT2216_Ovarian_083126.docx"
)

BLACK = RGBColor(0x00, 0x00, 0x00)
HEADER_FILL = "E7E6E6"
BORDER = "B7C2CC"
CONTENT_DXA = 8640  # 6.0 in; Letter with 1.25 in left/right


def set_run(run, size=11, bold=False, italic=False, name="Arial"):
    run.font.name = name
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    rfonts.set(qn("w:ascii"), name)
    rfonts.set(qn("w:hAnsi"), name)
    rfonts.set(qn("w:eastAsia"), name)
    rfonts.set(qn("w:cs"), name)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = BLACK


def set_spacing(paragraph, before=0, after=8, line=1.12):
    paragraph.paragraph_format.space_before = Pt(before)
    paragraph.paragraph_format.space_after = Pt(after)
    paragraph.paragraph_format.line_spacing = line


def add_page_number(section):
    footer = section.footer
    footer.is_linked_to_previous = False
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p.add_run("Page ")
    set_run(r, size=10)
    fld1 = OxmlElement("w:fldChar")
    fld1.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    fld2 = OxmlElement("w:fldChar")
    fld2.set(qn("w:fldCharType"), "end")
    r2 = p.add_run()
    set_run(r2, size=10)
    r2._r.append(fld1)
    r2._r.append(instr)
    r2._r.append(fld2)


def add_hyperlink(paragraph, text, url, size=8.5):
    part = paragraph.part
    r_id = part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)
    new_run = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    rfonts = OxmlElement("w:rFonts")
    rfonts.set(qn("w:ascii"), "Arial")
    rfonts.set(qn("w:hAnsi"), "Arial")
    rfonts.set(qn("w:eastAsia"), "Arial")
    rfonts.set(qn("w:cs"), "Arial")
    u = OxmlElement("w:u")
    u.set(qn("w:val"), "single")
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "0563C1")
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), str(int(size * 2)))
    sz_cs = OxmlElement("w:szCs")
    sz_cs.set(qn("w:val"), str(int(size * 2)))
    rpr.append(rfonts)
    rpr.append(sz)
    rpr.append(sz_cs)
    rpr.append(color)
    rpr.append(u)
    new_run.append(rpr)
    t = OxmlElement("w:t")
    t.set(qn("xml:space"), "preserve")
    t.text = text
    new_run.append(t)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)


def shade_cell(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)
    shd.set(qn("w:val"), "clear")


def set_cell_border(cell):
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = tc_pr.find(qn("w:tcBorders"))
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tc_pr.append(borders)
    for edge in ("top", "left", "bottom", "right"):
        el = borders.find(qn(f"w:{edge}"))
        if el is None:
            el = OxmlElement(f"w:{edge}")
            borders.append(el)
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), BORDER)


def set_cell_margins(cell, twips=90):
    tc_pr = cell._tc.get_or_add_tcPr()
    mar = tc_pr.find(qn("w:tcMar"))
    if mar is None:
        mar = OxmlElement("w:tcMar")
        tc_pr.append(mar)
    for edge in ("top", "left", "bottom", "right", "start", "end"):
        node = mar.find(qn(f"w:{edge}"))
        if node is None:
            node = OxmlElement(f"w:{edge}")
            mar.append(node)
        node.set(qn("w:w"), str(twips))
        node.set(qn("w:type"), "dxa")


def set_col_width(cell, inches):
    cell.width = Inches(inches)
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_w = tc_pr.find(qn("w:tcW"))
    if tc_w is None:
        tc_w = OxmlElement("w:tcW")
        tc_pr.append(tc_w)
    tc_w.set(qn("w:w"), str(int(inches * 1440)))
    tc_w.set(qn("w:type"), "dxa")


def fill_cell(cell, text, *, header=False, first_col=False, width=None):
    cell.text = ""
    if width is not None:
        set_col_width(cell, width)
    set_cell_border(cell)
    set_cell_margins(cell)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    if header:
        shade_cell(cell, HEADER_FILL)
    p = cell.paragraphs[0]
    set_spacing(p, before=0, after=0, line=1.05)
    r = p.add_run(text)
    set_run(r, size=9.5, bold=header or first_col)


def add_table(doc, headers, rows, widths):
    assert abs(sum(widths) - 6.0) < 0.02
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.allow_autofit = False
    tbl = table._tbl
    tbl_pr = tbl.tblPr
    tbl_w = tbl_pr.find(qn("w:tblW"))
    if tbl_w is None:
        tbl_w = OxmlElement("w:tblW")
        tbl_pr.append(tbl_w)
    tbl_w.set(qn("w:w"), str(CONTENT_DXA))
    tbl_w.set(qn("w:type"), "dxa")
    layout = tbl_pr.find(qn("w:tblLayout"))
    if layout is None:
        layout = OxmlElement("w:tblLayout")
        tbl_pr.append(layout)
    layout.set(qn("w:type"), "fixed")

    grid = tbl.find(qn("w:tblGrid"))
    if grid is None:
        grid = OxmlElement("w:tblGrid")
        tbl.insert(1, grid)
    for child in list(grid):
        grid.remove(child)
    for w in widths:
        col = OxmlElement("w:gridCol")
        col.set(qn("w:w"), str(int(w * 1440)))
        grid.append(col)

    def _cant_split(row):
        tr = row._tr
        tr_pr = tr.get_or_add_trPr()
        existing = tr_pr.find(qn("w:cantSplit"))
        if existing is None:
            tr_pr.append(OxmlElement("w:cantSplit"))

    def _repeat_header(row):
        tr = row._tr
        tr_pr = tr.get_or_add_trPr()
        existing = tr_pr.find(qn("w:tblHeader"))
        if existing is None:
            tr_pr.append(OxmlElement("w:tblHeader"))

    for i, h in enumerate(headers):
        fill_cell(table.rows[0].cells[i], h, header=True, width=widths[i])
    _repeat_header(table.rows[0])
    _cant_split(table.rows[0])
    for r_i, row in enumerate(rows):
        for c_i, val in enumerate(row):
            fill_cell(
                table.rows[r_i + 1].cells[c_i],
                val,
                first_col=(c_i == 0),
                width=widths[c_i],
            )
        _cant_split(table.rows[r_i + 1])
    return table


def body(doc, text, *, size=11, bold=False, italic=False, before=0, after=8):
    p = doc.add_paragraph()
    set_spacing(p, before=before, after=after)
    r = p.add_run(text)
    set_run(r, size=size, bold=bold, italic=italic)
    return p


def blank(doc):
    p = doc.add_paragraph()
    set_spacing(p, before=0, after=0)
    return p


def heading1(doc, text):
    p = doc.add_paragraph()
    p.style = doc.styles["Heading 1"]
    set_spacing(p, before=0, after=2)
    p.clear()
    r = p.add_run(text)
    set_run(r, size=11, bold=True)
    return p


def heading2(doc, text):
    p = doc.add_paragraph()
    p.style = doc.styles["Heading 2"]
    set_spacing(p, before=14, after=6)
    p.clear()
    r = p.add_run(text)
    set_run(r, size=11, bold=True)
    return p


def source_line(doc, pairs):
    """pairs: list of (label, url) after a 'Sources: ' prefix."""
    p = doc.add_paragraph()
    set_spacing(p, before=2, after=8)
    r = p.add_run("Sources: ")
    set_run(r, size=8.5)
    for i, (label, url) in enumerate(pairs):
        if i:
            sep = p.add_run("; ")
            set_run(sep, size=8.5)
        add_hyperlink(p, label, url, size=8.5)
    end = p.add_run(".")
    set_run(end, size=8.5)
    return p


def caption(doc, text):
    p = doc.add_paragraph()
    set_spacing(p, before=4, after=4)
    r = p.add_run(text)
    set_run(r, size=8.5, italic=True)
    return p


def main():
    doc = Document()
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.left_margin = Inches(1.25)
    section.right_margin = Inches(1.25)
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.header_distance = Inches(0.5)
    section.footer_distance = Inches(0.5)
    add_page_number(section)

    normal = doc.styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(11)
    rpr = normal.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    rfonts.set(qn("w:ascii"), "Arial")
    rfonts.set(qn("w:hAnsi"), "Arial")
    rfonts.set(qn("w:eastAsia"), "Arial")
    rfonts.set(qn("w:cs"), "Arial")

    def _force_heading_black(style_name, size_pt):
        st = doc.styles[style_name]
        st.font.name = "Arial"
        st.font.size = Pt(size_pt)
        st.font.bold = True
        st.font.color.rgb = BLACK
        rpr = st.element.get_or_add_rPr()
        rfonts = rpr.find(qn("w:rFonts"))
        if rfonts is None:
            rfonts = OxmlElement("w:rFonts")
            rpr.append(rfonts)
        rfonts.set(qn("w:ascii"), "Arial")
        rfonts.set(qn("w:hAnsi"), "Arial")
        rfonts.set(qn("w:eastAsia"), "Arial")

    _force_heading_black("Heading 1", 11)
    _force_heading_black("Heading 2", 11)

    heading1(doc, "Prepared for Stephen Friedberg | Dialectic Therapeutics")
    blank(doc)
    heading1(doc, "Japan Grant Landscape for DT2216")
    blank(doc)
    body(doc, "Last Updated: 08.31.2026", after=10)
    body(
        doc,
        "Source basis: official AMED, JSGO, JGOG, and foundation pages as of 31 August 2026. "
        "Dollar amounts are yen divided by 150 and are labeled arithmetic, not a live foreign-exchange quote. "
        "No Japan collaborator is named in Dialectic files. Dialectic is a Texas for-profit. "
        "The live trial is platinum-resistant ovarian cancer Phase 1b/2 (NCT06964009), Dana-Farber-led, "
        "principal investigator Elizabeth Stover. Dialectic / DT Sciences track. Separate from JDH.",
        size=8.5,
        italic=True,
        after=10,
    )

    heading2(doc, "Executive Summary:")
    body(
        doc,
        "Japan will not write a CPRIT-style check to Dallas. The large analogue is AMED\u2019s "
        "pharmaceutical-startup program: about $44 million from AMED if a Japan company and an "
        "AMED-certified lead venture firm are in place. That window closed 19 August 2026. "
        "Japan has no ovarian-only grant at trial scale. Two intakes are still open; Dialectic "
        "cannot draw either.",
    )
    body(
        doc,
        "Eligible cash to Dialectic as a Dallas-only applicant is zero on every Japan program "
        "in this file. The work now is a Japan company plus a certified-venture conversation "
        "before the next startup call, or a named Japan principal investigator for an FY2027 "
        "academic cancer filing. Near-term trial-scale application remains the United States "
        "CDMRP ovarian clinical-trial award, letter of intent 15 September 2026, about $2.8 million.",
    )

    heading2(doc, "The Large Option:")
    body(
        doc,
        "AMED Strengthening Program for Pharmaceutical Startup Ecosystem is the CPRIT Product "
        "Development twin. It funds company-run nonclinical, Phase 1, Phase 2, or exploratory "
        "clinical development of a drug, including cancer. The subsidized-cost ceiling is about "
        "$67 million (10 billion yen; larger proposals are allowed). AMED pays up to two-thirds, "
        "or about $44 million. A certified lead venture firm must put in at least one-third of "
        "subsidized costs, and at least about $6.7 million when the candidate is already chosen. "
        "DT2216 is a chosen candidate.",
    )
    body(
        doc,
        "The applicant is an unlisted Japan-registered company with a Japan research hub. A foreign "
        "100 percent parent plus Japan subsidiary is an explicit path if the certified firm funds "
        "the parent and the Japan company receives at least one-third of subsidized costs. Overseas "
        "development is allowed once the Japan hub exists.",
    )
    body(
        doc,
        "The program runs about four times a year. The fourteenth call closed 19 August 2026 at noon "
        "Japan time. Hearing is 15 October 2026 for applicants only. The thirteenth call closed "
        "15 May and was awarded 27 August; guidelines put start around early November. The fifteenth "
        "call is not posted. The last four windows were 15 October to 12 November 2025, 22 January "
        "to 20 February 2026, 14 April to 15 May 2026, and 21 July to 19 August 2026. Judgment: the "
        "next window is around mid-October to mid-November 2026.",
    )
    body(
        doc,
        "AMED takes confidential consults from companies and venture firms when a call is not open "
        "(v-eco@amed.go.jp). That is the workstream now: stand up a Japan company and start a "
        "certified-venture conversation before the next call.",
    )

    caption(
        doc,
        "Table 1. AMED pharmaceutical-startup program \u2014 facts that change the file",
    )
    add_table(
        doc,
        ["Item", "Fact", "Implication"],
        [
            [
                "Amount",
                "Ceiling about $67 million subsidized costs. AMED up to about $44 million. Lead certified venture at least about $6.7 million because DT2216 is a chosen candidate.",
                "This is the only Japan program at CPRIT Product Development scale.",
            ],
            [
                "Applicant",
                "Unlisted Japan company, or a 100 percent Japan subsidiary of a foreign parent, plus one AMED-certified lead venture firm.",
                "Dallas cannot be the awardee. No Japan company or certified-venture relationship is named in Dialectic files.",
            ],
            [
                "What it funds",
                "Company-run nonclinical through Phase 2 or exploratory proof of concept, including cancer. Overseas development is allowed once a Japan hub exists.",
                "Fits DT2216 development if the Japan hub and lead venture firm exist.",
            ],
            [
                "Dates",
                "Fourteenth call closed 19 August 2026. Hearing 15 October 2026, applicants only. Fifteenth call not posted.",
                "Judgment: next window around mid-October to mid-November 2026. Consult now; do not wait for the posting.",
            ],
        ],
        [1.15, 2.55, 2.30],
    )
    source_line(
        doc,
        [
            ("program home", "https://www.amed.go.jp/program/list/19/02/005.html"),
            ("fourteenth call", "https://www.amed.go.jp/koubo/03008/01/B_00015.html"),
            (
                "certified venture list",
                "https://www.amed.go.jp/program/list/19/02/005_Capital.html",
            ),
            (
                "thirteenth-call guidelines",
                "https://www.amed.go.jp/content/000158460.pdf",
            ),
        ],
    )

    heading2(doc, "What Is Open as of 31 August 2026:")
    body(
        doc,
        "No CPRIT-scale or trial-scale Japan grant is accepting applications today. Two intakes "
        "are open. Dialectic eligible cash on both is zero.",
    )

    caption(doc, "Table 2. Open Japan intakes as of 31 August 2026")
    add_table(
        doc,
        ["Program", "Amount", "Due", "Implication"],
        [
            [
                "AMED Drug Discovery Booster",
                "About $53,000 to $200,000 a year in experiments, plus optional CRO. In-kind, not a cash grant to a company.",
                "24 September 2026, noon Japan time",
                "Japan university or public-lab investigator only. Companies cannot apply. Not a trial award.",
            ],
            [
                "JSGO Nozawa Memorial (FY2027)",
                "$3,333 (500,000 yen). Up to three awards. One year of gynecologic-malignancy work.",
                "30 September 2026",
                "Under-50 Japan investigator, not a professor, one nominee per institution. Dialectic is not eligible.",
            ],
        ],
        [1.45, 1.85, 1.25, 1.45],
    )
    source_line(
        doc,
        [
            ("AMED Booster", "https://www.amed.go.jp/news/program/booster.html"),
            (
                "JSGO Nozawa FY2027",
                "https://jsgo.or.jp/entry_member/news/20260723/4313/",
            ),
        ],
    )

    heading2(doc, "Next-Largest Company Cash, Not Yet Open:")
    body(
        doc,
        "AMED pre-orphan is a company subsidy toward Japanese orphan designation and PMDA approval. "
        "Prior-year ceiling was about $333,000 a year before first-in-human and $667,000 a year after. "
        "Preview only: planned open early October to early November 2026. Ovarian platinum-resistant "
        "disease is not a Japan orphan path. DT2216\u2019s FDA orphan is T-cell lymphoma, a separate question.",
    )
    source_line(
        doc,
        [
            (
                "AMED pre-orphan program",
                "https://www.amed.go.jp/program/list/11/02/001_03-01.html",
            )
        ],
    )
    body(
        doc,
        "AMED Innovative Cancer Field 3-2 funds a Japan investigator-initiated trial of a new cancer "
        "drug toward Japanese approval. About $1.3 million over roughly two and a half years "
        "($287,000 in year one, then about $513,000 a year). Money stays with the Japan principal "
        "investigator. Closed 30 June 2026. Next cycle FY2027.",
    )
    source_line(
        doc,
        [
            (
                "Innovative Cancer FY2026 second call",
                "https://www.amed.go.jp/koubo/03005/02/B_00019.html",
            )
        ],
    )

    heading2(doc, "Ovarian-Specific Grants:")
    body(
        doc,
        "Japan has no OCRA or CDMRP ovarian-program equivalent. Nothing at trial scale is ovarian-only.",
    )
    body(
        doc,
        "JSGO Nozawa covers gynecologic malignancies, including ovary. Imai Seiichi Foundation covers "
        "perinatal, gynecologic oncology, reproductive, and women\u2019s health at about $13,333; that call "
        "closed 14 July 2026. JGOG runs ovarian trials and does not grant to companies. Smiley is "
        "advocacy and has no research-grant program.",
    )
    body(
        doc,
        "AMED has funded ovarian projects inside general cancer calls. That is topic-eligible, not an "
        "ovarian request for applications. The large AMED startup program is all diseases, including cancer.",
    )
    body(
        doc,
        "The ovarian-named, trial-scale application that is actually live is the United States CDMRP "
        "Ovarian Cancer Research Program Clinical Trial Award, letter of intent 15 September 2026, "
        "about $2.8 million.",
    )
    source_line(
        doc,
        [
            (
                "Imai Seiichi Foundation",
                "https://www.imaiseiichi-foundation.or.jp/subsidy/index.html",
            ),
            ("JGOG", "https://jgog.gr.jp/en"),
            ("CDMRP OCRP", "https://cdmrp.health.mil/funding/ocrp"),
        ],
    )

    heading2(doc, "Collaborators:")
    body(
        doc,
        "None of the following is a live named relationship in Dialectic files.",
    )
    body(
        doc,
        "The hard gate on the large program is one AMED-certified lead venture firm plus a Japan "
        "company. Clinical- or oncology-relevant names on the 1 April 2026 list include Blackstone "
        "Life Sciences, RA Capital, TPG Life Sciences Innovations, EQT Life Sciences, Curie Bio, "
        "4BIO Partners, Taiho Ventures, Astellas Venture Management, MP Healthcare, Catalys Pacific, "
        "Remiges, F-Prime / Eight Roads, JIC VGI, and Fast Track Initiative. The eighth certified-venture "
        "round was awarded 27 August 2026; re-check the list for adds.",
    )
    body(
        doc,
        "The academic path requires a Japan principal investigator at a Japan site. JGOG (181 sites) "
        "is the vehicle. President is Aikou Okamoto, Jikei University School of Medicine. National "
        "Cancer Center Central and East are core clinical-research hospitals. Elizabeth Stover at "
        "Dana-Farber can appear as a foreign collaborator, not as the Japan principal investigator. "
        "Dialectic would supply investigational product and the IND package and is paid only if the "
        "Japan award subcontracts the company.",
    )

    heading2(doc, "Recommended Next Step:")
    body(
        doc,
        "Staff the Japan company and a certified-venture conversation before the next AMED startup "
        "call. In parallel, name a JGOG or National Cancer Center principal investigator for an FY2027 "
        "Innovative Cancer Field 3-2 filing if a Japan investigator-initiated trial is the academic path.",
    )
    body(
        doc,
        "Do not staff JSGO Nozawa or the Booster as trial finance. Watch the AMED call list for the "
        "fifteenth startup round and the October pre-orphan posting. Near-term trial-scale application "
        "remains United States CDMRP OCRP, letter of intent 15 September 2026.",
    )
    source_line(
        doc,
        [("AMED call list", "https://www.amed.go.jp/koubo/koubo_index.html")],
    )

    heading2(doc, "Appendix:")
    caption(
        doc,
        "Table 3. Program comparison. Amounts are official yen ceilings converted at 150 yen per dollar "
        "(arithmetic). Status as of 31 August 2026.",
    )
    add_table(
        doc,
        ["Program", "Amount (USD)", "Status", "Implication"],
        [
            [
                "AMED pharmaceutical startup (CPRIT twin)",
                "Ceiling about $67M subsidized. AMED up to about $44M. Lead certified venture at least about $6.7M.",
                "14th closed 19 Aug 2026. Hearing 15 Oct, applicants only. Next call not posted. Judgment: mid-Oct to mid-Nov 2026.",
                "Only Japan door at CPRIT scale. Requires a Japan company and a certified lead venture firm.",
            ],
            [
                "AMED Innovative Cancer Field 3-2",
                "About $1.3M over ~2.5 years ($287k year 1, then about $513k a year).",
                "Closed 30 Jun 2026. Next cycle FY2027.",
                "Money stays with a Japan principal investigator. Dialectic is paid only if subcontracted.",
            ],
            [
                "AMED pre-orphan",
                "Prior year: about $333k a year before first-in-human; about $667k a year after.",
                "Preview. Planned open early Oct to early Nov 2026. Not open 31 Aug.",
                "Company cash, but ovarian platinum-resistant disease is a poor Japan-orphan fit.",
            ],
            [
                "AMED Drug Discovery Booster",
                "About $53k to $200k a year in experiments, plus optional CRO.",
                "Open. Next batch 24 Sep 2026, noon Japan time.",
                "In-kind academia seed support. Companies cannot apply. Not a trial award.",
            ],
            [
                "JSGO Nozawa Memorial (FY2027)",
                "$3,333 per award. Up to three awards.",
                "Open. Due 30 Sep 2026.",
                "Closest Japan gynecologic award. Society scale. Dialectic is not eligible.",
            ],
            [
                "Imai Seiichi Foundation",
                "About $13,333.",
                "Closed 14 Jul 2026.",
                "Women\u2019s-health / gynecologic research; investigator under 41.",
            ],
            [
                "JGOG",
                "None to Dialectic.",
                "Cooperative group. Not a company grantor.",
                "Vehicle for a Japan ovarian investigator-initiated trial, not a check.",
            ],
            [
                "U.S. CDMRP OCRP Clinical Trial Award",
                "About $2.8M total costs.",
                "Letter of intent 15 Sep 2026. Full application 1 Oct 2026.",
                "Live ovarian-named, trial-scale application. Not a Japan program.",
            ],
        ],
        [1.45, 1.45, 1.55, 1.55],
    )
    caption(
        doc,
        "Table 3 sources: AMED program and call pages cited above; JSGO; Imai Seiichi Foundation; "
        "JGOG; CDMRP OCRP. Cutoff 31 August 2026.",
    )

    body(doc, "Official links:", size=11, bold=True, before=12, after=4)
    links = [
        ("AMED all calls", "https://www.amed.go.jp/koubo/koubo_index.html"),
        ("e-Rad submissions", "https://www.e-rad.go.jp/"),
        ("AMED startup program", "https://www.amed.go.jp/program/list/19/02/005.html"),
        ("Fourteenth startup call", "https://www.amed.go.jp/koubo/03008/01/B_00015.html"),
        (
            "Certified venture contacts",
            "https://www.amed.go.jp/program/list/19/02/005_Capital.html",
        ),
        (
            "Thirteenth-call guidelines (PDF)",
            "https://www.amed.go.jp/content/000158460.pdf",
        ),
        ("Booster intake", "https://www.amed.go.jp/news/program/booster.html"),
        (
            "Innovative Cancer FY2026 second call",
            "https://www.amed.go.jp/koubo/03005/02/B_00019.html",
        ),
        (
            "Pre-orphan program",
            "https://www.amed.go.jp/program/list/11/02/001_03-01.html",
        ),
        ("JSGO Nozawa FY2027", "https://jsgo.or.jp/entry_member/news/20260723/4313/"),
        ("JGOG", "https://jgog.gr.jp/en"),
        (
            "Imai Seiichi Foundation",
            "https://www.imaiseiichi-foundation.or.jp/subsidy/index.html",
        ),
        ("CDMRP OCRP", "https://cdmrp.health.mil/funding/ocrp"),
    ]
    for label, url in links:
        p = doc.add_paragraph()
        set_spacing(p, before=0, after=3)
        p.paragraph_format.left_indent = Inches(0.15)
        add_hyperlink(p, label, url, size=10)

    doc.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
