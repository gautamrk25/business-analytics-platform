import { useState } from 'react';
import { Header } from './Header';

export function HeaderPreview() {
  const [activePath, setActivePath] = useState('/');

  return (
    <div className="min-h-screen bg-gray-100 pt-16">
      <Header
        notifications={3}
        userName="Jane Smith"
        activePath={activePath}
        onNavigate={setActivePath}
      />
      <main className="max-w-7xl mx-auto p-4">
        <h2 className="text-2xl font-bold">Current Page: {activePath}</h2>
      </main>
    </div>
  );
} 