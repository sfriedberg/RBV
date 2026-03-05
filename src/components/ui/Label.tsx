"use client";

import { motion } from "framer-motion";

interface LabelProps {
  x: number;
  y: number;
  text: string;
  visible?: boolean;
  color?: string;
  size?: number;
}

export default function Label({
  x,
  y,
  text,
  visible = true,
  color = "var(--foreground)",
  size = 8,
}: LabelProps) {
  return (
    <motion.text
      x={x}
      y={y}
      textAnchor="middle"
      fill={color}
      fontSize={size}
      fontFamily="var(--font-geist-sans), system-ui, sans-serif"
      fontWeight={600}
      initial={{ opacity: 0, y: y + 5 }}
      animate={visible ? { opacity: 0.9, y } : { opacity: 0, y: y + 5 }}
      transition={{ duration: 0.5 }}
    >
      {text}
    </motion.text>
  );
}
