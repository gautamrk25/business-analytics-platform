export type PracticeStatus = 'not_started' | 'in_progress' | 'completed';
export type PracticeCategory = 
  | 'initial_setup' 
  | 'data_preparation' 
  | 'pipeline_setup'
  | 'model_development'
  | 'experimentation'
  | 'model_registry'
  | 'model_deployment'
  | 'monitoring';

export interface Practice {
  id: string;
  name: string;
  category: PracticeCategory;
  description: string;
  status: PracticeStatus;
  progress: number; // 0-100
  selected?: boolean;
  steps: PracticeStep[];
}

export interface PracticeStep {
  id: string;
  name: string;
  status: PracticeStatus;
  progress: number;
  codeTemplate?: string;
  resources?: DeployedResource[];
}

export interface DeployedResource {
  id: string;
  name: string;
  type: string;
  status: 'pending' | 'active' | 'failed';
  details: string;
  lastUpdated: Date;
}

export interface Notification {
  id: string;
  title: string;
  message: string;
  timestamp: Date;
  read: boolean;
  type: 'success' | 'warning' | 'error' | 'info';
} 