"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { glossaryTerms } from "@/data/glossary";

export default function Glossary() {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  return (
    <section className="max-w-4xl mx-auto px-6 py-24" id="glossary">
      <h2 className="text-3xl font-bold mb-2">Glossary</h2>
      <p className="text-[var(--text-muted)] mb-10">
        Key terms used in this guide.
      </p>
      <div className="flex flex-col divide-y divide-white/10">
        {glossaryTerms.map((item, i) => (
          <div key={item.term}>
            <button
              onClick={() => setOpenIndex(openIndex === i ? null : i)}
              className="w-full flex items-center justify-between py-4 text-left group"
            >
              <span className="font-semibold text-lg group-hover:text-[var(--text-accent)] transition-colors">
                {item.term}
              </span>
              <motion.span
                animate={{ rotate: openIndex === i ? 45 : 0 }}
                transition={{ duration: 0.2 }}
                className="text-[var(--text-muted)] text-xl"
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
                  <p className="pb-4 text-[var(--text-muted)] leading-relaxed pl-2 border-l-2 border-[var(--text-accent)]/30 ml-1">
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
