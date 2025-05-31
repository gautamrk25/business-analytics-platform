"""Tests for ConfigManager component"""
import pytest
import os
import yaml
from pathlib import Path
from unittest.mock import patch, mock_open

from src.utils.config import ConfigManager


class TestConfigManager:
    """Test suite for ConfigManager"""
    
    def test_load_from_config_yaml(self, tmp_path):
        """Test loading configuration from config.yaml file"""
        # Create test config file
        config_content = """
        analysis_config:
          max_attempts: 3
          timeout: 30
        
        models:
          default: "gpt-4"
          temperature: 0.7
        """
        config_file = tmp_path / "config.yaml"
        config_file.write_text(config_content)
        
        # Test loading
        with patch('pathlib.Path.cwd', return_value=tmp_path):
            config = ConfigManager()
            assert config.get('analysis_config.max_attempts') == 3
            assert config.get('models.default') == "gpt-4"
    
    def test_default_values(self):
        """Test providing default values when keys don't exist"""
        config = ConfigManager()
        
        # Test non-existent key with default
        assert config.get('non.existent.key', default='default_value') == 'default_value'
        
        # Test non-existent key without default should return None
        assert config.get('non.existent.key') is None
    
    def test_dot_notation_access(self, tmp_path):
        """Test accessing nested values using dot notation"""
        config_content = """
        level1:
          level2:
            level3:
              value: "deep_value"
        
        analysis_config:
          max_attempts: 5
          settings:
            verbose: true
        """
        config_file = tmp_path / "config.yaml"
        config_file.write_text(config_content)
        
        with patch('pathlib.Path.cwd', return_value=tmp_path):
            config = ConfigManager()
            
            # Test deep nested access
            assert config.get('level1.level2.level3.value') == "deep_value"
            
            # Test intermediate level access
            assert config.get('analysis_config.settings.verbose') is True
            
            # Test partial path returns dict
            result = config.get('analysis_config')
            assert isinstance(result, dict)
            assert result['max_attempts'] == 5
    
    def test_missing_config_file_handling(self):
        """Test graceful handling when config file is missing"""
        with patch('pathlib.Path.exists', return_value=False):
            config = ConfigManager()
            
            # Should not raise exception
            assert config.get('any.key', default='fallback') == 'fallback'
            
            # Should return None for non-existent keys
            assert config.get('missing.key') is None
    
    def test_invalid_yaml_handling(self, tmp_path):
        """Test handling of invalid YAML content"""
        invalid_yaml = "invalid: yaml: content:"
        config_file = tmp_path / "config.yaml"
        config_file.write_text(invalid_yaml)
        
        with patch('pathlib.Path.cwd', return_value=tmp_path):
            # Should not raise exception on initialization
            config = ConfigManager()
            
            # Should fallback to defaults
            assert config.get('any.key', default='default') == 'default'
    
    def test_reload_config(self, tmp_path):
        """Test reloading configuration from file"""
        # Initial config
        initial_content = "key: initial_value"
        config_file = tmp_path / "config.yaml"
        config_file.write_text(initial_content)
        
        with patch('pathlib.Path.cwd', return_value=tmp_path):
            config = ConfigManager()
            assert config.get('key') == 'initial_value'
            
            # Update config file
            updated_content = "key: updated_value"
            config_file.write_text(updated_content)
            
            # Reload and verify
            config.reload()
            assert config.get('key') == 'updated_value'
    
    def test_result_format_compliance(self):
        """Test that result format matches required structure"""
        config = ConfigManager()
        
        # Test successful operation
        result = config.load_config()
        assert isinstance(result, dict)
        assert 'success' in result
        assert 'data' in result
        assert 'errors' in result
        assert isinstance(result['errors'], list)
        
        # Test with missing file
        with patch('pathlib.Path.exists', return_value=False):
            result = config.load_config()
            assert result['success'] is True  # Should still succeed with empty config
            assert result['data'] == {}
            assert result['errors'] == []
    
    def test_environment_variables_override(self):
        """Test that environment variables can override config values"""
        # Mock a non-existent config file so we start with empty config
        with patch('pathlib.Path.exists', return_value=False), \
             patch.dict(os.environ, {'CONFIG_OVERRIDE_analysis_config__max_attempts': '10'}):
            config = ConfigManager()
            
            # Environment variable should override config file value
            # The double underscore is used to represent dots in nested keys
            assert config.get('analysis_config.max_attempts', default=3) == 10
    
    def test_type_conversions(self, tmp_path):
        """Test automatic type conversions for common data types"""
        config_content = """
        string_value: "text"
        int_value: 42
        float_value: 3.14
        bool_value: true
        list_value: [1, 2, 3]
        dict_value:
          nested: "value"
        """
        config_file = tmp_path / "config.yaml"
        config_file.write_text(config_content)
        
        with patch('pathlib.Path.cwd', return_value=tmp_path):
            config = ConfigManager()
            
            assert isinstance(config.get('string_value'), str)
            assert isinstance(config.get('int_value'), int)
            assert isinstance(config.get('float_value'), float)
            assert isinstance(config.get('bool_value'), bool)
            assert isinstance(config.get('list_value'), list)
            assert isinstance(config.get('dict_value'), dict)