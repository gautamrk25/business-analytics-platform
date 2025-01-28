export enum PracticeCategory {
    INITIAL_SETUP = 'Initial Setup',
    DATA_PREPARATION = 'Data Preparation',
    PIPELINE_SETUP = 'Pipeline Setup',
    MODEL_DEVELOPMENT = 'Model Development'
}

export interface Practice {
    id: string;
    category: PracticeCategory;
    title: string;
    description: string;
}