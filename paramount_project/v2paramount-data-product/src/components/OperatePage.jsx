import React, { useState } from 'react';
import { Search, MessageSquare, AlertTriangle, Activity, Shield, Leaf, 
         Database, Code, DollarSign, BrainCircuit, AlertCircle, CheckCircle, TrendingUp, Users, 
         FileText, Bell, Filter, BarChart2, ChevronDown, 
         Clock, Zap, GitBranch, Timer, RefreshCw, ArrowLeft, Brain, Cpu, Bot, LineChart, ArrowRight } from 'lucide-react';

const CopilotIcon = ({ className = "w-5 h-5" }) => (
  <svg 
    viewBox="0 0 24 24" 
    className={className}
    fill="currentColor"
  >
    <path d="M12 2L9 9H2L7 14L5 21L12 17L19 21L17 14L22 9H15L12 2Z" />
  </svg>
);

const Card = ({ children, className = '' }) => (
  <div className={`bg-white dark:bg-gray-800 rounded-lg shadow-lg text-sm ${className}`}>
    {children}
  </div>
);

const ProcessingTimelineChart = () => {
  // Sample hourly data for the last 24 hours
  const data = [
    { hour: '00:00', activeJobs: 245, queuedJobs: 12, avgProcessingTime: 1.2, throughput: 2.8 },
    { hour: '01:00', activeJobs: 232, queuedJobs: 15, avgProcessingTime: 1.3, throughput: 2.6 },
    { hour: '02:00', activeJobs: 218, queuedJobs: 18, avgProcessingTime: 1.4, throughput: 2.5 },
    { hour: '03:00', activeJobs: 225, queuedJobs: 14, avgProcessingTime: 1.2, throughput: 2.7 },
    { hour: '04:00', activeJobs: 238, queuedJobs: 10, avgProcessingTime: 1.1, throughput: 2.9 },
    { hour: '05:00', activeJobs: 252, queuedJobs: 8, avgProcessingTime: 1.0, throughput: 3.0 },
    { hour: '06:00', activeJobs: 265, queuedJobs: 11, avgProcessingTime: 1.1, throughput: 2.8 },
    { hour: '07:00', activeJobs: 278, queuedJobs: 13, avgProcessingTime: 1.2, throughput: 2.7 },
    { hour: '08:00', activeJobs: 285, queuedJobs: 15, avgProcessingTime: 1.3, throughput: 2.6 },
    { hour: '09:00', activeJobs: 292, queuedJobs: 14, avgProcessingTime: 1.2, throughput: 2.7 },
    { hour: '10:00', activeJobs: 288, queuedJobs: 12, avgProcessingTime: 1.1, throughput: 2.8 },
    { hour: '11:00', activeJobs: 275, queuedJobs: 10, avgProcessingTime: 1.0, throughput: 2.9 },
    { hour: '12:00', activeJobs: 268, queuedJobs: 9, avgProcessingTime: 1.0, throughput: 3.0 },
    { hour: '13:00', activeJobs: 262, queuedJobs: 11, avgProcessingTime: 1.1, throughput: 2.9 },
    { hour: '14:00', activeJobs: 255, queuedJobs: 13, avgProcessingTime: 1.2, throughput: 2.8 },
    { hour: '15:00', activeJobs: 248, queuedJobs: 14, avgProcessingTime: 1.3, throughput: 2.7 },
    { hour: '16:00', activeJobs: 242, queuedJobs: 12, avgProcessingTime: 1.2, throughput: 2.8 },
    { hour: '17:00', activeJobs: 235, queuedJobs: 10, avgProcessingTime: 1.1, throughput: 2.9 },
    { hour: '18:00', activeJobs: 228, queuedJobs: 9, avgProcessingTime: 1.0, throughput: 3.0 },
    { hour: '19:00', activeJobs: 235, queuedJobs: 11, avgProcessingTime: 1.1, throughput: 2.9 },
    { hour: '20:00', activeJobs: 242, queuedJobs: 13, avgProcessingTime: 1.2, throughput: 2.8 },
    { hour: '21:00', activeJobs: 248, queuedJobs: 14, avgProcessingTime: 1.3, throughput: 2.7 },
    { hour: '22:00', activeJobs: 245, queuedJobs: 12, avgProcessingTime: 1.2, throughput: 2.8 },
    { hour: '23:00', activeJobs: 245, queuedJobs: 12, avgProcessingTime: 1.2, throughput: 2.8 },
  ];

  const metrics = [
    { name: 'Active Jobs', color: 'rgb(59, 130, 246)', key: 'activeJobs', maxValue: 300 },
    { name: 'Queued Jobs', color: 'rgb(139, 92, 246)', key: 'queuedJobs', maxValue: 20 },
    { name: 'Avg Processing Time (s)', color: 'rgb(16, 185, 129)', key: 'avgProcessingTime', maxValue: 2 },
    { name: 'Throughput (TB/hr)', color: 'rgb(245, 158, 11)', key: 'throughput', maxValue: 4 },
  ];

  return (
    <div className="h-80 relative p-4">
      {/* Y-axis */}
      <div className="absolute left-0 top-0 bottom-20 w-16 flex flex-col justify-between text-xs text-gray-500">
        {[...Array(6)].map((_, i) => (
          <span key={i} className="text-right w-full pr-2">
            {(5 - i) * 20}%
          </span>
        ))}
      </div>

      {/* Chart area */}
      <div className="ml-16 h-full">
        {/* Grid lines */}
        <div className="absolute left-16 right-4 top-0 bottom-20 grid grid-rows-5 gap-0">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="border-t border-gray-200" />
          ))}
        </div>

        {/* Lines for each metric */}
        <svg className="absolute left-16 right-4 top-0 bottom-20 h-[calc(100%-80px)] w-[calc(100%-80px)]">
          {metrics.map((metric) => (
            <g key={metric.key}>
              <path
                d={`M ${data.map((d, i) => `${(i * 100) / (data.length - 1)}% ${100 - (d[metric.key] / metric.maxValue) * 100}%`).join(' L ')}`}
                stroke={metric.color}
                strokeWidth="2"
                fill="none"
              />
              {data.map((d, i) => (
                <circle
                  key={i}
                  cx={`${(i * 100) / (data.length - 1)}%`}
                  cy={`${100 - (d[metric.key] / metric.maxValue) * 100}%`}
                  r="3"
                  fill="white"
                  stroke={metric.color}
                  strokeWidth="2"
                  className="hover:r-4 transition-all duration-200"
                />
              ))}
            </g>
          ))}
        </svg>

        {/* X-axis labels */}
        <div className="absolute left-16 right-4 bottom-12 flex justify-between text-xs text-gray-500">
          {data.filter((_, i) => i % 2 === 0).map((d) => (
            <span key={d.hour} className="transform -rotate-45 origin-top-left">
              {d.hour}
            </span>
          ))}
        </div>

        {/* Legend moved to bottom */}
        <div className="absolute left-16 right-4 bottom-0 flex justify-between items-center pt-2">
          {metrics.map((metric) => (
            <div key={metric.name} className="flex items-center space-x-2">
              <div className="w-3 h-3 rounded-full" style={{ backgroundColor: metric.color }}></div>
              <span className="text-xs text-gray-600 whitespace-nowrap">{metric.name}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

const EscalationLevel = ({ icon: Icon, title, status, actions, condition }) => (
  <div className="bg-white p-6 rounded-lg shadow-md mb-4">
    <div className="flex items-center gap-3 mb-3">
      <Icon className="w-6 h-6 text-blue-600" />
      <h3 className="font-semibold text-lg">{title}</h3>
      <span className="ml-auto text-sm text-gray-500">{status}</span>
    </div>
    <ul className="space-y-2 mb-3">
      {actions.map((action, i) => (
        <li key={i} className="flex items-center gap-2 text-sm">
          <CheckCircle className="w-4 h-4 text-green-500" />
          {action}
        </li>
      ))}
    </ul>
    {condition && (
      <div className="text-sm text-gray-600 border-t pt-2">
        Escalation Condition: {condition}
      </div>
    )}
  </div>
);

const PatternCard = ({ title, metrics, confidence, status }) => (
  <div className="bg-white p-4 rounded-lg shadow-md">
    <div className="flex justify-between items-center mb-3">
      <h4 className="font-semibold">{title}</h4>
      <span className={`px-2 py-1 rounded-full text-sm ${
        status === 'Critical' ? 'bg-red-100 text-red-700' :
        status === 'Warning' ? 'bg-yellow-100 text-yellow-700' :
        'bg-green-100 text-green-700'
      }`}>
        {status}
      </span>
    </div>
    <div className="flex flex-wrap gap-2 mb-3">
      {metrics.map((metric, i) => (
        <span key={i} className="px-2 py-1 bg-blue-100 rounded-full text-xs text-blue-700">
          {metric}
        </span>
      ))}
    </div>
    <div className="w-full bg-gray-200 rounded-full h-2">
      <div 
        className="bg-blue-600 rounded-full h-2"
        style={{ width: `${confidence}%` }}
      />
    </div>
    <span className="text-sm text-gray-600">{confidence}% confidence</span>
  </div>
);

const PlatformContent = () => {
  const [activeSection, setActiveSection] = useState(0);
  const [openExamples, setOpenExamples] = useState({
    low: null,
    medium: null,
    high: null
  });

  const sections = [
    { id: 0, title: "AI Agents" },
    { id: 1, title: "Pattern Recognition" },
    { id: 2, title: "Self-Healing" },
    { id: 3, title: "Smart Escalation" }
  ];

  const toggleExample = (complexity, idx) => {
    setOpenExamples(prev => ({
      ...prev,
      [complexity]: prev[complexity] === idx ? null : idx
    }));
  };

  return (
    <div className="w-full max-w-7xl mx-auto p-8 bg-gray-50">
      {/* Header */}
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold mb-4">
          Intelligent Cloud Operations Platform
        </h1>
        <p className="text-xl text-gray-600">
          Autonomous monitoring, self-healing, and intelligent escalation
        </p>
      </div>

      {/* Navigation */}
      <div className="flex justify-center mb-8">
        {sections.map((section) => (
          <button
            key={section.id}
            onClick={() => setActiveSection(section.id)}
            className={`px-6 py-2 mx-2 rounded-full transition-all ${
              activeSection === section.id 
                ? 'bg-blue-600 text-white' 
                : 'bg-white text-gray-600'
            }`}
          >
            {section.title}
          </button>
        ))}
      </div>

      {/* Content */}
      <div className="mt-8">
        {activeSection === 0 && (
          <div className="grid grid-cols-3 gap-6">
            {[
              {
                icon: Shield,
                title: "24/7 Monitoring",
                description: "Continuous system analysis",
                features: ["Real-time analysis", "Anomaly detection", "Predictive alerts"]
              },
              {
                icon: Brain,
                title: "Intelligent Analysis",
                description: "Pattern recognition and correlation",
                features: ["Multi-metric analysis", "Historical patterns", "Risk assessment"]
              },
              {
                icon: Activity,
                title: "Automated Response",
                description: "Immediate action on issues",
                features: ["Self-healing", "Resource optimization", "Performance tuning"]
              }
            ].map((card, i) => (
              <div key={i} className="bg-white p-6 rounded-lg shadow-md">
                <div className="flex items-center gap-3 mb-4">
                  <card.icon className="w-6 h-6 text-blue-600" />
                  <h3 className="font-semibold">{card.title}</h3>
                </div>
                <p className="text-gray-600 mb-4">{card.description}</p>
                <ul className="space-y-2">
                  {card.features.map((feature, j) => (
                    <li key={j} className="flex items-center gap-2 text-sm">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        )}

        {activeSection === 1 && (
          <div className="space-y-8">
            {/* Data Sources Section */}
            <div className="grid grid-cols-3 gap-6">
              {[
                {
                  title: "Infrastructure Metrics",
                  icon: Cpu,
                  metrics: [
                    "CPU & Memory Patterns",
                    "Network Traffic Patterns",
                    "Resource Allocation Trends",
                    "System Load Patterns"
                  ]
                },
                {
                  title: "Application Metrics",
                  icon: Activity,
                  metrics: [
                    "Query Execution Patterns",
                    "Cache Hit/Miss Ratios",
                    "Request Latency Patterns",
                    "Error Rate Patterns"
                  ]
                },
                {
                  title: "Business Metrics",
                  icon: DollarSign,
                  metrics: [
                    "Cost Operation Patterns",
                    "Resource Cost Trends",
                    "Usage Time Patterns",
                    "SLA Compliance Patterns"
                  ]
                }
              ].map((source, i) => (
                <div key={i} className="bg-white p-6 rounded-lg shadow-md">
                  <div className="flex items-center gap-3 mb-4">
                    <source.icon className="w-6 h-6 text-blue-600" />
                    <h3 className="font-semibold">{source.title}</h3>
                  </div>
                  <ul className="space-y-2">
                    {source.metrics.map((metric, j) => (
                      <li key={j} className="flex items-center gap-2 text-sm">
                        <div className="w-2 h-2 rounded-full bg-blue-500"></div>
                        {metric}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>

            {/* Algorithm Categories */}
            <div className="grid grid-cols-2 gap-6">
              {[
                {
                  title: "Time Series Analysis",
                  algorithms: [
                    { name: "ARIMA", desc: "Predicts future values based on historical patterns" },
                    { name: "Prophet", desc: "Handles multiple seasonality patterns and outliers" },
                    { name: "LSTM", desc: "Deep learning for complex sequential patterns" }
                  ]
                },
                {
                  title: "Anomaly Detection",
                  algorithms: [
                    { name: "Isolation Forest", desc: "Efficiently identifies outliers through random splitting" },
                    { name: "DBSCAN", desc: "Groups patterns based on density clustering" },
                    { name: "One-Class SVM", desc: "Learns boundary of normal behavior" }
                  ]
                },
                {
                  title: "Correlation Analysis",
                  algorithms: [
                    { name: "Pearson Correlation", desc: "Measures linear relationships between metrics" },
                    { name: "Dynamic Time Warping", desc: "Finds similarity between temporal sequences" },
                    { name: "Granger Causality", desc: "Determines predictive relationships" }
                  ]
                },
                {
                  title: "Pattern Classification",
                  algorithms: [
                    { name: "Random Forest", desc: "Ensemble learning for robust pattern classification" },
                    { name: "XGBoost", desc: "Gradient boosting for complex feature relationships" },
                    { name: "Neural Networks", desc: "Deep learning for non-linear pattern recognition" }
                  ]
                }
              ].map((category, i) => (
                <div key={i} className="bg-white p-6 rounded-lg shadow-md">
                  <h3 className="text-lg font-semibold mb-4">{category.title}</h3>
                  <div className="space-y-4">
                    {category.algorithms.map((algo, j) => (
                      <div key={j} className="border-b pb-2">
                        <div className="flex items-center gap-2">
                          <Brain className="w-4 h-4 text-blue-500" />
                          <span className="font-medium">{algo.name}</span>
                        </div>
                        <p className="text-sm text-gray-600 mt-1">{algo.desc}</p>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            {/* Pattern Analysis Output */}
            <div className="grid grid-cols-3 gap-6">
              <PatternCard
                title="Temporal Pattern Analysis"
                metrics={['24hr Cycle', '3 Peak Times', '2 Low Times']}
                confidence={95}
                status="Normal"
              />
              <PatternCard
                title="Resource Pattern Analysis"
                metrics={['Memory Pressure', 'Swap Usage', 'GC Frequency']}
                confidence={89}
                status="Warning"
              />
              <PatternCard
                title="Performance Pattern Analysis"
                metrics={['Query Degradation', 'Cache Impact', 'Load Correlation']}
                confidence={91}
                status="Critical"
              />
            </div>

            {/* AI Decision Making */}
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-lg font-semibold mb-4">AI Agent Decision Flow</h3>
              <div className="grid grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <h4 className="font-medium mb-2">Pattern Detection</h4>
                    <div className="text-sm space-y-2">
                      <div className="flex justify-between">
                        <span>Type: Resource Exhaustion</span>
                        <span className="text-blue-600">94% Confidence</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Time to Impact</span>
                        <span className="text-yellow-600">15 minutes</span>
                      </div>
                    </div>
                  </div>
                  <div className="bg-green-50 p-4 rounded-lg">
                    <h4 className="font-medium mb-2">Automated Actions</h4>
                    <ul className="text-sm space-y-2">
                      <li className="flex items-center gap-2">
                        <CheckCircle className="w-4 h-4 text-green-500" />
                        Optimize Running Queries
                      </li>
                      <li className="flex items-center gap-2">
                        <CheckCircle className="w-4 h-4 text-green-500" />
                        Activate Query Throttling
                      </li>
                      <li className="flex items-center gap-2">
                        <CheckCircle className="w-4 h-4 text-green-500" />
                        Reallocate Resources
                      </li>
                    </ul>
                  </div>
                </div>
                <div className="space-y-4">
                  <div className="bg-purple-50 p-4 rounded-lg">
                    <h4 className="font-medium mb-2">Outcome Prediction</h4>
                    <div className="text-sm space-y-2">
                      <div className="flex justify-between">
                        <span>Resolution Probability</span>
                        <span className="text-purple-600">92%</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Expected Improvement</span>
                        <span className="text-purple-600">65%</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Side Effects</span>
                        <span className="text-green-600">Minimal</span>
                      </div>
                    </div>
                  </div>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <h4 className="font-medium mb-2">Escalation Decision</h4>
                    <div className="text-sm space-y-2">
                      <div className="flex items-center gap-2">
                        <Shield className="w-4 h-4 text-green-500" />
                        <span>No Escalation Required</span>
                      </div>
                      <p className="text-gray-600">
                        Pattern within automated resolution capabilities
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeSection === 2 && (
          <div className="space-y-8">
            {/* Definition Section */}
            <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-lg">
              <h3 className="text-xl font-semibold mb-4">Self-Healing Systems</h3>
              <p className="text-gray-700">
                Self-healing systems continuously monitor themselves for errors or potential problems and then take corrective actions automatically. 
                These systems use artificial intelligence and machine learning algorithms to predict, detect, and respond to operational issues in real-time.
              </p>
            </div>

            {/* Outcomes Grid */}
            <div className="grid grid-cols-3 gap-6">
              {[
                {
                  title: "Enhanced System Reliability",
                  icon: Shield,
                  items: [
                    "Automated issue resolution",
                    "Reduced downtime",
                    "Faster recovery times",
                    "Continuous monitoring"
                  ]
                },
                {
                  title: "Improved Efficiency",
                  icon: Zap,
                  items: [
                    "Optimized resource usage",
                    "Automated configuration",
                    "Dynamic adjustments",
                    "Minimal manual intervention"
                  ]
                },
                {
                  title: "Cost Optimization",
                  icon: DollarSign,
                  items: [
                    "Lower operational costs",
                    "Efficient resource allocation",
                    "Reduced maintenance",
                    "Optimized performance"
                  ]
                },
                {
                  title: "Enhanced Security",
                  icon: Shield,
                  items: [
                    "Automated threat detection",
                    "Continuous compliance",
                    "Real-time mitigation",
                    "Proactive protection"
                  ]
                },
                {
                  title: "Increased Scalability",
                  icon: Activity,
                  items: [
                    "Seamless scaling",
                    "Workload adaptation",
                    "Dynamic resource allocation",
                    "Flexible deployment"
                  ]
                },
                {
                  title: "Improved Productivity",
                  icon: Users,
                  items: [
                    "Reduced manual tasks",
                    "Proactive problem-solving",
                    "Focus on innovation",
                    "Strategic initiatives"
                  ]
                }
              ].map((category, i) => (
                <div key={i} className="bg-white p-6 rounded-lg shadow-md">
                  <div className="flex items-center gap-3 mb-4">
                    <category.icon className="w-6 h-6 text-blue-600" />
                    <h3 className="font-semibold">{category.title}</h3>
                  </div>
                  <ul className="space-y-2">
                    {category.items.map((item, j) => (
                      <li key={j} className="flex items-center gap-2 text-sm">
                        <CheckCircle className="w-4 h-4 text-green-500" />
                        {item}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>

            {/* Maturity Levels Section */}
            <div className="space-y-4">
              <div className="text-center">
                <h2 className="text-2xl font-bold mb-2">Maturity Levels & Categories</h2>
                <p className="text-gray-600 max-w-3xl mx-auto">
                  From basic automated responses to AI-driven predictive actions, our self-healing capabilities evolve with your operational maturity
                </p>
              </div>

              <div className="grid grid-cols-3 gap-6">
                {[
                  {
                    title: "Low Complexity",
                    icon: Shield,
                    color: "green",
                    features: [
                      "Automatic query retries and timeout management",
                      "Programmatic resource allocation",
                      "Job configuration management",
                      "Basic error handling and monitoring"
                    ],
                    examples: [
                      {
                        title: "Automatic Job Retries",
                        description: "BigQuery Python client supports automatic query job retries for timeouts and transient errors. Configure using job_retries parameter.",
                        code: `from google.cloud import bigquery

client = bigquery.Client()
job_config = bigquery.QueryJobConfig(
    job_timeout_ms=10000,
    job_retries=3
)
query_job = client.query("YOUR_QUERY", job_config=job_config)`,
                        details: [
                          "Handles transient errors automatically",
                          "Configurable retry attempts",
                          "Customizable timeout settings",
                          "Built-in error tracking"
                        ]
                      },
                      {
                        title: "Basic Resource Management",
                        description: "Use BigQuery Reservations API to programmatically manage slot allocations based on utilization thresholds.",
                        code: `from google.cloud import bigquery_reservation_v1

client = bigquery_reservation_v1.ReservationServiceClient()
parent = f"projects/{project_id}/locations/{location}"

reservation = {
    "slot_capacity": 100,
    "ignore_idle_slots": True
}

response = client.create_reservation(
    parent=parent,
    reservation_id=reservation_id,
    reservation=reservation
)`,
                        details: [
                          "Dynamic slot allocation",
                          "Utilization-based scaling",
                          "Automated resource management",
                          "Cost optimization"
                        ]
                      },
                      {
                        title: "Query Timeout Management",
                        description: "Set query timeouts programmatically to automatically terminate long-running queries.",
                        code: `from google.cloud import bigquery

client = bigquery.Client()
job_config = bigquery.QueryJobConfig(
    timeout_ms=300000  # 5 minutes
)
query_job = client.query("YOUR_QUERY", job_config=job_config)`,
                        details: [
                          "Automatic query termination",
                          "Configurable timeout thresholds",
                          "Resource protection",
                          "Performance monitoring"
                        ]
                      }
                    ]
                  },
                  {
                    title: "Medium Complexity",
                    icon: Brain,
                    color: "yellow",
                    features: [
                      "Cost-aware query optimization",
                      "MLOps pipeline recovery",
                      "Query performance optimization",
                      "Automated resource management"
                    ],
                    examples: [
                      {
                        title: "Cost-aware Query Optimization",
                        description: "Implement intelligent query cost management using Cloud Monitoring API, BigQuery Reservations API, and Information Schema.",
                        code: `// Analyze query costs using Information Schema
const analyzeCosts = async () => {
  const query = \`
    SELECT 
      project_id,
      user_email,
      total_bytes_processed,
      total_slot_ms
    FROM \`region-us\`.INFORMATION_SCHEMA.JOBS
    WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)
    ORDER BY total_bytes_processed DESC
    LIMIT 10
  \`
  return await bigquery.query(query)
}

// Manage dedicated resources
const optimizeResources = async (queryStats) => {
  const client = new BigQueryReservation()
  const reservation = {
    slotCapacity: calculateOptimalSlots(queryStats),
    ignoreIdleSlots: false
  }
  return await client.createReservation(reservation)
}

// Route expensive queries
const routeToReservation = async (queryId, reservationId) => {
  const jobConfig = {
    queryPriority: 'BATCH',
    reservationId: reservationId
  }
  return await bigquery.createQueryJob(jobConfig)
}`,
                        details: [
                          "Real-time cost monitoring",
                          "Dynamic resource allocation",
                          "Intelligent query routing",
                          "Cost optimization feedback"
                        ]
                      },
                      {
                        title: "MLOps Pipeline Recovery",
                        description: "Build resilient ML pipelines using Cloud Composer and Vertex AI with automated recovery mechanisms.",
                        code: `from kfp import dsl
from google.cloud import aiplatform

@dsl.pipeline(
    name='resilient-training-pipeline',
    description='Pipeline with automated recovery'
)
def training_pipeline():
    # Configure checkpointing
    checkpoint_config = {
        'frequency': 100,
        'storage': 'gs://your-bucket/checkpoints'
    }
    
    # Define training with recovery
    training = aiplatform.CustomTrainingJob(
        display_name='recoverable-training',
        script_path='training.py',
        container_uri='gcr.io/your-image',
        model_serving_container_image_uri='gcr.io/serve-image',
        retry_config={
            'max_retry_count': 3,
            'exponential_backoff': True
        }
    )
    
    # Execute with checkpointing
    model = training.run(
        checkpoint_config=checkpoint_config,
        recovery_config={
            'enable_auto_recovery': True,
            'max_recovery_attempts': 2
        }
    )`,
                        details: [
                          "Automated checkpointing",
                          "Intelligent retry logic",
                          "State persistence",
                          "Failure recovery"
                        ]
                      },
                      {
                        title: "Query Performance Optimization",
                        description: "Dynamic query optimization using BigQuery INFORMATION_SCHEMA and DDL for automated performance tuning.",
                        code: `// Analyze query patterns
const analyzePatterns = async () => {
  const query = \`
    SELECT 
      table_name,
      total_rows,
      total_logical_bytes,
      total_physical_bytes,
      clustering_fields
    FROM \`project.dataset\`.INFORMATION_SCHEMA.TABLES
    WHERE table_schema = 'your_dataset'
  \`
  return await bigquery.query(query)
}

// Optimize table structure
const optimizeTable = async (tableName, patterns) => {
  const ddl = \`
    ALTER TABLE \${tableName}
    SET OPTIONS (
      clustering_fields = [\${getOptimalClustering(patterns)}],
      require_partition_filter = true
    )
  \`
  return await bigquery.query(ddl)
}

// Measure performance impact
const measureImpact = async (tableId, beforeMetrics) => {
  const afterMetrics = await getQueryPerformance(tableId)
  return calculateImprovement(beforeMetrics, afterMetrics)
}`,
                        details: [
                          "Pattern-based optimization",
                          "Automated DDL updates",
                          "Performance monitoring",
                          "Impact analysis"
                        ]
                      }
                    ]
                  },
                  {
                    title: "High Complexity",
                    icon: Cpu,
                    color: "red",
                    features: [
                      "AI-driven predictive scaling",
                      "Automated threat mitigation",
                      "ML-based optimization",
                      "Continuous adaptation"
                    ],
                    examples: [
                      {
                        title: "Predictive Resource Scaling",
                        description: "Implement AI-driven resource scaling using Cloud Monitoring metrics and Vertex AI for demand forecasting.",
                        code: `from google.cloud import monitoring_v3
from google.cloud import aiplatform

class PredictiveScaler:
    def __init__(self):
        self.client = monitoring_v3.MetricServiceClient()
        self.model = aiplatform.Model(model_name="projects/*/models/*")

    async def collect_metrics(self, project_id):
        # Get historical metrics
        metric_type = "compute.googleapis.com/instance/cpu/utilization"
        interval = monitoring_v3.TimeInterval({
            "start_time": {"seconds": int(time.time() - 3600)},
            "end_time": {"seconds": int(time.time())}
        })
        return await self.client.list_time_series(
            request={
                "name": f"projects/{project_id}",
                "filter": f'metric.type = "{metric_type}"',
                "interval": interval
            }
        )

    async def predict_demand(self, metrics):
        # Generate prediction using Vertex AI
        prediction = await self.model.predict([
            metrics.cpu_usage,
            metrics.memory_usage,
            metrics.request_rate
        ])
        return {
            'expected_load': prediction.forecast,
            'confidence': prediction.confidence,
            'time_horizon': '1h'
        }

    async def adjust_resources(self, prediction):
        if prediction.confidence > 0.85:
            return await self.scale_resources(
                target_capacity=prediction.expected_load
            )`,
                        details: [
                          "Real-time metric analysis",
                          "ML-based load prediction",
                          "Confidence-based scaling",
                          "Automated resource adjustment"
                        ]
                      },
                      {
                        title: "Intelligent Threat Detection",
                        description: "Use Cloud Armor and Security Command Center with custom ML models for advanced threat detection.",
                        code: `from google.cloud import security_center_v1
from google.cloud import armor_v1

class ThreatDetector:
    def __init__(self):
        self.security_client = security_center_v1.SecurityCenterClient()
        self.armor_client = armor_v1.CloudArmorClient()

    async def analyze_traffic_pattern(self, project_id):
        # Analyze traffic patterns for anomalies
        findings = await self.security_client.list_findings(
            request={
                "parent": f"projects/{project_id}",
                "filter": "category=\"APPLICATION_THREAT\""
            }
        )
        return self.classify_threats(findings)

    async def apply_mitigation(self, threat_data):
        if threat_data.confidence > 0.9:
            # Apply adaptive security rules
            rule = {
                "priority": 1000,
                "description": "ML-detected threat pattern",
                "action": "deny(403)",
                "match": {
                    "expr": {
                        "expression": threat_data.pattern
                    }
                }
            }
            return await self.armor_client.create_rule(rule)`,
                        details: [
                          "Real-time threat analysis",
                          "Adaptive rule generation",
                          "Automated mitigation",
                          "Pattern-based protection"
                        ]
                      },
                      {
                        title: "Performance Auto-tuning",
                        description: "Implement continuous performance optimization using BigQuery ML and Vertex AI for workload analysis.",
                        code: `from google.cloud import bigquery
from google.cloud import aiplatform

class PerformanceOptimizer:
    def __init__(self):
        self.bq_client = bigquery.Client()
        self.ai_client = aiplatform.Model(model_name="workload_optimizer")

    async def analyze_workload(self):
        # Analyze query patterns and performance
        analysis_query = """
            SELECT
                query_text,
                total_slot_ms,
                total_bytes_processed,
                cache_hit,
                execution_time
            FROM \`project.region.INFORMATION_SCHEMA.JOBS\`
            WHERE creation_time >= TIMESTAMP_SUB(
                CURRENT_TIMESTAMP(), INTERVAL 24 HOUR
            )
        """
        return await self.bq_client.query(analysis_query)

    async def generate_optimization(self, workload_data):
        # Generate optimization recommendations
        prediction = await self.ai_client.predict(workload_data)
        return {
            'partition_keys': prediction.partition_recommendation,
            'clustering_keys': prediction.clustering_recommendation,
            'materialization_candidates': prediction.mv_candidates
        }

    async def apply_optimizations(self, recommendations):
        if recommendations.confidence > 0.8:
            # Apply recommended optimizations
            for table in recommendations.tables:
                await self.optimize_table(
                    table, 
                    recommendations.optimizations
                )`,
                        details: [
                          "Workload pattern analysis",
                          "ML-based recommendations",
                          "Automated optimization",
                          "Performance monitoring"
                        ]
                      }
                    ]
                  }
                ].map((level, i) => (
                  <div key={i} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                    <div className={`bg-${level.color}-50 p-6`}>
                      <div className="flex items-center gap-3 mb-4">
                        <div className={`p-2 bg-${level.color}-100 rounded-lg`}>
                          <level.icon className={`w-6 h-6 text-${level.color}-600`} />
                        </div>
                        <h3 className="font-semibold text-lg">{level.title}</h3>
                      </div>
                      <ul className="space-y-3 mb-6">
                        {level.features.map((feature, j) => (
                          <li key={j} className="flex items-center gap-2 text-sm">
                            <div className={`w-2 h-2 rounded-full bg-${level.color}-500`} />
                            <span className="text-gray-700">{feature}</span>
                          </li>
                        ))}
                      </ul>
                      {level.examples ? (
                        <div className="space-y-4">
                          {level.examples.map((example, idx) => (
                            <div key={idx} className="border border-gray-200 rounded-lg overflow-hidden">
                              <button
                                onClick={() => toggleExample(
                                  level.title.toLowerCase().replace(' ', '_'),
                                  idx
                                )}
                                className="w-full flex items-center justify-between p-3 bg-white hover:bg-gray-50"
                              >
                                <span className="font-medium text-sm">{example.title}</span>
                                <ChevronDown 
                                  className={`w-5 h-5 text-gray-500 transform transition-transform ${
                                    openExamples[level.title.toLowerCase().replace(' ', '_')] === idx ? 'rotate-180' : ''
                                  }`}
                                />
                              </button>
                              {openExamples[level.title.toLowerCase().replace(' ', '_')] === idx && (
                                <div className="bg-white p-4 border-t border-gray-200">
                                  <p className="text-sm text-gray-600 mb-4">{example.description}</p>
                                  <div className="max-h-96 overflow-y-auto">
                                    <pre className="bg-gray-900 text-gray-100 p-3 rounded text-sm">
                                      <code className="language-python">{example.code}</code>
                                    </pre>
                                  </div>
                                  <div className="grid grid-cols-2 gap-3 mt-4">
                                    {example.details.map((detail, i) => (
                                      <div key={i} className="flex items-center gap-2 text-sm">
                                        <CheckCircle className="w-4 h-4 text-green-500" />
                                        <span className="text-gray-600">{detail}</span>
                                      </div>
                                    ))}
                                  </div>
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                      ) : (
                        <div className="p-4 bg-gray-50">
                          <h4 className="font-medium text-sm mb-2">{level.example.title}</h4>
                          <pre className="bg-gray-900 text-gray-100 p-3 rounded text-sm overflow-x-auto">
                            <code>{level.example.code}</code>
                          </pre>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Interactive Demo */}
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-lg font-semibold mb-4">Self-Healing in Action</h3>
              <div className="grid grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <h4 className="font-medium mb-2">Issue Detection</h4>
                    <div className="animate-pulse space-y-2">
                      <div className="h-4 bg-blue-200 rounded w-3/4"></div>
                      <div className="h-4 bg-blue-200 rounded w-1/2"></div>
                    </div>
                  </div>
                  <div className="bg-yellow-50 p-4 rounded-lg">
                    <h4 className="font-medium mb-2">Analysis</h4>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span>Confidence</span>
                        <span>94%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div className="bg-yellow-500 h-2 rounded-full" style={{ width: '94%' }}></div>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="space-y-4">
                  <div className="bg-green-50 p-4 rounded-lg">
                    <h4 className="font-medium mb-2">Automated Resolution</h4>
                    <ul className="space-y-2">
                      {[
                        "Identify root cause",
                        "Select resolution strategy",
                        "Execute automated fix",
                        "Verify resolution"
                      ].map((step, i) => (
                        <li key={i} className="flex items-center gap-2 text-sm">
                          <CheckCircle className="w-4 h-4 text-green-500" />
                          {step}
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div className="bg-purple-50 p-4 rounded-lg">
                    <h4 className="font-medium mb-2">Learning & Adaptation</h4>
                    <div className="text-sm space-y-2">
                      <p>Pattern recorded for future reference</p>
                      <p>Resolution strategy optimized</p>
                      <p>Response time improved by 15%</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeSection === 3 && (
          <div className="space-y-4">
            <EscalationLevel 
              icon={Brain}
              title="AI Agent"
              status="Active"
              actions={["Autonomous monitoring", "Pattern detection", "Self-healing"]}
              condition="Escalates if unable to resolve within 15 minutes"
            />
            <EscalationLevel 
              icon={Shield}
              title="L1 Support"
              status="On standby"
              actions={["Initial investigation", "Standard procedures", "Basic troubleshooting"]}
              condition="Escalates if requires deeper technical expertise"
            />
            <EscalationLevel 
              icon={Users}
              title="L3 India"
              status="Available"
              actions={["Advanced troubleshooting", "Performance optimization", "Root cause analysis"]}
              condition="Escalates if requires customer-specific knowledge"
            />
            <EscalationLevel 
              icon={Shield}
              title="L3 US"
              status="Final escalation"
              actions={["Strategic decisions", "Customer escalations", "Architectural issues"]}
              condition="Final escalation point"
            />
          </div>
        )}
      </div>
    </div>
  );
};

const OperatePage = () => {
  const [selectedPillar, setSelectedPillar] = useState(null);
  const [selectedTimeframe, setSelectedTimeframe] = useState('24h');
  const [selectedView, setSelectedView] = useState('overview');
  const [lastUpdated, setLastUpdated] = useState(new Date());
  const [showPlatform, setShowPlatform] = useState(false);

  const operationalKPIs = {
    pipelineHealth: 98.5,
    dataFreshness: 96.2,
    dataQuality: 94.8,
    serviceLevel: 99.9
  };

  const processingMetrics = {
    activeJobs: 245,
    queuedJobs: 12,
    avgProcessingTime: '1.2s',
    throughput: '2.8TB/hr'
  };

  const pillars = [
    {
      id: 'cloudops',
      title: 'CloudOps',
      icon: <Activity className="w-6 h-6" />,
      color: 'bg-blue-500',
      metrics: ['Resource Utilization: 78%', 'Uptime: 99.99%', 'Active Alerts: 3'],
      aiInsights: 'AI detected potential resource optimization opportunities in Production environment'
    },
    {
      id: 'mlops',
      title: 'MLOps',
      icon: <BrainCircuit className="w-6 h-6" />,
      color: 'bg-cyan-500',
      metrics: ['Model Accuracy: 94%', 'Training Time: 2.3h', 'Active Models: 12'],
      aiInsights: 'AutoML detected drift in production model, retraining recommended'
    },
    {
      id: 'finops',
      title: 'FinOps',
      icon: <DollarSign className="w-6 h-6" />,
      color: 'bg-yellow-500',
      metrics: ['Monthly Spend: $45.2K', 'Cost Optimization: 23%', 'Budget Adherence: 92%'],
      aiInsights: 'AI forecasting predicts 15% cost reduction opportunity in storage usage'
    },
    {
      id: 'dataops',
      title: 'DataOps',
      icon: <Database className="w-6 h-6" />,
      color: 'bg-purple-500',
      metrics: ['Pipeline Health: 96%', 'Data Quality: 99%', 'Processing Latency: 1.2s'],
      aiInsights: 'Anomaly detection identified potential data drift in customer dataset'
    },
    {
      id: 'devops',
      title: 'SRE & DevOps',
      icon: <Code className="w-6 h-6" />,
      color: 'bg-indigo-500',
      metrics: ['Deploy Frequency: 8/day', 'Lead Time: 45min', 'MTTR: 12min'],
      aiInsights: 'AI suggested optimization in CI/CD pipeline could reduce build time by 35%'
    },
    {
      id: 'secops',
      title: 'SecOps',
      icon: <Shield className="w-6 h-6" />,
      color: 'bg-red-500',
      metrics: ['Threat Score: Low', 'Vulnerabilities: 2', 'Compliance: 98%'],
      aiInsights: 'AI detected unusual access patterns in staging environment'
    }
  ];

  const renderDataOpsContent = () => {
    switch (selectedView) {
      case 'overview':
        return (
          <div className="grid grid-cols-12 gap-6">
            {/* Operational Health - Top Row */}
            <div className="col-span-12 grid grid-cols-4 gap-6">
              <div className="bg-white rounded-lg p-6 shadow-sm">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <p className="text-sm text-gray-500">Pipeline Health</p>
                    <h3 className="text-2xl font-bold text-gray-900">{operationalKPIs.pipelineHealth}%</h3>
                  </div>
                  <div className="bg-green-100 p-2 rounded-lg">
                    <Activity className="w-5 h-5 text-green-600" />
                  </div>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-green-500 h-2 rounded-full" 
                    style={{ width: `${operationalKPIs.pipelineHealth}%` }}
                  ></div>
                </div>
              </div>

              <div className="bg-white rounded-lg p-6 shadow-sm">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <p className="text-sm text-gray-500">Data Freshness</p>
                    <h3 className="text-2xl font-bold text-gray-900">{operationalKPIs.dataFreshness}%</h3>
                  </div>
                  <div className="bg-blue-100 p-2 rounded-lg">
                    <Clock className="w-5 h-5 text-blue-600" />
                  </div>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-blue-500 h-2 rounded-full" 
                    style={{ width: `${operationalKPIs.dataFreshness}%` }}
                  ></div>
                </div>
              </div>

              <div className="bg-white rounded-lg p-6 shadow-sm">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <p className="text-sm text-gray-500">Data Quality</p>
                    <h3 className="text-2xl font-bold text-gray-900">{operationalKPIs.dataQuality}%</h3>
                  </div>
                  <div className="bg-purple-100 p-2 rounded-lg">
                    <CheckCircle className="w-5 h-5 text-purple-600" />
                  </div>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-purple-500 h-2 rounded-full" 
                    style={{ width: `${operationalKPIs.dataQuality}%` }}
                  ></div>
                </div>
              </div>

              <div className="bg-white rounded-lg p-6 shadow-sm">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <p className="text-sm text-gray-500">Service Level</p>
                    <h3 className="text-2xl font-bold text-gray-900">{operationalKPIs.serviceLevel}%</h3>
                  </div>
                  <div className="bg-yellow-100 p-2 rounded-lg">
                    <Timer className="w-5 h-5 text-yellow-600" />
                  </div>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-yellow-500 h-2 rounded-full" 
                    style={{ width: `${operationalKPIs.serviceLevel}%` }}
                  ></div>
                </div>
              </div>
            </div>

            {/* Processing Metrics - Left Column */}
            <div className="col-span-8">
              <div className="bg-white rounded-lg p-6 shadow-sm mb-6">
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-lg font-semibold">Processing Performance</h2>
                  <div className="flex items-center space-x-4">
                    <button className="text-sm text-gray-500 hover:text-gray-700">More details</button>
                  </div>
                </div>
                
                <div className="grid grid-cols-4 gap-4 mb-6">
                  <div className="p-4 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-500">Active Jobs</p>
                    <p className="text-xl font-semibold">{processingMetrics.activeJobs}</p>
                  </div>
                  <div className="p-4 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-500">Queued Jobs</p>
                    <p className="text-xl font-semibold">{processingMetrics.queuedJobs}</p>
                  </div>
                  <div className="p-4 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-500">Avg Processing Time</p>
                    <p className="text-xl font-semibold">{processingMetrics.avgProcessingTime}</p>
                  </div>
                  <div className="p-4 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-500">Throughput</p>
                    <p className="text-xl font-semibold">{processingMetrics.throughput}</p>
                  </div>
                </div>

                <ProcessingTimelineChart />
              </div>
            </div>

            {/* Alerts and Actions - Right Column */}
            <div className="col-span-4 space-y-6">
              <div className="bg-white rounded-lg p-6 shadow-sm">
                <h2 className="text-lg font-semibold mb-4">Active Alerts</h2>
                <div className="space-y-4">
                  <div className="flex items-center space-x-3 p-3 bg-red-50 rounded-lg">
                    <AlertCircle className="w-5 h-5 text-red-500" />
                    <div>
                      <p className="text-sm font-medium">High Processing Latency</p>
                      <p className="text-xs text-gray-500">5 min ago</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-3 p-3 bg-yellow-50 rounded-lg">
                    <AlertCircle className="w-5 h-5 text-yellow-500" />
                    <div>
                      <p className="text-sm font-medium">Data Quality Check Failed</p>
                      <p className="text-xs text-gray-500">15 min ago</p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg p-6 shadow-sm">
                <h2 className="text-lg font-semibold mb-4">Quick Actions</h2>
                <div className="space-y-3">
                  <button className="w-full flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100">
                    <span>View Pipeline Details</span>
                    <GitBranch className="w-5 h-5 text-gray-400" />
                  </button>
                  <button className="w-full flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100">
                    <span>Run Quality Check</span>
                    <CheckCircle className="w-5 h-5 text-gray-400" />
                  </button>
                  <button className="w-full flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100">
                    <span>Generate Report</span>
                    <FileText className="w-5 h-5 text-gray-400" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        );

      case 'pipelines':
        return (
          <div className="space-y-6">
            <div className="bg-white rounded-lg p-6 shadow-sm">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-lg font-semibold">Data Pipelines</h2>
                <button className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">
                  New Pipeline
                </button>
              </div>
              
              <div className="space-y-4">
                {['Production ETL', 'Customer Analytics', 'Marketing Data', 'Financial Reports'].map((pipeline) => (
                  <div key={pipeline} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div className="flex items-center space-x-4">
                      <GitBranch className="w-5 h-5 text-gray-500" />
                      <div>
                        <p className="font-medium">{pipeline}</p>
                        <p className="text-sm text-gray-500">Last run: 2 hours ago</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className="px-2 py-1 bg-green-100 text-green-700 rounded-md text-sm">Healthy</span>
                      <button className="p-2 hover:bg-gray-200 rounded-lg">
                        <BarChart2 className="w-4 h-4 text-gray-500" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        );

      case 'quality':
        return (
          <div className="space-y-6">
            <div className="bg-white rounded-lg p-6 shadow-sm">
              <h2 className="text-lg font-semibold mb-6">Data Quality Metrics</h2>
              <div className="grid grid-cols-3 gap-6">
                {[
                  { title: 'Completeness', score: '98%', trend: 'up' },
                  { title: 'Accuracy', score: '95%', trend: 'up' },
                  { title: 'Consistency', score: '97%', trend: 'stable' },
                ].map((metric) => (
                  <div key={metric.title} className="p-4 bg-gray-50 rounded-lg">
                    <div className="flex justify-between items-start mb-2">
                      <p className="text-sm text-gray-500">{metric.title}</p>
                      <TrendingUp className="w-4 h-4 text-green-500" />
                    </div>
                    <p className="text-2xl font-bold">{metric.score}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        );

      case 'governance':
        return (
          <div className="space-y-6">
            <div className="bg-white rounded-lg p-6 shadow-sm">
              <h2 className="text-lg font-semibold mb-6">Data Governance</h2>
              <div className="grid grid-cols-2 gap-6">
                <div className="p-6 border rounded-lg">
                  <h3 className="text-md font-medium mb-4">Compliance Status</h3>
                  <div className="space-y-4">
                    {[
                      { name: 'GDPR Compliance', status: 'Compliant' },
                      { name: 'Data Privacy', status: 'Review Required' },
                      { name: 'Data Retention', status: 'Compliant' },
                    ].map((item) => (
                      <div key={item.name} className="flex justify-between items-center">
                        <span className="text-sm">{item.name}</span>
                        <span className={`px-2 py-1 rounded-md text-sm ${
                          item.status === 'Compliant' 
                            ? 'bg-green-100 text-green-700' 
                            : 'bg-yellow-100 text-yellow-700'
                        }`}>
                          {item.status}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="p-6 border rounded-lg">
                  <h3 className="text-md font-medium mb-4">Access Control</h3>
                  <div className="space-y-4">
                    {[
                      { role: 'Admin', users: 5 },
                      { role: 'Data Steward', users: 12 },
                      { role: 'Analyst', users: 45 },
                    ].map((item) => (
                      <div key={item.role} className="flex justify-between items-center">
                        <span className="text-sm">{item.role}</span>
                        <div className="flex items-center space-x-2">
                          <Users className="w-4 h-4 text-gray-400" />
                          <span className="text-sm text-gray-600">{item.users}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        );

      case 'analytics':
        return (
          <div className="space-y-6">
            <div className="bg-white rounded-lg p-6 shadow-sm">
              <h2 className="text-lg font-semibold mb-6">Data Analytics</h2>
              <div className="grid grid-cols-2 gap-6">
                <div className="h-80 bg-gray-50 rounded-lg flex items-center justify-center">
                  <p className="text-gray-500">Data Volume Trends</p>
                </div>
                <div className="h-80 bg-gray-50 rounded-lg flex items-center justify-center">
                  <p className="text-gray-500">Processing Performance</p>
                </div>
              </div>
            </div>
          </div>
        );

      case 'bigquery':
        return (
          <div className="w-full max-w-6xl mx-auto p-8 bg-gradient-to-b from-blue-50 to-white rounded-lg shadow-lg">
            {/* Header Section */}
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold mb-4">Intelligent BigQuery Management</h2>
              <p className="text-lg text-gray-600 max-w-3xl mx-auto">
                Your BigQuery environment, enhanced with AI agents that proactively monitor, optimize, and protect your data operations
              </p>
            </div>

            {/* Central AI Brain Visualization */}
            <div className="relative mb-16">
              <div className="absolute inset-0 bg-blue-50 rounded-full blur-3xl opacity-20"></div>
              <div className="relative flex justify-center mb-8">
                <div className="p-8 bg-white rounded-full shadow-lg">
                  <Brain className="w-16 h-16 text-blue-600" />
                </div>
              </div>
              
              {/* AI Capabilities Ring */}
              <div className="grid grid-cols-3 gap-6">
                {[
                  {
                    icon: Zap,
                    title: "Real-Time Analysis",
                    desc: "Continuous monitoring with millisecond precision"
                  },
                  {
                    icon: Bot,
                    title: "Autonomous Operations",
                    desc: "Self-healing and automated optimization"
                  },
                  {
                    icon: Clock,
                    title: "Predictive Intelligence",
                    desc: "Anticipate issues before they impact"
                  }
                ].map((item, i) => (
                  <div key={i} className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
                    <div className="flex items-center gap-3 mb-3">
                      <item.icon className="w-6 h-6 text-blue-500" />
                      <h3 className="font-semibold">{item.title}</h3>
                    </div>
                    <p className="text-gray-600">{item.desc}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Monitoring Categories */}
            <div className="grid grid-cols-2 gap-8 mb-12">
              {[
                {
                  icon: Database,
                  title: "Query Performance",
                  metrics: ["Query patterns", "Execution times", "Resource usage"],
                  color: "text-purple-600"
                },
                {
                  icon: Cpu,
                  title: "Resource Utilization",
                  metrics: ["Slot usage", "Workload distribution", "Capacity planning"],
                  color: "text-green-600"
                },
                {
                  icon: DollarSign,
                  title: "Cost Management",
                  metrics: ["Query costs", "Storage optimization", "Resource allocation"],
                  color: "text-yellow-600"
                },
                {
                  icon: BarChart2,
                  title: "Data Architecture",
                  metrics: ["Table structures", "Pipeline performance", "Data freshness"],
                  color: "text-red-600"
                }
              ].map((category, i) => (
                <div key={i} className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
                  <div className="flex items-center gap-3 mb-4">
                    <category.icon className={`w-8 h-8 ${category.color}`} />
                    <h3 className="text-xl font-semibold">{category.title}</h3>
                  </div>
                  <ul className="space-y-2">
                    {category.metrics.map((metric, j) => (
                      <li key={j} className="flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full bg-blue-500"></div>
                        <span className="text-gray-600">{metric}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>

            {/* Benefits & Outcomes Section */}
            <div className="space-y-4">
              <div className="text-center mb-8">
                <h2 className="text-2xl font-bold mb-2">Benefits & Outcomes</h2>
                <p className="text-gray-600 max-w-3xl mx-auto">
                  Transform your operations with intelligent automation that delivers measurable improvements across reliability, efficiency, security, and productivity
                </p>
              </div>
              
              <div className="grid grid-cols-3 gap-6">
                {[
                  {
                    icon: AlertTriangle,
                    title: "90% Faster Issue Resolution",
                    desc: "AI-powered diagnostics and automated remediation"
                  },
                  {
                    icon: LineChart,
                    title: "40% Cost Reduction",
                    desc: "Intelligent resource optimization and cost management"
                  },
                  {
                    icon: Shield,
                    title: "99.9% Reliability",
                    desc: "Proactive monitoring and predictive maintenance"
                  }
                ].map((benefit, i) => (
                  <div key={i} className="bg-white p-4 rounded-lg shadow-sm">
                    <div className="flex items-center gap-2 mb-2">
                      <benefit.icon className="w-5 h-5 text-blue-500" />
                      <h4 className="font-medium">{benefit.title}</h4>
                    </div>
                    <p className="text-sm text-gray-600">{benefit.desc}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  if (selectedPillar === 'dataops') {
    return (
      <div className="min-h-screen bg-gray-50">
        {/* Top Navigation Bar */}
        <div className="bg-white border-b px-6 py-3">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-8">
              <button 
                onClick={() => setSelectedPillar(null)}
                className="text-gray-600 hover:text-gray-900 p-2 rounded-lg hover:bg-gray-100"
                title="Back"
              >
                <ArrowLeft className="w-5 h-5" />
              </button>
              <h1 className="text-sm font-bold text-gray-900">DataOps Command Center</h1>
              <nav className="flex space-x-4">
                {[
                  'Overview',
                  'BigQuery',
                  'Pipelines',
                  'Quality',
                  'Governance',
                  'Analytics'
                ].map((item) => (
                  <button 
                    key={item}
                    className={`px-3 py-2 rounded-md text-sm font-medium ${
                      selectedView === item.toLowerCase() 
                        ? 'bg-blue-50 text-blue-700' 
                        : 'text-gray-600 hover:bg-gray-50'
                    }`}
                    onClick={() => setSelectedView(item.toLowerCase())}
                  >
                    {item}
                  </button>
                ))}
              </nav>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <RefreshCw 
                  className="w-4 h-4 cursor-pointer" 
                  onClick={() => setLastUpdated(new Date())}
                />
                <span>Last updated: {lastUpdated.toLocaleString('en-US', {
                  year: '2-digit',
                  month: '2-digit',
                  day: '2-digit',
                  hour: '2-digit',
                  minute: '2-digit',
                  second: '2-digit',
                  hour12: false
                })}</span>
              </div>
              <button className="flex items-center space-x-2 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600">
                <CopilotIcon className="w-5 h-5" />
                <span>DataOps Copilot</span>
              </button>
            </div>
          </div>
        </div>

        <div className="p-6">
          {/* Time Range Selector and Filters */}
          <div className="mb-6 flex justify-between items-center">
            {/* ... rest of the DataOps component content ... */}
          </div>

          {/* Render content based on selected view */}
          {renderDataOpsContent()}
        </div>
      </div>
    );
  }

  return (
    <Card className="w-full">
      {/* Header */}
      <div className="p-8">
        <div className="mb-8 flex justify-between items-center">
          <div className="flex items-center space-x-4">
            <h1 className="text-2xl font-bold text-gray-900">Cloud Operations Command Center</h1>
            <button
              onClick={() => setShowPlatform(!showPlatform)}
              className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 flex items-center space-x-2"
            >
              <span>Ops Platform</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
          <div className="flex items-center space-x-4">
            <div className="relative">
              <Search className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search operations..."
                className="pl-10 pr-4 py-2 border rounded-lg w-64 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <button className="flex items-center space-x-2 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600">
              <CopilotIcon className="w-5 h-5" />
              <span>Ops Copilot</span>
            </button>
          </div>
        </div>

        {showPlatform ? (
          <PlatformContent />
        ) : (
          <>
            {/* AI Insights Banner */}
            <div className="bg-gradient-to-r from-blue-500 to-indigo-600 rounded-lg p-4 mb-8 text-white flex items-center">
              <BrainCircuit className="w-8 h-8 mr-4" />
              <div>
                <h2 className="font-semibold">Ops Insight Engine</h2>
                <p className="text-sm opacity-90">Continuously monitoring and optimizing your cloud operations</p>
              </div>
            </div>

            {/* Pillars Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {pillars.map((pillar) => (
                <div 
                  key={pillar.id}
                  className="bg-white dark:bg-gray-700 rounded-lg shadow-lg p-6 cursor-pointer transform transition-transform hover:scale-102"
                  onClick={() => setSelectedPillar(pillar.id)}
                >
                  <div className="flex items-center mb-4">
                    <div className={`${pillar.color} p-3 rounded-lg text-white mr-4`}>
                      {pillar.icon}
                    </div>
                    <h2 className="text-xl font-semibold text-gray-900 dark:text-white">{pillar.title}</h2>
                  </div>
                  
                  <div className="space-y-3 mb-4">
                    {pillar.metrics.map((metric, idx) => (
                      <div key={idx} className="flex items-center text-sm text-gray-600 dark:text-gray-300">
                        <div className="w-2 h-2 rounded-full bg-green-500 mr-2"></div>
                        {metric}
                      </div>
                    ))}
                  </div>

                  <div className="bg-blue-50 dark:bg-blue-900 p-3 rounded-lg">
                    <div className="flex items-center text-sm text-blue-700 dark:text-blue-300">
                      <BrainCircuit className="w-4 h-4 mr-2" />
                      {pillar.aiInsights}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </Card>
  );
};

export default OperatePage; 