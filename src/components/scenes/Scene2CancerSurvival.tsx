"use client";

import { useState } from "react";
import { MotionValue, useTransform, useMotionValueEvent, motion } from "framer-motion";
import Cell from "@/components/biology/Cell";
import Mitochondrion from "@/components/biology/Mitochondrion";
import BclXL from "@/components/biology/BclXL";
import BaxBak from "@/components/biology/BaxBak";
import Bim from "@/components/biology/Bim";
import PulseGlow from "@/components/ui/PulseGlow";
import Label from "@/components/ui/Label";

interface Scene2Props {
  progress: MotionValue<number>;
  isInView: boolean;
}

export default function Scene2CancerSurvival({ progress, isInView }: Scene2Props) {
  // Phase 1 (0-0.3): Cancer cell appears, BCL-XL prominent
  // Phase 2 (0.3-0.6): BIM signals appear and get trapped by BCL-XL
  // Phase 3 (0.6-1.0): "Primed for death" state - shield holds

  const shieldIntensity = useTransform(progress, [0.3, 0.7], [0.15, 0.35]);

  const [bimTrapped, setBimTrapped] = useState(false);
  const [primedLabel, setPrimedLabel] = useState(false);
  useMotionValueEvent(progress, "change", (v) => {
    setBimTrapped(v > 0.35);
    setPrimedLabel(v > 0.65);
  });

  return (
    <svg
      viewBox="0 0 600 500"
      className="w-full h-auto max-h-[70vh]"
      preserveAspectRatio="xMidYMid meet"
    >
      {isInView && (
        <>
          {/* Cancer cell - red tinted */}
          <Cell cx={300} cy={250} rx={180} ry={150} color="var(--color-cancer-cell)">
            <Mitochondrion x={230} y={210} scale={0.9} />
            <Mitochondrion x={370} y={280} scale={0.8} />

            {/* Multiple BCL-XL shields (overexpressed) */}
            <PulseGlow cx={200} cy={180} r={35} color="var(--color-bclxl)" />
            <BclXL x={200} y={180} showGlow={true} />

            <PulseGlow cx={300} cy={160} r={30} color="var(--color-bclxl)" />
            <BclXL x={300} y={160} showGlow={true} />

            <PulseGlow cx={400} cy={190} r={30} color="var(--color-bclxl)" />
            <BclXL x={400} y={190} showGlow={true} />

            {/* BAX/BAK suppressed */}
            <BaxBak x={260} y={330} label="BAX" activated={false} />
            <BaxBak x={340} y={330} label="BAK" activated={false} />

            {/* BIM signals getting trapped */}
            <Bim x={220} y={200} trapped={bimTrapped} />
            <Bim x={310} y={185} trapped={bimTrapped} />
            <Bim x={390} y={210} trapped={bimTrapped} />
            <Bim x={270} y={175} trapped={bimTrapped} />
          </Cell>

          {/* Shield effect overlay */}
          <motion.ellipse
            cx={300} cy={185}
            rx={140} ry={40}
            fill="none"
            stroke="var(--color-bclxl)"
            strokeWidth={1.5}
            strokeDasharray="6 3"
            style={{ opacity: shieldIntensity }}
          />

          {/* Labels */}
          <Label
            x={300} y={130}
            text="BCL-XL overexpressed"
            visible={true}
            color="var(--color-bclxl)"
            size={8}
          />
          <Label
            x={300} y={440}
            text="'Primed for death' — but the shield holds"
            visible={primedLabel}
            color="var(--color-cancer-cell)"
            size={9}
          />
        </>
      )}
    </svg>
  );
}
