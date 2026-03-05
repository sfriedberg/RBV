"use client";

import { motion, MotionValue, useTransform, useMotionValue } from "framer-motion";

interface CellProps {
  cx?: number;
  cy?: number;
  rx?: number;
  ry?: number;
  color?: string;
  progress?: MotionValue<number>;
  shrinkRange?: [number, number];
  children?: React.ReactNode;
}

export default function Cell({
  cx = 300,
  cy = 250,
  rx = 180,
  ry = 150,
  color = "var(--color-cell-membrane)",
  progress,
  shrinkRange,
  children,
}: CellProps) {
  const fallback = useMotionValue(0);
  const hasProgress = !!(progress && shrinkRange);
  const source = hasProgress ? progress! : fallback;
  const range = hasProgress ? shrinkRange! : [0, 1] as [number, number];
  const fadeEnd = hasProgress ? shrinkRange![1] + 0.05 : 1;

  const scaleMV = useTransform(source, range, [1, 0.3]);
  const opacityMV = useTransform(source, [range[1], fadeEnd], [1, 0]);

  const scale = hasProgress ? scaleMV : undefined;
  const opacity = hasProgress ? opacityMV : undefined;

  return (
    <motion.g
      style={scale ? { scale, opacity, transformOrigin: `${cx}px ${cy}px` } : undefined}
    >
      {/* Cell membrane glow */}
      <ellipse
        cx={cx} cy={cy} rx={rx + 8} ry={ry + 8}
        fill="none"
        stroke={color}
        strokeWidth={1}
        opacity={0.15}
      />
      {/* Main membrane */}
      <ellipse
        cx={cx} cy={cy} rx={rx} ry={ry}
        fill={color}
        fillOpacity={0.05}
        stroke={color}
        strokeWidth={2}
        strokeDasharray="8 4"
      />
      {/* Nucleus */}
      <circle
        cx={cx}
        cy={cy}
        r={rx * 0.25}
        fill="var(--color-nucleus)"
        fillOpacity={0.3}
        stroke="var(--color-nucleus)"
        strokeWidth={1.5}
      />
      {children}
    </motion.g>
  );
}
