// frontend/src/App.tsx
import React, { useState } from "react";
import { analyzeUrl, type WordItem } from "./api";
import { WordCloud3D } from "./components/WordCloud3D";
import { HUD } from "./components/HUD";

const SAMPLE_URLS = [
  "https://www.bbc.com",
  "https://www.nytimes.com"
];

/**
 * Top-level application component.
 * Manages UI state, triggers analysis requests and renders the 3D word cloud
 * and HUD when keywords are available.
 */
function App() {
  const [url, setUrl] = useState<string>(SAMPLE_URLS[0]);
  const [words, setWords] = useState<WordItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  /**
   * Fetch keywords for the current `url` and update UI state.
   * Handles loading and error states appropriately.
   */
  const handleAnalyze = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await analyzeUrl(url);
      setWords(res.words);
    } catch (e: any) {
      setError(e.message ?? "Failed to analyze URL");
      setWords([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-root">
      <header className="app-header">
        <div className="app-title">3D Word Cloud – News Topics</div>
        <div className="app-subtitle">
          Enter a news article URL to see its topics as an interactive 3D word cloud.
        </div>

        <div className="app-controls">
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Paste article URL..."
          />
          <button onClick={handleAnalyze} disabled={loading || !url}>
            {loading ? "Analyzing..." : "Analyze"}
          </button>
        </div>

        <div className="app-status">
          {error && <span style={{ color: "#f97373" }}>{error}</span>}
          {!error && loading && <span>Fetching article and extracting topics…</span>}
          {!error && !loading && words.length === 0 && (
            <span>Try one of the sample URLs above to get started.</span>
          )}
          {!error && !loading && words.length > 0 && (
            <span>Showing {words.length} keywords from this article.</span>
          )}
        </div>
      </header>

      <main className="app-main">
        {words.length > 0 && <WordCloud3D words={words} />}
        {words.length > 0 && <HUD words={words} />}
      </main>
    </div>
  );
}

export default App;
