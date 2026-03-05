"use client";

import { motion } from "framer-motion";

interface ApoptosomeProps {
  x?: number;
  y?: number;
  visible?: boolean;
}

export default function Apoptosome({
  x = 0,
  y = 0,
  visible = false,
}: ApoptosomeProps) {
  const spokes = 7;

  return (
    <motion.g
      initial={{ opacity: 0, scale: 0.3 }}
      animate={visible ? { opacity: 1, scale: 1 } : { opacity: 0, scale: 0.3 }}
      transition={{ duration: 0.8, ease: "easeOut" }}
      style={{ x, y }}
    >
      {/* Hub */}
      <circle cx={0} cy={0} r={6} fill="var(--color-cytochrome-c)" fillOpacity={0.7} />
      {/* Spokes and outer nodes */}
      {Array.from({ length: spokes }).map((_, i) => {
        const angle = (i / spokes) * Math.PI * 2 - Math.PI / 2;
        const outerX = Math.cos(angle) * 22;
        const outerY = Math.sin(angle) * 22;
        return (
          <g key={i}>
            <line
              x1={0} y1={0} x2={outerX} y2={outerY}
              stroke="var(--color-cytochrome-c)"
              strokeWidth={1}
              opacity={0.5}
            />
            <circle
              cx={outerX} cy={outerY} r={5}
              fill="var(--color-cytochrome-c)"
              fillOpacity={0.5}
              stroke="var(--color-cytochrome-c)"
              strokeWidth={1}
            />
          </g>
        );
      })}
      <text
        x={0} y={38}
        textAnchor="middle"
        fill="var(--color-cytochrome-c)"
        fontSize={6}
        fontFamily="var(--font-geist-mono), monospace"
      >
        Apoptosome
      </text>
    </motion.g>
  );
}
