# Dialectic A+ Deck Implementation Plan

**Goal:** Save the forwarded company deck unchanged as an original comparison file and create a separate investor-grade version centered on DT2216 plus weekly paclitaxel.

**Architecture:** Build from vDRAFT5 so the prior factual corrections remain in place. Replace the scientific spine with six new slides based on the July 2026 submitted manuscript, then simplify the executive summary and clinical translation slides. Preserve the Dialectic master and all source files.

**Tech Stack:** Python 3, python-pptx, Pillow, Poppler, LibreOffice.

## Global Constraints

- Confidential and CDA-only.
- No cloud-model review of scientific materials.
- No AI-style prose, formatting or labels.
- Current proposed therapy is DT2216 plus weekly paclitaxel.
- ADC data are payload-only and future optionality.
- No invented financing, clinical efficacy or commercial claims.
- Original, vDRAFT4 and vDRAFT5 remain unchanged.
- No email or external distribution.

### Task 1: Freeze the original and verify sources

**Files:**
- Create: `drafts/Dialectic_Presentation_09.03.26_ORIGINAL_AS_RECEIVED.pptx`
- Create: `sources/kris-forward-2026-09-03/SOURCE_MANIFEST.md`

- [ ] Download the 3 September deck attachment from its Rockbrook message.
- [ ] Compare its SHA-256 hash with the Dropbox `vDRAFT.pptx`.
- [ ] Save a byte-identical copy as `ORIGINAL_AS_RECEIVED.pptx`.
- [ ] Record the three controlling source files and hashes.

Verification:

```bash
shasum -a 256 \
  "drafts/Dialectic_Presentation_09.03.26_ORIGINAL_AS_RECEIVED.pptx" \
  "/Users/stephenfriedberg/Library/CloudStorage/Dropbox/Dialectic Therapeutics/Company Presentations/Dialectic Presentation_09.03.26_vDRAFT.pptx"
```

Expected: identical hashes.

### Task 2: Prepare legible manuscript panels

**Files:**
- Create: `sources/kris-forward-2026-09-03/aplus-assets/figure3F-paclitaxel-breadth.png`
- Create: `sources/kris-forward-2026-09-03/aplus-assets/figure4E-specificity.png`
- Create: `sources/kris-forward-2026-09-03/aplus-assets/figure4F-adc-payloads.png`
- Create: `sources/kris-forward-2026-09-03/aplus-assets/figure6D-pdx-breadth.png`
- Create: `sources/kris-forward-2026-09-03/aplus-assets/figure8-FH-flank.png`
- Create: `sources/kris-forward-2026-09-03/aplus-assets/figure8-PS-intraperitoneal.png`
- Create: `drafts/prepare_aplus_assets.py`

- [ ] Render manuscript figure pages 43, 49 and 53 at 300 dpi.
- [ ] Crop only the cited panels, leaving panel letters, axes, legends and treatment labels visible.
- [ ] Render the high-resolution Figure 4 attachment at 360 dpi and crop panels E and F.
- [ ] Create a contact sheet and inspect every crop before deck assembly.

Verification:

```bash
python3 drafts/prepare_aplus_assets.py
```

Expected: six non-empty PNG panel files plus a contact sheet.

### Task 3: Build the A+ presentation

**Files:**
- Create: `drafts/build_aplus_deck.py`
- Create: `drafts/Dialectic_Presentation_09.03.26_A_PLUS_DRAFT.pptx`

- [ ] Open vDRAFT5 and preserve slides 1–16 and 23–34.
- [ ] Replace slides 17–22 with the approved six-slide sequence.
- [ ] Rewrite slide 4 as a concise investment summary using only sourced facts.
- [ ] Simplify slides 26–28 so Phase 1a, the mouse-to-human bridge and the ovarian trial are readable.
- [ ] Rewrite slide 31 as conventional clinical-development questions.
- [ ] Correct visible slide numbers and obsolete June 2025 citations.
- [ ] Save the new presentation without changing vDRAFT5.

Verification:

```bash
python3 drafts/build_aplus_deck.py
python3 -m markitdown "drafts/Dialectic_Presentation_09.03.26_A_PLUS_DRAFT.pptx"
```

Expected: 34 slides, correct order, no old Figure 7 description, no “DT2216 plus any agent” language and no claim that intact Elahere was tested.

### Task 4: Factual and local-model review

- [ ] Extract every quantitative statement on revised slides.
- [ ] Check the claims against the July manuscript and Mahadevan Phase 1 publication.
- [ ] Run a private local DeepSeek critique for unsupported claims and narrative gaps.
- [ ] Correct all identified factual issues.

Required checks:

```text
Figure 4E n=3
Figure 4F DM4/MMAE n=3; MMAF n=1
Figure 6D 7/8 PDX models; representative of n=2 biological replicates
Figure 8 flank treatment stopped day 138; no regrowth during 100 additional days
Figure 8 disseminated model median survival +35 days versus paclitaxel
Figure 3 55 cell lines; 12 tumor types; synergy at one or more tested doses
```

### Task 5: Visual QA and delivery

**Files:**
- Create: `drafts/qa-aplus/`
- Create: Dropbox `Dialectic Presentation_09.03.26_ORIGINAL_AS_RECEIVED.pptx`
- Create: Dropbox `Dialectic Presentation_09.03.26_A_PLUS_DRAFT.pptx`

- [ ] Render all 34 slides through LibreOffice.
- [ ] Inspect the full contact sheet and revised slides at full resolution.
- [ ] Correct overflow, poor crop resolution, illegible labels, inconsistent title treatment and footer collisions.
- [ ] Render revised slides again after the first correction pass.
- [ ] Copy the original and upgraded files to the Company Presentations Dropbox folder.
- [ ] Verify the local and Dropbox hashes match.
- [ ] Open both files for Stephen.

Verification:

```bash
pdfinfo "drafts/qa-aplus/Dialectic_Presentation_09.03.26_A_PLUS_DRAFT.pdf"
shasum -a 256 \
  "drafts/Dialectic_Presentation_09.03.26_A_PLUS_DRAFT.pptx" \
  "/Users/stephenfriedberg/Library/CloudStorage/Dropbox/Dialectic Therapeutics/Company Presentations/Dialectic Presentation_09.03.26_A_PLUS_DRAFT.pptx"
```

Expected: 34 rendered pages and identical local/Dropbox hashes.
