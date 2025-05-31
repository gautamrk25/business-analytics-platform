import os
import yaml
from business_analysis_platform import (
    AgentTemplateManager,
    MarketingTemplateFactory,
    FinanceTemplateFactory,
    OperationsTemplateFactory,
    GeneralTemplateFactory
)

def test_template_creation():
    # Initialize template manager
    manager = AgentTemplateManager()
    
    # Test 1: Verify template loading
    templates = manager.list_templates()
    print(f"\n1. Template Loading Test:")
    print(f"Loaded templates: {len(templates)}")
    print(f"Template names: {[t.name for t in templates]}")
    
    # Test 2: Department-specific templates
    print("\n2. Department-specific Templates Test:")
    for dept in ['marketing', 'finance', 'operations', 'general']:
        dept_templates = manager.get_templates_by_department(dept)
        print(f"{dept.capitalize()} templates: {[t.name for t in dept_templates]}")
    
    # Test 3: Template compatibility
    print("\n3. Template Compatibility Test:")
    template = MarketingTemplateFactory.create_campaign_analyzer()
    test_columns = ['campaign_spend', 'impressions', 'clicks', 'conversions', 'revenue']
    compatibility = manager.validate_template_compatibility(template, test_columns)
    print(f"Campaign analyzer compatibility: {compatibility['compatible']}")
    print(f"Compatibility score: {compatibility['compatibility_score']}")
    print(f"Missing required columns: {compatibility['missing_required']}")
    print(f"Available optional columns: {compatibility['available_optional']}")
    
    # Test 4: YAML file operations
    print("\n4. YAML File Operations Test:")
    test_template = MarketingTemplateFactory.create_campaign_analyzer()
    yaml_path = "test_template.yaml"
    
    # Save template
    test_template.save_to_file(yaml_path)
    print(f"Template saved to {yaml_path}")
    
    # Load template
    loaded_template = test_template.load_from_file(yaml_path)
    print(f"Template loaded from {yaml_path}")
    print(f"Loaded template name: {loaded_template.name}")
    
    # Clean up
    os.remove(yaml_path)
    
    # Test 5: Building block workflow steps
    print("\n5. Building Block Workflow Steps Test:")
    for template in templates:
        print(f"\nTemplate: {template.name}")
        print(f"Number of workflow steps: {len(template.workflow_steps)}")
        for i, step in enumerate(template.workflow_steps, 1):
            print(f"Step {i}: {step['name']} ({step['type']})")

if __name__ == "__main__":
    test_template_creation() 