import { Practice, PracticeCategory } from '../types/practice';

export const getPractices = async (): Promise<Practice[]> => {
  // Simulated API call
  return mockPractices;
};

const mockPractices: Practice[] = [
  {
    id: '1',
    name: 'Configure Compute Resources',
    category: 'initial_setup',
    description: 'Set up and configure compute resources for ML workloads',
    status: 'completed',
    progress: 100,
    selected: true,
    steps: [
      {
        id: 's1',
        name: 'Code Generation',
        status: 'completed',
        progress: 100,
        codeTemplate: '# Configure compute\n...'
      },
      // ... more steps
    ]
  },
  // ... more practices
]; 