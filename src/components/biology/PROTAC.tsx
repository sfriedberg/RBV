"use client";

import { motion, MotionValue, useTransform, useMotionValue } from "framer-motion";

interface PROTACProps {
  x?: number;
  y?: number;
  progress?: MotionValue<number>;
  enterRange?: [number, number];
}

export default function PROTAC({
  x = 0,
  y = 0,
  progress,
  enterRange,
}: PROTACProps) {
  const fallback = useMotionValue(0);
  const hasProgress = !!(progress && enterRange);
  const source = hasProgress ? progress! : fallback;
  const fadeStart = hasProgress ? enterRange![0] : 0;
  const enterStart = hasProgress ? enterRange![0] : 0;
  const enterEnd = hasProgress ? enterRange![1] : 1;

  const opacityMV = useTransform(source, [fadeStart, fadeStart + 0.05], [0, 1]);
  const xPosMV = useTransform(source, [enterStart, enterEnd], [x - 80, x]);

  const opacity = hasProgress ? opacityMV : 1;
  const xPos = hasProgress ? xPosMV : x;

  return (
    <motion.g style={{ x: xPos, y, opacity }}>
      {/* BCL-XL binding end */}
      <circle
        cx={-20} cy={0} r={10}
        fill="var(--color-dt2216)"
        fillOpacity={0.9}
        stroke="var(--color-dt2216)"
        strokeWidth={1.5}
      />
      <text
        x={-20} y={3}
        textAnchor="middle"
        fill="white"
        fontSize={4}
        fontFamily="var(--font-geist-mono), monospace"
      >
        Bind
      </text>
      {/* Linker */}
      <line
        x1={-10} y1={0} x2={10} y2={0}
        stroke="var(--color-dt2216)"
        strokeWidth={2}
        strokeDasharray="3 2"
      />
      {/* VHL recruiting end */}
      <circle
        cx={20} cy={0} r={10}
        fill="var(--color-dt2216)"
        fillOpacity={0.6}
        stroke="var(--color-dt2216)"
        strokeWidth={1.5}
      />
      <text
        x={20} y={3}
        textAnchor="middle"
        fill="white"
        fontSize={4}
        fontFamily="var(--font-geist-mono), monospace"
      >
        VHL
      </text>
      {/* DT2216 label */}
      <text
        x={0} y={-18}
        textAnchor="middle"
        fill="var(--color-dt2216)"
        fontSize={7}
        fontWeight="bold"
        fontFamily="var(--font-geist-mono), monospace"
      >
        DT2216
      </text>
    </motion.g>
  );
}
