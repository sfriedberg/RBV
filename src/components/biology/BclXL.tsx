"use client";

import { motion, MotionValue, useTransform, useMotionValue } from "framer-motion";

interface BclXLProps {
  x?: number;
  y?: number;
  progress?: MotionValue<number>;
  degradeRange?: [number, number];
  showGlow?: boolean;
  label?: boolean;
}

export default function BclXL({
  x = 0,
  y = 0,
  progress,
  degradeRange,
  showGlow = true,
  label = true,
}: BclXLProps) {
  const fallback = useMotionValue(0);
  const hasProgress = !!(progress && degradeRange);
  const source = hasProgress ? progress! : fallback;
  const range = hasProgress ? degradeRange! : [0, 1] as [number, number];

  const opacityMV = useTransform(source, range, [1, 0]);
  const scaleMV = useTransform(source, range, [1, 0.2]);

  const opacity = hasProgress ? opacityMV : undefined;
  const scale = hasProgress ? scaleMV : undefined;

  return (
    <motion.g
      style={{
        x, y,
        ...(opacity ? { opacity } : {}),
        ...(scale ? { scale } : {}),
        transformOrigin: "0px 0px",
      }}
    >
      {/* Shield glow */}
      {showGlow && (
        <motion.circle
          cx={0} cy={0} r={28}
          fill="var(--color-bclxl-glow)"
          fillOpacity={0.2}
          animate={{ r: [28, 33, 28], fillOpacity: [0.2, 0.1, 0.2] }}
          transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
        />
      )}
      {/* Shield shape */}
      <path
        d="M0,-18 L15,-8 L12,12 L0,18 L-12,12 L-15,-8 Z"
        fill="var(--color-bclxl)"
        fillOpacity={0.8}
        stroke="var(--color-bclxl)"
        strokeWidth={1.5}
      />
      {/* Label */}
      {label && (
        <text
          x={0} y={2}
          textAnchor="middle"
          fill="white"
          fontSize={7}
          fontWeight="bold"
          fontFamily="var(--font-geist-mono), monospace"
        >
          BCL-XL
        </text>
      )}
    </motion.g>
  );
}
