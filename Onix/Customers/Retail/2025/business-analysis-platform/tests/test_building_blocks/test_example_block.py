"""
Test suite for DataSummaryBlock demonstrating TDD approach.
This file shows how to write comprehensive tests for building blocks.
"""
import pytest
import asyncio
from src.building_blocks.examples.example_block import DataSummaryBlock


class TestDataSummaryBlock:
    """Test suite for DataSummaryBlock."""
    
    @pytest.fixture
    def block(self):
        """Create a DataSummaryBlock instance for testing."""
        return DataSummaryBlock()
    
    def test_initialization(self, block):
        """Test block can be initialized with required properties."""
        assert block.name == "data_summary"
        assert block.category == "analysis"
    
    @pytest.mark.asyncio
    async def test_execute_with_valid_numeric_data(self, block):
        """Test successful execution with valid numeric input."""
        data = {'dataset': [1, 2, 3, 4, 5]}
        config = {'include_stats': True}
        
        result = await block.execute(data, config)
        
        assert result['success'] is True
        assert result['errors'] == []
        assert 'summary' in result['data']
        
        summary = result['data']['summary']
        assert summary['count'] == 5
        assert summary['unique_values'] == 5
        assert summary['min'] == 1
        assert summary['max'] == 5
        assert summary['mean'] == 3.0
    
    @pytest.mark.asyncio
    async def test_execute_with_valid_mixed_data(self, block):
        """Test execution with mixed data types (no stats)."""
        data = {'dataset': ['a', 'b', 'c', 'a']}
        config = {'include_stats': True}
        
        result = await block.execute(data, config)
        
        assert result['success'] is True
        assert result['errors'] == []
        
        summary = result['data']['summary']
        assert summary['count'] == 4
        assert summary['unique_values'] == 3
        assert 'mean' not in summary  # No stats for non-numeric data
    
    @pytest.mark.asyncio
    async def test_execute_without_stats(self, block):
        """Test execution with stats disabled."""
        data = {'dataset': [1, 2, 3]}
        config = {'include_stats': False}
        
        result = await block.execute(data, config)
        
        assert result['success'] is True
        summary = result['data']['summary']
        assert 'mean' not in summary
        assert 'min' not in summary
        assert 'max' not in summary
    
    @pytest.mark.asyncio
    async def test_execute_with_invalid_data(self, block):
        """Test proper error handling with invalid input."""
        data = {}  # Missing 'dataset'
        config = {}
        
        result = await block.execute(data, config)
        
        assert result['success'] is False
        assert len(result['errors']) > 0
        assert "Missing required field: 'dataset'" in result['errors']
    
    def test_validate_input_missing_dataset(self, block):
        """Test input validation catches missing dataset."""
        errors = block.validate_input({})
        assert "Missing required field: 'dataset'" in errors
    
    def test_validate_input_invalid_type(self, block):
        """Test input validation catches invalid type."""
        errors = block.validate_input({'dataset': 'not_a_list'})
        assert "'dataset' must be a list" in errors
    
    def test_validate_input_empty_dataset(self, block):
        """Test input validation catches empty dataset."""
        errors = block.validate_input({'dataset': []})
        assert "'dataset' cannot be empty" in errors
    
    def test_validate_input_valid_data(self, block):
        """Test input validation passes with valid data."""
        errors = block.validate_input({'dataset': [1, 2, 3]})
        assert errors == []
    
    def test_config_schema(self, block):
        """Test config schema is properly defined."""
        schema = block.get_config_schema()
        
        assert schema['type'] == 'object'
        assert 'include_stats' in schema['properties']
        assert schema['properties']['include_stats']['type'] == 'boolean'
        assert schema['properties']['include_stats']['default'] is True
    
    @pytest.mark.asyncio
    async def test_execute_with_exception(self, block, mocker):
        """Test exception handling during execution."""
        # Mock the validate_input method to raise an exception
        mocker.patch.object(block, 'validate_input', side_effect=Exception("Test error"))
        
        data = {'dataset': [1, 2, 3]}
        config = {}
        
        result = await block.execute(data, config)
        
        assert result['success'] is False
        assert len(result['errors']) > 0
        assert "Test error" in result['errors'][0]