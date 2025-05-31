# Terminal Setup Guide - May 18, 2025

## Quick Setup for Each Terminal

Before starting work in each terminal, run these setup commands:

### Terminal 1-7: Initial Setup
```bash
# Navigate to project directory
cd /Users/gautamkotwal/Documents/Code/Onix/Customers/Retail/2025/business-analysis-platform

# Activate virtual environment
source venv/bin/activate

# Verify Python version
python --version

# Install/update dependencies
pip install -r requirements.txt

# Run existing tests to verify setup
python -m pytest -v
```

## Terminal-Specific Setup

### Terminal 1: Industry Detective Agent
```bash
# After initial setup, verify current test status
python -m pytest tests/test_agents/test_industry_detective.py -v

# You should see 9 passing and 15 failing tests
```

### Terminal 2: Trend Analyzer
```bash
# Create necessary directories
mkdir -p tests/test_building_blocks/analysis
mkdir -p src/building_blocks/analysis

# Create __init__.py files if they don't exist
touch tests/test_building_blocks/analysis/__init__.py
touch src/building_blocks/analysis/__init__.py
```

### Terminal 3: Segmentation Block
```bash
# Use same directories as Terminal 2
# Just create the test and source files when ready
```

### Terminal 4: Chart Generator
```bash
# Create necessary directories
mkdir -p tests/test_building_blocks/visualization
mkdir -p src/building_blocks/visualization

# Create __init__.py files
touch tests/test_building_blocks/visualization/__init__.py
touch src/building_blocks/visualization/__init__.py

# Install visualization dependencies if needed
pip install plotly
```

### Terminal 5: Execution Manager
```bash
# Create necessary directories
mkdir -p tests/test_agents
mkdir -p src/agents

# These should already exist, just verify
```

### Terminal 6: Memory Keeper
```bash
# Same as Terminal 5 - directories should exist
# Verify Learning History Manager is working
python -c "from src.utils.learning_history import LearningHistoryManager; print('Learning History OK')"
```

### Terminal 7: Business Analysis Agent
```bash
# Same as Terminal 5 - directories should exist
# This will create basic structure only
```

## Important Reminders

1. **Each terminal works independently** - Don't wait for others
2. **Write tests first** - Follow TDD strictly
3. **Check existing patterns** - Look at completed components for style
4. **Commit often** - Create feature branches if using git
5. **Ask for help** - If stuck, the other components might have examples

## Monitoring Progress

In a separate terminal, you can monitor overall progress:

```bash
# Watch test results
watch -n 5 'python -m pytest -v --tb=no | grep -E "(PASSED|FAILED)"'

# Check coverage
python -m pytest --cov=src --cov-report=term-missing

# See what's implemented
find src -name "*.py" -type f | grep -E "(building_blocks|agents)" | sort
```

## Troubleshooting

If you encounter issues:

1. **Import errors**: Make sure virtual environment is activated
2. **Test failures**: Check if dependencies are installed
3. **Path issues**: Ensure you're in the correct directory
4. **Permission errors**: Check file permissions

Remember: Each terminal can work completely independently. No need to coordinate or wait.