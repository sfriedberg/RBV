"use client";

import { useState } from "react";
import { MotionValue, useTransform, useMotionValueEvent, motion } from "framer-motion";
import Cell from "@/components/biology/Cell";
import Mitochondrion from "@/components/biology/Mitochondrion";
import BclXL from "@/components/biology/BclXL";
import BaxBak from "@/components/biology/BaxBak";
import Bim from "@/components/biology/Bim";
import Mcl1 from "@/components/biology/Mcl1";
import Microtubule from "@/components/biology/Microtubule";
import Label from "@/components/ui/Label";

interface Scene3Props {
  progress: MotionValue<number>;
  isInView: boolean;
}

export default function Scene3Paclitaxel({ progress, isInView }: Scene3Props) {
  // Phase 1 (0-0.25): Cell with microtubules visible
  // Phase 2 (0.25-0.45): Paclitaxel locks microtubules, mitotic arrest
  // Phase 3 (0.45-0.65): MCL-1 degrades, BIM accumulates
  // Phase 4 (0.65-1.0): BCL-XL catches everything, cell survives (slippage)

  const mcl1DegradeRange: [number, number] = [0.45, 0.6];

  // Paclitaxel molecules entering - used in style on motion.g, so keep as MotionValues
  const paxOpacity = useTransform(progress, [0.15, 0.25], [0, 1]);
  const paxX = useTransform(progress, [0.15, 0.3], [-60, 0]);

  // Reactive state for props passed to non-motion components
  const [mtLocked, setMtLocked] = useState(false);
  const [bimFreed, setBimFreed] = useState(false);
  const [bimTrapped, setBimTrapped] = useState(false);
  const [slippageLabel, setSlippageLabel] = useState(false);
  const [mcl1DestroyedLabel, setMcl1DestroyedLabel] = useState(false);

  useMotionValueEvent(progress, "change", (v) => {
    setMtLocked(v > 0.25);
    setBimFreed(v > 0.5 && v < 0.75);
    setBimTrapped(v > 0.75);
    setSlippageLabel(v > 0.8);
    setMcl1DestroyedLabel(v > 0.55);
  });

  return (
    <svg
      viewBox="0 0 600 500"
      className="w-full h-auto max-h-[70vh]"
      preserveAspectRatio="xMidYMid meet"
    >
      {isInView && (
        <>
          <Cell cx={300} cy={260} rx={180} ry={150} color="var(--color-cancer-cell)">
            <Mitochondrion x={230} y={220} scale={0.8} />

            {/* Microtubule structure */}
            <Microtubule x={300} y={200} locked={mtLocked} />

            {/* Paclitaxel molecules */}
            <motion.g style={{ opacity: paxOpacity, x: paxX }}>
              <g transform="translate(260, 195)">
                <polygon points="0,-6 5,3 -5,3" fill="var(--color-paclitaxel)" fillOpacity={0.9} />
              </g>
              <g transform="translate(300, 195)">
                <polygon points="0,-6 5,3 -5,3" fill="var(--color-paclitaxel)" fillOpacity={0.9} />
              </g>
              <g transform="translate(340, 195)">
                <polygon points="0,-6 5,3 -5,3" fill="var(--color-paclitaxel)" fillOpacity={0.9} />
              </g>
            </motion.g>

            {/* MCL-1 degrading */}
            <Mcl1 x={370} y={280} progress={progress} degradeRange={mcl1DegradeRange} />

            {/* BCL-XL shields (still standing) */}
            <BclXL x={220} y={300} showGlow={true} />
            <BclXL x={380} y={310} showGlow={true} />

            {/* BAX/BAK still suppressed */}
            <BaxBak x={280} y={360} label="BAX" activated={false} />
            <BaxBak x={340} y={360} label="BAK" activated={false} />

            {/* BIM accumulating then getting caught */}
            <Bim x={260} y={270} freed={bimFreed} trapped={bimTrapped} />
            <Bim x={310} y={260} freed={bimFreed} trapped={bimTrapped} />
            <Bim x={350} y={275} freed={bimFreed} trapped={bimTrapped} />
          </Cell>

          {/* Arrest label */}
          <Label
            x={300}
            y={130}
            text="Mitotic Arrest"
            visible={mtLocked}
            color="var(--color-paclitaxel)"
            size={10}
          />

          {/* MCL-1 degraded label */}
          <Label
            x={430}
            y={265}
            text="MCL-1 destroyed"
            visible={mcl1DestroyedLabel}
            color="var(--color-mcl1)"
            size={7}
          />

          {/* Slippage */}
          <Label
            x={300}
            y={460}
            text="BCL-XL catches all death signals — cell survives"
            visible={slippageLabel}
            color="var(--color-bclxl)"
            size={9}
          />
        </>
      )}
    </svg>
  );
}
