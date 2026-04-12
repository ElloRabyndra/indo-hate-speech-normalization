import { Search, MoreHorizontal } from 'lucide-react';

const TRENDS = [
  { category: 'NLP · Trending', topic: '#LexicalNormalization', posts: '12,4 rb' },
  { category: 'Sedang tren dalam topik Indonesia', topic: '#HateSpeech', posts: '8.941' },
  { category: 'AI · Trending', topic: '#NaiveBayes', posts: '5.102' },
  { category: 'Sedang tren dalam topik Indonesia', topic: '#TF-IDF', posts: '3.751' },
  { category: 'Sedang tren dalam topik Indonesia', topic: '#TwitterNLP', posts: '2.287' },
];

export default function RightSidebar() {
  return (
    <aside className="right-sidebar">
      {/* Search bar */}
      <div className="search-bar">
        <Search size={16} className="search-icon-svg" />
        <input className="search-input" type="text" placeholder="Cari" readOnly />
      </div>

      {/* Sedang hangat dibicarakan */}
      <div className="widget">
        <h2 className="widget-title">Sedang hangat dibicarakan</h2>
        {TRENDS.map((t) => (
          <div key={t.topic} className="trend-item">
            <div className="trend-left">
              <span className="trend-category">{t.category}</span>
              <span className="trend-topic">{t.topic}</span>
              <span className="trend-count">{t.posts} postingan</span>
            </div>
            <button className="trend-more" aria-label="More">
              <MoreHorizontal size={16} />
            </button>
          </div>
        ))}
        <button className="show-more">Tampilkan lebih banyak</button>
      </div>

      <p className="footer-links">
        Ketentuan Layanan · Kebijakan Privasi · Kebijakan Cookie · Aksesibilitas · Info Iklan · Lainnya ·
        <br />© 2025 X Corp.
      </p>
    </aside>
  );
}
