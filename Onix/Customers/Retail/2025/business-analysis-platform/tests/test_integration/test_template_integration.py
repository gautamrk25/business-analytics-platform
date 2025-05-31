import asyncio
from business_analysis_platform import BusinessAnalysisOrchestrator

async def test_template_integration():
    # Initialize orchestrator
    orchestrator = BusinessAnalysisOrchestrator(None, "config.yaml")
    
    # Test template suggestions
    question = "How are our marketing campaigns performing?"
    data_columns = ['campaign_spend', 'impressions', 'clicks', 'conversions']
    suggestions = orchestrator.suggest_templates(question, data_columns)
    
    print(f"Template suggestions: {len(suggestions)}")
    if suggestions:
        print(f"Best suggestion: {suggestions[0]['template']['name']}")
        print(f"Compatibility score: {suggestions[0]['compatibility_score']}")
    
    # Test template-based analysis
    test_data = {
        'campaign_spend': [1000, 1500, 1200],
        'impressions': [10000, 15000, 12000],
        'clicks': [500, 750, 600],
        'conversions': [50, 75, 60]
    }
    
    result = await orchestrator.analyze_business_question(
        question, 
        test_data, 
        auto_suggest_templates=True
    )
    
    print(f"Analysis completed with method: {result.get('execution_method')}")
    if 'template_used' in result:
        print(f"Template used: {result['template_used']['name']}")

if __name__ == "__main__":
    asyncio.run(test_template_integration()) 