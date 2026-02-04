// frontend/src/components/HUD.tsx
import React from "react";
import type { WordItem } from "../api";

interface HUDProps {
  words: WordItem[];
}

export const HUD: React.FC<HUDProps> = ({ words }) => {
  const top = words.slice(0, 5);
  return (
    <div
      style={{
        position: "absolute",
        right: "1rem",
        bottom: "1rem",
        padding: "0.75rem 1rem",
        borderRadius: "0.5rem",
        background: "rgba(15, 23, 42, 0.85)",
        border: "1px solid rgba(148, 163, 184, 0.4)",
        fontSize: "0.8rem",
      }}
    >
      <div style={{ marginBottom: "0.25rem", fontWeight: 600 }}>Top words</div>
      {top.map((w) => (
        <div key={w.word}>
          {w.word} <span style={{ opacity: 0.7 }}>({w.weight.toFixed(2)})</span>
        </div>
      ))}
    </div>
  );
};
