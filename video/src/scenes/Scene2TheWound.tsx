import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const Scene2TheWound: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const card1Spring = spring({ frame: frame - 10, fps, config: { damping: 12 } });
  const card2Spring = spring({ frame: frame - 25, fps, config: { damping: 12 } });
  const card3Spring = spring({ frame: frame - 45, fps, config: { damping: 10 } });

  const flash = Math.sin(frame / 4) > 0 ? 1 : 0.4;

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
        padding: "60px",
        boxSizing: "border-box",
      }}
    >
      <div
        style={{
          fontSize: "18px",
          color: "#E8611A",
          fontWeight: 600,
          letterSpacing: "0.2em",
          marginBottom: "16px",
          textTransform: "uppercase",
        }}
      >
        THE INVISIBLE WOUND
      </div>

      <h2
        style={{
          fontSize: "48px",
          fontWeight: 700,
          margin: "0 0 50px 0",
          textAlign: "center",
        }}
      >
        Why Standard Tools Pass Silently Into Catastrophe
      </h2>

      {/* 3 Status Cards */}
      <div
        style={{
          display: "flex",
          gap: "30px",
          width: "100%",
          maxWidth: "1400px",
          justifyContent: "center",
        }}
      >
        {/* Card 1: Git Merge */}
        <div
          style={{
            flex: 1,
            backgroundColor: "#161616",
            border: "1px solid #252525",
            borderRadius: "4px",
            padding: "36px",
            opacity: interpolate(card1Spring, [0, 1], [0, 1]),
            transform: `translateY(${(1 - card1Spring) * 40}px)`,
          }}
        >
          <div style={{ fontSize: "16px", color: "#888888", marginBottom: "14px" }}>STAGE 01 // TEXT MERGE</div>
          <div style={{ fontSize: "28px", fontWeight: 700, marginBottom: "20px" }}>Git Merge-Tree</div>
          <div
            style={{
              padding: "16px 20px",
              backgroundColor: "rgba(76, 175, 80, 0.12)",
              border: "1px solid #4CAF50",
              color: "#4CAF50",
              fontSize: "22px",
              fontWeight: 700,
              borderRadius: "4px",
            }}
          >
            ✓ 0 CONFLICTS
          </div>
          <p style={{ fontSize: "16px", color: "#888888", marginTop: "18px", lineHeight: 1.5 }}>
            Subagents work in distinct scratchpad files. Git reports a clean merge.
          </p>
        </div>

        {/* Card 2: Linter / Mypy */}
        <div
          style={{
            flex: 1,
            backgroundColor: "#161616",
            border: "1px solid #252525",
            borderRadius: "4px",
            padding: "36px",
            opacity: interpolate(card2Spring, [0, 1], [0, 1]),
            transform: `translateY(${(1 - card2Spring) * 40}px)`,
          }}
        >
          <div style={{ fontSize: "16px", color: "#888888", marginBottom: "14px" }}>STAGE 02 // TYPE SYSTEM</div>
          <div style={{ fontSize: "28px", fontWeight: 700, marginBottom: "20px" }}>mypy & Compiler</div>
          <div
            style={{
              padding: "16px 20px",
              backgroundColor: "rgba(76, 175, 80, 0.12)",
              border: "1px solid #4CAF50",
              color: "#4CAF50",
              fontSize: "22px",
              fontWeight: 700,
              borderRadius: "4px",
            }}
          >
            ✓ 0 TYPE ERRORS
          </div>
          <p style={{ fontSize: "16px", color: "#888888", marginTop: "18px", lineHeight: 1.5 }}>
            Both subagents use valid Python syntax and conform to static type declarations.
          </p>
        </div>

        {/* Card 3: Runtime */}
        <div
          style={{
            flex: 1,
            backgroundColor: "#161616",
            border: "1px solid #E8611A",
            borderRadius: "4px",
            padding: "36px",
            opacity: interpolate(card3Spring, [0, 1], [0, 1]),
            transform: `translateY(${(1 - card3Spring) * 40}px)`,
          }}
        >
          <div style={{ fontSize: "16px", color: "#E8611A", marginBottom: "14px" }}>STAGE 03 // EXECUTION</div>
          <div style={{ fontSize: "28px", fontWeight: 700, marginBottom: "20px" }}>Production Runtime</div>
          <div
            style={{
              padding: "16px 20px",
              backgroundColor: "rgba(232, 97, 26, 0.18)",
              border: "1px solid #E8611A",
              color: "#FF5722",
              fontSize: "22px",
              fontWeight: 700,
              borderRadius: "4px",
              opacity: flash,
            }}
          >
            💥 CATASTROPHIC OUTAGE
          </div>
          <p style={{ fontSize: "16px", color: "#D0CDC8", marginTop: "18px", lineHeight: 1.5 }}>
            -$1,400 billing overcharge / Gateway timeout / Zombie auth window.
          </p>
        </div>
      </div>

      {/* Quote Banner */}
      <div
        style={{
          marginTop: "50px",
          padding: "18px 40px",
          backgroundColor: "#161616",
          borderLeft: "4px solid #F5A623",
          maxWidth: "1200px",
          fontSize: "20px",
          color: "#D0CDC8",
          fontStyle: "italic",
        }}
      >
        "Git was built for lines of text. Linters only check local syntax. Neither tool knows what your autonomous agents were actually assuming."
      </div>
    </div>
  );
};
