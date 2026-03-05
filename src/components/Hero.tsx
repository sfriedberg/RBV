"use client";

import { motion } from "framer-motion";

export default function Hero() {
  return (
    <section className="relative h-screen flex flex-col items-center justify-center px-6 overflow-hidden">
      {/* Background glow */}
      <div className="absolute inset-0 overflow-hidden">
        <div
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] rounded-full opacity-20"
          style={{
            background:
              "radial-gradient(circle, var(--color-dt2216) 0%, transparent 70%)",
          }}
        />
      </div>

      {/* Floating cell shapes background */}
      <svg
        className="absolute inset-0 w-full h-full opacity-10"
        viewBox="0 0 1000 600"
        preserveAspectRatio="xMidYMid slice"
      >
        <motion.circle
          cx={200} cy={150} r={60}
          fill="none" stroke="var(--color-cell-membrane)" strokeWidth={1}
          animate={{ y: [0, -20, 0], rotate: [0, 5, 0] }}
          transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
        />
        <motion.circle
          cx={750} cy={400} r={45}
          fill="none" stroke="var(--color-bclxl)" strokeWidth={1}
          animate={{ y: [0, 15, 0], rotate: [0, -3, 0] }}
          transition={{ duration: 6, repeat: Infinity, ease: "easeInOut" }}
        />
        <motion.ellipse
          cx={500} cy={300} rx={80} ry={50}
          fill="none" stroke="var(--color-mitochondria)" strokeWidth={0.5}
          animate={{ y: [0, -10, 0] }}
          transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
        />
      </svg>

      <motion.div
        className="relative z-10 text-center max-w-3xl"
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1, ease: "easeOut" }}
      >
        <p className="text-sm font-mono tracking-[0.3em] uppercase text-[var(--text-muted)] mb-6">
          Dialectic Therapeutics
        </p>
        <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold tracking-tight leading-[1.1] mb-6">
          How{" "}
          <span className="text-[var(--color-dt2216)]">DT2216</span>
          {" "}+{" "}
          <span className="text-[var(--color-paclitaxel)]">Paclitaxel</span>
          <br />
          Kill Cancer Cells
        </h1>
        <p className="text-lg md:text-xl text-[var(--text-muted)] max-w-2xl mx-auto leading-relaxed">
          An animated guide to understanding how a next-generation PROTAC degrader
          removes cancer&apos;s survival shield and restores the power of apoptosis.
        </p>
      </motion.div>

      {/* Scroll indicator */}
      <motion.div
        className="absolute bottom-8 flex flex-col items-center gap-2"
        animate={{ y: [0, 8, 0] }}
        transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
      >
        <span className="text-xs text-[var(--text-muted)] tracking-widest uppercase">
          Scroll to explore
        </span>
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
          <path
            d="M4 7 L10 13 L16 7"
            stroke="var(--text-muted)"
            strokeWidth="1.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </motion.div>
    </section>
  );
}
