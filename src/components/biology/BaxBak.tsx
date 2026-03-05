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
  x = 0, y = 0,
  activated = false,
  progress, activateRange,
  label = "BAX",
}: BaxBakProps) {
  const fallback = useMotionValue(0);
  const hasProgress = !!(progress && activateRange);
  const source = hasProgress ? progress! : fallback;
  const range = hasProgress ? activateRange! : ([0, 1] as [number, number]);

  const fillOpacityMV = useTransform(source, range, [0.3, 1]);
  const scaleMV = useTransform(source, range, [0.8, 1.2]);

  const useMV = hasProgress;
  const fillOpacity = useMV ? fillOpacityMV : activated ? 1 : 0.3;
  const s = useMV ? scaleMV : activated ? 1.2 : 0.8;
  const isActive = activated || hasProgress;

  return (
    <motion.g
      style={{ x, y, scale: s, transformOrigin: "0px 0px" }}
    >
      {/* Activation glow */}
      {isActive && (
        <motion.circle
          cx={0} cy={0} r={18}
          fill="var(--color-bax-bak)" fillOpacity={0.06}
          filter="url(#glow-sm)"
          animate={{ fillOpacity: [0.04, 0.1, 0.04] }}
          transition={{ duration: 1.5, repeat: Infinity }}
        />
      )}
      {/* Channel body */}
      <rect
        x={-11} y={-13} width={22} height={26} rx={5}
        fill="url(#grad-baxbak)"
        stroke="#86efac" strokeWidth={1} strokeOpacity={0.5}
      />
      {fillOpacity instanceof Object && (
        <motion.rect
          x={-11} y={-13} width={22} height={26} rx={5}
          fill="url(#grad-baxbak)"
          style={{ fillOpacity }}
          stroke="#86efac" strokeWidth={1} strokeOpacity={0.5}
        />
      )}
      {/* Inner pore ring when activated */}
      {isActive && (
        <motion.circle
          cx={0} cy={0} r={4}
          fill="none" stroke="white" strokeWidth={0.8}
          initial={{ opacity: 0 }} animate={{ opacity: 0.4 }}
          transition={{ duration: 0.5 }}
        />
      )}
      <text
        x={0} y={3} textAnchor="middle"
        fill="white" fontSize={6} fontWeight="bold"
        fontFamily="var(--font-geist-mono), monospace"
      >
        {label}
      </text>
    </motion.g>
  );
}
