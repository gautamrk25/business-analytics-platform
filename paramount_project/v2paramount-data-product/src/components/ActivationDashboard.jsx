import React, { useState } from 'react';
import { 
  Target, Users, Sparkles, Heart,
  CheckCircle, X
} from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';

const kpiDetails = {
  'Premium Conversion Rate': {
    calculation: 'Number of Premium Conversions / Total Free Users * 100',
    explanation: 'Measures the percentage of free users who upgrade to premium subscriptions.'
  },
  'Average Revenue Per User (ARPU)': {
    calculation: 'Total Revenue / Total Number of Active Users',
    explanation: 'Average revenue generated per user, indicating monetization effectiveness.'
  },
  'Upgrade Campaign Response Rate': {
    calculation: 'Number of Campaign Responses / Total Campaign Recipients * 100',
    explanation: 'Percentage of users who respond to premium upgrade campaigns.'
  },
  'Churn Rate Reduction': {
    calculation: '(Previous Churn Rate - Current Churn Rate) / Previous Churn Rate * 100',
    explanation: 'Percentage decrease in customer churn rate over time.'
  },
  'Customer Retention Rate': {
    calculation: '((Total Customers End - New Customers) / Total Customers Start) * 100',
    explanation: 'Percentage of customers retained over a specific period.'
  },
  'Reactivation Success Rate': {
    calculation: 'Number of Reactivated Users / Total Churned Users Targeted * 100',
    explanation: 'Success rate of bringing churned users back to the platform.'
  },
  'Customer Satisfaction Score': {
    calculation: 'Sum of All Satisfaction Scores / Total Number of Responses',
    explanation: 'Average satisfaction score from customer feedback surveys.'
  },
  'Content Engagement Rate': {
    calculation: 'Total Engagement Actions / Total Content Views * 100',
    explanation: 'Percentage of viewers who engage with recommended content.'
  },
  'Watch Time per Session': {
    calculation: 'Total Watch Time / Total Number of Sessions',
    explanation: 'Average duration users spend watching content per session.'
  },
  'Recommendation Click-Through Rate': {
    calculation: 'Number of Recommendation Clicks / Total Recommendations Shown * 100',
    explanation: 'Percentage of recommended content that users click on.'
  },
  'Campaign Conversion Rate': {
    calculation: 'Number of Campaign Conversions / Total Campaign Recipients * 100',
    explanation: 'Success rate of segment-specific marketing campaigns.'
  },
  'Segment Growth Rate': {
    calculation: '(Current Segment Size - Previous Segment Size) / Previous Segment Size * 100',
    explanation: 'Rate at which each viewer segment is growing over time.'
  },
  'Marketing ROI per Segment': {
    calculation: '(Campaign Revenue - Campaign Cost) / Campaign Cost * 100',
    explanation: 'Return on investment for marketing campaigns per segment.'
  }
};

const KPIDialog = ({ kpi, isOpen, onClose }) => {
  if (!isOpen) return null;

  const details = kpiDetails[kpi];

  return (
    <div className="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-50" onClick={onClose}>
      <div className="bg-white rounded-lg shadow-lg p-4 max-w-sm" onClick={e => e.stopPropagation()}>
        <div className="flex justify-between items-start mb-3">
          <h3 className="text-sm font-medium">{kpi}</h3>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
            <X className="w-4 h-4" />
          </button>
        </div>
        <div className="space-y-2">
          <div>
            <p className="text-xs font-medium text-gray-500">Calculation:</p>
            <p className="text-xs text-gray-600">{details.calculation}</p>
          </div>
          <div>
            <p className="text-xs font-medium text-gray-500">Explanation:</p>
            <p className="text-xs text-gray-600">{details.explanation}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

const useCases = [
  {
    id: 'high-value',
    title: 'Target High-Value Users',
    description: 'Identify and target users likely to upgrade to premium subscriptions',
    icon: Target,
    kpis: [
      'Premium Conversion Rate',
      'Average Revenue Per User (ARPU)',
      'Upgrade Campaign Response Rate'
    ]
  },
  {
    id: 'retention',
    title: 'Retention Risk Analysis',
    description: 'Identify at-risk users for retention campaigns',
    icon: Users,
    kpis: [
      'Churn Rate Reduction',
      'Customer Retention Rate',
      'Reactivation Success Rate',
      'Customer Satisfaction Score'
    ]
  },
  {
    id: 'recommendations',
    title: 'Content Recommendations',
    description: 'Personalize content recommendations based on viewing patterns',
    icon: Sparkles,
    kpis: [
      'Content Engagement Rate',
      'Watch Time per Session',
      'Recommendation Click-Through Rate'
    ]
  },
  {
    id: 'segmentation',
    title: 'Viewer Segmentation',
    description: 'Tailor marketing campaigns to specific viewer segments',
    icon: Heart,
    kpis: [
      'Campaign Conversion Rate',
      'Segment Growth Rate',
      'Marketing ROI per Segment'
    ]
  }
];

const ActivationDashboard = () => {
  const [selectedKPI, setSelectedKPI] = useState(null);

  return (
    <div className="w-full">
      <Card>
        <CardHeader>
          <CardTitle>Use Cases</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-4 gap-4">
            {useCases.map((useCase) => (
              <button
                key={useCase.id}
                className="p-4 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors text-left"
              >
                <div className="flex items-center gap-2 mb-2">
                  <useCase.icon className="w-5 h-5" />
                  <span className="font-medium">{useCase.title}</span>
                </div>
                <p className="text-sm text-gray-600 mb-3">{useCase.description}</p>
                <div className="space-y-1">
                  <p className="text-xs font-medium text-gray-500">Key Performance Indicators:</p>
                  {useCase.kpis.map((kpi, index) => (
                    <div key={index} className="text-xs text-gray-600 flex items-center gap-1">
                      <CheckCircle className="w-3 h-3 text-green-500 flex-shrink-0" />
                      <button 
                        onClick={(e) => {
                          e.stopPropagation();
                          setSelectedKPI(kpi);
                        }}
                        className="hover:text-blue-600 hover:underline text-left"
                      >
                        {kpi}
                      </button>
                    </div>
                  ))}
                </div>
              </button>
            ))}
          </div>
        </CardContent>
      </Card>
      <KPIDialog 
        kpi={selectedKPI} 
        isOpen={!!selectedKPI} 
        onClose={() => setSelectedKPI(null)} 
      />
    </div>
  );
};

export default ActivationDashboard; 