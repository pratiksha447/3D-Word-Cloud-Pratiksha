// frontend/src/components/WordCloud3D.tsx
import React, { useMemo } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, Text } from "@react-three/drei";
import type { WordItem } from "../api";

interface WordCloud3DProps {
  words: WordItem[];
}

/**
 * Return a random point on the surface of a sphere of the given `radius`.
 * Uses uniform sampling on the sphere via spherical coordinates.
 */
function randomOnSphere(radius: number) {
  const u = Math.random();
  const v = Math.random();
  const theta = 2 * Math.PI * u;
  const phi = Math.acos(2 * v - 1);
  const x = radius * Math.sin(phi) * Math.cos(theta);
  const y = radius * Math.sin(phi) * Math.sin(theta);
  const z = radius * Math.cos(phi);
  return [x, y, z] as [number, number, number];
}

/**
 * Map a normalized weight in [0,1] to an RGB color string.
 * Lower weights trend towards blue; higher weights trend towards pink.
 */
function weightToColor(weight: number): string {
  // 0 -> blue, 1 -> pink
  const t = Math.min(Math.max(weight, 0), 1);
  const r = Math.round(99 + t * (236 - 99));
  const g = Math.round(102 + t * (72 - 102));
  const b = Math.round(241 + t * (153 - 241));
  return `rgb(${r}, ${g}, ${b})`;
}

/**
 * Internal component that positions words on a sphere and renders them as
 * 3D text using @react-three/fiber and @react-three/drei.
 */
const WordCloud3DInner: React.FC<WordCloud3DProps> = ({ words }) => {
  const positioned = useMemo(() => {
    const radius = 4;
    return words.map((w) => ({
      ...w,
      position: randomOnSphere(radius),
    }));
  }, [words]);

  return (
    <>
      <ambientLight intensity={0.6} />
      <directionalLight position={[5, 5, 5]} intensity={0.8} />
      {positioned.map((item, idx) => {
        const size = 0.4 + item.weight * 1.2;
        const color = weightToColor(item.weight);
        return (
          <Text
            key={`${item.word}-${idx}`}
            position={item.position}
            fontSize={size}
            color={color}
            anchorX="center"
            anchorY="middle"
          >
            {item.word}
          </Text>
        );
      })}
      <OrbitControls enablePan enableZoom enableRotate />
    </>
  );
};

/**
 * Top-level component embedding the 3D canvas and rendering the word cloud.
 */
export const WordCloud3D: React.FC<WordCloud3DProps> = ({ words }) => {
  return (
    <Canvas camera={{ position: [0, 0, 10], fov: 60 }}>
      <WordCloud3DInner words={words} />
    </Canvas>
  );
};
