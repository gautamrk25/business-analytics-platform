import { useState } from 'react';

export function Header() {
  const [notificationsOpen, setNotificationsOpen] = useState(false);

  return (
    <header className="bg-white shadow">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-6">
            <h1 className="text-2xl font-bold text-gray-900">
              MLOps Implementation Tracker
            </h1>
            <nav className="space-x-4">
              <button className="text-gray-600 hover:text-gray-900">Home</button>
              <button className="text-gray-600 hover:text-gray-900">Documentation</button>
              <button className="text-gray-600 hover:text-gray-900">Settings</button>
            </nav>
          </div>
          
          <div className="flex items-center space-x-4">
            <button 
              className="relative p-2"
              onClick={() => setNotificationsOpen(!notificationsOpen)}
            >
              <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                3
              </span>
              <span className="sr-only">Notifications</span>
              <svg className="h-6 w-6 text-gray-600" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
                <path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path>
              </svg>
            </button>
            
            <button className="flex items-center space-x-2">
              <img 
                className="h-8 w-8 rounded-full"
                src="https://via.placeholder.com/32"
                alt="User profile"
              />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
} 