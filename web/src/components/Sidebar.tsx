import {
  Home,
  Search,
  Bell,
  Mail,
  Bookmark,
  User,
  GitBranch,
  Info,
} from 'lucide-react';

const NAV_ITEMS = [
  { icon: Home, label: 'Home', active: true },
  { icon: Search, label: 'Explore' },
  { icon: Bell, label: 'Notifications' },
  { icon: Mail, label: 'Messages' },
  { icon: Bookmark, label: 'Bookmarks' },
  { icon: Info, label: 'About' },
  { icon: GitBranch, label: 'GitHub' },
  { icon: User, label: 'Profile' },
];

export default function Sidebar() {
  return (
    <aside className="sidebar">
      {/* X Logo */}
      <div className="sidebar-logo">
        <svg viewBox="0 0 24 24" aria-hidden="true" className="x-logo-svg">
          <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
        </svg>
      </div>

      {/* Nav */}
      <nav className="sidebar-nav">
        {NAV_ITEMS.map(({ icon: Icon, label, active }) => (
          <button
            key={label}
            className={`nav-item${active ? ' nav-item--active' : ''}`}
            aria-label={label}
          >
            <Icon size={26} className="nav-icon" />
            <span className="nav-label">{label}</span>
          </button>
        ))}
      </nav>

      {/* Post / Analyze CTA */}
      <button className="tweet-btn">Posting</button>
    </aside>
  );
}
