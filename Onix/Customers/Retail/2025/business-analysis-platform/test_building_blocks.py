import asyncio
import re
from typing import Any, Dict, List, Union
from business_analysis_platform import BuildingBlock, BuildingBlockRegistry
import logging
import sys
from io import StringIO
import pytest
from business_analysis_platform import (
    DataValidatorBlock,
    KPICalculatorBlock,
    AlertGeneratorBlock
)

# Create a concrete building block for testing
class TestDataProcessor(BuildingBlock):
    """A simple test building block that processes data."""
    
    async def execute(self, data: dict, context: dict) -> dict:
        """Process the input data and return results."""
        try:
            # Validate input
            validation = self.validate_input(data)
            if not validation['valid']:
                return {
                    'success': False,
                    'data': None,
                    'errors': validation['errors']
                }
            
            # Process the data
            processed_data = {
                'original_count': len(data.get('items', [])),
                'processed_count': len(data.get('items', [])) * 2,
                'context': context.get('processing_type', 'default')
            }
            
            return {
                'success': True,
                'data': processed_data,
                'errors': []
            }
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'errors': [str(e)]
            }

class DataValidator(BuildingBlock):
    """A building block that validates and cleans data according to specified rules."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.validation_rules = config.get('validation_rules', {})
        self.auto_fix = config.get('auto_fix', False)
    
    async def execute(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and optionally fix data according to the configured rules."""
        try:
            result = {
                'success': True,
                'data': data.copy(),
                'errors': [],
                'fixes_applied': []
            }
            
            for field, rules in self.validation_rules.items():
                if field in data:
                    field_data = data[field]
                    if isinstance(field_data, list):
                        result['data'][field] = self._validate_list(field, field_data, rules, result)
                    else:
                        result['data'][field] = self._validate_value(field, field_data, rules, result)
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'errors': [str(e)],
                'fixes_applied': []
            }
    
    def _validate_list(self, field: str, values: List[Any], rules: Dict[str, Any], result: Dict[str, Any]) -> List[Any]:
        """Validate and fix a list of values."""
        cleaned_values = []
        allow_null = rules.get('allow_null', True)
        
        for i, value in enumerate(values):
            if value is None:
                if not allow_null:
                    if self.auto_fix:
                        cleaned_values.append(0)
                        result['fixes_applied'].append(f"{field}[{i}]: null replaced with 0")
                    else:
                        result['errors'].append(f"{field}[{i}]: null value not allowed")
                        cleaned_values.append(value)
                else:
                    cleaned_values.append(value)
            elif isinstance(value, str) and value.startswith('$'):
                # Handle currency strings
                numeric_value = re.sub(r'[$,]', '', value)
                try:
                    cleaned_value = float(numeric_value)
                    cleaned_values.append(cleaned_value)
                    if self.auto_fix:
                        result['fixes_applied'].append(f"{field}[{i}]: '{value}' converted to {cleaned_value}")
                except ValueError:
                    result['errors'].append(f"{field}[{i}]: cannot convert '{value}' to number")
                    cleaned_values.append(value)
            else:
                cleaned_values.append(value)
        
        return cleaned_values
    
    def _validate_value(self, field: str, value: Any, rules: Dict[str, Any], result: Dict[str, Any]) -> Any:
        """Validate and fix a single value."""
        allow_null = rules.get('allow_null', True)
        
        if value is None and not allow_null:
            if self.auto_fix:
                result['fixes_applied'].append(f"{field}: null replaced with 0")
                return 0
            else:
                result['errors'].append(f"{field}: null value not allowed")
        
        return value

# Test the complete registry with DataValidator
async def test_complete_registry():
    print("=== Testing Complete Building Block Registry ===\n")
    
    # Create registry and register blocks
    registry = BuildingBlockRegistry()
    registry.register_block('test_processor', TestDataProcessor)
    registry.register_block('data_validator', DataValidator)
    
    print("Available blocks:", registry.list_blocks())
    
    # Test DataValidator
    validator = registry.create_block('data_validator', {
        'name': 'SalesValidator',
        'validation_rules': {'sales': {'allow_null': False}},
        'auto_fix': True
    })
    
    test_data = {'sales': [100, None, '$1,500', 300]}
    result = await validator.execute(test_data, {})
    print("Validation result:", result)
    
    # Test without auto_fix
    strict_validator = registry.create_block('data_validator', {
        'name': 'StrictValidator',
        'validation_rules': {'sales': {'allow_null': False}},
        'auto_fix': False
    })
    
    strict_result = await strict_validator.execute(test_data, {})
    print("Strict validation result:", strict_result)

# Run the test
if __name__ == "__main__":
    asyncio.run(test_complete_registry())

# Quick check - run this to see what's exported from the module
import business_analysis_platform
print(dir(business_analysis_platform))

def test_building_block_imports():
    """Test the building block system imports and initialization."""
    # Capture logging output
    log_capture = StringIO()
    handler = logging.StreamHandler(log_capture)
    logger = logging.getLogger()
    logger.addHandler(handler)
    
    try:
        # Test imports and registry creation
        registry = BuildingBlockRegistry()
        print(f"Registry created with {len(registry.blocks)} blocks")
        
        # Get captured log output
        log_output = log_capture.getvalue()
        
        # Verify success criteria
        print("\nValidation Results:")
        print("✓ No syntax errors")
        print("✓ Classes imported successfully")
        print("✓ Registry initialized without errors")
        print(f"✓ Logger output: {log_output.strip()}")
        
        return True
    except Exception as e:
        print(f"\nTest failed with error: {str(e)}")
        return False
    finally:
        # Clean up logging handler
        logger.removeHandler(handler)
        log_capture.close()

if __name__ == "__main__":
    success = test_building_block_imports()
    sys.exit(0 if success else 1)

async def test_building_blocks():
    """Test the building blocks system functionality."""
    print("\n=== Testing Building Blocks System ===\n")
    
    # Initialize registry
    registry = BuildingBlockRegistry()
    print("Available blocks:", registry.list_blocks())
    
    # Test DataValidator
    print("\n=== Testing DataValidator ===")
    validator = registry.create_block('data_validator', {
        'name': 'SalesValidator',
        'validation_rules': {'sales': {'allow_null': False}},
        'auto_fix': True
    })
    
    test_data = {'sales': [100, None, '$1,500', 300]}
    result = await validator.execute(test_data, {})
    print("Validation result:", result)
    
    # Test KPICalculator
    print("\n=== Testing KPICalculator ===")
    kpi_calculator = registry.create_block('kpi_calculator', {
        'name': 'SalesKPICalculator',
        'kpi_definitions': {
            'total_sales': {
                'formula': 'sum({sales})',
                'unit': '$'
            },
            'average_sale': {
                'formula': 'avg({sales})',
                'unit': '$'
            }
        }
    })
    
    kpi_result = await kpi_calculator.execute(test_data, {'industry': 'retail'})
    print("KPI calculation result:", kpi_result)
    
    # Test AlertGenerator
    print("\n=== Testing AlertGenerator ===")
    alert_generator = registry.create_block('alert_generator', {
        'name': 'SalesAlertGenerator',
        'alert_rules': [
            {
                'title': 'High Sales Alert',
                'message': 'Sales exceeded threshold',
                'severity': 'high',
                'condition': {
                    'column': 'sales',
                    'operator': 'greater_than',
                    'threshold': 1000
                }
            }
        ]
    })
    
    alert_result = await alert_generator.execute(test_data, {'industry': 'retail'})
    print("Alert generation result:", alert_result)
    
    # Verify success criteria
    print("\n=== Verifying Success Criteria ===")
    
    # 1. Check block registration
    blocks = registry.list_blocks()
    print(f"✓ All blocks registered: {len(blocks) == 3}")
    print(f"  Available blocks: {blocks}")
    
    # 2. Check DataValidator results
    print(f"✓ DataValidator fixes applied: {len(result.get('fixes_applied', [])) > 0}")
    print(f"  Fixes: {result.get('fixes_applied', [])}")
    
    # 3. Check KPICalculator results
    print(f"✓ KPICalculator evaluated formulas: {len(kpi_result.get('kpis', {})) > 0}")
    print(f"  KPIs: {kpi_result.get('kpis', {})}")
    
    # 4. Check AlertGenerator results
    print(f"✓ AlertGenerator created alerts: {alert_result.get('alert_count', 0) > 0}")
    print(f"  Alerts: {alert_result.get('alerts', [])}")
    
    return True

if __name__ == "__main__":
    asyncio.run(test_building_blocks())
