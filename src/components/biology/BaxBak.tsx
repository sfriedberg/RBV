"use client";

import { motion, MotionValue, useTransform, useMotionValue } from "framer-motion";

interface BaxBakProps {
  x?: number;
  y?: number;
  activated?: boolean;
  progress?: MotionValue<number>;
  activateRange?: [number, number];
  label?: string;
}

export default function BaxBak({
  x = 0,
  y = 0,
  activated = false,
  progress,
  activateRange,
  label = "BAX",
}: BaxBakProps) {
  const fallback = useMotionValue(0);
  const hasProgress = !!(progress && activateRange);
  const source = hasProgress ? progress! : fallback;
  const range = hasProgress ? activateRange! : [0, 1] as [number, number];

  const fillOpacityMV = useTransform(source, range, [0.3, 1]);
  const scaleMV = useTransform(source, range, [0.8, 1.2]);

  const useMV = hasProgress;
  const fillOpacity = useMV ? fillOpacityMV : (activated ? 1 : 0.3);
  const s = useMV ? scaleMV : (activated ? 1.2 : 0.8);

  return (
    <motion.g
      style={{
        x, y,
        scale: s,
        transformOrigin: "0px 0px",
      }}
    >
      <rect
        x={-10} y={-12} width={20} height={24}
        rx={4}
        fill="var(--color-bax-bak)"
        fillOpacity={typeof fillOpacity === "number" ? fillOpacity : undefined}
        stroke="var(--color-bax-bak)"
        strokeWidth={1.5}
      />
      {fillOpacity instanceof Object && (
        <motion.rect
          x={-10} y={-12} width={20} height={24}
          rx={4}
          fill="var(--color-bax-bak)"
          style={{ fillOpacity }}
          stroke="var(--color-bax-bak)"
          strokeWidth={1.5}
        />
      )}
      <text
        x={0} y={3}
        textAnchor="middle"
        fill="white"
        fontSize={6}
        fontWeight="bold"
        fontFamily="var(--font-geist-mono), monospace"
      >
        {label}
      </text>
    </motion.g>
  );
}
