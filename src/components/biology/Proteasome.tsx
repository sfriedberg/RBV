"use client";

import { motion } from "framer-motion";

interface ProteasomeProps {
  x?: number;
  y?: number;
  active?: boolean;
}

export default function Proteasome({
  x = 0, y = 0,
  active = false,
}: ProteasomeProps) {
  return (
    <g transform={`translate(${x}, ${y})`}>
      {/* Background glow */}
      <motion.circle
        cx={0} cy={0} r={40}
        fill="var(--color-proteasome)" fillOpacity={0.04}
        filter="url(#glow-lg)"
        animate={active ? { fillOpacity: [0.03, 0.08, 0.03] } : {}}
        transition={{ duration: 1, repeat: Infinity }}
      />

      {/* Barrel body */}
      <motion.rect
        x={-20} y={-28} width={40} height={56} rx={10}
        fill="url(#grad-proteasome)"
        stroke="var(--color-proteasome)" strokeWidth={2}
        animate={active ? { fillOpacity: [0.8, 1, 0.8] } : {}}
        transition={{ duration: 0.8, repeat: Infinity }}
      />

      {/* Barrel rings (alpha/beta subunits) */}
      {[-16, -6, 4, 14].map((ry, i) => (
        <line key={i} x1={-16} y1={ry} x2={16} y2={ry}
          stroke="var(--color-proteasome)" strokeWidth={1.2}
          opacity={0.4 + i * 0.05} />
      ))}

      {/* End caps */}
      <ellipse cx={0} cy={-28} rx={20} ry={5}
        fill="var(--color-proteasome)" fillOpacity={0.3}
        stroke="var(--color-proteasome)" strokeWidth={1} strokeOpacity={0.4} />
      <ellipse cx={0} cy={28} rx={20} ry={5}
        fill="var(--color-proteasome)" fillOpacity={0.2}
        stroke="var(--color-proteasome)" strokeWidth={1} strokeOpacity={0.3} />

      {/* Active state: chewing particles */}
      {active && (
        <>
          {[0, 1, 2].map((i) => (
            <motion.circle
              key={i}
              cx={0} cy={35 + i * 8} r={2}
              fill="var(--color-bclxl)" fillOpacity={0.6}
              animate={{
                cy: [35, 50 + i * 10],
                opacity: [0.6, 0],
                r: [2, 0.5],
              }}
              transition={{
                duration: 1.2,
                delay: i * 0.2,
                repeat: Infinity,
              }}
            />
          ))}
        </>
      )}

      {/* Label */}
      <text x={0} y={42} textAnchor="middle"
        fill="var(--color-proteasome)" fontSize={6}
        fontFamily="var(--font-geist-mono), monospace">
        Proteasome
      </text>
    </g>
  );
}
