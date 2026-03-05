"use client";

import { motion } from "framer-motion";

interface MicrotubuleProps {
  x?: number;
  y?: number;
  locked?: boolean;
}

export default function Microtubule({
  x = 0,
  y = 0,
  locked = false,
}: MicrotubuleProps) {
  return (
    <g transform={`translate(${x}, ${y})`}>
      {/* Tubulin subunits - two parallel rows */}
      {Array.from({ length: 8 }).map((_, i) => (
        <g key={i}>
          <motion.rect
            x={i * 14 - 56} y={-8}
            width={12} height={7}
            rx={2}
            fill="var(--color-microtubule)"
            fillOpacity={locked ? 0.9 : 0.5}
            animate={
              !locked
                ? { fillOpacity: [0.3, 0.6, 0.3] }
                : {}
            }
            transition={{
              duration: 1.5,
              delay: i * 0.1,
              repeat: Infinity,
            }}
          />
          <motion.rect
            x={i * 14 - 56} y={2}
            width={12} height={7}
            rx={2}
            fill="var(--color-microtubule)"
            fillOpacity={locked ? 0.7 : 0.4}
            animate={
              !locked
                ? { fillOpacity: [0.2, 0.5, 0.2] }
                : {}
            }
            transition={{
              duration: 1.5,
              delay: i * 0.1 + 0.5,
              repeat: Infinity,
            }}
          />
        </g>
      ))}
      {/* Lock indicator when stabilized */}
      {locked && (
        <motion.g
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
        >
          <rect
            x={-60} y={-12} width={120} height={24}
            rx={4}
            fill="none"
            stroke="var(--color-paclitaxel)"
            strokeWidth={1.5}
            strokeDasharray="4 2"
          />
        </motion.g>
      )}
    </g>
  );
}
