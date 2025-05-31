"""Example implementation of an executive demo.

This module provides an example of how to create a concrete demo class
that inherits from ExecutiveDemo.
"""

from typing import Any, Dict

from .executive_demo import ExecutiveDemo

class ExampleBusinessDemo(ExecutiveDemo):
    """Example business analysis demo implementation.
    
    This class demonstrates how to create a concrete demo that inherits
    from ExecutiveDemo. It shows a typical business analysis workflow
    with multiple steps and progress tracking.
    """
    
    async def run_demo(self) -> Dict[str, Any]:
        """Run the example business analysis demo.
        
        This demo shows:
        1. Data loading and validation
        2. Basic analysis
        3. Advanced insights
        4. Recommendations
        
        Returns:
            Dict containing demo results and outputs.
        """
        # Initialize results
        self.demo_results = {
            'steps_completed': 0,
            'total_steps': 4,
            'analysis_results': {},
            'recommendations': []
        }
        
        # Step 1: Data Loading
        self.display_section_header("Data Loading & Validation")
        await self.demo_delay(1.0)
        self.display_progress("Loading sample data...", 25)
        
        # Simulate data loading
        sample_data = {
            'sales': [100, 200, 150, 300],
            'customers': [10, 20, 15, 30],
            'date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04']
        }
        self.demo_results['sample_data'] = sample_data
        
        # Step 2: Basic Analysis
        self.display_section_header("Basic Analysis")
        await self.demo_delay(1.5)
        self.display_progress("Performing basic analysis...", 50)
        
        # Simulate basic analysis
        basic_analysis = {
            'total_sales': sum(sample_data['sales']),
            'avg_customers': sum(sample_data['customers']) / len(sample_data['customers']),
            'sales_trend': 'increasing'
        }
        self.demo_results['analysis_results']['basic'] = basic_analysis
        
        # Step 3: Advanced Insights
        self.display_section_header("Advanced Insights")
        await self.demo_delay(2.0)
        self.display_progress("Generating advanced insights...", 75)
        
        # Simulate advanced analysis
        advanced_insights = {
            'customer_value': basic_analysis['total_sales'] / basic_analysis['avg_customers'],
            'growth_rate': '15%',
            'key_findings': [
                'Strong correlation between customer count and sales',
                'Weekend sales show higher performance',
                'New customer acquisition cost is decreasing'
            ]
        }
        self.demo_results['analysis_results']['advanced'] = advanced_insights
        
        # Step 4: Recommendations
        self.display_section_header("Recommendations")
        await self.demo_delay(1.0)
        self.display_progress("Generating recommendations...", 100)
        
        # Simulate recommendations
        recommendations = [
            'Increase marketing spend during weekends',
            'Focus on customer retention programs',
            'Consider expanding to new markets'
        ]
        self.demo_results['recommendations'] = recommendations
        
        # Demo complete
        self.display_section_header("Demo Complete")
        return self.demo_results 