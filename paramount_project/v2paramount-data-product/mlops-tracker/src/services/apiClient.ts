import { MLOpsTrackerAPI } from '../interfaces/api';
import { mockPractices } from './mockData';

export class ApiClient implements MLOpsTrackerAPI {
    async getPractices() {
        return mockPractices;
    }
    
    async updatePractice(id: string, updates: any) {
        // Mock implementation
        return { ...mockPractices[0], ...updates };
    }
}