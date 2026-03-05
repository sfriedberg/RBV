"use client";

import { useRef } from "react";
import { useScroll, useTransform, useInView, MotionValue } from "framer-motion";

export function useScrollScene(): {
  ref: React.RefObject<HTMLElement | null>;
  progress: MotionValue<number>;
  isInView: boolean;
} {
  const ref = useRef<HTMLElement>(null);

  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start end", "end start"],
  });

  // Remap so 0 = section enters viewport, 1 = section leaves viewport
  const progress = useTransform(scrollYProgress, [0.15, 0.85], [0, 1]);

  const isInView = useInView(ref, { margin: "-10% 0px" });

  return { ref, progress, isInView };
}
