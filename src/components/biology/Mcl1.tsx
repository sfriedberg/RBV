"use client";

import { motion, MotionValue, useTransform, useMotionValue } from "framer-motion";

interface Mcl1Props {
  x?: number;
  y?: number;
  progress?: MotionValue<number>;
  degradeRange?: [number, number];
}

export default function Mcl1({
  x = 0,
  y = 0,
  progress,
  degradeRange,
}: Mcl1Props) {
  const fallback = useMotionValue(0);
  const hasProgress = !!(progress && degradeRange);
  const source = hasProgress ? progress! : fallback;
  const range = hasProgress ? degradeRange! : [0, 1] as [number, number];

  const opacityMV = useTransform(source, range, [1, 0]);
  const scaleMV = useTransform(source, range, [1, 0]);

  const opacity = hasProgress ? opacityMV : 1;
  const scale = hasProgress ? scaleMV : 1;

  return (
    <motion.g
      style={{
        x, y,
        opacity,
        scale,
        transformOrigin: "0px 0px",
      }}
    >
      {/* Triangle shape */}
      <polygon
        points="0,-14 12,10 -12,10"
        fill="var(--color-mcl1)"
        fillOpacity={0.8}
        stroke="var(--color-mcl1)"
        strokeWidth={1.5}
      />
      <text
        x={0} y={5}
        textAnchor="middle"
        fill="white"
        fontSize={5.5}
        fontWeight="bold"
        fontFamily="var(--font-geist-mono), monospace"
      >
        MCL-1
      </text>
    </motion.g>
  );
}
