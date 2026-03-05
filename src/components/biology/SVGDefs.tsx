"use client";

/**
 * Shared SVG gradient and filter definitions.
 * Include <SVGDefs /> inside every scene <svg> so all biology
 * components can reference these ids.
 */
export default function SVGDefs() {
  return (
    <defs>
      {/* ── Glow filters ─────────────────────────────────── */}
      <filter id="glow-sm" x="-50%" y="-50%" width="200%" height="200%">
        <feGaussianBlur stdDeviation="3" result="blur" />
        <feMerge>
          <feMergeNode in="blur" />
          <feMergeNode in="SourceGraphic" />
        </feMerge>
      </filter>
      <filter id="glow-md" x="-50%" y="-50%" width="200%" height="200%">
        <feGaussianBlur stdDeviation="6" result="blur" />
        <feMerge>
          <feMergeNode in="blur" />
          <feMergeNode in="SourceGraphic" />
        </feMerge>
      </filter>
      <filter id="glow-lg" x="-80%" y="-80%" width="260%" height="260%">
        <feGaussianBlur stdDeviation="12" result="blur" />
        <feMerge>
          <feMergeNode in="blur" />
          <feMergeNode in="SourceGraphic" />
        </feMerge>
      </filter>
      <filter id="soft-shadow" x="-30%" y="-30%" width="160%" height="160%">
        <feDropShadow dx="0" dy="2" stdDeviation="4" floodColor="#000" floodOpacity="0.4" />
      </filter>

      {/* ── Cell gradients ────────────────────────────────── */}
      <radialGradient id="grad-cytoplasm" cx="50%" cy="45%" r="55%">
        <stop offset="0%" stopColor="var(--color-cell-membrane)" stopOpacity="0.12" />
        <stop offset="70%" stopColor="var(--color-cell-membrane)" stopOpacity="0.04" />
        <stop offset="100%" stopColor="var(--color-cell-membrane)" stopOpacity="0" />
      </radialGradient>
      <radialGradient id="grad-cytoplasm-cancer" cx="50%" cy="45%" r="55%">
        <stop offset="0%" stopColor="var(--color-cancer-cell)" stopOpacity="0.14" />
        <stop offset="70%" stopColor="var(--color-cancer-cell)" stopOpacity="0.05" />
        <stop offset="100%" stopColor="var(--color-cancer-cell)" stopOpacity="0" />
      </radialGradient>
      <radialGradient id="grad-nucleus" cx="40%" cy="38%" r="60%">
        <stop offset="0%" stopColor="#818cf8" stopOpacity="0.6" />
        <stop offset="60%" stopColor="var(--color-nucleus)" stopOpacity="0.35" />
        <stop offset="100%" stopColor="#3730a3" stopOpacity="0.2" />
      </radialGradient>

      {/* ── Protein gradients ─────────────────────────────── */}
      <radialGradient id="grad-bclxl" cx="35%" cy="30%" r="70%">
        <stop offset="0%" stopColor="#fca5a5" stopOpacity="1" />
        <stop offset="50%" stopColor="var(--color-bclxl)" stopOpacity="0.95" />
        <stop offset="100%" stopColor="#991b1b" stopOpacity="0.85" />
      </radialGradient>
      <radialGradient id="grad-baxbak" cx="35%" cy="30%" r="70%">
        <stop offset="0%" stopColor="#86efac" stopOpacity="1" />
        <stop offset="50%" stopColor="var(--color-bax-bak)" stopOpacity="0.9" />
        <stop offset="100%" stopColor="#166534" stopOpacity="0.8" />
      </radialGradient>
      <radialGradient id="grad-bim" cx="40%" cy="35%" r="65%">
        <stop offset="0%" stopColor="#d9f99d" stopOpacity="1" />
        <stop offset="100%" stopColor="#65a30d" stopOpacity="0.85" />
      </radialGradient>
      <radialGradient id="grad-mcl1" cx="40%" cy="30%" r="65%">
        <stop offset="0%" stopColor="#fdba74" stopOpacity="1" />
        <stop offset="60%" stopColor="var(--color-mcl1)" stopOpacity="0.95" />
        <stop offset="100%" stopColor="#9a3412" stopOpacity="0.8" />
      </radialGradient>

      {/* ── Organelle gradients ───────────────────────────── */}
      <radialGradient id="grad-mito" cx="40%" cy="40%" r="60%">
        <stop offset="0%" stopColor="#fcd34d" stopOpacity="0.35" />
        <stop offset="60%" stopColor="var(--color-mitochondria)" stopOpacity="0.2" />
        <stop offset="100%" stopColor="#92400e" stopOpacity="0.1" />
      </radialGradient>

      {/* ── Drug gradients ────────────────────────────────── */}
      <linearGradient id="grad-dt2216" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stopColor="#22d3ee" stopOpacity="1" />
        <stop offset="50%" stopColor="var(--color-dt2216)" stopOpacity="0.9" />
        <stop offset="100%" stopColor="#0e7490" stopOpacity="0.85" />
      </linearGradient>
      <radialGradient id="grad-proteasome" cx="45%" cy="40%" r="55%">
        <stop offset="0%" stopColor="#e879f9" stopOpacity="0.5" />
        <stop offset="100%" stopColor="var(--color-proteasome)" stopOpacity="0.25" />
      </radialGradient>
      <radialGradient id="grad-ubiquitin" cx="40%" cy="35%" r="60%">
        <stop offset="0%" stopColor="#fef08a" stopOpacity="1" />
        <stop offset="100%" stopColor="var(--color-ubiquitin)" stopOpacity="0.9" />
      </radialGradient>

      {/* ── Microtubule gradient ──────────────────────────── */}
      <linearGradient id="grad-tubulin-a" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stopColor="#a78bfa" stopOpacity="1" />
        <stop offset="100%" stopColor="#6d28d9" stopOpacity="0.8" />
      </linearGradient>
      <linearGradient id="grad-tubulin-b" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stopColor="#7c3aed" stopOpacity="0.85" />
        <stop offset="100%" stopColor="#4c1d95" stopOpacity="0.7" />
      </linearGradient>

      {/* ── Paclitaxel gradient ───────────────────────────── */}
      <radialGradient id="grad-paclitaxel" cx="50%" cy="40%" r="55%">
        <stop offset="0%" stopColor="#93c5fd" stopOpacity="1" />
        <stop offset="100%" stopColor="var(--color-paclitaxel)" stopOpacity="0.9" />
      </radialGradient>

      {/* ── Cytochrome c / Apoptosome ─────────────────────── */}
      <radialGradient id="grad-cytc" cx="40%" cy="35%" r="60%">
        <stop offset="0%" stopColor="#fdba74" stopOpacity="1" />
        <stop offset="100%" stopColor="var(--color-cytochrome-c)" stopOpacity="0.9" />
      </radialGradient>
      <radialGradient id="grad-caspase" cx="45%" cy="40%" r="55%">
        <stop offset="0%" stopColor="#fb7185" stopOpacity="1" />
        <stop offset="100%" stopColor="var(--color-caspase)" stopOpacity="0.9" />
      </radialGradient>
    </defs>
  );
}
