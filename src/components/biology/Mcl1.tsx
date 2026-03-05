"use client";

import { motion, MotionValue, useTransform, useMotionValue } from "framer-motion";

interface Mcl1Props {
  x?: number;
  y?: number;
  progress?: MotionValue<number>;
  degradeRange?: [number, number];
}

export default function Mcl1({
  x = 0, y = 0,
  progress, degradeRange,
}: Mcl1Props) {
  const fallback = useMotionValue(0);
  const hasProgress = !!(progress && degradeRange);
  const source = hasProgress ? progress! : fallback;
  const range = hasProgress ? degradeRange! : ([0, 1] as [number, number]);

  const opacityMV = useTransform(source, range, [1, 0]);
  const scaleMV = useTransform(source, range, [1, 0]);

  const opacity = hasProgress ? opacityMV : 1;
  const scale = hasProgress ? scaleMV : 1;

  return (
    <motion.g
      style={{ x, y, opacity, scale, transformOrigin: "0px 0px" }}
    >
      {/* Glow */}
      <circle
        cx={0} cy={0} r={20}
        fill="var(--color-mcl1)" fillOpacity={0.06}
        filter="url(#glow-sm)"
      />
      {/* Triangle shield */}
      <polygon
        points="0,-16 14,11 -14,11"
        fill="url(#grad-mcl1)"
        stroke="#fdba74" strokeWidth={1} strokeOpacity={0.5}
      />
      {/* Inner highlight */}
      <polygon
        points="0,-10 8,7 -8,7"
        fill="none" stroke="white" strokeWidth={0.4} strokeOpacity={0.15}
      />
      <text
        x={0} y={5} textAnchor="middle"
        fill="white" fontSize={5.5} fontWeight="bold"
        fontFamily="var(--font-geist-mono), monospace"
      >
        MCL-1
      </text>
    </motion.g>
  );
}
