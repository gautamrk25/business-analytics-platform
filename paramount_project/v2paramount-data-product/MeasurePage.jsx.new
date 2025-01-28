import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { ArrowUp, ArrowDown } from 'lucide-react';
import { AreaChart, Area } from 'recharts';
import { BarChart, Bar } from 'recharts';

const Card = ({ children, className = '' }) => (
  <div className={`bg-white dark:bg-gray-800 rounded-lg shadow-lg text-sm ${className}`}>
    {children}
  </div>
);

const TimeToggle = ({ active, onChange }) => (
  <div className="flex gap-2 text-sm mb-4">
    {['Today', 'Week', 'Month', 'Year'].map(period => (
      <button
        key={period}
        className={`px-3 py-1 rounded ${
          active === period.toLowerCase() 
            ? 'bg-blue-500 text-white' 
            : 'bg-gray-100 dark:bg-gray-700'
        }`}
        onClick={() => onChange(period.toLowerCase())}
      >
        {period}
      </button>
    ))}
  </div>
);

const KPICard = ({ title, value, change, data, type, chartType }) => {
  const getChartColor = (type) => {
    switch(type) {
      case 'conversion': return '#3b82f6';
      case 'revenue': return '#10b981';
      case 'engagement': return '#8b5cf6';
      case 'risk': return '#ef4444';
      default: return '#6b7280';
    }
  };

  const renderChart = () => {
    const color = getChartColor(type);

    switch(chartType) {
      case 'area':
        return (
          <AreaChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" fontSize={10} angle={-45} textAnchor="end" height={50} />
            <YAxis />
            <Tooltip />
            <Area type="monotone" dataKey="value" stroke={color} fill={color} fillOpacity={0.2} />
          </AreaChart>
        );
      case 'bar':
        return (
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" fontSize={10} angle={-45} textAnchor="end" height={50} />
            <YAxis />
            <Tooltip />
            <Bar dataKey="value" fill={color} />
          </BarChart>
        );
      default:
        return (
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" fontSize={10} angle={-45} textAnchor="end" height={50} />
            <YAxis />
            <Tooltip />
            <Line 
              type={type === 'risk' ? 'stepAfter' : 'monotone'} 
              dataKey="value" 
              stroke={color}
              strokeWidth={2}
            />
          </LineChart>
        );
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 p-4 rounded-lg">
      <div className="flex justify-between items-center mb-2">
        <h3 className="font-medium text-sm">{title}</h3>
        <div className={`flex items-center ${change >= 0 ? 'text-green-500' : 'text-red-500'}`}>
          {change >= 0 ? <ArrowUp size={16} /> : <ArrowDown size={16} />}
          <span className="text-sm">{Math.abs(change)}%</span>
        </div>
      </div>
      <div className="h-[150px]">
        <ResponsiveContainer width="100%" height="100%">
          {renderChart()}
        </ResponsiveContainer>
      </div>
    </div>
  );
};

const UseCaseSection = ({ title, kpis, period }) => (
  <div className="mb-6">
    <h2 className="text-lg font-semibold mb-4">{title}</h2>
    <div className="grid grid-cols-2 lg:grid-cols-3 gap-4">
      {kpis.map(kpi => (
        <KPICard
          key={kpi.title}
          title={kpi.title}
          value={kpi.value}
          change={kpi.change}
          data={kpi.data[period]}
          type={kpi.type}
          chartType={kpi.chartType}
        />
      ))}
    </div>
  </div>
);

const MeasurePage = () => {
  console.log('MeasurePage rendered');
  const [period, setPeriod] = useState('today');
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    // Simulate API call to fetch metrics
    const generateData = (min, max, points) => {
      return Array.from({ length: points }, (_, i) => ({
        name: `P${i + 1}`,
        value: Math.floor(Math.random() * (max - min) + min)
      }));
    };

    const generateTimeSeriesData = (type, period) => {
      switch(type) {
        case 'conversion':
          return generateData(20, 30, 24);
        case 'revenue':
          return generateData(18, 38, 24);
        case 'engagement':
          return generateData(70, 80, 24);
        case 'risk':
          return generateData(12, 18, 24);
        default:
          return [];
      }
    };

    const generateMetrics = () => ({
      highValueUsers: {
        title: 'Target High-Value Users',
        kpis: [
          {
            title: 'Premium Conversion Rate',
            value: '12.5%',
            change: 5.2,
            type: 'conversion',
            chartType: 'line',
            data: {
              today: generateTimeSeriesData('conversion', 'today'),
              week: generateTimeSeriesData('conversion', 'week'),
              month: generateTimeSeriesData('conversion', 'month'),
              year: generateTimeSeriesData('conversion', 'year')
            }
          },
          {
            title: 'Average Revenue Per User',
            value: '$24.50',
            change: 3.8,
            type: 'revenue',
            chartType: 'area',
            data: {
              today: generateTimeSeriesData('revenue', 'today'),
              week: generateTimeSeriesData('revenue', 'week'),
              month: generateTimeSeriesData('revenue', 'month'),
              year: generateTimeSeriesData('revenue', 'year')
            }
          },
          {
            title: 'Premium Trial Activation Rate',
            value: '28.3%',
            change: -2.1,
            type: 'conversion',
            chartType: 'bar',
            data: {
              today: generateTimeSeriesData('conversion', 'today'),
              week: generateTimeSeriesData('conversion', 'week'),
              month: generateTimeSeriesData('conversion', 'month'),
              year: generateTimeSeriesData('conversion', 'year')
            }
          }
        ]
      },
      retentionRisk: {
        title: 'Retention Risk Analysis',
        kpis: [
          {
            title: 'Churn Risk Score',
            value: '15.2%',
            change: -3.1,
            type: 'risk',
            chartType: 'line',
            data: {
              today: generateTimeSeriesData('risk', 'today'),
              week: generateTimeSeriesData('risk', 'week'),
              month: generateTimeSeriesData('risk', 'month'),
              year: generateTimeSeriesData('risk', 'year')
            }
          },
          {
            title: 'Engagement Trend',
            value: '84.3%',
            change: 2.4,
            type: 'engagement',
            chartType: 'area',
            data: {
              today: generateTimeSeriesData('engagement', 'today'),
              week: generateTimeSeriesData('engagement', 'week'),
              month: generateTimeSeriesData('engagement', 'month'),
              year: generateTimeSeriesData('engagement', 'year')
            }
          },
          {
            title: 'Days Since Last Watch',
            value: '2.4',
            change: -1.8,
            type: 'engagement',
            chartType: 'bar',
            data: {
              today: generateTimeSeriesData('engagement', 'today'),
              week: generateTimeSeriesData('engagement', 'week'),
              month: generateTimeSeriesData('engagement', 'month'),
              year: generateTimeSeriesData('engagement', 'year')
            }
          }
        ]
      },
      contentRecommendations: {
        title: 'Content Recommendations',
        kpis: [
          {
            title: 'Recommendation CTR',
            value: '32.1%',
            change: 4.3,
            type: 'conversion',
            chartType: 'line',
            data: {
              today: generateTimeSeriesData('conversion', 'today'),
              week: generateTimeSeriesData('conversion', 'week'),
              month: generateTimeSeriesData('conversion', 'month'),
              year: generateTimeSeriesData('conversion', 'year')
            }
          },
          {
            title: 'Watch Completion Rate',
            value: '71.5%',
            change: 2.8,
            type: 'engagement',
            chartType: 'area',
            data: {
              today: generateTimeSeriesData('engagement', 'today'),
              week: generateTimeSeriesData('engagement', 'week'),
              month: generateTimeSeriesData('engagement', 'month'),
              year: generateTimeSeriesData('engagement', 'year')
            }
          },
          {
            title: 'Time to First Watch',
            value: '45s',
            change: -5.2,
            type: 'engagement',
            chartType: 'bar',
            data: {
              today: generateTimeSeriesData('engagement', 'today'),
              week: generateTimeSeriesData('engagement', 'week'),
              month: generateTimeSeriesData('engagement', 'month'),
              year: generateTimeSeriesData('engagement', 'year')
            }
          }
        ]
      },
      viewerSegmentation: {
        title: 'Viewer Segmentation',
        kpis: [
          {
            title: 'Campaign Response Rate',
            value: '24.8%',
            change: 3.9,
            type: 'conversion',
            chartType: 'line',
            data: {
              today: generateTimeSeriesData('conversion', 'today'),
              week: generateTimeSeriesData('conversion', 'week'),
              month: generateTimeSeriesData('conversion', 'month'),
              year: generateTimeSeriesData('conversion', 'year')
            }
          },
          {
            title: 'Segment Stability Index',
            value: '89.2%',
            change: 1.4,
            type: 'engagement',
            chartType: 'area',
            data: {
              today: generateTimeSeriesData('engagement', 'today'),
              week: generateTimeSeriesData('engagement', 'week'),
              month: generateTimeSeriesData('engagement', 'month'),
              year: generateTimeSeriesData('engagement', 'year')
            }
          },
          {
            title: 'Revenue Impact/Segment',
            value: '$156.2',
            change: 6.7,
            type: 'revenue',
            chartType: 'bar',
            data: {
              today: generateTimeSeriesData('revenue', 'today'),
              week: generateTimeSeriesData('revenue', 'week'),
              month: generateTimeSeriesData('revenue', 'month'),
              year: generateTimeSeriesData('revenue', 'year')
            }
          }
        ]
      }
    });

    setMetrics(generateMetrics());
  }, []);

  if (!metrics) return <div>Loading...</div>;

  return (
    <div className="p-4">
      <TimeToggle active={period} onChange={setPeriod} />
      <div className="grid gap-6">
        {Object.entries(metrics).map(([key, section]) => (
          <UseCaseSection
            key={key}
            title={section.title}
            kpis={section.kpis}
            period={period}
          />
        ))}
      </div>
    </div>
  );
};

export default MeasurePage; 