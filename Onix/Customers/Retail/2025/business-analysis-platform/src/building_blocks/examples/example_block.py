"""
Example building block demonstrating TDD implementation pattern.
This file shows the structure all new building blocks should follow.
"""
from typing import Dict, Any, List
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class BuildingBlock(ABC):
    """Abstract base class for all building blocks."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Unique name for the block."""
        pass
    
    @property
    @abstractmethod
    def category(self) -> str:
        """Category of the block (e.g., 'data', 'analysis', 'visualization')."""
        pass
    
    @abstractmethod
    async def execute(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the building block logic.
        
        Args:
            data: Input data for processing
            config: Configuration parameters
            
        Returns:
            Dict with 'success', 'data', and 'errors' keys
        """
        pass
    
    @abstractmethod
    def validate_input(self, data: Dict[str, Any]) -> List[str]:
        """
        Validate input data and return list of errors.
        
        Args:
            data: Input data to validate
            
        Returns:
            List of error messages (empty if valid)
        """
        pass
    
    @abstractmethod
    def get_config_schema(self) -> Dict[str, Any]:
        """
        Return JSON schema for configuration parameters.
        
        Returns:
            JSON schema dictionary
        """
        pass


class DataSummaryBlock(BuildingBlock):
    """
    Example building block that creates data summaries.
    This demonstrates the standard implementation pattern.
    """
    
    @property
    def name(self) -> str:
        return "data_summary"
    
    @property
    def category(self) -> str:
        return "analysis"
    
    async def execute(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute data summary analysis.
        
        Args:
            data: Input data containing 'dataset' key with list of values
            config: Configuration with optional 'include_stats' boolean
            
        Returns:
            Standard result dictionary with summary data
        """
        try:
            # Validate input
            errors = self.validate_input(data)
            if errors:
                return {'success': False, 'data': None, 'errors': errors}
            
            # Extract data
            dataset = data['dataset']
            include_stats = config.get('include_stats', True)
            
            # Create summary
            summary = {
                'count': len(dataset),
                'unique_values': len(set(dataset))
            }
            
            if include_stats and all(isinstance(x, (int, float)) for x in dataset):
                summary.update({
                    'min': min(dataset),
                    'max': max(dataset),
                    'mean': sum(dataset) / len(dataset)
                })
            
            logger.info(f"Data summary created successfully for {len(dataset)} items")
            
            return {
                'success': True,
                'data': {'summary': summary},
                'errors': []
            }
            
        except Exception as e:
            logger.error(f"DataSummaryBlock error: {str(e)}")
            return {
                'success': False,
                'data': None,
                'errors': [str(e)]
            }
    
    def validate_input(self, data: Dict[str, Any]) -> List[str]:
        """
        Validate that input contains required 'dataset' field.
        
        Args:
            data: Input data to validate
            
        Returns:
            List of validation errors
        """
        errors = []
        
        if 'dataset' not in data:
            errors.append("Missing required field: 'dataset'")
        elif not isinstance(data['dataset'], list):
            errors.append("'dataset' must be a list")
        elif len(data['dataset']) == 0:
            errors.append("'dataset' cannot be empty")
            
        return errors
    
    def get_config_schema(self) -> Dict[str, Any]:
        """
        Define configuration schema for the block.
        
        Returns:
            JSON schema for configuration options
        """
        return {
            'type': 'object',
            'properties': {
                'include_stats': {
                    'type': 'boolean',
                    'description': 'Include statistical summary for numeric data',
                    'default': True
                }
            }
        }