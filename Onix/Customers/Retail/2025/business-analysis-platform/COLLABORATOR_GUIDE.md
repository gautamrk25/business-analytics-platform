# Collaborator Guide - Business Analysis Platform

Welcome to the Business Analysis Platform project! This guide will help you get set up with Claude Code and understand our development workflow.

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/gautamrk25/2025.git
cd 2025/Onix/Customers/Retail/2025/business-analysis-platform
```

### 2. Set Up Claude Code
1. Install Claude Code CLI from [claude.ai/code](https://claude.ai/code)
2. Create a CLAUDE.md file if not present (already included in repo)
3. Use Claude Opus 4 model for all development

### 3. Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 4. Run Tests to Verify Setup
```bash
python -m pytest tests/ -v
```

## Development Philosophy

### 🎯 Core Principles
1. **Claude Code First**: Use Claude Opus 4 for ALL code generation
2. **Test-Driven Development (TDD)**: Write tests BEFORE implementation
3. **Documentation Driven**: Update docs as you code
4. **Workflow Adherence**: Follow DEVELOPMENT_WORKFLOW.md exactly

### 🚨 Critical Rules
- **NEVER** write code manually - always use Claude Code
- **NEVER** skip tests - follow TDD religiously
- **NEVER** proceed if tests are failing
- **ALWAYS** check PROJECT_STATUS.md before starting work

## Key Documentation Files

### Must-Read Documents (In Order)
1. **[DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md)** - The exact workflow to follow
2. **[PROJECT_STATUS.md](PROJECT_STATUS.md)** - Current status and next tasks
3. **[CLAUDE.md](CLAUDE.md)** - Instructions for Claude Code
4. **[TDD_CHECKLIST.md](TDD_CHECKLIST.md)** - Test-driven development steps

### Reference Documents
- **[AI_AGENTS_IMPLEMENTATION.md](AI_AGENTS_IMPLEMENTATION.md)** - AI agent architecture
- **[backend_api_design.md](backend_api_design.md)** - API endpoint specifications
- **[ERROR_RECOVERY.md](ERROR_RECOVERY.md)** - Troubleshooting guide
- **[IMPLEMENTATION_SEQUENCE.md](IMPLEMENTATION_SEQUENCE.md)** - Build order

## Claude Code Best Practices

### Starting a Work Session
```bash
# 1. Check current status
cat PROJECT_STATUS.md | grep -A 20 "Current Focus"

# 2. Open Claude Code in the project directory
claude .

# 3. Tell Claude what you want to work on
# Example: "I want to complete the Industry Detective Agent tests"
```

### Effective Claude Prompts

#### For Implementing Features
```
Following the TDD workflow in TDD_CHECKLIST.md, implement the [feature name] 
to make all tests in tests/[test_file.py] pass. The current test failures are:
[paste test output]
```

#### For Writing Tests
```
Following TDD principles, write comprehensive tests for [component name] 
that cover all functionality described in [documentation file]. 
Include edge cases and error conditions.
```

#### For Debugging
```
The test [test_name] in [test_file] is failing with this error:
[paste error]
Following ERROR_RECOVERY.md, help me fix this issue.
```

## Current Project Status

### ✅ Completed Components
- Foundation layer (ConfigManager, Logger, Base classes)
- Data Validator Block (17/17 tests passing)
- Smart Data Profiler Block (22/22 tests passing)
- Code Inspector Agent (22/25 tests passing)

### 🚧 In Progress
- Industry Detective Agent (9/24 tests passing)
  - Next: Complete remaining 15 tests

### 📋 Upcoming Work
1. Complete Industry Detective Agent
2. Implement Trend Analyzer Block
3. Start FastAPI endpoints

## Working with AI Agents

The project includes intelligent agents that work together:
- **Industry Detective**: Auto-detects business type
- **Code Inspector**: Analyzes errors and suggests fixes
- **Business Analysis Agent**: Core analysis engine
- **Memory Keeper**: Learns from usage patterns

See [AI_AGENTS_IMPLEMENTATION.md](AI_AGENTS_IMPLEMENTATION.md) for details.

## Git Workflow

### Daily Development
```bash
# 1. Pull latest changes
git pull origin main

# 2. Create feature branch (optional)
git checkout -b feature/component-name

# 3. Work with Claude Code
# Let Claude handle all code changes

# 4. Commit when tests pass
git add .
git commit -m "Implement [feature]: [description]"

# 5. Push changes
git push origin main  # or feature branch
```

### Commit Message Format
```
[Component]: Brief description

- Detail 1
- Detail 2
- Tests: X/Y passing
```

## Testing Guidelines

### Running Tests
```bash
# All tests
python -m pytest tests/ -v

# Specific component
python -m pytest tests/test_agents/test_industry_detective.py -v

# With coverage
python -m pytest tests/ --cov=src --cov-report=html

# Watch mode (if pytest-watch installed)
python -m pytest tests/ --watch
```

### Test Requirements
- Minimum 80% code coverage
- All tests must pass before committing
- Write tests BEFORE implementation

## Common Claude Code Commands

### Check Project Status
Tell Claude: "Check PROJECT_STATUS.md and tell me what to work on next"

### Implement Next Feature
Tell Claude: "Following DEVELOPMENT_WORKFLOW.md, implement the next priority task"

### Fix Failing Tests
Tell Claude: "These tests are failing [paste output]. Fix the implementation"

### Update Documentation
Tell Claude: "Update PROJECT_STATUS.md with the current progress"

## Troubleshooting

### Import Errors
- Check virtual environment is activated
- Verify all dependencies installed

### Test Failures
- Follow ERROR_RECOVERY.md
- Ask Claude: "Help me debug this test failure [paste error]"

### Claude Code Issues
- Ensure you're using Claude Opus 4 model
- Provide clear, specific prompts
- Reference documentation files in prompts

## Communication

### Progress Updates
- Update PROJECT_STATUS.md after each component
- Commit frequently with clear messages
- Document any blockers or issues

### Questions
- Check documentation first
- Use Claude Code to explore codebase
- Create GitHub issues for discussions

## Next Steps

1. Read all documentation files listed above
2. Check PROJECT_STATUS.md for current tasks
3. Set up your environment
4. Start with the current focus task
5. Use Claude Code for ALL implementation

Remember: The key to success is following the established workflow and using Claude Code consistently. Happy coding!

---
**Important**: This is a backend API project. The frontend will be implemented separately. Focus only on Python/FastAPI backend components.