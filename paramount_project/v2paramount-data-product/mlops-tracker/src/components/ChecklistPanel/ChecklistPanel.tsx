import { Search, ChevronDown, ChevronRight } from 'lucide-react';
import { useState } from 'react';

interface Practice {
  id: string;
  name: string;
  status: 'complete' | 'in-progress' | 'not-started';
  steps: {
    id: string;
    name: string;
    completed: boolean;
  }[];
}

interface Category {
  id: string;
  name: string;
  practices: Practice[];
}

const mockCategories: Category[] = [
  {
    id: '1',
    name: 'Version Control',
    practices: [
      {
        id: '1-1',
        name: 'Git Repository Setup',
        status: 'complete',
        steps: [
          { id: '1-1-1', name: 'Initialize repo', completed: true },
          { id: '1-1-2', name: 'Add .gitignore', completed: true },
        ]
      },
      {
        id: '1-2',
        name: 'Branching Strategy',
        status: 'in-progress',
        steps: [
          { id: '1-2-1', name: 'Define strategy', completed: true },
          { id: '1-2-2', name: 'Document workflow', completed: false },
        ]
      }
    ]
  },
  {
    id: '2',
    name: 'CI/CD',
    practices: [
      {
        id: '2-1',
        name: 'Pipeline Setup',
        status: 'not-started',
        steps: [
          { id: '2-1-1', name: 'Choose CI tool', completed: false },
          { id: '2-1-2', name: 'Configure builds', completed: false },
        ]
      }
    ]
  }
];

export function ChecklistPanel() {
  console.log('ChecklistPanel mounting');

  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [expandedCategories, setExpandedCategories] = useState<string[]>([]);
  const [selectedPractice, setSelectedPractice] = useState<string | null>(null);

  const categories = mockCategories;
  console.log('Categories data:', categories);

  const toggleCategory = (categoryId: string) => {
    setExpandedCategories(prev =>
      prev.includes(categoryId)
        ? prev.filter(id => id !== categoryId)
        : [...prev, categoryId]
    );
  };

  return (
    <aside className="fixed left-0 top-[64px] w-1/4 h-[calc(100vh-64px)] flex flex-col bg-white border-r border-gray-200 shadow-lg">
      {/* Sticky Header Section */}
      <div className="sticky top-0 z-10 bg-white border-b border-gray-200 px-4 pt-4">
        <h2 className="font-bold text-xl mb-4">MLOps Best Practices</h2>
        {console.log('Rendering header')}
        
        {/* Search Bar */}
        <div className="mb-4">
          <div className="relative">
            <input
              type="text"
              placeholder="Search practices..."
              className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
          </div>
        </div>

        {/* Filter Dropdown */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Filter by:
          </label>
          <select
            className="w-full p-2 border border-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
          >
            <option value="all">All Categories ▼</option>
          </select>
        </div>
      </div>

      {/* Scrollable Content Area */}
      <div className="flex-1 overflow-y-auto">
        {categories?.map((category) => (
          <div 
            key={category.id} 
            className="border-b border-gray-200"
          >
            <button
              onClick={() => toggleCategory(category.id)}
              className="w-full px-4 py-3 flex items-center justify-between hover:bg-gray-50 transition-colors"
            >
              <div className="flex items-center space-x-2">
                {expandedCategories.includes(category.id) ? (
                  <ChevronDown className="w-4 h-4 transition-transform duration-200" />
                ) : (
                  <ChevronRight className="w-4 h-4 transition-transform duration-200" />
                )}
                <span className="font-medium">{category.name}</span>
              </div>
              <span className="text-gray-500 text-sm">
                {/* Add counter here */}
                0/0
              </span>
            </button>

            {/* Practice Items */}
            <div 
              className={`
                overflow-hidden transition-all duration-200 ease-in-out
                ${expandedCategories.includes(category.id) ? 'max-h-[1000px]' : 'max-h-0'}
              `}
            >
              {category.practices?.map((practice) => (
                <div
                  key={practice.id}
                  className={`
                    group pl-10 pr-4 py-2 flex items-center space-x-3 cursor-pointer
                    hover:bg-gray-50 transition-colors
                    ${selectedPractice === practice.id ? 'bg-blue-50 border-l-4 border-blue-500' : ''}
                  `}
                  onClick={() => setSelectedPractice(practice.id)}
                >
                  <input
                    type="checkbox"
                    checked={practice.status === 'complete'}
                    className="rounded border-gray-300 text-blue-500 focus:ring-blue-500"
                    onChange={() => {/* Add toggle handler */}}
                  />
                  <span>{practice.name}</span>
                  <StatusIndicator status={practice.status} />
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </aside>
  );
}

// Helper Components
function StatusIndicator({ status }: { status: Practice['status'] }) {
  const statusConfig = {
    'complete': {
      color: 'text-green-500',
      icon: '✓'
    },
    'in-progress': {
      color: 'text-blue-500',
      icon: '↻'
    },
    'not-started': {
      color: 'text-gray-400',
      icon: '○'
    }
  };

  const config = statusConfig[status];

  return (
    <div className={`ml-auto ${config.color} font-bold`}>
      {config.icon}
    </div>
  );
} 