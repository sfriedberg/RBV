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
  x,
  y,
  active = false,
  count = 12,
  color = "var(--color-cancer-cell)",
}: ParticleEffectProps) {
  if (!active) return null;

  return (
    <g>
      {Array.from({ length: count }).map((_, i) => {
        const angle = (i / count) * Math.PI * 2;
        const dist = 40 + Math.random() * 60;
        const targetX = x + Math.cos(angle) * dist;
        const targetY = y + Math.sin(angle) * dist;

        return (
          <motion.circle
            key={i}
            cx={x}
            cy={y}
            r={2 + Math.random() * 3}
            fill={color}
            fillOpacity={0.7}
            initial={{ cx: x, cy: y, opacity: 0.8 }}
            animate={{
              cx: targetX,
              cy: targetY,
              opacity: 0,
              r: 0.5,
            }}
            transition={{
              duration: 1.5 + Math.random(),
              delay: i * 0.05,
              ease: "easeOut",
            }}
          />
        );
      })}
    </g>
  );
}
