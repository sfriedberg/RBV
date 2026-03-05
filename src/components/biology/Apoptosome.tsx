"use client";

import { motion } from "framer-motion";

interface ApoptosomeProps {
  x?: number;
  y?: number;
  visible?: boolean;
}

export default function Apoptosome({
  x = 0, y = 0,
  visible = false,
}: ApoptosomeProps) {
  const spokes = 7;

  return (
    <motion.g
      initial={{ opacity: 0, scale: 0.3 }}
      animate={visible ? { opacity: 1, scale: 1, rotate: 360 } : { opacity: 0, scale: 0.3 }}
      transition={{ duration: 1.2, ease: "easeOut", rotate: { duration: 60, repeat: Infinity, ease: "linear" } }}
      style={{ x, y }}
    >
      {/* Outer glow ring */}
      <motion.circle
        cx={0} cy={0} r={32}
        fill="var(--color-cytochrome-c)" fillOpacity={0.05}
        filter="url(#glow-md)"
        animate={visible ? { fillOpacity: [0.03, 0.08, 0.03] } : {}}
        transition={{ duration: 2, repeat: Infinity }}
      />

      {/* Hub (cytochrome c core) */}
      <circle cx={0} cy={0} r={8}
        fill="url(#grad-cytc)"
        stroke="var(--color-cytochrome-c)" strokeWidth={1.5} strokeOpacity={0.6} />
      <circle cx={-2} cy={-2} r={3}
        fill="white" fillOpacity={0.12} />

      {/* Spokes and APAF-1 subunits */}
      {Array.from({ length: spokes }).map((_, i) => {
        const angle = (i / spokes) * Math.PI * 2 - Math.PI / 2;
        const outerX = Math.cos(angle) * 24;
        const outerY = Math.sin(angle) * 24;
        return (
          <g key={i}>
            {/* Spoke arm */}
            <line x1={0} y1={0} x2={outerX} y2={outerY}
              stroke="var(--color-cytochrome-c)" strokeWidth={1.5}
              opacity={0.4} strokeLinecap="round" />
            {/* APAF-1 outer node */}
            <circle cx={outerX} cy={outerY} r={6}
              fill="url(#grad-cytc)"
              stroke="var(--color-cytochrome-c)" strokeWidth={1}
              strokeOpacity={0.5} />
            {/* Highlight */}
            <circle cx={outerX - 1.5} cy={outerY - 1.5} r={2}
              fill="white" fillOpacity={0.1} />
          </g>
        );
      })}

      <text x={0} y={42} textAnchor="middle"
        fill="var(--color-cytochrome-c)" fontSize={6.5}
        fontFamily="var(--font-geist-mono), monospace" fontWeight="bold">
        Apoptosome
      </text>
    </motion.g>
  );
}
