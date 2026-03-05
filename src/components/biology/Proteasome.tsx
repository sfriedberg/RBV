"use client";

import { motion } from "framer-motion";

interface ProteasomeProps {
  x?: number;
  y?: number;
  active?: boolean;
}

export default function Proteasome({
  x = 0,
  y = 0,
  active = false,
}: ProteasomeProps) {
  return (
    <g transform={`translate(${x}, ${y})`}>
      {/* Barrel shape */}
      <motion.rect
        x={-18} y={-25} width={36} height={50}
        rx={8}
        fill="var(--color-proteasome)"
        fillOpacity={0.2}
        stroke="var(--color-proteasome)"
        strokeWidth={2}
        animate={
          active
            ? { fillOpacity: [0.2, 0.4, 0.2] }
            : {}
        }
        transition={{ duration: 0.8, repeat: Infinity }}
      />
      {/* Inner rings */}
      <line x1={-14} y1={-10} x2={14} y2={-10} stroke="var(--color-proteasome)" strokeWidth={1} opacity={0.5} />
      <line x1={-14} y1={0} x2={14} y2={0} stroke="var(--color-proteasome)" strokeWidth={1} opacity={0.5} />
      <line x1={-14} y1={10} x2={14} y2={10} stroke="var(--color-proteasome)" strokeWidth={1} opacity={0.5} />
      {/* Label */}
      <text
        x={0} y={38}
        textAnchor="middle"
        fill="var(--color-proteasome)"
        fontSize={6}
        fontFamily="var(--font-geist-mono), monospace"
      >
        Proteasome
      </text>
    </g>
  );
}
