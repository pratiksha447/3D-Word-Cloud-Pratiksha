// frontend/src/api.ts
/**
 * A single keyword item returned by the API.
 */
export interface WordItem {
  word: string;
  weight: number;
}

/**
 * Response shape for the /analyze API endpoint.
 */
export interface AnalyzeResponse {
  words: WordItem[];
}

const API_BASE = "http://localhost:8000";

/**
 * Send the given URL to the backend /analyze endpoint and return parsed JSON.
 * Throws an Error when the response is not OK.
 */
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
