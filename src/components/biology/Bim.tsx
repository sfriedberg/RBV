"use client";

import { motion } from "framer-motion";

interface BimProps {
  x?: number;
  y?: number;
  trapped?: boolean;
  freed?: boolean;
}

export default function Bim({
  x = 0,
  y = 0,
  trapped = false,
  freed = false,
}: BimProps) {
  return (
    <motion.g
      animate={{
        x: freed ? x + (Math.random() * 40 - 20) : x,
        y: freed ? y + (Math.random() * 40 - 20) : y,
        scale: freed ? 1.3 : trapped ? 0.7 : 1,
        opacity: trapped ? 0.4 : 1,
      }}
      transition={{ duration: 1.5, ease: "easeInOut" }}
    >
      <motion.circle
        cx={0} cy={0} r={7}
        fill="var(--color-bim)"
        fillOpacity={0.9}
        animate={
          freed
            ? { r: [7, 9, 7], fillOpacity: [0.9, 1, 0.9] }
            : {}
        }
        transition={{ duration: 1, repeat: Infinity, ease: "easeInOut" }}
      />
      <text
        x={0} y={3}
        textAnchor="middle"
        fill="#1a2e05"
        fontSize={5}
        fontWeight="bold"
        fontFamily="var(--font-geist-mono), monospace"
      >
        BIM
      </text>
    </motion.g>
  );
}
