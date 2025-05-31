"""Tests for the Base Building Block abstract class"""
import pytest
from abc import ABCMeta
from typing import Dict, Any, List

from src.building_blocks.base import BuildingBlock


class TestBuildingBlock:
    """Test suite for the abstract BuildingBlock class"""
    
    def test_building_block_is_abstract(self):
        """Test that BuildingBlock is an abstract class and cannot be instantiated"""
        with pytest.raises(TypeError) as exc_info:
            BuildingBlock()
        
        assert "Can't instantiate abstract class" in str(exc_info.value)
    
    def test_building_block_has_abstract_methods(self):
        """Test that BuildingBlock has all required abstract methods"""
        # Check that BuildingBlock has ABCMeta as metaclass
        assert isinstance(BuildingBlock, ABCMeta)
        
        # Check for specific abstract methods
        abstract_methods = BuildingBlock.__abstractmethods__
        expected_methods = {'name', 'category', 'execute', 'validate_input', 'get_config_schema'}
        
        assert expected_methods.issubset(abstract_methods)
    
    def test_concrete_implementation_required(self):
        """Test that subclasses must implement all abstract methods"""
        # Create a partial implementation (missing some abstract methods)
        class IncompleteBlock(BuildingBlock):
            @property
            def name(self) -> str:
                return "incomplete"
            
            @property
            def category(self) -> str:
                return "test"
            
            # Missing execute, validate_input, and get_config_schema
        
        # Should not be able to instantiate
        with pytest.raises(TypeError) as exc_info:
            IncompleteBlock()
        
        assert "Can't instantiate abstract class" in str(exc_info.value)
    
    def test_complete_implementation_works(self):
        """Test that a complete implementation can be instantiated"""
        # Create a complete implementation
        class CompleteBlock(BuildingBlock):
            @property
            def name(self) -> str:
                return "complete"
            
            @property
            def category(self) -> str:
                return "test"
            
            async def execute(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
                return {"success": True, "data": data, "errors": []}
            
            def validate_input(self, data: Dict[str, Any]) -> List[str]:
                return []
            
            def get_config_schema(self) -> Dict[str, Any]:
                return {"type": "object", "properties": {}}
        
        # Should be able to instantiate
        block = CompleteBlock()
        assert block.name == "complete"
        assert block.category == "test"
    
    def test_return_types_enforced(self):
        """Test that return types are properly defined for abstract methods"""
        class TestBlock(BuildingBlock):
            @property
            def name(self) -> str:
                return "test"
            
            @property
            def category(self) -> str:
                return "test"
            
            async def execute(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
                return {"success": True, "data": {}, "errors": []}
            
            def validate_input(self, data: Dict[str, Any]) -> List[str]:
                return []
            
            def get_config_schema(self) -> Dict[str, Any]:
                return {}
        
        block = TestBlock()
        
        # Test return types
        assert isinstance(block.name, str)
        assert isinstance(block.category, str)
        assert isinstance(block.validate_input({}), list)
        assert isinstance(block.get_config_schema(), dict)
    
    def test_execute_method_signature(self):
        """Test that execute method has correct signature"""
        import inspect
        import asyncio
        
        class TestBlock(BuildingBlock):
            @property
            def name(self) -> str:
                return "test"
            
            @property
            def category(self) -> str:
                return "test"
            
            async def execute(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
                return {"success": True, "data": data, "errors": []}
            
            def validate_input(self, data: Dict[str, Any]) -> List[str]:
                return []
            
            def get_config_schema(self) -> Dict[str, Any]:
                return {}
        
        block = TestBlock()
        
        # Check that execute is async
        assert asyncio.iscoroutinefunction(block.execute)
        
        # Check method signature
        sig = inspect.signature(block.execute)
        params = list(sig.parameters.keys())
        assert params == ['data', 'config']  # 'self' is not included in bound method signature
    
    def test_validate_input_method_signature(self):
        """Test that validate_input method has correct signature"""
        import inspect
        
        class TestBlock(BuildingBlock):
            @property
            def name(self) -> str:
                return "test"
            
            @property
            def category(self) -> str:
                return "test"
            
            async def execute(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
                return {"success": True, "data": data, "errors": []}
            
            def validate_input(self, data: Dict[str, Any]) -> List[str]:
                errors = []
                if not data:
                    errors.append("Data cannot be empty")
                return errors
            
            def get_config_schema(self) -> Dict[str, Any]:
                return {}
        
        block = TestBlock()
        
        # Check method signature
        sig = inspect.signature(block.validate_input)
        params = list(sig.parameters.keys())
        assert params == ['data']  # 'self' is not included in bound method signature
        
        # Test validation
        assert block.validate_input({}) == ["Data cannot be empty"]
        assert block.validate_input({"key": "value"}) == []
    
    def test_execute_result_format(self):
        """Test that execute method returns correct result format"""
        import asyncio
        
        class TestBlock(BuildingBlock):
            @property
            def name(self) -> str:
                return "test"
            
            @property
            def category(self) -> str:
                return "test"
            
            async def execute(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
                return {
                    "success": True,
                    "data": {"processed": data},
                    "errors": []
                }
            
            def validate_input(self, data: Dict[str, Any]) -> List[str]:
                return []
            
            def get_config_schema(self) -> Dict[str, Any]:
                return {}
        
        block = TestBlock()
        
        # Test execute result
        result = asyncio.run(block.execute({"input": "value"}, {}))
        
        assert "success" in result
        assert "data" in result
        assert "errors" in result
        assert isinstance(result["success"], bool)
        assert isinstance(result["data"], dict)
        assert isinstance(result["errors"], list)
    
    def test_config_schema_format(self):
        """Test that get_config_schema returns proper JSON schema format"""
        class TestBlock(BuildingBlock):
            @property
            def name(self) -> str:
                return "test"
            
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
                        "option1": {"type": "string"},
                        "option2": {"type": "number"}
                    },
                    "required": ["option1"]
                }
        
        block = TestBlock()
        schema = block.get_config_schema()
        
        assert schema["type"] == "object"
        assert "properties" in schema
        assert "option1" in schema["properties"]
        assert schema["properties"]["option1"]["type"] == "string"
        assert "required" in schema
        assert "option1" in schema["required"]
    
    def test_multiple_inheritance_support(self):
        """Test that BuildingBlock can be used with multiple inheritance"""
        class AnotherMixin:
            def additional_method(self):
                return "mixin"
        
        class MultiBlock(BuildingBlock, AnotherMixin):
            @property
            def name(self) -> str:
                return "multi"
            
            @property
            def category(self) -> str:
                return "test"
            
            async def execute(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
                return {"success": True, "data": {}, "errors": []}
            
            def validate_input(self, data: Dict[str, Any]) -> List[str]:
                return []
            
            def get_config_schema(self) -> Dict[str, Any]:
                return {}
        
        block = MultiBlock()
        assert block.name == "multi"
        assert block.additional_method() == "mixin"
    
    def test_string_representations(self):
        """Test __str__ and __repr__ methods"""
        class TestBlock(BuildingBlock):
            @property
            def name(self) -> str:
                return "test_name"
            
            @property
            def category(self) -> str:
                return "test_category"
            
            async def execute(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
                return {"success": True, "data": {}, "errors": []}
            
            def validate_input(self, data: Dict[str, Any]) -> List[str]:
                return []
            
            def get_config_schema(self) -> Dict[str, Any]:
                return {}
        
        block = TestBlock()
        
        # Test __str__
        assert str(block) == "test_category.test_name"
        
        # Test __repr__
        repr_str = repr(block)
        assert "TestBlock" in repr_str
        assert "name=test_name" in repr_str
        assert "category=test_category" in repr_str