export interface ChecklistPanelProps {
  categories: Category[];
  selectedPracticeId?: string;
  onPracticeSelect: (practiceId: string) => void;
  onPracticeToggle: (practiceId: string, checked: boolean) => void;
  onCategoryToggle: (categoryId: string) => void;
  onSearch: (searchTerm: string) => void;
  onFilter: (category: string) => void;
}

export interface Category {
  id: string;
  name: string;
  practices: Practice[];
  isExpanded: boolean;
  completedCount: number;
  totalCount: number;
}

export interface Practice {
  id: string;
  name: string;
  status: 'not_started' | 'in_progress' | 'completed';
  progress: number;
  steps: PracticeStep[];
  isSelected: boolean;
}

export interface PracticeStep {
  id: string;
  name: string;
  status: 'not_started' | 'in_progress' | 'completed';
} 