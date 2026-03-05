export interface GlossaryTerm {
  term: string;
  definition: string;
}

export const glossaryTerms: GlossaryTerm[] = [
  {
    term: "Apoptosis",
    definition:
      "Programmed cell death — a controlled self-destruct process that removes damaged or unneeded cells without harming surrounding tissue.",
  },
  {
    term: "BCL-XL",
    definition:
      "A survival protein that sits on the mitochondrial surface and acts as a shield, blocking the cell death machinery. Cancer cells often overproduce it.",
  },
  {
    term: "BAX & BAK",
    definition:
      "Executioner proteins that, when activated, punch holes in mitochondria to trigger irreversible cell death.",
  },
  {
    term: "BIM",
    definition:
      "A stress-sensor protein that activates the death machinery. It's the 'go' signal for apoptosis, but BCL-XL can trap and neutralize it.",
  },
  {
    term: "MCL-1",
    definition:
      "Another survival protein similar to BCL-XL. Paclitaxel treatment causes it to be destroyed during mitotic arrest.",
  },
  {
    term: "PROTAC",
    definition:
      "Proteolysis-Targeting Chimera — a molecular matchmaker that brings a target protein together with the cell's recycling machinery to destroy it.",
  },
  {
    term: "DT2216",
    definition:
      "A first-in-class PROTAC that selectively degrades BCL-XL in tumor cells by recruiting the VHL E3 ligase. Developed by Dialectic Therapeutics.",
  },
  {
    term: "VHL (E3 Ligase)",
    definition:
      "A cellular tagging machine that marks proteins for destruction. DT2216 hijacks VHL to tag BCL-XL. Crucially, platelets have very little VHL.",
  },
  {
    term: "Ubiquitin",
    definition:
      "A small 'destroy me' tag that gets attached to proteins destined for the proteasome. Multiple ubiquitins form a chain.",
  },
  {
    term: "Proteasome",
    definition:
      "The cell's protein shredder — a barrel-shaped machine that chews up ubiquitin-tagged proteins into small fragments.",
  },
  {
    term: "Cytochrome c",
    definition:
      "A molecule normally inside mitochondria. When released through BAX/BAK pores, it triggers assembly of the death machinery.",
  },
  {
    term: "Apoptosome",
    definition:
      "A wheel-shaped molecular machine assembled after cytochrome c release. It activates caspases to execute cell death.",
  },
  {
    term: "Caspases",
    definition:
      "Protein-cutting enzymes that systematically dismantle the cell during apoptosis — the final executioners.",
  },
  {
    term: "Paclitaxel",
    definition:
      "A chemotherapy drug (taxane) that stabilizes microtubules, freezing cells mid-division and triggering stress signals that push toward cell death.",
  },
  {
    term: "Mitotic Arrest",
    definition:
      "When a cell gets stuck in the middle of dividing and cannot proceed — paclitaxel causes this by locking microtubules in place.",
  },
  {
    term: "Thrombocytopenia",
    definition:
      "Dangerously low platelet counts — a side effect of older BCL-XL inhibitors. DT2216 avoids this because platelets lack VHL.",
  },
  {
    term: "MOMP",
    definition:
      "Mitochondrial Outer Membrane Permeabilization — the point of no return when BAX/BAK punch holes and release death signals.",
  },
];
