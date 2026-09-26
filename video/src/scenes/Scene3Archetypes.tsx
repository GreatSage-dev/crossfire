import React from "react";
import { interpolate, useCurrentFrame } from "remotion";

export const Scene3Archetypes: React.FC = () => {
  const frame = useCurrentFrame();

  const archetypes = [
    {
      num: "01",
      name: "Invariant Scale Drift",
      symbol: "discount",
      agentA: "float[0.0, 1.0]",
      agentB: "int[0, 100]",
      failure: "-1,400% Price Charge",
      tcas: "HALTED (EXIT 2)",
    },
    {
      num: "02",
      name: "Lifecycle Desync",
      symbol: "evict_session",
      agentA: "async coroutine",
      agentB: "sync function",
      failure: "Event Loop Crash",
      tcas: "HALTED (EXIT 2)",
    },
    {
      num: "03",
      name: "Contract Divergence",
      symbol: "get_item",
      agentA: "raise ItemNotFound",
      agentB: "return None",
      failure: "Silent Null Corruption",
      tcas: "HALTED (EXIT 2)",
    },
    {
      num: "04",
      name: "Same-Type Unit Drift",
      symbol: "timeout",
      agentA: "int (seconds: 1..60)",
      agentB: "int (milliseconds: 5000)",
      failure: "Defeats mypy! Gateway Timeout",
      tcas: "HALTED (EXIT 2)",
      highlight: true,
    },
  ];

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
        padding: "60px 80px",
        boxSizing: "border-box",
      }}
    >
      <div
        style={{
          fontSize: "18px",
          color: "#E8611A",
          fontWeight: 600,
          letterSpacing: "0.2em",
          marginBottom: "12px",
          textTransform: "uppercase",
        }}
      >
        THE DIFFERENTIAL MATRIX
      </div>

      <h2 style={{ fontSize: "44px", fontWeight: 700, margin: "0 0 35px 0", textAlign: "center" }}>
        Four Controlled Multi-Agent Collision Archetypes
      </h2>

      {/* Table Container */}
      <div
        style={{
          width: "100%",
          maxWidth: "1500px",
          backgroundColor: "#161616",
          border: "1px solid #252525",
          borderRadius: "6px",
          overflow: "hidden",
        }}
      >
        {/* Table Header */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "2.2fr 1.4fr 1.6fr 1.6fr 2fr 1.6fr",
            padding: "18px 24px",
            backgroundColor: "#202020",
            borderBottom: "1px solid #252525",
            fontSize: "15px",
            fontWeight: 700,
            color: "#888888",
            letterSpacing: "0.08em",
          }}
        >
          <div>COLLISION ARCHETYPE</div>
          <div>SYMBOL</div>
          <div>SUBAGENT A</div>
          <div>SUBAGENT B</div>
          <div>STANDARD FAILURE</div>
          <div>CROSSFIRE TCAS</div>
        </div>

        {/* Table Rows */}
        {archetypes.map((row, idx) => {
          const rowOpacity = interpolate(frame - idx * 15, [0, 15], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });

          return (
            <div
              key={row.num}
              style={{
                display: "grid",
                gridTemplateColumns: "2.2fr 1.4fr 1.6fr 1.6fr 2fr 1.6fr",
                padding: "20px 24px",
                borderBottom: idx < archetypes.length - 1 ? "1px solid #252525" : "none",
                backgroundColor: row.highlight ? "rgba(232, 97, 26, 0.08)" : "transparent",
                borderLeft: row.highlight ? "4px solid #E8611A" : "4px solid transparent",
                opacity: rowOpacity,
                fontSize: "17px",
                alignItems: "center",
              }}
            >
              <div style={{ fontWeight: 600, color: row.highlight ? "#F5A623" : "#F0EDE8" }}>
                <span style={{ color: "#666666", marginRight: "10px" }}>{row.num}</span>
                {row.name}
              </div>
              <div style={{ color: "#E8611A" }}>{row.symbol}</div>
              <div style={{ color: "#4CAF50" }}>{row.agentA}</div>
              <div style={{ color: "#F5A623" }}>{row.agentB}</div>
              <div style={{ color: row.highlight ? "#FF7043" : "#E57373", fontWeight: 600 }}>
                {row.failure}
              </div>
              <div>
                <span
                  style={{
                    backgroundColor: "rgba(232, 97, 26, 0.2)",
                    border: "1px solid #E8611A",
                    color: "#E8611A",
                    padding: "4px 12px",
                    borderRadius: "4px",
                    fontWeight: 700,
                    fontSize: "14px",
                  }}
                >
                  {row.tcas}
                </span>
              </div>
            </div>
          );
        })}
      </div>

      <div
        style={{
          marginTop: "30px",
          fontSize: "18px",
          color: "#A09D98",
          textAlign: "center",
        }}
      >
        In all 4 cases: Git reports 0 conflicts • mypy reports 0 errors • CROSSFIRE intercepts at AST boundary
      </div>
    </div>
  );
};
