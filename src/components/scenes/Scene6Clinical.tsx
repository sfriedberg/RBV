"use client";

import { useState } from "react";
import { MotionValue, useTransform, useMotionValueEvent, motion } from "framer-motion";
import Label from "@/components/ui/Label";

interface Scene6Props {
  progress: MotionValue<number>;
  isInView: boolean;
}

export default function Scene6Clinical({ progress, isInView }: Scene6Props) {
  // Phase 1 (0-0.3): Tumor cluster visible
  // Phase 2 (0.3-0.6): Tumor shrinks, cells die
  // Phase 3 (0.6-1.0): Platelet comparison graph

  // MotionValues used in style props on motion.* elements (these are fine)
  const tumorScale = useTransform(progress, [0.2, 0.6], [1, 0.3]);
  const tumorOpacity = useTransform(progress, [0.5, 0.65], [1, 0.2]);
  const graphProgress = useTransform(progress, [0.55, 0.85], [0, 1]);
  const checkmarkOpacity = useTransform(progress, [0.55, 0.65], [0, 1]);
  const lineLabelsOpacity = useTransform(progress, [0.75, 0.85], [0, 1]);

  // Reactive state for props passed to non-motion components and conditional rendering
  const [showGraph, setShowGraph] = useState(false);
  const [summaryVisible, setSummaryVisible] = useState(false);

  useMotionValueEvent(progress, "change", (v) => {
    setShowGraph(v > 0.55);
    setSummaryVisible(v > 0.8);
  });

  return (
    <svg
      viewBox="0 0 600 500"
      className="w-full h-auto max-h-[70vh]"
      preserveAspectRatio="xMidYMid meet"
    >
      {isInView && (
        <>
          {/* Tumor cluster */}
          <motion.g
            style={{
              scale: tumorScale,
              opacity: tumorOpacity,
              transformOrigin: "200px 220px",
            }}
          >
            {/* Cancer cells cluster */}
            {[
              [200, 200], [230, 180], [170, 190], [210, 230],
              [240, 210], [180, 220], [220, 250], [250, 235],
              [190, 250], [160, 225], [235, 260], [175, 170],
            ].map(([cx, cy], i) => (
              <circle
                key={i}
                cx={cx}
                cy={cy}
                r={18 + (i % 3) * 3}
                fill="var(--color-cancer-cell)"
                fillOpacity={0.15 + (i % 3) * 0.05}
                stroke="var(--color-cancer-cell)"
                strokeWidth={1}
              />
            ))}
            <text
              x={205} y={275}
              textAnchor="middle"
              fill="var(--color-cancer-cell)"
              fontSize={8}
              fontFamily="var(--font-geist-mono), monospace"
            >
              Tumor
            </text>
          </motion.g>

          {/* Success checkmark appears as tumor shrinks */}
          <motion.g
            style={{
              opacity: checkmarkOpacity,
            }}
          >
            <circle
              cx={200} cy={220}
              r={25}
              fill="var(--color-bax-bak)"
              fillOpacity={0.15}
              stroke="var(--color-bax-bak)"
              strokeWidth={2}
            />
            <text
              x={200} y={227}
              textAnchor="middle"
              fill="var(--color-bax-bak)"
              fontSize={20}
            >
              ✓
            </text>
          </motion.g>

          {/* Platelet safety comparison */}
          {showGraph && (
            <motion.g
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              {/* Graph box */}
              <rect
                x={320} y={140}
                width={250} height={200}
                rx={8}
                fill="white"
                fillOpacity={0.03}
                stroke="white"
                strokeWidth={0.5}
                strokeOpacity={0.1}
              />

              <text x={445} y={165} textAnchor="middle" fill="var(--foreground)" fontSize={9} fontWeight="bold">
                Platelet Counts
              </text>

              {/* Y axis */}
              <line x1={350} y1={180} x2={350} y2={320} stroke="var(--text-muted)" strokeWidth={0.5} />
              <text x={342} y={190} textAnchor="end" fill="var(--text-muted)" fontSize={5}>Normal</text>
              <text x={342} y={310} textAnchor="end" fill="var(--text-muted)" fontSize={5}>Low</text>

              {/* Danger zone */}
              <rect x={350} y={270} width={200} height={50} fill="var(--color-bclxl)" fillOpacity={0.05} />
              <text x={540} y={300} textAnchor="end" fill="var(--color-bclxl)" fontSize={5} opacity={0.5}>
                Danger zone
              </text>

              {/* Old approach line (navitoclax) - drops into danger */}
              <motion.path
                d="M370,195 Q420,200 440,260 Q460,310 500,310"
                fill="none"
                stroke="var(--color-bclxl)"
                strokeWidth={2}
                strokeDasharray="4 2"
                style={{
                  pathLength: graphProgress,
                  opacity: 0.7,
                }}
              />
              <motion.text
                x={505} y={315}
                fill="var(--color-bclxl)"
                fontSize={6}
                style={{ opacity: lineLabelsOpacity }}
              >
                Old inhibitors
              </motion.text>

              {/* DT2216 line - stays in safe zone */}
              <motion.path
                d="M370,195 Q420,200 440,210 Q470,215 500,210"
                fill="none"
                stroke="var(--color-bax-bak)"
                strokeWidth={2.5}
                style={{
                  pathLength: graphProgress,
                }}
              />
              <motion.text
                x={505} y={208}
                fill="var(--color-bax-bak)"
                fontSize={6}
                fontWeight="bold"
                style={{ opacity: lineLabelsOpacity }}
              >
                DT2216
              </motion.text>
            </motion.g>
          )}

          {/* Summary label */}
          <Label
            x={300}
            y={460}
            text="Full anti-tumor power with safe platelet levels"
            visible={summaryVisible}
            color="var(--color-dt2216)"
            size={10}
          />
        </>
      )}
    </svg>
  );
}
