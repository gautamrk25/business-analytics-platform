import React, { useState, useRef, useEffect } from 'react';
import { 
  Brain, Box, Play, Focus, GitBranch, Server, Upload, Monitor, 
  Users, Heart, Sparkles, Database, Table, Target, FileStack, Check, Shield, Bot
} from 'lucide-react';
import VertexAIWorkflow from './VertexAIWorkflow';
import ActivationDashboard from './ActivationDashboard';
import { motion } from 'framer-motion';

// Add back the workflowSteps constant
const workflowSteps = [
  {
    id: 'feature-mgmt',
    icon: Database,
    title: "Feature Management",
    description: "Use Phoenix AI Feature Store for feature engineering and serving",
    subSteps: [
      "Create and manage feature definitions",
      "Set up online and offline feature serving",
      "Implement feature computation pipelines",
      "Enable real-time feature serving"
    ]
  },
  {
    id: 'pipeline',
    icon: Box,
    title: "Pipeline Orchestration",
    description: "Orchestrate ML workflows using Phoenix AI Pipelines",
    subSteps: [
      "Define pipeline components for each stage",
      "Set up data validation and preprocessing steps",
      "Configure model training and evaluation components",
      "Implement automated deployment pipelines"
    ]
  },
  {
    id: 'experimentation',
    icon: Focus,
    title: "Experimentation",
    description: "Track and manage experiments using Phoenix AI Experiments",
    subSteps: [
      "Log training runs and parameters",
      "Track model metrics and artifacts",
      "Compare experiment results",
      "Version control for experiment configurations"
    ]
  },
  {
    id: 'registry',
    icon: GitBranch,
    title: "Model Registry & Versioning",
    description: "Manage model lifecycle in Phoenix AI Model Registry",
    subSteps: [
      "Version models (dev/staging/prod)",
      "Track model metadata and lineage",
      "Implement model tagging system",
      "Manage model promotion workflow"
    ]
  },
  {
    id: 'deployment',
    icon: Server,
    title: "Deployment",
    description: "Deploy and serve models across environments",
    subSteps: [
      "Configure endpoints for different stages",
      "Set up A/B testing capabilities",
      "Implement deployment validation",
      "Enable rollback procedures"
    ]
  },
  {
    id: 'monitoring',
    icon: Monitor,
    title: "Monitoring & Maintenance",
    description: "Monitor model performance using Phoenix AI Monitoring",
    subSteps: [
      "Track model metrics and predictions",
      "Set up custom monitoring solutions",
      "Configure drift detection",
      "Implement automated retraining triggers"
    ]
  }
];

const MLLifecycleDashboard = ({ defaultView = 'bestPractices' }) => {
  const [selectedView, setSelectedView] = useState(defaultView);
  const [selectedSteps, setSelectedSteps] = useState(new Set([
    'Data Preparation & Feature Engineering',
    'Pipeline Orchestration',
    'Model Development',
    'Experimentation & Optimization',
    'Model Registry & Versioning',
    'Model Deployment',
    'Monitoring & Maintenance',
    'Infrastructure & Security'
  ]));
  const [showWorkflowVisualization, setShowWorkflowVisualization] = useState(defaultView === 'useCases');
  const [activeButton, setActiveButton] = useState('bestPractices');

  // Handler for view switching
  const handleViewSwitch = (view) => {
    setSelectedView(view);
    // When switching to use cases, ensure workflow visualization is shown
    if (view === 'useCases') {
      setShowWorkflowVisualization(true);
    }
  };

  const buttons = [
    {
      id: 'bestPractices',
      label: 'Best Practices',
      icon: FileStack,
      onClick: () => {
        window.open('https://confluence.paramount.com/display/DSAI/MLOps+Best+Practices', '_blank');
        setActiveButton('bestPractices');
      },
    },
    {
      id: 'phoenixMLOps',
      label: 'Phoenix MLOps',
      icon: Bot,
      onClick: () => {
        window.open('http://localhost:8000/develop', '_blank');
        setActiveButton('phoenixMLOps');
      },
    },
  ];

  return (
    <div className="space-y-4">
      {/* View Selection Buttons */}
      <div className="flex gap-2">
        {buttons.map((button) => (
          <button
            key={button.id}
            onClick={button.onClick}
            className={`px-3 py-1.5 rounded-lg text-sm transition-colors flex items-center gap-1 ${
              activeButton === button.id
                ? 'bg-blue-100 text-blue-700'
                : 'bg-gray-100 hover:bg-gray-200'
            }`}
          >
            <button.icon className="w-3.5 h-3.5" />
            {button.label}
          </button>
        ))}
      </div>

      {/* Content */}
      <div className="w-full">
        {selectedView === 'bestPractices' ? (
          <VertexAIWorkflow 
            onStepSelect={(step, checked) => {
              setSelectedSteps(prev => {
                const newSet = new Set(prev);
                if (checked) {
                  newSet.add(step);
                } else {
                  newSet.delete(step);
                }
                return newSet;
              });
            }} 
          />
        ) : (
          <div className="bg-white rounded-lg shadow-sm border">
            <div className="p-4 border-b">
              <h2 className="text-lg font-medium">Use Cases</h2>
            </div>
            <div className="p-4">
              <UseCaseWorkflow 
                selectedBestPractices={selectedSteps}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

// Update the UseCaseWorkflow component styling
const UseCaseWorkflow = ({ selectedBestPractices }) => {
  const [workflowProgress, setWorkflowProgress] = useState({});
  
  // Group stages by major MLOps phases
  const workflowPhases = {
    preparation: {
      title: 'Data & Feature Engineering',
      steps: ['Data Preparation & Feature Engineering', 'Pipeline Orchestration'],
      icon: Database,
      color: 'blue'
    },
    development: {
      title: 'Model Development & Experimentation',
      steps: ['Model Development', 'Experimentation & Optimization'],
      icon: Brain,
      color: 'green'
    },
    deployment: {
      title: 'Deployment & Operations',
      steps: ['Model Registry & Versioning', 'Model Deployment', 'Monitoring & Maintenance'],
      icon: Server,
      color: 'purple'
    },
    infrastructure: {
      title: 'Infrastructure & Security',
      steps: ['Infrastructure & Security'],
      icon: Shield,
      color: 'orange'
    }
  };

  return (
    <div className="space-y-4">
      {/* Phase-based workflow visualization */}
      {Object.entries(workflowPhases).map(([phaseKey, phase]) => {
        const isPhaseActive = phase.steps.some(step => selectedBestPractices.has(step));
        
        if (!isPhaseActive) return null;

        return (
          <motion.div
            key={phaseKey}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="border rounded-lg p-4"
          >
            {/* Phase Header - Increased font size */}
            <div className="flex items-center gap-2 mb-3">
              <phase.icon className={`w-5 h-5 text-${phase.color}-600`} />
              <h3 className="text-lg font-medium">{phase.title}</h3>
            </div>

            {/* Selected Best Practices for this phase */}
            <div className="grid grid-cols-2 gap-4">
              {phase.steps.filter(step => selectedBestPractices.has(step)).map(step => (
                <motion.div
                  key={step}
                  className={`bg-${phase.color}-50 p-3 rounded-lg border border-${phase.color}-200`}
                >
                  {/* Increased font size for step title */}
                  <h4 className={`text-base font-medium text-${phase.color}-700 mb-2`}>{step}</h4>
                  <div className="space-y-1">
                    {/* Increased font size for sub-steps */}
                    {workflowSteps.find(ws => ws.title === step)?.subSteps.map((subStep, idx) => (
                      <div key={idx} className="flex items-center gap-1.5">
                        <Check className="w-3.5 h-3.5 text-green-500 flex-shrink-0" />
                        <span className="text-base text-gray-600">{subStep}</span>
                      </div>
                    ))}
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        );
      })}
    </div>
  );
};

export default MLLifecycleDashboard; 