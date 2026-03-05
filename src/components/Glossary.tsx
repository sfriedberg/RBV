"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { glossaryTerms } from "@/data/glossary";

export default function Glossary() {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  return (
    <section className="max-w-3xl mx-auto px-6 py-28" id="glossary">
      <div className="flex items-center gap-4 mb-3">
        <span className="text-[10px] font-mono tracking-[0.35em] uppercase text-[var(--text-muted)] opacity-60">
          REFERENCE
        </span>
        <div className="h-px flex-1 bg-gradient-to-r from-[var(--text-accent)]/20 to-transparent" />
      </div>
      <h2 className="text-3xl lg:text-4xl font-bold tracking-tight mb-2">Glossary</h2>
      <p className="text-[var(--text-muted)] text-[15px] mb-10">
        Key terms used throughout this guide.
      </p>
      <div className="flex flex-col">
        {glossaryTerms.map((item, i) => (
          <div key={item.term} className="border-b border-white/[0.06]">
            <button
              onClick={() => setOpenIndex(openIndex === i ? null : i)}
              className="w-full flex items-center justify-between py-5 text-left group"
            >
              <span className="font-semibold text-[17px] group-hover:text-[var(--text-accent)] transition-colors duration-200">
                {item.term}
              </span>
              <motion.span
                animate={{ rotate: openIndex === i ? 45 : 0 }}
                transition={{ duration: 0.2 }}
                className="text-[var(--text-muted)] text-lg opacity-40 group-hover:opacity-80 transition-opacity"
              >
                +
              </motion.span>
            </button>
            <AnimatePresence>
              {openIndex === i && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.25 }}
                  className="overflow-hidden"
                >
                  <p className="pb-5 text-[var(--text-muted)] text-[15px] leading-[1.75] pl-5 border-l border-[var(--text-accent)]/20 ml-1">
                    {item.definition}
                  </p>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        ))}
      </div>
    </section>
  );
}
