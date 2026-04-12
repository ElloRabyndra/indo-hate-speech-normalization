import type { AnalysisResult } from '../types';
import { CheckCircle, AlertTriangle, MessageCircle, Heart, Repeat2, Share } from 'lucide-react';

interface Props {
  result: AnalysisResult;
  originalText: string;
}

const NOW = new Date().toLocaleTimeString('en-US', {
  hour: '2-digit',
  minute: '2-digit',
});

const DATE = new Date().toLocaleDateString('en-US', {
  month: 'long',
  day: 'numeric',
  year: 'numeric',
});

export default function ResultCard({ result, originalText }: Props) {
  const isHate = result.label === 'Hate Speech';
  const pct = Math.round(result.probability * 100);

  return (
    <article className={`result-card result-card--${isHate ? 'hate' : 'safe'}`} id="result-card">
      {/* Accent bar */}
      <div className={`result-accent-bar result-accent-bar--${isHate ? 'hate' : 'safe'}`} />

      {/* Card header */}
      <div className="tweet-header">
        <div className="tweet-avatar">
          <span>AI</span>
        </div>

        <div className="tweet-meta">
          <span className="tweet-name">NLP Analyzer</span>
          <span className="tweet-handle">@nlp_analyze · {NOW}</span>
        </div>

        {/* Label badge */}
        <div className={`label-badge label-badge--${isHate ? 'hate' : 'safe'}`}>
          {isHate
            ? <><AlertTriangle size={14} /> Hate Speech</>
            : <><CheckCircle size={14} /> Non Hate Speech</>}
        </div>
      </div>

      {/* Original text */}
      <p className="tweet-body">{originalText}</p>

      {/* Confidence */}
      <div className="confidence-section">
        <div className="confidence-header">
          <span className="confidence-label">Confidence</span>
          <span className={`confidence-pct confidence-pct--${isHate ? 'hate' : 'safe'}`}>
            {pct}%
          </span>
        </div>
        <div className="confidence-bar-track">
          <div
            className={`confidence-bar-fill confidence-bar-fill--${isHate ? 'hate' : 'safe'}`}
            style={{ width: `${pct}%` }}
          />
        </div>
      </div>

      {/* Processed text */}
      {result.processed_text && (
        <details className="processed-details">
          <summary className="processed-summary">View preprocessed text</summary>
          <p className="processed-body">{result.processed_text || '(empty after preprocessing)'}</p>
        </details>
      )}

      {/* Pipeline stages badge row */}
      <div className="pipeline-badges">
        {['Tokenize', 'Slang Norm', 'Abbrev Expand', 'Stopword', 'Stem', 'TF-IDF', 'Naive Bayes'].map(
          (step) => (
            <span key={step} className="pipeline-badge">{step}</span>
          )
        )}
      </div>

      {/* Tweet footer — date + fake interactions */}
      <div className="tweet-timestamp">{NOW} · {DATE} · <strong>Indonesian NLP</strong></div>

      <div className="tweet-stats">
        <span><strong>1</strong> Retweet</span>
        <span><strong>5</strong> Quote Tweets</span>
        <span><strong>12</strong> Likes</span>
      </div>

      <div className="tweet-actions">
        <button className="tweet-action-btn" aria-label="Reply"><MessageCircle size={18} /></button>
        <button className="tweet-action-btn" aria-label="Retweet"><Repeat2 size={18} /></button>
        <button className="tweet-action-btn tweet-action-btn--like" aria-label="Like"><Heart size={18} /></button>
        <button className="tweet-action-btn" aria-label="Share"><Share size={18} /></button>
      </div>
    </article>
  );
}
