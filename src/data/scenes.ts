export interface SceneData {
  id: string;
  index: number;
  title: string;
  subtitle: string;
  paragraphs: string[];
}

export const scenes: SceneData[] = [
  {
    id: "apoptosis",
    index: 0,
    title: "What is Apoptosis?",
    subtitle: "The cell's self-destruct program",
    paragraphs: [
      "Every cell in your body has a built-in self-destruct mechanism called apoptosis. It's how your body safely removes billions of old, damaged, or unneeded cells every day.",
      "The decision to live or die is governed by a family of proteins on the surface of mitochondria — the cell's powerhouses. Survival proteins like BCL-XL act as shields, while death proteins like BAX and BAK stand ready to execute.",
      "When the balance tips toward death, BAX and BAK punch holes in the mitochondria, releasing signals that activate caspases — molecular scissors that systematically dismantle the cell from within.",
    ],
  },
  {
    id: "cancer-survival",
    index: 1,
    title: "Cancer's Survival Shield",
    subtitle: "How cancer cells cheat death",
    paragraphs: [
      "Cancer cells are under enormous stress — DNA damage, immune attacks, and rapid growth all generate strong death signals. By rights, they should self-destruct.",
      "Instead, many cancers massively overproduce BCL-XL. This survival protein intercepts death signals like BIM before they can activate BAX and BAK. The cell is 'primed for death' but the shield holds.",
      "This is why some tumors resist chemotherapy. The drugs generate death signals, but BCL-XL absorbs them all, keeping the cancer cell alive.",
    ],
  },
  {
    id: "paclitaxel",
    index: 2,
    title: "Paclitaxel's Attack",
    subtitle: "Freezing cells mid-division",
    paragraphs: [
      "Paclitaxel is a powerful chemotherapy drug that targets the cell's skeleton — specifically the microtubules that pull chromosomes apart during division.",
      "By locking microtubules in place, paclitaxel freezes the cell in mitotic arrest. During this crisis, one key survival protein (MCL-1) is destroyed, and death signals like BIM accumulate.",
      "But in BCL-XL-rich cancers, the remaining shield catches every freed death signal. The cell eventually slips through the arrest and survives. BCL-XL is the last line of defense — and it holds.",
    ],
  },
  {
    id: "dt2216",
    index: 3,
    title: "Enter DT2216",
    subtitle: "A molecular matchmaker for destruction",
    paragraphs: [
      "DT2216 is a PROTAC — a two-headed molecule designed to destroy specific proteins. One end grabs BCL-XL. The other end recruits VHL, a component of the cell's protein recycling system.",
      "By bringing BCL-XL and VHL together, DT2216 triggers ubiquitin tagging — small 'destroy me' labels are attached to BCL-XL. The tagged protein is then fed into the proteasome and shredded.",
      "The breakthrough: platelets (blood cells needed for clotting) depend on BCL-XL too, but they barely produce any VHL. So DT2216 destroys BCL-XL in tumor cells while leaving platelets unharmed.",
    ],
  },
  {
    id: "combination",
    index: 4,
    title: "The Combination",
    subtitle: "Two drugs, one devastating strategy",
    paragraphs: [
      "Together, paclitaxel and DT2216 execute a coordinated attack. Paclitaxel freezes the cancer cell mid-division and destroys MCL-1. DT2216 simultaneously degrades BCL-XL.",
      "With both survival shields gone, the accumulated death signals are finally free. BIM activates BAX and BAK, which punch holes in the mitochondria. Cytochrome c floods out.",
      "The released cytochrome c assembles the apoptosome — a molecular death machine that activates caspases. The cascade is irreversible. The cancer cell is dismantled from within.",
    ],
  },
  {
    id: "clinical",
    index: 5,
    title: "Therapeutic Advantage",
    subtitle: "A wider therapeutic window",
    paragraphs: [
      "Previous BCL-XL inhibitors showed powerful anti-cancer activity but caused dangerous drops in platelet counts (thrombocytopenia), limiting their clinical use.",
      "DT2216's tissue-selective approach — exploiting low VHL in platelets — means the combination can be dosed effectively against tumors while maintaining safe platelet levels.",
      "This opens a therapeutic window that was previously impossible: the full power of BCL-XL elimination with an acceptable safety profile. Clinical trials are underway to bring this strategy to patients.",
    ],
  },
];
