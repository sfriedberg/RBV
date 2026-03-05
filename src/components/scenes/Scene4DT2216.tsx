"use client";

import { useState } from "react";
import { MotionValue, useTransform, useMotionValueEvent, motion } from "framer-motion";
import Cell from "@/components/biology/Cell";
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
  // Phase 3 (0.4-0.55): DT2216 binds BCL-XL
  // Phase 4 (0.55-0.7): Ubiquitin chain grows
  // Phase 5 (0.7-0.85): Proteasome degrades BCL-XL
  // Phase 6 (0.85-1.0): Platelet sparing callout

  const ubGrowRange: [number, number] = [0.55, 0.7];
  const bclDegradeRange: [number, number] = [0.7, 0.85];

  // MotionValues used in style props on motion.* elements (these are fine)
  const protacX = useTransform(progress, [0.2, 0.4], [80, 260]);
  const protacY = useTransform(progress, [0.2, 0.4], [150, 200]);
  const arrowOpacity = useTransform(progress, [0.65, 0.72], [0, 0.6]);
  const proteasomeFadeIn = useTransform(progress, [0.6, 0.7], [0, 1]);

  // Reactive state for props passed to non-motion components
  const [protacBinds, setProtacBinds] = useState(false);
  const [proteasomeActive, setProteasomeActive] = useState(false);
  const [bclDegraded, setBclDegraded] = useState(false);
  const [showPlatelet, setShowPlatelet] = useState(false);
  const [protacXVal, setProtacXVal] = useState(80);
  const [protacYVal, setProtacYVal] = useState(150);
  const [proteasomeFadeInVal, setProteasomeFadeInVal] = useState(0);

  useMotionValueEvent(progress, "change", (v) => {
    setProtacBinds(v > 0.35);
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

    // Compute proteasome fade-in
    if (v <= 0.6) {
      setProteasomeFadeInVal(0);
    } else if (v >= 0.7) {
      setProteasomeFadeInVal(1);
    } else {
      setProteasomeFadeInVal((v - 0.6) / 0.1);
    }
  });

  return (
    <svg
      viewBox="0 0 600 500"
      className="w-full h-auto max-h-[70vh]"
      preserveAspectRatio="xMidYMid meet"
    >
      {isInView && (
        <>
          {/* Cancer cell */}
          <Cell cx={300} cy={260} rx={170} ry={140} color="var(--color-cancer-cell)">
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
          </Cell>

          {/* DT2216 PROTAC molecule */}
          <PROTAC
            x={protacXVal}
            y={protacYVal}
            progress={progress}
            enterRange={[0.2, 0.4]}
          />

          {/* Proteasome */}
          <motion.g
            style={{ opacity: proteasomeFadeIn }}
          >
            <Proteasome x={450} y={260} active={proteasomeActive} />
          </motion.g>

          {/* Degradation particles */}
          <ParticleEffect
            x={300}
            y={200}
            active={bclDegraded}
            count={8}
            color="var(--color-bclxl)"
          />

          {/* Arrow from BCL-XL to proteasome */}
          <motion.path
            d="M320,210 Q400,220 440,250"
            fill="none"
            stroke="var(--color-ubiquitin)"
            strokeWidth={1.5}
            strokeDasharray="4 3"
            style={{
              opacity: arrowOpacity,
            }}
          />

          {/* Labels */}
          <Label
            x={130}
            y={160}
            text="DT2216 binds BCL-XL"
            visible={protacBinds}
            color="var(--color-dt2216)"
            size={8}
          />

          <Label
            x={450}
            y={310}
            text="Protein shredder"
            visible={proteasomeActive}
            color="var(--color-proteasome)"
            size={7}
          />

          {/* Platelet callout */}
          {showPlatelet && (
            <motion.g
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <rect
                x={20} y={400}
                width={200} height={70}
                rx={8}
                fill="var(--color-bax-bak)"
                fillOpacity={0.08}
                stroke="var(--color-bax-bak)"
                strokeWidth={1}
              />
              {/* Platelet icon (small oval) */}
              <ellipse
                cx={60} cy={435}
                rx={15} ry={10}
                fill="var(--color-cell-membrane)"
                fillOpacity={0.3}
                stroke="var(--color-cell-membrane)"
                strokeWidth={1.5}
              />
              <text
                x={60} y={438}
                textAnchor="middle"
                fill="var(--color-cell-membrane)"
                fontSize={5}
                fontWeight="bold"
              >
                PLT
              </text>
              <text
                x={130} y={428}
                textAnchor="middle"
                fill="var(--color-bax-bak)"
                fontSize={7}
                fontWeight="bold"
              >
                Platelets spared
              </text>
              <text
                x={130} y={445}
                textAnchor="middle"
                fill="var(--text-muted)"
                fontSize={6}
              >
                No VHL = No degradation
              </text>
            </motion.g>
          )}
        </>
      )}
    </svg>
  );
}
