"""Database connection and session management"""
import os
import logging
from typing import Generator, Optional
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from sqlalchemy.pool import StaticPool

from src.utils.config import ConfigManager

logger = logging.getLogger(__name__)


# Create the declarative base for SQLAlchemy 2.0
class Base(DeclarativeBase):
    """Base class for all database models"""
    pass


class DatabaseManager:
    """Singleton database manager for handling connections and sessions"""
    
    _instance: Optional['DatabaseManager'] = None
    _initialized: bool = False
    
    def __new__(cls) -> 'DatabaseManager':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize database manager (only runs once due to singleton)"""
        if not self._initialized:
            self._init()
            self._initialized = True
    
    def _init(self):
        """Actual initialization of database components"""
        # Get database URL from environment or config
        database_url = os.getenv('DATABASE_URL')
        
        if not database_url:
            config = ConfigManager()
            database_url = config.get('database.url', default='sqlite:///./business_analysis.db')
        
        logger.info(f"Initializing database connection: {database_url}")
        
        # Create engine with appropriate settings
        if database_url.startswith('sqlite'):
            # SQLite specific settings
            self.engine = create_engine(
                database_url,
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
                echo=False
            )
        else:
            # PostgreSQL/MySQL settings
            self.engine = create_engine(
                database_url,
                pool_pre_ping=True,
                echo=False
            )
        
        # Create session factory
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        logger.info("Database manager initialized successfully")
    
    def get_session(self) -> Session:
        """Get a new database session"""
        return self.SessionLocal()
    
    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        """Context manager for database sessions"""
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


# Module-level functions
def get_db() -> Generator[Session, None, None]:
    """Dependency for FastAPI to get database session"""
    manager = DatabaseManager()
    db = manager.get_session()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all database tables"""
    manager = DatabaseManager()
    Base.metadata.create_all(manager.engine)
    logger.info("Database tables created")


def drop_tables():
    """Drop all database tables (use with caution!)"""
    manager = DatabaseManager()
    Base.metadata.drop_all(manager.engine)
    logger.info("Database tables dropped")