"""Learning History Manager for tracking and learning from past operations"""
import json
import logging
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional
from collections import defaultdict
from dataclasses import dataclass, asdict

from src.utils.config import ConfigManager

logger = logging.getLogger(__name__)


@dataclass
class OperationRecord:
    """Record of a single operation"""
    type: str
    input: Dict[str, Any]
    result: Dict[str, Any]
    timestamp: datetime
    success: bool
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['timestamp'] = data['timestamp'].isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OperationRecord':
        """Create from dictionary (JSON deserialization)"""
        data = data.copy()
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)


class LearningHistoryManager:
    """Manages learning history from past operations"""
    
    def __init__(self):
        """Initialize the Learning History Manager"""
        self.config = ConfigManager()
        self.history_file = self.config.get(
            'learning_history.file', 
            default='learning_history.json'
        )
        self.history: List[OperationRecord] = []
        self._lock = threading.Lock()
        self.load_history()
    
    def store_operation(self, operation: Dict[str, Any]) -> None:
        """Store an operation in history"""
        with self._lock:
            # Extract success and error from result if not provided
            success = operation.get('success', operation.get('result', {}).get('success', False))
            error = operation.get('error', operation.get('result', {}).get('error'))
            
            record = OperationRecord(
                type=operation['type'],
                input=operation['input'],
                result=operation['result'],
                timestamp=operation.get('timestamp', datetime.utcnow()),
                success=success,
                error=error,
                metadata=operation.get('metadata')
            )
            
            self.history.append(record)
            logger.info(f"Stored operation: {record.type} - Success: {record.success}")
    
    def get_error_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Analyze and return error patterns from history"""
        patterns = defaultdict(lambda: {'count': 0, 'type': None, 'examples': []})
        
        for record in self.history:
            if not record.success and record.error:
                patterns[record.error]['count'] += 1
                patterns[record.error]['type'] = record.type
                patterns[record.error]['examples'].append(record.input)
        
        return dict(patterns)
    
    def save_history(self) -> None:
        """Save history to JSON file"""
        try:
            with self._lock:
                history_data = [record.to_dict() for record in self.history]
                
            with open(self.history_file, 'w') as f:
                json.dump(history_data, f, indent=2)
            
            logger.info(f"Saved {len(history_data)} operations to {self.history_file}")
        except Exception as e:
            logger.error(f"Failed to save history: {e}")
    
    def load_history(self) -> None:
        """Load history from JSON file"""
        try:
            history_path = Path(self.history_file)
            if history_path.exists():
                with open(history_path, 'r') as f:
                    history_data = json.load(f)
                
                with self._lock:
                    self.history = [
                        OperationRecord.from_dict(data) 
                        for data in history_data
                    ]
                
                logger.info(f"Loaded {len(self.history)} operations from {self.history_file}")
        except Exception as e:
            logger.error(f"Failed to load history: {e}")
            self.history = []
    
    def suggest_fixes(self, error_message: str) -> List[Dict[str, Any]]:
        """Suggest fixes based on past errors and successful operations"""
        suggestions = []
        
        # Find similar errors and their subsequent fixes
        for i, record in enumerate(self.history):
            if (not record.success and record.error and 
                error_message in record.error):
                
                # Look for successful operations after this error
                for j in range(i + 1, min(i + 5, len(self.history))):
                    next_record = self.history[j]
                    
                    if (next_record.success and 
                        next_record.type == record.type):
                        
                        # Check if it's a fix for the same type of operation
                        suggestion = self._create_suggestion(
                            record, next_record, error_message
                        )
                        if suggestion:
                            suggestions.append(suggestion)
        
        # Sort by confidence
        suggestions.sort(key=lambda x: x['confidence'], reverse=True)
        return suggestions
    
    def _create_suggestion(self, error_record: OperationRecord, 
                          success_record: OperationRecord, 
                          error_message: str) -> Optional[Dict[str, Any]]:
        """Create a suggestion based on error and success records"""
        # For column mapping errors
        if error_record.type == "column_mapping":
            error_source = error_record.input.get('source', '')
            success_source = success_record.input.get('source', '')
            
            if error_source and success_source and error_source != success_source:
                return {
                    'suggestion': f"Try '{success_source}' instead of '{error_source}'",
                    'confidence': 0.8,
                    'based_on': {
                        'error': error_record.to_dict(),
                        'success': success_record.to_dict()
                    }
                }
        
        return None
    
    def get_learned_mappings(self) -> Dict[str, Dict[str, Any]]:
        """Get learned column mappings from successful operations"""
        mappings = defaultdict(lambda: {'target': None, 'count': 0, 'confidence': 0})
        
        for record in self.history:
            if (record.success and record.type == "column_mapping" and 
                'source' in record.input):
                
                source = record.input['source']
                target = record.result.get('mapped_to', record.input.get('target'))
                
                if target:
                    mappings[source]['target'] = target
                    mappings[source]['count'] += 1
        
        # Calculate confidence based on frequency
        total_mappings = sum(m['count'] for m in mappings.values())
        for source, mapping in mappings.items():
            mapping['confidence'] = mapping['count'] / max(total_mappings, 1)
        
        return dict(mappings)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about operations"""
        stats = {
            'total_operations': len(self.history),
            'success_rate': 0,
            'by_type': defaultdict(lambda: {'total': 0, 'success': 0, 'success_rate': 0})
        }
        
        if not self.history:
            return stats
        
        success_count = 0
        
        for record in self.history:
            if record.success:
                success_count += 1
                stats['by_type'][record.type]['success'] += 1
            
            stats['by_type'][record.type]['total'] += 1
        
        stats['success_rate'] = success_count / len(self.history)
        
        # Calculate success rate by type
        for type_name, type_stats in stats['by_type'].items():
            if type_stats['total'] > 0:
                type_stats['success_rate'] = (
                    type_stats['success'] / type_stats['total']
                )
        
        return dict(stats)
    
    def clear_old_history(self, days: int = 30) -> None:
        """Clear history entries older than specified days"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        with self._lock:
            old_count = len(self.history)
            self.history = [
                record for record in self.history 
                if record.timestamp > cutoff_date
            ]
            removed_count = old_count - len(self.history)
        
        if removed_count > 0:
            logger.info(f"Removed {removed_count} operations older than {days} days")
    
    def export_learnings(self, export_file: str) -> None:
        """Export learned patterns to a file"""
        learnings = {
            'mappings': self.get_learned_mappings(),
            'error_patterns': self.get_error_patterns(),
            'statistics': self.get_statistics(),
            'export_date': datetime.utcnow().isoformat()
        }
        
        try:
            with open(export_file, 'w') as f:
                json.dump(learnings, f, indent=2)
            logger.info(f"Exported learnings to {export_file}")
        except Exception as e:
            logger.error(f"Failed to export learnings: {e}")
    
    def search_history(self, operation_type: Optional[str] = None,
                      input_contains: Optional[str] = None,
                      error_contains: Optional[str] = None) -> List[OperationRecord]:
        """Search through history with filters"""
        results = []
        
        for record in self.history:
            # Filter by operation type
            if operation_type and record.type != operation_type:
                continue
            
            # Filter by input content
            if input_contains:
                input_str = json.dumps(record.input, default=str).lower()
                if input_contains.lower() not in input_str:
                    continue
            
            # Filter by error content
            if error_contains:
                if not record.error or error_contains.lower() not in record.error.lower():
                    continue
            
            results.append(record)
        
        return results
    
    def get_recent_operations(self, limit: int = 10) -> List[OperationRecord]:
        """Get most recent operations"""
        with self._lock:
            # Return most recent operations (reverse chronological order)
            return sorted(
                self.history, 
                key=lambda x: x.timestamp, 
                reverse=True
            )[:limit]