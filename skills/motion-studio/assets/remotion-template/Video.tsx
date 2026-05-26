/**
 * Motion Studio — main composition.
 *
 * AUDIO_MODE dictates the structure:
 *   - "dialogue": clips have AI voiceover → use Series (hard cuts between clips; no fade overlap
 *                 between dialogue sequences, so voiceovers don't talk over each other).
 *                 Intro/outro can still fade since they're silent.
 *   - "music":    clips are muted and a single music bed plays over the whole composition →
 *                 use TransitionSeries for smooth visual crossfades.
 *   - "silent":   clips are muted, no audio at all → use TransitionSeries.
 *
 * Duration math:
 *   - dialogue mode (no inter-clip transitions):
 *       TOTAL = INTRO + Σ CLIPS + OUTRO − 2 × TRANSITION_FRAMES
 *               (only 2 transitions: intro↔first clip and last clip↔outro)
 *   - music/silent mode (all transitions):
 *       TOTAL = INTRO + Σ CLIPS + OUTRO − (N_SECTIONS − 1) × TRANSITION_FRAMES
 */

import React from "react";
import {
  AbsoluteFill,
  Audio,
  OffthreadVideo,
  Series,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";

// ===== Configure per project =====
export const FPS = 30;

// Vertical (TikTok/Reels/Shorts):
export const WIDTH = 1080;
export const HEIGHT = 1920;

// Landscape (YouTube): swap to 1920 × 1080
// export const WIDTH = 1920;
// export const HEIGHT = 1080;

// Durations in frames (@30fps: 30f = 1s)
const INTRO_FRAMES = 45;
const CLIP_FRAMES = 240;
const OUTRO_FRAMES = 60;
const TRANSITION_FRAMES = 15;

/**
 * AUDIO_MODE — change to match how your clips were generated.
 *
 * "dialogue": Kling V3 with generateAudio: true, or any clip with embedded voiceover.
 *             NEVER use crossfade transitions between dialogue clips — you'll get
 *             overlapping voiceovers during the 0.5s overlap. Series uses hard cuts.
 *
 * "music":    All clips are muted. A single audio track plays over the whole composition.
 *             Smooth crossfades are fine because there's only one audio source.
 *
 * "silent":   No audio anywhere. Safe to crossfade visually.
 */
type AudioMode = "dialogue" | "music" | "silent";
export const AUDIO_MODE = "dialogue" as AudioMode;
const MUSIC_FILE = "audio/music.mp3"; // only used if AUDIO_MODE === "music"
const MUSIC_VOLUME = 0.35;

// N_CLIPS and TOTAL_DURATION_FRAMES are derived from CLIPS.length below.

// Brand palette (Picsart-adjacent; override per project)
const BRAND = {
  pink: "#FF006E",
  purple: "#8338EC",
  yellow: "#FFBE0B",
  ink: "#0D0A1F",
};

// ===== Intro Card =====
const IntroCard: React.FC<{ title: string; subtitle?: string }> = ({
  title,
  subtitle,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleSpring = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 200, mass: 0.7 },
  });
  const subOpacity = interpolate(frame, [15, 35], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        background: `linear-gradient(135deg, ${BRAND.purple} 0%, ${BRAND.pink} 100%)`,
        alignItems: "center",
        justifyContent: "center",
        flexDirection: "column",
        fontFamily:
          "-apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif",
      }}
    >
      <div
        style={{
          fontSize: WIDTH < HEIGHT ? 130 : 160,
          fontWeight: 900,
          color: "#FFFFFF",
          textAlign: "center",
          lineHeight: 1,
          letterSpacing: -3,
          transform: `scale(${titleSpring})`,
          textShadow: "0 8px 40px rgba(0,0,0,0.3)",
          padding: "0 60px",
        }}
      >
        {title}
      </div>
      {subtitle ? (
        <div
          style={{
            marginTop: 48,
            fontSize: 42,
            fontWeight: 600,
            color: BRAND.yellow,
            opacity: subOpacity,
            letterSpacing: 4,
            textTransform: "uppercase",
          }}
        >
          {subtitle}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

// ===== Scene with clip + overlays =====
type SceneProps = {
  clipFile: string;
  chip: string;
  chipColor: string;
  caption: string;
  subCaption?: string;
};

const Scene: React.FC<SceneProps> = ({
  clipFile,
  chip,
  chipColor,
  caption,
  subCaption,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Clip plays unmuted only in dialogue mode; muted otherwise
  const clipMuted = AUDIO_MODE !== "dialogue";

  // Chip slides down from top
  const chipSpring = spring({
    frame: frame - 6,
    fps,
    config: { damping: 15, stiffness: 180 },
  });
  const chipY = interpolate(chipSpring, [0, 1], [-120, 0]);

  // Caption pops in from below
  const captionSpring = spring({
    frame: frame - 20,
    fps,
    config: { damping: 14, stiffness: 200 },
  });
  const captionY = interpolate(captionSpring, [0, 1], [80, 0]);
  const captionOpacity = interpolate(frame, [20, 38], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Fade UI out before the scene ends (cleans the handoff)
  const uiFadeOut = interpolate(
    frame,
    [CLIP_FRAMES - 20, CLIP_FRAMES - 5],
    [1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );

  // Subtle Ken Burns zoom
  const zoom = interpolate(frame, [0, CLIP_FRAMES], [1.0, 1.06]);

  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <AbsoluteFill style={{ transform: `scale(${zoom})` }}>
        <OffthreadVideo
          src={staticFile(clipFile)}
          endAt={CLIP_FRAMES}
          muted={clipMuted}
          style={{ width: "100%", height: "100%", objectFit: "cover" }}
        />
      </AbsoluteFill>

      <div
        style={{
          position: "absolute",
          top: 80,
          left: "50%",
          transform: `translateX(-50%) translateY(${chipY}px)`,
          opacity: uiFadeOut,
          padding: "16px 40px",
          background: chipColor,
          color: "#FFFFFF",
          fontSize: 38,
          fontWeight: 900,
          letterSpacing: 4,
          borderRadius: 999,
          boxShadow: "0 10px 40px rgba(0,0,0,0.4)",
          fontFamily:
            "-apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif",
          whiteSpace: "nowrap",
        }}
      >
        {chip}
      </div>

      <AbsoluteFill
        style={{
          background:
            "linear-gradient(to top, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0) 45%)",
          opacity: uiFadeOut,
        }}
      />

      <div
        style={{
          position: "absolute",
          bottom: 140,
          left: 50,
          right: 50,
          opacity: captionOpacity * uiFadeOut,
          transform: `translateY(${captionY}px)`,
          fontFamily:
            "-apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif",
        }}
      >
        <div
          style={{
            fontSize: 72,
            fontWeight: 900,
            color: "#FFFFFF",
            lineHeight: 1.05,
            letterSpacing: -1,
            textShadow: "0 4px 24px rgba(0,0,0,0.6)",
          }}
        >
          {caption}
        </div>
        {subCaption ? (
          <div
            style={{
              marginTop: 20,
              fontSize: 36,
              fontWeight: 500,
              color: BRAND.yellow,
              letterSpacing: 1,
              textShadow: "0 2px 12px rgba(0,0,0,0.6)",
            }}
          >
            {subCaption}
          </div>
        ) : null}
      </div>
    </AbsoluteFill>
  );
};

// ===== Outro Card =====
const OutroCard: React.FC<{ headline: string; cta?: string }> = ({
  headline,
  cta,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const logoSpring = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 180 },
  });
  const ctaOpacity = interpolate(frame, [20, 40], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        background: BRAND.ink,
        alignItems: "center",
        justifyContent: "center",
        flexDirection: "column",
        fontFamily:
          "-apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif",
      }}
    >
      <div
        style={{
          position: "absolute",
          width: 800,
          height: 800,
          borderRadius: "50%",
          background: `radial-gradient(circle, ${BRAND.pink}66 0%, transparent 70%)`,
          filter: "blur(60px)",
        }}
      />
      <div
        style={{
          fontSize: 110,
          fontWeight: 900,
          color: "#FFFFFF",
          textAlign: "center",
          letterSpacing: -3,
          lineHeight: 1,
          transform: `scale(${logoSpring})`,
          padding: "0 50px",
        }}
      >
        {headline}
      </div>
      {cta ? (
        <div
          style={{
            marginTop: 40,
            fontSize: 36,
            fontWeight: 500,
            color: "#FFFFFF99",
            opacity: ctaOpacity,
            textAlign: "center",
            letterSpacing: 2,
          }}
        >
          {cta}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

// ===== Scene content (shared between both pipelines) =====
// Add or remove entries freely — both compositions adapt to CLIPS.length.
const INTRO_PROPS = { title: "YOUR\nTITLE\nHERE", subtitle: "TAGLINE" };
const OUTRO_PROPS = { headline: "CTA", cta: "your handle here" };
const CLIPS: SceneProps[] = [
  {
    clipFile: "clips/01.mp4",
    chip: "ACT I",
    chipColor: BRAND.pink,
    caption: "Scene 1 headline.",
    subCaption: "Supporting line.",
  },
  {
    clipFile: "clips/02.mp4",
    chip: "ACT II",
    chipColor: BRAND.purple,
    caption: "Scene 2 headline.",
    subCaption: "Supporting line.",
  },
  {
    clipFile: "clips/03.mp4",
    chip: "ACT III",
    chipColor: BRAND.yellow,
    caption: "Scene 3 headline.",
    subCaption: "Payoff line.",
  },
];

const N_CLIPS = CLIPS.length;
if (N_CLIPS < 1) {
  throw new Error("motion-studio: CLIPS must contain at least 1 entry");
}

// Duration by mode:
//   dialogue: only intro and outro fade (2 transitions) — clips hard-cut
//   music/silent: every boundary fades (N_CLIPS + 1 transitions)
export const TOTAL_DURATION_FRAMES =
  AUDIO_MODE === "dialogue"
    ? INTRO_FRAMES +
      CLIP_FRAMES * N_CLIPS +
      OUTRO_FRAMES -
      2 * TRANSITION_FRAMES
    : INTRO_FRAMES +
      CLIP_FRAMES * N_CLIPS +
      OUTRO_FRAMES -
      (N_CLIPS + 1) * TRANSITION_FRAMES;

// ===== Pipeline A: dialogue mode =====
// Intro fades into clip[0]; middle clips are hard cuts; clip[N-1] fades into outro.
// For N = 1 the "first super-sequence" contains intro + clip[0] + outro so there's
// still a full fade on each end and no middle section to worry about.
const DialogueComposition: React.FC = () => {
  // Special case: N=1 — one TransitionSeries spans the whole composition.
  if (N_CLIPS === 1) {
    return (
      <AbsoluteFill style={{ backgroundColor: "black" }}>
        <TransitionSeries>
          <TransitionSeries.Sequence durationInFrames={INTRO_FRAMES}>
            <IntroCard {...INTRO_PROPS} />
          </TransitionSeries.Sequence>
          <TransitionSeries.Transition
            presentation={fade()}
            timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
          />
          <TransitionSeries.Sequence durationInFrames={CLIP_FRAMES}>
            <Scene {...CLIPS[0]} />
          </TransitionSeries.Sequence>
          <TransitionSeries.Transition
            presentation={fade()}
            timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
          />
          <TransitionSeries.Sequence durationInFrames={OUTRO_FRAMES}>
            <OutroCard {...OUTRO_PROPS} />
          </TransitionSeries.Sequence>
        </TransitionSeries>
      </AbsoluteFill>
    );
  }

  // General case: N >= 2.
  // First super-sequence: intro + clip[0] with a fade between them.
  // Middle super-sequences (only when N >= 3): clip[1..N-2] as plain Series items — hard cuts, no audio overlap.
  // Last super-sequence: clip[N-1] + outro with a fade between them.
  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      <Series>
        <Series.Sequence
          durationInFrames={INTRO_FRAMES + CLIP_FRAMES - TRANSITION_FRAMES}
        >
          <TransitionSeries>
            <TransitionSeries.Sequence durationInFrames={INTRO_FRAMES}>
              <IntroCard {...INTRO_PROPS} />
            </TransitionSeries.Sequence>
            <TransitionSeries.Transition
              presentation={fade()}
              timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
            />
            <TransitionSeries.Sequence durationInFrames={CLIP_FRAMES}>
              <Scene {...CLIPS[0]} />
            </TransitionSeries.Sequence>
          </TransitionSeries>
        </Series.Sequence>

        {CLIPS.slice(1, N_CLIPS - 1).map((props, i) => (
          <Series.Sequence key={`mid-${i}`} durationInFrames={CLIP_FRAMES}>
            <Scene {...props} />
          </Series.Sequence>
        ))}

        <Series.Sequence
          durationInFrames={CLIP_FRAMES + OUTRO_FRAMES - TRANSITION_FRAMES}
        >
          <TransitionSeries>
            <TransitionSeries.Sequence durationInFrames={CLIP_FRAMES}>
              <Scene {...CLIPS[N_CLIPS - 1]} />
            </TransitionSeries.Sequence>
            <TransitionSeries.Transition
              presentation={fade()}
              timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
            />
            <TransitionSeries.Sequence durationInFrames={OUTRO_FRAMES}>
              <OutroCard {...OUTRO_PROPS} />
            </TransitionSeries.Sequence>
          </TransitionSeries>
        </Series.Sequence>
      </Series>
    </AbsoluteFill>
  );
};

// ===== Pipeline B: music/silent mode (TransitionSeries all the way, clips muted) =====
const CrossfadeComposition: React.FC = () => {
  const clipSections: React.ReactNode[] = [];
  CLIPS.forEach((props, i) => {
    clipSections.push(
      <TransitionSeries.Transition
        key={`fade-before-${i}`}
        presentation={fade()}
        timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
      />,
    );
    clipSections.push(
      <TransitionSeries.Sequence
        key={`clip-${i}`}
        durationInFrames={CLIP_FRAMES}
      >
        <Scene {...props} />
      </TransitionSeries.Sequence>,
    );
  });

  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      {AUDIO_MODE === "music" ? (
        <Audio src={staticFile(MUSIC_FILE)} volume={MUSIC_VOLUME} />
      ) : null}

      <TransitionSeries>
        <TransitionSeries.Sequence durationInFrames={INTRO_FRAMES}>
          <IntroCard {...INTRO_PROPS} />
        </TransitionSeries.Sequence>

        {clipSections}

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
        />

        <TransitionSeries.Sequence durationInFrames={OUTRO_FRAMES}>
          <OutroCard {...OUTRO_PROPS} />
        </TransitionSeries.Sequence>
      </TransitionSeries>
    </AbsoluteFill>
  );
};

// ===== Main composition — dispatches based on AUDIO_MODE =====
export const Video: React.FC = () => {
  if (AUDIO_MODE === "dialogue") {
    return <DialogueComposition />;
  }
  return <CrossfadeComposition />;
};
