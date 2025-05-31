"""Building Block Registry for managing all available building blocks"""
import inspect
import logging
from typing import Dict, Type, List, Any, Optional

from src.building_blocks.base import BuildingBlock
from src.utils.logger import get_logger

logger = get_logger(__name__)


class BuildingBlockRegistry:
    """Registry for managing and accessing building blocks.
    
    This class provides a central location for registering, discovering,
    and instantiating building blocks in the system.
    """
    
    def __init__(self):
        """Initialize the registry with empty block collection"""
        self._blocks: Dict[str, Type[BuildingBlock]] = {}
        self._metadata: Dict[str, Dict[str, Any]] = {}
        logger.info("Initialized BuildingBlockRegistry")
    
    def register(self, block_class: Type[BuildingBlock], metadata: Optional[Dict[str, Any]] = None) -> None:
        """Register a new building block class.
        
        Args:
            block_class: The building block class to register
            metadata: Optional metadata about the block
            
        Raises:
            ValueError: If block is already registered
            TypeError: If block_class is not a subclass of BuildingBlock
        """
        if not inspect.isclass(block_class) or not issubclass(block_class, BuildingBlock):
            raise TypeError(f"{block_class} must be a subclass of BuildingBlock")
        
        # Create a temporary instance to get the name
        temp_instance = block_class()
        block_name = temp_instance.name
        
        if block_name in self._blocks:
            raise ValueError(f"Building block '{block_name}' is already registered")
        
        self._blocks[block_name] = block_class
        if metadata:
            self._metadata[block_name] = metadata
        
        logger.info(f"Registered building block: {block_name}")
    
    def create_block(self, name: str, config: Dict[str, Any]) -> BuildingBlock:
        """Create an instance of a registered building block.
        
        Args:
            name: Name of the block to create
            config: Configuration for the block
            
        Returns:
            Instance of the requested building block
            
        Raises:
            KeyError: If block name is not found
        """
        if name not in self._blocks:
            raise KeyError(f"Building block '{name}' not found")
        
        block_class = self._blocks[name]
        block_instance = block_class()
        
        logger.info(f"Created instance of building block: {name}")
        return block_instance
    
    def list_blocks(self, category: Optional[str] = None) -> List[str]:
        """List all registered building blocks.
        
        Args:
            category: Optional category filter
            
        Returns:
            List of block names
        """
        if category is None:
            return list(self._blocks.keys())
        
        # Filter by category
        filtered_blocks = []
        for name, block_class in self._blocks.items():
            instance = block_class()
            if instance.category == category:
                filtered_blocks.append(name)
        
        return filtered_blocks
    
    def get_block(self, name: str) -> Type[BuildingBlock]:
        """Get a building block class by name.
        
        Args:
            name: Name of the block
            
        Returns:
            The building block class
            
        Raises:
            KeyError: If block name is not found
        """
        if name not in self._blocks:
            raise KeyError(f"Building block '{name}' not found")
        
        return self._blocks[name]
    
    def get_block_info(self, name: str) -> Dict[str, Any]:
        """Get detailed information about a building block.
        
        Args:
            name: Name of the block
            
        Returns:
            Dictionary with block information
            
        Raises:
            KeyError: If block name is not found
        """
        if name not in self._blocks:
            raise KeyError(f"Building block '{name}' not found")
        
        block_class = self._blocks[name]
        instance = block_class()
        
        info = {
            "name": instance.name,
            "category": instance.category,
            "config_schema": instance.get_config_schema(),
            "class": block_class.__name__,
            "module": block_class.__module__
        }
        
        return info
    
    def validate_config(self, name: str, config: Dict[str, Any]) -> List[str]:
        """Validate configuration for a building block.
        
        Args:
            name: Name of the block
            config: Configuration to validate
            
        Returns:
            List of validation errors (empty if valid)
            
        Raises:
            KeyError: If block name is not found
        """
        if name not in self._blocks:
            raise KeyError(f"Building block '{name}' not found")
        
        # For now, just check basic type validation
        # In a real implementation, you'd use a JSON schema validator
        errors = []
        
        block_class = self._blocks[name]
        instance = block_class()
        schema = instance.get_config_schema()
        
        if "properties" in schema:
            for prop, prop_schema in schema["properties"].items():
                if prop in config:
                    # Basic type checking
                    expected_type = prop_schema.get("type")
                    value = config[prop]
                    
                    if expected_type == "number" and not isinstance(value, (int, float)):
                        errors.append(f"Property '{prop}' must be a number")
                    elif expected_type == "string" and not isinstance(value, str):
                        errors.append(f"Property '{prop}' must be a string")
                    elif expected_type == "boolean" and not isinstance(value, bool):
                        errors.append(f"Property '{prop}' must be a boolean")
        
        return errors
    
    def clear(self) -> None:
        """Clear all registered blocks from the registry."""
        self._blocks.clear()
        self._metadata.clear()
        logger.info("Cleared all blocks from registry")
    
    def get_block_metadata(self, name: str) -> Dict[str, Any]:
        """Get metadata for a building block.
        
        Args:
            name: Name of the block
            
        Returns:
            Metadata dictionary (empty if no metadata)
            
        Raises:
            KeyError: If block name is not found
        """
        if name not in self._blocks:
            raise KeyError(f"Building block '{name}' not found")
        
        return self._metadata.get(name, {})
    
    def discover_blocks(self, module) -> None:
        """Discover and register building blocks in a module.
        
        Args:
            module: Python module to search for blocks
        """
        for name, obj in inspect.getmembers(module):
            if (inspect.isclass(obj) and 
                issubclass(obj, BuildingBlock) and 
                obj is not BuildingBlock):
                try:
                    self.register(obj)
                    logger.info(f"Discovered and registered block: {obj}")
                except ValueError:
                    # Block already registered, skip
                    pass
    
    def export_config(self) -> Dict[str, Any]:
        """Export registry configuration.
        
        Returns:
            Dictionary with registry configuration
        """
        config = {
            "blocks": []
        }
        
        for name, block_class in self._blocks.items():
            instance = block_class()
            block_config = {
                "name": name,
                "category": instance.category,
                "class": block_class.__name__,
                "module": block_class.__module__,
                "metadata": self._metadata.get(name, {})
            }
            config["blocks"].append(block_config)
        
        return config