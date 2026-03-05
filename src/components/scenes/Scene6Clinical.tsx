"use client";

import { useState } from "react";
import { MotionValue, useTransform, useMotionValueEvent, motion } from "framer-motion";
import Label from "@/components/ui/Label";
import SVGDefs from "@/components/biology/SVGDefs";

interface Scene6Props {
  progress: MotionValue<number>;
  isInView: boolean;
}

export default function Scene6Clinical({ progress, isInView }: Scene6Props) {
  // Phase 1 (0-0.3): Tumor cluster visible
  // Phase 2 (0.3-0.6): Tumor shrinks, cells die
  // Phase 3 (0.6-1.0): Platelet comparison graph

  const tumorScale = useTransform(progress, [0.2, 0.6], [1, 0.3]);
  const tumorOpacity = useTransform(progress, [0.5, 0.65], [1, 0.15]);
  const graphProgress = useTransform(progress, [0.55, 0.85], [0, 1]);
  const checkmarkOpacity = useTransform(progress, [0.55, 0.65], [0, 1]);
  const lineLabelsOpacity = useTransform(progress, [0.75, 0.85], [0, 1]);

  const [showGraph, setShowGraph] = useState(false);
  const [summaryVisible, setSummaryVisible] = useState(false);

  useMotionValueEvent(progress, "change", (v) => {
    setShowGraph(v > 0.55);
    setSummaryVisible(v > 0.82);
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
          {/* ── Tumor cluster ──────────────────── */}
          <motion.g
            style={{
              scale: tumorScale,
              opacity: tumorOpacity,
              transformOrigin: "200px 220px",
            }}
          >
            {/* Ambient glow */}
            <circle cx={205} cy={215} r={65}
              fill="var(--color-cancer-cell)" fillOpacity={0.04}
              filter="url(#glow-lg)" />
            {[
              [200, 200], [230, 180], [170, 190], [210, 230],
              [240, 210], [180, 220], [220, 250], [250, 235],
              [190, 250], [160, 225], [235, 260], [175, 170],
            ].map(([cx, cy], i) => (
              <g key={i}>
                <circle cx={cx} cy={cy} r={18 + (i % 3) * 3}
                  fill="var(--color-cancer-cell)"
                  fillOpacity={0.10 + (i % 4) * 0.03}
                  stroke="var(--color-cancer-cell)"
                  strokeWidth={1} strokeOpacity={0.4} />
                <circle cx={cx! + 2} cy={cy! - 1} r={4 + (i % 2)}
                  fill="var(--color-cancer-cell)" fillOpacity={0.2} />
              </g>
            ))}
            <text
              x={205} y={280}
              textAnchor="middle"
              fill="var(--color-cancer-cell)"
              fontSize={7}
              fontFamily="var(--font-geist-mono), monospace"
              fontWeight="600"
              letterSpacing="0.1em"
            >
              TUMOR
            </text>
          </motion.g>

          {/* ── Success indicator ────────────────── */}
          <motion.g style={{ opacity: checkmarkOpacity }}>
            <circle cx={200} cy={220} r={28}
              fill="var(--color-bax-bak)" fillOpacity={0.08}
              filter="url(#glow-md)" />
            <circle
              cx={200} cy={220}
              r={22}
              fill="none"
              stroke="var(--color-bax-bak)"
              strokeWidth={1.5}
              strokeOpacity={0.6}
            />
            <text
              x={200} y={227}
              textAnchor="middle"
              fill="var(--color-bax-bak)"
              fontSize={18}
              fontWeight="bold"
            >
              ✓
            </text>
            <text
              x={200} y={258}
              textAnchor="middle"
              fill="var(--color-bax-bak)"
              fontSize={6}
              fontFamily="var(--font-geist-mono), monospace"
              fontWeight="600"
              letterSpacing="0.08em"
            >
              TUMOR RESPONSE
            </text>
          </motion.g>

          {/* ── Platelet safety graph ────────────── */}
          {showGraph && (
            <motion.g
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              {/* Graph container */}
              <rect
                x={315} y={135}
                width={260} height={215}
                rx={10}
                fill="var(--background)" fillOpacity={0.6}
                stroke="white" strokeWidth={0.5} strokeOpacity={0.08}
              />
              <rect
                x={315} y={135}
                width={260} height={215}
                rx={10}
                fill="none"
                stroke="white" strokeWidth={2} strokeOpacity={0.03}
                filter="url(#glow-sm)"
              />

              {/* Title */}
              <text x={445} y={160} textAnchor="middle"
                fill="var(--foreground)" fontSize={8.5} fontWeight="bold"
                fontFamily="var(--font-geist-sans), system-ui, sans-serif"
                letterSpacing="0.02em">
                Platelet Count
              </text>
              <text x={445} y={172} textAnchor="middle"
                fill="var(--text-muted)" fontSize={5}
                fontFamily="var(--font-geist-mono), monospace"
                opacity={0.6}>
                over treatment cycles
              </text>

              {/* Y axis */}
              <line x1={350} y1={185} x2={350} y2={330} stroke="var(--text-muted)" strokeWidth={0.4} strokeOpacity={0.3} />
              <text x={344} y={193} textAnchor="end" fill="var(--text-muted)" fontSize={5} opacity={0.6}>Normal</text>
              <text x={344} y={318} textAnchor="end" fill="var(--text-muted)" fontSize={5} opacity={0.6}>Low</text>

              {/* Gridlines */}
              {[215, 245, 275].map((y) => (
                <line key={y} x1={350} y1={y} x2={555} y2={y}
                  stroke="white" strokeWidth={0.3} strokeOpacity={0.04} />
              ))}

              {/* Danger zone */}
              <rect x={350} y={285} width={205} height={45} rx={4}
                fill="var(--color-bclxl)" fillOpacity={0.04} />
              <text x={555} y={312} textAnchor="end"
                fill="var(--color-bclxl)" fontSize={5} opacity={0.4}
                fontFamily="var(--font-geist-mono), monospace">
                thrombocytopenia
              </text>

              {/* Old approach line (navitoclax) — drops into danger */}
              <motion.path
                d="M370,200 Q410,205 430,260 Q450,310 505,315"
                fill="none"
                stroke="var(--color-bclxl)"
                strokeWidth={2}
                strokeDasharray="5 3"
                style={{
                  pathLength: graphProgress,
                  opacity: 0.6,
                }}
              />
              <motion.g style={{ opacity: lineLabelsOpacity }}>
                <circle cx={515} cy={315} r={3} fill="var(--color-bclxl)" fillOpacity={0.6} />
                <text x={523} y={318} fill="var(--color-bclxl)" fontSize={5.5} fontWeight="600">
                  Old inhibitors
                </text>
              </motion.g>

              {/* DT2216 line — stays in safe zone */}
              <motion.path
                d="M370,200 Q410,204 435,212 Q470,218 505,214"
                fill="none"
                stroke="var(--color-bax-bak)"
                strokeWidth={2.5}
                strokeLinecap="round"
                style={{
                  pathLength: graphProgress,
                }}
              />
              <motion.g style={{ opacity: lineLabelsOpacity }}>
                <circle cx={515} cy={214} r={3} fill="var(--color-bax-bak)" />
                <text x={523} y={217} fill="var(--color-bax-bak)" fontSize={5.5} fontWeight="bold">
                  DT2216
                </text>
              </motion.g>
            </motion.g>
          )}

          {/* Summary */}
          <Label
            x={300}
            y={465}
            text="Full anti-tumor efficacy with manageable platelet levels"
            visible={summaryVisible}
            color="var(--color-dt2216)"
            size={9}
          />
        </>
      )}
    </svg>
  );
}
