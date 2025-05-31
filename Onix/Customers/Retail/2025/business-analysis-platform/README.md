# Business Analysis Platform - Backend API

**Note: This repository contains the FastAPI backend service only. The React frontend will be implemented separately.**

A comprehensive REST API that combines AI-driven business intelligence with modular architecture for extensible analysis capabilities. Built with FastAPI, this backend service provides endpoints for data analysis, AI agent orchestration, and real-time processing.

## Overview

The Business Analysis Platform uses a building block architecture inspired by AWS Lambda functions, allowing users to create complex analysis workflows by chaining together modular components.

### Key Features

- **RESTful API**: FastAPI-based backend service with OpenAPI documentation
- **Modular Building Blocks**: Self-contained analysis components accessible via API
- **AI Agents System**: Intelligent agents for industry detection, error recovery, and analysis
- **Industry Intelligence**: Built-in knowledge for retail, healthcare, finance
- **Self-Healing Data**: Automatic data quality fixes with learning capabilities
- **Template System**: Pre-configured analysis workflows via API
- **Real-time Updates**: WebSocket support for live analysis progress
- **Extensible Architecture**: Easy to add new analysis capabilities

## Documentation Structure

### For Developers

1. **[CLAUDE.md](docs/development/CLAUDE.md)** - Development context and guidelines
2. **[TDD_CHECKLIST.md](docs/development/TDD_CHECKLIST.md)** - Test-driven development workflow
3. **[IMPLEMENTATION_SEQUENCE.md](docs/project/IMPLEMENTATION_SEQUENCE.md)** - Build order and dependencies
4. **[ERROR_RECOVERY.md](docs/development/ERROR_RECOVERY.md)** - Troubleshooting guide

### For Project Managers

1. **[QUICK_REFERENCE.md](docs/development/QUICK_REFERENCE.md)** - Quick reference guide
2. **[PROJECT_STATUS.md](docs/project/PROJECT_STATUS.md)** - Current project status
3. **[implementation_recommendations_backend_api.md](docs/architecture/implementation_recommendations_backend_api.md)** - Feature cohorts

### Technical Documentation

1. **[backend_api_design.md](docs/architecture/backend_api_design.md)** - Backend API design
2. **[building_block_system_design_backend_api.md](docs/architecture/building_block_system_design_backend_api.md)** - Architecture overview
3. **[AI_AGENTS_IMPLEMENTATION.md](docs/architecture/AI_AGENTS_IMPLEMENTATION.md)** - AI agents architecture
4. **[BUSINESS_VALUE_PROPOSITION.md](docs/project/BUSINESS_VALUE_PROPOSITION.md)** - Business value and use cases

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

**For new collaborators**: Start with the documentation in the docs/ directory

1. Read [DEVELOPMENT_WORKFLOW.md](docs/development/DEVELOPMENT_WORKFLOW.md) - **MANDATORY**
2. Check [PROJECT_STATUS.md](docs/project/PROJECT_STATUS.md) for current tasks
3. Follow [TDD_CHECKLIST.md](docs/development/TDD_CHECKLIST.md) for each component
4. Use [CLAUDE.md](docs/development/CLAUDE.md) for coding patterns
5. Refer to [ERROR_RECOVERY.md](docs/development/ERROR_RECOVERY.md) when issues arise

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    React Frontend (Separate Repo)               │
├─────────────────────────────────────────────────────────────────┤
│                        REST API / WebSocket                     │
├─────────────────────────────────────────────────────────────────┤
│                      FastAPI Backend                            │
├─────────────────┬─────────────────┬─────────────────────────────┤
│   AI Agents     │   API Routes    │    WebSocket Handlers       │
│  Orchestrator   │  (/blocks,      │    (Real-time updates)      │
│                 │   /analysis,     │                             │
│                 │   /data)         │                             │
├─────────────────┴─────────────────┴─────────────────────────────┤
│                        AI Agents System                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  Industry   │  │    Code     │  │   Memory    │             │
│  │  Detective  │  │  Inspector  │  │   Keeper    │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
├─────────────────────────────────────────────────────────────────┤
│                     Building Blocks                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │    Data     │  │  Analysis   │  │Visualization│             │
│  │  Validator  │  │   Blocks    │  │   Blocks    │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
├─────────────────────────────────────────────────────────────────┤
│          Database (SQLAlchemy) / Configuration Manager          │
└─────────────────────────────────────────────────────────────────┘
```

## Project Structure

```
business-analysis-platform/
├── main.py                  # FastAPI application entry
├── src/                     # Source code
│   ├── api/                 # API route definitions
│   │   ├── auth.py         # Authentication endpoints
│   │   ├── blocks.py       # Building block endpoints
│   │   ├── data.py         # Data management endpoints
│   │   └── analysis.py     # Analysis orchestration
│   ├── agents/              # AI agent implementations
│   │   ├── industry_detective.py
│   │   └── code_inspector.py
│   ├── building_blocks/     # Analysis components
│   │   ├── data/           # Data processing blocks
│   │   └── analysis/       # Analysis blocks
│   ├── models/              # Database models & schemas
│   ├── services/            # Business logic layer
│   └── utils/               # Utilities (config, logger)
├── tests/                   # Comprehensive test suite
├── data/                   # Data files and samples
│   └── samples/            # Sample data files
├── scripts/                # Utility scripts
│   ├── debug/              # Debug scripts
│   └── data/               # Data generation scripts
├── docs/                   # Documentation
│   ├── development/        # Development guides
│   ├── architecture/       # Architecture docs
│   └── project/            # Project management
├── .env.example            # Environment variables template
├── requirements.txt        # Python dependencies
└── README.md              # This file
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

## API Endpoints

### Available Endpoints

#### Implemented:
- `GET /api/v1/health` - Health check
- `GET /api/v1/version` - API version information
- `GET /api/v1/blocks` - List available building blocks (mock data)
- `GET /api/v1/blocks/{block_id}` - Get block details
- `POST /api/v1/blocks/{block_id}/execute` - Execute a building block
- `GET /api/v1/blocks/{block_id}/metrics` - Get block execution metrics

#### Placeholder (not yet implemented):
- `GET /api/v1/data` - List datasets
- `GET /api/v1/analysis` - List analyses
- `GET /api/v1/templates` - List templates

#### Planned (not yet started):
- `POST /api/v1/data/upload` - Upload data for analysis
- `POST /api/v1/analysis/jobs` - Start analysis job
- `GET /api/v1/analysis/jobs/{job_id}` - Get job status
- `WS /ws/{job_id}` - WebSocket for real-time updates

### Running the API
```bash
# Development
uvicorn main:app --reload

# Production
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Contributing

**Important**: Use Claude Code (Claude Opus 4) for ALL development

1. Read the documentation in [docs/](docs/) first
2. Follow [DEVELOPMENT_WORKFLOW.md](docs/development/DEVELOPMENT_WORKFLOW.md) exactly
3. Check [PROJECT_STATUS.md](docs/project/PROJECT_STATUS.md) for current tasks
4. Use [TDD_CHECKLIST.md](docs/development/TDD_CHECKLIST.md) for testing
5. Update documentation as you code

## Support

For issues or questions:
1. Check [ERROR_RECOVERY.md](docs/development/ERROR_RECOVERY.md)
2. Review relevant documentation
3. Create an issue with details

## License

[Specify your license here]

## Acknowledgments

Built with Claude AI assistance following best practices for maintainable, testable code.