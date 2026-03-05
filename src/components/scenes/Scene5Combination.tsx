"use client";

import { useState } from "react";
import { MotionValue, useTransform, useMotionValueEvent, motion } from "framer-motion";
import Cell from "@/components/biology/Cell";
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
  // Phase 1 (0-0.15): Cell with both MCL-1 and BCL-XL
  // Phase 2 (0.15-0.3): MCL-1 gone (X), BCL-XL gone (X)
  // Phase 3 (0.3-0.45): BIM freed, BAX/BAK activate
  // Phase 4 (0.45-0.6): Pore opens, cytochrome c streams out
  // Phase 5 (0.6-0.75): Apoptosome assembles
  // Phase 6 (0.75-1.0): Caspase cascade, cell death

  const mcl1Range: [number, number] = [0.12, 0.22];
  const bclxlRange: [number, number] = [0.18, 0.28];

  // Reactive state for props passed to non-motion components
  const [bimFreed, setBimFreed] = useState(false);
  const [baxActivated, setBaxActivated] = useState(false);
  const [showPore, setShowPore] = useState(false);
  const [streaming, setStreaming] = useState(false);
  const [showApoptosome, setShowApoptosome] = useState(false);
  const [cellDeath, setCellDeath] = useState(false);
  const [showMcl1X, setShowMcl1X] = useState(false);
  const [showBclxlX, setShowBclxlX] = useState(false);

  useMotionValueEvent(progress, "change", (v) => {
    setBimFreed(v > 0.3);
    setBaxActivated(v > 0.35);
    setShowPore(v > 0.45);
    setStreaming(v > 0.5);
    setShowApoptosome(v > 0.6);
    setCellDeath(v > 0.78);
    setShowMcl1X(v > 0.2 && v < 0.5);
    setShowBclxlX(v > 0.26 && v < 0.5);
  });

  return (
    <svg
      viewBox="0 0 600 500"
      className="w-full h-auto max-h-[70vh]"
      preserveAspectRatio="xMidYMid meet"
    >
      {isInView && (
        <>
          <Cell
            cx={280}
            cy={250}
            rx={165}
            ry={140}
            color="var(--color-cancer-cell)"
            progress={progress}
            shrinkRange={[0.78, 0.92]}
          >
            <Mitochondrion x={220} y={220} scale={0.9} showPore={showPore} />

            {/* MCL-1 being destroyed */}
            <Mcl1 x={180} y={180} progress={progress} degradeRange={mcl1Range} />
            {showMcl1X && (
              <motion.g initial={{ opacity: 0, scale: 0.5 }} animate={{ opacity: 1, scale: 1 }}>
                <text x={180} y={185} textAnchor="middle" fill="var(--color-paclitaxel)" fontSize={16} fontWeight="bold">
                  ✕
                </text>
                <text x={180} y={168} textAnchor="middle" fill="var(--color-paclitaxel)" fontSize={5}>
                  Paclitaxel
                </text>
              </motion.g>
            )}

            {/* BCL-XL being destroyed */}
            <BclXL x={350} y={190} progress={progress} degradeRange={bclxlRange} showGlow={false} />
            {showBclxlX && (
              <motion.g initial={{ opacity: 0, scale: 0.5 }} animate={{ opacity: 1, scale: 1 }}>
                <text x={350} y={195} textAnchor="middle" fill="var(--color-dt2216)" fontSize={16} fontWeight="bold">
                  ✕
                </text>
                <text x={350} y={178} textAnchor="middle" fill="var(--color-dt2216)" fontSize={5}>
                  DT2216
                </text>
              </motion.g>
            )}

            {/* BIM proteins freed */}
            <Bim x={240} y={200} freed={bimFreed} />
            <Bim x={280} y={190} freed={bimFreed} />
            <Bim x={310} y={210} freed={bimFreed} />

            {/* BAX/BAK activating */}
            <BaxBak
              x={200} y={240}
              label="BAX"
              activated={baxActivated}
            />
            <BaxBak
              x={240} y={240}
              label="BAK"
              activated={baxActivated}
            />

            {/* Cytochrome c streaming out */}
            <CytochromeC x={260} y={220} count={8} streaming={streaming} />
          </Cell>

          {/* Apoptosome assembly (outside cell area) */}
          <Apoptosome x={480} y={250} visible={showApoptosome} />

          {/* Caspase cascade label */}
          {showApoptosome && (
            <motion.g
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3 }}
            >
              {/* Caspase arrows */}
              <motion.path
                d="M500,280 L500,320 L480,340 M500,320 L520,340"
                fill="none"
                stroke="var(--color-caspase)"
                strokeWidth={1.5}
                strokeLinecap="round"
                animate={{ pathLength: [0, 1] }}
                transition={{ duration: 1, delay: 0.5 }}
              />
              <text
                x={500} y={360}
                textAnchor="middle"
                fill="var(--color-caspase)"
                fontSize={7}
                fontWeight="bold"
                fontFamily="var(--font-geist-mono), monospace"
              >
                Caspase Cascade
              </text>
            </motion.g>
          )}

          {/* Cell death particles */}
          <ParticleEffect
            x={280}
            y={250}
            active={cellDeath}
            count={16}
            color="var(--color-cancer-cell)"
          />

          {/* Final label */}
          <Label
            x={300}
            y={460}
            text="Both shields down — irreversible cell death"
            visible={cellDeath}
            color="var(--color-bax-bak)"
            size={10}
          />
        </>
      )}
    </svg>
  );
}
