"use client";

import { motion, MotionValue, useTransform, useMotionValue } from "framer-motion";

interface PROTACProps {
  x?: number;
  y?: number;
  progress?: MotionValue<number>;
  enterRange?: [number, number];
}

export default function PROTAC({
  x = 0, y = 0,
  progress, enterRange,
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
      {/* Ambient glow */}
      <motion.ellipse
        cx={0} cy={0} rx={35} ry={16}
        fill="var(--color-dt2216)" fillOpacity={0.06}
        filter="url(#glow-md)"
        animate={{ fillOpacity: [0.04, 0.1, 0.04] }}
        transition={{ duration: 2, repeat: Infinity }}
      />

      {/* BCL-XL binding end */}
      <circle cx={-22} cy={0} r={12}
        fill="url(#grad-dt2216)" stroke="#22d3ee"
        strokeWidth={1} strokeOpacity={0.6} />
      <circle cx={-24} cy={-3} r={4}
        fill="white" fillOpacity={0.1} />
      <text x={-22} y={3} textAnchor="middle"
        fill="white" fontSize={4.5} fontWeight="bold"
        fontFamily="var(--font-geist-mono), monospace">
        Bind
      </text>

      {/* Linker with animated dashes */}
      <motion.line
        x1={-10} y1={0} x2={10} y2={0}
        stroke="var(--color-dt2216)" strokeWidth={2.5}
        strokeDasharray="3 2"
        animate={{ strokeDashoffset: [0, -10] }}
        transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }}
      />

      {/* VHL recruiting end */}
      <circle cx={22} cy={0} r={12}
        fill="url(#grad-dt2216)"
        stroke="#22d3ee" strokeWidth={1} strokeOpacity={0.4}
        opacity={0.75} />
      <circle cx={20} cy={-3} r={4}
        fill="white" fillOpacity={0.08} />
      <text x={22} y={3} textAnchor="middle"
        fill="white" fontSize={4.5} fontWeight="bold"
        fontFamily="var(--font-geist-mono), monospace">
        VHL
      </text>

      {/* DT2216 label */}
      <text x={0} y={-20} textAnchor="middle"
        fill="var(--color-dt2216)" fontSize={7.5} fontWeight="bold"
        fontFamily="var(--font-geist-mono), monospace"
        filter="url(#glow-sm)">
        DT2216
      </text>
    </motion.g>
  );
}
