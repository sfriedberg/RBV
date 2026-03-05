"use client";

import { motion } from "framer-motion";

interface MitochondrionProps {
  x?: number;
  y?: number;
  scale?: number;
  showPore?: boolean;
}

export default function Mitochondrion({
  x = 0,
  y = 0,
  scale = 1,
  showPore = false,
}: MitochondrionProps) {
  return (
    <g transform={`translate(${x}, ${y}) scale(${scale})`}>
      {/* Outer membrane */}
      <ellipse
        cx={0} cy={0} rx={55} ry={30}
        fill="var(--color-mitochondria)"
        fillOpacity={0.15}
        stroke="var(--color-mitochondria)"
        strokeWidth={2}
      />
      {/* Cristae (inner folds) */}
      <path
        d="M-30,-8 Q-20,10 -10,-5 Q0,10 10,-5 Q20,10 30,-8"
        fill="none"
        stroke="var(--color-mitochondria)"
        strokeWidth={1.2}
        opacity={0.6}
      />
      <path
        d="M-25,8 Q-15,-5 -5,8 Q5,-5 15,8 Q25,-5 25,8"
        fill="none"
        stroke="var(--color-mitochondria)"
        strokeWidth={1}
        opacity={0.4}
      />
      {/* Pore opening */}
      {showPore && (
        <motion.g
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          <motion.line
            x1={40} y1={-15} x2={40} y2={15}
            stroke="var(--color-cytochrome-c)"
            strokeWidth={3}
            strokeLinecap="round"
            animate={{ opacity: [0.4, 1, 0.4] }}
            transition={{ duration: 1.5, repeat: Infinity }}
          />
        </motion.g>
      )}
    </g>
  );
}
