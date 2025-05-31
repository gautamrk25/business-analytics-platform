import React from 'react';
import { Library } from 'lucide-react';

const Card = ({ children, className = '' }) => (
  <div className={`bg-white dark:bg-gray-800 rounded-lg shadow-lg text-sm ${className}`}>
    {children}
  </div>
);

const ResourcesPage = () => {
  return (
    <Card className="w-full">
      <div className="p-8 flex flex-col items-center justify-center text-center">
        <Library className="w-16 h-16 text-blue-500 mb-4" />
        <h2 className="text-2xl font-semibold mb-4">Coming Soon</h2>
        <p className="text-gray-600 dark:text-gray-400">
          Resource library is being built. Check back later!
        </p>
      </div>
    </Card>
  );
};

export default ResourcesPage; 