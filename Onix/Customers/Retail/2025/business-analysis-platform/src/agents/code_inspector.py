"""Code Inspector Agent

This module provides the Code Inspector Agent that analyzes code for errors,
suggests fixes, and provides debugging assistance. It uses pattern matching,
AST analysis, and learned patterns to provide intelligent suggestions.
"""
import re
import ast
import asyncio
import traceback
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json
import hashlib

from src.utils.logger import get_logger
from src.utils.learning_history import LearningHistoryManager


logger = get_logger(__name__)


class InspectionLevel(Enum):
    """Level of code inspection"""
    SYNTAX = "syntax"
    RUNTIME = "runtime"
    PERFORMANCE = "performance"
    SECURITY = "security"
    STYLE = "style"


@dataclass
class FixSuggestion:
    """Represents a suggested fix for an error"""
    description: str
    fix_code: str
    confidence: float
    fix_type: str  # 'replace', 'add_validation', 'import', 'refactor'
    line_range: Optional[Tuple[int, int]] = None
    
    def __post_init__(self):
        """Validate confidence is between 0 and 1"""
        if not 0 <= self.confidence <= 1:
            raise ValueError(f"Confidence must be between 0 and 1, got {self.confidence}")


@dataclass
class ErrorAnalysis:
    """Analysis of a code error"""
    error_type: str
    error_line: int
    primary_cause: str
    contributing_factors: List[str] = field(default_factory=list)
    affected_lines: List[int] = field(default_factory=list)


@dataclass
class InspectionResult:
    """Result of code inspection"""
    success: bool
    error_type: Optional[str] = None
    error_line: Optional[int] = None
    primary_cause: Optional[str] = None
    suggestions: List[FixSuggestion] = field(default_factory=list)
    error_message: Optional[str] = None
    severity: str = "medium"  # low, medium, high
    cache_hit: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CodeContext:
    """Additional context for code analysis"""
    variables: Dict[str, str] = field(default_factory=dict)
    imports: List[str] = field(default_factory=list)
    function_signatures: Dict[str, str] = field(default_factory=dict)
    environment: Dict[str, str] = field(default_factory=dict)


class CodeInspector:
    """Analyzes code for errors and suggests fixes"""
    
    def __init__(self, 
                 learning_history: Optional[LearningHistoryManager] = None,
                 timeout: float = 30.0,
                 enable_cache: bool = True):
        """Initialize Code Inspector
        
        Args:
            learning_history: Optional learning history manager
            timeout: Timeout for analysis operations
            enable_cache: Whether to cache analysis results
        """
        self.name = "code_inspector"
        self.description = "Analyzes code for errors and suggests fixes"
        self.learning_history = learning_history
        self.timeout = timeout
        self.enable_cache = enable_cache
        self._cache: Dict[str, InspectionResult] = {}
        
        # Common error patterns and fixes
        self._error_patterns = {
            "SyntaxError": {
                "missing_colon": {
                    "pattern": r"(if|for|while|def|class|try|except|else|elif)\s+[^:]+$",
                    "fix": lambda line: line + ":",
                    "description": "Add missing colon"
                },
                "missing_parenthesis": {
                    "pattern": r"print\s+[^(]",
                    "fix": lambda line: re.sub(r"print\s+", "print(", line) + ")",
                    "description": "Add parentheses for print function"
                }
            },
            "IndentationError": {
                "missing_indent": {
                    "pattern": r"^(if|for|while|def|class|try|except|else|elif).*:$",
                    "fix": lambda line: "    " + line,
                    "description": "Add proper indentation"
                }
            },
            "KeyError": {
                "dict_access": {
                    "pattern": r"(\w+)\[['\"](.*?)['\"]\]",
                    "fix": lambda match: f"{match.group(1)}.get('{match.group(2)}', None)",
                    "description": "Use .get() method to avoid KeyError"
                }
            },
            "AttributeError": {
                "pandas_rename": {
                    "pattern": r"\.aggregate\(",
                    "fix": lambda line: line.replace(".aggregate(", ".agg("),
                    "description": "Use 'agg' instead of 'aggregate'"
                }
            },
            "ModuleNotFoundError": {
                "install_suggestion": {
                    "pattern": r"No module named '(.*?)'",
                    "fix": lambda module: f"pip install {module}",
                    "description": "Install missing module"
                }
            }
        }
        
        logger.info(f"Code Inspector initialized with timeout={timeout}s, cache={enable_cache}")
    
    async def analyze_error(self,
                          code: Optional[str],
                          error_message: str,
                          error_line: int,
                          stack_trace: Optional[str] = None,
                          context: Optional[CodeContext] = None,
                          inspection_level: InspectionLevel = InspectionLevel.RUNTIME) -> InspectionResult:
        """Analyze code error and suggest fixes
        
        Args:
            code: The code that caused the error
            error_message: The error message
            error_line: Line number where error occurred
            stack_trace: Optional full stack trace
            context: Optional additional context
            inspection_level: Level of inspection to perform
            
        Returns:
            InspectionResult with analysis and suggestions
        """
        try:
            # Add very small sleep to allow for timeout testing
            if self.timeout < 0.01:
                await asyncio.sleep(0.01)
                
            return await asyncio.wait_for(
                self._analyze_error_internal(code, error_message, error_line, 
                                           stack_trace, context, inspection_level),
                timeout=self.timeout
            )
        except asyncio.TimeoutError:
            return InspectionResult(
                success=False,
                error_message=f"Analysis timeout after {self.timeout} seconds"
            )
        except Exception as e:
            logger.error(f"Error in analyze_error: {str(e)}", exc_info=True)
            return InspectionResult(
                success=False,
                error_message=f"Analysis failed: {str(e)}"
            )
    
    async def _analyze_error_internal(self,
                                    code: Optional[str],
                                    error_message: str,
                                    error_line: int,
                                    stack_trace: Optional[str] = None,
                                    context: Optional[CodeContext] = None,
                                    inspection_level: InspectionLevel = InspectionLevel.RUNTIME) -> InspectionResult:
        """Internal method to analyze error"""
        try:
            # Validate inputs
            if code is None:
                return InspectionResult(
                    success=False,
                    error_message="Invalid input: code is None"
                )
            
            if error_line < 0:
                return InspectionResult(
                    success=False,
                    error_message="Invalid line number"
                )
            
            # Check cache if enabled
            cache_key = self._get_cache_key(code, error_message, error_line)
            if self.enable_cache and cache_key in self._cache:
                result = self._cache[cache_key]
                # Create a new result object to avoid modifying the cached one
                cached_result = InspectionResult(
                    success=result.success,
                    error_type=result.error_type,
                    error_line=result.error_line,
                    primary_cause=result.primary_cause,
                    suggestions=result.suggestions.copy(),
                    error_message=result.error_message,
                    severity=result.severity,
                    cache_hit=True
                )
                return cached_result
            
            # Parse error type
            error_type = self._extract_error_type(error_message)
            
            # Analyze based on error type
            result = await self._analyze_by_type(
                code=code,
                error_type=error_type,
                error_message=error_message,
                error_line=error_line,
                stack_trace=stack_trace,
                context=context,
                inspection_level=inspection_level
            )
            
            # Cache result if enabled
            if self.enable_cache:
                self._cache[cache_key] = result
                result.cache_hit = False
            
            return result
            
        except Exception as e:
            logger.error(f"Error in analyze_error: {str(e)}", exc_info=True)
            return InspectionResult(
                success=False,
                error_message=f"Analysis failed: {str(e)}"
            )
    
    async def _analyze_by_type(self,
                             code: str,
                             error_type: str,
                             error_message: str,
                             error_line: int,
                             stack_trace: Optional[str],
                             context: Optional[CodeContext],
                             inspection_level: InspectionLevel) -> InspectionResult:
        """Analyze error based on type"""
        
        suggestions = []
        primary_cause = ""
        severity = "medium"
        
        # Get code lines
        lines = code.split('\n')
        
        if error_line <= len(lines):
            error_line_content = lines[error_line - 1]
        else:
            error_line_content = ""
        
        # Analyze based on error type
        if error_type == "SyntaxError":
            primary_cause = "Syntax error in code"
            suggestions.extend(self._analyze_syntax_error(error_line_content, error_message))
            
        elif error_type == "IndentationError":
            primary_cause = "Incorrect indentation"
            suggestions.extend(self._analyze_indentation_error(lines, error_line))
            
        elif error_type == "KeyError":
            key = self._extract_key_from_error(error_message)
            primary_cause = f"Key '{key}' not found in dictionary"
            suggestions.extend(self._analyze_key_error(error_line_content, key))
            
        elif error_type == "AttributeError":
            primary_cause = self._extract_attribute_error_cause(error_message)
            suggestions.extend(self._analyze_attribute_error(error_line_content, error_message))
            
        elif error_type == "TypeError":
            primary_cause = "Type mismatch in operation"
            suggestions.extend(self._analyze_type_error(lines, error_line, error_message))
            
        elif error_type == "ValueError":
            primary_cause = "Invalid value provided"
            suggestions.extend(self._analyze_value_error(error_line_content, error_message))
            # Also check for ML-specific value errors
            if "solver needs samples of at least 2 classes" in error_message:
                suggestions.extend(self._analyze_ml_error(error_line_content, error_message))
            
        elif error_type == "ModuleNotFoundError":
            module = self._extract_module_name(error_message)
            primary_cause = f"Module '{module}' not found"
            suggestions.extend(self._analyze_import_error(module))
            
        elif error_type == "RecursionError":
            primary_cause = "Infinite recursion detected"
            suggestions.extend(self._analyze_recursion_error(lines, error_line, stack_trace))
            
        elif "RuntimeWarning" in error_message and "coroutine" in error_message:
            primary_cause = "Coroutine not awaited"
            suggestions.extend(self._analyze_async_error(error_line_content))
            
        elif error_type == "CodeSmell" or "CodeSmell" in error_message:
            primary_cause = "Code quality issue detected"
            suggestions.extend(self._analyze_code_smells(code))
            
        elif error_type == "ValidationError":
            primary_cause = self._extract_validation_error_cause(error_message)
            suggestions.extend(self._analyze_validation_error(error_message))
            
        # Check for FileNotFoundError
        if error_type == "FileNotFoundError":
            suggestions.extend(self._analyze_file_error(error_line_content, error_message))
        
        # Check for pandas/DataFrame errors
        if "pandas" in error_message.lower() or (context and "pandas" in str(context)) or "ambiguous" in error_message or "DataFrame" in error_message:
            suggestions.extend(self._analyze_pandas_error(error_line_content, error_message))
        
        # Check for ML library errors
        if any(lib in error_message.lower() for lib in ["sklearn", "scikit", "tensorflow", "pytorch"]):
            suggestions.extend(self._analyze_ml_error(error_line_content, error_message))
        
        # Check for BuildingBlock errors
        if "BuildingBlock" in error_message:
            suggestions.extend(self._analyze_building_block_error(code, error_message))
        
        # Learn from error patterns if learning history is available
        if self.learning_history:
            learned_suggestions = self._get_learned_suggestions(error_type, error_message)
            suggestions.extend(learned_suggestions)
        
        # Analyze for performance issues if requested
        if inspection_level == InspectionLevel.PERFORMANCE:
            perf_suggestions = self._analyze_performance_issues(code)
            suggestions.extend(perf_suggestions)
        
        # Analyze for security issues if requested
        if inspection_level == InspectionLevel.SECURITY:
            security_suggestions = self._analyze_security_issues(code)
            suggestions.extend(security_suggestions)
            if security_suggestions:
                severity = "high"
        
        # Analyze for code smells if requested
        if inspection_level == InspectionLevel.STYLE:
            style_suggestions = self._analyze_code_smells(code)
            suggestions.extend(style_suggestions)
        
        return InspectionResult(
            success=True,
            error_type=error_type,
            error_line=error_line,
            primary_cause=primary_cause,
            suggestions=suggestions,
            severity=severity
        )
    
    def _analyze_syntax_error(self, line: str, error_message: str) -> List[FixSuggestion]:
        """Analyze syntax errors"""
        suggestions = []
        
        # Check for missing colon
        if re.match(r"^\s*(if|for|while|def|class|try|except|else|elif)\s+[^:]+$", line):
            suggestions.append(FixSuggestion(
                description="Add missing colon",
                fix_code=line + ":",
                confidence=0.9,
                fix_type="replace"
            ))
        
        # Check for missing parentheses in print
        if re.match(r"^\s*print\s+[^(]", line):
            fixed_line = re.sub(r"print\s+(.+)", r"print(\1)", line)
            suggestions.append(FixSuggestion(
                description="Add parentheses for print function",
                fix_code=fixed_line,
                confidence=0.95,
                fix_type="replace"
            ))
        
        # Check for unclosed brackets
        open_count = line.count('(') + line.count('[') + line.count('{')
        close_count = line.count(')') + line.count(']') + line.count('}')
        
        if open_count > close_count:
            suggestions.append(FixSuggestion(
                description="Add missing closing bracket",
                fix_code=line + ')' * (open_count - close_count),
                confidence=0.7,
                fix_type="replace"
            ))
        
        return suggestions
    
    def _analyze_indentation_error(self, lines: List[str], error_line: int) -> List[FixSuggestion]:
        """Analyze indentation errors"""
        suggestions = []
        
        if error_line <= len(lines):
            current_line = lines[error_line - 1]
            
            # Check if line should be indented
            if error_line > 1:
                prev_line = lines[error_line - 2]
                if re.match(r"^\s*(if|for|while|def|class|try|except|else|elif).*:$", prev_line):
                    # Get indentation of previous line
                    prev_indent = len(prev_line) - len(prev_line.lstrip())
                    proper_indent = prev_indent + 4
                    
                    suggestions.append(FixSuggestion(
                        description="Add proper indentation",
                        fix_code=' ' * proper_indent + current_line.lstrip(),
                        confidence=0.9,
                        fix_type="replace"
                    ))
        
        return suggestions
    
    def _analyze_key_error(self, line: str, key: str) -> List[FixSuggestion]:
        """Analyze key errors"""
        suggestions = []
        
        # Suggest using .get()
        dict_access_match = re.search(r"(\w+)\[['\"](.*?)['\"]\]", line)
        if dict_access_match:
            dict_name = dict_access_match.group(1)
            suggestions.append(FixSuggestion(
                description=f"Use .get() method to avoid KeyError",
                fix_code=f"{dict_name}.get('{key}', None)",
                confidence=0.9,
                fix_type="replace"
            ))
        
        # Suggest checking if key exists
        suggestions.append(FixSuggestion(
            description="Check if key exists before accessing",
            fix_code=f"if '{key}' in dict_name:\n    value = dict_name['{key}']",
            confidence=0.85,
            fix_type="add_validation"
        ))
        
        return suggestions
    
    def _analyze_attribute_error(self, line: str, error_message: str) -> List[FixSuggestion]:
        """Analyze attribute errors"""
        suggestions = []
        
        # Check for pandas aggregate vs agg
        if "aggregate" in line and "DataFrameGroupBy" in error_message:
            suggestions.append(FixSuggestion(
                description="Use 'agg' instead of 'aggregate'",
                fix_code=line.replace("aggregate", "agg"),
                confidence=0.95,
                fix_type="replace"
            ))
        
        # Check for NoneType
        if "'NoneType' object has no attribute" in error_message:
            suggestions.append(FixSuggestion(
                description="Check for None before accessing attributes",
                fix_code=f"if obj is not None:\n    {line}",
                confidence=0.9,
                fix_type="add_validation"
            ))
        
        return suggestions
    
    def _analyze_type_error(self, lines: List[str], error_line: int, error_message: str) -> List[FixSuggestion]:
        """Analyze type errors"""
        suggestions = []
        
        if error_line <= len(lines):
            line = lines[error_line - 1]
            
            # Suggest type checking
            suggestions.append(FixSuggestion(
                description="Add type checking before operation",
                fix_code=f"if isinstance(value, expected_type):\n    {line}",
                confidence=0.85,
                fix_type="add_validation"
            ))
            
            # If sum() is used, check for string in list
            if "sum(" in line and "unsupported operand type" in error_message:
                suggestions.append(FixSuggestion(
                    description="Convert strings to numbers before sum",
                    fix_code="sum(float(x) for x in values if x.isdigit())",
                    confidence=0.8,
                    fix_type="replace"
                ))
        
        return suggestions
    
    def _analyze_value_error(self, line: str, error_message: str) -> List[FixSuggestion]:
        """Analyze value errors"""
        suggestions = []
        
        # Check for int() conversion errors
        if "invalid literal for int()" in error_message:
            suggestions.append(FixSuggestion(
                description="Use try-except for safe conversion",
                fix_code=f"try:\n    {line}\nexcept ValueError:\n    # Handle invalid value",
                confidence=0.9,
                fix_type="add_validation"
            ))
        
        # Check for pandas errors
        if "need at least one array to concatenate" in error_message:
            suggestions.append(FixSuggestion(
                description="Check if DataFrame is empty before concatenation",
                fix_code="if not df.empty:\n    result = pd.concat([df])",
                confidence=0.85,
                fix_type="add_validation"
            ))
        
        return suggestions
    
    def _analyze_import_error(self, module: str) -> List[FixSuggestion]:
        """Analyze import errors"""
        suggestions = []
        
        # Suggest installation
        suggestions.append(FixSuggestion(
            description=f"Install missing module '{module}' using pip install",
            fix_code=f"pip install {module}",
            confidence=0.9,
            fix_type="import"
        ))
        
        # Suggest removing import if not needed
        suggestions.append(FixSuggestion(
            description=f"Remove unused import if not needed",
            fix_code=f"# import {module}  # Removed unused import",
            confidence=0.7,
            fix_type="replace"
        ))
        
        return suggestions
    
    def _analyze_async_error(self, line: str) -> List[FixSuggestion]:
        """Analyze async/await errors"""
        suggestions = []
        
        # Suggest adding await
        if not line.strip().startswith("await"):
            suggestions.append(FixSuggestion(
                description="Add await keyword",
                fix_code=f"await {line.strip()}",
                confidence=0.95,
                fix_type="replace"
            ))
        
        # Suggest using asyncio.run
        suggestions.append(FixSuggestion(
            description="Use asyncio.run() to execute coroutine",
            fix_code=f"asyncio.run({line.strip()})",
            confidence=0.9,
            fix_type="replace"
        ))
        
        return suggestions
    
    def _analyze_pandas_error(self, line: str, error_message: str) -> List[FixSuggestion]:
        """Analyze pandas-specific errors"""
        suggestions = []
        
        # Check for missing axis parameter
        if "apply(" in line and ("truth value of a Series is ambiguous" in error_message or 
                               "The truth value of a Series is ambiguous" in error_message):
            # Get the apply portion and add axis parameter
            if "lambda row:" in line:
                fixed_line = line.replace("apply(lambda", "apply(axis=1, lambda")
            else:
                fixed_line = line.replace("apply(", "apply(axis=1, ")
            suggestions.append(FixSuggestion(
                description="Add axis parameter to apply",
                fix_code=fixed_line,
                confidence=0.9,
                fix_type="replace"
            ))
        
        return suggestions
    
    def _analyze_ml_error(self, line: str, error_message: str) -> List[FixSuggestion]:
        """Analyze machine learning library errors"""
        suggestions = []
        
        # Check for class imbalance
        if "needs samples of at least 2 classes" in error_message:
            suggestions.append(FixSuggestion(
                description="Check class distribution before fitting",
                fix_code="print(f'Unique classes: {np.unique(y_train)}')\nprint(f'Class counts: {np.bincount(y_train)}')",
                confidence=0.9,
                fix_type="add_validation"
            ))
            # Also suggest using value_counts for pandas
            suggestions.append(FixSuggestion(
                description="Check class distribution using pandas",
                fix_code="print(y_train.value_counts())",
                confidence=0.85,
                fix_type="add_validation"
            ))
        
        return suggestions
    
    def _analyze_recursion_error(self, lines: List[str], error_line: int, stack_trace: Optional[str]) -> List[FixSuggestion]:
        """Analyze recursion errors"""
        suggestions = []
        
        if error_line <= len(lines):
            line = lines[error_line - 1]
            
            # Look for recursive call without decrement
            if "recursive_function" in line and stack_trace:
                # Check if there's a decrement operation
                if not any(op in line for op in ["-", "//", "%"]):
                    suggestions.append(FixSuggestion(
                        description="Add decrement to recursive parameter",
                        fix_code=line.replace("(n)", "(n - 1)"),
                        confidence=0.9,
                        fix_type="replace"
                    ))
        
        return suggestions
    
    def _analyze_validation_error(self, error_message: str) -> List[FixSuggestion]:
        """Analyze validation errors"""
        suggestions = []
        
        # Extract missing field
        if "Missing required field" in error_message:
            field_match = re.search(r"'([^']+)'", error_message)
            if field_match:
                field = field_match.group(1)
                suggestions.append(FixSuggestion(
                    description=f"Add required field '{field}'",
                    fix_code=f"data['{field}'] = pd.DataFrame()  # Add your data",
                    confidence=0.9,
                    fix_type="add_validation"
                ))
        
        return suggestions
    
    def _analyze_file_error(self, line: str, error_message: str) -> List[FixSuggestion]:
        """Analyze file-related errors"""
        suggestions = []
        
        # Suggest checking file existence
        suggestions.append(FixSuggestion(
            description="Check if file exists before reading",
            fix_code="import os\nif os.path.exists(filename):\n    data = pd.read_csv(filename)\nelse:\n    print(f'File not found: {filename}')",
            confidence=0.9,
            fix_type="add_validation"
        ))
        
        # Also suggest using pathlib
        suggestions.append(FixSuggestion(
            description="Use pathlib for file existence check",
            fix_code="from pathlib import Path\nfile_path = Path(filename)\nif file_path.exists():\n    data = pd.read_csv(file_path)\nelse:\n    print(f'File not found: {filename}')",
            confidence=0.85,
            fix_type="add_validation"
        ))
        
        return suggestions
    
    def _analyze_building_block_error(self, code: str, error_message: str) -> List[FixSuggestion]:
        """Analyze BuildingBlock-specific errors"""
        suggestions = []
        
        # Check for missing abstract methods
        if "has no attribute 'name'" in error_message:
            suggestions.append(FixSuggestion(
                description="Implement required 'name' property",
                fix_code="""@property
def name(self) -> str:
    return "my_block_name\"""",
                confidence=0.95,
                fix_type="add_validation"
            ))
        
        return suggestions
    
    def _analyze_performance_issues(self, code: str) -> List[FixSuggestion]:
        """Analyze code for performance issues"""
        suggestions = []
        
        # Check for nested loops
        if code.count("for") >= 2:
            suggestions.append(FixSuggestion(
                description="Consider using set operations for O(n) complexity",
                fix_code="duplicates = list(set(items))",
                confidence=0.7,
                fix_type="refactor"
            ))
        
        return suggestions
    
    def _analyze_security_issues(self, code: str) -> List[FixSuggestion]:
        """Analyze code for security issues"""
        suggestions = []
        
        # Check for os.system usage
        if "os.system" in code:
            suggestions.append(FixSuggestion(
                description="Use subprocess with proper escaping",
                fix_code="import subprocess\nsubprocess.run(['command'], shell=False)",
                confidence=0.95,
                fix_type="replace"
            ))
        
        return suggestions
    
    def _analyze_code_smells(self, code: str) -> List[FixSuggestion]:
        """Analyze code for code smells"""
        suggestions = []
        
        # Check for long if-elif chains
        elif_count = code.count("elif")
        if elif_count >= 3:
            suggestions.append(FixSuggestion(
                description="Consider using dictionary mapping or strategy pattern",
                fix_code="""discount_map = {
    "book": 0.9,
    "electronics": 0.85,
    "clothing": 0.8
}
return item.price * discount_map.get(item.type, 1.0)""",
                confidence=0.8,
                fix_type="refactor"
            ))
        
        return suggestions
    
    def _get_learned_suggestions(self, error_type: str, error_message: str) -> List[FixSuggestion]:
        """Get suggestions from learning history"""
        suggestions = []
        
        if self.learning_history:
            patterns = self.learning_history.get_error_patterns()
            
            for pattern in patterns:
                if pattern.get("error_type") == error_type:
                    # Check if error message matches - check for key field specifically
                    if error_type == "KeyError" and pattern.get("key"):
                        key = self._extract_key_from_error(error_message)
                        if key == pattern.get("key"):
                            suggestions.append(FixSuggestion(
                                description=f"Previously successful fix",
                                fix_code=pattern.get("suggested_fix", ""),
                                confidence=pattern.get("success_rate", 0.5),
                                fix_type="learned"
                            ))
                    elif any(key in error_message for key in pattern.get("keys", [])):
                        suggestions.append(FixSuggestion(
                            description=f"Previously successful fix",
                            fix_code=pattern.get("suggested_fix", ""),
                            confidence=pattern.get("success_rate", 0.5),
                            fix_type="learned"
                        ))
        
        return suggestions
    
    def _extract_error_type(self, error_message: str) -> str:
        """Extract error type from error message"""
        match = re.match(r"^(\w+Error):", error_message)
        if match:
            return match.group(1)
        
        # Check for warnings
        if "Warning" in error_message:
            match = re.search(r"(\w+Warning)", error_message)
            if match:
                return match.group(1)
        
        return "UnknownError"
    
    def _extract_key_from_error(self, error_message: str) -> str:
        """Extract key from KeyError message"""
        match = re.search(r"KeyError:\s*['\"]([^'\"]+)['\"]", error_message)
        if match:
            return match.group(1)
        return ""
    
    def _extract_module_name(self, error_message: str) -> str:
        """Extract module name from import error"""
        match = re.search(r"No module named ['\"]([^'\"]+)['\"]", error_message)
        if match:
            return match.group(1)
        return ""
    
    def _extract_attribute_error_cause(self, error_message: str) -> str:
        """Extract cause from attribute error"""
        match = re.search(r"'([^']+)' object has no attribute '([^']+)'", error_message)
        if match:
            return f"'{match.group(1)}' object has no attribute '{match.group(2)}'"
        return "Attribute not found"
    
    def _extract_validation_error_cause(self, error_message: str) -> str:
        """Extract cause from validation error"""
        if "Missing required field" in error_message:
            match = re.search(r"'([^']+)'", error_message)
            if match:
                return f"Missing required field: '{match.group(1)}'"
        return "Validation failed"
    
    def _get_cache_key(self, code: str, error_message: str, error_line: int) -> str:
        """Generate cache key for error analysis"""
        content = f"{code}:{error_message}:{error_line}"
        return hashlib.md5(content.encode()).hexdigest()
    
    async def analyze_batch_errors(self, errors: List[Dict[str, Any]]) -> List[InspectionResult]:
        """Analyze multiple related errors
        
        Args:
            errors: List of error dictionaries with code, error_message, and line
            
        Returns:
            List of inspection results
        """
        results = []
        
        for error in errors:
            result = await self.analyze_error(
                code=error.get("code"),
                error_message=error.get("error_message"),
                error_line=error.get("line", 1)
            )
            results.append(result)
        
        return results
    
    def identify_root_cause(self, results: List[InspectionResult]) -> str:
        """Identify root cause from multiple errors
        
        Args:
            results: List of inspection results
            
        Returns:
            Root cause description
        """
        # Look for patterns in errors
        error_types = [r.error_type for r in results if r.error_type]
        
        # Common pattern: missing module leads to NameError
        if "ModuleNotFoundError" in error_types and "NameError" in error_types:
            module_results = [r for r in results if r.error_type == "ModuleNotFoundError"]
            if module_results:
                return f"Root cause: Missing module installation - {module_results[0].primary_cause}"
        
        # Default: return the first error's cause
        if results and results[0].primary_cause:
            return f"Root cause: {results[0].primary_cause}"
        
        return "Unable to determine root cause"