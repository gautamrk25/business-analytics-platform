"""Base Building Block abstract class for the business analysis platform"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import logging

from src.utils.logger import get_logger

logger = get_logger(__name__)


class BuildingBlock(ABC):
    """Abstract base class for all building blocks in the business analysis platform.
    
    All building blocks must inherit from this class and implement the required
    abstract methods to ensure consistent interface across the system.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get the name of the building block.
        
        Returns:
            str: The unique name identifier for this building block
        """
        pass
    
    @property
    @abstractmethod
    def category(self) -> str:
        """Get the category of the building block.
        
        Returns:
            str: The category this block belongs to (e.g., 'data', 'analysis', 'visualization')
        """
        pass
    
    @abstractmethod
    async def execute(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the building block's main functionality.
        
        Args:
            data: Input data to process
            config: Configuration parameters for the execution
            
        Returns:
            Dict with the following structure:
            {
                "success": bool,  # Whether execution was successful
                "data": Any,     # The processed output data
                "errors": List[str]  # List of any errors encountered
            }
        """
        pass
    
    @abstractmethod
    def validate_input(self, data: Dict[str, Any]) -> List[str]:
        """Validate the input data before execution.
        
        Args:
            data: The input data to validate
            
        Returns:
            List of validation error messages (empty if validation passes)
        """
        pass
    
    @abstractmethod
    def get_config_schema(self) -> Dict[str, Any]:
        """Get the JSON schema for the configuration parameters.
        
        Returns:
            JSON schema defining the configuration structure and validation rules
        """
        pass
    
    def __str__(self) -> str:
        """String representation of the building block."""
        return f"{self.category}.{self.name}"
    
    def __repr__(self) -> str:
        """Detailed string representation for debugging."""
        return f"<{self.__class__.__name__}(name={self.name}, category={self.category})>"