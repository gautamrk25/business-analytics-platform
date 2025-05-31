"""Tests for the ExecutiveDemo base class."""

import asyncio
from typing import TYPE_CHECKING, Any, Dict
import pytest
from unittest.mock import MagicMock, patch

from goob_ai.demo.executive_demo import ExecutiveDemo
from goob_ai.orchestrator import BusinessAnalysisOrchestrator

if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture
    from _pytest.fixtures import FixtureRequest
    from _pytest.logging import LogCaptureFixture
    from _pytest.monkeypatch import MonkeyPatch
    from pytest_mock.plugin import MockerFixture

class TestExecutiveDemo:
    """Test suite for ExecutiveDemo class."""
    
    @pytest.fixture
    def mock_orchestrator(self) -> BusinessAnalysisOrchestrator:
        """Create a mock orchestrator for testing."""
        return MagicMock(spec=BusinessAnalysisOrchestrator)
    
    @pytest.fixture
    def demo(self, mock_orchestrator: BusinessAnalysisOrchestrator) -> ExecutiveDemo:
        """Create an ExecutiveDemo instance for testing."""
        return ExecutiveDemo(mock_orchestrator)
    
    def test_init(self, demo: ExecutiveDemo, mock_orchestrator: BusinessAnalysisOrchestrator) -> None:
        """Test ExecutiveDemo initialization."""
        assert demo.orchestrator == mock_orchestrator
        assert demo.demo_results == {}
        assert demo.timing_delays is True
    
    def test_set_timing(self, demo: ExecutiveDemo) -> None:
        """Test setting timing delays."""
        demo.set_timing(False)
        assert demo.timing_delays is False
        
        demo.set_timing(True)
        assert demo.timing_delays is True
    
    @pytest.mark.asyncio
    async def test_demo_delay_with_timing(self, demo: ExecutiveDemo) -> None:
        """Test demo delay with timing enabled."""
        demo.timing_delays = True
        start_time = asyncio.get_event_loop().time()
        await demo.demo_delay(0.1)
        end_time = asyncio.get_event_loop().time()
        
        assert end_time - start_time >= 0.1
    
    @pytest.mark.asyncio
    async def test_demo_delay_without_timing(self, demo: ExecutiveDemo) -> None:
        """Test demo delay with timing disabled."""
        demo.timing_delays = False
        start_time = asyncio.get_event_loop().time()
        await demo.demo_delay(0.1)
        end_time = asyncio.get_event_loop().time()
        
        assert end_time - start_time < 0.1
    
    def test_display_section_header(self, demo: ExecutiveDemo, capsys: "CaptureFixture") -> None:
        """Test section header display."""
        title = "Test Section"
        demo.display_section_header(title)
        captured = capsys.readouterr()
        
        expected = f"\n{'=' * 80}\n{title.center(80)}\n{'=' * 80}\n\n"
        assert captured.out == expected
    
    def test_display_progress(self, demo: ExecutiveDemo, capsys: "CaptureFixture") -> None:
        """Test progress display."""
        message = "Processing..."
        progress = 50
        demo.display_progress(message, progress)
        captured = capsys.readouterr()
        
        expected = f"[{progress:3d}%] {message}\n"
        assert captured.out == expected
    
    @pytest.mark.asyncio
    async def test_run_demo_not_implemented(self, demo: ExecutiveDemo) -> None:
        """Test that run_demo raises NotImplementedError."""
        with pytest.raises(NotImplementedError):
            await demo.run_demo()
    
    def test_get_results(self, demo: ExecutiveDemo) -> None:
        """Test getting demo results."""
        test_results = {"key": "value"}
        demo.demo_results = test_results.copy()
        
        results = demo.get_results()
        assert results == test_results
        assert results is not demo.demo_results  # Should return a copy 