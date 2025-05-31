import React from 'react';
import { Database, Box, Play, LineChart, Settings, Upload, Monitor, GitBranch, Focus, Server, FileStack, Shield } from 'lucide-react';

const WorkflowStep = ({ icon: Icon, title, description, subSteps, isLast }) => (
  <div className="flex items-start space-x-4">
    <div className="flex flex-col items-center">
      <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center">
        <Icon className="w-5 h-5 text-blue-600" />
      </div>
      {!isLast && <div className="w-0.5 h-8 bg-gray-200 mt-2"></div>}
    </div>
    <div className="flex-1">
      <h3 className="font-medium text-lg">{title}</h3>
      <p className="text-gray-600 mt-1">{description}</p>
      {subSteps && (
        <div className="mt-2 space-y-1">
          {subSteps.map((step, idx) => (
            <label key={idx} className="flex items-start gap-2 text-sm text-gray-600 ml-4 cursor-pointer hover:bg-gray-50 p-1 rounded">
              <input 
                type="checkbox" 
                className="mt-1 rounded text-blue-600 focus:ring-blue-500"
                defaultChecked={true}
              />
              <span>{step}</span>
            </label>
          ))}
        </div>
      )}
    </div>
  </div>
);

const VertexAIWorkflow = () => {
  const steps = [
    {
      icon: Shield,
      title: "1. Initial Setup & Infrastructure",
      description: "Configure base infrastructure and security",
      subSteps: [
        "Configure compute resources and networking",
        "Set up access controls and service accounts",
        "Enable audit logging and security configurations",
        "Configure cost monitoring",
        "Set up backup and recovery procedures",
        "Configure Vertex AI Workbench environment",
        "Set up Artifact Registry for storing container images",
        "Configure Cloud Build for CI/CD pipelines"
      ]
    },
    {
      icon: Database,
      title: "2. Data Preparation & Feature Engineering",
      description: "Comprehensive data preparation and feature management",
      subSteps: [
        "Connect to Cloud Storage and BigQuery",
        "Perform initial EDA in Vertex AI Workbench",
        "Set up Dataproc Serverless Spark for large-scale processing",
        "Implement data validation and quality checks",
        "Create feature definitions in Feature Store",
        "Configure feature computation pipelines",
        "Set up online feature serving",
        "Set up offline feature serving",
        "Split data into training, validation, and test sets",
        "Implement data versioning using Vertex AI Datasets",
        "Set up data labeling workflows if applicable"
      ]
    },
    {
      icon: Box,
      title: "3. Pipeline Setup",
      description: "Set up core pipeline infrastructure",
      subSteps: [
        "Define core pipeline components",
        "Create data preprocessing pipeline",
        "Set up validation pipeline",
        "Configure pipeline triggers",
        "Implement error handling",
        "Set up pipeline monitoring",
        "Configure CI/CD integration",
        "Test pipeline end-to-end",
        "Implement Vertex AI Pipelines for workflow orchestration",
        "Set up pipeline components using KFP or TFX"
      ]
    },
    {
      icon: Settings,
      title: "4. Model Development",
      description: "Comprehensive model development approach",
      subSteps: [
        "Evaluate AutoML vs custom training approach",
        "Set up development environment in Workbench",
        "Configure Ray framework for distributed training",
        "Set up Ray clusters",
        "Implement custom algorithms",
        "Test Model Garden pre-built models",
        "Evaluate Generative AI models if applicable",
        "Integrate with chosen ML frameworks",
        "Implement distributed training configuration",
        "Implement feature selection algorithms (e.g., AMI, CMIM, JMIM, MRMR)",
        "Set up Vertex AI TensorBoard for experiment visualization"
      ]
    },
    {
      icon: Focus,
      title: "5. Experimentation & Optimization",
      description: "Track and optimize model experiments",
      subSteps: [
        "Set up Vertex AI Experiments tracking",
        "Configure experiment metadata logging",
        "Implement version control for experiments",
        "Configure Vizier for hyperparameter tuning",
        "Run initial training experiments",
        "Compare ML techniques",
        "Document experiment results",
        "Select best performing model approach",
        "Implement cross-validation strategies",
        "Set up automated model evaluation metrics"
      ]
    },
    {
      icon: GitBranch,
      title: "6. Model Registry & Versioning",
      description: "Comprehensive model lifecycle management",
      subSteps: [
        "Set up model registry structure",
        "Configure dev/staging/prod environments",
        "Define model versioning strategy",
        "Implement model approval workflow",
        "Set up model promotion criteria",
        "Configure model artifact tracking",
        "Document model dependencies",
        "Implement model lineage tracking",
        "Implement model governance policies",
        "Set up model metadata tracking using Vertex AI ML Metadata"
      ]
    },
    {
      icon: Server,
      title: "7. Model Deployment",
      description: "Multi-environment model deployment and serving",
      subSteps: [
        "Set up deployment pipelines",
        "Configure Ray clusters for serving",
        "Implement deployment validation tests",
        "Set up canary deployment process",
        "Configure A/B testing framework",
        "Set up autoscaling rules",
        "Configure batch prediction jobs",
        "Implement rollback procedures",
        "Deploy to initial environment",
        "Implement blue-green deployment strategies",
        "Set up model monitoring for deployed models"
      ]
    },
    {
      icon: Monitor,
      title: "8. Monitoring & Maintenance",
      description: "Comprehensive model monitoring and maintenance",
      subSteps: [
        "Set up basic model monitoring",
        "Configure training-serving skew detection",
        "Implement prediction drift monitoring",
        "Set up Explainable AI tooling",
        "Configure endpoint performance monitoring",
        "Set up Feature Store monitoring",
        "Configure alerting thresholds",
        "Implement automated retraining triggers",
        "Document maintenance procedures",
        "Implement continuous evaluation of model performance",
        "Set up automated model retraining pipelines"
      ]
    }
  ];

  return (
    <div className="bg-white rounded-lg shadow-lg w-full">
      <div className="p-6 border-b">
        <p className="text-gray-600 mb-4 text-xl">
          Focus on data science, Shorten Time to Value. 
          Onix handles the complexity and applies practices that improve the stability and reliability of your ML systems
        </p>
        <h2 className="text-xl font-bold">Comprehensive Vertex AI MLOps Workflow</h2>
      </div>
      <div className="p-6">
        <div className="space-y-6">
          {steps.map((step, index) => (
            <WorkflowStep
              key={index}
              icon={step.icon}
              title={step.title}
              description={step.description}
              subSteps={step.subSteps}
              isLast={index === steps.length - 1}
            />
          ))}
        </div>
      </div>
    </div>
  );
}

export default VertexAIWorkflow;