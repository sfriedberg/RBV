#!/usr/bin/env python3
"""TAP inquiry pack on Dialectic's designed slides.

Copies the company presentation. Keeps chrome and figures.
Rewrites only the frames that have to carry the TAP/CTCL ask.
Writes into existing paragraphs — never dumps '\\n' into a single run.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from pptx import Presentation
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "Dialectic_Presentation_09.03.26_ORIGINAL_AS_RECEIVED.pptx"
DST = ROOT / "Dialectic_TAP_Inquiry_CTCL_091426.pptx"

# Cover → TOC → ask → T-cell BCL-XL → vs navitoclax → MOLT4/Khan →
# He/MyLa → Phase 1a → CTCL design → pipeline → team → IP.
# Dropped the BRET/specificity figure (orig 8): navitoclax + MOLT4 cover that ground.
KEEP = [0, 2, 3, 7, 11, 9, 19, 21, 22, 6, 5, 28]


def set_paragraph_text(paragraph, text: str) -> None:
    """Replace a paragraph without inventing line breaks or extra runs."""
    if "\n" in text:
        raise ValueError(f"paragraph text must be a single line: {text!r}")
    if not paragraph.runs:
        paragraph.text = text
        return
    paragraph.runs[0].text = text
    for run in paragraph.runs[1:]:
        run.text = ""


def set_shape_lines(shape, lines: list[str]) -> None:
    """Map lines onto existing paragraphs; clear leftovers. Do not add frames."""
    frame = getattr(shape, "text_frame", None)
    if frame is None:
        return
    paragraphs = list(frame.paragraphs)
    for index, paragraph in enumerate(paragraphs):
        set_paragraph_text(paragraph, lines[index] if index < len(lines) else "")


def shape_named(slide, name: str):
    for shape in slide.shapes:
        if shape.name == name:
            return shape
    raise KeyError(name)


def first_shape_containing(slide, needle: str):
    for shape in slide.shapes:
        if shape.has_text_frame and needle in shape.text_frame.text:
            return shape
    raise KeyError(needle)


def drop_shapes(slide, names: set[str]) -> None:
    for shape in list(slide.shapes):
        if shape.name in names:
            shape._element.getparent().remove(shape._element)


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


def set_page_numbers(prs) -> None:
    for number, slide in enumerate(prs.slides, 1):
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            compact = shape.text_frame.text.replace("\n", "").replace(" ", "").strip()
            if compact.isdigit() and shape.left > Inches(11.4) and shape.top > Inches(6.55):
                set_shape_lines(shape, [str(number)])
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        if run.font.size is None:
                            run.font.size = Pt(11)


def rewrite_cover(slide) -> None:
    set_shape_lines(first_shape_containing(slide, "Company Presentation"), ["TAP Inquiry"])
    set_shape_lines(first_shape_containing(slide, "CONFIDENTIAL"), ["NON-CONFIDENTIAL", ""])
    set_shape_lines(first_shape_containing(slide, "August 12, 2026"), ["September 16, 2026"])


def rewrite_toc(slide) -> None:
    # Seven company TOC slots. Keep that count so bullets and spacing stay designed.
    set_shape_lines(
        first_shape_containing(slide, "Company Overview"),
        [
            "The TAP ask",
            "Why BCL-XL in T-cell lymphoma",
            "CTCL and T-ALL preclinical evidence",
            "Phase 1a: dose in hand, no heme patients",
            "Proposed CTCL Phase 2",
            "Solid-tumor trials that are not this ask",
            "Team and intellectual property",
        ],
    )


def rewrite_exec(slide) -> None:
    body = first_shape_containing(slide, "Company Overview: Founded")
    # p1–p2 were the APTaD platform tour. TAP funds a blood-cancer path, not a platform.
    # p10–p17 were the IP dump; IP already has its own closing slide.
    set_paragraph_text(
        body.text_frame.paragraphs[0],
        (
            "Company Overview: Dialectic Therapeutics is a Dallas clinical-stage company "
            "developing DT2216, a VHL-based BCL-XL PROTAC (APTaD®). FDA orphan designation "
            "covers T-cell lymphoma; Fast Track covers adult relapsed/refractory PTCL and CTCL."
        ),
    )
    set_paragraph_text(
        body.text_frame.paragraphs[1],
        (
            "The TAP thesis: fund the first CTCL clinical cohort under the existing IND. "
            "Do not rediscover BCL-XL."
        ),
    )
    set_paragraph_text(
        body.text_frame.paragraphs[2],
        (
            "Mature T cells down-regulate BCL-XL after thymic selection; many T-cell lymphomas "
            "re-express it. That is the orphan / Fast Track rationale."
        ),
    )
    set_paragraph_text(
        body.text_frame.paragraphs[4],
        (
            "TAP inquiry: DT2216 for cutaneous T-cell lymphoma. Phase 1a is complete. "
            "The first blood-cancer cohort has not been opened. That is the ask."
        ),
    )
    set_paragraph_text(
        body.text_frame.paragraphs[5],
        (
            "Phase 1a established the RP2D of 0.40 mg/kg IV twice weekly, showed transient "
            "manageable thrombocytopenia, and produced complete, sustained BCL-XL degradation "
            "in PBMCs at that dose. No CTCL or PTCL patients were enrolled."
        ),
    )
    set_paragraph_text(
        body.text_frame.paragraphs[6],
        (
            "Published CTCL and T-ALL models show single-agent activity versus navitoclax "
            "with less platelet toxicity (He et al., J Hematol Oncol 2020; Khan et al., Nat Med 2019)."
        ),
    )
    set_paragraph_text(
        body.text_frame.paragraphs[7],
        (
            "Trial-design discussions with MD Anderson (Drs. Iyer and Akkad) are underway "
            "for a CTCL Phase 2, targeting initiation in 2027. n, IND amendment, and "
            "steroid use remain open."
        ),
    )
    set_paragraph_text(
        body.text_frame.paragraphs[8],
        (
            "Two solid-tumor combination trials (PROC NCT06964009; COG/FLC NCT06620302) "
            "are not this TAP ask. CPRIT TXCO DP210005 supported T-cell lymphoma and SCLC work."
        ),
    )
    set_paragraph_text(
        body.text_frame.paragraphs[10],
        (
            "Use of proceeds (12 months): first CTCL Phase 2 cohort — investigational product, "
            "CRO, 1–2 sites. Dollar ask open with the board."
        ),
    )
    set_paragraph_text(
        body.text_frame.paragraphs[11],
        (
            "Population: relapsed/refractory CTCL after approved agents (mogamulizumab, "
            "brentuximab, HDAC inhibitors, denileukin diftitox). Not front-line."
        ),
    )
    set_paragraph_text(
        body.text_frame.paragraphs[12],
        (
            "Intellectual property (high level): exclusive UAMS license; issued U.S. DT2216 "
            "composition patents, company-reported expiry 2037."
        ),
    )
    for index in (13, 14, 15, 16, 17):
        set_paragraph_text(body.text_frame.paragraphs[index], "")


def rewrite_bclxl(slide) -> None:
    """Keep the company figure; retitle the science as T-cell lymphoma, not SnC/Treg."""
    body = first_shape_containing(slide, "Rationale for Targeting")
    set_paragraph_text(body.text_frame.paragraphs[0], "Why BCL-XL in T-cell lymphoma:")
    set_paragraph_text(
        body.text_frame.paragraphs[1],
        (
            "Mature T cells down-regulate BCL-XL after thymic selection; many T-cell lymphomas "
            "re-express it as a survival factor."
        ),
    )
    set_paragraph_text(
        body.text_frame.paragraphs[2],
        (
            "That re-expression is the orphan / Fast Track rationale — not a solid-tumor-first story."
        ),
    )
    set_paragraph_text(body.text_frame.paragraphs[3], "Published heme models:")
    set_paragraph_text(
        body.text_frame.paragraphs[4],
        "MyLa CTCL xenograft — He et al., J Hematol Oncol 2020",
    )
    set_paragraph_text(
        body.text_frame.paragraphs[5],
        "MOLT-4 T-ALL — Khan et al., Nat Med 2019",
    )
    set_paragraph_text(
        body.text_frame.paragraphs[6],
        "Single-agent activity versus navitoclax, with less platelet toxicity",
    )
    set_paragraph_text(body.text_frame.paragraphs[8], "Why not a conventional inhibitor:")
    set_paragraph_text(
        body.text_frame.paragraphs[9],
        "Continuous BCL-XL inhibition (navitoclax) is dose-limited by thrombocytopenia",
    )
    set_paragraph_text(body.text_frame.paragraphs[11], "Dialectic's solution:")
    set_paragraph_text(
        body.text_frame.paragraphs[12],
        (
            "DT2216 degrades BCL-XL in VHL-competent tumor cells and spares platelets, "
            "which lack the ligase machinery"
        ),
    )
    set_shape_lines(
        first_shape_containing(slide, "Scientific Foundation"),
        ["Why BCL-XL in T-cell lymphoma — and why a degrader"],
    )
    set_shape_lines(
        first_shape_containing(slide, "target tumor cells, SnCs"),
        ["DT2216 degrades BCL-XL in T-cell models and spares platelets"],
    )
    set_shape_lines(
        first_shape_containing(slide, "common survival factor"),
        ["The TAP setting: T-cell lymphomas re-express BCL-XL"],
    )


def rewrite_phase1a(slide) -> None:
    set_shape_lines(
        shape_named(slide, "Title 1"),
        ["Phase 1a set a human dose. It did not enroll CTCL."],
    )
    body = first_shape_containing(slide, "Study: Open-label")
    set_paragraph_text(
        body.text_frame.paragraphs[0],
        (
            "Study: Open-label, first-in-human dose escalation in relapsed/refractory solid tumors "
            "(n=20). No CTCL or PTCL patients enrolled. Mahadevan et al., J Hematol Oncol 2025."
        ),
    )


def rewrite_trial_design(slide) -> None:
    """PROC two-row chassis: top = completed Phase 1a; bottom = proposed CTCL Phase 2.

    Do not turn this into a fake CTCL Phase 1b. Josh's frame is direct-to-Phase 2.
    """
    # DFCI logo and "Lead site / PI" belong to the PROC protocol, not this ask.
    drop_shapes(slide, {"Picture 29", "TextBox 27"})
    set_shape_lines(shape_named(slide, "Title 1"), ["Proposed CTCL Phase 2 — the TAP ask"])

    set_shape_lines(
        shape_named(slide, "Rectangle 6"),
        [
            "Completed",
            "Phase 1a",
            "",
            "n=20",
            "",
            "Solid tumors",
            "RP2D set",
        ],
    )
    set_shape_lines(
        shape_named(slide, "Rectangle 12"),
        [
            "What was studied",
            "",
            "",
            "Relapsed/refractory solid malignancies",
            "No CTCL or PTCL enrolled",
            "Published: Mahadevan et al., 2025",
        ],
    )
    set_shape_lines(
        shape_named(slide, "Rectangle 13"),
        [
            "Dosing",
            "",
            "DT2216 monotherapy",
            "0.40 mg/kg IV twice weekly",
            "30-minute infusion",
            "No combination in Phase 1a",
        ],
    )
    set_shape_lines(
        shape_named(slide, "Rectangle 14"),
        [
            "What was shown",
            "",
            "",
            "RP2D 0.40 mg/kg",
            "PBMC BCL-XL degraded",
            "Transient, recoverable platelets",
            "No single-agent solid-tumor ORR",
        ],
    )
    set_shape_lines(
        shape_named(slide, "Rectangle 18"),
        [
            "Proposed",
            "CTCL Phase 2",
            "",
            "n to lock",
            "",
            "1–2 sites",
            "",
            "Target start 2027",
            "Working design",
        ],
    )
    set_shape_lines(
        shape_named(slide, "Rectangle 23"),
        [
            "Eligibility",
            "",
            "Relapsed/refractory CTCL",
            "After approved agents",
            "Not front-line",
            "",
            "MDA design discussions",
            "Iyer and Akkad",
            "",
        ],
    )
    set_shape_lines(
        shape_named(slide, "Rectangle 24"),
        [
            "Dosing",
            "",
            "0.40 mg/kg IV BIW ± dex",
            "(open with MDA)",
            "",
            "",
        ],
    )
    set_shape_lines(
        shape_named(slide, "Rectangle 25"),
        [
            "Outcomes",
            "",
            "Primary: safety in a heme population",
            "Activity by mSWAT",
            "Go/no-go on expansion",
        ],
    )
    set_shape_lines(
        shape_named(slide, "TextBox 26"),
        [
            "Working design from the 1 Sep TAP 1-pager. Not a locked protocol. n and steroid use remain open with MDA."
        ],
    )
    set_shape_lines(shape_named(slide, "TextBox 31"), ["MDA design: Iyer / Akkad"])


def rewrite_pipeline(slide) -> None:
    set_shape_lines(
        first_shape_containing(slide, "Strong pipeline of protein degraders"),
        ["Pipeline: proposed CTCL Phase 2 is the TAP ask"],
    )
    set_shape_lines(shape_named(slide, "Arrow: Right 78"), ["CTCL Phase 2 (TAP ask)"])
    # Left rail sits on the PROC/FLC rows (T~2.3), not the CTCL row (T~3.3).
    # Do not claim "currently dosing" — enrollment status is a Josh sentence.
    set_shape_lines(
        first_shape_containing(slide, "Currently"),
        ["Solid-tumor", "trials", "not this ask"],
    )
    set_shape_lines(
        first_shape_containing(slide, "Source: Company information"),
        [
            "Source: Company information. Milestone timing is an estimate. PROC and FLC are not this TAP ask."
        ],
    )
    for shape in slide.shapes:
        if not shape.has_table:
            continue
        method = shape.table.cell(5, 1)
        set_shape_lines(method, ["Monotherapy", "(± dex to lock)"])


def main() -> None:
    shutil.copy2(SRC, DST)
    prs = Presentation(str(DST))
    slides = list(prs.slides)

    rewrite_cover(slides[0])
    rewrite_toc(slides[2])
    rewrite_exec(slides[3])
    rewrite_bclxl(slides[7])
    rewrite_phase1a(slides[21])
    rewrite_trial_design(slides[22])
    rewrite_pipeline(slides[6])

    keep_slides(prs, KEEP)
    set_page_numbers(prs)
    prs.core_properties.title = "DT2216 — TAP Inquiry — CTCL Phase 2"
    prs.core_properties.subject = "Blood Cancer United Therapy Acceleration Program"
    prs.core_properties.comments = (
        "Non-confidential TAP pack. Company slides only; PROC design chassis "
        "reused as Phase 1a vs proposed CTCL Phase 2. Not sent."
    )
    prs.save(str(DST))
    print(DST)
    print("slides", len(Presentation(str(DST)).slides))


if __name__ == "__main__":
    main()
