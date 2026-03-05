"use client";

import { useState } from "react";
import { MotionValue, useTransform, useMotionValueEvent } from "framer-motion";
import Cell from "@/components/biology/Cell";
import SVGDefs from "@/components/biology/SVGDefs";
import Mitochondrion from "@/components/biology/Mitochondrion";
import BclXL from "@/components/biology/BclXL";
import BaxBak from "@/components/biology/BaxBak";
import Bim from "@/components/biology/Bim";
import Label from "@/components/ui/Label";

interface Scene1Props {
  progress: MotionValue<number>;
  isInView: boolean;
}

export default function Scene1Apoptosis({ progress, isInView }: Scene1Props) {
  // Phase 1 (0-0.3): Cell appears with balanced proteins
  // Phase 2 (0.3-0.6): Labels appear explaining each protein
  // Phase 3 (0.6-1.0): Death signals tip the balance, cell shrinks

  const baxActivated = useTransform(progress, [0.6, 0.8], [0, 1]);

  const [labelVisible, setLabelVisible] = useState(false);
  useMotionValueEvent(progress, "change", (v) => {
    const showLabels = v >= 0.25 ? Math.min((v - 0.25) / 0.1, 1) : 0;
    setLabelVisible(showLabels > 0.5);
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
          {/* Healthy cell */}
          <Cell cx={300} cy={250} rx={180} ry={150} progress={progress} shrinkRange={[0.85, 0.95]}>
            {/* Mitochondria */}
            <Mitochondrion x={220} y={200} scale={0.9} />
            <Mitochondrion x={380} y={280} scale={0.7} />

            {/* BCL-XL (survival shield) */}
            <BclXL x={200} y={175} showGlow={false} />

            {/* MCL-1 partner */}
            <g transform="translate(370, 260)">
              <polygon
                points="0,-14 12,10 -12,10"
                fill="var(--color-mcl1)"
                fillOpacity={0.8}
                stroke="var(--color-mcl1)"
                strokeWidth={1.5}
              />
              <text x={0} y={5} textAnchor="middle" fill="white" fontSize={5} fontWeight="bold" fontFamily="var(--font-geist-mono), monospace">
                MCL-1
              </text>
            </g>

            {/* BAX and BAK (inactive) */}
            <BaxBak x={250} y={320} label="BAX" progress={progress} activateRange={[0.6, 0.8]} />
            <BaxBak x={350} y={320} label="BAK" progress={progress} activateRange={[0.6, 0.8]} />

            {/* BIM signals */}
            <Bim x={300} y={180} />
            <Bim x={330} y={200} />
          </Cell>

          {/* Labels */}
          <Label x={130} y={160} text="Survival proteins" visible={labelVisible} color="var(--color-bclxl)" size={7} />
          <Label x={300} y={370} text="Death executioners" visible={labelVisible} color="var(--color-bax-bak)" size={7} />
          <Label x={340} y={165} text="Death signals" visible={labelVisible} color="var(--color-bim)" size={7} />

          {/* Scene title within SVG */}
          <text
            x={300} y={450}
            textAnchor="middle"
            fill="var(--text-muted)"
            fontSize={10}
            fontFamily="var(--font-geist-mono), monospace"
            opacity={0.5}
          >
            The balance between life and death
          </text>
        </>
      )}
    </svg>
  );
}
