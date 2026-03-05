"use client";

import { motion } from "framer-motion";

interface BimProps {
  x?: number;
  y?: number;
  trapped?: boolean;
  freed?: boolean;
}

export default function Bim({
  x = 0, y = 0,
  trapped = false, freed = false,
}: BimProps) {
  return (
    <motion.g
      animate={{
        x: freed ? x + (Math.random() * 40 - 20) : x,
        y: freed ? y + (Math.random() * 40 - 20) : y,
        scale: freed ? 1.3 : trapped ? 0.7 : 1,
        opacity: trapped ? 0.35 : 1,
      }}
      transition={{ duration: 1.5, ease: "easeInOut" }}
    >
      {/* Outer glow when freed */}
      {freed && (
        <motion.circle
          cx={0} cy={0} r={14}
          fill="var(--color-bim)" fillOpacity={0.1}
          filter="url(#glow-sm)"
          animate={{ r: [14, 18, 14], fillOpacity: [0.1, 0.2, 0.1] }}
          transition={{ duration: 1.2, repeat: Infinity }}
        />
      )}
      <motion.circle
        cx={0} cy={0} r={8}
        fill="url(#grad-bim)"
        stroke="var(--color-bim)" strokeWidth={1} strokeOpacity={0.5}
        animate={freed ? { r: [8, 10, 8] } : {}}
        transition={{ duration: 1, repeat: Infinity, ease: "easeInOut" }}
      />
      {/* Inner highlight */}
      <circle
        cx={-2} cy={-2} r={3}
        fill="white" fillOpacity={0.15}
      />
      <text
        x={0} y={3} textAnchor="middle"
        fill="#1a2e05" fontSize={5} fontWeight="bold"
        fontFamily="var(--font-geist-mono), monospace"
      >
        BIM
      </text>
    </motion.g>
  );
}
