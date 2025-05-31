"""Tests for Logger Setup component"""
import pytest
import logging
import os
import sys
from unittest.mock import patch, MagicMock
from io import StringIO

from src.utils.logger import setup_logging, get_logger
from src.utils.config import ConfigManager


class TestLoggerSetup:
    """Test suite for Logger setup and configuration"""
    
    @pytest.fixture
    def mock_config(self):
        """Mock ConfigManager with logging configuration"""
        config = MagicMock()
        config.get.side_effect = lambda key, default=None: {
            'logging.level': 'INFO',
            'logging.format': '[%(asctime)s] %(levelname)s - %(name)s - %(message)s',
            'logging.file_output': 'logs/app.log',
            'logging.console_output': True,
            'logging.file_output_enabled': True
        }.get(key, default)
        return config
    
    @pytest.fixture
    def capture_logs(self):
        """Capture log output for testing"""
        log_capture_string = StringIO()
        ch = logging.StreamHandler(log_capture_string)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(levelname)s - %(name)s - %(message)s')
        ch.setFormatter(formatter)
        
        # Get root logger
        logger = logging.getLogger()
        logger.addHandler(ch)
        logger.setLevel(logging.DEBUG)
        
        yield log_capture_string
        
        # Clean up
        logger.removeHandler(ch)
    
    def test_setup_logging_from_config(self, mock_config):
        """Test setting up logging based on configuration"""
        from src.utils.logger import reset_logging
        reset_logging()  # Clear any existing configuration
        
        with patch('src.utils.logger.ConfigManager', return_value=mock_config):
            setup_logging()
            
            # Verify ConfigManager was called with correct keys
            mock_config.get.assert_any_call('logging.level', default='INFO')
            mock_config.get.assert_any_call('logging.format', 
                default='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    
    def test_create_logger_instances_for_modules(self):
        """Test creating logger instances for different modules"""
        # Create loggers for different modules
        logger1 = get_logger('module1')
        logger2 = get_logger('module2')
        logger3 = get_logger('module1')  # Same module name
        
        # Verify logger instances
        assert logger1.name == 'module1'
        assert logger2.name == 'module2'
        assert logger1 is logger3  # Same logger instance for same module
    
    def test_handle_different_log_levels(self, capture_logs):
        """Test handling different log levels (DEBUG, INFO, WARNING, ERROR)"""
        logger = get_logger('test_module')
        
        # Set different log levels and test
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        
        log_contents = capture_logs.getvalue()
        assert "DEBUG - test_module - Debug message" in log_contents
        assert "INFO - test_module - Info message" in log_contents
        assert "WARNING - test_module - Warning message" in log_contents
        assert "ERROR - test_module - Error message" in log_contents
    
    def test_format_log_messages_consistently(self, mock_config):
        """Test that log messages are formatted consistently"""
        with patch('src.utils.logger.ConfigManager', return_value=mock_config):
            setup_logging()
            logger = get_logger('test_formatting')
            
            # Create a string handler to capture output
            log_capture_string = StringIO()
            ch = logging.StreamHandler(log_capture_string)
            ch.setLevel(logging.INFO)
            
            # Use the format from config
            formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(name)s - %(message)s')
            ch.setFormatter(formatter)
            logger.addHandler(ch)
            
            # Log a message
            logger.info("Test message")
            
            log_output = log_capture_string.getvalue()
            # Check format pattern (without checking exact timestamp)
            assert "INFO - test_formatting - Test message" in log_output
            assert "[20" in log_output  # Timestamp starts with [20xx
    
    def test_log_level_configuration(self, mock_config):
        """Test that log level is properly configured from config"""
        from src.utils.logger import reset_logging
        
        # Test different log levels
        test_levels = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR
        }
        
        for level_str, level_const in test_levels.items():
            reset_logging()  # Clear any existing configuration
            mock_config.get.side_effect = lambda key, default=None: {
                'logging.level': level_str,
            }.get(key, default)
            
            with patch('src.utils.logger.ConfigManager', return_value=mock_config):
                setup_logging()
                root_logger = logging.getLogger()
                # Check the root logger level was set correctly
                assert root_logger.level == level_const
    
    def test_file_output_configuration(self, mock_config, tmp_path):
        """Test file output configuration"""
        from src.utils.logger import reset_logging
        reset_logging()  # Clear any existing configuration
        
        log_file = tmp_path / "test.log"
        mock_config.get.side_effect = lambda key, default=None: {
            'logging.level': 'INFO',
            'logging.file_output': str(log_file),
            'logging.file_output_enabled': True
        }.get(key, default)
        
        with patch('src.utils.logger.ConfigManager', return_value=mock_config):
            setup_logging()
            logger = get_logger('file_test')
            logger.info("Test file output")
            
            # Force handlers to flush
            for handler in logger.handlers:
                handler.flush()
            
            # Check if log file was created
            assert log_file.exists()
            with open(log_file, 'r') as f:
                content = f.read()
                assert "Test file output" in content
    
    def test_console_output_configuration(self, mock_config):
        """Test console output configuration"""
        # Test with console output disabled
        mock_config.get.side_effect = lambda key, default=None: {
            'logging.level': 'INFO',
            'logging.console_output': False
        }.get(key, default)
        
        with patch('src.utils.logger.ConfigManager', return_value=mock_config):
            setup_logging()
            logger = get_logger('console_test')
            
            # Check that console handler is not added when disabled
            console_handlers = [h for h in logger.handlers 
                              if isinstance(h, logging.StreamHandler) 
                              and h.stream in (sys.stdout, sys.stderr)]
            assert len(console_handlers) == 0
    
    def test_logger_singleton_pattern(self):
        """Test that logger follows singleton pattern per module"""
        logger1 = get_logger('singleton_test')
        logger2 = get_logger('singleton_test')
        logger3 = get_logger('different_module')
        
        assert logger1 is logger2
        assert logger1 is not logger3
    
    def test_logger_inheritance(self):
        """Test logger inheritance and propagation"""
        parent_logger = get_logger('parent')
        child_logger = get_logger('parent.child')
        
        # Child logger should have parent logger as parent
        assert child_logger.parent.name == 'parent'
        
        # Test propagation
        assert child_logger.propagate is True
    
    def test_default_configuration(self):
        """Test logger setup with default configuration when config is missing"""
        with patch('src.utils.logger.ConfigManager') as mock_config_class:
            # Mock ConfigManager to return None for all keys
            mock_instance = MagicMock()
            mock_instance.get.return_value = None
            mock_config_class.return_value = mock_instance
            
            setup_logging()
            logger = get_logger('default_test')
            
            # Should still work with defaults
            assert logger is not None
            assert logger.name == 'default_test'
    
    def test_exception_logging(self):
        """Test exception logging with traceback"""
        logger = get_logger('exception_test')
        
        # Create a string handler to capture output
        log_capture_string = StringIO()
        ch = logging.StreamHandler(log_capture_string)
        ch.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(levelname)s - %(name)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
        try:
            raise ValueError("Test exception")
        except ValueError:
            logger.exception("An error occurred")
        
        log_output = log_capture_string.getvalue()
        assert "ERROR - exception_test - An error occurred" in log_output
        assert "ValueError: Test exception" in log_output
        assert "Traceback" in log_output
    
    def test_log_rotation_configuration(self, mock_config, tmp_path):
        """Test log rotation configuration"""
        from src.utils.logger import reset_logging
        reset_logging()  # Clear any existing configuration
        
        log_file = tmp_path / "rotating.log"
        mock_config.get.side_effect = lambda key, default=None: {
            'logging.file_output': str(log_file),
            'logging.file_output_enabled': True,
            'logging.max_bytes': 1024,
            'logging.backup_count': 3,
            'logging.enable_rotation': True
        }.get(key, default)
        
        with patch('src.utils.logger.ConfigManager', return_value=mock_config):
            setup_logging()
            root_logger = logging.getLogger()
            
            # Verify rotation handler is set up on root logger
            rotating_handlers = [h for h in root_logger.handlers 
                               if hasattr(h, 'maxBytes')]
            assert len(rotating_handlers) > 0
    
    def test_custom_formatter(self, mock_config):
        """Test custom log formatter from configuration"""
        custom_format = '%(levelname)s | %(name)s | %(message)s'
        mock_config.get.side_effect = lambda key, default=None: {
            'logging.format': custom_format,
            'logging.level': 'INFO'
        }.get(key, default)
        
        with patch('src.utils.logger.ConfigManager', return_value=mock_config):
            setup_logging()
            logger = get_logger('format_test')
            
            # Create a string handler to capture output
            log_capture_string = StringIO()
            ch = logging.StreamHandler(log_capture_string)
            ch.setLevel(logging.INFO)
            ch.setFormatter(logging.Formatter(custom_format))
            logger.addHandler(ch)
            
            logger.info("Custom format test")
            
            log_output = log_capture_string.getvalue()
            assert "INFO | format_test | Custom format test" in log_output

