"""Logging configuration and utilities"""
import logging
import logging.handlers
import os
import sys
from pathlib import Path
from typing import Optional

from src.utils.config import ConfigManager


# Global variable to track if logging has been set up
_logging_configured = False
# Global variable to prevent recursive setup
_setup_in_progress = False


def setup_logging() -> None:
    """Set up logging configuration based on config settings"""
    global _logging_configured, _setup_in_progress
    
    if _logging_configured or _setup_in_progress:
        return
    
    _setup_in_progress = True
    
    try:
        # Load configuration
        config = ConfigManager()
        
        # Get logging configuration
        log_level = config.get('logging.level', default='INFO')
        log_format = config.get('logging.format', 
                              default='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        console_output = config.get('logging.console_output', default=True)
        file_output = config.get('logging.file_output', default=None)
        file_output_enabled = config.get('logging.file_output_enabled', default=False)
        
        # Set up root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
        
        # Remove existing handlers to avoid duplicates
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Create formatter
        formatter = logging.Formatter(log_format)
        
        # Console handler
        if console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)
        
        # File handler
        if file_output_enabled and file_output:
            # Check if log rotation is enabled
            enable_rotation = config.get('logging.enable_rotation', default=False)
            
            if enable_rotation:
                # Rotating file handler
                max_bytes = config.get('logging.max_bytes', default=10*1024*1024)  # 10MB default
                backup_count = config.get('logging.backup_count', default=5)
                
                # Create log directory if it doesn't exist
                log_dir = Path(file_output).parent
                log_dir.mkdir(parents=True, exist_ok=True)
                
                file_handler = logging.handlers.RotatingFileHandler(
                    filename=file_output,
                    maxBytes=max_bytes,
                    backupCount=backup_count
                )
            else:
                # Simple file handler
                log_dir = Path(file_output).parent
                log_dir.mkdir(parents=True, exist_ok=True)
                
                file_handler = logging.FileHandler(file_output)
            
            file_handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        
        _logging_configured = True
    finally:
        _setup_in_progress = False


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a specific module
    
    Args:
        name: Name of the module/component requesting the logger
        
    Returns:
        Configured logger instance
    """
    # Ensure logging is set up
    setup_logging()
    
    # Return logger instance
    return logging.getLogger(name)


def reset_logging() -> None:
    """Reset logging configuration (mainly for testing)"""
    global _logging_configured, _setup_in_progress
    _logging_configured = False
    _setup_in_progress = False
    
    # Clear all handlers from root logger
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)


# Don't auto-initialize logging on import to avoid conflicts with tests