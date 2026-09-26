import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const Scene1Intro: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Entrance spring
  const titleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });
  const titleScale = spring({ frame, fps, config: { damping: 14 } });

  // Rotating radar angle
  const radarRotation = (frame * 3) % 360;

  // Pulse
  const pulse = Math.sin(frame / 6) * 0.2 + 0.8;

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: "#0D0D0D",
        color: "#F0EDE8",
        fontFamily: "'IBM Plex Mono', monospace, sans-serif",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* Background Subtle Radar */}
      <svg
        width="600"
        height="600"
        style={{
          position: "absolute",
          opacity: 0.25,
          pointerEvents: "none",
        }}
        viewBox="0 0 600 600"
      >
        <circle cx="300" cy="300" r="100" stroke="#252525" strokeWidth="2" fill="none" />
        <circle cx="300" cy="300" r="180" stroke="#252525" strokeWidth="2" fill="none" />
        <circle cx="300" cy="300" r="260" stroke="#252525" strokeWidth="2" fill="none" />
        <line x1="40" y1="300" x2="560" y2="300" stroke="#252525" strokeWidth="1" strokeDasharray="4 4" />
        <line x1="300" y1="40" x2="300" y2="560" stroke="#252525" strokeWidth="1" strokeDasharray="4 4" />

        {/* Sweep arm */}
        <g transform={`rotate(${radarRotation} 300 300)`}>
          <line x1="300" y1="300" x2="560" y2="300" stroke="#E8611A" strokeWidth="3" opacity="0.8" />
        </g>

        {/* Threat dots */}
        <circle cx="390" cy="220" r="7" fill="#E8611A" opacity={pulse} />
        <circle cx="230" cy="380" r="6" fill="#F5A623" opacity={pulse} />
        <circle cx="440" cy="370" r="6" fill="#E8611A" opacity={pulse} />
      </svg>

      {/* Badge */}
      <div
        style={{
          opacity: titleOpacity,
          padding: "8px 20px",
          borderRadius: "999px",
          border: "1px solid #E8611A",
          backgroundColor: "rgba(232, 97, 26, 0.12)",
          color: "#E8611A",
          fontSize: "18px",
          fontWeight: 600,
          letterSpacing: "0.15em",
          marginBottom: "28px",
          textTransform: "uppercase",
        }}
      >
        ✦ TCAS FOR IBM BOB 2.0
      </div>

      {/* Main Brand Title */}
      <h1
        style={{
          opacity: titleOpacity,
          transform: `scale(${titleScale})`,
          fontSize: "108px",
          fontWeight: 800,
          margin: 0,
          letterSpacing: "0.12em",
          color: "#F0EDE8",
          textShadow: "0 0 40px rgba(232, 97, 26, 0.35)",
        }}
      >
        CROSSFIRE
      </h1>

      {/* Subtitle */}
      <p
        style={{
          opacity: titleOpacity,
          fontSize: "26px",
          color: "#A09D98",
          marginTop: "20px",
          maxWidth: "880px",
          textAlign: "center",
          lineHeight: 1.5,
          fontWeight: 400,
        }}
      >
        Air Traffic Collision Avoidance for Parallel AI Agents
      </p>

      {/* Bottom Metadata */}
      <div
        style={{
          position: "absolute",
          bottom: "50px",
          display: "flex",
          gap: "40px",
          fontSize: "16px",
          color: "#666666",
          letterSpacing: "0.08em",
        }}
      >
        <span>TEAM: MRSAGE</span>
        <span>•</span>
        <span>LABLAB IBM BOB 2.0 HACKATHON</span>
        <span>•</span>
        <span>SEPTEMBER 2026</span>
      </div>
    </div>
  );
};
