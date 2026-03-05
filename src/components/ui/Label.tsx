"use client";

import { motion } from "framer-motion";

interface LabelProps {
  x: number;
  y: number;
  text: string;
  visible?: boolean;
  color?: string;
  size?: number;
  pill?: boolean;
}

export default function Label({
  x,
  y,
  text,
  visible = true,
  color = "var(--foreground)",
  size = 8,
  pill = true,
}: LabelProps) {
  const pillW = text.length * size * 0.52 + 16;
  const pillH = size + 10;

  return (
    <motion.g
      initial={{ opacity: 0, y: y + 6 }}
      animate={visible ? { opacity: 1, y } : { opacity: 0, y: y + 6 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
    >
      {/* Background pill for legibility */}
      {pill && (
        <rect
          x={x - pillW / 2}
          y={y - pillH / 2 - 2}
          width={pillW}
          height={pillH}
          rx={pillH / 2}
          fill="var(--background)"
          fillOpacity={0.7}
          stroke={color}
          strokeWidth={0.5}
          strokeOpacity={0.2}
        />
      )}
      <text
        x={x}
        y={y + size * 0.3}
        textAnchor="middle"
        fill={color}
        fontSize={size}
        fontFamily="var(--font-geist-sans), system-ui, sans-serif"
        fontWeight={600}
        letterSpacing="0.02em"
      >
        {text}
      </text>
    </motion.g>
  );
}
