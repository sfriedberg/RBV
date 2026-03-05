"use client";

import { useState } from "react";
import { MotionValue, useTransform, useMotionValueEvent, motion } from "framer-motion";
import Cell from "@/components/biology/Cell";
import SVGDefs from "@/components/biology/SVGDefs";
import Mitochondrion from "@/components/biology/Mitochondrion";
import BclXL from "@/components/biology/BclXL";
import BaxBak from "@/components/biology/BaxBak";
import Bim from "@/components/biology/Bim";
import Mcl1 from "@/components/biology/Mcl1";
import CytochromeC from "@/components/biology/CytochromeC";
import Apoptosome from "@/components/biology/Apoptosome";
import ParticleEffect from "@/components/ui/ParticleEffect";
import Label from "@/components/ui/Label";

interface Scene5Props {
  progress: MotionValue<number>;
  isInView: boolean;
}

export default function Scene5Combination({ progress, isInView }: Scene5Props) {
  // Phase 1 (0-0.10): Cancer cell with MCL-1 + BCL-XL active, both drugs approach
  // Phase 2 (0.10-0.25): Paclitaxel locks microtubules → MCL-1 degrades
  //                       DT2216 PROTAC binds BCL-XL → ubiquitin → degraded
  // Phase 3 (0.25-0.40): Both shields gone — BIM freed, BAX/BAK activate
  // Phase 4 (0.40-0.55): Pore opens, cytochrome c streams out
  // Phase 5 (0.55-0.70): Apoptosome assembles
  // Phase 6 (0.70-1.0): Caspase cascade → cell death

  const mcl1Range: [number, number] = [0.10, 0.20];
  const bclxlRange: [number, number] = [0.14, 0.24];

  // Drug entrance motion values
  const paxOpacity = useTransform(progress, [0.0, 0.08], [0, 1]);
  const paxX = useTransform(progress, [0.0, 0.12], [-50, 0]);
  const protacOpacity = useTransform(progress, [0.02, 0.10], [0, 1]);
  const protacX = useTransform(progress, [0.02, 0.14], [60, 0]);

  // Reactive state
  const [bimFreed, setBimFreed] = useState(false);
  const [baxActivated, setBaxActivated] = useState(false);
  const [showPore, setShowPore] = useState(false);
  const [streaming, setStreaming] = useState(false);
  const [showApoptosome, setShowApoptosome] = useState(false);
  const [cellDeath, setCellDeath] = useState(false);
  const [showMcl1X, setShowMcl1X] = useState(false);
  const [showBclxlX, setShowBclxlX] = useState(false);
  const [showDrugLabels, setShowDrugLabels] = useState(false);
  const [showShieldsDown, setShowShieldsDown] = useState(false);

  useMotionValueEvent(progress, "change", (v) => {
    setShowDrugLabels(v > 0.06 && v < 0.35);
    setShowMcl1X(v > 0.18 && v < 0.50);
    setShowBclxlX(v > 0.22 && v < 0.50);
    setShowShieldsDown(v > 0.26 && v < 0.50);
    setBimFreed(v > 0.30);
    setBaxActivated(v > 0.35);
    setShowPore(v > 0.42);
    setStreaming(v > 0.48);
    setShowApoptosome(v > 0.58);
    setCellDeath(v > 0.75);
  });

  return (
    <svg
      viewBox="0 0 600 500"
      className="w-full h-auto max-h-[70vh]"
      preserveAspectRatio="xMidYMid meet"
    >
      <SVGDefs />
      {isInView && (
        <>
          {/* ── Cancer cell ──────────────────────────── */}
          <Cell
            cx={280}
            cy={250}
            rx={165}
            ry={140}
            color="var(--color-cancer-cell)"
            cancer
            progress={progress}
            shrinkRange={[0.75, 0.90]}
          >
            <Mitochondrion x={220} y={220} scale={0.9} showPore={showPore} />

            {/* ── MCL-1: Paclitaxel target ───────── */}
            <Mcl1 x={180} y={185} progress={progress} degradeRange={mcl1Range} />
            {showMcl1X && (
              <motion.g
                initial={{ opacity: 0, scale: 0.3 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ type: "spring", stiffness: 200 }}
              >
                <circle cx={180} cy={185} r={14}
                  fill="var(--color-paclitaxel)" fillOpacity={0.1}
                  stroke="var(--color-paclitaxel)" strokeWidth={1.2} strokeOpacity={0.4}
                  filter="url(#glow-sm)" />
                <text x={180} y={190} textAnchor="middle"
                  fill="var(--color-paclitaxel)" fontSize={16} fontWeight="bold">
                  ✕
                </text>
              </motion.g>
            )}

            {/* ── BCL-XL: DT2216 target ──────────── */}
            <BclXL x={350} y={195} progress={progress} degradeRange={bclxlRange} showGlow={false} />
            {showBclxlX && (
              <motion.g
                initial={{ opacity: 0, scale: 0.3 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ type: "spring", stiffness: 200, delay: 0.1 }}
              >
                <circle cx={350} cy={195} r={14}
                  fill="var(--color-dt2216)" fillOpacity={0.1}
                  stroke="var(--color-dt2216)" strokeWidth={1.2} strokeOpacity={0.4}
                  filter="url(#glow-sm)" />
                <text x={350} y={200} textAnchor="middle"
                  fill="var(--color-dt2216)" fontSize={16} fontWeight="bold">
                  ✕
                </text>
              </motion.g>
            )}

            {/* ── BIM proteins freed ─────────────── */}
            <Bim x={240} y={200} freed={bimFreed} />
            <Bim x={280} y={190} freed={bimFreed} />
            <Bim x={310} y={210} freed={bimFreed} />

            {/* ── BAX/BAK activating ─────────────── */}
            <BaxBak x={200} y={240} label="BAX" activated={baxActivated} />
            <BaxBak x={240} y={248} label="BAK" activated={baxActivated} />

            {/* ── Cytochrome c streaming out ──────── */}
            <CytochromeC x={260} y={220} count={8} streaming={streaming} />
          </Cell>

          {/* ── Paclitaxel entering (left side) ──── */}
          <motion.g style={{ opacity: paxOpacity, x: paxX }}>
            {/* Paclitaxel triangle cluster */}
            <g transform="translate(110, 170)">
              <circle cx={0} cy={0} r={16}
                fill="var(--color-paclitaxel)" fillOpacity={0.06}
                filter="url(#glow-sm)" />
              <polygon points="0,-10 9,5 -9,5"
                fill="url(#grad-paclitaxel)" fillOpacity={0.9}
                stroke="var(--color-paclitaxel)" strokeWidth={0.8} />
              <text x={0} y={-14} textAnchor="middle"
                fill="var(--color-paclitaxel)" fontSize={5.5}
                fontFamily="var(--font-geist-mono), monospace"
                fontWeight="bold" letterSpacing="0.05em">
                PACLITAXEL
              </text>
            </g>
            {/* Arrow to MCL-1 */}
            <motion.path
              d="M126,170 Q145,175 160,180"
              fill="none" stroke="var(--color-paclitaxel)"
              strokeWidth={1.2} strokeDasharray="3 2"
              strokeLinecap="round"
              animate={{ pathLength: [0, 1] }}
              transition={{ duration: 1.2, delay: 0.2 }}
            />
          </motion.g>

          {/* ── DT2216 PROTAC entering (right side) ── */}
          <motion.g style={{ opacity: protacOpacity, x: protacX }}>
            {/* PROTAC dumbbell */}
            <g transform="translate(480, 185)">
              <circle cx={0} cy={0} r={16}
                fill="var(--color-dt2216)" fillOpacity={0.06}
                filter="url(#glow-sm)" />
              {/* Two-headed molecule */}
              <circle cx={-10} cy={0} r={6}
                fill="url(#grad-dt2216)" fillOpacity={0.9}
                stroke="var(--color-dt2216)" strokeWidth={0.6} />
              <line x1={-4} y1={0} x2={4} y2={0}
                stroke="var(--color-dt2216)" strokeWidth={1} strokeDasharray="2 1" />
              <circle cx={10} cy={0} r={6}
                fill="url(#grad-dt2216)" fillOpacity={0.9}
                stroke="var(--color-dt2216)" strokeWidth={0.6} />
              <text x={0} y={-14} textAnchor="middle"
                fill="var(--color-dt2216)" fontSize={5.5}
                fontFamily="var(--font-geist-mono), monospace"
                fontWeight="bold" letterSpacing="0.05em">
                DT2216
              </text>
            </g>
            {/* Arrow to BCL-XL */}
            <motion.path
              d="M466,188 Q430,190 370,195"
              fill="none" stroke="var(--color-dt2216)"
              strokeWidth={1.2} strokeDasharray="3 2"
              strokeLinecap="round"
              animate={{ pathLength: [0, 1] }}
              transition={{ duration: 1.2, delay: 0.3 }}
            />
          </motion.g>

          {/* ── Drug target labels ────────────────── */}
          {showDrugLabels && (
            <motion.g initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.4 }}>
              <text x={180} y={166} textAnchor="middle"
                fill="var(--color-paclitaxel)" fontSize={5} fontWeight="600"
                fontFamily="var(--font-geist-mono), monospace" opacity={0.7}>
                MCL-1 target
              </text>
              <text x={350} y={174} textAnchor="middle"
                fill="var(--color-dt2216)" fontSize={5} fontWeight="600"
                fontFamily="var(--font-geist-mono), monospace" opacity={0.7}>
                BCL-XL target
              </text>
            </motion.g>
          )}

          {/* ── "Both shields down" banner ────────── */}
          {showShieldsDown && (
            <motion.g
              initial={{ opacity: 0, y: 5 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <rect x={185} y={138} width={190} height={20} rx={10}
                fill="var(--background)" fillOpacity={0.7}
                stroke="var(--color-bax-bak)" strokeWidth={0.6} strokeOpacity={0.3} />
              <text x={280} y={152} textAnchor="middle"
                fill="var(--color-bax-bak)" fontSize={7} fontWeight="bold"
                fontFamily="var(--font-geist-sans), system-ui, sans-serif"
                letterSpacing="0.06em">
                BOTH SHIELDS ELIMINATED
              </text>
            </motion.g>
          )}

          {/* ── Apoptosome assembly ──────────────── */}
          <Apoptosome x={480} y={265} visible={showApoptosome} />

          {/* ── Caspase cascade ──────────────────── */}
          {showApoptosome && (
            <motion.g
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.4 }}
            >
              {/* Cascade branching arrows */}
              <motion.path
                d="M480,290 L480,330 L462,355 M480,330 L498,355"
                fill="none"
                stroke="var(--color-caspase)"
                strokeWidth={1.5}
                strokeLinecap="round"
                animate={{ pathLength: [0, 1] }}
                transition={{ duration: 1, delay: 0.5 }}
              />
              {/* Caspase-9 label */}
              <circle cx={480} cy={310} r={6}
                fill="url(#grad-caspase)" fillOpacity={0.5}
                stroke="var(--color-caspase)" strokeWidth={0.6} />
              <text x={480} y={313} textAnchor="middle"
                fill="white" fontSize={4} fontWeight="bold">
                C9
              </text>
              {/* Caspase-3 / Caspase-7 */}
              <circle cx={462} cy={362} r={6}
                fill="url(#grad-caspase)" fillOpacity={0.6}
                stroke="var(--color-caspase)" strokeWidth={0.6} />
              <text x={462} y={365} textAnchor="middle"
                fill="white" fontSize={4} fontWeight="bold">
                C3
              </text>
              <circle cx={498} cy={362} r={6}
                fill="url(#grad-caspase)" fillOpacity={0.6}
                stroke="var(--color-caspase)" strokeWidth={0.6} />
              <text x={498} y={365} textAnchor="middle"
                fill="white" fontSize={4} fontWeight="bold">
                C7
              </text>
              <text
                x={480} y={385}
                textAnchor="middle"
                fill="var(--color-caspase)"
                fontSize={6}
                fontWeight="bold"
                fontFamily="var(--font-geist-mono), monospace"
                letterSpacing="0.08em"
              >
                CASPASE CASCADE
              </text>
            </motion.g>
          )}

          {/* ── Cell death particles ─────────────── */}
          <ParticleEffect
            x={280}
            y={250}
            active={cellDeath}
            count={20}
            color="var(--color-cancer-cell)"
          />

          {/* ── Final label ──────────────────────── */}
          <Label
            x={300}
            y={465}
            text="Irreversible apoptosis — cancer cell eliminated"
            visible={cellDeath}
            color="var(--color-bax-bak)"
            size={9}
          />
        </>
      )}
    </svg>
  );
}
