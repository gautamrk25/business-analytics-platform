"""Tests for the Building Block Registry"""
import pytest
from typing import Dict, Any, List

from src.building_blocks.registry import BuildingBlockRegistry
from src.building_blocks.base import BuildingBlock


# Test implementation of a building block
class TestAnalysisBlock(BuildingBlock):
    """Test implementation of a building block for testing"""
    
    @property
    def name(self) -> str:
        return "test_analysis"
    
    @property
    def category(self) -> str:
        return "analysis"
    
    async def execute(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        result = {"processed": True, "input_count": len(data)}
        return {"success": True, "data": result, "errors": []}
    
    def validate_input(self, data: Dict[str, Any]) -> List[str]:
        errors = []
        if not isinstance(data, dict):
            errors.append("Input must be a dictionary")
        return errors
    
    def get_config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "threshold": {"type": "number", "default": 0.5}
            }
        }


class TestDataBlock(BuildingBlock):
    """Another test implementation for testing"""
    
    @property
    def name(self) -> str:
        return "test_data"
    
    @property
    def category(self) -> str:
        return "data"
    
    async def execute(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        return {"success": True, "data": {"cleaned": data}, "errors": []}
    
    def validate_input(self, data: Dict[str, Any]) -> List[str]:
        return []
    
    def get_config_schema(self) -> Dict[str, Any]:
        return {"type": "object", "properties": {}}


class TestBuildingBlockRegistry:
    """Test suite for BuildingBlockRegistry"""
    
    @pytest.fixture
    def registry(self):
        """Create a fresh registry for each test"""
        return BuildingBlockRegistry()
    
    def test_register_new_building_block(self, registry):
        """Test registering a new building block"""
        # Register a block
        registry.register(TestAnalysisBlock)
        
        # Verify it's registered
        assert "test_analysis" in registry.list_blocks()
        assert TestAnalysisBlock in registry._blocks.values()
    
    def test_create_block_instance(self, registry):
        """Test creating a block instance with configuration"""
        # Register a block
        registry.register(TestAnalysisBlock)
        
        # Create instance
        config = {"threshold": 0.8}
        block = registry.create_block("test_analysis", config)
        
        # Verify instance
        assert isinstance(block, TestAnalysisBlock)
        assert block.name == "test_analysis"
    
    def test_list_all_available_blocks(self, registry):
        """Test listing all available blocks"""
        # Start with empty registry
        assert registry.list_blocks() == []
        
        # Register multiple blocks
        registry.register(TestAnalysisBlock)
        registry.register(TestDataBlock)
        
        # List blocks
        blocks = registry.list_blocks()
        assert len(blocks) == 2
        assert "test_analysis" in blocks
        assert "test_data" in blocks
    
    def test_get_block_by_name(self, registry):
        """Test getting a block by name"""
        # Register blocks
        registry.register(TestAnalysisBlock)
        registry.register(TestDataBlock)
        
        # Get by name
        analysis_block = registry.get_block("test_analysis")
        data_block = registry.get_block("test_data")
        
        assert analysis_block == TestAnalysisBlock
        assert data_block == TestDataBlock
    
    def test_handle_unknown_block_error(self, registry):
        """Test error handling for unknown blocks"""
        # Try to get non-existent block
        with pytest.raises(KeyError) as exc_info:
            registry.get_block("non_existent")
        
        assert "Building block 'non_existent' not found" in str(exc_info.value)
        
        # Try to create non-existent block
        with pytest.raises(KeyError) as exc_info:
            registry.create_block("non_existent", {})
        
        assert "Building block 'non_existent' not found" in str(exc_info.value)
    
    def test_register_duplicate_block_error(self, registry):
        """Test error when registering duplicate blocks"""
        # Register first block
        registry.register(TestAnalysisBlock)
        
        # Try to register again
        with pytest.raises(ValueError) as exc_info:
            registry.register(TestAnalysisBlock)
        
        assert "Building block 'test_analysis' is already registered" in str(exc_info.value)
    
    def test_get_block_info(self, registry):
        """Test getting detailed block information"""
        # Register block
        registry.register(TestAnalysisBlock)
        
        # Get info
        info = registry.get_block_info("test_analysis")
        
        assert info["name"] == "test_analysis"
        assert info["category"] == "analysis"
        assert "config_schema" in info
        assert info["config_schema"]["type"] == "object"
    
    def test_list_blocks_by_category(self, registry):
        """Test listing blocks filtered by category"""
        # Register blocks in different categories
        registry.register(TestAnalysisBlock)
        registry.register(TestDataBlock)
        
        # List by category
        analysis_blocks = registry.list_blocks(category="analysis")
        data_blocks = registry.list_blocks(category="data")
        
        assert analysis_blocks == ["test_analysis"]
        assert data_blocks == ["test_data"]
    
    def test_validate_block_config(self, registry):
        """Test validating block configuration"""
        # Register block
        registry.register(TestAnalysisBlock)
        
        # Valid config
        valid_config = {"threshold": 0.7}
        assert registry.validate_config("test_analysis", valid_config) == []
        
        # Invalid config (wrong type)
        invalid_config = {"threshold": "not a number"}
        errors = registry.validate_config("test_analysis", invalid_config)
        assert len(errors) > 0
    
    def test_registry_singleton_pattern(self):
        """Test that registry can be used as singleton"""
        registry1 = BuildingBlockRegistry()
        registry2 = BuildingBlockRegistry()
        
        # They should be different instances by default
        assert registry1 is not registry2
        
        # But can share state if needed (this is optional behavior)
        registry1.register(TestAnalysisBlock)
        assert "test_analysis" not in registry2.list_blocks()
    
    def test_clear_registry(self, registry):
        """Test clearing all blocks from registry"""
        # Register blocks
        registry.register(TestAnalysisBlock)
        registry.register(TestDataBlock)
        
        # Clear registry
        registry.clear()
        
        # Verify empty
        assert registry.list_blocks() == []
    
    def test_block_metadata(self, registry):
        """Test storing and retrieving block metadata"""
        # Register block with metadata
        metadata = {"version": "1.0", "author": "test"}
        registry.register(TestAnalysisBlock, metadata=metadata)
        
        # Get metadata
        stored_metadata = registry.get_block_metadata("test_analysis")
        assert stored_metadata == metadata
    
    def test_discover_blocks_in_module(self, registry):
        """Test automatic discovery of blocks in a module"""
        import sys
        import types
        
        # Create a mock module with blocks
        mock_module = types.ModuleType("mock_blocks")
        mock_module.TestAnalysisBlock = TestAnalysisBlock
        mock_module.TestDataBlock = TestDataBlock
        mock_module.NotABlock = "something else"
        
        # Discover blocks
        registry.discover_blocks(mock_module)
        
        # Verify discovered
        assert "test_analysis" in registry.list_blocks()
        assert "test_data" in registry.list_blocks()
    
    def test_export_registry_config(self, registry):
        """Test exporting registry configuration"""
        # Register blocks
        registry.register(TestAnalysisBlock)
        registry.register(TestDataBlock)
        
        # Export config
        config = registry.export_config()
        
        assert "blocks" in config
        assert len(config["blocks"]) == 2
        assert any(b["name"] == "test_analysis" for b in config["blocks"])
        assert any(b["name"] == "test_data" for b in config["blocks"])
    
    def test_register_invalid_class(self, registry):
        """Test registering an invalid class that's not a BuildingBlock"""
        class NotABlock:
            pass
        
        with pytest.raises(TypeError) as exc_info:
            registry.register(NotABlock)
        
        assert "must be a subclass of BuildingBlock" in str(exc_info.value)
    
    def test_validate_config_complex_types(self, registry):
        """Test config validation with more complex types"""
        # Register block
        registry.register(TestAnalysisBlock)
        
        # Test with boolean type
        class BooleanBlock(BuildingBlock):
            @property
            def name(self) -> str:
                return "boolean_test"
            
            @property
            def category(self) -> str:
                return "test"
            
            async def execute(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
                return {"success": True, "data": {}, "errors": []}
            
            def validate_input(self, data: Dict[str, Any]) -> List[str]:
                return []
            
            def get_config_schema(self) -> Dict[str, Any]:
                return {
                    "type": "object",
                    "properties": {
                        "enabled": {"type": "boolean"},
                        "name": {"type": "string"}
                    }
                }
        
        registry.register(BooleanBlock)
        
        # Test boolean validation
        invalid_bool_config = {"enabled": "not a boolean"}
        errors = registry.validate_config("boolean_test", invalid_bool_config)
        assert len(errors) > 0
        assert "must be a boolean" in errors[0]
        
        # Test string validation
        invalid_string_config = {"name": 123}
        errors = registry.validate_config("boolean_test", invalid_string_config)
        assert len(errors) > 0
        assert "must be a string" in errors[0]