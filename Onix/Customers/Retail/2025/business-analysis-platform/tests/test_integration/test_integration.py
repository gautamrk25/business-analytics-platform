import asyncio
from business_analysis_platform import BusinessAnalysisAgent, ConfigManager

async def test_integration():
    config = ConfigManager()
    agent = BusinessAnalysisAgent({}, config)
    
    # Test with workflow
    workflow_steps = [
        {
            'name': 'validate_data',
            'type': 'data_validator',
            'config': {
                'validation_rules': {'sales': {'allow_null': False}},
                'auto_fix': True
            }
        }
    ]
    
    test_data = {'sales': [100, 200, None, 300]}
    result = await agent.analyze_data_with_correction(test_data, "Analyze sales", workflow_steps=workflow_steps)
    print("Integration test result:", result.get('execution_method'))
    print("Workflow results:", result.get('workflow_result', {}).get('workflow_summary'))
    # Success criteria checks
    assert hasattr(agent, 'building_block_registry'), "Agent missing building_block_registry"
    assert result.get('execution_method') == 'building_blocks', "Execution method should be 'building_blocks'"
    assert result.get('workflow_result', {}).get('steps_completed', 0) == 1, "Workflow should complete 1 step"
    assert any('validate_data' == step['step'] for step in result.get('workflow_result', {}).get('workflow_summary', [])), "Workflow summary should include 'validate_data' step"
    assert any('fixes' in s.get('message', '').lower() or 'fixes' in str(result.get('insights', [])).lower() for s in result.get('workflow_result', {}).get('workflow_summary', [{}])), "Insights should mention data quality fixes"
    print("All integration success criteria met.")

if __name__ == "__main__":
    asyncio.run(test_integration()) 