"use client";

import { motion } from "framer-motion";

interface MicrotubuleProps {
  x?: number;
  y?: number;
  locked?: boolean;
}

export default function Microtubule({
  x = 0, y = 0,
  locked = false,
}: MicrotubuleProps) {
  return (
    <g transform={`translate(${x}, ${y})`}>
      {/* Tubulin subunits (alpha/beta heterodimers) */}
      {Array.from({ length: 8 }).map((_, i) => (
        <g key={i}>
          {/* Alpha tubulin */}
          <motion.rect
            x={i * 14 - 56} y={-9} width={12} height={8} rx={2.5}
            fill="url(#grad-tubulin-a)"
            stroke="#a78bfa" strokeWidth={0.6} strokeOpacity={0.4}
            animate={!locked ? { fillOpacity: [0.4, 0.8, 0.4] } : { fillOpacity: 0.95 }}
            transition={{ duration: 1.5, delay: i * 0.1, repeat: Infinity }}
          />
          {/* Beta tubulin */}
          <motion.rect
            x={i * 14 - 56} y={2} width={12} height={8} rx={2.5}
            fill="url(#grad-tubulin-b)"
            stroke="#7c3aed" strokeWidth={0.6} strokeOpacity={0.3}
            animate={!locked ? { fillOpacity: [0.3, 0.7, 0.3] } : { fillOpacity: 0.85 }}
            transition={{ duration: 1.5, delay: i * 0.1 + 0.5, repeat: Infinity }}
          />
        </g>
      ))}

      {/* Lock indicator when stabilized by paclitaxel */}
      {locked && (
        <motion.g
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
        >
          {/* Blue clamping frame */}
          <rect
            x={-62} y={-13} width={124} height={27} rx={5}
            fill="var(--color-paclitaxel)" fillOpacity={0.06}
            stroke="var(--color-paclitaxel)" strokeWidth={1.8}
            strokeDasharray="6 3" strokeOpacity={0.6}
          />
          {/* Lock glow */}
          <rect
            x={-62} y={-13} width={124} height={27} rx={5}
            fill="none" stroke="var(--color-paclitaxel)"
            strokeWidth={4} strokeOpacity={0.08}
            filter="url(#glow-sm)"
          />
        </motion.g>
      )}
    </g>
  );
}
