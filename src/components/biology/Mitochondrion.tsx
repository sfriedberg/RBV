"use client";

import { motion } from "framer-motion";

interface MitochondrionProps {
  x?: number;
  y?: number;
  scale?: number;
  showPore?: boolean;
}

export default function Mitochondrion({
  x = 0, y = 0,
  scale = 1,
  showPore = false,
}: MitochondrionProps) {
  return (
    <g transform={`translate(${x}, ${y}) scale(${scale})`}>
      {/* Ambient glow */}
      <ellipse
        cx={0} cy={0} rx={62} ry={36}
        fill="var(--color-mitochondria)" fillOpacity={0.05}
        filter="url(#glow-md)"
      />
      {/* Outer membrane */}
      <ellipse
        cx={0} cy={0} rx={55} ry={30}
        fill="url(#grad-mito)"
        stroke="var(--color-mitochondria)" strokeWidth={2.2}
      />
      {/* Inner membrane */}
      <ellipse
        cx={0} cy={0} rx={49} ry={25}
        fill="none"
        stroke="var(--color-mitochondria)" strokeWidth={0.8} opacity={0.35}
      />
      {/* Cristae folds (more detailed) */}
      <path
        d="M-35,-6 Q-25,12 -15,-4 Q-5,14 5,-4 Q15,12 25,-4 Q35,8 38,-2"
        fill="none" stroke="var(--color-mitochondria)"
        strokeWidth={1.3} opacity={0.55}
      />
      <path
        d="M-30,6 Q-20,-8 -10,6 Q0,-8 10,6 Q20,-8 30,6"
        fill="none" stroke="var(--color-mitochondria)"
        strokeWidth={1} opacity={0.35}
      />
      {/* Matrix granules */}
      {[[-20, -2], [5, 5], [22, -4], [-8, -8]].map(([gx, gy], i) => (
        <circle
          key={i} cx={gx} cy={gy} r={1.2}
          fill="var(--color-mitochondria)" fillOpacity={0.4}
        />
      ))}
      {/* Pore opening */}
      {showPore && (
        <motion.g
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          <motion.ellipse
            cx={42} cy={0} rx={4} ry={12}
            fill="var(--color-cytochrome-c)" fillOpacity={0.2}
            animate={{ fillOpacity: [0.1, 0.3, 0.1] }}
            transition={{ duration: 1.2, repeat: Infinity }}
          />
          <motion.line
            x1={42} y1={-14} x2={42} y2={14}
            stroke="var(--color-cytochrome-c)" strokeWidth={3}
            strokeLinecap="round"
            animate={{ opacity: [0.4, 1, 0.4] }}
            transition={{ duration: 1.5, repeat: Infinity }}
          />
        </motion.g>
      )}
    </g>
  );
}
