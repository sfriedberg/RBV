"use client";

import { motion } from "framer-motion";

interface PulseGlowProps {
  cx: number;
  cy: number;
  r?: number;
  color?: string;
}

export default function PulseGlow({
  cx,
  cy,
  r = 30,
  color = "var(--color-bclxl)",
}: PulseGlowProps) {
  return (
    <motion.circle
      cx={cx}
      cy={cy}
      r={r}
      fill={color}
      fillOpacity={0.08}
      animate={{
        r: [r, r + 10, r],
        fillOpacity: [0.08, 0.15, 0.08],
      }}
      transition={{ duration: 2.5, repeat: Infinity, ease: "easeInOut" }}
    />
  );
}
