# Dialectic Full-Deck Polish Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a separate, source-audited 34-slide Dialectic investor presentation with consistent writing, design and evidence standards.

**Architecture:** Use the existing A+ draft as the immutable source presentation. Rebuild the dense legacy slides in place with `python-pptx`, retain the strongest current slides, and apply a global typography, title, footer and page-number pass. Keep factual content in a slide manifest, record source support in a claim ledger, and validate the generated presentation with a separate verification script before visual review.

**Tech Stack:** Python 3, `python-pptx`, Pillow, LibreOffice, Poppler, MarkItDown, local DeepSeek-V4-Flash.

## Global Constraints

- Keep exactly 34 slides and preserve the current topic order.
- Preserve `drafts/Dialectic_Presentation_09.03.26_A_PLUS_DRAFT.pptx` unchanged.
- Save the new deck as `drafts/Dialectic_Presentation_09.04.26_A_PLUS_REFINED.pptx`.
- Keep all confidential scientific materials local.
- Use no cloud-model review of the manuscript or scientific exhibits.
- Use natural company-authored prose. Avoid slogans, arrow-chain sentences, mechanical labels, generic marketing language and repetitive constructions.
- Keep DT2216 plus weekly paclitaxel in platinum-resistant ovarian cancer as the primary clinical thesis.
- Describe the Qin Figure 4 work as free microtubule-payload data. Do not imply that intact Elahere was tested.
- Label submitted-manuscript findings as confidential and not peer reviewed.
- Label future pipeline dates and unpublished programs as company estimates.
- Use normal body text of at least 15 points, except the legal disclaimer, source notes and labels embedded in scientific figures.
- Do not email or otherwise distribute the refined file without Stephen's explicit instruction after review.
- This workspace is not a Git repository. Do not initialize Git or create commits.

---

### Task 1: Build the claim and source ledger

**Files:**
- Create: `drafts/Dialectic_Presentation_09.04.26_CLAIM_LEDGER.md`
- Read: `drafts/Dialectic_Presentation_09.03.26_A_PLUS_DRAFT_extract.md`
- Read: `sources/Mahadevan_JHO_2025_DT2216_Phase1.txt`
- Read: `sources/kris-forward-2026-09-03/BCLXL_Chemoresistance_2026-07-21.txt`
- Read: `sources/kris-forward-2026-09-03/SOURCE_MANIFEST.md`
- Read: `sources/Dialectic_Presentation_09.03.26_vDRAFT_extract.md`

**Interfaces:**
- Produces: A slide-by-slide record with fields `slide`, `claim`, `source`, `status`, `required_wording` and `notes`.
- Consumes: Controlling company, publication, trial-registry and submitted-manuscript evidence.

- [ ] **Step 1: Inventory every material claim**

Record every scientific result, clinical result, dose, sample size, date, milestone, market statistic, institutional affiliation, collaboration and IP statement from the current deck.

- [ ] **Step 2: Assign one of four statuses**

Use only:

```text
VERIFIED
COMPANY-SUPPLIED
FORWARD-LOOKING COMPANY ESTIMATE
REMOVE OR REWRITE
```

- [ ] **Step 3: Verify public claims from primary sources**

Use peer-reviewed publications, ClinicalTrials.gov and official company or regulator materials. Verify the Revolution Medicines comparison, trial identifiers and status, dosing, patient counts, milestone dates and patent statements. If a primary source is unavailable, remove the numerical or categorical claim rather than relying on an unsourced secondary statement.

- [ ] **Step 4: Verify confidential scientific claims locally**

Check all Qin manuscript statements against the July 2026 manuscript and supplied Figure 4. Confirm:

```text
Figure 3: 55 cell lines, 12 tumor types, synergy at one or more tested doses
Figure 4E: n=3 biological replicates
Figure 4F: DM4 and MMAE n=3; MMAF n=1 biological replicate
Figure 6D: 7 of 8 HGSOC PDX models showed ex-vivo synergy
Figure 8 flank: treatment stopped at day 138; no regrowth during 100 additional days
Figure 8 disseminated model: background-level signal by day 40; median survival increased 35 days versus paclitaxel
```

- [ ] **Step 5: Verify Phase 1 statements**

Check all Mahadevan Phase 1 statements against the publication, including:

```text
20 patients
0.40 mg/kg IV twice weekly recommended Phase 2 dose
thrombocytopenia in 9 of 20 patients
one dose-limiting grade 4 thrombocytopenia event resolved within 48 hours
no major bleeding, treatment-related deaths or platelet transfusions reported
stable disease as best RECIST response in 4 of 20 patients
median stable-disease duration of 107 days
```

- [ ] **Step 6: Review the completed ledger**

Expected result: every material claim has a source and status; no row remains blank.

---

### Task 2: Define the final slide manifest

**Files:**
- Create: `drafts/refined_deck_content.py`
- Consume: `drafts/Dialectic_Presentation_09.04.26_CLAIM_LEDGER.md`

**Interfaces:**
- Produces: `SLIDES: dict[int, SlideSpec]`
- Produces: `SlideSpec(number: int, title: str, subtitle: str, body: tuple[str, ...], source: str, status_note: str)`
- Consumes: Verified or explicitly labeled content from Task 1.

- [ ] **Step 1: Define the content type**

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class SlideSpec:
    number: int
    title: str
    subtitle: str = ""
    body: tuple[str, ...] = ()
    source: str = ""
    status_note: str = ""
```

- [ ] **Step 2: Define all 34 slide titles**

Use the following topic sequence:

```python
SLIDE_TITLES = {
    1: "Creating Innovative Technologies to Treat Cancer",
    2: "Disclaimer",
    3: "Presentation Overview",
    4: "DT2216 plus weekly paclitaxel is the lead value-creation program",
    5: "A different modality can unlock a validated but previously constrained target",
    6: "Leadership and scientific advisors",
    7: "DT2216 is the clinical priority within a broader degrader pipeline",
    8: "BCL-XL is biologically validated but direct inhibition is limited by platelet toxicity",
    9: "DT2216 uses VHL-mediated degradation to target BCL-XL selectively",
    10: "Tumor BCL-XL degradation outlasted the effect measured in circulating white blood cells",
    11: "Tissue retention can sustain pharmacology after plasma concentrations decline",
    12: "Intermittent degradation differs from continuous BCL-XL inhibition",
    13: "Platelet recovery supports intermittent BCL-XL degradation",
    14: "DT2216 exposure is substantially higher in tumor tissue than in plasma",
    15: "Preclinical evidence spans multiple models, with the strongest current case in ovarian cancer",
    16: "Preclinical programs support one active lead thesis and several additional options",
    17: "DT2216 plus paclitaxel targets complementary survival pathways",
    18: "Paclitaxel moves surviving HGSOC cells onto BCL-XL",
    19: "Seven of eight patient-derived ovarian models showed combination synergy ex vivo",
    20: "DT2216 plus paclitaxel produced durable control in two DF83 PDX settings",
    21: "DT2216 plus paclitaxel showed in-vitro synergy across 55 cell lines and 12 tumor types",
    22: "DT2216 increased apoptosis with three microtubule ADC payloads in OVCAR8",
    23: "DT2216 plus irinotecan produced regression in fibrolamellar carcinoma PDX models",
    24: "DT2216 showed antitumor activity with less platelet toxicity than navitoclax in a CTCL xenograft",
    25: "DT2216 plus fulvestrant is an unpublished ER-positive breast-cancer development option",
    26: "Phase 1 established a human dose and systemic target engagement",
    27: "Phase 1 established systemic pharmacodynamics; Phase 1b will test tumor pharmacodynamics",
    28: "The Phase 1b/2 study directly tests DT2216 plus weekly paclitaxel in PROC",
    29: "The FLC Phase 1b/2 study tests DT2216 plus irinotecan",
    30: "The ovarian combination readout is the primary near-term value inflection",
    31: "Key questions for the ovarian program",
    32: "Licensed patent rights cover DT2216, DT5321 and related BCL-family degraders",
    33: "Academic collaborations broaden the evidence base and development options",
    34: "Selected publications supporting the DT2216 platform",
}
```

- [ ] **Step 3: Write concise, sourced content for every rebuilt slide**

Each rebuilt slide must contain no more than one conclusion, three supporting points and one source line. Exceptions are slides 2, 6, 29, 33 and 34, where the legal or reference function requires more entries.

- [ ] **Step 4: Run a content-manifest check**

Run:

```bash
python3 - <<'PY'
from drafts.refined_deck_content import SLIDES, SLIDE_TITLES
assert set(SLIDE_TITLES) == set(range(1, 35))
assert set(SLIDES) == set(range(1, 35))
for number, spec in SLIDES.items():
    assert spec.number == number
    assert spec.title == SLIDE_TITLES[number]
print("PASS: 34 complete slide specifications")
PY
```

Expected: `PASS: 34 complete slide specifications`

---

### Task 3: Build the refined presentation

**Files:**
- Create: `drafts/build_refined_deck.py`
- Read: `drafts/build_aplus_deck.py`
- Read: `drafts/refined_deck_content.py`
- Source: `drafts/Dialectic_Presentation_09.03.26_A_PLUS_DRAFT.pptx`
- Create: `drafts/Dialectic_Presentation_09.04.26_A_PLUS_REFINED.pptx`

**Interfaces:**
- Consumes: `SLIDES` and `SLIDE_TITLES` from `refined_deck_content.py`
- Produces: `build() -> pathlib.Path`
- Produces: 34-slide `.pptx` with the approved topic order.

- [ ] **Step 1: Copy the existing helper layer**

Reuse and tighten the existing color, text, panel, picture and footer helpers. Set:

```python
TEAL = RGBColor(0x00, 0xA9, 0x98)
DEEP_TEAL = RGBColor(0x00, 0x72, 0x69)
NAVY = RGBColor(0x1F, 0x4E, 0x79)
DARK = RGBColor(0x1F, 0x29, 0x33)
MID = RGBColor(0x4D, 0x5B, 0x66)
LIGHT = RGBColor(0xF3, 0xF6, 0xF7)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
FONT = "Aptos"
FONT_DISPLAY = "Aptos Display"
BODY_MIN_PT = 15
SOURCE_PT = 9
```

- [ ] **Step 2: Add explicit slide-replacement helpers**

Define:

```python
def delete_slide(prs: Presentation, index: int) -> None: ...
def insert_slide_at(prs: Presentation, slide, index: int) -> None: ...
def replace_slide(prs: Presentation, index: int, builder) -> None: ...
def apply_global_style(prs: Presentation) -> None: ...
def set_page_numbers(prs: Presentation) -> None: ...
```

Use the slide relationship IDs when deleting and reordering. Do not edit the source presentation in place.

- [ ] **Step 3: Preserve slides that already meet the standard**

Retain slides 1, 2, 4, 13, 17–22, 26–28 and 31 as the content base. Apply only title, footer, page-number, spacing and copy corrections supported by the claim ledger.

- [ ] **Step 4: Rebuild slides 3, 5–12, 14–16, 23–25, 29–30 and 32–34**

Use the slide manifest and the following layouts:

```text
3   short section list
5   restrained two-column modality comparison
6   three-column board, management and scientific-advisor roster
7   active, planned and research pipeline lanes
8   target biology diagram plus platelet-toxicity constraint
9   molecule-mechanism visual plus specificity evidence
10  two-panel tumor-versus-blood duration comparison
11  plasma-to-tissue-to-pharmacology sequence with supporting figure
12  balanced DT2216-versus-navitoclax comparison
14  large tissue/plasma figure plus two measured conclusions
15  published evidence matrix, grouped by indication and evidence type
16  four-program evidence and development map
23  FLC PDX evidence with one principal chart and one treatment timeline
24  CTCL xenograft evidence with tumor, platelet and survival panels
25  ER-positive breast-cancer evidence clearly marked unpublished
29  two-row Phase 1b and Phase 2 trial-design summary
30  completed, active and estimated catalyst timeline
32  licensed-rights, issued-patent and strategy columns
33  simplified collaboration map grouped by active asset
34  publications grouped as clinical, ovarian mechanism and platform foundation
```

- [ ] **Step 5: Apply the global style**

Enforce:

```text
0.45-inch minimum left and right margins
single consistent title bar
15-point minimum normal body copy
9-point minimum source line
one source line above the page footer
no title underlines
no decorative chevron chains
no low-contrast gray body copy
no duplicate page numbers
```

- [ ] **Step 6: Save and reopen the deck**

Run:

```bash
python3 drafts/build_refined_deck.py
python3 - <<'PY'
from pptx import Presentation
path = "drafts/Dialectic_Presentation_09.04.26_A_PLUS_REFINED.pptx"
prs = Presentation(path)
assert len(prs.slides) == 34
print(f"PASS: {len(prs.slides)} slides")
PY
```

Expected: `PASS: 34 slides`

---

### Task 4: Add structural and copy verification

**Files:**
- Create: `drafts/verify_refined_deck.py`
- Test: `drafts/Dialectic_Presentation_09.04.26_A_PLUS_REFINED.pptx`

**Interfaces:**
- Consumes: Path to a `.pptx`
- Produces: process exit code `0` on pass and a printed list of failures otherwise.

- [ ] **Step 1: Implement presentation checks**

Include:

```python
def extract_text(prs: Presentation) -> list[str]: ...
def check_slide_count(prs: Presentation) -> list[str]: ...
def check_titles(prs: Presentation) -> list[str]: ...
def check_page_numbers(prs: Presentation) -> list[str]: ...
def check_required_phrases(text: str) -> list[str]: ...
def check_banned_phrases(text: str) -> list[str]: ...
def check_manuscript_labels(slides: list[str]) -> list[str]: ...
def check_minimum_font_sizes(prs: Presentation) -> list[str]: ...
```

- [ ] **Step 2: Require critical wording**

```python
REQUIRED = [
    "DT2216 plus weekly paclitaxel",
    "0.40 mg/kg",
    "7 of 8",
    "55",
    "12 tumor types",
    "Free payload was tested; the intact ADC was not",
    "confidential",
    "not peer reviewed",
]
```

- [ ] **Step 3: Ban unsupported or stale wording**

```python
BANNED = [
    "Dosing stopped day 130",
    "no tumor detectable day 236",
    "Elahere combination",
    "intact Elahere",
    "all dose combinations were synergistic",
    "no platelet toxicity",
    "proven safety superiority",
    "owns the entire APTaD",
    "H2 2025",
    "upcoming Phase 1b/2 pediatric COG trial",
]
```

- [ ] **Step 4: Run verification**

Run:

```bash
python3 drafts/verify_refined_deck.py \
  drafts/Dialectic_Presentation_09.04.26_A_PLUS_REFINED.pptx
```

Expected:

```text
PASS: 34 slides
PASS: titles and page numbers
PASS: critical wording
PASS: manuscript labels
PASS: no banned wording
PASS: font-size policy
```

---

### Task 5: Conduct factual and narrative review

**Files:**
- Modify: `drafts/Dialectic_Presentation_09.04.26_CLAIM_LEDGER.md`
- Modify: `drafts/refined_deck_content.py`
- Modify: `drafts/build_refined_deck.py`

**Interfaces:**
- Consumes: Extracted text from the generated deck and controlling sources.
- Produces: Corrected slide copy and a ledger with no unresolved material claims.

- [ ] **Step 1: Extract the generated deck**

Run:

```bash
python3 -m markitdown \
  "drafts/Dialectic_Presentation_09.04.26_A_PLUS_REFINED.pptx" \
  > "drafts/Dialectic_Presentation_09.04.26_A_PLUS_REFINED_extract.md"
```

- [ ] **Step 2: Run two private local reviews**

Ask local DeepSeek-V4-Flash to review:

1. scientific and clinical claims against the Mahadevan publication and July 2026 Qin manuscript;
2. investor narrative, overstatement, repetition and slide-to-slide logic.

Require each review to identify the slide number, exact wording, source conflict and replacement wording.

- [ ] **Step 3: Resolve every finding**

For each finding, either:

```text
CORRECTED
RETAINED WITH SOURCE SUPPORT
REMOVED
```

Record the disposition in the claim ledger.

- [ ] **Step 4: Rebuild and rerun verification**

Run:

```bash
python3 drafts/build_refined_deck.py
python3 drafts/verify_refined_deck.py \
  drafts/Dialectic_Presentation_09.04.26_A_PLUS_REFINED.pptx
```

Expected: all checks pass.

---

### Task 6: Render, inspect and correct the presentation

**Files:**
- Create: `drafts/qa-refined/`
- Create: `drafts/qa-refined/Dialectic_Presentation_09.04.26_A_PLUS_REFINED.pdf`
- Create: `drafts/qa-refined/slide-01.jpg` through `slide-34.jpg`
- Create: `drafts/qa-refined/contact-sheet.jpg`

**Interfaces:**
- Consumes: Final `.pptx`
- Produces: 34 rendered slide images and one contact sheet.

- [ ] **Step 1: Render the presentation**

Run:

```bash
"/Applications/LibreOffice.app/Contents/MacOS/soffice" \
  --headless \
  --convert-to pdf \
  --outdir "drafts/qa-refined" \
  "drafts/Dialectic_Presentation_09.04.26_A_PLUS_REFINED.pptx"

pdftoppm \
  -jpeg \
  -r 180 \
  "drafts/qa-refined/Dialectic_Presentation_09.04.26_A_PLUS_REFINED.pdf" \
  "drafts/qa-refined/slide"
```

- [ ] **Step 2: Build and inspect the contact sheet**

Use Pillow to create a four-column contact sheet with slide numbers. Inspect all 34 slides for hierarchy, readability, consistency and density.

- [ ] **Step 3: Inspect high-risk slides at full size**

Review slides 5, 6, 7, 8, 11, 12, 15, 16, 17–22, 23–25, 29, 30, 32, 33 and 34 individually.

- [ ] **Step 4: Complete one correction cycle**

Fix every observed overlap, overflow, weak contrast, unreadable figure, inconsistent source line, excessive wrapping and margin violation. Rebuild and rerender all affected slides.

- [ ] **Step 5: Complete a fresh-eyes final pass**

Expected: no new visual issue is found. If a new issue is found, repeat Step 4.

---

### Task 7: Document and present the result

**Files:**
- Create: `drafts/Dialectic_Presentation_09.04.26_A_PLUS_REFINED_CHANGES.md`
- Preserve: `drafts/Dialectic_Presentation_09.03.26_A_PLUS_DRAFT.pptx`
- Final: `drafts/Dialectic_Presentation_09.04.26_A_PLUS_REFINED.pptx`

**Interfaces:**
- Consumes: Verified final deck and claim ledger.
- Produces: Review package for Stephen.

- [ ] **Step 1: Write the change log**

List the major changes by slide range, factual corrections, source-label changes and items intentionally retained.

- [ ] **Step 2: Hash the original and refined files**

Run:

```bash
shasum -a 256 \
  "drafts/Dialectic_Presentation_09.03.26_A_PLUS_DRAFT.pptx" \
  "drafts/Dialectic_Presentation_09.04.26_A_PLUS_REFINED.pptx"
```

Expected: two different hashes, confirming the existing A+ file remains a separate artifact.

- [ ] **Step 3: Open both versions**

Open the existing A+ draft and the refined deck for side-by-side review.

- [ ] **Step 4: Report completion**

Report:

```text
final file path
34-slide verification result
factual-review result
visual-QA result
claim-ledger path
change-log path
distribution status: not emailed
```

