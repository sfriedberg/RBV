"use client";

import { motion } from "framer-motion";

export default function Hero() {
  return (
    <section className="relative h-screen flex flex-col items-center justify-center px-6 overflow-hidden">
      {/* Background glow layers */}
      <div className="absolute inset-0 overflow-hidden">
        <div
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[900px] h-[900px] rounded-full opacity-[0.12]"
          style={{
            background:
              "radial-gradient(circle, var(--color-dt2216) 0%, transparent 55%)",
          }}
        />
        <div
          className="absolute top-[40%] left-[60%] -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full opacity-[0.08]"
          style={{
            background:
              "radial-gradient(circle, var(--color-paclitaxel) 0%, transparent 65%)",
          }}
        />
        <div
          className="absolute top-[55%] left-[35%] -translate-x-1/2 -translate-y-1/2 w-[400px] h-[400px] rounded-full opacity-[0.06]"
          style={{
            background:
              "radial-gradient(circle, var(--color-bax-bak) 0%, transparent 70%)",
          }}
        />
      </div>

      {/* Floating biological shapes background */}
      <svg
        className="absolute inset-0 w-full h-full opacity-[0.06]"
        viewBox="0 0 1000 600"
        preserveAspectRatio="xMidYMid slice"
      >
        {/* Cell membrane */}
        <motion.circle
          cx={200} cy={150} r={60}
          fill="none" stroke="var(--color-cell-membrane)" strokeWidth={1.5}
          strokeDasharray="8 4"
          animate={{ cy: [150, 130, 150], rotate: [0, 5, 0] }}
          transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
        />
        {/* BCL-XL shield */}
        <motion.g
          animate={{ y: [0, 12, 0] }}
          transition={{ duration: 6, repeat: Infinity, ease: "easeInOut" }}
        >
          <path
            d="M750,400 L770,390 L768,415 L750,422 L732,415 L730,390 Z"
            fill="none" stroke="var(--color-bclxl)" strokeWidth={1}
          />
        </motion.g>
        {/* Mitochondria */}
        <motion.ellipse
          cx={500} cy={300} rx={80} ry={50}
          fill="none" stroke="var(--color-mitochondria)" strokeWidth={0.8}
          animate={{ cy: [300, 288, 300] }}
          transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
        />
        <motion.path
          d="M440,300 Q460,280 480,300 Q500,280 520,300 Q540,280 560,300"
          fill="none" stroke="var(--color-mitochondria)" strokeWidth={0.5} opacity={0.5}
          animate={{ y: [0, -5, 0] }}
          transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
        />
        {/* DT2216 PROTAC dumbbell */}
        <motion.g
          animate={{ x: [0, 15, 0], y: [0, -8, 0] }}
          transition={{ duration: 7, repeat: Infinity, ease: "easeInOut" }}
        >
          <circle cx={130} cy={420} r={12} fill="none" stroke="var(--color-dt2216)" strokeWidth={0.8} />
          <line x1={142} y1={420} x2={158} y2={420} stroke="var(--color-dt2216)" strokeWidth={0.8} strokeDasharray="3 2" />
          <circle cx={170} cy={420} r={12} fill="none" stroke="var(--color-dt2216)" strokeWidth={0.8} />
        </motion.g>
        {/* Ubiquitin beads */}
        <motion.g
          animate={{ y: [0, -10, 0] }}
          transition={{ duration: 5, repeat: Infinity, ease: "easeInOut" }}
        >
          {[0, 1, 2, 3].map(i => (
            <circle key={i} cx={850 + i * 14} cy={200} r={5}
              fill="none" stroke="var(--color-ubiquitin)" strokeWidth={0.6} />
          ))}
        </motion.g>
        {/* DNA helix hint */}
        <motion.path
          d="M820,80 Q830,100 820,120 Q810,140 820,160"
          fill="none" stroke="var(--color-nucleus)" strokeWidth={0.6}
          animate={{ x: [0, 5, 0] }}
          transition={{ duration: 9, repeat: Infinity, ease: "easeInOut" }}
        />
        <motion.path
          d="M825,80 Q815,100 825,120 Q835,140 825,160"
          fill="none" stroke="var(--color-nucleus)" strokeWidth={0.6}
          animate={{ x: [0, -5, 0] }}
          transition={{ duration: 9, repeat: Infinity, ease: "easeInOut" }}
        />
      </svg>

      <motion.div
        className="relative z-10 text-center max-w-3xl"
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1, ease: "easeOut" }}
      >
        <motion.p
          className="text-[11px] font-mono tracking-[0.4em] uppercase text-[var(--text-muted)] mb-8 opacity-70"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.7 }}
          transition={{ delay: 0.3, duration: 0.8 }}
        >
          Dialectic Therapeutics
        </motion.p>

        <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold tracking-tight leading-[1.08] mb-8">
          How{" "}
          <span className="text-[var(--color-dt2216)]">DT2216</span>
          {" "}+{" "}
          <span className="text-[var(--color-paclitaxel)]">Paclitaxel</span>
          <br />
          Kill Cancer Cells
        </h1>

        <motion.p
          className="text-lg md:text-xl text-[var(--text-muted)] max-w-2xl mx-auto leading-relaxed"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 0.8 }}
        >
          An animated guide to understanding how a next-generation PROTAC degrader
          removes cancer&apos;s survival shield and restores the power of apoptosis.
        </motion.p>

        {/* Subtle mechanism hint below subtitle */}
        <motion.div
          className="flex items-center justify-center gap-4 mt-10"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.0, duration: 0.8 }}
        >
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-[var(--color-paclitaxel)]" />
            <span className="text-xs text-[var(--text-muted)] font-mono">MCL-1 depletion</span>
          </div>
          <span className="text-[var(--text-muted)] opacity-30">+</span>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-[var(--color-dt2216)]" />
            <span className="text-xs text-[var(--text-muted)] font-mono">BCL-XL degradation</span>
          </div>
          <span className="text-[var(--text-muted)] opacity-30">→</span>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-[var(--color-bax-bak)]" />
            <span className="text-xs text-[var(--text-muted)] font-mono">Apoptosis</span>
          </div>
        </motion.div>
      </motion.div>

      {/* Scroll indicator */}
      <motion.div
        className="absolute bottom-8 flex flex-col items-center gap-2"
        animate={{ y: [0, 8, 0] }}
        transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
      >
        <span className="text-[10px] text-[var(--text-muted)] tracking-[0.2em] uppercase opacity-50">
          Scroll to explore
        </span>
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
          <path
            d="M4 7 L10 13 L16 7"
            stroke="var(--text-muted)"
            strokeWidth="1.5"
            strokeLinecap="round"
            strokeLinejoin="round"
            opacity="0.4"
          />
        </svg>
      </motion.div>
    </section>
  );
}
