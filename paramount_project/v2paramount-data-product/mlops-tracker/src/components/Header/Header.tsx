import { useState } from 'react';
import { Home, BookOpen, Settings, Bell, User, Menu } from 'lucide-react';

interface HeaderProps {
  notifications?: number;
  userName?: string;
  onNavigate?: (path: string) => void;
  activePath?: string;
}

export function Header({
  notifications = 0,
  userName = 'John Doe',
  onNavigate = () => {},
  activePath = '/'
}: HeaderProps) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const navItems = [
    { icon: Home, label: 'Home', path: '/' },
    { icon: BookOpen, label: 'Documentation', path: '/docs' },
    { icon: Settings, label: 'Settings', path: '/settings' }
  ];

  return (
    <header className="fixed top-0 w-full h-16 bg-blue-900 text-white shadow-lg">
      <div className="max-w-7xl mx-auto h-full px-4">
        <div className="flex items-center justify-between h-full">
          {/* Brand Section */}
          <div className="w-1/4">
            <h1 className="text-lg font-semibold">
              <span className="lg:inline hidden">MLOps AI Agent</span>
              <span className="lg:hidden md:inline hidden">MLOps AI</span>
              <span className="md:hidden">MLOps</span>
            </h1>
          </div>

          {/* Navigation - Desktop */}
          <nav className="hidden md:flex w-1/2 justify-center">
            <ul className="flex space-x-8">
              {navItems.map(({ icon: Icon, label, path }) => (
                <li key={path}>
                  <button
                    onClick={() => onNavigate(path)}
                    className={`flex flex-col items-center group relative py-1 px-3
                      hover:bg-white/10 rounded transition-colors`}
                  >
                    <Icon className="w-4 h-4 mb-1" />
                    <span className="text-sm">{label}</span>
                    {activePath === path && (
                      <div className="absolute bottom-0 left-0 w-full h-0.5 bg-orange-500" />
                    )}
                  </button>
                </li>
              ))}
            </ul>
          </nav>

          {/* User Controls */}
          <div className="flex items-center justify-end w-1/4 space-x-4">
            <button className="relative p-2 hover:bg-white/10 rounded">
              <Bell className="w-5 h-5" />
              {notifications > 0 && (
                <span className="absolute top-0 right-0 w-4 h-4 bg-red-500 rounded-full text-xs flex items-center justify-center">
                  {notifications}
                </span>
              )}
            </button>
            
            <div className="hidden md:flex items-center space-x-2">
              <User className="w-5 h-5" />
              <span className="text-sm">{userName}</span>
            </div>

            {/* Mobile Menu Button */}
            <button 
              className="md:hidden p-2 hover:bg-white/10 rounded"
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            >
              <Menu className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation Menu */}
      {isMobileMenuOpen && (
        <div className="md:hidden absolute top-16 left-0 w-full bg-blue-900 border-t border-white/10">
          <nav className="px-4 py-2">
            <ul className="space-y-2">
              {navItems.map(({ icon: Icon, label, path }) => (
                <li key={path}>
                  <button
                    onClick={() => {
                      onNavigate(path);
                      setIsMobileMenuOpen(false);
                    }}
                    className="flex items-center space-x-3 w-full p-3 hover:bg-white/10 rounded"
                  >
                    <Icon className="w-4 h-4" />
                    <span>{label}</span>
                  </button>
                </li>
              ))}
            </ul>
          </nav>
        </div>
      )}
    </header>
  );
} 