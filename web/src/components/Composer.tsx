import { useRef } from 'react';
import { ImageIcon, Smile, Calendar, MapPin } from 'lucide-react';

interface Props {
  text: string;
  loading: boolean;
  onChange: (val: string) => void;
  onSubmit: () => void;
}

const MAX_CHARS = 280;

export default function Composer({ text, loading, onChange, onSubmit }: Props) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const remaining = MAX_CHARS - text.length;
  const isOverLimit = remaining < 0;
  const isEmpty = text.trim().length === 0;

  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    onChange(e.target.value);
    // auto-resize
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      onSubmit();
    }
  };

  return (
    <div className="composer">
      {/* Avatar */}
      <div className="composer-avatar">
        <span>NLP</span>
      </div>

      {/* Right part */}
      <div className="composer-body">
        <textarea
          id="tweet-input"
          ref={textareaRef}
          className="composer-textarea"
          placeholder="Paste Indonesian text to analyze…"
          value={text}
          onChange={handleInput}
          onKeyDown={handleKeyDown}
          rows={3}
          disabled={loading}
        />

        {/* Bottom bar */}
        <div className="composer-footer">
          {/* Media icons */}
          <div className="composer-actions">
            <button className="composer-icon-btn" title="Image" disabled>
              <ImageIcon size={20} />
            </button>
            <button className="composer-icon-btn" title="Emoji" disabled>
              <Smile size={20} />
            </button>
            <button className="composer-icon-btn" title="Poll" disabled>
              <Calendar size={20} />
            </button>
            <button className="composer-icon-btn" title="Location" disabled>
              <MapPin size={20} />
            </button>
          </div>

          <div className="composer-right">
            {/* Character counter */}
            {text.length > 0 && (
              <>
                <div className="char-ring-wrapper" title={`${remaining} characters remaining`}>
                  <svg className="char-ring" viewBox="0 0 36 36">
                    <circle
                      className="char-ring-bg"
                      cx="18" cy="18" r="15"
                      fill="none" strokeWidth="3"
                    />
                    <circle
                      className={`char-ring-fill ${isOverLimit ? 'char-ring-fill--over' : remaining < 20 ? 'char-ring-fill--warn' : ''}`}
                      cx="18" cy="18" r="15"
                      fill="none" strokeWidth="3"
                      strokeDasharray={`${Math.min((text.length / MAX_CHARS) * 94, 94)} 94`}
                      strokeLinecap="round"
                      transform="rotate(-90 18 18)"
                    />
                  </svg>
                  {remaining <= 20 && (
                    <span className={`char-count-text ${isOverLimit ? 'char-count-text--over' : ''}`}>
                      {remaining}
                    </span>
                  )}
                </div>
                <div className="composer-divider" />
              </>
            )}

            {/* Analyze button */}
            <button
              id="analyze-btn"
              className="analyze-btn"
              onClick={onSubmit}
              disabled={isEmpty || isOverLimit || loading}
            >
              {loading ? (
                <span className="spinner" />
              ) : (
                'Analyze'
              )}
            </button>
          </div>
        </div>

        <p className="composer-hint">Ctrl+Enter to analyze</p>
      </div>
    </div>
  );
}
