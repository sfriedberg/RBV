"use client";

import { motion } from "framer-motion";

interface PulseGlowProps {
  cx: number;
  cy: number;
  r?: number;
  color?: string;
}

export default function PulseGlow({
  cx, cy,
  r = 30,
  color = "var(--color-bclxl)",
}: PulseGlowProps) {
  return (
    <>
      {/* Outer soft ring */}
      <motion.circle
        cx={cx} cy={cy} r={r + 8}
        fill={color} fillOpacity={0.03}
        filter="url(#glow-lg)"
        animate={{ r: [r + 8, r + 16, r + 8], fillOpacity: [0.03, 0.06, 0.03] }}
        transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
      />
      {/* Inner pulse */}
      <motion.circle
        cx={cx} cy={cy} r={r}
        fill={color} fillOpacity={0.08}
        animate={{ r: [r, r + 10, r], fillOpacity: [0.08, 0.16, 0.08] }}
        transition={{ duration: 2.5, repeat: Infinity, ease: "easeInOut" }}
      />
    </>
  );
}
