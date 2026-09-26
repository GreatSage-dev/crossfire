import React from "react";
import { Series } from "remotion";
import { Scene1Intro } from "./scenes/Scene1Intro";
import { Scene2TheWound } from "./scenes/Scene2TheWound";
import { Scene3Archetypes } from "./scenes/Scene3Archetypes";
import { Scene4Console } from "./scenes/Scene4Console";
import { Scene5Thesis } from "./scenes/Scene5Thesis";

export const MainComposition: React.FC = () => {
  return (
    <Series>
      {/* Scene 1: Intro (0s - 10s) */}
      <Series.Sequence durationInFrames={300}>
        <Scene1Intro />
      </Series.Sequence>

      {/* Scene 2: The Wound (10s - 25s) */}
      <Series.Sequence durationInFrames={450}>
        <Scene2TheWound />
      </Series.Sequence>

      {/* Scene 3: The 4 Archetypes (25s - 45s) */}
      <Series.Sequence durationInFrames={600}>
        <Scene3Archetypes />
      </Series.Sequence>

      {/* Scene 4: Operations Console & Live Demo (45s - 75s) */}
      <Series.Sequence durationInFrames={900}>
        <Scene4Console />
      </Series.Sequence>

      {/* Scene 5: Proof Metrics & Core Thesis (75s - 90s) */}
      <Series.Sequence durationInFrames={450}>
        <Scene5Thesis />
      </Series.Sequence>
    </Series>
  );
};
