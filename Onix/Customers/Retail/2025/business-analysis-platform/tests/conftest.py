"""
Pytest configuration and fixtures for the Business Analysis Platform tests.
"""
import pytest
import asyncio
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def sample_data():
    """Provide sample data for testing."""
    return {
        'sales': [100, 200, 300, 400, 500],
        'customers': ['A', 'B', 'C', 'A', 'B'],
        'dates': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05']
    }


@pytest.fixture
def config_defaults():
    """Provide default configuration for testing."""
    return {
        'timeout_seconds': 60,
        'max_retries': 3,
        'enable_logging': True
    }


@pytest.fixture
def mock_logger(mocker):
    """Mock logger for testing."""
    return mocker.patch('logging.getLogger')