# Parallel Development Plan - May 18, 2025

This document contains copy-paste ready prompts for Claude 3.7 Sonnet to implement the Business Analysis Platform components in parallel across 7 terminals/computers.

## Important Notes
- Each terminal/computer should work on ONE component only
- Follow Test-Driven Development (TDD) - write tests first
- Each prompt is self-contained and can be executed independently
- No dependencies between these 7 streams

---

## Terminal 1: Complete Industry Detective Agent (PRIORITY)

### Current Status
- 9/24 tests passing
- Located at: `src/agents/industry_detective.py`
- Tests at: `tests/test_agents/test_industry_detective.py`

### Copy this prompt:
```
I need to complete the Industry Detective Agent implementation. Currently 9 out of 24 tests are passing. The agent is located at src/agents/industry_detective.py and tests are at tests/test_agents/test_industry_detective.py.

Please run the tests first to see which ones are failing, then implement the missing functionality to make all 24 tests pass. The remaining features needed are:
- Manufacturing industry detection
- Healthcare industry detection  
- Financial services industry detection
- Hospitality industry detection
- Error handling for invalid data
- Learning mechanism improvements
- Batch detection and accuracy reporting

Follow the existing code patterns and ensure all tests pass. Use the same style as the already implemented retail, SaaS, and B2B services detection.

First, run: python -m pytest tests/test_agents/test_industry_detective.py -v

Then implement the missing features one by one until all tests pass.
```

---

## Terminal 2: Implement Trend Analyzer Block

### Copy this prompt:
```
I need to implement a new building block called Trend Analyzer following Test-Driven Development (TDD) principles.

Step 1: Create comprehensive tests first at tests/test_building_blocks/analysis/test_trend_analyzer.py

The Trend Analyzer should:
- Inherit from BuildingBlock base class
- Analyze trends in time-series data
- Support multiple trend types (linear, exponential, seasonal)
- Calculate trend strength and confidence
- Generate trend forecasts
- Handle missing data gracefully
- Support customizable time windows
- Return trend metrics and visualizations

Include tests for:
- Initialization with proper configuration
- Basic linear trend detection
- Seasonal pattern recognition
- Trend forecasting
- Missing data handling
- Edge cases (single data point, all same values)
- Invalid input handling
- Configuration validation

Step 2: After tests are written and failing, implement src/building_blocks/analysis/trend_analyzer.py

Follow these patterns from existing blocks:
- Use the BuildingBlock base class from src/building_blocks/base.py
- Follow the validation patterns from DataValidator
- Use similar configuration structure
- Return results in the standard format: {success: bool, data: any, errors: []}

Make sure all tests pass and achieve at least 80% code coverage.
```

---

## Terminal 3: Implement Segmentation Block

### Copy this prompt:
```
I need to implement a new building block called Segmentation Block following Test-Driven Development (TDD).

Step 1: Create comprehensive tests at tests/test_building_blocks/analysis/test_segmentation.py

The Segmentation Block should:
- Inherit from BuildingBlock base class
- Perform customer/product segmentation analysis
- Support multiple segmentation methods (K-means, RFM, behavioral)
- Handle both numeric and categorical features
- Provide segment profiles and descriptions
- Calculate segment metrics (size, value, characteristics)
- Support custom segmentation rules
- Visualize segment distributions

Include tests for:
- Initialization and configuration
- K-means clustering segmentation
- RFM (Recency, Frequency, Monetary) analysis
- Behavioral segmentation
- Mixed data type handling
- Segment stability analysis
- Edge cases (single segment, no variation)
- Invalid input handling

Step 2: After tests are written, implement src/building_blocks/analysis/segmentation.py

Use patterns from existing blocks:
- Follow the BuildingBlock base class structure
- Use similar validation patterns as DataValidator
- Implement the standard execute method
- Return results in the expected format

Ensure all tests pass with at least 80% coverage.
```

---

## Terminal 4: Implement Chart Generator Block

### Copy this prompt:
```
I need to implement a Chart Generator building block following TDD principles.

Step 1: Create tests at tests/test_building_blocks/visualization/test_chart_generator.py

The Chart Generator should:
- Inherit from BuildingBlock base class
- Create various chart types (line, bar, scatter, pie, heatmap)
- Use Plotly for interactive visualizations
- Support customizable styling and themes
- Handle different data formats
- Auto-detect appropriate chart types based on data
- Generate multiple charts in one execution
- Export charts in various formats (PNG, SVG, HTML)

Test scenarios to include:
- Initialization with configuration
- Line chart generation
- Bar chart generation  
- Scatter plot generation
- Pie chart generation
- Heatmap generation
- Auto chart type detection
- Custom styling application
- Export functionality
- Invalid data handling
- Edge cases (empty data, single point)

Step 2: Implement src/building_blocks/visualization/chart_generator.py

Follow existing patterns:
- Use BuildingBlock base class
- Implement proper validation
- Use Plotly for chart generation
- Return charts in a structured format
- Include chart metadata in results

Achieve all tests passing with 80%+ coverage.
```

---

## Terminal 5: Implement Execution Manager Agent

### Copy this prompt:
```
I need to implement the Execution Manager Agent following TDD principles.

Step 1: Create comprehensive tests at tests/test_agents/test_execution_manager.py

The Execution Manager should:
- Track execution progress in real-time
- Implement timeout handling
- Support cancellation of long-running tasks
- Provide progress updates via callbacks
- Handle concurrent executions
- Implement retry logic for failures
- Track execution metrics (time, memory, CPU)
- Support different execution priorities
- Integrate with WebSocket for real-time updates

Test cases to include:
- Basic execution tracking
- Progress update callbacks
- Timeout handling (short and long timeouts)
- Task cancellation
- Concurrent execution management
- Retry logic with backoff
- Metric collection
- Priority queue management
- Error propagation
- Edge cases (instant completion, infinite loops)

Step 2: Implement src/agents/execution_manager.py

Key implementation points:
- Use asyncio for async execution
- Implement progress tracking with percentages
- Use callbacks for progress updates
- Implement proper timeout mechanisms
- Handle cleanup on cancellation
- Track metrics during execution
- Use priority queue for task management

Make all tests pass with 80%+ coverage.
```

---

## Terminal 6: Implement Memory Keeper Agent

### Copy this prompt:
```
I need to implement the Memory Keeper Agent following TDD principles.

Step 1: Create tests at tests/test_agents/test_memory_keeper.py

The Memory Keeper should:
- Store analysis history with metadata
- Retrieve similar past analyses
- Track error patterns and solutions
- Implement pattern learning from history
- Support fuzzy matching for similarity
- Provide analysis recommendations based on history
- Clean up old/irrelevant memories
- Export/import memory state
- Integrate with Learning History Manager

Test scenarios:
- Store and retrieve analysis results
- Find similar analyses by question
- Find similar analyses by data structure
- Pattern detection in errors
- Learning from successful fixes
- Memory cleanup/pruning
- Export/import functionality
- Fuzzy matching for questions
- Recommendation generation
- Integration with Learning History

Step 2: Implement src/agents/memory_keeper.py

Implementation notes:
- Use the existing Learning History Manager
- Implement similarity scoring algorithms
- Use embeddings for semantic similarity
- Store metadata for better retrieval
- Implement efficient search mechanisms
- Handle memory limits and cleanup

Ensure all tests pass with good coverage.
```

---

## Terminal 7: Implement Business Analysis Agent (Basic Structure)

### Copy this prompt:
```
I need to implement the basic structure of the Business Analysis Agent following TDD.

Step 1: Create initial tests at tests/test_agents/test_business_analysis.py

The Business Analysis Agent (basic structure) should:
- Perform core business analysis with industry context
- Support multiple analysis types (trend, comparison, correlation)
- Generate insights and recommendations
- Apply industry-specific knowledge
- Handle self-correction on errors
- Format results for easy consumption
- Support custom analysis rules
- Integrate with other agents (later)

Initial test cases:
- Agent initialization
- Basic trend analysis
- Simple comparison analysis
- Correlation analysis
- Industry-specific insights generation
- Recommendation generation
- Error handling and self-correction
- Result formatting
- Configuration management
- Input validation

Step 2: Implement basic structure in src/agents/business_analysis.py

Focus on:
- Core analysis methods
- Industry knowledge application
- Insight generation logic
- Recommendation engine
- Error handling patterns
- Result formatting

Note: Full implementation will integrate with Industry Detective later, but create the basic structure now.

Make initial tests pass.
```

---

## Verification Commands

After implementing each component, run these commands to verify:

```bash
# Run specific tests
python -m pytest tests/test_<component_path> -v

# Check coverage
python -m pytest tests/test_<component_path> --cov=src/<component_path> --cov-report=html

# Run all tests to ensure nothing broke
python -m pytest -v
```

## Success Criteria

For each component:
1. All tests pass
2. Code coverage is at least 80%
3. Code follows existing patterns
4. Documentation is complete
5. No breaking changes to other components

## Next Steps

After all 7 parallel streams are complete:
1. Integrate Business Analysis Agent with Industry Detective
2. Implement Orchestrator Agent (depends on all other agents)
3. Create API endpoints for each service
4. Implement Template Manager
5. Complete WebSocket integration

Remember: Each terminal works independently. No need to wait for others to complete.