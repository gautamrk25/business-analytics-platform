"""Edge case tests for Learning History Manager"""
import json
import pytest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch, mock_open

from src.utils.learning_history import LearningHistoryManager, OperationRecord


class TestLearningHistoryEdgeCases:
    """Test edge cases and error handling"""
    
    def test_save_history_error_handling(self, tmp_path):
        """Test save history with write errors"""
        with patch('src.utils.learning_history.ConfigManager') as mock_config:
            mock_config.return_value.get.return_value = str(tmp_path / "history.json")
            manager = LearningHistoryManager()
        
        # Add some operations
        manager.store_operation({
            "type": "test",
            "input": {},
            "result": {"success": True}
        })
        
        # Mock file write error
        with patch('builtins.open', side_effect=IOError("Permission denied")):
            manager.save_history()  # Should not raise, just log error
            # The method handles the exception internally
    
    def test_load_history_error_handling(self, tmp_path):
        """Test load history with read errors and invalid JSON"""
        history_file = tmp_path / "history.json"
        
        # Test with invalid JSON
        history_file.write_text("invalid json content")
        
        with patch('src.utils.learning_history.ConfigManager') as mock_config:
            mock_config.return_value.get.return_value = str(history_file)
            manager = LearningHistoryManager()
            
        # Should handle error gracefully and have empty history
        assert len(manager.history) == 0
    
    def test_suggest_fixes_no_fixes_found(self):
        """Test suggest fixes when no fixes are found"""
        with patch('src.utils.learning_history.ConfigManager') as mock_config:
            mock_config.return_value.get.return_value = "history.json"
            manager = LearningHistoryManager()
        
        # Add only errors
        manager.store_operation({
            "type": "column_mapping",
            "input": {"source": "bad_col"},
            "result": {"success": False, "error": "Column not found"}
        })
        
        suggestions = manager.suggest_fixes("Column not found")
        assert suggestions == []
    
    def test_create_suggestion_non_column_mapping(self):
        """Test create suggestion for non-column mapping operations"""
        with patch('src.utils.learning_history.ConfigManager') as mock_config:
            mock_config.return_value.get.return_value = "history.json"
            manager = LearningHistoryManager()
        
        error_record = OperationRecord(
            type="data_validation",
            input={"file": "test.csv"},
            result={"success": False},
            timestamp=datetime.utcnow(),
            success=False,
            error="Invalid format"
        )
        
        success_record = OperationRecord(
            type="data_validation",
            input={"file": "test2.csv"},
            result={"success": True},
            timestamp=datetime.utcnow(),
            success=True
        )
        
        # Should return None for non-column mapping
        suggestion = manager._create_suggestion(error_record, success_record, "Invalid format")
        assert suggestion is None
    
    def test_export_learnings_error_handling(self, tmp_path):
        """Test export learnings with write errors"""
        with patch('src.utils.learning_history.ConfigManager') as mock_config:
            mock_config.return_value.get.return_value = "history.json"
            manager = LearningHistoryManager()
        
        export_file = str(tmp_path / "readonly" / "export.json")
        
        # Try to export to non-existent directory
        manager.export_learnings(export_file)  # Should handle error gracefully
    
    def test_empty_history_operations(self):
        """Test operations on empty history"""
        with patch('src.utils.learning_history.ConfigManager') as mock_config:
            mock_config.return_value.get.return_value = "history.json"
            manager = LearningHistoryManager()
        
        # Test all methods with empty history
        assert manager.get_error_patterns() == {}
        assert manager.get_learned_mappings() == {}
        assert manager.get_statistics()['total_operations'] == 0
        assert manager.search_history() == []
        assert manager.get_recent_operations() == []
    
    def test_operation_record_edge_cases(self):
        """Test OperationRecord with edge cases"""
        # Test with None metadata
        record = OperationRecord(
            type="test",
            input={},
            result={},
            timestamp=datetime.utcnow(),
            success=True,
            error=None,
            metadata=None
        )
        
        record_dict = record.to_dict()
        assert record_dict['metadata'] is None
        
        # Test from_dict with missing optional fields
        minimal_dict = {
            'type': 'test',
            'input': {},
            'result': {},
            'timestamp': datetime.utcnow().isoformat(),
            'success': True
        }
        
        recreated = OperationRecord.from_dict(minimal_dict)
        assert recreated.error is None
        assert recreated.metadata is None