"use client";

import { motion, MotionValue, useTransform } from "framer-motion";

interface UbiquitinProps {
  x?: number;
  y?: number;
  count?: number;
  progress?: MotionValue<number>;
  growRange?: [number, number];
}

export default function Ubiquitin({
  x = 0, y = 0,
  count = 4,
  progress, growRange,
}: UbiquitinProps) {
  return (
    <g transform={`translate(${x}, ${y})`}>
      {/* Chain connector line */}
      <line x1={0} y1={0} x2={(count - 1) * 11} y2={0}
        stroke="var(--color-ubiquitin)" strokeWidth={1}
        strokeOpacity={0.3} strokeDasharray="2 2" />

      {Array.from({ length: count }).map((_, i) => {
        const tagOpacity = progress && growRange
          ? useTransform(
              progress,
              [
                growRange[0] + (i / count) * (growRange[1] - growRange[0]),
                growRange[0] + ((i + 1) / count) * (growRange[1] - growRange[0]),
              ],
              [0, 1]
            )
          : 1;

        return (
          <motion.g key={i} style={{ opacity: tagOpacity }}>
            {/* Glow behind each tag */}
            <circle cx={i * 11} cy={0} r={7}
              fill="var(--color-ubiquitin)" fillOpacity={0.08}
              filter="url(#glow-sm)" />
            {/* Ubiquitin bead */}
            <circle cx={i * 11} cy={0} r={5}
              fill="url(#grad-ubiquitin)"
              stroke="var(--color-ubiquitin)" strokeWidth={0.8}
              strokeOpacity={0.6} />
            {/* Highlight */}
            <circle cx={i * 11 - 1.5} cy={-1.5} r={2}
              fill="white" fillOpacity={0.15} />
            <text x={i * 11} y={2.5} textAnchor="middle"
              fill="#422006" fontSize={4} fontWeight="bold">
              Ub
            </text>
          </motion.g>
        );
      })}
    </g>
  );
}
