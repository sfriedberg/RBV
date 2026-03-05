"use client";

import ScrollScene from "@/components/ScrollScene";
import Scene1Apoptosis from "@/components/scenes/Scene1Apoptosis";
import Scene2CancerSurvival from "@/components/scenes/Scene2CancerSurvival";
import Scene3Paclitaxel from "@/components/scenes/Scene3Paclitaxel";
import Scene4DT2216 from "@/components/scenes/Scene4DT2216";
import Scene5Combination from "@/components/scenes/Scene5Combination";
import Scene6Clinical from "@/components/scenes/Scene6Clinical";
import type { SceneData } from "@/data/scenes";

const SCENE_BG_COLORS = [
  "var(--scene-1-bg)",
  "var(--scene-2-bg)",
  "var(--scene-3-bg)",
  "var(--scene-4-bg)",
  "var(--scene-5-bg)",
  "var(--scene-6-bg)",
];

const SCENE_COMPONENTS = [
  Scene1Apoptosis,
  Scene2CancerSurvival,
  Scene3Paclitaxel,
  Scene4DT2216,
  Scene5Combination,
  Scene6Clinical,
];

interface SceneWrapperProps {
  scene: SceneData;
}

export default function SceneWrapper({ scene }: SceneWrapperProps) {
  const SceneComponent = SCENE_COMPONENTS[scene.index];

  return (
    <ScrollScene
      id={scene.id}
      index={scene.index}
      bgColor={SCENE_BG_COLORS[scene.index]}
      title={scene.title}
      subtitle={scene.subtitle}
      paragraphs={scene.paragraphs}
    >
      {({ progress, isInView }) => (
        <SceneComponent progress={progress} isInView={isInView} />
      )}
    </ScrollScene>
  );
}
