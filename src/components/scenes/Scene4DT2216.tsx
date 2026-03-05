"use client";

import { useState } from "react";
import { MotionValue, useTransform, useMotionValueEvent, motion } from "framer-motion";
import Cell from "@/components/biology/Cell";
import SVGDefs from "@/components/biology/SVGDefs";
import Mitochondrion from "@/components/biology/Mitochondrion";
import BclXL from "@/components/biology/BclXL";
import PROTAC from "@/components/biology/PROTAC";
import Ubiquitin from "@/components/biology/Ubiquitin";
import Proteasome from "@/components/biology/Proteasome";
import Label from "@/components/ui/Label";
import ParticleEffect from "@/components/ui/ParticleEffect";

interface Scene4Props {
  progress: MotionValue<number>;
  isInView: boolean;
}

export default function Scene4DT2216({ progress, isInView }: Scene4Props) {
  // Phase 1 (0-0.2): Cancer cell with BCL-XL
  // Phase 2 (0.2-0.4): DT2216 enters
  // Phase 3 (0.4-0.55): DT2216 binds BCL-XL + recruits VHL
  // Phase 4 (0.55-0.7): Ubiquitin chain grows
  // Phase 5 (0.7-0.85): Proteasome degrades BCL-XL
  // Phase 6 (0.85-1.0): Platelet sparing callout

  const ubGrowRange: [number, number] = [0.55, 0.7];
  const bclDegradeRange: [number, number] = [0.7, 0.85];

  // MotionValues for motion.* elements
  const arrowOpacity = useTransform(progress, [0.65, 0.72], [0, 0.6]);
  const proteasomeFadeIn = useTransform(progress, [0.6, 0.7], [0, 1]);

  // Reactive state
  const [protacBinds, setProtacBinds] = useState(false);
  const [proteasomeActive, setProteasomeActive] = useState(false);
  const [bclDegraded, setBclDegraded] = useState(false);
  const [showPlatelet, setShowPlatelet] = useState(false);
  const [showVHL, setShowVHL] = useState(false);
  const [protacXVal, setProtacXVal] = useState(80);
  const [protacYVal, setProtacYVal] = useState(150);

  useMotionValueEvent(progress, "change", (v) => {
    setProtacBinds(v > 0.35);
    setShowVHL(v > 0.42 && v < 0.85);
    setProteasomeActive(v > 0.7 && v < 0.9);
    setBclDegraded(v > 0.82);
    setShowPlatelet(v > 0.85);

    // Compute PROTAC position
    if (v <= 0.2) {
      setProtacXVal(80);
      setProtacYVal(150);
    } else if (v >= 0.4) {
      setProtacXVal(260);
      setProtacYVal(200);
    } else {
      const t = (v - 0.2) / 0.2;
      setProtacXVal(80 + t * (260 - 80));
      setProtacYVal(150 + t * (200 - 150));
    }
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
          {/* Cancer cell */}
          <Cell cx={300} cy={260} rx={170} ry={140} color="var(--color-cancer-cell)" cancer>
            <Mitochondrion x={250} y={230} scale={0.8} />

            {/* BCL-XL (will be degraded) */}
            <BclXL
              x={300}
              y={200}
              showGlow={!bclDegraded}
              progress={progress}
              degradeRange={bclDegradeRange}
            />

            {/* Ubiquitin chain on BCL-XL */}
            <Ubiquitin
              x={320}
              y={185}
              count={4}
              progress={progress}
              growRange={ubGrowRange}
            />

            {/* VHL recruitment label */}
            {showVHL && (
              <motion.g
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.4 }}
              >
                <circle cx={270} cy={215} r={10}
                  fill="var(--color-bax-bak)" fillOpacity={0.12}
                  stroke="var(--color-bax-bak)" strokeWidth={0.8} strokeOpacity={0.5} />
                <text x={270} y={218} textAnchor="middle"
                  fill="var(--color-bax-bak)" fontSize={5} fontWeight="bold"
                  fontFamily="var(--font-geist-mono), monospace">
                  VHL
                </text>
              </motion.g>
            )}
          </Cell>

          {/* DT2216 PROTAC molecule */}
          <PROTAC
            x={protacXVal}
            y={protacYVal}
            progress={progress}
            enterRange={[0.2, 0.4]}
          />

          {/* Proteasome */}
          <motion.g style={{ opacity: proteasomeFadeIn }}>
            <Proteasome x={450} y={260} active={proteasomeActive} />
          </motion.g>

          {/* Degradation particles */}
          <ParticleEffect
            x={300}
            y={200}
            active={bclDegraded}
            count={10}
            color="var(--color-bclxl)"
          />

          {/* Arrow from BCL-XL to proteasome */}
          <motion.path
            d="M330,210 Q390,225 435,250"
            fill="none"
            stroke="var(--color-ubiquitin)"
            strokeWidth={1.5}
            strokeDasharray="4 3"
            strokeLinecap="round"
            style={{ opacity: arrowOpacity }}
          />

          {/* Labels */}
          <Label
            x={130}
            y={155}
            text="DT2216 binds BCL-XL"
            visible={protacBinds && !bclDegraded}
            color="var(--color-dt2216)"
            size={7}
          />

          <Label
            x={450}
            y={310}
            text="Proteasome shreds tagged protein"
            visible={proteasomeActive}
            color="var(--color-proteasome)"
            size={6.5}
          />

          <Label
            x={300}
            y={135}
            text="BCL-XL eliminated"
            visible={bclDegraded}
            color="var(--color-dt2216)"
            size={8}
          />

          {/* Platelet callout */}
          {showPlatelet && (
            <motion.g
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <rect
                x={20} y={395}
                width={220} height={80}
                rx={10}
                fill="var(--background)"
                fillOpacity={0.75}
                stroke="var(--color-bax-bak)"
                strokeWidth={0.8}
                strokeOpacity={0.3}
              />
              {/* Platelet icon */}
              <ellipse
                cx={60} cy={430}
                rx={16} ry={11}
                fill="var(--color-cell-membrane)"
                fillOpacity={0.2}
                stroke="var(--color-cell-membrane)"
                strokeWidth={1.5}
              />
              <text
                x={60} y={433}
                textAnchor="middle"
                fill="var(--color-cell-membrane)"
                fontSize={5}
                fontWeight="bold"
                fontFamily="var(--font-geist-mono), monospace"
              >
                PLT
              </text>
              {/* Shield check icon */}
              <text x={60} y={452} textAnchor="middle"
                fill="var(--color-bax-bak)" fontSize={10}>
                ✓
              </text>
              <text
                x={148} y={424}
                textAnchor="middle"
                fill="var(--color-bax-bak)"
                fontSize={7.5}
                fontWeight="bold"
                fontFamily="var(--font-geist-sans), system-ui, sans-serif"
              >
                Platelets spared
              </text>
              <text
                x={148} y={440}
                textAnchor="middle"
                fill="var(--text-muted)"
                fontSize={5.5}
                fontFamily="var(--font-geist-sans), system-ui, sans-serif"
              >
                Low VHL expression in platelets
              </text>
              <text
                x={148} y={453}
                textAnchor="middle"
                fill="var(--text-muted)"
                fontSize={5.5}
                fontFamily="var(--font-geist-sans), system-ui, sans-serif"
                opacity={0.7}
              >
                → No DT2216-mediated degradation
              </text>
            </motion.g>
          )}
        </>
      )}
    </svg>
  );
}
