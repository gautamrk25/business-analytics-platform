"""Configuration management utilities"""
import os
import yaml
import logging
from pathlib import Path
from typing import Any, Dict, Optional, Union

logger = logging.getLogger(__name__)


class ConfigManager:
    """Central configuration management with dot-notation access"""
    
    def __init__(self, config_file: str = "config.yaml"):
        """Initialize ConfigManager with optional config file path
        
        Args:
            config_file: Path to configuration file (default: config.yaml)
        """
        self.config_file = config_file
        self._config: Dict[str, Any] = {}
        self.load_config()
    
    def load_config(self) -> Dict[str, Union[bool, Any, list]]:
        """Load configuration from YAML file
        
        Returns:
            Result dictionary with success status, data, and errors
        """
        errors = []
        config_path = Path.cwd() / self.config_file
        
        try:
            if config_path.exists():
                with open(config_path, 'r') as f:
                    self._config = yaml.safe_load(f) or {}
                logger.info(f"Configuration loaded from {config_path}")
            else:
                logger.warning(f"Config file not found: {config_path}")
                self._config = {}
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML in config file: {e}")
            errors.append(f"Invalid YAML: {e}")
            self._config = {}
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            errors.append(f"Error loading config: {e}")
            self._config = {}
        
        # Apply environment variable overrides
        self._apply_env_overrides()
        
        return {
            'success': True,
            'data': self._config,
            'errors': errors
        }
    
    def _apply_env_overrides(self) -> None:
        """Apply environment variable overrides to configuration"""
        prefix = "CONFIG_OVERRIDE_"
        
        for env_key, env_value in os.environ.items():
            if env_key.startswith(prefix):
                # Convert ENV_VAR_NAME to nested.config.key
                # Double underscore (__) represents a dot in the config key
                # Single underscore (_) is kept as underscore
                key_without_prefix = env_key[len(prefix):]
                
                # Replace double underscores with dots
                config_key = key_without_prefix.lower().replace('__', '.')
                
                # Convert string values to appropriate types
                try:
                    if env_value.lower() in ('true', 'false'):
                        value = env_value.lower() == 'true'
                    elif env_value.isdigit():
                        value = int(env_value)
                    elif '.' in env_value and env_value.replace('.', '').replace('-', '').isdigit():
                        value = float(env_value)
                    else:
                        value = env_value
                    
                    self._set_nested_value(config_key, value)
                except Exception as e:
                    logger.warning(f"Failed to apply env override {env_key}: {e}")
    
    def _set_nested_value(self, key: str, value: Any) -> None:
        """Set a nested value in the config using dot notation"""
        keys = key.split('.')
        current = self._config
        
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        current[keys[-1]] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation
        
        Args:
            key: Configuration key in dot notation (e.g., 'analysis_config.max_attempts')
            default: Default value if key doesn't exist
            
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        current = self._config
        
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return default
        
        return current
    
    def reload(self) -> None:
        """Reload configuration from file"""
        self.load_config()
        logger.info("Configuration reloaded")