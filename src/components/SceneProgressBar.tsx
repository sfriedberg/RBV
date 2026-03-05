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
    <nav className="fixed right-4 top-1/2 -translate-y-1/2 z-50 hidden lg:flex flex-col gap-3">
      {scenes.map((scene, i) => (
        <button
          key={scene.id}
          onClick={() => {
            document.getElementById(scene.id)?.scrollIntoView({ behavior: "smooth" });
          }}
          className="group relative flex items-center justify-end gap-3"
          aria-label={`Go to ${scene.title}`}
        >
          <span className="text-xs font-mono opacity-0 group-hover:opacity-100 transition-opacity text-[var(--text-muted)] whitespace-nowrap">
            {scene.title}
          </span>
          <motion.div
            className="rounded-full"
            animate={{
              width: activeScene === i ? 12 : 6,
              height: activeScene === i ? 12 : 6,
              backgroundColor:
                activeScene === i ? "var(--text-accent)" : "var(--text-muted)",
            }}
            transition={{ duration: 0.3 }}
          />
        </button>
      ))}
    </nav>
  );
}
