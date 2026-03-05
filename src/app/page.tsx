import Hero from "@/components/Hero";
import SceneProgressBar from "@/components/SceneProgressBar";
import Glossary from "@/components/Glossary";
import { scenes } from "@/data/scenes";
import SceneWrapper from "@/components/SceneWrapper";

export default function Home() {
  return (
    <main className="relative">
      <Hero />

      {scenes.map((scene) => (
        <SceneWrapper key={scene.id} scene={scene} />
      ))}

      <Glossary />
      <SceneProgressBar />

      {/* Footer */}
      <footer className="relative text-center py-16 text-sm border-t border-white/[0.04]">
        <div className="max-w-lg mx-auto px-6">
          <p className="text-[var(--text-accent)] font-semibold tracking-wide text-[13px] mb-3">
            Dialectic Therapeutics
          </p>
          <p className="text-[12px] leading-[1.8] text-[var(--text-muted)] opacity-50">
            This is an educational visualization. Biological shapes are schematic
            representations, not molecular-scale models. For clinical information,
            consult published research and clinical trial data.
          </p>
        </div>
      </footer>
    </main>
  );
}
