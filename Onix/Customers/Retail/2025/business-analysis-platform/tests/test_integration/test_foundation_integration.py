"""Integration tests for foundation components"""
import pytest
import asyncio
import tempfile
import yaml
import os
from pathlib import Path
import logging
from typing import Dict, Any

from src.utils.config import ConfigManager
from src.utils.logger import get_logger, setup_logging, reset_logging
from src.building_blocks.registry import BuildingBlockRegistry
from src.building_blocks.data.data_validator import DataValidatorBlock


class TestFoundationIntegration:
    """Integration tests for foundation components working together"""
    
    @pytest.fixture
    def temp_config_file(self):
        """Create a temporary config file for testing"""
        config_data = {
            "logging": {
                "level": "DEBUG",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "console_output": True,
                "file_output": "test.log",
                "file_output_enabled": True
            },
            "analysis_config": {
                "max_attempts": 3,
                "timeout": 300
            },
            "data_validation": {
                "auto_fix": True,
                "default_rules": {
                    "email": {"pattern": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"}
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            yield f.name
        
        # Cleanup
        os.unlink(f.name)
        if os.path.exists("test.log"):
            os.unlink("test.log")
    
    def test_config_manager_loads_correctly(self, temp_config_file):
        """Test that ConfigManager loads configuration correctly"""
        # Create ConfigManager with test config
        config = ConfigManager(temp_config_file)
        
        # Verify configuration loaded
        assert config.get("logging.level") == "DEBUG"
        assert config.get("analysis_config.max_attempts") == 3
        assert config.get("data_validation.auto_fix") is True
        
        # Test nested access
        email_pattern = config.get("data_validation.default_rules.email.pattern")
        assert email_pattern is not None
        assert "@" in email_pattern
    
    def test_logger_uses_config_settings(self, temp_config_file, tmp_path):
        """Test that Logger uses ConfigManager settings"""
        import logging as log
        reset_logging()  # Clear any existing logging setup
        
        # Need to ensure the logger setup uses our temp config file
        # by creating a temporary config.yaml in the current directory
        import shutil
        import yaml
        
        # Read config to modify log location
        with open(temp_config_file, 'r') as f:
            config_data = yaml.safe_load(f)
        
        # Set log file to a test location
        log_file = tmp_path / "test.log"
        config_data["logging"]["file_output"] = str(log_file)
        
        # Write to local config.yaml
        with open("config.yaml", 'w') as f:
            yaml.dump(config_data, f)
        
        try:
            # Setup logging (should use the config.yaml we just created)
            setup_logging()
            
            # Get logger and test it
            logger = get_logger("test_module")
            
            # Verify logger level is DEBUG from config
            root_logger = logging.getLogger()
            assert root_logger.level == logging.DEBUG or any(h.level == logging.DEBUG for h in root_logger.handlers)
            
            # Test logging
            logger.debug("Debug message")
            logger.info("Info message")
            
            # Force flush
            for handler in logging.getLogger().handlers:
                handler.flush()
            
            # Check log file was created and contains our messages
            assert log_file.exists(), f"Log file not created at {log_file}"
            
            with open(log_file, 'r') as f:
                log_content = f.read()
                assert "Debug message" in log_content, f"Debug message not found in: {log_content}"
                assert "Info message" in log_content, f"Info message not found in: {log_content}"
                assert "test_module" in log_content, "Logger name not in log"
            
        finally:
            # Clean up
            if os.path.exists("config.yaml"):
                os.unlink("config.yaml")
    
    def test_registry_registration_and_creation(self):
        """Test that Registry can register and create Data Validator"""
        # Create registry
        registry = BuildingBlockRegistry()
        
        # Register Data Validator
        registry.register(DataValidatorBlock)
        
        # Verify registration
        assert "data_validator" in registry.list_blocks()
        assert registry.get_block("data_validator") == DataValidatorBlock
        
        # Create instance
        validator = registry.create_block("data_validator", {})
        assert isinstance(validator, DataValidatorBlock)
        assert validator.name == "data_validator"
        assert validator.category == "data"
    
    def test_data_validator_with_real_data(self):
        """Test Data Validator with real data scenarios"""
        validator = DataValidatorBlock()
        
        # Test case 1: Valid data
        valid_data = {
            "data": {
                "name": "John Doe",
                "email": "john@example.com",
                "age": 30
            }
        }
        
        config = {
            "required_fields": ["name", "email", "age"],
            "field_types": {
                "name": "string",
                "email": "string", 
                "age": "number"
            }
        }
        
        result = asyncio.run(validator.execute(valid_data, config))
        assert result["success"] is True
        assert len(result["errors"]) == 0
        
        # Test case 2: Invalid data with auto-fix
        invalid_data = {
            "data": {
                "name": "  Jane Doe  ",  # Needs trimming
                "email": "JANE@EXAMPLE.COM",  # Needs lowercase
                "age": "25"  # String instead of number
            }
        }
        
        fix_config = {
            "auto_fix": True,
            "field_types": {
                "age": "number"
            },
            "transformations": {
                "name": "trim",
                "email": "lowercase"
            }
        }
        
        result = asyncio.run(validator.execute(invalid_data, fix_config))
        assert result["success"] is True
        assert result["data"]["name"] == "Jane Doe"
        assert result["data"]["email"] == "jane@example.com"
        assert result["data"]["age"] == 25
    
    def test_full_workflow_integration(self, temp_config_file, tmp_path):
        """Test complete workflow from config to validation"""
        reset_logging()
        
        # Step 1: Load configuration
        config = ConfigManager(temp_config_file)
        auto_fix = config.get("data_validation.auto_fix")
        
        # Step 2: Setup logging by creating a local config file
        # Copy the temp config but modify the log file location
        import shutil
        import yaml
        
        # Read the original config
        with open(temp_config_file, 'r') as f:
            config_data = yaml.safe_load(f)
        
        # Update log file location
        log_file = tmp_path / "test.log"
        config_data["logging"]["file_output"] = str(log_file)
        
        # Write to local config.yaml
        with open("config.yaml", 'w') as f:
            yaml.dump(config_data, f)
        
        try:
            # Setup logging (will use the local config.yaml)
            setup_logging()
            
            logger = get_logger("integration_test")
            logger.info("Starting integration test")
            
            # Step 3: Create registry and register validator
            registry = BuildingBlockRegistry()
            registry.register(DataValidatorBlock)
            logger.info(f"Registered blocks: {registry.list_blocks()}")
            
            # Step 4: Create validator instance
            validator = registry.create_block("data_validator", {})
            
            # Step 5: Validate data using config settings
            test_data = {
                "data": {
                    "name": "Test User",
                    "email": "TEST@EXAMPLE.COM",
                    "age": "forty"  # Invalid type
                }
            }
            
            validation_config = {
                "auto_fix": auto_fix,
                "field_types": {
                    "age": "number"
                },
                "transformations": {
                    "email": "lowercase"
                }
            }
            
            result = asyncio.run(validator.execute(test_data, validation_config))
            
            # Verify results
            if auto_fix:
                assert result["data"]["email"] == "test@example.com"
            else:
                assert result["data"]["email"] == "TEST@EXAMPLE.COM"
            
            # Log results
            logger.info(f"Validation result: {result}")
            
            # Force handlers to flush
            for handler in logging.getLogger().handlers:
                handler.flush()
            
            # Verify logging worked - use the log file from tmp_path
            assert log_file.exists(), f"Log file not created at {log_file}"
            with open(log_file, "r") as f:
                log_content = f.read()
                assert "Starting integration test" in log_content
                assert "Validation result" in log_content
        
        finally:
            # Clean up
            if os.path.exists("config.yaml"):
                os.unlink("config.yaml")
    
    def test_error_handling_integration(self):
        """Test error handling across components"""
        # Test registry with invalid block
        registry = BuildingBlockRegistry()
        
        with pytest.raises(TypeError):
            registry.register("not a block class")
        
        # Test validator with invalid input
        validator = DataValidatorBlock()
        result = asyncio.run(validator.execute("invalid input", {}))
        assert result["success"] is False
        assert len(result["errors"]) > 0
        
        # Test config with missing file
        config = ConfigManager("non_existent.yaml")
        assert config.get("any_key") is None
    
    def test_performance_with_large_dataset(self):
        """Test performance with larger dataset"""
        validator = DataValidatorBlock()
        
        # Create large dataset
        large_data = {
            "data": {f"field_{i}": f"value_{i}" for i in range(1000)}
        }
        
        # Add some fields that need fixing
        large_data["data"]["email_1"] = "NEEDS@LOWERCASE.COM"
        large_data["data"]["number_1"] = "123"
        
        config = {
            "auto_fix": True,
            "field_types": {
                "number_1": "number"
            },
            "transformations": {
                "email_1": "lowercase"
            }
        }
        
        # Execute and measure time
        import time
        start_time = time.time()
        result = asyncio.run(validator.execute(large_data, config))
        execution_time = time.time() - start_time
        
        assert result["success"] is True
        assert result["data"]["email_1"] == "needs@lowercase.com"
        assert result["data"]["number_1"] == 123
        assert execution_time < 1.0  # Should complete within 1 second
    
    def test_component_isolation(self):
        """Test that components work independently"""
        # Test ConfigManager independently
        config = ConfigManager()
        assert config is not None
        
        # Test Logger independently
        logger = get_logger("test")
        assert logger is not None
        
        # Test Registry independently
        registry = BuildingBlockRegistry()
        assert registry.list_blocks() == []
        
        # Test DataValidator independently
        validator = DataValidatorBlock()
        schema = validator.get_config_schema()
        assert schema["type"] == "object"
    
    def test_concurrent_operations(self):
        """Test concurrent operations with async components"""
        validator = DataValidatorBlock()
        
        async def validate_dataset(data, config):
            return await validator.execute(data, config)
        
        async def run_concurrent_validations():
            datasets = [
                {"data": {"id": i, "value": str(i)}} for i in range(5)
            ]
            
            config = {
                "field_types": {"value": "number"},
                "auto_fix": True
            }
            
            # Run validations concurrently
            tasks = [validate_dataset(data, config) for data in datasets]
            results = await asyncio.gather(*tasks)
            
            return results
        
        results = asyncio.run(run_concurrent_validations())
        
        # Verify all succeeded
        assert len(results) == 5
        for i, result in enumerate(results):
            assert result["success"] is True
            assert result["data"]["value"] == i
    
    def test_learning_history_tracking(self, temp_config_file):
        """Test that operations can be tracked for learning history"""
        # This is a placeholder for future learning history implementation
        # For now, we'll track operations manually
        
        operations_log = []
        
        # Track config loading
        config = ConfigManager(temp_config_file)
        operations_log.append({
            "operation": "config_load",
            "status": "success",
            "config_file": temp_config_file
        })
        
        # Track validator creation
        validator = DataValidatorBlock()
        operations_log.append({
            "operation": "create_validator",
            "status": "success",
            "block_name": validator.name
        })
        
        # Track validation
        result = asyncio.run(validator.execute(
            {"data": {"test": "value"}}, 
            {}
        ))
        operations_log.append({
            "operation": "validate_data",
            "status": "success" if result["success"] else "failure",
            "errors": result.get("errors", [])
        })
        
        # Verify tracking
        assert len(operations_log) == 3
        assert all(op["status"] == "success" for op in operations_log)
    
    def test_cross_platform_compatibility(self, tmp_path):
        """Test that components work across different file systems"""
        # Create config in platform-agnostic way
        config_path = tmp_path / "test_config.yaml"
        config_data = {
            "logging": {
                "file_output": str(tmp_path / "test.log")
            }
        }
        
        with open(config_path, "w") as f:
            yaml.dump(config_data, f)
        
        # Test loading
        config = ConfigManager(str(config_path))
        log_path = config.get("logging.file_output")
        
        # Verify path handling
        assert Path(log_path).parent == tmp_path
    
    def test_graceful_degradation(self):
        """Test that system degrades gracefully when components fail"""
        # Test with invalid config
        config = ConfigManager("non_existent.yaml")
        
        # Should still work with defaults
        logger = get_logger("test")
        logger.info("This should work even without config")
        
        # Registry should work independently
        registry = BuildingBlockRegistry()
        registry.register(DataValidatorBlock)
        
        # Validator should work with minimal config
        validator = registry.create_block("data_validator", {})
        result = asyncio.run(validator.execute(
            {"data": {"test": "value"}}, 
            {}
        ))
        
        assert result["success"] is True