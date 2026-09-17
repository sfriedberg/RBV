"""Verified and attributed content for the refined Dialectic presentation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SlideSpec:
    number: int
    title: str
    subtitle: str = ""
    body: tuple[str, ...] = ()
    source: str = ""
    status_note: str = ""


SLIDE_TITLES = {
    1: "Creating Innovative Technologies to Treat Cancer",
    2: "Disclaimer",
    3: "Presentation Overview",
    4: "DT2216 plus weekly paclitaxel is the lead value-creation program",
    5: "A different binding strategy made active RAS addressable",
    6: "Leadership and scientific advisors",
    7: "DT2216 is the clinical priority within a broader degrader pipeline",
    8: "BCL-XL is biologically validated, but direct inhibition is limited by platelet toxicity",
    9: "DT2216 uses VHL-mediated degradation to target BCL-XL selectively",
    10: "Tumor BCL-XL degradation outlasted the effect measured in circulating white blood cells",
    11: "Tissue retention can sustain pharmacology after plasma concentrations decline",
    12: "Intermittent degradation differs from continuous BCL-XL inhibition",
    13: "Platelet recovery supports intermittent BCL-XL degradation",
    14: "Preclinical tissue exposure supports intermittent DT2216 dosing",
    15: "Preclinical evidence spans multiple models, with the strongest current case in ovarian cancer",
    16: "The development portfolio combines one active lead thesis with additional options",
    17: "DT2216 plus paclitaxel targets complementary survival pathways",
    18: "Paclitaxel moves surviving HGSOC cells onto BCL-XL",
    19: "Seven of eight patient-derived ovarian models showed combination synergy ex vivo",
    20: "DT2216 plus paclitaxel produced durable control in two DF83 PDX settings",
    21: "DT2216 plus paclitaxel showed in-vitro synergy across 55 cell lines and 12 tumor types",
    22: "DT2216 increased apoptosis with three microtubule ADC payloads in OVCAR8",
    23: "DT2216 plus irinotecan produced regression in fibrolamellar carcinoma PDX models",
    24: "DT2216 showed preclinical CTCL activity with less platelet toxicity than navitoclax",
    25: "DT2216 plus fulvestrant is an unpublished ER-positive breast-cancer option",
    26: "Phase 1 established a human dose and systemic target engagement",
    27: "Phase 1 established systemic pharmacodynamics; Phase 1b will test tumor pharmacodynamics",
    28: "The registered ovarian study is a recruiting Phase 1b trial",
    29: "The FLC Phase 1/2 study is suspended",
    30: "The ovarian Phase 1b readout is the primary near-term value inflection",
    31: "Key questions for the ovarian program",
    32: "Licensed patent rights cover DT2216, DT5321 and related BCL-family degraders",
    33: "Academic collaborations broaden the evidence base and development options",
    34: "Selected publications supporting the DT2216 platform",
}


SLIDES = {
    1: SlideSpec(
        1,
        SLIDE_TITLES[1],
        "Company Presentation | September 4, 2026",
        status_note="CONFIDENTIAL",
    ),
    2: SlideSpec(
        2,
        SLIDE_TITLES[2],
        body=("Preserve the company-provided legal disclaimer.",),
        source="Company information.",
    ),
    3: SlideSpec(
        3,
        SLIDE_TITLES[3],
        body=(
            "Investment proposition",
            "Why BCL-XL and why degradation",
            "Why paclitaxel in ovarian cancer",
            "Preclinical evidence",
            "Human evidence and active trials",
            "Key risks, intellectual property and supporting work",
        ),
    ),
    4: SlideSpec(
        4,
        SLIDE_TITLES[4],
        "A mechanism-matched ovarian combination is now being tested in patients.",
        body=(
            "Phase 1 established 0.40 mg/kg IV twice weekly as the recommended Phase 2 dose and showed rapid, sustained BCL-XL degradation in peripheral leukocytes.",
            "Seven of eight patient-derived ovarian models showed ex-vivo synergy. The combination produced durable control in flank and disseminated DF83 PDX models.",
            "The registered ovarian Phase 1b study is recruiting. Human combination efficacy has not been reported.",
        ),
        source="Sources: Mahadevan et al., J Hematol Oncol 2025; Qin et al., submitted manuscript, July 2026; NCT06964009.",
        status_note="Submitted-manuscript data are confidential and not peer reviewed.",
    ),
    5: SlideSpec(
        5,
        SLIDE_TITLES[5],
        "The RAS precedent illustrates the potential value of changing how a difficult target is engaged.",
        body=(
            "Daraxonrasib uses tri-complex pharmacology to inhibit active RAS signaling across multiple variants.",
            "In the Phase 3 RASolute 302 trial, median overall survival was 13.2 months with daraxonrasib and 6.7 months with chemotherapy in previously treated metastatic PDAC.",
            "DT2216 addresses a different target, disease and development risk. The comparison is about molecular design, not a prediction of clinical success.",
        ),
        source="Source: Revolution Medicines releases dated April 13 and May 31, 2026; RASolute 302, NCT06625320.",
    ),
    6: SlideSpec(
        6,
        SLIDE_TITLES[6],
        body=(
            "Board | John Harkey, Jr., JD, MBA; Robert Hromas, MD; Daohong Zhou, MD; David Hitt, JD, MTax, observer",
            "Management | John Harkey, Jr.; Joshua Sills; Stephen Friedberg; James Strauss, MD; Larry Tremaine, PhD; Guangrong Zheng, PhD; Eric Rasmussen",
            "Scientific advisors | Jonathan Licht, MD; Joan Brugge, PhD",
        ),
        source="Source: Company information as of September 3, 2026.",
        status_note="David Genecov, MD, co-founder, deceased.",
    ),
    7: SlideSpec(
        7,
        SLIDE_TITLES[7],
        body=(
            "Ovarian cancer | DT2216 plus weekly paclitaxel | Phase 1b recruiting | NCT06964009",
            "Fibrolamellar carcinoma | DT2216 plus irinotecan | Phase 1/2 suspended for unacceptable toxicity | NCT06620302",
            "CTCL and ER-positive breast cancer | Proposed DT2216 programs | Company plans",
            "DT5321 and third-generation degraders | Preclinical research | Company plans",
        ),
        source="Sources: ClinicalTrials.gov, accessed September 4, 2026; company information for proposed programs.",
    ),
    8: SlideSpec(
        8,
        SLIDE_TITLES[8],
        body=(
            "BCL-XL is an anti-apoptotic protein that supports survival in multiple tumor contexts and contributes to treatment resistance.",
            "Platelets also depend on BCL-XL. Direct inhibition can therefore cause on-target, dose-limiting thrombocytopenia.",
            "DT2216 was designed to use the cell's degradation machinery to improve the separation between tumor pharmacology and platelet exposure.",
        ),
        source="Sources: Khan et al., Nat Med 2019; Mahadevan et al., J Hematol Oncol 2025.",
    ),
    9: SlideSpec(
        9,
        SLIDE_TITLES[9],
        body=(
            "One end of DT2216 binds BCL-XL; the other recruits the VHL E3 ligase.",
            "The ternary complex promotes ubiquitination and proteasomal degradation of BCL-XL.",
            "Preclinical proteomic and complex-formation experiments support the intended degradation specificity.",
        ),
        source="Source: Khan et al., Nat Med 2019.",
        status_note="Preclinical mechanism; clinical safety is addressed separately.",
    ),
    10: SlideSpec(
        10,
        SLIDE_TITLES[10],
        "A MOLT4 xenograft experiment showed a longer pharmacodynamic effect in tumor than in white blood cells.",
        body=(
            "Dose: DT2216 15 mg/kg intraperitoneally.",
            "Circulating-cell and tumor measurements were made in the same experiment.",
            "The result supports a tissue-retention hypothesis; it does not establish human tumor exposure.",
        ),
        source="Source: Company preclinical data.",
    ),
    11: SlideSpec(
        11,
        SLIDE_TITLES[11],
        body=(
            "VHL-recruiting degraders can remain in tissues after plasma concentrations fall.",
            "Sustained intracellular exposure can extend target degradation beyond the period of measurable plasma drug.",
            "For DT2216, this remains a preclinical explanation for the observed PK/PD disconnect. Human tumor retention has not been shown.",
        ),
        source="Sources: Zhang et al., Commun Med 2024; company DT2216 preclinical data.",
    ),
    12: SlideSpec(
        12,
        SLIDE_TITLES[12],
        body=(
            "Navitoclax directly inhibits BCL-XL while circulating drug remains present, and platelet toxicity has limited dosing.",
            "DT2216 recruits VHL to degrade BCL-XL and showed no plasma accumulation with twice-weekly dosing in Phase 1.",
            "DT2216 reduced the preclinical platelet liability but did not eliminate it: thrombocytopenia occurred in 9 of 20 Phase 1 patients.",
        ),
        source="Sources: Khan et al., Nat Med 2019; Mahadevan et al., J Hematol Oncol 2025.",
    ),
    13: SlideSpec(
        13,
        SLIDE_TITLES[13],
        "Newly produced platelets are less primed and less dependent on BCL-XL; megakaryocytes have low VHL expression.",
        body=(
            "The biology supports platelet recovery between intermittent doses.",
            "Phase 1 nevertheless showed transient thrombocytopenia, including one dose-limiting grade 4 event.",
        ),
        source="Sources: Grozovsky, Fraser, Qin et al., Cell Death Dis 2026; Khan et al., Nat Med 2019; Mahadevan et al., 2025.",
    ),
    14: SlideSpec(
        14,
        SLIDE_TITLES[14],
        body=(
            "Company preclinical measurements showed greater and more persistent DT2216 exposure in tumor tissue than in plasma.",
            "Tumor BCL-XL degradation persisted after circulating exposure declined.",
            "The result supports intermittent dosing. Human tumor exposure and degradation remain unproven.",
        ),
        source="Source: Company preclinical data.",
    ),
    15: SlideSpec(
        15,
        SLIDE_TITLES[15],
        body=(
            "Published single-agent evidence | T-ALL and CTCL models",
            "Published combination evidence | AML, SCLC, KRAS G12C cancers, pancreatic cancer, breast cancer and FLC models",
            "Submitted evidence | Paclitaxel combination across ovarian cell lines, patient-derived models and PDX studies",
        ),
        source="Sources: Selected peer-reviewed studies listed on slide 34; Qin et al., submitted manuscript, July 2026.",
        status_note="Selected preclinical evidence; not a clinical-efficacy comparison across indications.",
    ),
    16: SlideSpec(
        16,
        SLIDE_TITLES[16],
        body=(
            "Ovarian cancer | Most complete current package | Recruiting Phase 1b",
            "Fibrolamellar carcinoma | Published PDX rationale | Phase 1/2 suspended for unacceptable toxicity",
            "CTCL | Published xenograft evidence | Proposed company program",
            "ER-positive breast cancer | Unpublished preclinical evidence | Proposed company program",
        ),
        source="Sources: NCT06964009; NCT06620302; cited publications; company information.",
    ),
    17: SlideSpec(
        17,
        SLIDE_TITLES[17],
        "Paclitaxel reduces MCL-1 during mitotic arrest while DT2216 degrades BCL-XL.",
        body=(
            "The combination functionally co-targets complementary survival pathways without administering a direct MCL-1 inhibitor.",
            "Direct BCL-XL and MCL-1 inhibition is mechanistic context, not the clinical regimen.",
        ),
        source="Source: Qin et al., submitted manuscript, July 2026, Figures 1–3.",
        status_note="Confidential; not peer reviewed.",
    ),
    18: SlideSpec(
        18,
        SLIDE_TITLES[18],
        "MCL-1 falls during mitotic arrest while BCL-XL dependence rises in the same cells.",
        body=(
            "Paclitaxel reduced MCL-1 and produced the BCL-XL phospho-shift.",
            "Mitotically arrested cells showed greater BCL-XL dependence by BH3 profiling.",
        ),
        source="Sources: Qin et al., submitted manuscript, July 2026, Figures 3 and 5; Sarosiek AACR 2026.",
        status_note="Confidential; not peer reviewed.",
    ),
    19: SlideSpec(
        19,
        SLIDE_TITLES[19],
        body=(
            "7 of 8 models showed synergy at one or more tested dose combinations.",
            "The models represented zero to seven prior chemotherapy lines.",
            "5 of 8 met the manuscript threshold for DT2216 single-agent sensitivity.",
        ),
        source="Source: Qin et al., submitted manuscript, July 2026, Figure 6D.",
        status_note="Short-term ex-vivo assay; one biological replicate shown, representative of two. Confidential; not peer reviewed.",
    ),
    20: SlideSpec(
        20,
        SLIDE_TITLES[20],
        body=(
            "Flank PDX | Complete regression; DT2216 stopped at day 138 with no regrowth during 100 additional days.",
            "Disseminated intraperitoneal PDX | Background-level signal by day 40; median survival increased 35 days versus paclitaxel.",
        ),
        source="Source: Qin et al., submitted manuscript, July 2026, Figure 8.",
        status_note="Preclinical. Confidential; not peer reviewed.",
    ),
    21: SlideSpec(
        21,
        SLIDE_TITLES[21],
        body=(
            "55 of 55 cell lines showed synergy at one or more tested dose combinations.",
            "Twelve tumor types and both wild-type and mutant TP53 cell lines were represented.",
            "Average excess over Bliss was 10.7; range -19.1 to 68.0.",
        ),
        source="Source: Qin et al., submitted manuscript, July 2026, Figure 3F and Figure S3H.",
        status_note="In vitro; some tested dose combinations were antagonistic. Confidential; not peer reviewed.",
    ),
    22: SlideSpec(
        22,
        SLIDE_TITLES[22],
        body=(
            "DT2216 increased apoptosis with free DM4, MMAE and MMAF payloads in OVCAR8 cells.",
            "MMAF-induced apoptosis increased with BCL-XL inhibition or degradation, but not with selective BCL-2 or MCL-1 inhibition.",
            "DM4 is the payload used by mirvetuximab soravtansine. Free payload was tested; the intact ADC was not.",
        ),
        source="Source: Qin et al., submitted manuscript, July 2026, Figure 4E–F.",
        status_note="Figure 4E n=3; Figure 4F DM4/MMAE n=3 and MMAF n=1 biological replicate. In vitro. Confidential; not peer reviewed.",
    ),
    23: SlideSpec(
        23,
        SLIDE_TITLES[23],
        body=(
            "DT2216 plus irinotecan produced regression in FLC PDX models, including PDX 31.",
            "Tumors remained undetectable through the reported post-treatment monitoring period.",
            "The published preclinical rationale remains relevant, but the current clinical study is suspended.",
        ),
        source="Source: Shebl et al., JCI Insight 2022.",
    ),
    24: SlideSpec(
        24,
        SLIDE_TITLES[24],
        body=(
            "DT2216 inhibited growth of BCL-XL-dependent MyLa CTCL xenografts.",
            "The preclinical experiment showed less platelet toxicity than navitoclax.",
            "The result supports clinical study in a biologically selected population; it is not clinical safety evidence.",
        ),
        source="Source: He et al., J Hematol Oncol 2020.",
    ),
    25: SlideSpec(
        25,
        SLIDE_TITLES[25],
        body=(
            "Company experiments tested DT2216 with fulvestrant in endocrine-resistant ER-positive breast-cancer models.",
            "The combination suppressed tumor growth in the displayed mouse and rat experiments.",
            "The evidence is unpublished and does not establish clinical activity.",
        ),
        source="Source: Li et al., unpublished company data.",
        status_note="Preclinical and unpublished.",
    ),
    26: SlideSpec(
        26,
        SLIDE_TITLES[26],
        body=(
            "20 heavily pretreated patients enrolled.",
            "0.40 mg/kg IV twice weekly selected as the recommended Phase 2 dose.",
            "Thrombocytopenia occurred in 9 of 20 patients; one dose-limiting grade 4 event resolved within 48 hours.",
            "Stable disease was the best RECIST response in 4 of 20 patients; median duration was 107 days.",
        ),
        source="Source: Mahadevan et al., J Hematol Oncol 2025; NCT04886622.",
    ),
    27: SlideSpec(
        27,
        SLIDE_TITLES[27],
        body=(
            "Preclinical | DT2216 15 mg/kg intraperitoneally every four days with paclitaxel in DF83 PDX studies.",
            "Human Phase 1 | 0.40 mg/kg IV twice weekly; rapid and sustained BCL-XL degradation in peripheral leukocytes from four patients at the recommended dose.",
            "Remaining question | Human tumor exposure and BCL-XL degradation have not been demonstrated.",
        ),
        source="Sources: Qin et al., submitted manuscript, July 2026; Mahadevan et al., J Hematol Oncol 2025.",
        status_note="Mouse dose and route cannot be converted directly into the human dose.",
    ),
    28: SlideSpec(
        28,
        SLIDE_TITLES[28],
        "NCT06964009 is testing DT2216 with weekly paclitaxel in recurrent platinum-resistant ovarian cancer.",
        body=(
            "Registered Phase 1b | Recruiting | Estimated enrollment 30 | BOIN dose-escalation design",
            "Company protocol doses | DT2216 0.32 or 0.40 mg/kg IV twice weekly; paclitaxel 70 or 80 mg/m² IV weekly",
            "Primary registered outcome | Combination maximum tolerated dose",
            "A later Phase 2 expansion remains a company plan and is not included in the current registry record.",
        ),
        source="Sources: ClinicalTrials.gov NCT06964009, accessed September 4, 2026; company protocol for dose levels.",
    ),
    29: SlideSpec(
        29,
        SLIDE_TITLES[29],
        "ClinicalTrials.gov lists NCT06620302 as suspended for unacceptable toxicity.",
        body=(
            "Registered design | Phase 1 dose escalation in recurrent or refractory solid tumors; Phase 2 FLC feasibility cohort",
            "Treatment | DT2216 IV on days 1, 4, 8, 11, 15 and 18; irinotecan IV on days 2–6 in cycle 1 and days 1–5 thereafter",
            "Current status | Suspended; status verified August 2026",
            "No assumption is made about restart timing or future enrollment.",
        ),
        source="Source: ClinicalTrials.gov NCT06620302, record updated August 24, 2026.",
    ),
    30: SlideSpec(
        30,
        SLIDE_TITLES[30],
        body=(
            "Completed | First-in-human dose escalation; 0.40 mg/kg twice-weekly recommended dose; Phase 1 publication",
            "Active | Ovarian Phase 1b recruiting; estimated primary completion December 30, 2026",
            "Suspended | FLC Phase 1/2 study; registry reason: unacceptable toxicity",
            "Planned | CTCL, ER-positive breast cancer and next-generation degraders; timing is a company estimate",
        ),
        source="Sources: Mahadevan et al., 2025; NCT06964009; NCT06620302; company information.",
    ),
    31: SlideSpec(
        31,
        SLIDE_TITLES[31],
        body=(
            "Does the human regimen reproduce tumor BCL-XL degradation?",
            "Can the combination maintain dose intensity through repeated cycles?",
            "Does clinical activity improve meaningfully on weekly paclitaxel experience?",
            "Is the preclinical combination effect reproducible in patients?",
        ),
        source="Sources: Mahadevan et al., 2025; Qin et al., submitted manuscript, July 2026; NCT06964009.",
    ),
    32: SlideSpec(
        32,
        SLIDE_TITLES[32],
        body=(
            "DT2216 | Company reports an exclusive worldwide UAMS license covering first-generation compounds and analogs.",
            "DT5321 | Company reports an exclusive worldwide University of Florida license covering second-generation compounds and analogs.",
            "Company reports two issued U.S. drug-substance patents for DT2216 expiring in 2037 and is pursuing additional analog and platform claims.",
        ),
        source="Source: Company information.",
        status_note="License scope, claim coverage and patent term remain subject to legal diligence.",
    ),
    33: SlideSpec(
        33,
        SLIDE_TITLES[33],
        body=(
            "DT2216 | Ovarian and endometrial cancer, FLC, CTCL, pancreatic cancer and other BCL-XL-dependent settings",
            "DT5321 | Leukemia, CLL and Richter transformation, prostate cancer and myeloproliferative neoplasms",
            "Third generation | Oral and broader BCL-family degradation research across additional solid and hematologic indications",
        ),
        source="Source: Company information.",
        status_note="Research collaborations do not establish clinical validation.",
    ),
    34: SlideSpec(
        34,
        SLIDE_TITLES[34],
        body=(
            "Clinical | Mahadevan et al., Journal of Hematology & Oncology, 2025",
            "Ovarian mechanism | Qin et al., bioRxiv preprint, 2025; confidential submitted manuscript, July 2026",
            "Platform foundation | Khan et al., Nature Medicine, 2019; Zhang et al., Chemical Communications, 2019; He et al., Journal of Hematology & Oncology, 2020",
            "Combination and indication evidence | Shebl et al., JCI Insight, 2022; Lv et al., Journal of Hematology & Oncology, 2022; selected 2025 studies",
        ),
        source="Sources: Journal and publication records; company bibliography.",
    ),
}


assert set(SLIDE_TITLES) == set(range(1, 35))
assert set(SLIDES) == set(range(1, 35))
for _number, _spec in SLIDES.items():
    assert _spec.number == _number
    assert _spec.title == SLIDE_TITLES[_number]

