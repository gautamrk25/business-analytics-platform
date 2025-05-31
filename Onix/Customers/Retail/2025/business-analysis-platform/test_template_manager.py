from business_analysis_platform import AgentTemplateManager, MarketingTemplateFactory

def test_template_manager():
    # Initialize template manager
    manager = AgentTemplateManager()
    
    # Test template listing
    templates = manager.list_templates()
    print(f"Total templates: {len(templates)}")
    
    # Test marketing template
    marketing_templates = manager.get_templates_by_department("marketing")
    print(f"Marketing templates: {len(marketing_templates)}")
    
    if marketing_templates:
        template = marketing_templates[0]
        print(f"Template name: {template.name}")
        print(f"Required columns: {template.required_columns}")
        
        # Test compatibility
        available_columns = ['campaign_spend', 'impressions', 'clicks', 'conversions']
        compatibility = manager.validate_template_compatibility(template, available_columns)
        print(f"Compatibility score: {compatibility['compatibility_score']}")
        print(f"Missing columns: {compatibility['missing_required']}")

if __name__ == "__main__":
    test_template_manager() 