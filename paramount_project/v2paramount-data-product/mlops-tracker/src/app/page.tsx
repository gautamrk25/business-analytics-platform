import { ChecklistPanel } from '@/components/ChecklistPanel/ChecklistPanel';

export default function Home() {
  // Mock data for testing
  const mockCategories = [
    {
      id: '1',
      name: 'Version Control',
      practices: [],
      isExpanded: true,
      completedCount: 0,
      totalCount: 3
    }
  ];

  return (
    <div className="relative flex">
      <ChecklistPanel 
        categories={mockCategories}
        onPracticeSelect={(id) => console.log('Selected:', id)}
        onPracticeToggle={(id, checked) => console.log('Toggled:', id, checked)}
        onCategoryToggle={(id) => console.log('Category:', id)}
        onSearch={(term) => console.log('Search:', term)}
        onFilter={(category) => console.log('Filter:', category)}
      />
      <main className="flex-1 ml-[25%] p-6">
        Main Content Area
      </main>
    </div>
  );
} 