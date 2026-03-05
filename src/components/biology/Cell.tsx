"use client";

import { motion, MotionValue, useTransform, useMotionValue } from "framer-motion";

interface CellProps {
  cx?: number;
  cy?: number;
  rx?: number;
  ry?: number;
  color?: string;
  cancer?: boolean;
  progress?: MotionValue<number>;
  shrinkRange?: [number, number];
  children?: React.ReactNode;
}

export default function Cell({
  cx = 300, cy = 250, rx = 180, ry = 150,
  color = "var(--color-cell-membrane)",
  cancer = false,
  progress, shrinkRange, children,
}: CellProps) {
  const fallback = useMotionValue(0);
  const hasProgress = !!(progress && shrinkRange);
  const source = hasProgress ? progress! : fallback;
  const range = hasProgress ? shrinkRange! : ([0, 1] as [number, number]);
  const fadeEnd = hasProgress ? shrinkRange![1] + 0.05 : 1;

  const scaleMV = useTransform(source, range, [1, 0.3]);
  const opacityMV = useTransform(source, [range[1], fadeEnd], [1, 0]);
  const scale = hasProgress ? scaleMV : undefined;
  const opacity = hasProgress ? opacityMV : undefined;
  const gradId = cancer ? "url(#grad-cytoplasm-cancer)" : "url(#grad-cytoplasm)";

  return (
    <motion.g
      style={scale ? { scale, opacity, transformOrigin: `${cx}px ${cy}px` } : undefined}
    >
      {/* Outer ambient glow */}
      <ellipse cx={cx} cy={cy} rx={rx + 20} ry={ry + 18}
        fill={color} fillOpacity={0.04} filter="url(#glow-lg)" />
      {/* Membrane outer halo */}
      <ellipse cx={cx} cy={cy} rx={rx + 6} ry={ry + 5}
        fill="none" stroke={color} strokeWidth={0.8} opacity={0.2} />
      {/* Cytoplasm fill */}
      <ellipse cx={cx} cy={cy} rx={rx} ry={ry} fill={gradId} />
      {/* Main lipid bilayer membrane */}
      <ellipse cx={cx} cy={cy} rx={rx} ry={ry}
        fill="none" stroke={color} strokeWidth={2.5}
        strokeDasharray="10 4 3 4" opacity={0.8} />
      {/* Inner membrane leaflet */}
      <ellipse cx={cx} cy={cy} rx={rx - 4} ry={ry - 3}
        fill="none" stroke={color} strokeWidth={0.6}
        strokeDasharray="2 6" opacity={0.25} />
      {/* Nucleus */}
      <circle cx={cx} cy={cy} r={rx * 0.26}
        fill="url(#grad-nucleus)" stroke="var(--color-nucleus)"
        strokeWidth={1.5} opacity={0.9} />
      {/* Nucleolus */}
      <circle cx={cx + rx * 0.06} cy={cy - rx * 0.05} r={rx * 0.08}
        fill="var(--color-nucleus)" fillOpacity={0.5} />
      {/* Chromatin speckles */}
      {[[-0.12, -0.1], [0.08, 0.12], [-0.05, 0.08], [0.14, -0.06]].map(([dx, dy], i) => (
        <circle key={i} cx={cx + rx * dx} cy={cy + rx * dy}
          r={1.5} fill="var(--color-nucleus)" fillOpacity={0.3} />
      ))}
      {children}
    </motion.g>
  );
}
