"""Executive demo base class for business analysis platform.

This module provides the base class for creating executive demos that showcase
the business analysis platform's capabilities.
"""

import asyncio
import logging
from typing import Any, Dict, Optional

from ..orchestrator import BusinessAnalysisOrchestrator

logger = logging.getLogger(__name__)

class ExecutiveDemo:
    """Base class for executive demos that showcase business analysis capabilities.
    
    This class provides core functionality for creating professional demos
    that demonstrate the platform's features. It handles timing, progress display,
    and result storage.
    
    Attributes:
        orchestrator (BusinessAnalysisOrchestrator): The orchestrator instance
            used for analysis.
        demo_results (Dict[str, Any]): Storage for demo results and outputs.
        timing_delays (bool): Whether to include timing delays for demo effect.
    """
    
    def __init__(self, orchestrator: BusinessAnalysisOrchestrator) -> None:
        """Initialize the executive demo.
        
        Args:
            orchestrator: The business analysis orchestrator instance.
        """
        self.orchestrator = orchestrator
        self.demo_results = {}
        self.timing_delays = True  # Set to False for testing
        logger.info("ExecutiveDemo initialized")
    
    def set_timing(self, enabled: bool) -> None:
        """Enable or disable timing delays for demo effect.
        
        Args:
            enabled: Whether to enable timing delays.
        """
        self.timing_delays = enabled
        logger.info(f"Demo timing delays {'enabled' if enabled else 'disabled'}")
    
    async def demo_delay(self, seconds: float) -> None:
        """Add a delay for demo effect if timing is enabled.
        
        Args:
            seconds: Number of seconds to delay.
        """
        if self.timing_delays:
            logger.debug(f"Adding demo delay of {seconds} seconds")
            await asyncio.sleep(seconds)
    
    def display_section_header(self, title: str) -> None:
        """Display a professional section header.
        
        Args:
            title: The section title to display.
        """
        # Implementation for formatted headers
        logger.info(f"Displaying section header: {title}")
        # TODO: Implement actual header display logic
        print(f"\n{'=' * 80}")
        print(f"{title.center(80)}")
        print(f"{'=' * 80}\n")
    
    def display_progress(self, message: str, progress: int) -> None:
        """Show demo progress with a message and percentage.
        
        Args:
            message: Progress message to display.
            progress: Progress percentage (0-100).
        """
        # Implementation for progress display
        logger.info(f"Progress {progress}%: {message}")
        # TODO: Implement actual progress display logic
        print(f"[{progress:3d}%] {message}")
    
    async def run_demo(self) -> Dict[str, Any]:
        """Run the executive demo.
        
        This method should be overridden by subclasses to implement
        specific demo flows.
        
        Returns:
            Dict containing demo results and outputs.
        """
        raise NotImplementedError("Subclasses must implement run_demo()")
    
    def get_results(self) -> Dict[str, Any]:
        """Get the stored demo results.
        
        Returns:
            Dict containing all demo results and outputs.
        """
        return self.demo_results.copy() 