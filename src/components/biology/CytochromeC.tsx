"use client";

import { motion } from "framer-motion";

interface CytochromeCProps {
  x?: number;
  y?: number;
  count?: number;
  streaming?: boolean;
}

export default function CytochromeC({
  x = 0,
  y = 0,
  count = 6,
  streaming = false,
}: CytochromeCProps) {
  return (
    <g transform={`translate(${x}, ${y})`}>
      {Array.from({ length: count }).map((_, i) => (
        <motion.circle
          key={i}
          cx={0} cy={0} r={3.5}
          fill="var(--color-cytochrome-c)"
          fillOpacity={0.9}
          initial={{ x: 0, y: 0, opacity: 0 }}
          animate={
            streaming
              ? {
                  x: 20 + i * 12 + Math.sin(i) * 8,
                  y: -10 + Math.cos(i * 2) * 15,
                  opacity: 1,
                }
              : { x: 0, y: 0, opacity: 0 }
          }
          transition={{
            duration: 1.2,
            delay: i * 0.15,
            ease: "easeOut",
          }}
        />
      ))}
    </g>
  );
}
