import { Practice } from './types';

export interface MLOpsTrackerAPI {
    getPractices(): Promise<Practice[]>;
    updatePractice(id: string, updates: Partial<Practice>): Promise<Practice>;
}