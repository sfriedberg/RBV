"use client";

import { motion } from "framer-motion";

interface ParticleEffectProps {
  x: number;
  y: number;
  active?: boolean;
  count?: number;
  color?: string;
}

export default function ParticleEffect({
  x, y,
  active = false,
  count = 12,
  color = "var(--color-cancer-cell)",
}: ParticleEffectProps) {
  if (!active) return null;

  return (
    <g>
      {Array.from({ length: count }).map((_, i) => {
        const angle = (i / count) * Math.PI * 2;
        const dist = 45 + Math.random() * 70;
        const targetX = x + Math.cos(angle) * dist;
        const targetY = y + Math.sin(angle) * dist;
        const size = 2 + Math.random() * 3;

        return (
          <motion.g key={i}>
            {/* Trailing glow */}
            <motion.circle
              cx={x} cy={y} r={size + 3}
              fill={color} fillOpacity={0}
              filter="url(#glow-sm)"
              animate={{ cx: targetX, cy: targetY, fillOpacity: [0, 0.15, 0] }}
              transition={{ duration: 1.8 + Math.random(), delay: i * 0.04, ease: "easeOut" }}
            />
            {/* Particle */}
            <motion.circle
              cx={x} cy={y} r={size}
              fill={color} fillOpacity={0.8}
              initial={{ cx: x, cy: y, opacity: 0.9 }}
              animate={{ cx: targetX, cy: targetY, opacity: 0, r: 0.5 }}
              transition={{ duration: 1.5 + Math.random(), delay: i * 0.04, ease: "easeOut" }}
            />
          </motion.g>
        );
      })}
    </g>
  );
}
