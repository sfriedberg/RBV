"use client";

import { motion } from "framer-motion";

interface CytochromeCProps {
  x?: number;
  y?: number;
  count?: number;
  streaming?: boolean;
}

export default function CytochromeC({
  x = 0, y = 0,
  count = 6,
  streaming = false,
}: CytochromeCProps) {
  return (
    <g transform={`translate(${x}, ${y})`}>
      {Array.from({ length: count }).map((_, i) => {
        const spreadX = 22 + i * 14 + Math.sin(i * 1.7) * 10;
        const spreadY = -12 + Math.cos(i * 2.3) * 18;

        return (
          <motion.g key={i}>
            {/* Trailing glow */}
            {streaming && (
              <motion.circle
                cx={0} cy={0} r={6}
                fill="var(--color-cytochrome-c)" fillOpacity={0}
                filter="url(#glow-sm)"
                animate={{ cx: spreadX, cy: spreadY, fillOpacity: [0, 0.15, 0] }}
                transition={{ duration: 1.8, delay: i * 0.12, ease: "easeOut" }}
              />
            )}
            {/* Main dot */}
            <motion.circle
              cx={0} cy={0} r={4}
              fill="url(#grad-cytc)"
              stroke="var(--color-cytochrome-c)" strokeWidth={0.6}
              strokeOpacity={0.4}
              initial={{ x: 0, y: 0, opacity: 0 }}
              animate={
                streaming
                  ? { x: spreadX, y: spreadY, opacity: 1 }
                  : { x: 0, y: 0, opacity: 0 }
              }
              transition={{ duration: 1.2, delay: i * 0.12, ease: "easeOut" }}
            />
            {/* Highlight */}
            <motion.circle
              cx={0} cy={0} r={1.5}
              fill="white" fillOpacity={0}
              animate={
                streaming
                  ? { cx: spreadX - 1, cy: spreadY - 1, fillOpacity: 0.2 }
                  : {}
              }
              transition={{ duration: 1.2, delay: i * 0.12 }}
            />
          </motion.g>
        );
      })}
    </g>
  );
}
