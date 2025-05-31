import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

interface MLOpsState {
  sections: Record<string, Section>;
  practices: Record<string, Practice>;
  selectedPractices: Set<string>;
  implementations: Record<string, Implementation>;
  
  // Actions
  selectPractice: (practiceId: string) => void;
  startImplementation: (practiceId: string) => void;
  updateProgress: (practiceId: string, phase: string, progress: number) => void;
  completeImplementation: (practiceId: string) => void;
}

export const useMLOpsStore = create<MLOpsState>()(
  devtools(
    persist(
      (set, get) => ({
        sections: {},
        practices: {},
        selectedPractices: new Set(),
        implementations: {},

        selectPractice: (practiceId) => 
          set((state) => {
            const selected = new Set(state.selectedPractices);
            if (selected.has(practiceId)) {
              selected.delete(practiceId);
            } else {
              selected.add(practiceId);
            }
            return { selectedPractices: selected };
          }),

        startImplementation: (practiceId) =>
          set((state) => ({
            implementations: {
              ...state.implementations,
              [practiceId]: {
                status: 'in_progress',
                startedAt: new Date(),
                phases: {
                  codeGeneration: { status: 'pending', progress: 0 },
                  resourceDeployment: { status: 'pending', progress: 0 },
                  testing: { status: 'pending', progress: 0 }
                }
              }
            }
          })),

        // ... other actions
      }),
      {
        name: 'mlops-storage'
      }
    )
  )
); 