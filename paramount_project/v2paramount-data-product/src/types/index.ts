// Core Types
interface Practice {
  id: string;
  name: string;
  sectionId: string;
  description: string;
  status: 'not_started' | 'in_progress' | 'completed';
  code: {
    template: string;
    current: string;
    language: string;
  };
  implementation: {
    codeGeneration: ProgressState;
    resourceDeployment: ProgressState;
    testing: ProgressState;
  };
  resources: Resource[];
  dependencies: string[]; // IDs of practices that must be completed first
}

interface Section {
  id: string;
  title: string;
  icon: string;
  order: number;
  practices: string[]; // Practice IDs
}

interface Resource {
  id: string;
  type: string;
  name: string;
  status: 'pending' | 'active' | 'failed';
  details: Record<string, any>;
  metrics: ResourceMetrics;
}

interface ProgressState {
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  progress: number;
  startedAt?: Date;
  completedAt?: Date;
  error?: string;
}