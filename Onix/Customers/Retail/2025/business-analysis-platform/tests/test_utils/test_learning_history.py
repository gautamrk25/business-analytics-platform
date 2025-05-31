"""Tests for Learning History Manager"""
import json
import os
import pytest
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch, mock_open

from src.utils.learning_history import LearningHistoryManager, OperationRecord


class TestLearningHistoryManager:
    """Test suite for Learning History Manager"""
    
    @pytest.fixture
    def temp_history_file(self, tmp_path):
        """Create a temporary history file for testing"""
        history_file = tmp_path / "test_history.json"
        return str(history_file)
    
    @pytest.fixture
    def manager(self, temp_history_file):
        """Create a LearningHistoryManager instance with temp file"""
        with patch('src.utils.learning_history.ConfigManager') as mock_config:
            mock_config.return_value.get.return_value = temp_history_file
            return LearningHistoryManager()
    
    def test_initialization(self):
        """Test Learning History Manager initialization"""
        with patch('src.utils.learning_history.ConfigManager') as mock_config:
            mock_config.return_value.get.return_value = "history.json"
            
            manager = LearningHistoryManager()
            
            assert manager.history_file == "history.json"
            assert isinstance(manager.history, list)
            assert len(manager.history) == 0
    
    def test_store_successful_operation(self, manager):
        """Test storing a successful operation"""
        operation = {
            "type": "column_mapping",
            "input": {"source": "user_name", "target": "username"},
            "result": {"success": True, "mapped_to": "username"},
            "metadata": {"confidence": 0.95}
        }
        
        manager.store_operation(operation)
        
        assert len(manager.history) == 1
        record = manager.history[0]
        assert record.type == "column_mapping"
        assert record.success is True
        assert record.input["source"] == "user_name"
        assert record.result["mapped_to"] == "username"
        assert isinstance(record.timestamp, datetime)
    
    def test_store_error_operation(self, manager):
        """Test storing an operation with error"""
        operation = {
            "type": "data_validation",
            "input": {"file": "data.csv", "column": "invalid_col"},
            "result": {"success": False, "error": "Column not found"},
            "metadata": {"line": 42}
        }
        
        manager.store_operation(operation)
        
        assert len(manager.history) == 1
        record = manager.history[0]
        assert record.type == "data_validation"
        assert record.success is False
        assert record.error == "Column not found"
        assert record.metadata["line"] == 42
    
    def test_track_error_patterns(self, manager):
        """Test tracking error patterns"""
        # Store multiple similar errors
        for i in range(3):
            operation = {
                "type": "data_validation",
                "input": {"file": f"file{i}.csv", "column": "missing_col"},
                "result": {
                    "success": False, 
                    "error": "Column 'missing_col' not found"
                }
            }
            manager.store_operation(operation)
        
        # Get error patterns
        patterns = manager.get_error_patterns()
        
        assert len(patterns) > 0
        assert "Column 'missing_col' not found" in patterns
        assert patterns["Column 'missing_col' not found"]["count"] == 3
        assert patterns["Column 'missing_col' not found"]["type"] == "data_validation"
    
    def test_save_history(self, manager, temp_history_file):
        """Test saving history to JSON file"""
        # Store some operations
        operation1 = {
            "type": "column_mapping",
            "input": {"source": "col1", "target": "column1"},
            "result": {"success": True}
        }
        operation2 = {
            "type": "data_validation",
            "input": {"file": "test.csv"},
            "result": {"success": False, "error": "Invalid format"}
        }
        
        manager.store_operation(operation1)
        manager.store_operation(operation2)
        
        # Save history
        manager.save_history()
        
        # Verify file was created and contains correct data
        with open(temp_history_file, 'r') as f:
            saved_data = json.load(f)
        
        assert len(saved_data) == 2
        assert saved_data[0]["type"] == "column_mapping"
        assert saved_data[1]["type"] == "data_validation"
        assert saved_data[1]["error"] == "Invalid format"
    
    def test_load_history(self, temp_history_file):
        """Test loading history from JSON file"""
        # Create test data
        test_history = [
            {
                "type": "column_mapping",
                "input": {"source": "src", "target": "dst"},
                "result": {"success": True},
                "timestamp": datetime.utcnow().isoformat(),
                "success": True
            },
            {
                "type": "data_validation",
                "input": {"file": "data.csv"},
                "result": {"success": False},
                "error": "File not found",
                "timestamp": datetime.utcnow().isoformat(),
                "success": False
            }
        ]
        
        # Write test data to file
        with open(temp_history_file, 'w') as f:
            json.dump(test_history, f)
        
        # Create manager and load history
        with patch('src.utils.learning_history.ConfigManager') as mock_config:
            mock_config.return_value.get.return_value = temp_history_file
            manager = LearningHistoryManager()
            manager.load_history()
        
        assert len(manager.history) == 2
        assert manager.history[0].type == "column_mapping"
        assert manager.history[1].error == "File not found"
    
    def test_suggest_fixes_based_on_errors(self, manager):
        """Test suggesting fixes based on past errors"""
        # Store some operations with errors and their fixes
        error_op = {
            "type": "column_mapping",
            "input": {"source": "usr_name", "target": "username"},
            "result": {"success": False, "error": "Column not found: usr_name"}
        }
        
        fix_op = {
            "type": "column_mapping",
            "input": {"source": "user_name", "target": "username"},
            "result": {"success": True, "mapped_to": "username"},
            "metadata": {"previous_error": "Column not found: usr_name"}
        }
        
        manager.store_operation(error_op)
        manager.store_operation(fix_op)
        
        # Get fix suggestions for similar error
        suggestions = manager.suggest_fixes("Column not found: usr_name")
        
        assert len(suggestions) > 0
        assert suggestions[0]["suggestion"] == "Try 'user_name' instead of 'usr_name'"
        assert suggestions[0]["confidence"] > 0
    
    def test_learn_column_mappings(self, manager):
        """Test learning column mappings from previous runs"""
        # Store successful column mappings
        mappings = [
            {
                "type": "column_mapping",
                "input": {"source": "cust_id", "target": "customer_id"},
                "result": {"success": True, "mapped_to": "customer_id"}
            },
            {
                "type": "column_mapping",
                "input": {"source": "prod_name", "target": "product_name"},
                "result": {"success": True, "mapped_to": "product_name"}
            },
            {
                "type": "column_mapping",
                "input": {"source": "cust_id", "target": "customer_id"},
                "result": {"success": True, "mapped_to": "customer_id"}
            }
        ]
        
        for mapping in mappings:
            manager.store_operation(mapping)
        
        # Get learned mappings
        learned = manager.get_learned_mappings()
        
        assert "cust_id" in learned
        assert learned["cust_id"]["target"] == "customer_id"
        assert learned["cust_id"]["confidence"] > learned["prod_name"]["confidence"]
    
    def test_get_operation_statistics(self, manager):
        """Test getting statistics about operations"""
        # Store various operations
        operations = [
            {"type": "column_mapping", "input": {}, "result": {"success": True}},
            {"type": "column_mapping", "input": {}, "result": {"success": False}},
            {"type": "data_validation", "input": {}, "result": {"success": True}},
            {"type": "data_validation", "input": {}, "result": {"success": True}},
            {"type": "data_validation", "input": {}, "result": {"success": False}}
        ]
        
        for op in operations:
            manager.store_operation(op)
        
        stats = manager.get_statistics()
        
        assert stats["total_operations"] == 5
        assert stats["success_rate"] == 0.6
        assert stats["by_type"]["column_mapping"]["total"] == 2
        assert stats["by_type"]["column_mapping"]["success_rate"] == 0.5
        assert stats["by_type"]["data_validation"]["success_rate"] == 2/3
    
    def test_clear_old_history(self, manager):
        """Test clearing old history entries"""
        # Store operations with different timestamps
        old_date = datetime(2020, 1, 1)
        recent_date = datetime.utcnow()
        
        old_op = {
            "type": "data_validation",
            "input": {"file": "old.csv"},
            "result": {"success": True},
            "timestamp": old_date,
            "success": True
        }
        
        recent_op = {
            "type": "data_validation",
            "input": {"file": "recent.csv"},
            "result": {"success": True},
            "timestamp": recent_date,
            "success": True
        }
        
        # Manually add operations with specific timestamps
        old_record = OperationRecord(**old_op)
        recent_record = OperationRecord(**recent_op)
        
        manager.history = [old_record, recent_record]
        
        # Clear history older than 30 days
        manager.clear_old_history(days=30)
        
        assert len(manager.history) == 1
        assert manager.history[0].input["file"] == "recent.csv"
    
    def test_export_learnings(self, manager, tmp_path):
        """Test exporting learned patterns to a file"""
        # Store some operations
        operations = [
            {
                "type": "column_mapping",
                "input": {"source": "id", "target": "user_id"},
                "result": {"success": True}
            },
            {
                "type": "data_validation",
                "input": {"file": "test.csv"},
                "result": {"success": False, "error": "Missing required columns"}
            }
        ]
        
        for op in operations:
            manager.store_operation(op)
        
        # Export learnings
        export_file = tmp_path / "learnings.json"
        manager.export_learnings(str(export_file))
        
        # Verify export
        with open(export_file, 'r') as f:
            learnings = json.load(f)
        
        assert "mappings" in learnings
        assert "error_patterns" in learnings
        assert "statistics" in learnings
    
    def test_thread_safety(self, manager):
        """Test thread-safe operations"""
        import threading
        
        def add_operations():
            for i in range(10):
                operation = {
                    "type": f"type_{i % 3}",
                    "input": {"id": i},
                    "result": {"success": i % 2 == 0}
                }
                manager.store_operation(operation)
        
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=add_operations)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Should have 50 operations without errors
        assert len(manager.history) == 50
    
    def test_search_history(self, manager):
        """Test searching through history"""
        # Store operations
        operations = [
            {
                "type": "column_mapping",
                "input": {"source": "user_id", "target": "id"},
                "result": {"success": True}
            },
            {
                "type": "column_mapping",
                "input": {"source": "product_id", "target": "id"},
                "result": {"success": True}
            },
            {
                "type": "data_validation",
                "input": {"file": "users.csv"},
                "result": {"success": False, "error": "Invalid user_id"}
            }
        ]
        
        for op in operations:
            manager.store_operation(op)
        
        # Search by type
        mapping_results = manager.search_history(operation_type="column_mapping")
        assert len(mapping_results) == 2
        
        # Search by input content
        user_results = manager.search_history(input_contains="user")
        assert len(user_results) == 2
        
        # Search by error
        error_results = manager.search_history(error_contains="Invalid")
        assert len(error_results) == 1
    
    def test_get_most_recent_operations(self, manager):
        """Test getting most recent operations"""
        # Store operations
        for i in range(10):
            operation = {
                "type": f"type_{i}",
                "input": {"id": i},
                "result": {"success": True}
            }
            manager.store_operation(operation)
        
        # Get most recent 5
        recent = manager.get_recent_operations(limit=5)
        
        assert len(recent) == 5
        assert recent[0].input["id"] == 9  # Most recent
        assert recent[4].input["id"] == 5  # 5th most recent