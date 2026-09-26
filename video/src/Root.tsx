import React from "react";
import { Composition } from "remotion";
import { MainComposition } from "./Composition";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="CrossfireDemo"
      component={MainComposition}
      durationInFrames={30 * 90} // 90 seconds @ 30fps
      fps={30}
      width={1920}
      height={1080}
    />
  );
};
