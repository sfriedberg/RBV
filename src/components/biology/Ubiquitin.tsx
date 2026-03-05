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
  x = 0,
  y = 0,
  count = 4,
  progress,
  growRange,
}: UbiquitinProps) {
  return (
    <g transform={`translate(${x}, ${y})`}>
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
            <circle
              cx={i * 10} cy={0} r={4}
              fill="var(--color-ubiquitin)"
              stroke="var(--color-ubiquitin)"
              strokeWidth={0.8}
              fillOpacity={0.9}
            />
            <text
              x={i * 10} y={2.5}
              textAnchor="middle"
              fill="#422006"
              fontSize={4}
              fontWeight="bold"
            >
              Ub
            </text>
          </motion.g>
        );
      })}
    </g>
  );
}
