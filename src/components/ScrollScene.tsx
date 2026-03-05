"use client";

import { useRef } from "react";
import {
  motion,
  useScroll,
  useTransform,
  useInView,
  MotionValue,
} from "framer-motion";

interface ScrollSceneProps {
  id: string;
  index: number;
  bgColor: string;
  children: (props: {
    progress: MotionValue<number>;
    isInView: boolean;
  }) => React.ReactNode;
  title: string;
  subtitle: string;
  paragraphs: string[];
}

export default function ScrollScene({
  id,
  index,
  bgColor,
  children,
  title,
  subtitle,
  paragraphs,
}: ScrollSceneProps) {
  const ref = useRef<HTMLElement>(null);

  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start end", "end start"],
  });

  const progress = useTransform(scrollYProgress, [0.1, 0.9], [0, 1]);
  const isInView = useInView(ref, { margin: "-5% 0px" });

  const textOpacity = useTransform(scrollYProgress, [0.15, 0.3], [0, 1]);
  const textY = useTransform(scrollYProgress, [0.15, 0.3], [40, 0]);

  return (
    <section
      ref={ref}
      id={id}
      className="relative min-h-[200vh] flex items-start justify-center"
      style={{
        background: `radial-gradient(ellipse at center, ${bgColor} 0%, var(--background) 70%)`,
      }}
    >
      <div className="sticky top-0 h-screen w-full max-w-7xl mx-auto flex flex-col lg:flex-row items-center px-6 lg:px-12 gap-8 lg:gap-12">
        {/* Animation area */}
        <div className="flex-1 w-full lg:w-[60%] flex items-center justify-center min-h-[40vh] lg:min-h-0">
          {children({ progress, isInView })}
        </div>

        {/* Text panel */}
        <motion.div
          className="flex-1 w-full lg:w-[40%] flex flex-col gap-4 pb-12 lg:pb-0"
          style={{ opacity: textOpacity, y: textY }}
        >
          <div className="flex items-center gap-3 mb-2">
            <span className="text-xs font-mono tracking-widest uppercase text-[var(--text-muted)]">
              {String(index + 1).padStart(2, "0")}
            </span>
            <div className="h-px flex-1 bg-gradient-to-r from-[var(--text-muted)]/30 to-transparent" />
          </div>
          <h2 className="text-3xl lg:text-4xl font-bold tracking-tight">
            {title}
          </h2>
          <p className="text-lg text-[var(--text-accent)] font-medium">
            {subtitle}
          </p>
          <div className="flex flex-col gap-4 mt-2">
            {paragraphs.map((p, i) => (
              <p key={i} className="text-base leading-relaxed text-[var(--text-muted)]">
                {p}
              </p>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
}
