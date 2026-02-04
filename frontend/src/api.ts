// frontend/src/api.ts
export interface WordItem {
  word: string;
  weight: number;
}

export interface AnalyzeResponse {
  words: WordItem[];
}

const API_BASE = "http://localhost:8000";

export async function analyzeUrl(url: string): Promise<AnalyzeResponse> {
  const res = await fetch(`${API_BASE}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `Request failed with status ${res.status}`);
  }

  return res.json();
}
