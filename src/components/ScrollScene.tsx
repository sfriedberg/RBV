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

  const textOpacity = useTransform(scrollYProgress, [0.12, 0.25], [0, 1]);
  const textY = useTransform(scrollYProgress, [0.12, 0.25], [30, 0]);

  return (
    <section
      ref={ref}
      id={id}
      className="relative min-h-[200vh] flex items-start justify-center"
      style={{
        background: `radial-gradient(ellipse at center, ${bgColor} 0%, var(--background) 70%)`,
      }}
    >
      <div className="sticky top-0 h-screen w-full max-w-7xl mx-auto flex flex-col lg:flex-row items-center px-6 lg:px-16 gap-8 lg:gap-16">
        {/* Animation area */}
        <div className="flex-1 w-full lg:w-[58%] flex items-center justify-center min-h-[40vh] lg:min-h-0">
          {children({ progress, isInView })}
        </div>

        {/* Text panel */}
        <motion.div
          className="flex-1 w-full lg:w-[42%] flex flex-col pb-12 lg:pb-0"
          style={{ opacity: textOpacity, y: textY }}
        >
          {/* Scene number and accent line */}
          <div className="flex items-center gap-4 mb-5">
            <span className="text-[10px] font-mono tracking-[0.35em] uppercase text-[var(--text-muted)] opacity-60">
              {String(index + 1).padStart(2, "0")}
            </span>
            <div className="h-px flex-1 bg-gradient-to-r from-[var(--text-accent)]/20 to-transparent" />
          </div>

          {/* Title */}
          <h2 className="text-3xl lg:text-[2.5rem] font-bold tracking-tight leading-[1.15] mb-3">
            {title}
          </h2>

          {/* Subtitle */}
          <p className="text-base lg:text-lg text-[var(--text-accent)] font-medium mb-6 tracking-wide">
            {subtitle}
          </p>

          {/* Paragraphs with left accent bar */}
          <div className="relative flex flex-col gap-5 pl-5 border-l border-white/[0.06]">
            {paragraphs.map((p, i) => (
              <motion.p
                key={i}
                className="text-[15px] leading-[1.75] text-[var(--text-muted)]"
                initial={{ opacity: 0, y: 12 }}
                animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 12 }}
                transition={{ duration: 0.6, delay: 0.3 + i * 0.15, ease: "easeOut" }}
              >
                {p}
              </motion.p>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
}
