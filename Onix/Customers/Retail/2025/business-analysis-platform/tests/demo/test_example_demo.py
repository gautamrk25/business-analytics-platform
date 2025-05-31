"""Tests for the ExampleBusinessDemo class."""

import asyncio
from typing import TYPE_CHECKING, Any, Dict
import pytest
from unittest.mock import MagicMock

from goob_ai.demo.example_demo import ExampleBusinessDemo
from goob_ai.orchestrator import BusinessAnalysisOrchestrator

if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture
    from _pytest.fixtures import FixtureRequest
    from _pytest.logging import LogCaptureFixture
    from _pytest.monkeypatch import MonkeyPatch
    from pytest_mock.plugin import MockerFixture

class TestExampleBusinessDemo:
    """Test suite for ExampleBusinessDemo class."""
    
    @pytest.fixture
    def mock_orchestrator(self) -> BusinessAnalysisOrchestrator:
        """Create a mock orchestrator for testing."""
        return MagicMock(spec=BusinessAnalysisOrchestrator)
    
    @pytest.fixture
    def demo(self, mock_orchestrator: BusinessAnalysisOrchestrator) -> ExampleBusinessDemo:
        """Create an ExampleBusinessDemo instance for testing."""
        return ExampleBusinessDemo(mock_orchestrator)
    
    @pytest.mark.asyncio
    async def test_run_demo_structure(self, demo: ExampleBusinessDemo) -> None:
        """Test the structure of the demo results."""
        results = await demo.run_demo()
        
        # Check basic structure
        assert 'steps_completed' in results
        assert 'total_steps' in results
        assert 'analysis_results' in results
        assert 'recommendations' in results
        assert 'sample_data' in results
        
        # Check analysis results structure
        analysis_results = results['analysis_results']
        assert 'basic' in analysis_results
        assert 'advanced' in analysis_results
        
        # Check basic analysis
        basic = analysis_results['basic']
        assert 'total_sales' in basic
        assert 'avg_customers' in basic
        assert 'sales_trend' in basic
        
        # Check advanced insights
        advanced = analysis_results['advanced']
        assert 'customer_value' in advanced
        assert 'growth_rate' in advanced
        assert 'key_findings' in advanced
        assert isinstance(advanced['key_findings'], list)
        
        # Check recommendations
        assert isinstance(results['recommendations'], list)
        assert len(results['recommendations']) > 0
    
    @pytest.mark.asyncio
    async def test_run_demo_calculations(self, demo: ExampleBusinessDemo) -> None:
        """Test the calculations in the demo results."""
        results = await demo.run_demo()
        
        # Get sample data
        sample_data = results['sample_data']
        sales = sample_data['sales']
        customers = sample_data['customers']
        
        # Check basic analysis calculations
        basic = results['analysis_results']['basic']
        assert basic['total_sales'] == sum(sales)
        assert basic['avg_customers'] == sum(customers) / len(customers)
        
        # Check advanced insights calculations
        advanced = results['analysis_results']['advanced']
        expected_customer_value = basic['total_sales'] / basic['avg_customers']
        assert advanced['customer_value'] == expected_customer_value
    
    @pytest.mark.asyncio
    async def test_run_demo_without_timing(self, demo: ExampleBusinessDemo) -> None:
        """Test running the demo with timing disabled."""
        demo.set_timing(False)
        start_time = asyncio.get_event_loop().time()
        await demo.run_demo()
        end_time = asyncio.get_event_loop().time()
        
        # Demo should complete quickly without timing delays
        assert end_time - start_time < 1.0
    
    @pytest.mark.asyncio
    async def test_run_demo_with_timing(self, demo: ExampleBusinessDemo) -> None:
        """Test running the demo with timing enabled."""
        demo.set_timing(True)
        start_time = asyncio.get_event_loop().time()
        await demo.run_demo()
        end_time = asyncio.get_event_loop().time()
        
        # Demo should take at least the sum of all delays
        total_delay = 1.0 + 1.5 + 2.0 + 1.0  # Sum of all demo_delay calls
        assert end_time - start_time >= total_delay 