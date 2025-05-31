"""Data Validator Building Block for validating and fixing data according to defined rules"""
import re
import json
from typing import Dict, Any, List, Optional, Union
from copy import deepcopy

from src.building_blocks.base import BuildingBlock
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DataValidatorBlock(BuildingBlock):
    """Building block for validating and optionally fixing data based on configurable rules.
    
    This block can validate data types, check for required fields, enforce constraints,
    and automatically fix certain issues when configured to do so.
    """
    
    @property
    def name(self) -> str:
        """Get the name of this building block.
        
        Returns:
            str: The name 'data_validator'
        """
        return "data_validator"
    
    @property
    def category(self) -> str:
        """Get the category of this building block.
        
        Returns:
            str: The category 'data'
        """
        return "data"
    
    def validate_input(self, data: Dict[str, Any]) -> List[str]:
        """Validate that the input data has required structure.
        
        Args:
            data: The input data to validate
            
        Returns:
            List[str]: List of validation errors (empty if valid)
        """
        errors = []
        
        if not isinstance(data, dict):
            errors.append("Input must be a dictionary")
            return errors
        
        # Check if 'data' key exists
        if "data" not in data:
            errors.append("Missing 'data' key")
            return errors
            
        # Check if 'data' value is a dictionary
        if not isinstance(data["data"], dict):
            errors.append("'data' value must be a dictionary")
            
        return errors
    
    async def execute(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute data validation and optional auto-fixing.
        
        Args:
            data: The data to validate and potentially fix
            config: Configuration containing validation rules and auto_fix settings
            
        Returns:
            Dict[str, Any]: Result dict with success status, validated/fixed data, and any errors
        """
        try:
            logger.debug(f"Starting validation with auto_fix={config.get('auto_fix', False)}")
            
            # Extract data from input
            input_data = data.get("data", {})
            auto_fix = config.get("auto_fix", False)
            
            # Create a copy for processing
            output_data = deepcopy(input_data)
            
            errors = []
            
            # Store custom messages for this execution
            self._custom_messages = config.get("custom_messages", {})
            
            # Edge case: no data provided
            if not data and not config:
                logger.warning("No data or config provided")
                return {
                    "success": False,
                    "data": {},
                    "errors": ["Input must contain 'data' key"]
                }
            
            # Check required fields
            required_fields = config.get("required_fields", [])
            if required_fields:
                field_errors = self._check_required_fields(output_data, required_fields)
                if field_errors:
                    if auto_fix:
                        # Auto-fix by adding empty strings for missing fields
                        for field in required_fields:
                            if field not in output_data:
                                output_data[field] = ""
                    else:
                        errors.extend(field_errors)
            
            # Check data types
            field_types = config.get("field_types", {})
            if field_types:
                type_errors, fixed_data = self._check_data_types(output_data, field_types, auto_fix)
                if fixed_data:
                    output_data = fixed_data
                if type_errors:
                    errors.extend(type_errors)
            
            # Check null/empty values
            null_empty_errors = self._check_null_empty_values(output_data, config)
            if null_empty_errors:
                errors.extend(null_empty_errors)
            
            # Apply transformations
            transformations = config.get("transformations", {})
            if transformations and auto_fix:
                output_data = self._apply_transformations(output_data, transformations)
            
            # Apply validation rules
            validation_rules = config.get("validation_rules", {})
            if validation_rules:
                rule_errors = self._apply_validation_rules(output_data, validation_rules)
                if rule_errors:
                    errors.extend(rule_errors)
            
            # Construct result
            success = len(errors) == 0
            result_data = output_data if (success or auto_fix) else input_data
            
            logger.info(f"Validation completed: success={success}, errors_count={len(errors)}")
            if errors:
                logger.debug(f"Validation errors: {errors}")
            
            return {
                "success": success,
                "data": result_data,
                "errors": errors
            }
            
        except Exception as e:
            logger.error(f"Error during validation: {str(e)}")
            return {
                "success": False,
                "data": data.get("data", {}),
                "errors": [f"Validation error: {str(e)}"]
            }
    
    def get_config_schema(self) -> Dict[str, Any]:
        """Get the JSON schema for configuration validation.
        
        Returns:
            Dict[str, Any]: JSON schema for config validation
        """
        return {
            "type": "object",
            "properties": {
                "required_fields": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "field_types": {
                    "type": "object",
                    "additionalProperties": {"type": "string"}
                },
                "allow_null": {
                    "type": "boolean",
                    "default": True
                },
                "allow_empty": {
                    "type": "boolean", 
                    "default": True
                },
                "transformations": {
                    "type": "object",
                    "additionalProperties": {
                        "oneOf": [
                            {"type": "string"},
                            {"type": "array", "items": {"type": "string"}}
                        ]
                    }
                },
                "validation_rules": {
                    "type": "object",
                    "additionalProperties": {
                        "type": "object"
                    }
                },
                "auto_fix": {
                    "type": "boolean",
                    "default": False
                },
                "custom_messages": {
                    "type": "object",
                    "additionalProperties": {"type": "string"}
                }
            },
            "required": []
        }
    
    def _check_required_fields(self, data: Dict[str, Any], required_fields: List[str]) -> List[str]:
        """Check if all required fields are present, supporting dot notation for nested fields."""
        errors = []
        for field in required_fields:
            if '.' in field:
                # Handle nested fields with dot notation
                value = self._get_nested_value(data, field)
                if value is None:
                    errors.append(f"Required field '{field}' is missing")
            else:
                # Handle top-level fields
                if field not in data:
                    errors.append(f"Required field '{field}' is missing")
        return errors
    
    def _check_data_types(self, data: Dict[str, Any], field_types: Dict[str, str], 
                         auto_fix: bool) -> tuple[List[str], Optional[Dict[str, Any]]]:
        """Check and optionally fix data types."""
        errors = []
        fixed_data = None
        
        for field, expected_type in field_types.items():
            # Handle nested fields with dot notation
            if '.' in field:
                value = self._get_nested_value(data, field)
                if value is not None and not self._is_correct_type(value, expected_type):
                    if auto_fix:
                        converted = self._convert_type(value, expected_type)
                        if converted is not None:
                            if fixed_data is None:
                                fixed_data = deepcopy(data)
                            self._set_nested_value(fixed_data, field, converted)
                        else:
                            errors.append(f"Field '{field}' has incorrect type and cannot be converted")
                    else:
                        errors.append(f"Field '{field}' has incorrect type")
            else:
                # Handle top-level fields
                if field in data:
                    value = data[field]
                    if not self._is_correct_type(value, expected_type):
                        if auto_fix:
                            converted = self._convert_type(value, expected_type)
                            if converted is not None:
                                if fixed_data is None:
                                    fixed_data = deepcopy(data)
                                fixed_data[field] = converted
                            else:
                                errors.append(f"Field '{field}' has incorrect type and cannot be converted")
                        else:
                            errors.append(f"Field '{field}' has incorrect type")
        
        return errors, fixed_data
    
    def _check_null_empty_values(self, data: Dict[str, Any], config: Dict[str, Any]) -> List[str]:
        """Check for null and empty values based on configuration."""
        errors = []
        allow_null = config.get("allow_null", True)
        allow_empty = config.get("allow_empty", True)
        
        if not allow_null or not allow_empty:
            def check_value(field_path: str, value: Any):
                """Recursively check values in nested structures."""
                if not allow_null and value is None:
                    errors.append(f"Field '{field_path}' cannot be null")
                if not allow_empty and isinstance(value, str) and value == "":
                    errors.append(f"Field '{field_path}' cannot be empty")
                    
                # Recursively check nested dictionaries
                if isinstance(value, dict):
                    for sub_field, sub_value in value.items():
                        check_value(f"{field_path}.{sub_field}", sub_value)
            
            for field, value in data.items():
                check_value(field, value)
        
        return errors
    
    def _apply_transformations(self, data: Dict[str, Any], 
                              transformations: Dict[str, Union[str, List[str]]]) -> Dict[str, Any]:
        """Apply transformations to data fields, supporting dot notation for nested fields."""
        result = deepcopy(data)
        
        for field, transform in transformations.items():
            # Handle nested fields with dot notation
            if '.' in field:
                value = self._get_nested_value(result, field)
                if value is not None:
                    if isinstance(transform, list):
                        # Apply multiple transformations in sequence
                        for t in transform:
                            value = self._apply_single_transformation(value, t)
                    else:
                        value = self._apply_single_transformation(value, transform)
                    self._set_nested_value(result, field, value)
            else:
                # Handle top-level fields
                if field in result:
                    if isinstance(transform, list):
                        # Apply multiple transformations in sequence
                        value = result[field]
                        for t in transform:
                            value = self._apply_single_transformation(value, t)
                        result[field] = value
                    else:
                        result[field] = self._apply_single_transformation(result[field], transform)
        
        return result
    
    def _apply_single_transformation(self, value: Any, transform: str) -> Any:
        """Apply a single transformation to a value."""
        if not isinstance(value, str):
            logger.debug(f"Skipping {transform} transformation on non-string value")
            return value
            
        original_value = value
        
        if transform == "trim":
            value = value.strip()
        elif transform == "uppercase":
            value = value.upper()
        elif transform == "lowercase":
            value = value.lower()
        elif transform == "title_case":
            value = value.title()
        elif transform == "format_phone":
            # Basic phone formatting - extract digits and format
            digits = ''.join(filter(str.isdigit, value))
            if len(digits) == 10:
                value = f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
            else:
                # Return original if can't format
                logger.debug(f"Cannot format phone number: {value} (has {len(digits)} digits)")
                
        if value != original_value:
            logger.debug(f"Applied {transform}: '{original_value}' -> '{value}'")
            
        return value
    
    def _apply_validation_rules(self, data: Dict[str, Any], 
                               rules: Dict[str, Dict[str, Any]]) -> List[str]:
        """Apply validation rules to data with support for nested fields."""
        errors = []
        
        for field, field_rules in rules.items():
            # Handle nested fields with dot notation
            if '.' in field:
                value = self._get_nested_value(data, field)
            else:
                value = data.get(field)
                
            if value is not None:
                # Check pattern
                if "pattern" in field_rules:
                    pattern = field_rules["pattern"]
                    try:
                        if value is not None and not re.match(pattern, str(value)):
                            custom_key = f"{field}.pattern"
                            error_msg = self._custom_messages.get(custom_key, f"Invalid {field}")
                            errors.append(error_msg)
                    except re.error:
                        logger.warning(f"Invalid regex pattern for field {field}: {pattern}")
                
                # Check min/max for numbers
                if isinstance(value, (int, float)):
                    if "min" in field_rules and value < field_rules["min"]:
                        custom_key = f"{field}.min"
                        if field == "age" and value < 0:
                            # Special case for age validation
                            error_msg = self._custom_messages.get(custom_key, "Age cannot be negative")
                        else:
                            error_msg = self._custom_messages.get(custom_key, f"Field '{field}' must be positive")
                        errors.append(error_msg)
                    if "max" in field_rules and value > field_rules["max"]:
                        custom_key = f"{field}.max"
                        error_msg = self._custom_messages.get(custom_key, f"Field '{field}' exceeds maximum value")
                        errors.append(error_msg)
                
                # Check length for strings
                if isinstance(value, str):
                    if "min_length" in field_rules and len(value) < field_rules["min_length"]:
                        custom_key = f"{field}.min_length"
                        error_msg = self._custom_messages.get(custom_key, f"Field '{field}' is too short")
                        errors.append(error_msg)
                    if "max_length" in field_rules and len(value) > field_rules["max_length"]:
                        custom_key = f"{field}.max_length"
                        error_msg = self._custom_messages.get(custom_key, f"Field '{field}' is too long")
                        errors.append(error_msg)
            else:
                # Field doesn't exist - check if it's required by the rule
                if field_rules.get("required", False):
                    custom_key = f"{field}.required"
                    error_msg = self._custom_messages.get(custom_key, f"Field '{field}' is required")
                    errors.append(error_msg)
        
        return errors
    
    def _is_correct_type(self, value: Any, expected_type: str) -> bool:
        """Check if a value matches the expected type."""
        type_map = {
            "string": str,
            "number": (int, float),
            "integer": int,
            "float": float,
            "boolean": bool,
            "array": list,
            "object": dict
        }
        
        expected_classes = type_map.get(expected_type)
        if expected_classes is None:
            return True
            
        # Special handling for number type with strings
        if expected_type == "number" and isinstance(value, str):
            try:
                float(value)
                return False  # It's convertible, so wrong type
            except ValueError:
                pass
                
        return isinstance(value, expected_classes)
    
    def _convert_type(self, value: Any, target_type: str) -> Optional[Any]:
        """Convert a value to the target type if possible."""
        if value is None:
            return None
            
        try:
            if target_type == "string":
                if isinstance(value, bool):
                    return "True" if value else "False"
                return str(value)
            elif target_type == "number":
                if isinstance(value, str):
                    # Handle edge cases like "not a number"
                    try:
                        # First try to convert to int if it's a whole number
                        if '.' not in value:
                            return int(value)
                        else:
                            result = float(value)
                            # Return int if it's a whole number
                            if result.is_integer():
                                return int(result)
                            return result
                    except ValueError:
                        return None
                elif isinstance(value, bool):
                    return 1 if value else 0
                return float(value)
            elif target_type == "integer":
                if isinstance(value, str):
                    return int(float(value))
                return int(value)
            elif target_type == "float":
                return float(value)
            elif target_type == "boolean":
                if isinstance(value, str):
                    return value.lower() in ("true", "1", "yes", "on")
                return bool(value)
            elif target_type == "array":
                if isinstance(value, str):
                    # Try to parse JSON array
                    try:
                        result = json.loads(value)
                        return result if isinstance(result, list) else [value]
                    except json.JSONDecodeError:
                        return [value]
                return list(value) if hasattr(value, "__iter__") else [value]
            elif target_type == "object":
                if isinstance(value, str):
                    try:
                        result = json.loads(value)
                        return result if isinstance(result, dict) else {"value": value}
                    except json.JSONDecodeError:
                        return {"value": value}
                return dict(value) if hasattr(value, "items") else {"value": value}
        except (ValueError, TypeError) as e:
            logger.debug(f"Failed to convert {value} to {target_type}: {e}")
            
        return None
    
    def _get_nested_value(self, data: Dict[str, Any], path: str) -> Any:
        """Get a value from a nested path in the data structure."""
        parts = path.split(".")
        current = data
        
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
                
        return current
    
    def _set_nested_value(self, data: Dict[str, Any], path: str, value: Any) -> None:
        """Set a value at a nested path in the data structure (modifies data in-place)."""
        parts = path.split(".")
        current = data
        
        for i, part in enumerate(parts[:-1]):
            if part not in current:
                current[part] = {}
            elif not isinstance(current[part], dict):
                # If the existing value is not a dict, we can't set a nested value
                logger.warning(f"Cannot set nested value at {path}: {part} is not a dictionary")
                return
            current = current[part]
            
        current[parts[-1]] = value