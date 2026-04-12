import { useState } from 'react';
import Sidebar from './components/Sidebar';
import RightSidebar from './components/RightSidebar';
import Composer from './components/Composer';
import ResultCard from './components/ResultCard';
import type { AnalysisResult } from './types';

export default function App() {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [analyzedText, setAnalyzedText] = useState('');

  const handleAnalyze = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });

      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.detail || `Server error: ${res.status}`);
      }

      const data: AnalysisResult = await res.json();
      setAnalyzedText(text);
      setResult(data);
      // Scroll to result
      setTimeout(() => {
        document.getElementById('result-card')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 100);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-layout">
      <Sidebar />

      {/* Main feed */}
      <main className="main-feed">
        {/* Header */}
        <header className="feed-header">
          <h1 className="feed-title">Home</h1>
          <p className="feed-subtitle">Indonesian Hate Speech Detector · Naive Bayes + TF-IDF</p>
        </header>

        {/* Tab bar */}
        <div className="tab-bar" role="tablist">
          <button role="tab" aria-selected="true" className="tab tab--active">For you</button>
          <button role="tab" aria-selected="false" className="tab">Following</button>
        </div>

        {/* Composer */}
        <section className="composer-section">
          <Composer
            text={text}
            loading={loading}
            onChange={setText}
            onSubmit={handleAnalyze}
          />
        </section>

        <div className="feed-divider" />

        {/* Error state */}
        {error && (
          <div className="error-banner" role="alert">
            <span>⚠️</span>
            <span>{error}</span>
          </div>
        )}

        {/* Loading skeleton */}
        {loading && (
          <div className="skeleton-wrapper" aria-busy="true" aria-label="Loading analysis">
            <div className="skeleton-avatar skeleton-pulse" />
            <div className="skeleton-lines">
              <div className="skeleton-line skeleton-pulse" style={{ width: '60%' }} />
              <div className="skeleton-line skeleton-pulse" style={{ width: '90%' }} />
              <div className="skeleton-line skeleton-pulse" style={{ width: '75%' }} />
            </div>
          </div>
        )}

        {/* Result */}
        {result && !loading && (
          <ResultCard result={result} originalText={analyzedText} />
        )}

        {/* Empty state */}
        {!result && !loading && !error && (
          <div className="empty-state">
            <div className="empty-icon">🧠</div>
            <h2 className="empty-title">Analyze Indonesian Text</h2>
            <p className="empty-desc">
              Paste a tweet or any Indonesian sentence above and click <strong>Analyze</strong> to detect hate speech using our Naive Bayes + TF-IDF model with lexical normalization.
            </p>
          </div>
        )}
      </main>

      <RightSidebar />
    </div>
  );
}
