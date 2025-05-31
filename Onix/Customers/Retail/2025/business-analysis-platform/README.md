# Business Analysis Platform

A comprehensive Python application that combines AI-driven business intelligence with modular architecture for extensible analysis capabilities.

## Overview

The Business Analysis Platform uses a building block architecture inspired by AWS Lambda functions, allowing users to create complex analysis workflows by chaining together modular components.

### Key Features

- **Modular Building Blocks**: Self-contained analysis components
- **Industry Intelligence**: Built-in knowledge for retail, healthcare, finance
- **Self-Healing Data**: Automatic data quality fixes
- **Template System**: Pre-configured analysis workflows
- **AI Integration**: Powered by advanced language models
- **Extensible Architecture**: Easy to add new capabilities

## Documentation Structure

### For Developers

1. **[CLAUDE.md](CLAUDE.md)** - Development context and guidelines
2. **[TDD_CHECKLIST.md](TDD_CHECKLIST.md)** - Test-driven development workflow
3. **[IMPLEMENTATION_SEQUENCE.md](IMPLEMENTATION_SEQUENCE.md)** - Build order and dependencies
4. **[ERROR_RECOVERY.md](ERROR_RECOVERY.md)** - Troubleshooting guide

### For Project Managers

1. **[QUICK_START.md](QUICK_START.md)** - Instructions for working with Claude
2. **[PRE_DEVELOPMENT_CHECKLIST.md](PRE_DEVELOPMENT_CHECKLIST.md)** - Setup verification
3. **[implementation_recommendations.md](implementation_recommendations.md)** - Feature cohorts

### Technical Documentation

1. **[business_analysis_platform_documentation.md](business_analysis_platform_documentation.md)** - Complete technical reference
2. **[building_block_system_design.md](building_block_system_design.md)** - Architecture overview
3. **[building_block_system_design_v2.md](building_block_system_design_v2.md)** - Enhanced design
4. **[realistic_feature_implementation_guide.md](realistic_feature_implementation_guide.md)** - Implementation examples

## Quick Start

### Prerequisites

- Python 3.9 or higher
- pip package manager
- Git (optional but recommended)

### Setup

1. Clone or download this repository
2. Create virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate virtual environment:
   ```bash
   # On macOS/Linux
   source venv/bin/activate
   
   # On Windows
   venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run specific test
python -m pytest tests/test_building_blocks/test_example_block.py -v
```

### Starting Development

1. Read [PRE_DEVELOPMENT_CHECKLIST.md](PRE_DEVELOPMENT_CHECKLIST.md)
2. Follow [IMPLEMENTATION_SEQUENCE.md](IMPLEMENTATION_SEQUENCE.md)
3. Use [TDD_CHECKLIST.md](TDD_CHECKLIST.md) for each component
4. Refer to [ERROR_RECOVERY.md](ERROR_RECOVERY.md) when issues arise

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Streamlit UI                             │
├─────────────────────────────────────────────────────────────────┤
│                    Business Analysis Agent                      │
├─────────────────┬─────────────────┬─────────────────────────────┤
│  Template       │   Building      │    Learning History         │
│  Manager        │   Block         │    Manager                  │
│                 │   Registry      │                             │
├─────────────────┴─────────────────┴─────────────────────────────┤
│                     Building Blocks                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │    Data     │  │  Analysis   │  │Visualization│             │
│  │  Validator  │  │   Blocks    │  │   Blocks    │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
├─────────────────────────────────────────────────────────────────┤
│                    Configuration Manager                        │
└─────────────────────────────────────────────────────────────────┘
```

## Project Structure

```
business-analysis-platform/
├── src/                      # Source code
│   ├── building_blocks/      # Building block implementations
│   ├── templates/            # Template definitions
│   ├── utils/                # Utility functions
│   └── ui/                   # User interface
├── tests/                    # Test suite
│   ├── test_building_blocks/ # Building block tests
│   ├── test_templates/       # Template tests
│   └── test_integration/     # Integration tests
├── docs/                     # Additional documentation
├── config.yaml              # Configuration file
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Development Workflow

1. **Plan**: Read requirements and documentation
2. **Test**: Write tests first (TDD)
3. **Implement**: Code to make tests pass
4. **Refactor**: Improve while keeping tests green
5. **Document**: Update docs and examples
6. **Integrate**: Ensure components work together

## Testing Philosophy

- **Test-Driven Development (TDD)** is mandatory
- **80% minimum code coverage** required
- **Tests must pass** before proceeding
- **Fix immediately** when tests fail

## Contributing

1. Follow the [TDD_CHECKLIST.md](TDD_CHECKLIST.md)
2. Implement in order per [IMPLEMENTATION_SEQUENCE.md](IMPLEMENTATION_SEQUENCE.md)
3. Maintain code quality standards
4. Update documentation as needed

## Support

For issues or questions:
1. Check [ERROR_RECOVERY.md](ERROR_RECOVERY.md)
2. Review relevant documentation
3. Create an issue with details

## License

[Specify your license here]

## Acknowledgments

Built with Claude AI assistance following best practices for maintainable, testable code.