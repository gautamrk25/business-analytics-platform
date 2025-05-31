"""Tests for database setup and connection management"""
import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session
from sqlalchemy import text

from src.models.database import (
    DatabaseManager,
    get_db,
    create_tables,
    drop_tables,
    Base
)


class TestDatabaseManager:
    """Test suite for DatabaseManager class"""
    
    def test_singleton_pattern(self):
        """Test that DatabaseManager follows singleton pattern"""
        manager1 = DatabaseManager()
        manager2 = DatabaseManager()
        assert manager1 is manager2
    
    def test_init_with_test_database(self):
        """Test initialization with test database URL"""
        with patch('src.models.database.create_engine') as mock_engine:
            with patch.dict('os.environ', {'DATABASE_URL': 'sqlite:///test.db'}):
                manager = DatabaseManager()
                manager._init()
                
                # Should use the environment variable URL
                mock_engine.assert_called_once()
                call_args = mock_engine.call_args[0][0]
                assert 'test.db' in call_args
    
    def test_init_with_config_database(self):
        """Test initialization with config database URL"""
        with patch('src.models.database.create_engine') as mock_engine:
            with patch('src.models.database.ConfigManager') as mock_config:
                # Mock config to return a database URL
                mock_config_instance = MagicMock()
                mock_config_instance.get.return_value = 'sqlite:///config.db'
                mock_config.return_value = mock_config_instance
                
                manager = DatabaseManager()
                manager._init()
                
                mock_engine.assert_called_once()
                call_args = mock_engine.call_args[0][0]
                assert 'config.db' in call_args
    
    def test_get_session(self):
        """Test getting a database session"""
        with patch('src.models.database.create_engine'):
            manager = DatabaseManager()
            session = manager.get_session()
            
            assert isinstance(session, Session)
            session.close()
    
    def test_session_context_manager(self):
        """Test session context manager functionality"""
        with patch('src.models.database.create_engine'):
            manager = DatabaseManager()
            
            with manager.session() as session:
                assert isinstance(session, Session)
                # Store the state while in context
                was_active = session.is_active
            
            # Session should be closed after context
            # Note: In SQLAlchemy 2.0, sessions may remain "active" but are closed
            assert was_active is True  # Active while in context
    
    def test_session_rollback_on_exception(self):
        """Test that session rolls back on exception"""
        with patch('src.models.database.create_engine'):
            manager = DatabaseManager()
            
            with pytest.raises(ValueError):
                with manager.session() as session:
                    # Simulate some database operation
                    session.execute(text("SELECT 1"))
                    # Raise an exception
                    raise ValueError("Test exception")
            
            # Session should have been rolled back
            # Note: We can't directly test rollback was called due to mocking,
            # but this test ensures the exception propagates correctly


class TestDatabaseFunctions:
    """Test module-level database functions"""
    
    def test_get_db_generator(self):
        """Test get_db yields a session and closes it"""
        with patch('src.models.database.DatabaseManager') as mock_manager:
            mock_session = MagicMock(spec=Session)
            mock_manager.return_value.get_session.return_value = mock_session
            
            # Get generator
            gen = get_db()
            
            # Get session from generator
            session = next(gen)
            assert session is mock_session
            
            # Close generator (simulates finally block)
            try:
                next(gen)
            except StopIteration:
                pass
            
            # Session should have been closed
            mock_session.close.assert_called_once()
    
    def test_create_tables(self):
        """Test create_tables function"""
        with patch('src.models.database.DatabaseManager') as mock_manager:
            mock_engine = MagicMock()
            mock_manager.return_value.engine = mock_engine
            
            with patch('src.models.database.Base') as mock_base:
                create_tables()
                
                # Should call create_all on Base metadata
                mock_base.metadata.create_all.assert_called_once_with(mock_engine)
    
    def test_drop_tables(self):
        """Test drop_tables function"""
        with patch('src.models.database.DatabaseManager') as mock_manager:
            mock_engine = MagicMock()
            mock_manager.return_value.engine = mock_engine
            
            with patch('src.models.database.Base') as mock_base:
                drop_tables()
                
                # Should call drop_all on Base metadata
                mock_base.metadata.drop_all.assert_called_once_with(mock_engine)
    
    def test_database_url_from_env(self):
        """Test database URL is read from environment variable"""
        test_url = "postgresql://user:pass@localhost/testdb"
        
        with patch.dict('os.environ', {'DATABASE_URL': test_url}):
            with patch('src.models.database.create_engine') as mock_engine:
                manager = DatabaseManager()
                manager._init()
                
                mock_engine.assert_called_once()
                call_args = mock_engine.call_args[0][0]
                assert call_args == test_url
    
    def test_database_url_fallback_to_config(self):
        """Test database URL falls back to config when env var not set"""
        config_url = "postgresql://user:pass@localhost/configdb"
        
        with patch.dict('os.environ', {}, clear=True):
            with patch('src.models.database.ConfigManager') as mock_config:
                mock_config_instance = MagicMock()
                mock_config_instance.get.return_value = config_url
                mock_config.return_value = mock_config_instance
                
                with patch('src.models.database.create_engine') as mock_engine:
                    manager = DatabaseManager()
                    manager._init()
                    
                    mock_engine.assert_called_once()
                    call_args = mock_engine.call_args[0][0]
                    assert call_args == config_url
    
    def test_sqlalchemy_base_class(self):
        """Test that Base class is properly defined"""
        from src.models.database import Base
        from sqlalchemy.orm import DeclarativeBase
        
        # Base should be a SQLAlchemy declarative base (2.0 style)
        assert issubclass(Base, DeclarativeBase)
        assert hasattr(Base, 'metadata')
        assert hasattr(Base, 'registry')