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
  x = 0, y = 0,
  progress, degradeRange,
  showGlow = true, label = true,
}: BclXLProps) {
  const fallback = useMotionValue(0);
  const hasProgress = !!(progress && degradeRange);
  const source = hasProgress ? progress! : fallback;
  const range = hasProgress ? degradeRange! : ([0, 1] as [number, number]);

  const opacityMV = useTransform(source, range, [1, 0]);
  const scaleMV = useTransform(source, range, [1, 0.2]);

  return (
    <motion.g
      style={{
        x, y,
        ...(hasProgress ? { opacity: opacityMV, scale: scaleMV } : {}),
        transformOrigin: "0px 0px",
      }}
    >
      {showGlow && (
        <>
          <motion.circle cx={0} cy={0} r={30}
            fill="var(--color-bclxl)" fillOpacity={0.08} filter="url(#glow-md)"
            animate={{ r: [30, 36, 30], fillOpacity: [0.08, 0.14, 0.08] }}
            transition={{ duration: 2.5, repeat: Infinity, ease: "easeInOut" }} />
          <motion.circle cx={0} cy={0} r={22}
            fill="none" stroke="var(--color-bclxl-glow)"
            strokeWidth={0.8} strokeOpacity={0.25}
            animate={{ r: [22, 26, 22], strokeOpacity: [0.25, 0.1, 0.25] }}
            transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }} />
        </>
      )}
      {/* Shield shape */}
      <path d="M0,-20 L17,-10 L14,13 L0,20 L-14,13 L-17,-10 Z"
        fill="url(#grad-bclxl)" stroke="#fca5a5"
        strokeWidth={1} strokeOpacity={0.6}
        filter={showGlow ? "url(#glow-sm)" : undefined} />
      {/* Inner highlight */}
      <path d="M0,-14 L11,-7 L9,9 L0,14 L-9,9 L-11,-7 Z"
        fill="none" stroke="white" strokeWidth={0.4} strokeOpacity={0.2} />
      {label && (
        <text x={0} y={2} textAnchor="middle"
          fill="white" fontSize={7} fontWeight="bold"
          fontFamily="var(--font-geist-mono), monospace">
          BCL-XL
        </text>
      )}
    </motion.g>
  );
}
