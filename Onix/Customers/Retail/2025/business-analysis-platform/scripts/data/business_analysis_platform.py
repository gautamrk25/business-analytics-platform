import sys
import logging
import traceback
import io
import time
import datetime
import warnings
import json
import asyncio
import re
import argparse
from io import StringIO
from collections import deque
from typing import Dict, Any, List, Callable, Optional, Union, Type
from abc import ABC, abstractmethod
import uuid
from dataclasses import dataclass
import yaml
from difflib import get_close_matches

# Error handling for missing third-party packages
missing_packages = []
try:
    import pandas as pd
except ImportError:
    missing_packages.append('pandas')
try:
    import numpy as np
except ImportError:
    missing_packages.append('numpy')
try:
    import streamlit as st
except ImportError:
    missing_packages.append('streamlit')
try:
    import yaml
except ImportError:
    missing_packages.append('yaml')

if missing_packages:
    warnings.warn(f"Missing required packages: {', '.join(missing_packages)}. Please install them to use all features.")

# Set up logging configuration
def _get_logging_level_from_config() -> int:
    try:
        with open('config.yaml', 'r') as f:
            loaded = yaml.safe_load(f)
            if loaded and 'logging' in loaded and 'level' in loaded['logging']:
                return getattr(logging, loaded['logging']['level'].upper(), logging.INFO)
    except Exception:
        pass
    return logging.INFO

logging.basicConfig(
    level=_get_logging_level_from_config(),
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ===============================================================
# TEMPLATE SYSTEM
# ===============================================================

@dataclass
class AgentTemplate:
    """Template for creating specialized business analysis agents."""
    id: str
    name: str
    description: str
    department: str
    industry_tags: List[str]
    workflow_steps: List[Dict[str, Any]]
    required_columns: List[str]
    optional_columns: List[str]
    sample_question: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert template to dictionary for serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'department': self.department,
            'industry_tags': self.industry_tags,
            'workflow_steps': self.workflow_steps,
            'required_columns': self.required_columns,
            'optional_columns': self.optional_columns,
            'sample_question': self.sample_question
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentTemplate':
        """Create template from dictionary."""
        return cls(**data)
    
    def save_to_file(self, filepath: str):
        """Save template to YAML file."""
        with open(filepath, 'w') as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False)
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'AgentTemplate':
        """Load template from YAML file."""
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        return cls.from_dict(data)

class MarketingTemplateFactory:
    """Creates marketing-specific analysis templates."""
    
    @staticmethod
    def create_campaign_analyzer() -> AgentTemplate:
        """Template for analyzing marketing campaign performance."""
        return AgentTemplate(
            id="marketing_campaign_analyzer",
            name="Marketing Campaign Analyzer",
            description="Analyzes campaign performance, ROI, and customer acquisition metrics",
            department="marketing",
            industry_tags=["all"],
            workflow_steps=[
                {
                    'name': 'validate_campaign_data',
                    'type': 'data_validator',
                    'config': {
                        'validation_rules': {
                            'campaign_spend': {'allow_null': False, 'expected_type': 'numeric'},
                            'impressions': {'allow_null': False, 'expected_type': 'numeric'},
                            'clicks': {'allow_null': False, 'expected_type': 'numeric'},
                            'conversions': {'allow_null': False, 'expected_type': 'numeric'}
                        },
                        'auto_fix': True
                    }
                },
                {
                    'name': 'calculate_campaign_kpis',
                    'type': 'kpi_calculator',
                    'config': {
                        'kpi_definitions': {
                            'click_through_rate': {
                                'formula': 'sum({clicks}) / sum({impressions})',
                                'unit': '%',
                                'description': 'Percentage of impressions that resulted in clicks'
                            },
                            'conversion_rate': {
                                'formula': 'sum({conversions}) / sum({clicks})',
                                'unit': '%',
                                'description': 'Percentage of clicks that resulted in conversions'
                            },
                            'cost_per_click': {
                                'formula': 'sum({campaign_spend}) / sum({clicks})',
                                'unit': '$',
                                'description': 'Average cost per click'
                            },
                            'return_on_ad_spend': {
                                'formula': 'sum({revenue}) / sum({campaign_spend})',
                                'unit': 'ratio',
                                'description': 'Revenue generated per dollar spent'
                            }
                        }
                    }
                }
            ],
            required_columns=['campaign_spend', 'impressions', 'clicks', 'conversions'],
            optional_columns=['revenue', 'campaign_name', 'channel', 'date'],
            sample_question="How are our marketing campaigns performing? What's the ROI and conversion rate?"
        )

class AgentTemplateManager:
    """Manages agent templates with loading, saving, and discovery capabilities."""
    
    def __init__(self):
        self.templates: Dict[str, AgentTemplate] = {}
        self.load_default_templates()
        logger.info("AgentTemplateManager initialized")
    
    def load_default_templates(self):
        """Load all default templates from factories."""
        # Marketing templates
        self.register_template(MarketingTemplateFactory.create_campaign_analyzer())
        logger.info(f"Loaded {len(self.templates)} default templates")
    
    def register_template(self, template: AgentTemplate):
        """Register a template in the manager."""
        self.templates[template.id] = template
        logger.info(f"Registered template: {template.name}")
    
    def get_template(self, template_id: str) -> Optional[AgentTemplate]:
        """Get a template by ID."""
        return self.templates.get(template_id)
    
    def list_templates(self) -> List[AgentTemplate]:
        """List all available templates."""
        return list(self.templates.values())
    
    def get_templates_by_department(self, department: str) -> List[AgentTemplate]:
        """Get templates for a specific department."""
        return [t for t in self.templates.values() if t.department == department]
    
    def validate_template_compatibility(self, template: AgentTemplate, available_columns: List[str]) -> Dict[str, Any]:
        """Check if a template is compatible with available data columns."""
        missing_required = [col for col in template.required_columns if col not in available_columns]
        available_optional = [col for col in template.optional_columns if col in available_columns]
        
        compatibility_score = 1.0
        if missing_required:
            compatibility_score = (len(template.required_columns) - len(missing_required)) / len(template.required_columns)
        
        return {
            'compatible': len(missing_required) == 0,
            'compatibility_score': compatibility_score,
            'missing_required': missing_required,
            'available_optional': available_optional,
            'suggestions': self._suggest_column_mappings(missing_required, available_columns)
        }
    
    def _suggest_column_mappings(self, missing_columns: List[str], available_columns: List[str]) -> Dict[str, str]:
        """Suggest potential column mappings using fuzzy matching."""
        suggestions = {}
        
        for missing_col in missing_columns:
            # Simple fuzzy matching
            matches = get_close_matches(missing_col, available_columns, n=1, cutoff=0.6)
            if matches:
                suggestions[missing_col] = matches[0]
        
        return suggestions

class ConfigManager:
    """Manages application configuration loaded from a YAML file with sensible defaults and dot notation access."""
    
    DEFAULTS: Dict[str, Any] = {
        'analysis_config': {
            'max_attempts': 3,
            'timeout_seconds': 60,
            'enable_logging': True,
        },
        'data_sources': {
            'primary': 'data/main.csv',
            'backup': 'data/backup.csv',
        },
        'ui': {
            'theme': 'light',
            'show_tutorial': True,
        },
        'logging': {
            'level': 'INFO',
        },
    }

    def __init__(self, config_path: Optional[str] = None) -> None:
        """
        Initialize ConfigManager and load configuration from a YAML file if provided.
        Falls back to sensible defaults if file is missing or invalid.
        Args:
            config_path (Optional[str]): Path to the YAML configuration file.
        """
        self._config: Dict[str, Any] = self.DEFAULTS.copy()
        if config_path:
            try:
                with open(config_path, 'r') as f:
                    loaded = yaml.safe_load(f)
                    if loaded:
                        self._deep_update(self._config, loaded)
                logger.info(f"Loaded configuration from {config_path}.")
            except FileNotFoundError:
                logger.warning(f"Configuration file '{config_path}' not found. Using default settings.")
            except Exception as e:
                logger.error(f"Error loading configuration: {e}\n{traceback.format_exc()}")
                logger.warning("Using default settings due to configuration load error.")
        else:
            logger.info("No configuration file provided. Using default settings.")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieve a configuration value using dot notation (e.g., 'section.key').
        Args:
            key (str): Dot notation key string.
            default (Any): Value to return if key is not found.
        Returns:
            Any: The configuration value or the provided default.
        """
        parts = key.split('.')
        value = self._config
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                logger.debug(f"Config key '{key}' not found. Returning default: {default!r}")
                return default if default is not None else self._get_default_for_key(key)
        return value

    def _get_default_for_key(self, key: str) -> Any:
        """
        Retrieve the default value for a given dot notation key.
        Args:
            key (str): Dot notation key string.
        Returns:
            Any: The default value or None if not found.
        """
        parts = key.split('.')
        value = self.DEFAULTS
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return None
        return value

    @staticmethod
    def _deep_update(d: Dict[str, Any], u: Dict[str, Any]) -> None:
        """
        Recursively update dictionary d with values from u.
        Args:
            d (Dict[str, Any]): The dictionary to update.
            u (Dict[str, Any]): The dictionary with updates.
        """
        for k, v in u.items():
            if isinstance(v, dict) and isinstance(d.get(k), dict):
                ConfigManager._deep_update(d[k], v)
            else:
                d[k] = v

# ===============================================================
# LAMBDA-INSPIRED BUILDING BLOCK SYSTEM
# ===============================================================

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, List, Type, Optional
import uuid

class BuildingBlock(ABC):
    """Abstract base class for all building blocks in LAMBDA-style architecture."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.block_id = config.get('id', str(uuid.uuid4())[:8])
        self.name = config.get('name', self.__class__.__name__)
        logger.info(f"Building block initialized: {self.name} ({self.block_id})")
    
    @abstractmethod
    async def execute(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the building block with given data and context."""
        pass
    
    def validate_input(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate input data against block requirements."""
        required_fields = self.config.get('required_fields', [])
        validation_result = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        for field in required_fields:
            if field not in data:
                validation_result['errors'].append(f"Missing required field: {field}")
                validation_result['valid'] = False
        
        return validation_result

class BuildingBlockRegistry:
    """Registry for managing and discovering building blocks."""
    
    def __init__(self):
        self.blocks: Dict[str, Type[BuildingBlock]] = {}
        self.execution_history: List[Dict[str, Any]] = []
        logger.info("BuildingBlockRegistry initialized")
        _register_default_blocks(self)
    
    def register_block(self, name: str, block_class: Type[BuildingBlock]):
        """Register a building block class."""
        self.blocks[name] = block_class
        logger.info(f"Registered building block: {name}")
    
    def create_block(self, name: str, config: Dict[str, Any]) -> BuildingBlock:
        """Create and return a building block instance."""
        if name not in self.blocks:
            raise ValueError(f"Block '{name}' not found in registry")
        return self.blocks[name](config)
    
    def list_blocks(self) -> List[str]:
        """List all registered building block names."""
        return list(self.blocks.keys())
    
    def get_block_info(self, name: str) -> Dict[str, Any]:
        """Get information about a specific building block."""
        if name not in self.blocks:
            return {}
        block_class = self.blocks[name]
        return {
            'name': name,
            'class': block_class.__name__,
            'description': block_class.__doc__ or 'No description'
        }

# ===============================================================
# CONCRETE BUILDING BLOCKS WITH INDUSTRY INTELLIGENCE
# ===============================================================

class DataValidatorBlock(BuildingBlock):
    """Validates data quality with self-healing capabilities."""
    
    async def execute(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        validation_rules = self.config.get('validation_rules', {})
        auto_fix = self.config.get('auto_fix', True)
        
        results = {
            'success': True,
            'validation_score': 1.0,
            'fixes_applied': [],
            'data_updates': {},
            'summary': {}
        }
        
        fixed_data = data.copy() if auto_fix else None
        
        try:
            for column, rules in validation_rules.items():
                if column not in data:
                    results['success'] = False
                    continue
                
                column_data = data[column]
                
                # Auto-fix null values
                if not rules.get('allow_null', True):
                    null_count = sum(1 for x in column_data if x is None or x == '')
                    
                    if null_count > 0 and auto_fix and fixed_data:
                        fill_value = rules.get('default_value', 0)
                        fixed_data[column] = [fill_value if (x is None or x == '') else x for x in column_data]
                        results['fixes_applied'].append(f"Fixed {null_count} null values in {column}")
                
                # Auto-fix data types
                if 'expected_type' in rules:
                    expected = rules['expected_type']
                    if expected == 'numeric' and auto_fix and fixed_data:
                        numeric_data = []
                        for val in column_data:
                            try:
                                if isinstance(val, str):
                                    # Clean currency/percentage strings
                                    clean_val = val.replace('$', '').replace(',', '').replace('%', '')
                                    num_val = float(clean_val)
                                    if '%' in val:
                                        num_val = num_val / 100
                                    numeric_data.append(num_val)
                                else:
                                    numeric_data.append(float(val))
                            except (ValueError, TypeError):
                                numeric_data.append(0)
                        
                        fixed_data[column] = numeric_data
                        results['fixes_applied'].append(f"Converted {column} to numeric")
                
                results['summary'][column] = {
                    'total_records': len(column_data),
                    'valid_values': len([x for x in column_data if x is not None and x != ''])
                }
            
            if auto_fix and fixed_data and results['fixes_applied']:
                results['data_updates'] = fixed_data
                logger.info(f"DataValidator applied {len(results['fixes_applied'])} fixes")
                
        except Exception as e:
            results['success'] = False
            results['error'] = str(e)
            logger.error(f"DataValidator error: {e}")
        
        return results

class KPICalculatorBlock(BuildingBlock):
    """Calculates KPIs with industry-specific intelligence."""
    
    async def execute(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        kpi_definitions = self.config.get('kpi_definitions', {})
        industry = context.get('industry', 'unknown')
        
        results = {
            'success': True,
            'kpis': {},
            'industry_context': industry,
            'recommendations': []
        }
        
        try:
            for kpi_name, kpi_config in kpi_definitions.items():
                formula = kpi_config.get('formula', '')
                
                # Enhanced formula evaluation
                value = await self._evaluate_formula(formula, data)
                
                # Industry-specific thresholds
                thresholds = self._get_industry_thresholds(kpi_name, industry)
                status = self._evaluate_threshold(value, thresholds)
                
                results['kpis'][kpi_name] = {
                    'value': value,
                    'formatted': self._format_value(value, kpi_config.get('unit', '')),
                    'status': status,
                    'thresholds': thresholds
                }
                
                # Generate recommendations
                recommendation = self._generate_recommendation(kpi_name, value, status, industry)
                if recommendation:
                    results['recommendations'].append(recommendation)
                
                logger.info(f"Calculated {kpi_name}: {value} ({status})")
                
        except Exception as e:
            results['success'] = False
            results['error'] = str(e)
            logger.error(f"KPICalculator error: {e}")
        
        return results
    
    async def _evaluate_formula(self, formula: str, data: Dict[str, Any]) -> float:
        """Safely evaluate KPI formulas."""
        import re
        
        # Replace {column_name} with actual values
        def replace_column(match):
            col_name = match.group(1)
            if col_name in data:
                values = [float(x) for x in data[col_name] if x is not None and str(x).replace('.', '').replace('-', '').isdigit()]
                return str(sum(values))
            return "0"
        
        safe_formula = re.sub(r'\{(\w+)\}', replace_column, formula)
        
        # Safe evaluation with business functions
        allowed_names = {
            'sum': sum, 'len': len, 'min': min, 'max': max,
            'avg': lambda x: sum(x) / len(x) if x else 0,
            'abs': abs, 'round': round,
            # Business-specific functions
            'cagr': lambda start, end, years: ((end / start) ** (1/years) - 1) if start and years else 0,
            'margin': lambda revenue, cost: (revenue - cost) / revenue if revenue else 0
        }
        
        try:
            return float(eval(safe_formula, {"__builtins__": {}}, allowed_names))
        except:
            return 0.0
    
    def _get_industry_thresholds(self, kpi_name: str, industry: str) -> Dict[str, float]:
        """Get industry-specific thresholds for KPIs."""
        industry_thresholds = {
            'retail': {
                'profit_margin': {'good': 0.2, 'warning': 0.1, 'critical': 0.05},
                'inventory_turnover': {'good': 6, 'warning': 4, 'critical': 2}
            },
            'saas': {
                'churn_rate': {'good': 0.02, 'warning': 0.05, 'critical': 0.1},
                'customer_acquisition_cost': {'good': 100, 'warning': 200, 'critical': 300}
            },
            'ecommerce': {
                'conversion_rate': {'good': 0.05, 'warning': 0.02, 'critical': 0.01}
            }
        }
        
        return industry_thresholds.get(industry, {}).get(kpi_name, {})
    
    def _evaluate_threshold(self, value: float, thresholds: Dict[str, float]) -> str:
        """Evaluate KPI value against thresholds."""
        if not thresholds:
            return 'normal'
        
        if 'critical' in thresholds and value <= thresholds['critical']:
            return 'critical'
        elif 'warning' in thresholds and value <= thresholds['warning']:
            return 'warning'
        elif 'good' in thresholds and value >= thresholds['good']:
            return 'excellent'
        
        return 'normal'
    
    def _format_value(self, value: float, unit: str) -> str:
        """Format KPI values for display."""
        if unit == '%':
            return f"{value:.1%}"
        elif unit == '$':
            return f"${value:,.2f}"
        elif unit == 'ratio':
            return f"{value:.2f}"
        else:
            return f"{value:.2f}"
    
    def _generate_recommendation(self, kpi_name: str, value: float, status: str, industry: str) -> Optional[str]:
        """Generate actionable recommendations."""
        if status == 'critical':
            return f"URGENT: {kpi_name} is at critical level ({value}). Immediate action required."
        elif status == 'warning':
            return f"Monitor {kpi_name} closely. Current value ({value}) approaching critical threshold."
        
        return None

class AlertGeneratorBlock(BuildingBlock):
    """Generates contextual business alerts."""
    
    async def execute(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        alert_rules = self.config.get('alert_rules', [])
        
        results = {
            'success': True,
            'alerts': [],
            'alert_count': 0,
            'severity_summary': {'low': 0, 'medium': 0, 'high': 0, 'critical': 0}
        }
        
        try:
            for rule in alert_rules:
                condition_met, details = await self._evaluate_condition(rule.get('condition', {}), data)
                
                if condition_met:
                    alert = self._create_alert(rule, details, context)
                    results['alerts'].append(alert)
                    results['severity_summary'][alert['severity']] += 1
            
            results['alert_count'] = len(results['alerts'])
            logger.info(f"Generated {results['alert_count']} alerts")
            
        except Exception as e:
            results['success'] = False
            results['error'] = str(e)
            logger.error(f"AlertGenerator error: {e}")
        
        return results
    
    async def _evaluate_condition(self, condition: Dict[str, Any], data: Dict[str, Any]) -> tuple:
        """Evaluate alert condition against data."""
        column = condition.get('column')
        operator = condition.get('operator')
        threshold = condition.get('threshold')
        
        if not all([column, operator, threshold]) or column not in data:
            return False, {}
        
        try:
            values = [float(x) for x in data[column] if x is not None]
            if not values:
                return False, {}
            
            test_value = values[-1]  # Use latest value
            
            condition_met = False
            if operator == 'greater_than' and test_value > threshold:
                condition_met = True
            elif operator == 'less_than' and test_value < threshold:
                condition_met = True
            elif operator == 'equals' and abs(test_value - threshold) < 0.01:
                condition_met = True
            
            return condition_met, {
                'column': column,
                'value': test_value,
                'threshold': threshold,
                'operator': operator
            }
            
        except Exception:
            return False, {}
    
    def _create_alert(self, rule: Dict[str, Any], details: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Create a formatted alert."""
        return {
            'id': str(uuid.uuid4())[:8],
            'title': rule.get('title', 'Alert'),
            'message': rule.get('message', 'Condition met'),
            'severity': rule.get('severity', 'medium'),
            'details': details,
            'timestamp': datetime.datetime.now().isoformat(),
            'context': context.get('industry', 'unknown')
        }

def _register_default_blocks(registry: BuildingBlockRegistry):
    """Register all default building blocks."""
    registry.register_block('data_validator', DataValidatorBlock)
    registry.register_block('kpi_calculator', KPICalculatorBlock)
    registry.register_block('alert_generator', AlertGeneratorBlock)
    logger.info("Default building blocks registered")

# ===============================================================
# LAMBDA-INSPIRED BUILDING BLOCK SYSTEM
# ===============================================================

class BusinessKnowledgeBase:
    """Stores industry patterns and provides methods to detect industry, find relevant metrics, and detect analysis template type."""
    
    INDUSTRY_PATTERNS: Dict[str, Dict[str, Any]] = {
        'retail': {
            'key_metrics': ['sales', 'inventory', 'customer_satisfaction', 'foot_traffic', 'daily_sales'],
            'seasonal_patterns': ['holiday_season', 'summer_sales', 'back_to_school'],
            'common_issues': ['stockouts', 'overstock', 'customer_returns'],
            'keywords': ['store', 'product', 'customer', 'sales', 'inventory', 'retail', 'daily_sales'],
            'recommended_analysis': ['trend', 'comparative', 'correlation']
        },
        'saas': {
            'key_metrics': ['mrr', 'churn_rate', 'customer_acquisition_cost', 'lifetime_value', 'churn'],
            'seasonal_patterns': ['q4_subscription_renewals', 'annual_contract_renewals'],
            'common_issues': ['churn', 'customer_onboarding', 'feature_adoption'],
            'keywords': ['subscription', 'user', 'revenue', 'churn', 'acquisition', 'mrr', 'saas'],
            'recommended_analysis': ['trend', 'comparative', 'correlation']
        },
        'ecommerce': {
            'key_metrics': ['conversion_rate', 'average_order_value', 'cart_abandonment', 'customer_acquisition_cost', 'website_visits'],
            'seasonal_patterns': ['holiday_season', 'summer_sales', 'back_to_school'],
            'common_issues': ['cart_abandonment', 'shipping_delays', 'product_returns'],
            'keywords': ['online', 'product', 'customer', 'sales', 'conversion', 'website', 'ecommerce', 'cart'],
            'recommended_analysis': ['trend', 'comparative', 'correlation']
        },
        'finance': {
            'key_metrics': ['roi', 'profit_margin', 'cash_flow', 'debt_to_equity', 'revenue'],
            'seasonal_patterns': ['q4_financial_reporting', 'tax_season'],
            'common_issues': ['cash_flow_issues', 'debt_management', 'investment_returns'],
            'keywords': ['revenue', 'profit', 'investment', 'cash', 'debt', 'finance', 'roi'],
            'recommended_analysis': ['trend', 'comparative', 'correlation']
        }
    }

    def __init__(self, config_manager: ConfigManager) -> None:
        """
        Initialize BusinessKnowledgeBase with a ConfigManager.
        Args:
            config_manager (ConfigManager): The configuration manager instance.
        """
        self.config_manager = config_manager
        logger.info("BusinessKnowledgeBase initialized.")

    def detect_industry(self, question: str, data_columns: List[str]) -> str:
        """
        Detect the industry based on a business question and data columns.
        Args:
            question (str): The business question.
            data_columns (List[str]): The list of data columns.
        Returns:
            str: The detected industry.
        """
        # Convert columns to lowercase for better matching
        columns_lower = [col.lower() for col in data_columns]
        question_lower = question.lower()
        
        # Score each industry based on matches
        industry_scores = {}
        
        for industry, patterns in self.INDUSTRY_PATTERNS.items():
            score = 0
            
            # Check question keywords
            for keyword in patterns['keywords']:
                if keyword in question_lower:
                    score += 2
            
            # Check column names
            for keyword in patterns['keywords']:
                for col in columns_lower:
                    if keyword in col:
                        score += 1
            
            # Check for key metrics in columns
            for metric in patterns['key_metrics']:
                if metric.lower() in columns_lower:
                    score += 3
            
            industry_scores[industry] = score
        
        # Return industry with highest score, or 'unknown' if no matches
        if industry_scores and max(industry_scores.values()) > 0:
            return max(industry_scores, key=industry_scores.get)
        
        # Try to detect from specific columns
        if any('sales' in col or 'revenue' in col for col in columns_lower):
            if any('inventory' in col for col in columns_lower):
                return 'retail'
            elif any('conversion' in col or 'website' in col for col in columns_lower):
                return 'ecommerce'
        
        return 'unknown'

    def find_relevant_metrics(self, industry: str, data_columns: List[str]) -> List[str]:
        """
        Find relevant metrics in data columns for the detected industry.
        Args:
            industry (str): The detected industry.
            data_columns (List[str]): The list of data columns.
        Returns:
            List[str]: The list of relevant metrics.
        """
        if industry in self.INDUSTRY_PATTERNS:
            return [metric for metric in self.INDUSTRY_PATTERNS[industry]['key_metrics'] if metric in data_columns]
        return []

    def detect_analysis_template(self, question: str) -> str:
        """
        Detect the analysis template type based on the business question.
        Args:
            question (str): The business question.
        Returns:
            str: The detected analysis template type.
        """
        if 'trend' in question.lower():
            return 'trend'
        elif 'compare' in question.lower():
            return 'comparative'
        elif 'correlation' in question.lower():
            return 'correlation'
        return 'unknown'

class ExecutionManager:
    """Manages analysis execution with timeouts, progress tracking, and async function execution."""
    
    def __init__(self, config_manager: ConfigManager) -> None:
        """
        Initialize ExecutionManager with a ConfigManager.
        Args:
            config_manager (ConfigManager): The configuration manager instance.
        """
        self.config_manager = config_manager
        self.timeout_seconds = self.config_manager.get('analysis_config.timeout_seconds', 60)
        logger.info(f"ExecutionManager initialized with timeout: {self.timeout_seconds} seconds.")

    async def execute_with_timeout(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """
        Execute a function with a timeout.
        Args:
            func (Callable): The function to execute.
            *args (Any): Positional arguments for the function.
            **kwargs (Any): Keyword arguments for the function.
        Returns:
            Any: The result of the function execution.
        Raises:
            asyncio.TimeoutError: If the function execution times out.
        """
        try:
            return await asyncio.wait_for(func(*args, **kwargs), timeout=self.timeout_seconds)
        except asyncio.TimeoutError:
            logger.error(f"Function execution timed out after {self.timeout_seconds} seconds.")
            raise asyncio.TimeoutError(f"Function execution timed out after {self.timeout_seconds} seconds.")

    async def async_track_progress(self, callback: Callable[[int], None], total_steps: int) -> None:
        """
        Asynchronously track progress of an analysis with a callback function.
        Args:
            callback (Callable[[int], None]): The callback function to call with progress updates.
            total_steps (int): The total number of steps in the analysis.
        """
        for step in range(total_steps):
            callback(step + 1)
            await asyncio.sleep(0.1)  # Simulate async work being done

class CodeInspectorAgent:
    """Analyzes errors, suggests corrections, and maintains inspection history."""
    
    ERROR_PATTERNS: Dict[str, Dict[str, Any]] = {
        'data_type_mismatch': {
            'pattern': r'TypeError: .* expected .* got .*',
            'suggestion': 'Check data types of variables and ensure they match expected types.',
            'confidence': 0.9
        },
        'missing_column': {
            'pattern': r'KeyError: .* not found in .*',
            'suggestion': 'Verify that the column exists in the DataFrame.',
            'confidence': 0.8
        },
        'division_by_zero': {
            'pattern': r'ZeroDivisionError: division by zero',
            'suggestion': 'Add a check to prevent division by zero.',
            'confidence': 0.95
        }
    }

    def __init__(self, config_manager: ConfigManager, claude_client: Optional[Any] = None) -> None:
        """
        Initialize CodeInspectorAgent with a ConfigManager and optional Claude client.
        Args:
            config_manager (ConfigManager): The configuration manager instance.
            claude_client (Optional[Any]): Optional Claude client for advanced error analysis.
        """
        self.config_manager = config_manager
        self.claude_client = claude_client
        self.inspection_history: List[Dict[str, Any]] = []
        logger.info("CodeInspectorAgent initialized.")

    def analyze_error(self, error_message: str) -> Dict[str, Any]:
        """
        Analyze an error message and suggest corrections.
        Args:
            error_message (str): The error message to analyze.
        Returns:
            Dict[str, Any]: A dictionary containing the suggested correction and confidence score.
        """
        for error_type, details in self.ERROR_PATTERNS.items():
            if re.search(details['pattern'], error_message):
                correction = {
                    'error_type': error_type,
                    'suggestion': details['suggestion'],
                    'confidence': details['confidence']
                }
                self.inspection_history.append(correction)
                return correction
        return {'error_type': 'unknown', 'suggestion': 'No specific suggestion available.', 'confidence': 0.0}

    def get_inspection_summary(self) -> List[Dict[str, Any]]:
        """
        Get a summary of the inspection history.
        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing the inspection history.
        """
        return self.inspection_history

    def analyze_common_errors(self) -> Dict[str, int]:
        """
        Analyze common errors from the inspection history.
        Returns:
            Dict[str, int]: A dictionary containing the count of each error type.
        """
        error_counts: Dict[str, int] = {}
        for inspection in self.inspection_history:
            error_type = inspection['error_type']
            error_counts[error_type] = error_counts.get(error_type, 0) + 1
        return error_counts

class MCPTool:
    """Represents a tool in the MCP framework."""
    
    def __init__(self, name: str, func: Callable) -> None:
        """
        Initialize MCPTool with a name and function.
        Args:
            name (str): The name of the tool.
            func (Callable): The function to be called.
        """
        self.name = name
        self.func = func

class MCPResource:
    """Represents a resource in the MCP framework."""
    
    def __init__(self, name: str, func: Callable) -> None:
        """
        Initialize MCPResource with a name and function.
        Args:
            name (str): The name of the resource.
            func (Callable): The function to be called.
        """
        self.name = name
        self.func = func

class MCPServer(ABC):
    """Abstract base class for MCP servers with automatic tool/resource registration."""
    
    def __init__(self) -> None:
        """Initialize MCPServer and register tools and resources."""
        self.tools: Dict[str, MCPTool] = {}
        self.resources: Dict[str, MCPResource] = {}
        self.request_count: int = 0
        self._register_tools_and_resources()
        logger.info("MCPServer initialized.")

    def _register_tools_and_resources(self) -> None:
        """Register all tools and resources marked with decorators."""
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if hasattr(attr, 'mcp_tool'):
                if not callable(attr) or not hasattr(attr, '__code__') or not attr.__code__.co_flags & 0x80:
                    logger.warning(f"Tool '{attr_name}' is not async. It should be an async function.")
                self.tools[attr_name] = MCPTool(attr_name, attr)
            elif hasattr(attr, 'mcp_resource'):
                if not callable(attr) or not hasattr(attr, '__code__') or not attr.__code__.co_flags & 0x80:
                    logger.warning(f"Resource '{attr_name}' is not async. It should be an async function.")
                self.resources[attr_name] = MCPResource(attr_name, attr)

    async def call_tool(self, tool_name: str, *args: Any, **kwargs: Any) -> Any:
        """
        Call a tool by name.
        Args:
            tool_name (str): The name of the tool to call.
            *args (Any): Positional arguments for the tool.
            **kwargs (Any): Keyword arguments for the tool.
        Returns:
            Any: The result of the tool execution.
        Raises:
            KeyError: If the tool is not found.
        """
        if tool_name not in self.tools:
            logger.error(f"Tool '{tool_name}' not found.")
            raise KeyError(f"Tool '{tool_name}' not found.")
        self.request_count += 1
        try:
            return await self.tools[tool_name].func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Exception in tool '{tool_name}': {e}")
            raise

    async def get_resource(self, resource_name: str, *args: Any, **kwargs: Any) -> Any:
        """
        Get a resource by name.
        Args:
            resource_name (str): The name of the resource to get.
            *args (Any): Positional arguments for the resource.
            **kwargs (Any): Keyword arguments for the resource.
        Returns:
            Any: The result of the resource execution.
        Raises:
            KeyError: If the resource is not found.
        """
        if resource_name not in self.resources:
            logger.error(f"Resource '{resource_name}' not found.")
            raise KeyError(f"Resource '{resource_name}' not found.")
        self.request_count += 1
        try:
            return await self.resources[resource_name].func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Exception in resource '{resource_name}': {e}")
            raise

def mcp_tool(func: Callable) -> Callable:
    """
    Decorator to mark a method as an MCP tool.
    Args:
        func (Callable): The function to be marked as a tool.
    Returns:
        Callable: The decorated function.
    """
    func.mcp_tool = True
    return func

def mcp_resource(func: Callable) -> Callable:
    """
    Decorator to mark a method as an MCP resource.
    Args:
        func (Callable): The function to be marked as a resource.
    Returns:
        Callable: The decorated function.
    """
    func.mcp_resource = True
    return func

class BIToolsMCPServer(MCPServer):
    """Extends MCPServer with business intelligence tools for dashboard creation, report generation, and more."""
    
    def __init__(self, config_manager: ConfigManager) -> None:
        """
        Initialize BIToolsMCPServer with a ConfigManager.
        Args:
            config_manager (ConfigManager): The configuration manager instance.
        """
        super().__init__()
        self.config_manager = config_manager
        logger.info("BIToolsMCPServer initialized.")

    @mcp_tool
    async def create_dashboard(self, industry: str, dashboard_type: str) -> Dict[str, Any]:
        """
        Create a dashboard with industry-specific visualizations.
        Args:
            industry (str): The industry for which to create the dashboard.
            dashboard_type (str): The type of dashboard (executive, financial, operational).
        Returns:
            Dict[str, Any]: A dictionary containing the dashboard data.
        """
        # Placeholder for dashboard creation logic
        return {'industry': industry, 'dashboard_type': dashboard_type, 'visualizations': []}

    @mcp_tool
    async def generate_report(self, data: Dict[str, Any]) -> str:
        """
        Generate a report with markdown output.
        Args:
            data (Dict[str, Any]): The data to include in the report.
        Returns:
            str: The generated report in markdown format.
        """
        # Placeholder for report generation logic
        return f"# Report\n\nData: {data}"

    @mcp_tool
    async def export_to_jupyter(self, data: Dict[str, Any]) -> str:
        """
        Export data to a Jupyter notebook.
        Args:
            data (Dict[str, Any]): The data to export.
        Returns:
            str: The path to the exported Jupyter notebook.
        """
        # Placeholder for Jupyter notebook export logic
        return "path/to/notebook.ipynb"

    @mcp_resource
    async def get_kpi_library(self) -> Dict[str, List[str]]:
        """
        Get the KPI library for different metrics.
        Returns:
            Dict[str, List[str]]: A dictionary containing KPIs for different categories.
        """
        # Placeholder for KPI library
        return {
            'financial': ['roi', 'profit_margin', 'cash_flow'],
            'operational': ['efficiency', 'productivity', 'quality'],
            'executive': ['market_share', 'customer_satisfaction', 'growth_rate']
        }

    @mcp_tool
    async def create_enhanced_visualization(self, data: Dict[str, Any], context: str) -> Dict[str, Any]:
        """
        Create enhanced visualizations based on knowledge context.
        Args:
            data (Dict[str, Any]): The data to visualize.
            context (str): The context for the visualization.
        Returns:
            Dict[str, Any]: A dictionary containing the visualization data.
        """
        # Placeholder for enhanced visualization logic
        return {'data': data, 'context': context, 'visualization': 'enhanced'}

class MCPClient:
    """Handles server communication, tracks call and error counts, and provides statistics on success rate."""
    
    def __init__(self, server_url: str) -> None:
        """
        Initialize MCPClient with a server URL.
        Args:
            server_url (str): The URL of the MCP server.
        """
        self.server_url = server_url
        self.call_count: int = 0
        self.error_count: int = 0
        logger.info(f"MCPClient initialized with server URL: {server_url}")

    async def call_server(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call the MCP server with the specified endpoint and data.
        Args:
            endpoint (str): The endpoint to call.
            data (Dict[str, Any]): The data to send.
        Returns:
            Dict[str, Any]: The response from the server.
        Raises:
            Exception: If the server call fails.
        """
        self.call_count += 1
        try:
            # Placeholder for actual server call logic
            response = {'status': 'success', 'data': data}
            return response
        except Exception as e:
            self.error_count += 1
            logger.error(f"Error calling server: {e}")
            raise

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics on the success rate of server calls.
        Returns:
            Dict[str, Any]: A dictionary containing call count, error count, and success rate.
        """
        success_rate = (self.call_count - self.error_count) / self.call_count if self.call_count > 0 else 0
        return {
            'call_count': self.call_count,
            'error_count': self.error_count,
            'success_rate': success_rate
        }

class ConversationMemory:
    """Stores conversation exchanges with metadata, tracks analysis patterns, and maintains success rates."""
    
    def __init__(self, config_manager: Optional[ConfigManager] = None) -> None:
        """
        Initialize ConversationMemory with an optional ConfigManager.
        Args:
            config_manager (Optional[ConfigManager]): The configuration manager instance.
        """
        self.config_manager = config_manager
        self.max_history = self.config_manager.get('conversation.max_history', 100) if self.config_manager else 100
        self.conversations: deque[Dict[str, Any]] = deque()
        self.question_types: Dict[str, int] = {}
        self.success_rates: Dict[str, float] = {}
        logger.info("ConversationMemory initialized.")

    def add_exchange(self, question: str, answer: str, metadata: Dict[str, Any]) -> None:
        """
        Add a conversation exchange with metadata.
        Args:
            question (str): The question asked.
            answer (str): The answer provided.
            metadata (Dict[str, Any]): Additional metadata for the exchange.
        """
        exchange = {
            'question': question,
            'answer': answer,
            'metadata': metadata,
            'timestamp': datetime.datetime.now().isoformat()
        }
        self.conversations.append(exchange)
        if len(self.conversations) > self.max_history:
            self.conversations.popleft()
        self._update_question_types(question)
        self._update_success_rates(question, answer)

    def _update_question_types(self, question: str) -> None:
        """
        Update the count of question types based on the question.
        Args:
            question (str): The question to classify.
        """
        question_type = self.classify_question(question)
        self.question_types[question_type] = self.question_types.get(question_type, 0) + 1

    def _update_success_rates(self, question: str, answer: str) -> None:
        """
        Update the success rates for different question types.
        Args:
            question (str): The question asked.
            answer (str): The answer provided.
        """
        question_type = self.classify_question(question)
        success = answer != "No answer available."
        current_success_rate = self.success_rates.get(question_type, 0.0)
        count = self.question_types.get(question_type, 0)
        self.success_rates[question_type] = (current_success_rate * (count - 1) + (1 if success else 0)) / count

    def classify_question(self, question: str) -> str:
        """
        Classify a question into a type (trend, comparative, etc.).
        Args:
            question (str): The question to classify.
        Returns:
            str: The classified question type.
        """
        if 'trend' in question.lower():
            return 'trend'
        elif 'compare' in question.lower():
            return 'comparative'
        elif 'correlation' in question.lower():
            return 'correlation'
        return 'unknown'

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics on question types and success rates.
        Returns:
            Dict[str, Any]: A dictionary containing question types and success rates.
        """
        return {
            'question_types': self.question_types,
            'success_rates': self.success_rates
        }

class BusinessAnalysisAgent:
    """Analyzes business data with self-correction, industry-specific insights, and recommendations."""
    
    def __init__(self, mcp_clients: Dict[str, MCPClient], config: ConfigManager, claude_client: Optional[Any] = None, execution_manager: Optional[ExecutionManager] = None) -> None:
        """
        Initialize BusinessAnalysisAgent with MCP clients, configuration, and optional Claude client.
        Args:
            mcp_clients (Dict[str, MCPClient]): Dictionary of MCP clients.
            config (ConfigManager): The configuration manager instance.
            claude_client (Optional[Any]): Optional Claude client for advanced analysis.
            execution_manager (Optional[ExecutionManager]): Optional execution manager for timeouts and progress.
        """
        self.mcp_clients = mcp_clients
        self.config = config
        self.claude_client = claude_client
        self.knowledge_base = BusinessKnowledgeBase(config)
        self.code_inspector = CodeInspectorAgent(config)
        self.execution_manager = execution_manager or ExecutionManager(config)
        self.building_block_registry = BuildingBlockRegistry()
        logger.info("BusinessAnalysisAgent initialized.")
        logger.info("BusinessAnalysisAgent initialized with building blocks")

    async def analyze_data_with_correction(self, data: Dict[str, Any], question: str, workflow_steps: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Analyze data with self-correction and optional building blocks workflow.
        Args:
            data: The data to analyze
            question: The question to answer
            workflow_steps: Optional list of building block workflow steps
        Returns:
            Dict containing analysis results
        """
        max_attempts = self.config.get('analysis_config.max_attempts', 3)
        
        for attempt in range(max_attempts):
            try:
                # Detect industry and analysis type
                industry = self.knowledge_base.detect_industry(question, list(data.keys()))
                analysis_type = self.knowledge_base.detect_analysis_template(question)
                
                context = {
                    'industry': industry,
                    'analysis_type': analysis_type,
                    'question': question,
                    'attempt': attempt + 1
                }
                
                # If workflow steps provided, use building blocks
                if workflow_steps:
                    workflow_result = await self.execute_building_blocks_workflow(data, workflow_steps, context)
                    
                    # Generate insights from workflow results
                    insights = await self._generate_insights_from_workflow(workflow_result, industry, analysis_type)
                    
                    result = {
                        'insights': insights,
                        'workflow_result': workflow_result,
                        'recommendations': self._provide_recommendations(industry, analysis_type),
                        'industry': industry,
                        'analysis_type': analysis_type,
                        'execution_method': 'building_blocks'
                    }
                else:
                    # Use traditional analysis
                    insights = await self.execution_manager.execute_with_timeout(
                        self._generate_insights, data, industry, analysis_type
                    )
                    
                    result = {
                        'insights': insights,
                        'recommendations': self._provide_recommendations(industry, analysis_type),
                        'industry': industry,
                        'analysis_type': analysis_type,
                        'execution_method': 'traditional'
                    }
                
                return result
                
            except Exception as e:
                error_message = str(e)
                correction = self.code_inspector.analyze_error(error_message)
                
                logger.warning(f"Analysis attempt {attempt + 1} failed: {error_message}")
                
                if attempt == max_attempts - 1:
                    # Last attempt, return error
                    return {
                        'error': error_message,
                        'correction': correction,
                        'attempts_made': max_attempts
                    }
                
                # Try to apply correction for next attempt
                if correction.get('confidence', 0) > 0.8:
                    logger.info(f"Applying correction: {correction.get('suggestion')}")
                    # Correction logic could be added here
                
                await asyncio.sleep(0.1)  # Brief pause before retry
        
        return {'error': 'Max attempts exceeded', 'attempts_made': max_attempts}

    async def _generate_insights_from_workflow(self, workflow_result: Dict[str, Any], industry: str, analysis_type: str) -> List[str]:
        """Generate insights from building blocks workflow results."""
        insights = []
        
        # Summary insight
        steps_completed = workflow_result.get('steps_completed', 0)
        total_steps = workflow_result.get('total_steps', 0)
        insights.append(f"Workflow completed {steps_completed}/{total_steps} building blocks successfully")
        
        # Extract insights from each building block result
        for step_name, step_result in workflow_result.get('results', {}).items():
            if step_result.get('success'):
                # DataValidator insights
                if 'fixes_applied' in step_result:
                    fixes = step_result['fixes_applied']
                    if fixes:
                        insights.append(f"Data quality fixes: {'; '.join(fixes)}")
                
                # KPI Calculator insights
                if 'kpis' in step_result:
                    kpis = step_result['kpis']
                    for kpi_name, kpi_data in kpis.items():
                        status = kpi_data.get('status', 'normal')
                        value = kpi_data.get('formatted', kpi_data.get('value'))
                        insights.append(f"{kpi_name}: {value} ({status})")
                
                # Alert Generator insights
                if 'alerts' in step_result:
                    alert_count = step_result.get('alert_count', 0)
                    if alert_count > 0:
                        insights.append(f"Generated {alert_count} business alerts")
                        # Add critical alerts detail
                        critical_alerts = [a for a in step_result['alerts'] if a.get('severity') == 'critical']
                        if critical_alerts:
                            insights.append(f"⚠️ {len(critical_alerts)} critical alerts require immediate attention")
        
        # Add traditional insights if no workflow insights found
        if len(insights) <= 1:
            traditional_insights = await self._generate_insights(workflow_result.get('final_data', {}), industry, analysis_type)
            insights.extend(traditional_insights)
        
        return insights

    async def _generate_insights(self, data: Dict[str, Any], industry: str, analysis_type: str) -> List[str]:
        """
        Generate real insights based on data, industry, and analysis type.
        Args:
            data (Dict[str, Any]): The data to analyze.
            industry (str): The detected industry.
            analysis_type (str): The type of analysis.
        Returns:
            List[str]: A list of insights.
        """
        insights = []
        
        try:
            # Convert dict back to DataFrame for analysis
            df = pd.DataFrame(data)
            
            # Handle missing values
            if df.empty:
                return ["No data available for analysis"]
            
            # Basic data insights
            insights.append(f"Dataset contains {len(df)} records across {len(df.columns)} columns")
            
            # Numeric columns analysis
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if len(numeric_cols) > 0:
                insights.append(f"Found {len(numeric_cols)} numeric columns for analysis: {', '.join(numeric_cols)}")
                
                # Find correlations
                if len(numeric_cols) > 1:
                    try:
                        corr_matrix = df[numeric_cols].corr()
                        strong_corr = []
                        for i, col1 in enumerate(numeric_cols):
                            for col2 in numeric_cols[i+1:]:
                                if col1 in corr_matrix.columns and col2 in corr_matrix.columns:
                                    corr_val = corr_matrix.loc[col1, col2]
                                    if abs(corr_val) > 0.7 and not pd.isna(corr_val):
                                        strong_corr.append(f"{col1} and {col2} (correlation: {corr_val:.2f})")
                        
                        if strong_corr:
                            insights.append(f"Strong correlations found: {', '.join(strong_corr)}")
                    except Exception as e:
                        insights.append(f"Correlation analysis error: {str(e)}")
            
            # Industry-specific insights
            if industry == 'retail':
                if 'daily_sales' in df.columns:
                    avg_sales = df['daily_sales'].mean()
                    max_sales = df['daily_sales'].max()
                    min_sales = df['daily_sales'].min()
                    insights.append(f"Daily sales - Average: ${avg_sales:,.2f}, Max: ${max_sales:,.2f}, Min: ${min_sales:,.2f}")
                    
                if 'region' in df.columns and 'daily_sales' in df.columns:
                    try:
                        region_sales = df.groupby('region')['daily_sales'].mean().sort_values(ascending=False)
                        best_region = region_sales.index[0]
                        worst_region = region_sales.index[-1]
                        insights.append(f"Best performing region: {best_region} (${region_sales.iloc[0]:,.2f})")
                        insights.append(f"Lowest performing region: {worst_region} (${region_sales.iloc[-1]:,.2f})")
                    except Exception as e:
                        insights.append(f"Regional analysis error: {str(e)}")
                        
                if 'inventory_level' in df.columns:
                    avg_inventory = df['inventory_level'].mean()
                    insights.append(f"Average inventory level: {avg_inventory:,.0f}")
            
            elif industry == 'ecommerce':
                if 'conversion_rate' in df.columns:
                    avg_conversion = df['conversion_rate'].mean()
                    max_conversion = df['conversion_rate'].max()
                    insights.append(f"Conversion rate - Average: {avg_conversion:.1%}, Best: {max_conversion:.1%}")
                    
                if 'cart_abandonment_rate' in df.columns:
                    avg_abandonment = df['cart_abandonment_rate'].mean()
                    insights.append(f"Average cart abandonment rate: {avg_abandonment:.1%}")
                    
                if 'website_visits' in df.columns and 'sales' in df.columns:
                    total_visits = df['website_visits'].sum()
                    total_sales = df['sales'].sum()
                    insights.append(f"Total website visits: {total_visits:,}, Total sales: ${total_sales:,.2f}")
            
            elif industry == 'saas':
                if 'mrr' in df.columns:
                    avg_mrr = df['mrr'].mean()
                    growth_rate = ((df['mrr'].iloc[-1] - df['mrr'].iloc[0]) / df['mrr'].iloc[0]) * 100 if len(df) > 1 else 0
                    insights.append(f"Average MRR: ${avg_mrr:,.2f}, Growth rate: {growth_rate:.1f}%")
                    
                if 'churn_rate' in df.columns:
                    avg_churn = df['churn_rate'].mean()
                    insights.append(f"Average churn rate: {avg_churn:.1%}")
            
            elif industry == 'finance':
                if 'revenue' in df.columns:
                    total_revenue = df['revenue'].sum()
                    avg_revenue = df['revenue'].mean()
                    insights.append(f"Total revenue: ${total_revenue:,.2f}, Average: ${avg_revenue:,.2f}")
                    
                if 'profit_margin' in df.columns:
                    avg_margin = df['profit_margin'].mean()
                    insights.append(f"Average profit margin: {avg_margin:.1%}")
                    
                if 'roi' in df.columns:
                    avg_roi = df['roi'].mean()
                    insights.append(f"Average ROI: {avg_roi:.1%}")
            
            # Time-based analysis if date column exists
            if analysis_type == 'trend' and 'date' in df.columns:
                insights.append(f"Time series analysis performed on {len(df)} data points")
                if len(df) > 1:
                    date_range = f"from {df['date'].min()} to {df['date'].max()}"
                    insights.append(f"Data covers period {date_range}")
            
            # Add general statistics for numeric columns
            if numeric_cols:
                insights.append("Key statistics:")
                for col in numeric_cols[:3]:  # Show stats for first 3 numeric columns
                    mean_val = df[col].mean()
                    std_val = df[col].std()
                    insights.append(f"  {col}: Mean={mean_val:.2f}, Std={std_val:.2f}")
                
        except Exception as e:
            insights.append(f"Analysis error: {str(e)}")
            logger.error(f"Error in _generate_insights: {str(e)}")
        
        return insights if insights else [f"Basic {analysis_type} analysis completed for {industry} industry"]

    def _provide_recommendations(self, industry: str, analysis_type: str) -> List[str]:
        """
        Provide real recommendations based on industry and analysis type.
        Args:
            industry (str): The detected industry.
            analysis_type (str): The type of analysis.
        Returns:
            List[str]: A list of actionable recommendations.
        """
        recommendations = []
        
        if industry == 'retail':
            recommendations.extend([
                "Monitor inventory levels to prevent stockouts in high-performing regions",
                "Focus marketing efforts on peak sales periods",
                "Analyze customer satisfaction scores to improve retention"
            ])
        elif industry == 'ecommerce':
            recommendations.extend([
                "Optimize conversion funnel to reduce cart abandonment",
                "A/B test website changes during high-traffic periods",
                "Implement personalized marketing based on customer behavior"
            ])
        elif industry == 'saas':
            recommendations.extend([
                "Monitor churn rate trends for early warning signs",
                "Focus on customer success to improve retention",
                "Analyze feature usage to guide product development"
            ])
        else:
            recommendations.extend([
                "Set up regular monitoring of key performance metrics",
                "Implement data quality checks to ensure accurate analysis",
                "Consider industry-specific KPIs for better insights"
            ])
        
        # Add analysis-type specific recommendations
        if analysis_type == 'trend':
            recommendations.append("Set up automated alerts for significant trend changes")
        elif analysis_type == 'comparative':
            recommendations.append("Focus resources on underperforming segments")
        elif analysis_type == 'correlation':
            recommendations.append("Investigate causal relationships behind strong correlations")
        
        return recommendations

    async def execute_building_blocks_workflow(self, data: Dict[str, Any], workflow_steps: List[Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a sequence of building blocks as a workflow."""
        workflow_results = {
            'success': True,
            'steps_completed': 0,
            'total_steps': len(workflow_steps),
            'results': {},
            'final_data': data.copy(),
            'workflow_summary': []
        }
        
        current_data = data.copy()
        
        try:
            for i, step in enumerate(workflow_steps):
                step_name = step.get('name', f"step_{i}")
                block_type = step.get('type')
                block_config = step.get('config', {})
                
                logger.info(f"Executing workflow step {i+1}/{len(workflow_steps)}: {step_name}")
                
                # Create and execute building block
                block = self.building_block_registry.create_block(block_type, block_config)
                step_result = await block.execute(current_data, context)
                
                # Store result
                workflow_results['results'][step_name] = step_result
                workflow_results['steps_completed'] = i + 1
                
                # If block updated data, use it for next step
                if step_result.get('data_updates'):
                    current_data.update(step_result['data_updates'])
                    workflow_results['final_data'] = current_data
                
                # Add to summary
                workflow_results['workflow_summary'].append({
                    'step': step_name,
                    'block_type': block_type,
                    'success': step_result.get('success', True),
                    'message': f"Completed {step_name}"
                })
                
                # Stop on failure if specified
                if not step_result.get('success', True) and block_config.get('stop_on_failure', False):
                    workflow_results['success'] = False
                    break
            
            logger.info(f"Workflow completed: {workflow_results['steps_completed']}/{workflow_results['total_steps']} steps")
            
        except Exception as e:
            workflow_results['success'] = False
            workflow_results['error'] = str(e)
            logger.error(f"Workflow execution error: {e}")
        
        return workflow_results

class BusinessAnalysisOrchestrator:
    """Orchestrates business analysis components, tracks statistics, and provides comprehensive system insights."""
    
    def __init__(self, claude_client: Any, config_path: str) -> None:
        """Initialize BusinessAnalysisOrchestrator with templates and enhanced capabilities."""
        self.config_manager = ConfigManager(config_path)
        self.mcp_clients = {'default': MCPClient('http://example.com')}
        self.business_agent = BusinessAnalysisAgent(self.mcp_clients, self.config_manager, claude_client)
        self.conversation_memory = ConversationMemory(self.config_manager)
        
        # Initialize template system
        self.template_manager = AgentTemplateManager()
        
        # Enhanced system stats
        self.system_stats = {
            'initializations': 1,
            'analyses': 0,
            'errors': 0,
            'template_usage': {},
            'workflow_executions': 0,
            'correction_attempts': 0
        }
        self.status_log = []
        logger.info("BusinessAnalysisOrchestrator initialized with template system")

    def log_status(self, message: str) -> None:
        """Log a status message."""
        self.status_log.append(message)
        logger.info(message)

    async def analyze_with_template(self, question: str, data: Dict[str, Any], template_id: str, 
                                   auto_apply_template: bool = True) -> Dict[str, Any]:
        """
        Analyze business question using a specific template.
        
        Args:
            question: Business question to analyze
            data: Data to analyze  
            template_id: ID of template to use
            auto_apply_template: Whether to automatically apply template or just suggest
            
        Returns:
            Analysis results with template context
        """
        template = self.template_manager.get_template(template_id)
        if not template:
            return {'error': f'Template {template_id} not found'}
        
        # Track template usage
        self.system_stats['template_usage'][template_id] = self.system_stats['template_usage'].get(template_id, 0) + 1
        self.system_stats['workflow_executions'] += 1
        
        # Validate template compatibility
        available_columns = list(data.keys())
        compatibility = self.template_manager.validate_template_compatibility(template, available_columns)
        
        if not compatibility['compatible'] and not auto_apply_template:
            return {
                'template_info': template.to_dict(),
                'compatibility': compatibility,
                'suggestion': 'Template requires data mapping before use',
                'can_proceed': False
            }
        
        # Apply column mappings if suggested
        mapped_data = data.copy()
        if compatibility['suggestions']:
            for missing_col, suggested_col in compatibility['suggestions'].items():
                if suggested_col in mapped_data:
                    mapped_data[missing_col] = mapped_data[suggested_col]
                    self.log_status(f"Mapped column: {suggested_col} -> {missing_col}")
        
        # Execute template workflow
        try:
            self.log_status(f"Executing template: {template.name}")
            
            # Use template's workflow steps
            result = await self.business_agent.analyze_data_with_correction(
                mapped_data, 
                question, 
                workflow_steps=template.workflow_steps
            )
            
            # Enhance result with template context
            result.update({
                'template_used': template.to_dict(),
                'compatibility_score': compatibility['compatibility_score'],
                'column_mappings': compatibility['suggestions'],
                'template_recommendations': self._generate_template_recommendations(template, result)
            })
            
            self.log_status(f"Template analysis completed: {template.name}")
            return result
            
        except Exception as e:
            self.system_stats['errors'] += 1
            logger.error(f"Template analysis error: {e}")
            return {
                'error': str(e),
                'template_info': template.to_dict(),
                'compatibility': compatibility
            }
    
    def suggest_templates(self, question: str, data_columns: List[str]) -> List[Dict[str, Any]]:
        """
        Suggest appropriate templates based on question and data columns.
        
        Args:
            question: Business question
            data_columns: Available data columns
            
        Returns:
            List of suggested templates with compatibility scores
        """
        # Detect industry and department from question
        industry = self.business_agent.knowledge_base.detect_industry(question, data_columns)
        
        # Score templates based on compatibility and relevance
        template_suggestions = []
        
        for template in self.template_manager.list_templates():
            # Check compatibility
            compatibility = self.template_manager.validate_template_compatibility(template, data_columns)
            
            # Calculate relevance score
            relevance_score = self._calculate_template_relevance(template, question, industry)
            
            # Combined score
            combined_score = (compatibility['compatibility_score'] * 0.7) + (relevance_score * 0.3)
            
            template_suggestions.append({
                'template': template.to_dict(),
                'compatibility_score': compatibility['compatibility_score'],
                'relevance_score': relevance_score,
                'combined_score': combined_score,
                'missing_columns': compatibility['missing_required'],
                'suggested_mappings': compatibility['suggestions'],
                'usage_count': self.system_stats['template_usage'].get(template.id, 0)
            })
        
        # Sort by combined score
        template_suggestions.sort(key=lambda x: x['combined_score'], reverse=True)
        
        return template_suggestions[:5]  # Return top 5 suggestions
    
    def _calculate_template_relevance(self, template: AgentTemplate, question: str, industry: str) -> float:
        """Calculate how relevant a template is to the question and context."""
        relevance_score = 0.0
        question_lower = question.lower()
        
        # Industry tag match
        if industry in template.industry_tags or 'all' in template.industry_tags:
            relevance_score += 0.3
        
        # Keyword matching with template description
        template_keywords = template.description.lower().split()
        question_words = question_lower.split()
        keyword_matches = sum(1 for word in question_words if word in template_keywords)
        relevance_score += (keyword_matches / len(question_words)) * 0.4
        
        # Department-specific keyword matching
        dept_keywords = {
            'marketing': ['campaign', 'roi', 'conversion', 'acquisition', 'customer'],
            'finance': ['budget', 'cost', 'revenue', 'profit', 'financial'],
            'operations': ['inventory', 'efficiency', 'turnover', 'optimization']
        }
        
        if template.department in dept_keywords:
            dept_matches = sum(1 for kw in dept_keywords[template.department] if kw in question_lower)
            relevance_score += (dept_matches / len(dept_keywords[template.department])) * 0.3
        
        return min(relevance_score, 1.0)
    
    def _generate_template_recommendations(self, template: AgentTemplate, analysis_result: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on template analysis results."""
        recommendations = []
        
        # Template-specific recommendations
        if template.department == 'marketing':
            if 'workflow_result' in analysis_result:
                workflow_result = analysis_result['workflow_result']
                kpi_results = workflow_result.get('results', {}).get('calculate_campaign_kpis', {})
                if 'kpis' in kpi_results:
                    for kpi_name, kpi_data in kpi_results['kpis'].items():
                        if kpi_data.get('status') == 'critical':
                            recommendations.append(f"Immediate attention needed for {kpi_name}")
        
        elif template.department == 'finance':
            if 'workflow_result' in analysis_result:
                workflow_result = analysis_result['workflow_result']
                if any('budget' in step_name for step_name in workflow_result.get('results', {})):
                    recommendations.append("Review budget allocation based on variance analysis")
        
        # General recommendations based on analysis success
        if analysis_result.get('success', True):
            recommendations.append(f"Consider setting up regular monitoring using '{template.name}' template")
        
        return recommendations

    async def analyze_business_question(self, question: str, data: Dict[str, Any], 
                                       use_self_correction: bool = True, 
                                       use_knowledge_base: bool = True,
                                       auto_suggest_templates: bool = True,
                                       template_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Enhanced business question analysis with template support.
        
        Args:
            question: Business question to analyze
            data: Data to analyze
            use_self_correction: Whether to use self-correction
            use_knowledge_base: Whether to use knowledge base
            auto_suggest_templates: Whether to automatically suggest templates
            template_id: Specific template ID to use
            
        Returns:
            Analysis results with template suggestions/usage
        """
        self.system_stats['analyses'] += 1
        
        try:
            self.log_status("Starting enhanced business analysis")
            
            # If specific template requested, use it
            if template_id:
                return await self.analyze_with_template(question, data, template_id)
            
            # Suggest templates if enabled
            template_suggestions = []
            if auto_suggest_templates:
                template_suggestions = self.suggest_templates(question, list(data.keys()))
                self.log_status(f"Found {len(template_suggestions)} template suggestions")
                
                # Auto-apply best template if high compatibility
                if template_suggestions and template_suggestions[0]['combined_score'] > 0.8:
                    best_template = template_suggestions[0]['template']
                    self.log_status(f"Auto-applying template: {best_template['name']}")
                    return await self.analyze_with_template(question, data, best_template['id'])
            
            # Run traditional analysis
            self.log_status("Running traditional analysis")
            result = await self.business_agent.analyze_data_with_correction(data, question)
            
            # Add template suggestions to result
            if template_suggestions:
                result['template_suggestions'] = template_suggestions
                result['suggestion_message'] = (
                    f"Consider using '{template_suggestions[0]['template']['name']}' template "
                    f"for enhanced {template_suggestions[0]['template']['department']} analysis"
                )
            
            # Update conversation memory with enhanced metadata
            metadata = {
                'industry': result.get('industry'),
                'analysis_type': result.get('analysis_type'),
                'template_suggestions_count': len(template_suggestions),
                'execution_method': result.get('execution_method', 'traditional')
            }
            
            self.conversation_memory.add_exchange(question, str(result), metadata)
            self.log_status("Analysis completed successfully")
            
            return result
            
        except Exception as e:
            self.system_stats['errors'] += 1
            logger.error(f"Enhanced analysis error: {e}")
            return {
                'error': str(e),
                'template_suggestions': template_suggestions if 'template_suggestions' in locals() else []
            }

    def get_template_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics including template usage."""
        stats = self.get_system_statistics()
        
        # Add template-specific statistics
        template_stats = {
            'total_templates': len(self.template_manager.list_templates()),
            'templates_by_department': {},
            'most_used_templates': [],
            'template_success_rate': {}
        }
        
        # Count templates by department
        for template in self.template_manager.list_templates():
            dept = template.department
            template_stats['templates_by_department'][dept] = template_stats['templates_by_department'].get(dept, 0) + 1
        
        # Most used templates
        if self.system_stats['template_usage']:
            sorted_usage = sorted(self.system_stats['template_usage'].items(), key=lambda x: x[1], reverse=True)
            template_stats['most_used_templates'] = [
                {'template_id': tid, 'usage_count': count} for tid, count in sorted_usage[:5]
            ]
        
        stats['template_statistics'] = template_stats
        return stats

    def get_system_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive system statistics.
        Returns:
            Dict[str, Any]: A dictionary containing system statistics.
        """
        return {
            'system_stats': self.system_stats,
            'conversation_stats': self.conversation_memory.get_statistics()
        }

async def async_main() -> None:
    """Async main function for testing orchestrator and analysis."""
    # Initialize components for CLI test
    components = initialize_components()
    orchestrator = components['orchestrator']

    # Sample data generation for testing
    sample_data = {
        'sales': [100, 200, 150, 300],
        'customers': [10, 20, 15, 30],
        'date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04']
    }
    question = "What are the sales trends over time?"
    
    # Test analysis
    result = await orchestrator.analyze_business_question(question, sample_data)
    print("Analysis Result:", result)
    print("System Statistics:", orchestrator.get_system_statistics())

def initialize_components() -> Dict[str, Any]:
    """Initialize all components and return them in a dictionary."""
    config_manager = ConfigManager("config.yaml")
    mcp_client = MCPClient('http://example.com')
    business_agent = BusinessAnalysisAgent(
        mcp_clients={'default': mcp_client},
        config=config_manager,
        claude_client=None
    )
    conversation_memory = ConversationMemory(config_manager)
    orchestrator = BusinessAnalysisOrchestrator(
        claude_client=None,
        config_path="config.yaml"
    )
    return {
        'config_manager': config_manager,
        'mcp_client': mcp_client,
        'business_agent': business_agent,
        'conversation_memory': conversation_memory,
        'orchestrator': orchestrator
    }

def main() -> None:
    """Main function to run the Streamlit application."""
    st.set_page_config(
        page_title="Business Analysis Platform",
        page_icon="📊",
        layout="wide"
    )

    # Initialize components only once using session state
    if 'components' not in st.session_state:
        st.session_state.components = initialize_components()

    # Custom CSS
    st.markdown("""
        <style>
        .main {
            background-color: #f5f5f5;
        }
        .sidebar .sidebar-content {
            background-color: #e0e0e0;
        }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar
    st.sidebar.title("System Status")
    st.sidebar.info("System is running smoothly.")
    st.sidebar.title("Configuration")
    use_self_correction = st.sidebar.checkbox("Use Self-Correction", value=True)
    use_knowledge_base = st.sidebar.checkbox("Use Knowledge Base", value=True)

    # Header
    st.title("🚀 Business Analysis Platform")
    st.markdown("*Powered by LAMBDA-inspired AI Building Blocks*")
    st.markdown("---")

    # ===============================================================
    # DATA UPLOAD AND PREVIEW SECTION
    # ===============================================================
    st.header("📁 Data Source Selection")
    st.markdown("*Upload your data or use sample datasets*")
    
    # Data source selection
    data_source = st.radio(
        "Choose Data Source",
        ["Upload File", "Sample Data"],
        horizontal=True,
        help="Upload your own data file or use pre-built sample datasets"
    )
    
    data = None
    
    # File Upload Section
    if data_source == "Upload File":
        uploaded_file = st.file_uploader(
            "Choose a file", 
            type=["csv", "xlsx"],
            help="Upload CSV or Excel files"
        )
        
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    data = pd.read_csv(uploaded_file, parse_dates=False)
                else:
                    data = pd.read_excel(uploaded_file)
                
                # Convert any datetime columns to strings for better handling
                for col in data.columns:
                    if data[col].dtype == 'datetime64[ns]':
                        data[col] = data[col].dt.strftime('%Y-%m-%d')
                
                st.success(f"✅ File uploaded successfully: {uploaded_file.name}")
                
            except Exception as e:
                st.error(f"❌ Error uploading file: {e}")
                return
    
    # Sample Data Section
    else:
        st.subheader("📊 Sample Datasets")
        sample_type = st.selectbox(
            "Select Sample Data Type", 
            ["Marketing Campaign", "E-commerce", "SaaS Metrics", "Retail Sales", "Finance"]
        )
        
        # Generate sample data based on selection
        if sample_type == "Marketing Campaign":
            data = pd.DataFrame({
                'campaign_name': ['Social Media', 'Email Campaign', 'PPC', 'Display Ads', 'Content Marketing'],
                'campaign_spend': [5000, 3000, 7000, 4000, 2500],
                'impressions': [50000, 25000, 75000, 40000, 20000],
                'clicks': [2500, 1500, 3750, 2000, 1000],
                'conversions': [250, 150, 375, 200, 100],
                'revenue': [15000, 9000, 22500, 12000, 6000],
                'date': pd.date_range('2024-01-01', periods=5).strftime('%Y-%m-%d')
            })
        elif sample_type == "E-commerce":
            data = pd.DataFrame({
                'date': pd.date_range('2024-01-01', periods=30).strftime('%Y-%m-%d'),
                'sales': np.random.randint(1000, 5000, 30),
                'customers': np.random.randint(100, 500, 30),
                'website_visits': np.random.randint(1000, 10000, 30),
                'conversion_rate': np.random.uniform(0.01, 0.1, 30),
                'cart_abandonment_rate': np.random.uniform(0.3, 0.8, 30),
                'average_order_value': np.random.uniform(50, 200, 30)
            })
        elif sample_type == "SaaS Metrics":
            data = pd.DataFrame({
                'date': pd.date_range('2024-01-01', periods=30).strftime('%Y-%m-%d'),
                'mrr': np.random.randint(10000, 50000, 30),
                'churn_rate': np.random.uniform(0.01, 0.05, 30),
                'new_customers': np.random.randint(50, 200, 30),
                'customer_lifetime_value': np.random.randint(500, 2000, 30),
                'customer_acquisition_cost': np.random.randint(50, 300, 30)
            })
        elif sample_type == "Retail Sales":
            data = pd.DataFrame({
                'date': pd.date_range('2024-01-01', periods=30).strftime('%Y-%m-%d'),
                'daily_sales': np.random.randint(5000, 15000, 30),
                'inventory_level': np.random.randint(100, 1000, 30),
                'foot_traffic': np.random.randint(200, 1000, 30),
                'customer_satisfaction': np.random.uniform(3.5, 5.0, 30),
                'region': np.random.choice(['North', 'South', 'East', 'West'], 30)
            })
        else:  # Finance
            data = pd.DataFrame({
                'date': pd.date_range('2024-01-01', periods=30).strftime('%Y-%m-%d'),
                'revenue': np.random.randint(100000, 500000, 30),
                'expenses': np.random.randint(50000, 300000, 30),
                'profit_margin': np.random.uniform(0.1, 0.3, 30),
                'cash_flow': np.random.randint(-50000, 100000, 30),
                'roi': np.random.uniform(0.05, 0.25, 30)
            })
        
        st.success(f"✅ Sample data loaded: {sample_type}")
    
    # Data Preview Section
    if data is not None:
        st.markdown("---")
        st.header("🔍 Data Preview")
        
        tab1, tab2, tab3 = st.tabs(["📋 Sample Data", "📊 Summary", "🔢 Data Info"])
        
        with tab1:
            st.dataframe(data.head(10), use_container_width=True)
            st.caption(f"Showing first 10 rows of {len(data)} total records")
        
        with tab2:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Rows", len(data))
            with col2:
                st.metric("Total Columns", len(data.columns))
            with col3:
                numeric_cols = data.select_dtypes(include=[np.number]).columns
                st.metric("Numeric Columns", len(numeric_cols))
            with col4:
                missing_data = data.isnull().sum().sum()
                st.metric("Missing Values", missing_data)
        
        with tab3:
            st.text("Column Information:")
            for col in data.columns:
                dtype = str(data[col].dtype)
                null_count = data[col].isnull().sum()
                st.text(f"  {col}: {dtype} ({null_count} nulls)")

        # ===============================================================
        # TEMPLATE SELECTION SYSTEM
        # ===============================================================
        st.markdown("---")
        st.header("🚀 Quick Start Templates")
        st.markdown("*Choose from pre-built analysis templates or create custom analysis*")
        
        # Template selection interface
        col1, col2 = st.columns([1, 1])
        
        with col1:
            template_mode = st.radio(
                "Analysis Mode",
                ["Use Template", "Custom Analysis"],
                help="Templates provide pre-configured analysis workflows for specific use cases"
            )
        
        selected_template = None
        template_compatibility = None
        
        if template_mode == "Use Template":
            with col2:
                # Get orchestrator for template access
                orchestrator = st.session_state.components['orchestrator']
                
                # Department filter
                available_templates = orchestrator.template_manager.list_templates()
                departments = ['all'] + list(set(t.department for t in available_templates))
                selected_dept = st.selectbox("Filter by Department", departments)
                
                # Get templates for selected department
                if selected_dept == 'all':
                    filtered_templates = available_templates
                else:
                    filtered_templates = [t for t in available_templates if t.department == selected_dept]
                
                # Template selection
                if filtered_templates:
                    template_options = {f"{t.name} ({t.department})": t.id for t in filtered_templates}
                    
                    selected_template_name = st.selectbox(
                        "Select Template",
                        options=list(template_options.keys()),
                        help="Choose a pre-built template that matches your analysis needs"
                    )
                    
                    if selected_template_name:
                        template_id = template_options[selected_template_name]
                        selected_template = orchestrator.template_manager.get_template(template_id)
                        
                        # Display template information
                        with st.expander("📋 Template Details", expanded=True):
                            st.write(f"**Description:** {selected_template.description}")
                            st.write(f"**Department:** {selected_template.department.title()}")
                            st.write(f"**Industry Tags:** {', '.join(selected_template.industry_tags)}")
                            st.write(f"**Required Columns:** {', '.join(selected_template.required_columns)}")
                            if selected_template.optional_columns:
                                st.write(f"**Optional Columns:** {', '.join(selected_template.optional_columns)}")
                            
                            # Show sample question
                            st.markdown("**Sample Question:**")
                            st.info(selected_template.sample_question)
                        
                        # Template compatibility check
                        template_compatibility = orchestrator.template_manager.validate_template_compatibility(
                            selected_template, 
                            list(data.columns)
                        )
                        
                        st.subheader("📊 Data Compatibility Analysis")
                        
                        col_comp1, col_comp2 = st.columns(2)
                        with col_comp1:
                            compatibility_score = template_compatibility['compatibility_score']
                            st.metric(
                                "Compatibility Score", 
                                f"{compatibility_score:.1%}",
                                delta=None
                            )
                            
                            # Show compatibility status
                            if compatibility_score >= 0.9:
                                st.success("✅ Excellent compatibility!")
                            elif compatibility_score >= 0.7:
                                st.warning("⚠️ Good compatibility with minor issues")
                            else:
                                st.error("❌ Poor compatibility - data mapping required")
                        
                        with col_comp2:
                            # Show required vs available columns
                            st.write("**Column Status:**")
                            for col in selected_template.required_columns:
                                if col in data.columns:
                                    st.success(f"✅ {col} (found)")
                                else:
                                    st.error(f"❌ {col} (missing)")
                                    
                                    # Show suggestion if available
                                    if col in template_compatibility['suggestions']:
                                        suggested = template_compatibility['suggestions'][col]
                                        st.info(f"💡 Suggestion: Map '{suggested}' to '{col}'")
                        
                        # Show optional columns that are available
                        available_optional = [col for col in selected_template.optional_columns if col in data.columns]
                        if available_optional:
                            st.write("**Available Optional Columns:**")
                            for col in available_optional:
                                st.success(f"✅ {col} (enhances analysis)")
                else:
                    st.warning("No templates available for selected department")
            
            # Visual workflow display
            if selected_template:
                st.subheader("🔄 Analysis Workflow Preview")
                
                # Create workflow visualization
                workflow_steps = selected_template.workflow_steps
                
                for i, step in enumerate(workflow_steps):
                    step_name = step.get('name', f"Step {i+1}")
                    block_type = step.get('type', 'unknown')
                    
                    # Create step card
                    with st.container():
                        step_col1, step_col2, step_col3 = st.columns([0.5, 3, 0.5])
                        
                        with step_col1:
                            st.markdown(f"**{i+1}**")
                        
                        with step_col2:
                            # Color-code by block type
                            if 'validator' in block_type:
                                st.info(f"🔍 **{step_name}** - Data Validation")
                            elif 'kpi' in block_type:
                                st.success(f"📊 **{step_name}** - KPI Calculation")
                            elif 'alert' in block_type:
                                st.warning(f"🚨 **{step_name}** - Alert Generation")
                            else:
                                st.info(f"⚙️ **{step_name}** - {block_type.title().replace('_', ' ')}")
                        
                        with step_col3:
                            if i < len(workflow_steps) - 1:
                                st.markdown("⬇️")
        else:
            # Custom analysis mode
            st.info("💭 Enter your custom business question below for flexible analysis")
            
            # Show suggested templates for custom analysis
            if data is not None:
                with col2:
                    st.markdown("**Template Suggestions:**")
                    st.caption("Based on your data columns, these templates might be helpful:")
                    
                    # Simple template suggestions based on column names
                    data_columns = data.columns.tolist()
                    orchestrator = st.session_state.components['orchestrator']
                    
                    # Show top 3 suggestions
                    suggestions = orchestrator.suggest_templates("general analysis", data_columns)
                    
                    for i, suggestion in enumerate(suggestions[:3]):
                        template_info = suggestion['template']
                        compatibility_score = suggestion['compatibility_score']
                        
                        with st.container():
                            st.markdown(f"**{i+1}. {template_info['name']}**")
                            st.caption(f"Department: {template_info['department']} | Compatibility: {compatibility_score:.1%}")

        # ===============================================================
        # BUSINESS QUESTION INPUT
        # ===============================================================
        st.markdown("---")
        st.header("❓ Business Question")
        
        # Use template question if available, otherwise custom input
        if template_mode == "Use Template" and selected_template:
            default_question = selected_template.sample_question
            if 'template_question' in st.session_state and st.session_state.template_question != default_question:
                default_question = st.session_state.template_question
        else:
            default_question = ""
        
        question = st.text_area(
            "Enter your business question:",
            value=default_question,
            height=100,
            help="Enter a specific business question about your data. Templates provide sample questions you can customize.",
            key="business_question"
        )
        
        # Question validation
        if question:
            if template_mode == "Use Template" and selected_template:
                st.success(f"✓ Using template: {selected_template.name}")
            else:
                st.success(f"✓ Question entered: {question[:50]}...")
        else:
            st.warning("Please enter a business question to analyze")
        
        # ===============================================================
        # ANALYSIS EXECUTION
        # ===============================================================
        st.markdown("---")
        st.header("🚀 Run Analysis")
        
        # Show analysis configuration
        if data is not None and question:
            analysis_config_col1, analysis_config_col2 = st.columns(2)
            
            with analysis_config_col1:
                if template_mode == "Use Template" and selected_template:
                    st.info(f"**Analysis Mode:** Template-Based")
                    st.write(f"**Template:** {selected_template.name}")
                    st.write(f"**Workflow Steps:** {len(selected_template.workflow_steps)}")
                    
                    # Show compatibility status
                    if template_compatibility:
                        comp_score = template_compatibility['compatibility_score']
                        if comp_score >= 0.9:
                            st.success(f"**Data Compatibility:** Excellent ({comp_score:.1%})")
                        elif comp_score >= 0.7:
                            st.warning(f"**Data Compatibility:** Good ({comp_score:.1%})")
                        else:
                            st.error(f"**Data Compatibility:** Poor ({comp_score:.1%})")
                else:
                    st.info(f"**Analysis Mode:** Custom Analysis")
                    
                    # Detect suggested templates for custom questions
                    orchestrator = st.session_state.components['orchestrator']
                    suggested_templates = orchestrator.suggest_templates(question, list(data.columns))
                    if suggested_templates:
                        best_template = suggested_templates[0]
                        st.write(f"**Suggested Template:** {best_template['template']['name']}")
                        st.write(f"**Compatibility:** {best_template['compatibility_score']:.1%}")
                        
                        # Offer to switch to template mode
                        if st.button("🔄 Switch to Suggested Template", key="switch_template"):
                            template_mode = "Use Template"
                            st.session_state.template_question = question
                            st.rerun()
            
            with analysis_config_col2:
                # Show data information
                st.write(f"**Data Shape:** {data.shape}")
                st.write(f"**Columns:** {len(data.columns)}")
                
                # Show industry detection
                orchestrator = st.session_state.components['orchestrator']
                detected_industry = orchestrator.business_agent.knowledge_base.detect_industry(question, list(data.columns))
                st.write(f"**Detected Industry:** {detected_industry.title()}")
                
                # Show analysis type
                analysis_type = orchestrator.business_agent.knowledge_base.detect_analysis_template(question)
                st.write(f"**Analysis Type:** {analysis_type.title()}")
            
            # Analysis button with different behavior based on mode
            button_col1, button_col2, button_col3 = st.columns([1, 2, 1])
            
            with button_col2:
                if template_mode == "Use Template" and selected_template:
                    # Check if template can be applied
                    can_apply = True
                    button_text = f"🚀 Run Analysis with {selected_template.name}"
                    
                    if template_compatibility and not template_compatibility['compatible']:
                        if template_compatibility['compatibility_score'] < 0.5:
                            can_apply = False
                            button_text = "❌ Template Incompatible - Missing Required Columns"
                        else:
                            button_text = f"⚠️ Run with {selected_template.name} (Missing columns will be mapped)"
                    
                    run_analysis = st.button(
                        button_text,
                        disabled=not can_apply,
                        use_container_width=True,
                        type="primary"
                    )
                else:
                    run_analysis = st.button(
                        "🚀 Run Custom Analysis",
                        use_container_width=True,
                        type="primary"
                    )
            
            # Analysis execution
            if run_analysis:
                # Show progress
                progress_container = st.container()
                with progress_container:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        # Progress simulation
                        progress_steps = [
                            (0, 20, "Initializing analysis engine..."),
                            (20, 40, "Loading building blocks..."),
                            (40, 60, "Processing data..."),
                            (60, 80, "Executing workflow..."),
                            (80, 95, "Generating insights..."),
                            (95, 100, "Finalizing results...")
                        ]
                        
                        for start, end, message in progress_steps:
                            status_text.text(message)
                            for i in range(start, end + 1):
                                progress_bar.progress(i)
                                time.sleep(0.02)
                        
                        # Get orchestrator
                        orchestrator = st.session_state.components['orchestrator']
                        
                        # Convert data to dictionary
                        data_dict = data.to_dict(orient='list')
                        
                        # Run analysis based on mode
                        if template_mode == "Use Template" and selected_template:
                            # Store analysis in session state for later access
                            st.session_state.analysis_result = asyncio.run(
                                orchestrator.analyze_with_template(
                                    question, 
                                    data_dict, 
                                    selected_template.id,
                                    auto_apply_template=True
                                )
                            )
                        else:
                            # Store analysis in session state for later access
                            st.session_state.analysis_result = asyncio.run(
                                orchestrator.analyze_business_question(
                                    question,
                                    data_dict,
                                    use_self_correction=use_self_correction,
                                    use_knowledge_base=use_knowledge_base,
                                    auto_suggest_templates=True
                                )
                            )
                        
                        # Clear progress indicators
                        progress_bar.empty()
                        status_text.empty()
                        
                        # Show success message
                        analysis_result = st.session_state.analysis_result
                        if analysis_result and 'error' not in analysis_result:
                            st.success("✅ Analysis completed successfully!")
                            
                            # Show execution summary
                            if 'template_used' in analysis_result:
                                template_name = analysis_result['template_used']['name']
                                st.info(f"📋 Applied template: **{template_name}**")
                            elif 'template_suggestions' in analysis_result:
                                suggestion_count = len(analysis_result['template_suggestions'])
                                st.info(f"💡 Found {suggestion_count} template suggestions for future use")
                            
                            # Show any warnings
                            if 'column_mappings' in analysis_result and analysis_result['column_mappings']:
                                st.warning("⚠️ Some columns were automatically mapped. Check results tab for details.")
                            
                            # Automatically scroll to results
                            st.balloons()
                            
                        else:
                            error_msg = analysis_result.get('error', 'Unknown error occurred') if analysis_result else 'Analysis failed'
                            st.error(f"❌ Analysis failed: {error_msg}")
                            
                    except Exception as e:
                        progress_bar.empty()
                        status_text.empty()
                        st.error(f"❌ Analysis failed with error: {str(e)}")
                        st.session_state.analysis_result = {'error': str(e)}

    # Continue with the rest of the implementation...

if __name__ == "__main__":
    # Comment this out temporarily
    # asyncio.run(async_main())
    
    # Force Streamlit mode
    main()

