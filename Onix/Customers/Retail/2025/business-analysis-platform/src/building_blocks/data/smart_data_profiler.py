"""Smart Data Profiler Building Block

This module provides intelligent data profiling capabilities with learning integration.
It analyzes data to provide statistical summaries, detect patterns, and learn from
previous profiling runs.
"""
import logging
import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, date
import numpy as np
import pandas as pd
from difflib import SequenceMatcher

from src.building_blocks.base import BuildingBlock
from src.utils.learning_history import LearningHistoryManager
from src.utils.logger import get_logger

logger = get_logger(__name__)


class SmartDataProfiler(BuildingBlock):
    """Smart data profiler with learning capabilities
    
    This building block analyzes dataframes to provide:
    - Statistical summaries for different data types
    - Pattern detection (emails, phones, IDs, etc.)
    - Correlation analysis
    - Outlier detection
    - Data quality scoring
    - Missing value pattern analysis
    - Learning from previous profiling runs
    """
    
    def __init__(self, learning_history: Optional[LearningHistoryManager] = None):
        """Initialize the profiler
        
        Args:
            learning_history: Optional learning history manager for pattern learning
        """
        self.learning_history = learning_history
        logger.info("SmartDataProfiler initialized")
    
    @property
    def name(self) -> str:
        """Get the name of the building block"""
        return "smart_data_profiler"
    
    @property
    def category(self) -> str:
        """Get the category of the building block"""
        return "data"
    
    async def execute(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute data profiling
        
        Args:
            data: Input data containing 'dataframe' key
            config: Configuration for profiling
            
        Returns:
            Dict with profiling results
        """
        try:
            # Validate input
            errors = self.validate_input(data)
            if errors:
                return {
                    'success': False,
                    'data': None,
                    'errors': errors
                }
            
            # Validate configuration
            config_errors = self._validate_config(config)
            if config_errors:
                return {
                    'success': False,
                    'data': None,
                    'errors': config_errors
                }
            
            df = data['dataframe']
            enable_learning = config.get('enable_learning', True)
            sample_size = config.get('sample_size', 100000)
            pattern_threshold = config.get('pattern_threshold', 0.8)
            
            # Sample if dataset is too large
            sampled = False
            original_size = len(df)
            if len(df) > sample_size:
                df = self._sample_dataframe(df, sample_size)
                sampled = True
                logger.info(f"Sampled {sample_size} rows from {original_size}")
            
            # Get learned patterns if learning is enabled
            learned_patterns = {}
            if enable_learning and self.learning_history:
                try:
                    learned_patterns = self.learning_history.get_learned_patterns()
                except AttributeError:
                    learned_patterns = {}
            
            # Profile each column
            profile = {}
            patterns = {}
            
            for column in df.columns:
                col_profile = self._profile_column(df[column], column, pattern_threshold)
                profile[column] = col_profile
                
                # Detect patterns
                col_patterns = self._detect_patterns(df[column], column, pattern_threshold)
                patterns[column] = col_patterns
                
                # Apply learning
                if enable_learning and self.learning_history:
                    suggested_type = self.learning_history.suggest_column_type(column)
                    if suggested_type:
                        col_profile['suggested_type'] = suggested_type
                    
                    # Learn from this profiling (method name matches test expectations)
                    if col_patterns.get('is_id'):
                        self.learning_history.record_pattern({'column': column, 'type': 'id', 'confidence': 0.9})
                    elif col_patterns.get('is_email'):
                        self.learning_history.record_pattern({'column': column, 'type': 'email', 'confidence': 0.95})
                    elif col_patterns.get('is_phone'):
                        self.learning_history.record_pattern({'column': column, 'type': 'phone', 'confidence': 0.9})
                    elif col_patterns.get('is_categorical'):
                        self.learning_history.record_pattern({'column': column, 'type': 'categorical', 'confidence': 0.85})
            
            # Calculate correlations
            correlations = self._calculate_correlations(df)
            
            # Detect missing value patterns
            missing_patterns = self._analyze_missing_patterns(df)
            
            # Calculate quality score
            quality_score = self._calculate_quality_score(profile, correlations, missing_patterns)
            
            result = {
                'success': True,
                'data': {
                    'profile': profile,
                    'patterns': patterns,
                    'correlations': correlations,
                    'missing_patterns': missing_patterns,
                    'quality_score': quality_score,
                    'metadata': {
                        'sampled': sampled,
                        'sample_size': len(df),
                        'original_size': original_size,
                        'profiled_at': datetime.now().isoformat()
                    }
                },
                'errors': []
            }
            
            logger.info(f"Profiling completed successfully. Quality score: {quality_score}")
            return result
            
        except Exception as e:
            logger.error(f"Error in SmartDataProfiler: {str(e)}")
            return {
                'success': False,
                'data': None,
                'errors': [str(e)]
            }
    
    def validate_input(self, data: Dict[str, Any]) -> List[str]:
        """Validate input data
        
        Args:
            data: Input data to validate
            
        Returns:
            List of validation errors
        """
        errors = []
        
        if 'dataframe' not in data:
            errors.append("Missing required field: 'dataframe'")
            return errors
        
        if not isinstance(data['dataframe'], pd.DataFrame):
            errors.append("'dataframe' must be a pandas DataFrame")
            return errors
        
        if data['dataframe'].empty:
            errors.append("'dataframe' cannot be empty")
            return errors
        
        return errors
    
    def get_config_schema(self) -> Dict[str, Any]:
        """Get configuration schema
        
        Returns:
            JSON schema for configuration
        """
        return {
            'type': 'object',
            'properties': {
                'enable_learning': {
                    'type': 'boolean',
                    'default': True,
                    'description': 'Enable learning from profiling results'
                },
                'sample_size': {
                    'type': 'integer',
                    'default': 100000,
                    'minimum': 1000,
                    'description': 'Maximum rows to process (sampling threshold)'
                },
                'pattern_threshold': {
                    'type': 'number',
                    'default': 0.8,
                    'minimum': 0,
                    'maximum': 1,
                    'description': 'Minimum confidence for pattern detection'
                }
            }
        }
    
    def _validate_config(self, config: Dict[str, Any]) -> List[str]:
        """Validate configuration values
        
        Args:
            config: Configuration to validate
            
        Returns:
            List of validation errors
        """
        errors = []
        
        sample_size = config.get('sample_size', 100000)
        if sample_size < 0:
            errors.append("Invalid sample_size: must be positive")
        
        pattern_threshold = config.get('pattern_threshold', 0.8)
        if not 0 <= pattern_threshold <= 1:
            errors.append("Invalid pattern_threshold: must be between 0 and 1")
        
        return errors
    
    def _sample_dataframe(self, df: pd.DataFrame, sample_size: int) -> pd.DataFrame:
        """Sample dataframe if it's too large
        
        Args:
            df: DataFrame to sample
            sample_size: Number of rows to sample
            
        Returns:
            Sampled DataFrame
        """
        if len(df) > sample_size:
            return df.sample(n=sample_size, random_state=42)
        return df
    
    def _profile_column(self, series: pd.Series, column_name: str, 
                       pattern_threshold: float) -> Dict[str, Any]:
        """Profile a single column
        
        Args:
            series: Column data
            column_name: Name of the column
            pattern_threshold: Threshold for pattern detection
            
        Returns:
            Column profile dictionary
        """
        profile = {
            'count': len(series),
            'null_count': series.isnull().sum(),
            'null_percentage': (series.isnull().sum() / len(series)) * 100
        }
        
        # Drop nulls for further analysis
        non_null = series.dropna()
        
        if len(non_null) == 0:
            profile['dtype'] = 'all_null'
            return profile
        
        # Determine data type
        dtype = self._determine_dtype(non_null)
        profile['dtype'] = dtype
        
        if dtype == 'numeric':
            profile.update(self._profile_numeric(non_null))
        elif dtype == 'string':
            profile.update(self._profile_string(non_null))
        elif dtype == 'datetime':
            profile.update(self._profile_datetime(non_null))
        elif dtype == 'boolean':
            profile.update(self._profile_boolean(non_null))
        elif dtype == 'mixed':
            profile.update(self._profile_mixed(non_null))
        else:
            profile.update(self._profile_object(non_null))
        
        return profile
    
    def _determine_dtype(self, series: pd.Series) -> str:
        """Determine the primary data type of a series
        
        Args:
            series: Non-null series data
            
        Returns:
            Data type string
        """
        # Handle empty series
        if len(series) == 0:
            return 'text'
            
        # Check if already datetime
        if pd.api.types.is_datetime64_any_dtype(series):
            return 'datetime'
            
        # Check for boolean first - handle properly to avoid subtraction issues
        try:
            unique_vals = series.unique()
            if series.dtype == bool:
                return 'boolean'
            # Only check for boolean-like values if we have exactly 2 unique values
            # and they're actually True/False (not just 0/1 which could be numeric)
            if (len(unique_vals) == 2 and 
                set(unique_vals).issubset({True, False, 'True', 'False', 'true', 'false'})):
                return 'boolean'
        except TypeError:
            # Unhashable types (dicts, lists) in the series
            pass
        
        # Check for numeric first (integers and floats are numeric)
        if pd.api.types.is_numeric_dtype(series):
            return 'numeric'
        
        # Check if all values are strings first (before numeric conversion)
        if all(isinstance(x, str) for x in series.head(100)):  # Sample for performance
            # Then check for numeric strings
            try:
                numeric_series = pd.to_numeric(series, errors='coerce')
                valid_numeric = numeric_series.notna().sum()
                # Only consider as numeric if ALL can be converted or mostly numeric
                if valid_numeric / len(series) > 0.9:  # Increased threshold
                    return 'numeric'
                elif valid_numeric > 0:
                    # Some numeric, some not = mixed
                    return 'mixed'
                else:
                    return 'string'
            except:
                return 'string'
        
        # Check for mixed types first - if we have multiple different types, it's mixed
        types = set(type(x) for x in series if x is not None)  # Exclude None
        if len(types) > 1:
            # Special case: datetime-like objects can include several types
            datetime_types = {str, datetime, pd.Timestamp, date}
            if types.issubset(datetime_types):
                # Check if they can all be converted to datetime
                try:
                    parsed = pd.to_datetime(series, errors='coerce', format='mixed')
                    valid_dates = parsed.notna().sum() 
                    # More strict: need very high ratio for datetime when mixed types
                    if valid_dates == len(series):  # All must be valid dates
                        return 'datetime'
                    else:
                        return 'mixed'
                except:
                    return 'mixed'
            else:
                # Check if types include complex objects like dict, list
                complex_types = {dict, list, tuple, set}
                if any(t in types for t in complex_types):
                    return 'object'  # Objects that are containers
                else:
                    return 'mixed'  # Mixed primitive types
        
        # Check for datetime strings
        try:
            parsed = pd.to_datetime(series, errors='coerce', format='mixed')
            valid_dates = parsed.notna().sum()
            if valid_dates > 0 and valid_dates / len(series) > 0.7:
                return 'datetime'
        except:
            pass
            
        # Check if all values are strings
        if all(isinstance(x, str) for x in series.head(100)):  # Sample for performance
            return 'string'
        
        return 'object'
    
    def _profile_numeric(self, series: pd.Series) -> Dict[str, Any]:
        """Profile numeric column
        
        Args:
            series: Numeric series
            
        Returns:
            Numeric profile dict
        """
        numeric_series = pd.to_numeric(series, errors='coerce').dropna()
        
        # Handle single value case
        std_dev = numeric_series.std()
        if pd.isna(std_dev) or len(numeric_series) == 1:
            std_dev = 0.0
            
        profile = {
            'mean': float(numeric_series.mean()),
            'median': float(numeric_series.median()),
            'std_dev': float(std_dev),
            'min': float(numeric_series.min()),
            'max': float(numeric_series.max()),
            'q1': float(numeric_series.quantile(0.25)),
            'q3': float(numeric_series.quantile(0.75))
        }
        
        # Detect outliers using IQR method with less sensitivity
        iqr = profile['q3'] - profile['q1']
        lower_bound = profile['q1'] - 2.0 * iqr  # Increased from 1.5 for less sensitivity
        upper_bound = profile['q3'] + 2.0 * iqr  # Increased from 1.5 for less sensitivity
        
        outliers_mask = (numeric_series < lower_bound) | (numeric_series > upper_bound)
        outliers = numeric_series[outliers_mask]
        
        profile['outliers'] = {
            'count': len(outliers),
            'values': outliers.tolist() if len(outliers) < 100 else outliers.head(100).tolist(),
            'indices': outliers.index.tolist() if len(outliers) < 100 else outliers.index[:100].tolist()
        }
        
        return profile
    
    def _profile_string(self, series: pd.Series) -> Dict[str, Any]:
        """Profile string column
        
        Args:
            series: String series
            
        Returns:
            String profile dict
        """
        try:
            unique_count = series.nunique()
            unique_percentage = (unique_count / len(series)) * 100
        except TypeError:
            unique_count = None
            unique_percentage = None
            
        profile = {
            'unique_count': unique_count,
            'unique_percentage': unique_percentage,
        }
        
        # Get value counts - only if we can compute it
        try:
            value_counts = series.value_counts()
            profile['most_common_values'] = value_counts.head(10).to_dict()
            
            # Check if potential ID (all unique)
            if unique_count and unique_count == len(series):
                profile['is_potential_id'] = True
            else:
                profile['is_potential_id'] = False
        except TypeError:
            profile['most_common_values'] = {}
            profile['is_potential_id'] = False
        
        # Average string length - only for actual strings
        try:
            profile['avg_length'] = series.str.len().mean()
            profile['min_length'] = series.str.len().min()
            profile['max_length'] = series.str.len().max()
        except AttributeError:
            profile['avg_length'] = None
            profile['min_length'] = None
            profile['max_length'] = None
        
        return profile
    
    def _profile_datetime(self, series: pd.Series) -> Dict[str, Any]:
        """Profile datetime column
        
        Args:
            series: Datetime series
            
        Returns:
            Datetime profile dict
        """
        # Convert to datetime with format mixed to avoid warnings
        dt_series = pd.to_datetime(series, errors='coerce', format='mixed').dropna()
        
        if len(dt_series) == 0:
            return {}
        
        profile = {
            'date_range': {
                'min': dt_series.min().isoformat(),
                'max': dt_series.max().isoformat()
            },
            'frequency': self._detect_date_frequency(dt_series)
        }
        
        return profile
    
    def _detect_date_frequency(self, series: pd.Series) -> str:
        """Detect frequency of datetime series
        
        Args:
            series: Datetime series
            
        Returns:
            Frequency string
        """
        if len(series) < 2:
            return 'insufficient_data'
        
        # Sort and calculate differences
        sorted_series = series.sort_values()
        diffs = sorted_series.diff().dropna()
        
        if len(diffs) == 0:
            return 'unknown'
        
        # Most common difference
        most_common_diff = diffs.mode()[0]
        
        # Map to frequency
        if most_common_diff == pd.Timedelta(days=1):
            return 'daily'
        elif most_common_diff == pd.Timedelta(days=7):
            return 'weekly'
        elif 28 <= most_common_diff.days <= 31:
            return 'monthly'
        elif 365 <= most_common_diff.days <= 366:
            return 'yearly'
        else:
            return f'custom ({most_common_diff})'
    
    def _profile_boolean(self, series: pd.Series) -> Dict[str, Any]:
        """Profile boolean column
        
        Args:
            series: Boolean series
            
        Returns:
            Boolean profile dict
        """
        value_counts = series.value_counts()
        return {
            'true_count': value_counts.get(True, 0),
            'false_count': value_counts.get(False, 0),
            'true_percentage': (value_counts.get(True, 0) / len(series)) * 100
        }
    
    def _profile_mixed(self, series: pd.Series) -> Dict[str, Any]:
        """Profile mixed type column
        
        Args:
            series: Mixed type series
            
        Returns:
            Mixed type profile dict
        """
        type_counts = {}
        for value in series:
            type_name = type(value).__name__
            type_counts[type_name] = type_counts.get(type_name, 0) + 1
        
        try:
            unique_count = series.nunique()
        except TypeError:
            # Can't calculate nunique for unhashable types
            unique_count = None
            
        return {
            'type_distribution': type_counts,
            'unique_count': unique_count
        }
    
    def _profile_object(self, series: pd.Series) -> Dict[str, Any]:
        """Profile object column
        
        Args:
            series: Object series
            
        Returns:
            Object profile dict
        """
        try:
            unique_count = series.nunique()
        except TypeError:
            # Can't calculate nunique for unhashable types
            unique_count = None
            
        return {
            'unique_count': unique_count,
            'type': 'object'
        }
    
    def _detect_patterns(self, series: pd.Series, column_name: str, 
                        threshold: float) -> Dict[str, Any]:
        """Detect patterns in column data
        
        Args:
            series: Column data
            column_name: Name of the column
            threshold: Pattern detection threshold
            
        Returns:
            Pattern detection results
        """
        patterns = {}
        
        # Drop nulls for pattern detection
        non_null = series.dropna()
        
        if len(non_null) == 0:
            return patterns
        
        # Only check patterns for string columns
        if all(isinstance(x, str) for x in non_null.head(100)):
            # Email pattern
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            email_matches = non_null.str.match(email_pattern).sum()
            patterns['is_email'] = bool((email_matches / len(non_null)) >= threshold)
            
            # Phone pattern (various formats)
            phone_pattern = r'^[+\-\(\)\d\s]+$'
            phone_matches = non_null.str.match(phone_pattern).sum()
            patterns['is_phone'] = bool((phone_matches / len(non_null)) >= threshold)
            
            # Date string pattern - check if detected as datetime in profile
            if self._determine_dtype(series) == 'datetime':
                patterns['is_date'] = True  
            else:
                # Otherwise check patterns
                date_patterns = [
                    r'^\d{4}-\d{2}-\d{2}$',  # YYYY-MM-DD
                    r'^\d{2}/\d{2}/\d{4}$',  # MM/DD/YYYY
                    r'^\d{2}-\d{2}-\d{4}$',  # DD-MM-YYYY
                    r'^\d{4}/\d{2}/\d{2}$'   # YYYY/MM/DD (added for the test data)
                ]
                date_matches = 0
                for pattern in date_patterns:
                    date_matches += non_null.str.match(pattern).sum()
                patterns['is_date'] = bool((date_matches / len(non_null)) >= threshold)
            
            # ID pattern (all unique with consistent format)
            try:
                if series.nunique() == len(series):
                    patterns['is_id'] = True
                else:
                    patterns['is_id'] = False
            except TypeError:
                # Can't calculate nunique for unhashable types
                patterns['is_id'] = False
        
        # Categorical detection - consider both ratio and absolute count
        try:
            unique_count = series.nunique()
            unique_ratio = unique_count / len(series)
            # Categorical if: few unique values OR low ratio and reasonable count
            patterns['is_categorical'] = bool((unique_count <= 10) or (unique_ratio < 0.05 and unique_count < 50))
        except TypeError:
            # Can't calculate nunique for unhashable types
            patterns['is_categorical'] = False
        
        # Continuous detection (numeric with high cardinality)
        try:
            numeric_series = pd.to_numeric(series, errors='coerce')
            if numeric_series.notna().sum() > 0:
                numeric_unique_ratio = numeric_series.nunique() / len(numeric_series)
                patterns['is_continuous'] = bool(numeric_unique_ratio > 0.5)
            else:
                patterns['is_continuous'] = False
        except:
            patterns['is_continuous'] = False
        
        return patterns
    
    def _calculate_correlations(self, df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """Calculate correlations between numeric columns
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Correlation matrix as nested dict
        """
        # Get numeric columns only
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_columns) < 2:
            return {}
        
        # Calculate correlation matrix
        corr_matrix = df[numeric_columns].corr()
        
        # Convert to nested dict
        correlations = {}
        for col1 in numeric_columns:
            correlations[col1] = {}
            for col2 in numeric_columns:
                if col1 != col2:
                    correlations[col1][col2] = float(corr_matrix.loc[col1, col2])
        
        return correlations
    
    def _analyze_missing_patterns(self, df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """Analyze patterns in missing values
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Missing value pattern analysis
        """
        patterns = {}
        
        for column in df.columns:
            null_mask = df[column].isnull()
            null_count = null_mask.sum()
            
            if null_count == 0:
                patterns[column] = {
                    'pattern': 'none',
                    'count': 0,
                    'percentage': 0
                }
            elif null_count == len(df):
                patterns[column] = {
                    'pattern': 'all_missing',
                    'count': null_count,
                    'percentage': 100
                }
            else:
                # Analyze pattern
                pattern = self._detect_missing_pattern(null_mask)
                patterns[column] = {
                    'pattern': pattern,
                    'count': null_count,
                    'percentage': (null_count / len(df)) * 100
                }
        
        return patterns
    
    def _detect_missing_pattern(self, null_mask: pd.Series) -> str:
        """Detect pattern in missing values
        
        Args:
            null_mask: Boolean series indicating null values
            
        Returns:
            Pattern name
        """
        # Check for block pattern (consecutive nulls)
        null_indices = null_mask[null_mask].index.tolist()
        
        if not null_indices:
            return 'none'
        
        # Check if nulls are at the beginning or end
        if null_indices == list(range(len(null_indices))):
            return 'block'
        
        # Check for systematic pattern (regular intervals)
        if len(null_indices) > 1:
            diffs = [null_indices[i+1] - null_indices[i] for i in range(len(null_indices)-1)]
            if len(set(diffs)) == 1:  # All differences are the same
                return 'systematic'
        
        # Otherwise, consider it random
        return 'random'
    
    def _calculate_quality_score(self, profile: Dict[str, Any], 
                               correlations: Dict[str, Dict[str, float]],
                               missing_patterns: Dict[str, Dict[str, Any]]) -> float:
        """Calculate overall data quality score
        
        Args:
            profile: Column profiles
            correlations: Correlation data
            missing_patterns: Missing value patterns
            
        Returns:
            Quality score (0-100)
        """
        scores = []
        
        # Completeness score (based on null percentage)
        for col_name, col_profile in profile.items():
            null_percentage = col_profile.get('null_percentage', 0)
            completeness_score = 100 - null_percentage
            scores.append(completeness_score)
        
        # Outlier score (for numeric columns)
        for col_name, col_profile in profile.items():
            if col_profile.get('dtype') == 'numeric' and 'outliers' in col_profile:
                outlier_count = col_profile['outliers']['count']
                total_count = col_profile['count']
                outlier_percentage = (outlier_count / total_count) * 100
                outlier_score = 100 - min(outlier_percentage * 10, 100)  # 10x penalty for outliers (increased)
                scores.append(outlier_score)
        
        # Pattern score (penalize random missing patterns)
        for col_name, pattern_info in missing_patterns.items():
            if pattern_info['pattern'] == 'random':
                pattern_score = 100 - pattern_info['percentage'] * 1.5  # Increased penalty
            elif pattern_info['pattern'] == 'systematic':
                pattern_score = 100 - (pattern_info['percentage'] * 0.7)  # Increased penalty
            else:
                pattern_score = 100
            scores.append(pattern_score)
        
        # Calculate average score
        return sum(scores) / len(scores) if scores else 100.0