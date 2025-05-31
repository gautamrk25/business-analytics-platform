import React from 'react';
import { Target, Users, Sparkles, Heart } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';

const useCases = [
  {
    id: 'high-value',
    title: 'Target High-Value Users',
    description: 'Identify and target users likely to upgrade to premium subscriptions',
    icon: Target
  },
  {
    id: 'retention',
    title: 'Retention Risk Analysis',
    description: 'Identify at-risk users for retention campaigns',
    icon: Users
  },
  {
    id: 'recommendations',
    title: 'Content Recommendations',
    description: 'Personalize content recommendations based on viewing patterns',
    icon: Sparkles
  },
  {
    id: 'segmentation',
    title: 'Viewer Segmentation',
    description: 'Tailor marketing campaigns to specific viewer segments',
    icon: Heart
  }
];

const ActivationFlow = () => {
  return (
    <div className="w-full">
      <Card>
        <CardHeader>
          <CardTitle>Activation Flow</CardTitle>
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
                <p className="text-sm text-gray-600">{useCase.description}</p>
              </button>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default ActivationFlow; 