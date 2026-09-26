import React from "react";
import { useCurrentFrame, staticFile } from "remotion";

export const Scene4Console: React.FC = () => {
  const frame = useCurrentFrame();

  // Radar sweep angle
  const radarRotation = (frame * 4) % 360;

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
        padding: "40px",
        boxSizing: "border-box",
      }}
    >
      <div
        style={{
          fontSize: "18px",
          color: "#E8611A",
          fontWeight: 600,
          letterSpacing: "0.2em",
          marginBottom: "10px",
          textTransform: "uppercase",
        }}
      >
        OPERATIONS CONSOLE & LIVE SANDBOX
      </div>

      <h2 style={{ fontSize: "38px", fontWeight: 700, margin: "0 0 25px 0" }}>
        Live Interactive TCAS Detection & Resolution
      </h2>

      {/* Browser Window Mockup */}
      <div
        style={{
          width: "100%",
          maxWidth: "1500px",
          height: "720px",
          backgroundColor: "#161616",
          border: "1px solid #333333",
          borderRadius: "8px",
          overflow: "hidden",
          display: "flex",
          flexDirection: "column",
          boxShadow: "0 25px 60px rgba(0, 0, 0, 0.7)",
        }}
      >
        {/* Browser Top Bar */}
        <div
          style={{
            height: "44px",
            backgroundColor: "#202020",
            borderBottom: "1px solid #333333",
            display: "flex",
            alignItems: "center",
            padding: "0 18px",
            gap: "14px",
          }}
        >
          <div style={{ display: "flex", gap: "8px" }}>
            <div style={{ width: "12px", height: "12px", borderRadius: "50%", backgroundColor: "#FF5F56" }} />
            <div style={{ width: "12px", height: "12px", borderRadius: "50%", backgroundColor: "#FFBD2E" }} />
            <div style={{ width: "12px", height: "12px", borderRadius: "50%", backgroundColor: "#27C93F" }} />
          </div>
          <div
            style={{
              flex: 1,
              maxWidth: "600px",
              height: "28px",
              backgroundColor: "#0D0D0D",
              border: "1px solid #282828",
              borderRadius: "4px",
              display: "flex",
              alignItems: "center",
              padding: "0 12px",
              fontSize: "13px",
              color: "#888888",
            }}
          >
            https://crossfire-production.vercel.app/dashboard
          </div>
          <div
            style={{
              padding: "4px 12px",
              backgroundColor: "rgba(232, 97, 26, 0.15)",
              border: "1px solid #E8611A",
              color: "#E8611A",
              fontSize: "12px",
              fontWeight: 700,
              borderRadius: "4px",
            }}
          >
            ● TCAS ACTIVE // 3 HALTS
          </div>
        </div>

        {/* Dashboard Content Mockup */}
        <div style={{ flex: 1, display: "grid", gridTemplateColumns: "1.2fr 2fr", gap: "20px", padding: "24px" }}>
          {/* Left: TCAS Radar Cockpit */}
          <div
            style={{
              backgroundColor: "#111111",
              border: "1px solid #252525",
              borderRadius: "6px",
              padding: "20px",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              position: "relative",
            }}
          >
            <div style={{ fontSize: "14px", color: "#888888", marginBottom: "10px", width: "100%" }}>
              AIR TRAFFIC RADAR COCKPIT
            </div>
            <svg width="340" height="340" viewBox="0 0 340 340">
              <circle cx="170" cy="170" r="50" stroke="#252525" strokeWidth="1.5" fill="none" />
              <circle cx="170" cy="170" r="100" stroke="#252525" strokeWidth="1.5" fill="none" />
              <circle cx="170" cy="170" r="150" stroke="#252525" strokeWidth="1.5" fill="none" />
              <line x1="20" y1="170" x2="320" y2="170" stroke="#252525" strokeWidth="1" strokeDasharray="3 3" />
              <line x1="170" y1="20" x2="170" y2="320" stroke="#252525" strokeWidth="1" strokeDasharray="3 3" />

              <g transform={`rotate(${radarRotation} 170 170)`}>
                <line x1="170" y1="170" x2="320" y2="170" stroke="#E8611A" strokeWidth="2.5" opacity="0.85" />
              </g>

              {/* Threat Dots */}
              <circle cx="230" cy="120" r="6" fill="#E8611A" />
              <text x="242" y="125" fill="#E8611A" fontSize="12">discount</text>

              <circle cx="120" cy="220" r="6" fill="#F5A623" />
              <text x="50" y="225" fill="#F5A623" fontSize="12">evict_session</text>

              <circle cx="260" cy="210" r="6" fill="#E8611A" />
              <text x="272" y="215" fill="#E8611A" fontSize="12">timeout</text>
            </svg>
            <div style={{ marginTop: "14px", fontSize: "13px", color: "#666666" }}>
              FAIL-CLOSED INTERCEPT: IBM Bob PreToolUse Exit Code 2
            </div>
          </div>

          {/* Right: Assumption Ledger & Advisory */}
          <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
            {/* Assumption Ledger */}
            <div
              style={{
                flex: 1,
                backgroundColor: "#111111",
                border: "1px solid #252525",
                borderRadius: "6px",
                padding: "16px",
              }}
            >
              <div style={{ fontSize: "14px", color: "#888888", marginBottom: "12px" }}>
                LIVE ASSUMPTION LEDGER
              </div>
              <div style={{ fontSize: "13px", lineHeight: "26px" }}>
                <div style={{ display: "flex", justifyContent: "space-between", color: "#E8611A" }}>
                  <span>▸ discount</span>
                  <span>float[0.0, 1.0] vs int[0, 100]</span>
                  <span style={{ fontWeight: 700 }}>HALTED (0.95)</span>
                </div>
                <div style={{ display: "flex", justifyContent: "space-between", color: "#F5A623" }}>
                  <span>▸ evict_session</span>
                  <span>async vs sync</span>
                  <span style={{ fontWeight: 700 }}>HALTED (0.85)</span>
                </div>
                <div style={{ display: "flex", justifyContent: "space-between", color: "#E8611A" }}>
                  <span>▸ timeout</span>
                  <span>int[1, 60]s vs int[val=5000]ms</span>
                  <span style={{ fontWeight: 700 }}>HALTED (0.95)</span>
                </div>
              </div>
            </div>

            {/* Resolution Advisory */}
            <div
              style={{
                backgroundColor: "#111111",
                border: "1px solid #252525",
                borderLeft: "4px solid #E8611A",
                borderRadius: "6px",
                padding: "16px",
              }}
            >
              <div style={{ fontSize: "14px", color: "#E8611A", fontWeight: 700, marginBottom: "8px" }}>
                TCAS RESOLUTION ADVISORY (AUTO-STEER HINT)
              </div>
              <div style={{ fontSize: "14px", color: "#F0EDE8", marginBottom: "8px" }}>
                Target: Subagent B • Symbol: <code style={{ color: "#F5A623" }}>timeout</code>
              </div>
              <div
                style={{
                  backgroundColor: "#0D0D0D",
                  padding: "10px 14px",
                  borderRadius: "4px",
                  fontSize: "13px",
                  color: "#4CAF50",
                }}
              >
                PATCH HINT: timeout = timeout // 1000 # Convert milliseconds to seconds
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
