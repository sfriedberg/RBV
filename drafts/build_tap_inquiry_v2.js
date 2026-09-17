const pptxgen = require("pptxgenjs");
const path = require("path");

const OUT = path.join(
  __dirname,
  "Dialectic_TAP_Inquiry_CTCL_091426.pptx"
);

const C = {
  deep: "0B3D3A",
  teal: "007D73",
  tealDark: "0F4C48",
  navy: "1F4E79",
  dark: "1F2933",
  mid: "4D5B66",
  mute: "6B7780",
  line: "D5DDE1",
  light: "F1F5F6",
  pale: "E5F5F2",
  white: "FFFFFF",
  cream: "F7F4EE",
  red: "8B3A3A",
};

const W = 13.333;
const H = 7.5;

function rail(slide, height) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 0.12, h: height == null ? H : height,
    fill: { color: C.teal }, line: { color: C.teal },
  });
}

function footer(slide, page, note) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 7.08, w: W, h: 0.42,
    fill: { color: C.light }, line: { color: C.light },
  });
  slide.addText(note, {
    x: 0.5, y: 7.08, w: 10.4, h: 0.42,
    fontFace: "Calibri", fontSize: 11, color: C.mid, italic: true,
    margin: 0, valign: "middle",
  });
  slide.addText(`${page}  /  12`, {
    x: 11.3, y: 7.08, w: 1.5, h: 0.42,
    fontFace: "Calibri", fontSize: 11, color: C.mid, align: "right",
    margin: 0, valign: "middle",
  });
}

function headerBar(slide, title) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: W, h: 0.92,
    fill: { color: C.deep }, line: { color: C.deep },
  });
  rail(slide, 7.08);
  slide.addText(title, {
    x: 0.5, y: 0.16, w: 12.3, h: 0.62,
    fontFace: "Calibri", fontSize: 24, bold: true, color: C.white,
    margin: 0, valign: "middle",
  });
}

const pres = new pptxgen();
pres.defineLayout({ name: "TAP_WIDE", width: W, height: H });
pres.layout = "TAP_WIDE";
pres.author = "Dialectic Therapeutics";
pres.title = "DT2216 — TAP Inquiry — CTCL Phase 2";
pres.subject = "Blood Cancer United Therapy Acceleration Program";
pres.company = "Dialectic Therapeutics, Inc.";

// ---------------------------------------------------------------------------
// 1. Cover
// ---------------------------------------------------------------------------
{
  const s = pres.addSlide();
  s.background = { color: C.deep };
  rail(s);
  s.addText("NON-CONFIDENTIAL  ·  THERAPY ACCELERATION PROGRAM INQUIRY", {
    x: 0.55, y: 0.42, w: 12.2, h: 0.28,
    fontFace: "Calibri", fontSize: 12, bold: true, color: C.teal, margin: 0, charSpacing: 0.8,
  });
  s.addText("DT2216 for cutaneous T-cell lymphoma", {
    x: 0.55, y: 1.05, w: 12.2, h: 1.05,
    fontFace: "Calibri", fontSize: 36, bold: true, color: C.white, margin: 0,
  });
  s.addText(
    "A first blood-cancer Phase 2, built on a completed solid-tumor dose-finding study, FDA orphan and Fast Track designations in T-cell lymphoma, and published single-agent activity in CTCL and T-ALL models.",
    {
      x: 0.55, y: 2.25, w: 11.4, h: 1.05,
      fontFace: "Calibri", fontSize: 16, color: "C9E8E4", margin: 0,
    }
  );

  const cards = [
    ["0.40 mg/kg IV BIW", "Phase 1a recommended dose\nSolid tumors only"],
    ["Orphan + Fast Track", "T-cell lymphoma / PTCL & CTCL\nDesignations, not human CTCL data"],
    ["2027 initiation", "MDA trial-design discussions\nIyer and Akkad"],
  ];
  cards.forEach((card, i) => {
    const x = 0.55 + i * 4.15;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: 3.55, w: 3.95, h: 2.05,
      fill: { color: C.tealDark }, line: { color: C.teal },
    });
    s.addText(card[0], {
      x: x + 0.2, y: 3.68, w: 3.55, h: 0.7,
      fontFace: "Calibri", fontSize: 18, bold: true, color: C.white, margin: 0,
    });
    s.addText(card[1], {
      x: x + 0.2, y: 4.40, w: 3.55, h: 1.0,
      fontFace: "Calibri", fontSize: 13, color: "C9E8E4", margin: 0,
    });
  });

  s.addText("Dialectic Therapeutics, Inc.  ·  Dallas  ·  September 2026  ·  Contact: Joshua Sills, COO  ·  sills@dtsciences.com", {
    x: 0.55, y: 6.78, w: 12.2, h: 0.28,
    fontFace: "Calibri", fontSize: 12, color: "9BC4C0", margin: 0,
  });
  s.addNotes(
    "Revised TAP scope: CTCL Phase 2 only. Do not attach the confidential ovarian investor deck. Dollar ask still a board choice (strategic $2–10M vs opportunistic ~$500k). Josh 1 Sep: frame as direct-to-Phase 2 single agent; 1-pager still says plus dexamethasone — lock before send."
  );
}

// ---------------------------------------------------------------------------
// 2. Scope
// ---------------------------------------------------------------------------
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  headerBar(s, "The TAP ask is the first DT2216 cohort in CTCL");
  footer(s, 2, "Aligned to Dialectic TAP Initial Inquiry Form, 1 September 2026.");

  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 1.18, w: 7.55, h: 5.62,
    fill: { color: C.light }, line: { color: C.line },
  });
  s.addText("In scope", {
    x: 0.72, y: 1.34, w: 7.1, h: 0.36,
    fontFace: "Calibri", fontSize: 16, bold: true, color: C.teal, margin: 0,
  });
  s.addText([
    { text: "Lead indication: relapsed/refractory CTCL, after approved agents.", options: { bullet: true, breakLine: true } },
    { text: "Asset: DT2216, a VHL-based BCL-XL PROTAC from the APTaD® platform.", options: { bullet: true, breakLine: true } },
    { text: "Starting point: Phase 1a RP2D of 0.40 mg/kg IV twice weekly.", options: { bullet: true, breakLine: true } },
    { text: "Site path: trial-design discussions with MD Anderson (Drs. Iyer and Akkad).", options: { bullet: true, breakLine: true } },
    { text: "Clock: initiation targeted for 2027, after protocol lock.", options: { bullet: true, breakLine: true } },
    { text: "Why TAP: fund the first heme cohort, not another solid-tumor monotherapy study.", options: { bullet: true } },
  ], {
    x: 0.72, y: 1.82, w: 7.1, h: 4.7,
    fontFace: "Calibri", fontSize: 15, color: C.dark, margin: 0, valign: "top",
  });

  s.addShape(pres.shapes.RECTANGLE, {
    x: 8.25, y: 1.18, w: 4.58, h: 5.62,
    fill: { color: C.pale }, line: { color: C.teal },
  });
  s.addText("Out of scope for this inquiry", {
    x: 8.47, y: 1.34, w: 4.16, h: 0.55,
    fontFace: "Calibri", fontSize: 16, bold: true, color: C.deep, margin: 0,
  });
  s.addText([
    { text: "Platinum-resistant ovarian cancer (NCT06964009)", options: { bullet: true, breakLine: true } },
    { text: "COG / PEP-CTN solid-tumor and FLC study (NCT06620302)", options: { bullet: true, breakLine: true } },
    { text: "DT5321 dual degrader (next heme asset)", options: { bullet: true, breakLine: true } },
    { text: "Investigator-initiated myeloid expansion (MF, post-MPN AML)", options: { bullet: true, breakLine: true } },
    { text: "Confidential unpublished combination figures", options: { bullet: true } },
  ], {
    x: 8.47, y: 2.05, w: 4.16, h: 4.5,
    fontFace: "Calibri", fontSize: 14, color: C.dark, margin: 0,
  });
}

// ---------------------------------------------------------------------------
// 3. Mechanism
// ---------------------------------------------------------------------------
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  headerBar(s, "BCL-XL is validated. Continuous inhibition was not doseable.");
  footer(s, 3, "Khan et al., Nat Med 2019; company Fast Track PR, 5 April 2022; TAP 1-pager §1.");

  const blocks = [
    ["01", "The target", "BCL-XL is the most commonly overexpressed anti-apoptotic protein in human cancer. Many T-cell lymphomas re-express it after normal mature T cells have dropped it."],
    ["02", "Why inhibitors stalled", "Navitoclax, AZD0466, and pelcitoclax ran into on-target thrombocytopenia. Platelets depend on BCL-XL. Continuous inhibition could not be dosed as a heme drug."],
    ["03", "What DT2216 changes", "DT2216 recruits VHL E3 ligase to degrade BCL-XL in tumor cells. Platelets express very little VHL, so they are relatively spared. The target becomes usable."],
    ["04", "What this is not", "Not a claim that platelets are untouched. Phase 1a still saw transient thrombocytopenia. Not a claim that CTCL patients have been treated."],
  ];
  blocks.forEach((b, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.5 + col * 6.4;
    const y = 1.18 + row * 2.85;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 6.2, h: 2.68,
      fill: { color: i === 3 ? C.cream : C.light }, line: { color: C.line },
    });
    s.addText(b[0], {
      x: x + 0.22, y: y + 0.18, w: 1.2, h: 0.4,
      fontFace: "Calibri", fontSize: 18, bold: true, color: C.teal, margin: 0,
    });
    s.addText(b[1], {
      x: x + 0.22, y: y + 0.62, w: 5.76, h: 0.4,
      fontFace: "Calibri", fontSize: 18, bold: true, color: C.deep, margin: 0,
    });
    s.addText(b[2], {
      x: x + 0.22, y: y + 1.10, w: 5.76, h: 1.35,
      fontFace: "Calibri", fontSize: 14, color: C.dark, margin: 0,
    });
  });
}

// ---------------------------------------------------------------------------
// 4. Preclinical
// ---------------------------------------------------------------------------
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  headerBar(s, "Published heme models show single-agent activity versus navitoclax");
  footer(s, 4, "Khan et al., Nat Med 2019; He et al., J Hematol Oncol 2020. Preclinical only.");

  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 1.18, w: 6.2, h: 4.55,
    fill: { color: C.white }, line: { color: C.line },
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 1.18, w: 6.2, h: 0.1,
    fill: { color: C.teal }, line: { color: C.teal },
  });
  s.addText("CTCL  ·  He 2020", {
    x: 0.72, y: 1.42, w: 5.76, h: 0.38,
    fontFace: "Calibri", fontSize: 18, bold: true, color: C.navy, margin: 0,
  });
  s.addText([
    { text: "MyLa cutaneous T-cell lymphoma xenografts.", options: { bullet: true, breakLine: true } },
    { text: "DT2216 monotherapy inhibited growth and outperformed navitoclax in the reported model.", options: { bullet: true, breakLine: true } },
    { text: "BCL-XL was degraded. The paper did not show BCL-2 or MCL-1 compensation.", options: { bullet: true, breakLine: true } },
    { text: "Less platelet toxicity than navitoclax, with a survival benefit in the model.", options: { bullet: true } },
  ], {
    x: 0.72, y: 1.92, w: 5.76, h: 3.5,
    fontFace: "Calibri", fontSize: 15, color: C.dark, margin: 0,
  });

  s.addShape(pres.shapes.RECTANGLE, {
    x: 6.9, y: 1.18, w: 5.93, h: 4.55,
    fill: { color: C.white }, line: { color: C.line },
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 6.9, y: 1.18, w: 5.93, h: 0.1,
    fill: { color: C.navy }, line: { color: C.navy },
  });
  s.addText("T-ALL  ·  Khan 2019", {
    x: 7.12, y: 1.42, w: 5.5, h: 0.38,
    fontFace: "Calibri", fontSize: 18, bold: true, color: C.navy, margin: 0,
  });
  s.addText([
    { text: "MOLT-4 T-ALL. Foundational DT2216 paper.", options: { bullet: true, breakLine: true } },
    { text: "Weekly DT2216 produced near-complete growth inhibition versus daily navitoclax in the reported experiment.", options: { bullet: true, breakLine: true } },
    { text: "Same pattern: BCL-XL degradation, no compensatory BCL-2 / MCL-1, reduced platelet liability versus continuous inhibition.", options: { bullet: true, breakLine: true } },
    { text: "Supports intermittent degradation as the heme dosing idea later used in Phase 1a (BIW).", options: { bullet: true } },
  ], {
    x: 7.12, y: 1.92, w: 5.5, h: 3.5,
    fontFace: "Calibri", fontSize: 15, color: C.dark, margin: 0,
  });

  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 5.88, w: 12.33, h: 1.1,
    fill: { color: C.pale }, line: { color: C.teal },
  });
  s.addText("These papers are why Fast Track exists. They are not a substitute for a treated CTCL patient.", {
    x: 0.72, y: 6.05, w: 11.9, h: 0.76,
    fontFace: "Calibri", fontSize: 16, bold: true, color: C.deep, margin: 0, valign: "middle",
  });
}

// ---------------------------------------------------------------------------
// 5. Phase 1
// ---------------------------------------------------------------------------
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  headerBar(s, "Phase 1a set a human dose. It did not enroll CTCL.");
  footer(s, 5, "Mahadevan et al., J Hematol Oncol 2025; NCT04886622. n = 20 advanced solid tumors.");

  const metrics = [
    ["20", "Patients\nSolid tumors only"],
    ["0.40", "mg/kg IV BIW\nRecommended Phase 2 dose"],
    ["1", "DLT — grade 4 platelets\nResolved in under 48 hours"],
    ["4 / 20", "Best RECIST\nStable disease. No responses."],
  ];
  metrics.forEach((m, i) => {
    const x = 0.5 + i * 3.2;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: 1.18, w: 3.05, h: 1.95,
      fill: { color: C.pale }, line: { color: C.teal },
    });
    s.addText(m[0], {
      x, y: 1.28, w: 3.05, h: 0.72,
      fontFace: "Calibri", fontSize: 28, bold: true, color: C.deep, align: "center", margin: 0,
    });
    s.addText(m[1], {
      x: x + 0.12, y: 2.05, w: 2.81, h: 0.9,
      fontFace: "Calibri", fontSize: 13, color: C.mid, align: "center", margin: 0,
    });
  });

  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 3.32, w: 12.33, h: 3.52,
    fill: { color: C.white }, line: { color: C.line },
  });
  s.addText([
    { text: "BCL-XL in peripheral leukocytes fell rapidly at 0.40 mg/kg and stayed down. Human tumor BCL-XL degradation has not been shown.", options: { bullet: true, breakLine: true } },
    { text: "Thrombocytopenia was transient and manageable. The paper reported recovery above 50k in four days and above 75k in one week. No bleeding events or treatment-emergent deaths.", options: { bullet: true, breakLine: true } },
    { text: "The 1-pager states there were no related SAEs, discontinuations, or deaths.", options: { bullet: true, breakLine: true } },
    { text: "Authors: monotherapy lacked single-agent activity in these solid tumors. That is why the TAP indication is a BCL-XL-dependent lymphoid population, not a repeat of solid-tumor monotherapy.", options: { bullet: true } },
  ], {
    x: 0.72, y: 3.48, w: 11.9, h: 3.2,
    fontFace: "Calibri", fontSize: 15, color: C.dark, margin: 0,
  });
}

// ---------------------------------------------------------------------------
// 6. Regulatory
// ---------------------------------------------------------------------------
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  headerBar(s, "Designations and prior Texas funding are in hand. A CTCL dataset is not.");
  footer(s, 6, "Orphan PR; Fast Track PR, 5 April 2022; CPRIT DP210005; TAP 1-pager §2.");

  const rows = [
    ["Orphan drug", "DT2216 for T-cell lymphoma", "Company designation. Not efficacy."],
    ["Fast Track", "Adult relapsed/refractory PTCL and CTCL", "Expedites FDA interaction. Not approval."],
    ["IND / Phase 1a", "NCT04886622 completed", "Solid-tumor dose escalation. RP2D set."],
    ["CPRIT TXCO", "DP210005  ·  $14.45M contracted", "Record includes T-cell lymphoma and SCLC."],
    ["MDA path", "Iyer and Akkad — design discussions", "CTCL Phase 2 targeted for 2027. Not a locked protocol."],
  ];
  rows.forEach((r, i) => {
    const y = 1.16 + i * 1.14;
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0.5, y, w: 12.33, h: 1.04,
      fill: { color: C.light }, line: { color: C.line },
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0.5, y, w: 0.1, h: 1.04,
      fill: { color: C.teal }, line: { color: C.teal },
    });
    s.addText(r[0], {
      x: 0.82, y, w: 2.5, h: 1.04,
      fontFace: "Calibri", fontSize: 16, bold: true, color: C.deep, margin: 0, valign: "middle",
    });
    s.addText(r[1], {
      x: 3.4, y, w: 4.7, h: 1.04,
      fontFace: "Calibri", fontSize: 15, color: C.dark, margin: 0, valign: "middle",
    });
    s.addText(r[2], {
      x: 8.2, y, w: 4.4, h: 1.04,
      fontFace: "Calibri", fontSize: 14, color: C.mid, margin: 0, valign: "middle",
    });
  });
}

// ---------------------------------------------------------------------------
// 7. Proposed study
// ---------------------------------------------------------------------------
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  headerBar(s, "Proposed CTCL Phase 2: use the dose already in hand");
  footer(s, 7, "Working design from the 1 September 2026 inquiry form. Not a protocol. Not submitted.");

  const rows = [
    ["Population", "Relapsed/refractory CTCL after approved targeted therapy. Not front-line."],
    ["Regimen", "DT2216 at 0.40 mg/kg IV twice weekly. Steroid combination to be locked with MDA."],
    ["Site / PI", "MD Anderson. Trial-design discussions with Drs. Iyer and Akkad."],
    ["Purpose", "First human CTCL dataset: safety in a heme population, activity by mSWAT, go/no-go on expansion."],
    ["Clock", "Protocol lock, then initiation targeted for 2027. TAP diligence is typically 3–6 months to committee."],
    ["What TAP funds", "The first heme cohort — drug, CRO, site, and the work to open it. Not PROC. Not COG."],
  ];
  rows.forEach((r, i) => {
    const y = 1.16 + i * 0.95;
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0.5, y, w: 12.33, h: 0.86,
      fill: { color: i % 2 === 0 ? C.light : C.white }, line: { color: C.line },
    });
    s.addText(r[0], {
      x: 0.7, y, w: 2.4, h: 0.86,
      fontFace: "Calibri", fontSize: 14, bold: true, color: C.deep, margin: 0, valign: "middle",
    });
    s.addText(r[1], {
      x: 3.2, y, w: 9.4, h: 0.86,
      fontFace: "Calibri", fontSize: 14, color: C.dark, margin: 0, valign: "middle",
    });
  });
  s.addNotes(
    "Josh 1 Sep: PROC/FLC are Phase 1b (and 1b/2); CTCL should be framed as direct-to-Phase 2 single agent. 1-pager still says plus dexamethasone. n, IND amendment vs existing IND, and $ ask remain open."
  );
}

// ---------------------------------------------------------------------------
// 8. Other trials
// ---------------------------------------------------------------------------
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  headerBar(s, "Two solid-tumor trials are visible. They are not this ask.");
  footer(s, 8, "NCT06964009; NCT06620302. Confidential ovarian manuscript is omitted on purpose.");

  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 1.18, w: 6.2, h: 5.62,
    fill: { color: C.white }, line: { color: C.line },
  });
  s.addText("What exists", {
    x: 0.72, y: 1.36, w: 5.76, h: 0.36,
    fontFace: "Calibri", fontSize: 16, bold: true, color: C.red, margin: 0,
  });
  s.addText([
    { text: "PROC: DT2216 plus weekly paclitaxel at DFCI / BIDMC (NCT06964009). Phase 1b/2. First efficacy expected 2027.", options: { bullet: true, breakLine: true } },
    { text: "COG / PEP-CTN: DT2216 plus irinotecan in relapsed/refractory solid tumors and fibrolamellar carcinoma (NCT06620302).", options: { bullet: true, breakLine: true } },
    { text: "The inquiry form treats these as the studies that extend the RP2D and the drug-supply path hematology will use.", options: { bullet: true, breakLine: true } },
    { text: "If TAP diligence reaches ClinicalTrials.gov, both records will be there. We are not hiding them.", options: { bullet: true } },
  ], {
    x: 0.72, y: 1.86, w: 5.76, h: 4.75,
    fontFace: "Calibri", fontSize: 15, color: C.dark, margin: 0,
  });

  s.addShape(pres.shapes.RECTANGLE, {
    x: 6.9, y: 1.18, w: 5.93, h: 5.62,
    fill: { color: C.pale }, line: { color: C.teal },
  });
  s.addText("What TAP is asked to fund", {
    x: 7.12, y: 1.36, w: 5.5, h: 0.36,
    fontFace: "Calibri", fontSize: 16, bold: true, color: C.deep, margin: 0,
  });
  s.addText([
    { text: "The first CTCL Phase 2 cohort in a BCL-XL-dependent T-cell lymphoma population.", options: { bullet: true, breakLine: true } },
    { text: "A protocol that uses the published heme models, Fast Track, orphan designation, and the human dose already established.", options: { bullet: true, breakLine: true } },
    { text: "Myelofibrosis, post-MPN AML, and DT5321 remain follow-on heme options. They are not the check TAP is being asked to write.", options: { bullet: true } },
  ], {
    x: 7.12, y: 1.86, w: 5.5, h: 4.75,
    fontFace: "Calibri", fontSize: 15, color: C.dark, margin: 0,
  });
}

// ---------------------------------------------------------------------------
// 9. Plan / supply
// ---------------------------------------------------------------------------
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  headerBar(s, "Dose, supply, and a 2027 CTCL start are the operating facts");
  footer(s, 9, "TAP 1-pager §4. Company-reported supply language. Not a CMC package.");

  const steps = [
    ["Now", "Phase 1a complete. RP2D 0.40 mg/kg IV BIW. Two solid-tumor combination trials on the register."],
    ["Supply", "GMP drug substance on hand through Phase 2. Lyophilized drug product developed, with FDA alignment."],
    ["2026–27", "Lock the CTCL protocol with MD Anderson. TAP diligence in parallel (typically 3–6 months to committee)."],
    ["2027", "Target CTCL Phase 2 initiation. First heme safety and activity read. Go/no-go on expansion."],
  ];
  steps.forEach((st, i) => {
    const y = 1.18 + i * 1.42;
    s.addShape(pres.shapes.OVAL, {
      x: 0.55, y: y + 0.28, w: 0.42, h: 0.42,
      fill: { color: C.teal }, line: { color: C.teal },
    });
    s.addText(String(i + 1), {
      x: 0.55, y: y + 0.28, w: 0.42, h: 0.42,
      fontFace: "Calibri", fontSize: 14, bold: true, color: C.white, align: "center", valign: "middle", margin: 0,
    });
    if (i < 3) {
      s.addShape(pres.shapes.RECTANGLE, {
        x: 0.73, y: y + 0.72, w: 0.06, h: 0.98,
        fill: { color: C.pale }, line: { color: C.pale },
      });
    }
    s.addText(st[0], {
      x: 1.2, y, w: 2.1, h: 1.28,
      fontFace: "Calibri", fontSize: 18, bold: true, color: C.deep, margin: 0, valign: "middle",
    });
    s.addText(st[1], {
      x: 3.4, y, w: 9.4, h: 1.28,
      fontFace: "Calibri", fontSize: 15, color: C.dark, margin: 0, valign: "middle",
    });
  });
}

// ---------------------------------------------------------------------------
// 10. Team
// ---------------------------------------------------------------------------
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  headerBar(s, "Texas company. Operators who already ran first-in-human.");
  footer(s, 10, "TAP 1-pager §5. TAP operating contact: Joshua Sills, COO.");

  const people = [
    ["John D. Harkey, Jr.", "Executive Chairman", "Co-founder and Executive Chairman of AveXis, acquired by Novartis for $8.7B."],
    ["Joshua Sills", "COO  ·  TAP contact", "Twenty years of biotech and technology operations. Also operates Cessation Therapeutics."],
    ["James Strauss, MD", "Chief Medical Officer", "Hematologist and medical oncologist, Texas Oncology. Phase 1–2 investigator, Mary Crowley."],
    ["Larry Tremaine, PhD", "Chief Scientific Officer", "Thirty-five years at Pfizer PDM. Led DT2216 preclinical development."],
    ["Stephen Friedberg", "Chief Financial Officer", "Business operations at Alphabet / Google. Principal investing and operating experience."],
    ["Zhou  ·  Zheng  ·  Hromas", "Scientific co-founders", "DT2216 inventors. Hromas chairs the board. SAB includes Joan Brugge and Jonathan Licht (LLS SCOR)."],
  ];
  people.forEach((p, i) => {
    const col = i % 3;
    const row = Math.floor(i / 3);
    const x = 0.5 + col * 4.2;
    const y = 1.18 + row * 2.88;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 4.05, h: 2.7,
      fill: { color: C.white }, line: { color: C.line },
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 4.05, h: 0.08,
      fill: { color: C.teal }, line: { color: C.teal },
    });
    s.addText(p[0], {
      x: x + 0.18, y: y + 0.28, w: 3.7, h: 0.5,
      fontFace: "Calibri", fontSize: 16, bold: true, color: C.deep, margin: 0,
    });
    s.addText(p[1], {
      x: x + 0.18, y: y + 0.82, w: 3.7, h: 0.36,
      fontFace: "Calibri", fontSize: 13, italic: true, color: C.navy, margin: 0,
    });
    s.addText(p[2], {
      x: x + 0.18, y: y + 1.28, w: 3.7, h: 1.2,
      fontFace: "Calibri", fontSize: 13, color: C.mid, margin: 0,
    });
  });
}

// ---------------------------------------------------------------------------
// 11. Landscape
// ---------------------------------------------------------------------------
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  headerBar(s, "The unmet need is after approved CTCL agents, not instead of them");
  footer(s, 11, "Landscape TAP already knows. Not a market model.");

  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 1.18, w: 6.2, h: 5.62,
    fill: { color: C.white }, line: { color: C.line },
  });
  s.addText("Already available", {
    x: 0.72, y: 1.36, w: 5.76, h: 0.36,
    fontFace: "Calibri", fontSize: 16, bold: true, color: C.navy, margin: 0,
  });
  s.addText([
    { text: "Mogamulizumab (CCR4) in CTCL.", options: { bullet: true, breakLine: true } },
    { text: "Brentuximab vedotin in CD30-expressing disease.", options: { bullet: true, breakLine: true } },
    { text: "Denileukin diftitox-cxdl (Lymphir) in relapsed/refractory CTCL.", options: { bullet: true, breakLine: true } },
    { text: "Skin-directed therapy, HDAC inhibitors, chemotherapy, and transplant in selected patients.", options: { bullet: true, breakLine: true } },
    { text: "A TAP reviewer will not accept “no options.” Response rates and durability are still the gap.", options: { bullet: true } },
  ], {
    x: 0.72, y: 1.86, w: 5.76, h: 4.75,
    fontFace: "Calibri", fontSize: 15, color: C.dark, margin: 0,
  });

  s.addShape(pres.shapes.RECTANGLE, {
    x: 6.9, y: 1.18, w: 5.93, h: 5.62,
    fill: { color: C.pale }, line: { color: C.teal },
  });
  s.addText("Where DT2216 would sit", {
    x: 7.12, y: 1.36, w: 5.5, h: 0.36,
    fontFace: "Calibri", fontSize: 16, bold: true, color: C.deep, margin: 0,
  });
  s.addText([
    { text: "Different mechanism: BCL-XL degradation, not CCR4, CD30, or IL-2 receptor targeting.", options: { bullet: true, breakLine: true } },
    { text: "Natural first use: after those agents, or in patients who are not candidates for them.", options: { bullet: true, breakLine: true } },
    { text: "Platelet recovery between doses is the therapeutic-index argument versus navitoclax — still to be shown in a heme cohort.", options: { bullet: true, breakLine: true } },
    { text: "Do not position DT2216 as front-line CTCL therapy in this inquiry.", options: { bullet: true } },
  ], {
    x: 7.12, y: 1.86, w: 5.5, h: 4.75,
    fontFace: "Calibri", fontSize: 15, color: C.dark, margin: 0,
  });
}

// ---------------------------------------------------------------------------
// 12. Close
// ---------------------------------------------------------------------------
{
  const s = pres.addSlide();
  s.background = { color: C.deep };
  rail(s);
  s.addText("WHAT TAP GETS", {
    x: 0.55, y: 0.42, w: 12.2, h: 0.28,
    fontFace: "Calibri", fontSize: 13, bold: true, color: "8ED8D0", margin: 0, charSpacing: 1,
  });
  s.addText("A CTCL partnership, not a platform tour", {
    x: 0.55, y: 0.78, w: 12.2, h: 0.62,
    fontFace: "Calibri", fontSize: 28, bold: true, color: C.white, margin: 0,
  });

  const pts = [
    ["A first heme Phase 2", "CTCL at MD Anderson, Fast Track and orphan already granted, RP2D 0.40 mg/kg IV BIW, GMP drug substance through Phase 2."],
    ["A defined use of proceeds", "Open and run the first CTCL cohort. PROC and COG stay on their own tickets."],
    ["What TAP already sells", "KOL network, trial-support credibility, and a signal other capital recognizes. We want that, not only the dollars."],
    ["Milestones, not slides", "Protocol lock. First patient. Heme safety and activity. A go/no-go on expansion."],
  ];
  pts.forEach((p, i) => {
    const y = 1.58 + i * 1.18;
    s.addText(p[0], {
      x: 0.55, y, w: 12.2, h: 0.34,
      fontFace: "Calibri", fontSize: 16, bold: true, color: C.white, margin: 0,
    });
    s.addText(p[1], {
      x: 0.55, y: y + 0.34, w: 12.2, h: 0.7,
      fontFace: "Calibri", fontSize: 15, color: "C9E8E4", margin: 0,
    });
  });
  s.addText("Dialectic Therapeutics  ·  1220 N. Stemmons Freeway, Suite 100, Dallas, TX 75234  ·  dtsciences.com", {
    x: 0.55, y: 6.72, w: 10.2, h: 0.28,
    fontFace: "Calibri", fontSize: 12, color: "9BC4C0", margin: 0,
  });
  s.addText("12  /  12", {
    x: 11.3, y: 6.72, w: 1.5, h: 0.28,
    fontFace: "Calibri", fontSize: 12, color: "9BC4C0", align: "right", margin: 0,
  });
  s.addNotes(
    "Board still picks strategic ($2–10M) vs opportunistic (~$500k). Do not send until Josh locks regimen (single-agent vs +dex), n/IND, and one study-conduct sentence or omit."
  );
}

pres.writeFile({ fileName: OUT }).then(() => {
  console.log(OUT);
});
