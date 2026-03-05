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
      <footer className="text-center py-12 text-sm text-[var(--text-muted)] border-t border-white/5">
        <p className="mb-2">
          <span className="text-[var(--text-accent)]">Dialectic Therapeutics</span>
        </p>
        <p className="max-w-lg mx-auto text-xs leading-relaxed opacity-60">
          This is an educational visualization. Biological shapes are schematic
          representations, not molecular-scale models. For clinical information,
          consult published research and clinical trial data.
        </p>
      </footer>
    </main>
  );
}
