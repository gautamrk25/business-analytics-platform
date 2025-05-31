"""Tests for Code Inspector Agent

This module contains comprehensive tests for the Code Inspector Agent that
analyzes code for errors, suggests fixes, and provides debugging assistance.
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
import asyncio
from datetime import datetime
import json
import ast
import traceback

from src.agents.code_inspector import (
    CodeInspector,
    InspectionResult,
    ErrorAnalysis,
    FixSuggestion,
    CodeContext,
    InspectionLevel
)
from src.utils.logger import get_logger


logger = get_logger(__name__)


class TestCodeInspector:
    """Test suite for Code Inspector Agent"""
    
    def test_initialization(self):
        """Test basic initialization of Code Inspector"""
        inspector = CodeInspector()
        assert inspector is not None
        assert inspector.name == "code_inspector"
        assert inspector.description == "Analyzes code for errors and suggests fixes"
        assert hasattr(inspector, 'learning_history')
    
    def test_initialization_with_learning_history(self):
        """Test initialization with learning history manager"""
        mock_learning = Mock()
        inspector = CodeInspector(learning_history=mock_learning)
        assert inspector.learning_history == mock_learning
    
    @pytest.mark.asyncio
    async def test_analyze_syntax_error(self):
        """Test analysis of Python syntax errors"""
        code = '''
def calculate_total(items):
    total = 0
    for item in items
        total += item.price
    return total
'''
        error_message = "SyntaxError: invalid syntax"
        error_line = 4
        
        inspector = CodeInspector()
        result = await inspector.analyze_error(
            code=code,
            error_message=error_message,
            error_line=error_line
        )
        
        assert result.success is True
        assert result.error_type == "SyntaxError"
        assert result.error_line == 4
        assert len(result.suggestions) > 0
        
        # Should suggest adding colon
        colon_suggestion = next(
            (s for s in result.suggestions if ":" in s.fix_code),
            None
        )
        assert colon_suggestion is not None
        assert colon_suggestion.confidence > 0.8
    
    @pytest.mark.asyncio
    async def test_analyze_import_error(self):
        """Test analysis of import errors"""
        code = '''
import pandas as pd
import numpy as np
from sklearn import preprocessing
import non_existent_module
'''
        error_message = "ModuleNotFoundError: No module named 'non_existent_module'"
        error_line = 5
        
        inspector = CodeInspector()
        result = await inspector.analyze_error(
            code=code,
            error_message=error_message,
            error_line=error_line
        )
        
        assert result.success is True
        assert result.error_type == "ModuleNotFoundError"
        assert len(result.suggestions) > 0
        
        # Should suggest installing or removing the import
        suggestions_text = [s.description for s in result.suggestions]
        assert any("pip install" in text for text in suggestions_text)
        assert any("remove" in text.lower() for text in suggestions_text)
    
    @pytest.mark.asyncio
    async def test_analyze_attribute_error(self):
        """Test analysis of attribute errors"""
        code = '''
data = pd.DataFrame({'A': [1, 2, 3]})
result = data.groupby('A').aggregate()
print(result)
'''
        error_message = "AttributeError: 'DataFrameGroupBy' object has no attribute 'aggregate'"
        error_line = 2
        
        inspector = CodeInspector()
        result = await inspector.analyze_error(
            code=code,
            error_message=error_message,
            error_line=error_line,
            context={"pandas_version": "1.3.0"}
        )
        
        assert result.success is True
        assert result.error_type == "AttributeError"
        assert len(result.suggestions) > 0
        
        # Should suggest using 'agg' instead of 'aggregate'
        agg_suggestion = next(
            (s for s in result.suggestions if "agg" in s.fix_code),
            None
        )
        assert agg_suggestion is not None
    
    @pytest.mark.asyncio
    async def test_analyze_type_error(self):
        """Test analysis of type errors"""
        code = '''
def process_data(values):
    total = sum(values)
    average = total / len(values)
    return average

result = process_data("not a list")
'''
        error_message = "TypeError: unsupported operand type(s) for +: 'int' and 'str'"
        error_line = 3
        
        inspector = CodeInspector()
        result = await inspector.analyze_error(
            code=code,
            error_message=error_message,
            error_line=error_line,
            stack_trace="..." # Would include full stack trace
        )
        
        assert result.success is True
        assert result.error_type == "TypeError"
        assert len(result.suggestions) > 0
        
        # Should suggest type checking or conversion
        assert any("isinstance" in s.fix_code for s in result.suggestions)
    
    @pytest.mark.asyncio
    async def test_analyze_indentation_error(self):
        """Test analysis of indentation errors"""
        code = '''
def process_items(items):
    for item in items:
    print(item.name)
        print(item.price)
'''
        error_message = "IndentationError: expected an indented block"
        error_line = 4
        
        inspector = CodeInspector()
        result = await inspector.analyze_error(
            code=code,
            error_message=error_message,
            error_line=error_line
        )
        
        assert result.success is True
        assert result.error_type == "IndentationError"
        assert len(result.suggestions) > 0
        
        # Should suggest proper indentation
        assert any("proper indentation" in s.description.lower() for s in result.suggestions)
    
    @pytest.mark.asyncio
    async def test_analyze_key_error(self):
        """Test analysis of key errors in dictionaries"""
        code = '''
config = {
    'host': 'localhost',
    'port': 5432
}
database_name = config['database']
'''
        error_message = "KeyError: 'database'"
        error_line = 6
        
        inspector = CodeInspector()
        result = await inspector.analyze_error(
            code=code,
            error_message=error_message,
            error_line=error_line
        )
        
        assert result.success is True
        assert result.error_type == "KeyError"
        assert len(result.suggestions) > 0
        
        # Should suggest using .get() or checking if key exists
        assert any(".get(" in s.fix_code for s in result.suggestions)
        assert any("if" in s.fix_code and "in" in s.fix_code for s in result.suggestions)
    
    @pytest.mark.asyncio
    async def test_analyze_value_error(self):
        """Test analysis of value errors"""
        code = '''
def convert_to_int(value):
    return int(value)

result = convert_to_int("not a number")
'''
        error_message = "ValueError: invalid literal for int() with base 10: 'not a number'"
        error_line = 3
        
        inspector = CodeInspector()
        result = await inspector.analyze_error(
            code=code,
            error_message=error_message,
            error_line=error_line
        )
        
        assert result.success is True
        assert result.error_type == "ValueError"
        assert len(result.suggestions) > 0
        
        # Should suggest try-except or validation
        assert any("try:" in s.fix_code for s in result.suggestions)
    
    @pytest.mark.asyncio
    async def test_analyze_async_error(self):
        """Test analysis of async/await errors"""
        code = '''
async def fetch_data(url):
    response = await requests.get(url)
    return response.json()

data = fetch_data("https://api.example.com")
print(data)
'''
        error_message = "RuntimeWarning: coroutine 'fetch_data' was never awaited"
        error_line = 6
        
        inspector = CodeInspector()
        result = await inspector.analyze_error(
            code=code,
            error_message=error_message,
            error_line=error_line
        )
        
        assert result.success is True
        assert "await" in result.primary_cause
        assert len(result.suggestions) > 0
        
        # Should suggest using await or asyncio.run
        assert any("await" in s.fix_code for s in result.suggestions)
        assert any("asyncio.run" in s.fix_code for s in result.suggestions)
    
    @pytest.mark.asyncio
    async def test_suggest_fix_for_pandas_error(self):
        """Test fix suggestions for common pandas errors"""
        code = '''
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
df['C'] = df.apply(lambda row: row['A'] + row['B'])
'''
        error_message = "ValueError: The truth value of a Series is ambiguous"
        error_line = 3
        
        inspector = CodeInspector()
        result = await inspector.analyze_error(
            code=code,
            error_message=error_message,
            error_line=error_line
        )
        
        assert result.success is True
        assert len(result.suggestions) > 0
        
        # Should suggest adding axis parameter
        axis_suggestion = next(
            (s for s in result.suggestions if "axis=" in s.fix_code),
            None
        )
        assert axis_suggestion is not None
        assert axis_suggestion.fix_code.count("axis=1") == 1
    
    @pytest.mark.asyncio
    async def test_analyze_with_context(self):
        """Test error analysis with additional context"""
        code = '''
from mypackage import process_data

result = process_data(input_data)
'''
        error_message = "AttributeError: 'NoneType' object has no attribute 'shape'"
        error_line = 3
        
        context = CodeContext(
            variables={"input_data": "None"},
            imports=["mypackage"],
            function_signatures={"process_data": "def process_data(data: np.ndarray) -> np.ndarray"},
            environment={"python_version": "3.9", "numpy_version": "1.21.0"}
        )
        
        inspector = CodeInspector()
        result = await inspector.analyze_error(
            code=code,
            error_message=error_message,
            error_line=error_line,
            context=context
        )
        
        assert result.success is True
        assert "None" in result.primary_cause
        assert len(result.suggestions) > 0
        
        # Should suggest checking for None before processing
        none_check = next(
            (s for s in result.suggestions if "is not None" in s.fix_code),
            None
        )
        assert none_check is not None
    
    @pytest.mark.asyncio
    async def test_analyze_building_block_error(self):
        """Test analysis of BuildingBlock-specific errors"""
        code = '''
class MyBlock(BuildingBlock):
    def execute(self, data, config):
        result = data['dataframe'].groupby('category').mean()
        return result
'''
        error_message = "AttributeError: 'MyBlock' object has no attribute 'name'"
        error_line = 1
        
        inspector = CodeInspector()
        result = await inspector.analyze_error(
            code=code,
            error_message=error_message,
            error_line=error_line,
            context={"class": "BuildingBlock"}
        )
        
        assert result.success is True
        assert len(result.suggestions) > 0
        
        # Should suggest implementing required abstract methods
        abstract_suggestion = next(
            (s for s in result.suggestions if "@property" in s.fix_code and "name" in s.fix_code),
            None
        )
        assert abstract_suggestion is not None
    
    @pytest.mark.asyncio
    async def test_analyze_validation_error(self):
        """Test analysis of validation errors"""
        code = '''
validator = DataValidator()
result = validator.execute(
    data={'invalid': 'structure'},
    config={'rules': []}
)
'''
        error_message = "ValidationError: Missing required field: 'dataframe'"
        error_line = 3
        
        inspector = CodeInspector()
        result = await inspector.analyze_error(
            code=code,
            error_message=error_message,
            error_line=error_line
        )
        
        assert result.success is True
        assert "dataframe" in result.primary_cause
        assert len(result.suggestions) > 0
        
        # Should suggest proper data structure
        assert any("dataframe" in s.fix_code for s in result.suggestions)
    
    @pytest.mark.asyncio
    async def test_learning_integration(self):
        """Test integration with learning history"""
        mock_learning = Mock()
        mock_learning.get_error_patterns.return_value = [
            {
                "error_type": "KeyError",
                "key": "database",
                "suggested_fix": "config.get('database', 'default_db')",
                "success_rate": 0.95
            }
        ]
        
        inspector = CodeInspector(learning_history=mock_learning)
        
        code = '''
config = {'host': 'localhost'}
db = config['database']
'''
        error_message = "KeyError: 'database'"
        
        result = await inspector.analyze_error(
            code=code,
            error_message=error_message,
            error_line=3
        )
        
        assert result.success is True
        assert len(result.suggestions) > 0
        
        # Should include learned pattern with high confidence
        learned_suggestion = next(
            (s for s in result.suggestions if s.confidence > 0.9),
            None
        )
        assert learned_suggestion is not None
        assert "get(" in learned_suggestion.fix_code
    
    @pytest.mark.asyncio
    async def test_multi_line_fix_suggestion(self):
        """Test suggestions that span multiple lines"""
        code = '''
def process_file(filename):
    data = pd.read_csv(filename)
    return data
'''
        error_message = "FileNotFoundError: [Errno 2] No such file or directory: 'data.csv'"
        error_line = 3
        
        inspector = CodeInspector()
        result = await inspector.analyze_error(
            code=code,
            error_message=error_message,
            error_line=error_line
        )
        
        assert result.success is True
        assert len(result.suggestions) > 0
        
        # Should suggest file existence check
        file_check = next(
            (s for s in result.suggestions if "os.path.exists" in s.fix_code or "Path" in s.fix_code),
            None
        )
        assert file_check is not None
        assert file_check.fix_type == "add_validation"
    
    @pytest.mark.asyncio
    async def test_performance_issue_detection(self):
        """Test detection of performance issues"""
        code = '''
def find_duplicates(items):
    duplicates = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j] and items[i] not in duplicates:
                duplicates.append(items[i])
    return duplicates
'''
        # Simulate a performance warning
        error_message = "PerformanceWarning: Quadratic time complexity detected"
        error_line = 2
        
        inspector = CodeInspector()
        result = await inspector.analyze_error(
            code=code,
            error_message=error_message,
            error_line=error_line,
            inspection_level=InspectionLevel.PERFORMANCE
        )
        
        assert result.success is True
        assert len(result.suggestions) > 0
        
        # Should suggest using set for O(n) solution
        set_suggestion = next(
            (s for s in result.suggestions if "set(" in s.fix_code),
            None
        )
        assert set_suggestion is not None
    
    @pytest.mark.asyncio
    async def test_security_issue_detection(self):
        """Test detection of security issues"""
        code = '''
import os
user_input = input("Enter command: ")
os.system(user_input)
'''
        error_message = "SecurityWarning: Potential command injection vulnerability"
        error_line = 3
        
        inspector = CodeInspector()
        result = await inspector.analyze_error(
            code=code,
            error_message=error_message,
            error_line=error_line,
            inspection_level=InspectionLevel.SECURITY
        )
        
        assert result.success is True
        assert len(result.suggestions) > 0
        assert result.severity == "high"
        
        # Should suggest using subprocess with proper escaping
        secure_suggestion = next(
            (s for s in result.suggestions if "subprocess" in s.fix_code),
            None
        )
        assert secure_suggestion is not None
    
    @pytest.mark.asyncio
    async def test_code_smell_detection(self):
        """Test detection of code smells"""
        code = '''
def calculate_price(item):
    if item.type == "book":
        return item.price * 0.9
    elif item.type == "electronics":
        return item.price * 0.85
    elif item.type == "clothing":
        return item.price * 0.8
    else:
        return item.price
'''
        error_message = "CodeSmell: Long if-elif chain detected"
        error_line = 2
        
        inspector = CodeInspector()
        result = await inspector.analyze_error(
            code=code,
            error_message=error_message,
            error_line=error_line,
            inspection_level=InspectionLevel.STYLE
        )
        
        assert result.success is True
        assert len(result.suggestions) > 0
        
        # Should suggest using dictionary mapping or strategy pattern
        pattern_suggestion = next(
            (s for s in result.suggestions if "dict" in s.fix_code.lower() or "strategy" in s.description.lower()),
            None
        )
        assert pattern_suggestion is not None
    
    @pytest.mark.asyncio
    async def test_analyze_with_stack_trace(self):
        """Test analysis with full stack trace"""
        code = '''
def recursive_function(n):
    if n <= 0:
        return 1
    return n * recursive_function(n)
    
result = recursive_function(5)
'''
        error_message = "RecursionError: maximum recursion depth exceeded"
        stack_trace = '''
Traceback (most recent call last):
  File "example.py", line 7, in <module>
    result = recursive_function(5)
  File "example.py", line 5, in recursive_function
    return n * recursive_function(n)
  File "example.py", line 5, in recursive_function
    return n * recursive_function(n)
  [Previous line repeated 996 more times]
RecursionError: maximum recursion depth exceeded
'''
        
        inspector = CodeInspector()
        result = await inspector.analyze_error(
            code=code,
            error_message=error_message,
            error_line=5,
            stack_trace=stack_trace
        )
        
        assert result.success is True
        assert "recursion" in result.primary_cause.lower()
        assert len(result.suggestions) > 0
        
        # Should identify the bug in recursive call
        fix_suggestion = next(
            (s for s in result.suggestions if "n - 1" in s.fix_code or "n-1" in s.fix_code),
            None
        )
        assert fix_suggestion is not None
    
    @pytest.mark.asyncio
    async def test_analyze_ml_error(self):
        """Test analysis of machine learning library errors"""
        code = '''
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
'''
        error_message = "ValueError: This solver needs samples of at least 2 classes in the data"
        error_line = 3
        
        inspector = CodeInspector()
        result = await inspector.analyze_error(
            code=code,
            error_message=error_message,
            error_line=error_line,
            context={"ml_framework": "sklearn"}
        )
        
        assert result.success is True
        assert len(result.suggestions) > 0
        
        # Should suggest checking class distribution
        class_check = next(
            (s for s in result.suggestions if "unique" in s.fix_code or "value_counts" in s.fix_code),
            None
        )
        assert class_check is not None
    
    @pytest.mark.asyncio
    async def test_batch_error_analysis(self):
        """Test analyzing multiple related errors"""
        errors = [
            {
                "code": "import pandas",
                "error_message": "ModuleNotFoundError: No module named 'pandas'",
                "line": 1
            },
            {
                "code": "df = pandas.DataFrame()",
                "error_message": "NameError: name 'pandas' is not defined",
                "line": 2
            }
        ]
        
        inspector = CodeInspector()
        results = await inspector.analyze_batch_errors(errors)
        
        assert len(results) == 2
        assert all(r.success for r in results)
        
        # Should identify root cause as missing pandas installation
        root_cause = inspector.identify_root_cause(results)
        assert "pandas" in root_cause.lower()
        assert "install" in root_cause.lower()
    
    @pytest.mark.asyncio
    async def test_invalid_input_handling(self):
        """Test handling of invalid inputs"""
        inspector = CodeInspector()
        
        # Test with None code
        result = await inspector.analyze_error(
            code=None,
            error_message="Some error",
            error_line=1
        )
        assert result.success is False
        assert "Invalid input" in result.error_message
        
        # Test with invalid line number
        result = await inspector.analyze_error(
            code="print('hello')",
            error_message="Some error",
            error_line=-1
        )
        assert result.success is False
        assert "Invalid line number" in result.error_message
    
    @pytest.mark.asyncio
    async def test_timeout_handling(self):
        """Test handling of analysis timeout"""
        inspector = CodeInspector(timeout=0.001)  # Very short timeout
        
        # Create complex code that takes time to analyze
        complex_code = '\n'.join([f"var_{i} = {i} * {i+1}" for i in range(1000)])
        
        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            mock_sleep.side_effect = asyncio.TimeoutError()
            
            result = await inspector.analyze_error(
                code=complex_code,
                error_message="Some error",
                error_line=500
            )
            
            assert result.success is False
            assert "timeout" in result.error_message.lower()
    
    @pytest.mark.asyncio  
    async def test_caching_mechanism(self):
        """Test caching of error analysis results"""
        inspector = CodeInspector(enable_cache=True)
        
        code = "print(undefined_var)"
        error_message = "NameError: name 'undefined_var' is not defined"
        
        # First call - should analyze
        result1 = await inspector.analyze_error(
            code=code,
            error_message=error_message,
            error_line=1
        )
        
        # Second call - should use cache
        result2 = await inspector.analyze_error(
            code=code,
            error_message=error_message,
            error_line=1
        )
        
        assert result1.cache_hit is False
        assert result2.cache_hit is True
        assert result1.suggestions == result2.suggestions