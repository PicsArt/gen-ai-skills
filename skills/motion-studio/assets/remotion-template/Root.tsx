import { Composition } from "remotion";
import { Video, TOTAL_DURATION_FRAMES, FPS, WIDTH, HEIGHT } from "./Video";

export const Root: React.FC = () => {
  return (
    <Composition
      id="Video"
      component={Video}
      durationInFrames={TOTAL_DURATION_FRAMES}
      fps={FPS}
      width={WIDTH}
      height={HEIGHT}
    />
  );
};
