"""Tests for Smart Data Profiler Building Block"""
import pytest
import asyncio
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from unittest.mock import Mock, patch, AsyncMock
from typing import Dict, Any, List

# Note: These imports will fail until implementation exists (TDD Red phase)
try:
    from src.building_blocks.data.smart_data_profiler import SmartDataProfiler
except ImportError:
    # This is expected in TDD red phase - tests written before implementation
    SmartDataProfiler = None

from src.building_blocks.base import BuildingBlock
from src.utils.learning_history import LearningHistoryManager


@pytest.mark.skipif(SmartDataProfiler is None, reason="SmartDataProfiler not implemented yet (TDD Red phase)")
class TestSmartDataProfiler:
    """Test suite for SmartDataProfiler"""
    
    @pytest.fixture
    def profiler(self):
        """Create a smart data profiler instance"""
        return SmartDataProfiler()
    
    @pytest.fixture
    def profiler_with_learning(self, mock_learning_history):
        """Create a profiler with learning history"""
        return SmartDataProfiler(learning_history=mock_learning_history)
    
    @pytest.fixture
    def sample_sales_data(self):
        """Create DataFrame with sales data"""
        dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
        return pd.DataFrame({
            'date': dates,
            'sales': np.random.randint(1000, 5000, size=len(dates)),
            'profit': np.random.uniform(100, 1000, size=len(dates)),
            'store_id': [f'STORE_{i%5:03d}' for i in range(len(dates))],
            'region': ['North', 'South', 'East', 'West'] * 8 + ['North'] * 3,
            'is_weekend': [d.weekday() >= 5 for d in dates]
        })
    
    @pytest.fixture
    def sample_customer_data(self):
        """Create DataFrame with customer data"""
        n_customers = 100
        return pd.DataFrame({
            'customer_id': [f'CUST_{i:05d}' for i in range(n_customers)],
            'email': [f'user{i}@example.com' for i in range(n_customers)],
            'age': np.random.randint(18, 80, size=n_customers),
            'signup_date': pd.date_range(start='2023-01-01', periods=n_customers, freq='D'),
            'total_purchases': np.random.poisson(10, size=n_customers),
            'category': np.random.choice(['Bronze', 'Silver', 'Gold'], size=n_customers),
            'phone': [f'+1-555-{np.random.randint(1000000, 9999999):07d}' for _ in range(n_customers)]
        })
    
    @pytest.fixture
    def large_dataset(self):
        """Create large DataFrame for performance testing"""
        n_rows = 100000
        return pd.DataFrame({
            'id': range(n_rows),
            'value': np.random.normal(100, 15, size=n_rows),
            'category': np.random.choice(['A', 'B', 'C', 'D'], size=n_rows),
            'timestamp': pd.date_range(start='2024-01-01', periods=n_rows, freq='1min')
        })
    
    @pytest.fixture
    def mock_learning_history(self):
        """Mock LearningHistoryManager"""
        mock = Mock(spec=LearningHistoryManager)
        mock.get_learned_patterns = Mock(return_value={})
        mock.record_pattern = Mock()
        mock.suggest_column_type = Mock(return_value=None)
        return mock
    
    def test_initialization(self, profiler):
        """Test profiler initialization without learning history"""
        assert profiler.name == "smart_data_profiler"
        assert profiler.category == "data"
        assert isinstance(profiler, BuildingBlock)
        assert profiler.learning_history is None
    
    def test_initialization_with_learning(self, profiler_with_learning, mock_learning_history):
        """Test profiler initialization with learning history"""
        assert profiler_with_learning.name == "smart_data_profiler"
        assert profiler_with_learning.category == "data"
        assert profiler_with_learning.learning_history == mock_learning_history
    
    @pytest.mark.asyncio
    async def test_execute_with_numeric_data(self, profiler):
        """Test profiling of numeric columns"""
        df = pd.DataFrame({
            'integers': [1, 2, 3, 4, 5, None],
            'floats': [1.1, 2.2, 3.3, None, 5.5, 6.6],
            'all_nulls': [None, None, None, None, None, None],
            'single_value': [42, 42, 42, 42, 42, 42]
        })
        
        data = {'dataframe': df}
        config = {'enable_learning': False}
        
        result = await profiler.execute(data, config)
        
        assert result['success'] is True
        assert 'profile' in result['data']
        
        profile = result['data']['profile']
        
        # Test integers profile
        assert 'integers' in profile
        int_profile = profile['integers']
        assert int_profile['dtype'] == 'numeric'
        assert int_profile['mean'] == 3.0
        assert int_profile['median'] == 3.0
        assert int_profile['std_dev'] > 0
        assert int_profile['min'] == 1
        assert int_profile['max'] == 5
        assert int_profile['null_count'] == 1
        
        # Test floats profile
        assert 'floats' in profile
        float_profile = profile['floats']
        assert float_profile['dtype'] == 'numeric'
        assert float_profile['null_count'] == 1
        
        # Test all nulls
        assert 'all_nulls' in profile
        null_profile = profile['all_nulls']
        assert null_profile['null_count'] == 6
        
        # Test single value
        assert 'single_value' in profile
        single_profile = profile['single_value']
        assert single_profile['std_dev'] == 0
        assert single_profile['min'] == 42
        assert single_profile['max'] == 42
    
    @pytest.mark.asyncio
    async def test_execute_with_string_data(self, profiler):
        """Test profiling of string columns"""
        df = pd.DataFrame({
            'categories': ['A', 'B', 'A', 'C', 'B', 'A', None],
            'unique_ids': ['ID001', 'ID002', 'ID003', 'ID004', 'ID005', 'ID006', 'ID007'],
            'mixed': ['text', 'text', 'text', None, 'other', 'text', 'different']
        })
        
        data = {'dataframe': df}
        config = {'enable_learning': False}
        
        result = await profiler.execute(data, config)
        
        assert result['success'] is True
        profile = result['data']['profile']
        
        # Test categories
        assert 'categories' in profile
        cat_profile = profile['categories']
        assert cat_profile['dtype'] == 'string'
        assert cat_profile['unique_count'] == 3  # A, B, C (excluding None)
        assert 'most_common_values' in cat_profile
        assert cat_profile['null_count'] == 1
        
        # Test unique IDs
        assert 'unique_ids' in profile
        id_profile = profile['unique_ids']
        assert id_profile['unique_count'] == 7
        assert id_profile['is_potential_id'] is True
    
    @pytest.mark.asyncio
    async def test_execute_with_date_data(self, profiler):
        """Test profiling of date columns"""
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        df = pd.DataFrame({
            'dates': dates,
            'sparse_dates': [dates[i] if i % 7 == 0 else None for i in range(len(dates))],
            'string_dates': dates.strftime('%Y-%m-%d')
        })
        
        data = {'dataframe': df}
        config = {'enable_learning': False}
        
        result = await profiler.execute(data, config)
        
        assert result['success'] is True
        profile = result['data']['profile']
        
        # Test date column
        assert 'dates' in profile
        date_profile = profile['dates']
        assert date_profile['dtype'] == 'datetime'
        assert 'date_range' in date_profile
        assert 'frequency' in date_profile
        
        # Test sparse dates
        assert 'sparse_dates' in profile
        sparse_profile = profile['sparse_dates']
        assert sparse_profile['null_count'] > 0
    
    @pytest.mark.asyncio
    async def test_pattern_detection(self, profiler):
        """Test pattern detection capabilities"""
        df = pd.DataFrame({
            'email': ['user1@example.com', 'user2@example.com', 'invalid', None],
            'phone': ['+1-555-123-4567', '+1-555-987-6543', '555-111-2222', 'invalid'],
            'date_string': ['2024-01-01', '2024-02-01', '2024/03/01', 'not a date'],
            'id_column': ['ID001', 'ID002', 'ID003', 'ID004'],
            'category': ['Type A', 'Type B', 'Type A', 'Type C'],
            'continuous': np.random.normal(100, 15, size=4)
        })
        
        data = {'dataframe': df}
        config = {'enable_learning': False, 'pattern_threshold': 0.6}
        
        result = await profiler.execute(data, config)
        
        assert result['success'] is True
        profile = result['data']['profile']
        patterns = result['data']['patterns']
        
        # Email pattern detection
        assert 'email' in patterns
        assert patterns['email']['is_email'] is True
        
        # Phone pattern detection
        assert 'phone' in patterns
        assert patterns['phone']['is_phone'] is True
        
        # Date pattern detection
        assert 'date_string' in patterns
        assert patterns['date_string']['is_date'] is True
        
        # ID detection
        assert 'id_column' in patterns
        assert patterns['id_column']['is_id'] is True
        
        # Categorical vs continuous detection
        assert patterns['category']['is_categorical'] is True
        assert patterns['continuous']['is_continuous'] is True
    
    @pytest.mark.asyncio
    async def test_learning_integration(self, profiler_with_learning, mock_learning_history):
        """Test integration with learning history"""
        df = pd.DataFrame({
            'customer_id': ['C001', 'C002', 'C003'],
            'amount': [100.50, 200.75, 150.25],
            'status': ['active', 'inactive', 'active']
        })
        
        # Mock learned patterns
        mock_learning_history.get_learned_patterns.return_value = {
            'customer_id': {'type': 'id', 'confidence': 0.95},
            'amount': {'type': 'currency', 'confidence': 0.87}
        }
        
        mock_learning_history.suggest_column_type.side_effect = [
            'id', 'currency', 'categorical'
        ]
        
        data = {'dataframe': df}
        config = {'enable_learning': True}
        
        result = await profiler_with_learning.execute(data, config)
        
        assert result['success'] is True
        assert mock_learning_history.get_learned_patterns.called
        assert mock_learning_history.record_pattern.call_count >= 3  # Called for each column
        
        # Verify learned patterns are used
        profile = result['data']['profile']
        assert profile['customer_id']['suggested_type'] == 'id'
        assert profile['amount']['suggested_type'] == 'currency'
    
    def test_validate_input(self, profiler):
        """Test input validation"""
        # Missing dataframe
        errors = profiler.validate_input({})
        assert len(errors) == 1
        assert "Missing required field: 'dataframe'" in errors[0]
        
        # Invalid dataframe type
        errors = profiler.validate_input({'dataframe': 'not a dataframe'})
        assert len(errors) == 1
        assert "'dataframe' must be a pandas DataFrame" in errors[0]
        
        # Empty dataframe
        errors = profiler.validate_input({'dataframe': pd.DataFrame()})
        assert len(errors) == 1
        assert "'dataframe' cannot be empty" in errors[0]
        
        # Valid input
        errors = profiler.validate_input({'dataframe': pd.DataFrame({'a': [1, 2, 3]})})
        assert len(errors) == 0
    
    def test_config_schema(self, profiler):
        """Test configuration schema"""
        schema = profiler.get_config_schema()
        
        assert schema['type'] == 'object'
        
        properties = schema['properties']
        assert 'enable_learning' in properties
        assert properties['enable_learning']['type'] == 'boolean'
        assert properties['enable_learning']['default'] is True
        
        assert 'sample_size' in properties
        assert properties['sample_size']['type'] == 'integer'
        assert properties['sample_size']['default'] == 100000
        
        assert 'pattern_threshold' in properties
        assert properties['pattern_threshold']['type'] == 'number'
        assert properties['pattern_threshold']['minimum'] == 0
        assert properties['pattern_threshold']['maximum'] == 1
        assert properties['pattern_threshold']['default'] == 0.8
    
    @pytest.mark.asyncio
    async def test_correlation_detection(self, profiler):
        """Test correlation detection between numeric columns"""
        n = 100
        x = np.linspace(0, 10, n)
        
        df = pd.DataFrame({
            'perfect_corr_1': x,
            'perfect_corr_2': x * 2 + 5,  # Perfect positive correlation
            'negative_corr': -x + 10,     # Perfect negative correlation
            'no_corr': np.random.random(n),  # No correlation
            'string_col': ['A'] * n      # Non-numeric column
        })
        
        data = {'dataframe': df}
        config = {'enable_learning': False}
        
        result = await profiler.execute(data, config)
        
        assert result['success'] is True
        correlations = result['data']['correlations']
        
        # Check perfect positive correlation
        assert abs(correlations['perfect_corr_1']['perfect_corr_2'] - 1.0) < 0.01
        
        # Check perfect negative correlation
        assert abs(correlations['perfect_corr_1']['negative_corr'] - (-1.0)) < 0.01
        
        # Check no correlation
        assert abs(correlations['perfect_corr_1']['no_corr']) < 0.3
        
        # String column should not appear in correlations
        assert 'string_col' not in correlations
    
    @pytest.mark.asyncio
    async def test_outlier_detection(self, profiler):
        """Test outlier detection in numeric data"""
        # Create data with clear outliers
        normal_data = np.random.normal(100, 10, size=95)
        outliers = [200, 250, -50, -100, 300]  # Clear outliers
        data_with_outliers = np.concatenate([normal_data, outliers])
        
        df = pd.DataFrame({
            'values': data_with_outliers,
            'no_outliers': np.random.normal(50, 5, size=100),
            'categories': ['A'] * 100  # Non-numeric
        })
        
        data = {'dataframe': df}
        config = {'enable_learning': False}
        
        result = await profiler.execute(data, config)
        
        assert result['success'] is True
        profile = result['data']['profile']
        
        # Check outliers detected in values column
        assert 'outliers' in profile['values']
        outlier_info = profile['values']['outliers']
        assert outlier_info['count'] >= 3  # At least some outliers detected
        assert 'indices' in outlier_info
        assert 'values' in outlier_info
        
        # No outliers in normal data
        assert profile['no_outliers']['outliers']['count'] == 0
    
    @pytest.mark.asyncio
    async def test_data_quality_scoring(self, profiler):
        """Test data quality scoring"""
        # High quality data
        high_quality_df = pd.DataFrame({
            'complete': range(100),
            'no_outliers': np.random.normal(50, 5, size=100)
        })
        
        # Poor quality data
        poor_quality_df = pd.DataFrame({
            'many_nulls': [None] * 50 + list(range(50)),
            'outliers': np.concatenate([np.random.normal(50, 5, 90), [500, -500] * 5]),
            'sparse': [1 if i % 10 == 0 else None for i in range(100)]
        })
        
        # Test high quality
        result_high = await profiler.execute(
            {'dataframe': high_quality_df},
            {'enable_learning': False}
        )
        assert result_high['success'] is True
        assert result_high['data']['quality_score'] > 90  # High score
        
        # Test poor quality
        result_poor = await profiler.execute(
            {'dataframe': poor_quality_df},
            {'enable_learning': False}
        )
        assert result_poor['success'] is True
        assert result_poor['data']['quality_score'] < 60  # Low score
    
    @pytest.mark.asyncio
    async def test_missing_value_patterns(self, profiler):
        """Test detection of missing value patterns"""
        n = 100
        df = pd.DataFrame({
            'random_missing': [None if np.random.random() < 0.1 else i for i in range(n)],
            'systematic_missing': [None if i % 5 == 0 else i for i in range(n)],  # Every 5th value
            'block_missing': [None] * 20 + list(range(20, n)),  # First 20 missing
            'no_missing': range(n)
        })
        
        data = {'dataframe': df}
        config = {'enable_learning': False}
        
        result = await profiler.execute(data, config)
        
        assert result['success'] is True
        missing_patterns = result['data']['missing_patterns']
        
        # Random missing pattern
        assert missing_patterns['random_missing']['pattern'] == 'random'
        
        # Systematic pattern
        assert missing_patterns['systematic_missing']['pattern'] == 'systematic'
        
        # Block pattern
        assert missing_patterns['block_missing']['pattern'] == 'block'
        
        # No missing values
        assert missing_patterns['no_missing']['pattern'] == 'none'
    
    @pytest.mark.asyncio
    async def test_large_dataset_sampling(self, profiler, large_dataset):
        """Test automatic sampling for large datasets"""
        data = {'dataframe': large_dataset}
        config = {
            'enable_learning': False,
            'sample_size': 10000  # Force sampling
        }
        
        # Mock the sampling to verify it's called
        with patch.object(profiler, '_sample_dataframe') as mock_sample:
            mock_sample.return_value = large_dataset.head(10000)
            
            result = await profiler.execute(data, config)
            
            assert result['success'] is True
            assert mock_sample.called
            assert result['data']['metadata']['sampled'] is True
            assert result['data']['metadata']['sample_size'] == 10000
            assert result['data']['metadata']['original_size'] == len(large_dataset)
    
    @pytest.mark.asyncio
    async def test_execute_with_mixed_types(self, profiler):
        """Test with dataframe containing multiple data types"""
        df = pd.DataFrame({
            'mixed_numeric': [1, 2.5, 3, None, 5],
            'mixed_string_numeric': ['1', '2', 'three', '4', None],
            'mixed_dates': [
                '2024-01-01',
                datetime(2024, 1, 2),
                pd.Timestamp('2024-01-03'),
                'not a date',
                None
            ],
            'boolean': [True, False, True, None, False],
            'object': [{'a': 1}, [1, 2, 3], 'string', 42, None]
        })
        
        data = {'dataframe': df}
        config = {'enable_learning': False}
        
        result = await profiler.execute(data, config)
        
        assert result['success'] is True
        profile = result['data']['profile']
        
        # Verify each column is handled appropriately
        assert 'mixed_numeric' in profile
        assert profile['mixed_numeric']['dtype'] == 'numeric'
        
        assert 'mixed_string_numeric' in profile
        assert profile['mixed_string_numeric']['dtype'] == 'mixed'
        
        assert 'mixed_dates' in profile
        assert profile['mixed_dates']['dtype'] == 'mixed'
        
        assert 'boolean' in profile
        assert profile['boolean']['dtype'] == 'boolean'
        
        assert 'object' in profile
        assert profile['object']['dtype'] == 'object'
    
    # Edge case tests
    @pytest.mark.asyncio
    async def test_empty_dataframe(self, profiler):
        """Test with empty dataframe"""
        df = pd.DataFrame()
        data = {'dataframe': df}
        config = {'enable_learning': False}
        
        # Should fail validation
        errors = profiler.validate_input(data)
        assert len(errors) > 0
        assert "empty" in errors[0].lower()
    
    @pytest.mark.asyncio
    async def test_single_row_dataframe(self, profiler):
        """Test with single row dataframe"""
        df = pd.DataFrame({'a': [1], 'b': ['test'], 'c': [datetime.now()]})
        data = {'dataframe': df}
        config = {'enable_learning': False}
        
        result = await profiler.execute(data, config)
        
        assert result['success'] is True
        profile = result['data']['profile']
        
        # Single row stats should still work
        assert profile['a']['count'] == 1
        assert profile['a']['std_dev'] == 0  # No variation in single row
    
    @pytest.mark.asyncio
    async def test_single_column_dataframe(self, profiler):
        """Test with single column dataframe"""
        df = pd.DataFrame({'only_column': range(10)})
        data = {'dataframe': df}
        config = {'enable_learning': False}
        
        result = await profiler.execute(data, config)
        
        assert result['success'] is True
        assert len(result['data']['profile']) == 1
        assert 'only_column' in result['data']['profile']
    
    @pytest.mark.asyncio 
    async def test_all_null_columns(self, profiler):
        """Test with columns containing only null values"""
        df = pd.DataFrame({
            'all_none': [None] * 10,
            'all_nan': [np.nan] * 10,
            'normal': range(10)
        })
        data = {'dataframe': df}
        config = {'enable_learning': False}
        
        result = await profiler.execute(data, config)
        
        assert result['success'] is True
        profile = result['data']['profile']
        
        assert profile['all_none']['null_count'] == 10
        assert profile['all_none']['null_percentage'] == 100.0
        
        assert profile['all_nan']['null_count'] == 10
        assert profile['all_nan']['null_percentage'] == 100.0
    
    @pytest.mark.asyncio
    async def test_invalid_config(self, profiler):
        """Test with invalid configuration"""
        df = pd.DataFrame({'a': [1, 2, 3]})
        data = {'dataframe': df}
        
        # Invalid sample size
        config = {'sample_size': -100}
        result = await profiler.execute(data, config)
        assert result['success'] is False
        assert 'Invalid sample_size' in result['errors'][0]
        
        # Invalid pattern threshold
        config = {'pattern_threshold': 2.0}  # Should be between 0 and 1
        result = await profiler.execute(data, config)
        assert result['success'] is False
        assert 'pattern_threshold' in result['errors'][0]
    
    # Performance tests
    @pytest.mark.asyncio
    async def test_performance_with_wide_dataframe(self, profiler):
        """Test performance with many columns"""
        # Create wide dataframe with 100 columns
        n_cols = 100
        n_rows = 1000
        
        data_dict = {f'col_{i}': np.random.random(n_rows) for i in range(n_cols)}
        df = pd.DataFrame(data_dict)
        
        data = {'dataframe': df}
        config = {'enable_learning': False}
        
        import time
        start_time = time.time()
        result = await profiler.execute(data, config)
        execution_time = time.time() - start_time
        
        assert result['success'] is True
        assert execution_time < 10  # Should complete within 10 seconds
        assert len(result['data']['profile']) == n_cols
    
    @pytest.mark.asyncio
    async def test_memory_usage(self, profiler, large_dataset):
        """Test memory usage doesn't explode with large datasets"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        data = {'dataframe': large_dataset}
        config = {'enable_learning': False, 'sample_size': 50000}
        
        result = await profiler.execute(data, config)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        assert result['success'] is True
        assert memory_increase < 500  # Should not use more than 500MB additional