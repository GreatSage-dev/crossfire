import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const Scene5Thesis: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const thesisSpring = spring({ frame: frame - 15, fps, config: { damping: 14 } });
  const badgeOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });

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
        padding: "60px 100px",
        boxSizing: "border-box",
        position: "relative",
      }}
    >
      {/* Proof Metric Pills */}
      <div
        style={{
          display: "flex",
          gap: "24px",
          opacity: badgeOpacity,
          marginBottom: "50px",
        }}
      >
        <div
          style={{
            padding: "8px 20px",
            backgroundColor: "#161616",
            border: "1px solid #252525",
            borderRadius: "999px",
            fontSize: "15px",
            color: "#4CAF50",
            fontWeight: 600,
          }}
        >
          ✓ 19/19 Unit Tests Passed
        </div>
        <div
          style={{
            padding: "8px 20px",
            backgroundColor: "#161616",
            border: "1px solid #252525",
            borderRadius: "999px",
            fontSize: "15px",
            color: "#4CAF50",
            fontWeight: 600,
          }}
        >
          ✓ 8/8 Architectural Mutants Killed (100%)
        </div>
        <div
          style={{
            padding: "8px 20px",
            backgroundColor: "#161616",
            border: "1px solid #252525",
            borderRadius: "999px",
            fontSize: "15px",
            color: "#F5A623",
            fontWeight: 600,
          }}
        >
          ⚡ 1.08 Bobcoins Used / 40.0 Allocation
        </div>
      </div>

      {/* The Core Thesis Box */}
      <div
        style={{
          maxWidth: "1280px",
          backgroundColor: "#141414",
          border: "1px solid #2E2E2E",
          borderLeft: "6px solid #E8611A",
          borderRadius: "6px",
          padding: "50px 60px",
          transform: `scale(${thesisSpring})`,
          boxShadow: "0 20px 50px rgba(0, 0, 0, 0.6)",
        }}
      >
        <div
          style={{
            fontSize: "16px",
            color: "#E8611A",
            letterSpacing: "0.2em",
            fontWeight: 700,
            marginBottom: "20px",
            textTransform: "uppercase",
          }}
        >
          THE CORE THESIS
        </div>

        <p
          style={{
            fontSize: "36px",
            fontWeight: 700,
            lineHeight: 1.45,
            margin: 0,
            color: "#F0EDE8",
          }}
        >
          Git detects textual conflicts. <br />
          Tests detect behavioral failures in isolation. <br />
          <span style={{ color: "#E8611A" }}>
            CROSSFIRE detects conflicts between the assumptions of autonomous software agents before those assumptions become a system.
          </span>
        </p>
      </div>

      {/* Footer Call to Action */}
      <div
        style={{
          marginTop: "60px",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: "12px",
        }}
      >
        <div style={{ fontSize: "24px", fontWeight: 700, color: "#F5A623" }}>
          crossfire-production.vercel.app
        </div>
        <div style={{ fontSize: "16px", color: "#666666" }}>
          TEAM MRSAGE // GITHUB: GreatSage-dev/crossfire // IBM BOB 2.0 HACKATHON
        </div>
      </div>
    </div>
  );
};
