"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { scenes } from "@/data/scenes";

export default function SceneProgressBar() {
  const [activeScene, setActiveScene] = useState(-1);

  useEffect(() => {
    const observers: IntersectionObserver[] = [];

    scenes.forEach((scene, index) => {
      const el = document.getElementById(scene.id);
      if (!el) return;

      const observer = new IntersectionObserver(
        ([entry]) => {
          if (entry.isIntersecting) {
            setActiveScene(index);
          }
        },
        { threshold: 0.3 }
      );

      observer.observe(el);
      observers.push(observer);
    });

    return () => observers.forEach((o) => o.disconnect());
  }, []);

  return (
    <nav className="fixed right-6 top-1/2 -translate-y-1/2 z-50 hidden lg:flex flex-col items-end gap-4">
      {scenes.map((scene, i) => {
        const isActive = activeScene === i;
        return (
          <button
            key={scene.id}
            onClick={() => {
              document.getElementById(scene.id)?.scrollIntoView({ behavior: "smooth" });
            }}
            className="group relative flex items-center justify-end gap-3"
            aria-label={`Go to ${scene.title}`}
          >
            {/* Hover label */}
            <span className="text-[10px] font-mono tracking-wider opacity-0 group-hover:opacity-80 transition-opacity duration-200 text-[var(--text-muted)] whitespace-nowrap">
              {scene.title}
            </span>

            {/* Dot with connecting line */}
            <div className="relative flex items-center">
              {isActive && (
                <motion.div
                  className="absolute -inset-1.5 rounded-full"
                  style={{ backgroundColor: "var(--text-accent)" }}
                  initial={{ opacity: 0, scale: 0 }}
                  animate={{ opacity: 0.15, scale: 1 }}
                  transition={{ duration: 0.3 }}
                />
              )}
              <motion.div
                className="relative rounded-full"
                animate={{
                  width: isActive ? 10 : 5,
                  height: isActive ? 10 : 5,
                  backgroundColor: isActive
                    ? "var(--text-accent)"
                    : "var(--text-muted)",
                  opacity: isActive ? 1 : 0.4,
                }}
                transition={{ duration: 0.3 }}
              />
            </div>
          </button>
        );
      })}
    </nav>
  );
}
