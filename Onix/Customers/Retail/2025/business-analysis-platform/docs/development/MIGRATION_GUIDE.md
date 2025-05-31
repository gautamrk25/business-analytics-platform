# Repository Reorganization Migration Guide

This guide documents the file reorganization performed on the Business Analysis Platform codebase and provides instructions for updating code and finding files in the new structure.

## Overview

The repository has been reorganized to improve maintainability and follow standard Python project conventions. All documentation, scripts, and data files have been moved from the root directory into organized subdirectories.

## File Movements

### Documentation Files

All documentation files have been moved from the root directory to the `docs/` directory:

#### Development Documentation → `docs/development/`
- `CLAUDE.md` → `docs/development/CLAUDE.md`
- `COLLABORATOR_GUIDE.md` → `docs/development/COLLABORATOR_GUIDE.md`
- `DEVELOPMENT_WORKFLOW.md` → `docs/development/DEVELOPMENT_WORKFLOW.md`
- `TDD_CHECKLIST.md` → `docs/development/TDD_CHECKLIST.md`
- `QUICK_REFERENCE.md` → `docs/development/QUICK_REFERENCE.md`
- `ERROR_RECOVERY.md` → `docs/development/ERROR_RECOVERY.md`
- `TERMINAL_SETUP_GUIDE_2025_05_18.md` → `docs/development/TERMINAL_SETUP_GUIDE_2025_05_18.md`

#### Architecture Documentation → `docs/architecture/`
- `AI_AGENTS_IMPLEMENTATION.md` → `docs/architecture/AI_AGENTS_IMPLEMENTATION.md`
- `backend_api_design.md` → `docs/architecture/backend_api_design.md`
- `building_block_system_design_backend_api.md` → `docs/architecture/building_block_system_design_backend_api.md`
- `implementation_recommendations_backend_api.md` → `docs/architecture/implementation_recommendations_backend_api.md`
- `platform_documentation_combined.md` → `docs/architecture/platform_documentation_combined.md`
- `platform_documentation_for_claude.md` → `docs/architecture/platform_documentation_for_claude.md`

#### Project Documentation → `docs/project/`
- `PROJECT_STATUS.md` → `docs/project/PROJECT_STATUS.md`
- `IMPLEMENTATION_SEQUENCE.md` → `docs/project/IMPLEMENTATION_SEQUENCE.md`
- `BUSINESS_VALUE_PROPOSITION.md` → `docs/project/BUSINESS_VALUE_PROPOSITION.md`
- `PARALLEL_DEVELOPMENT_PLAN_2025_05_18.md` → `docs/project/PARALLEL_DEVELOPMENT_PLAN_2025_05_18.md`
- `TECHNICAL_CONFIDENCE.md` → `docs/project/TECHNICAL_CONFIDENCE.md`
- `AGENT_WORKFLOW_EXAMPLES.md` → `docs/project/AGENT_WORKFLOW_EXAMPLES.md`

### Script Files

#### Debug Scripts → `scripts/debug/`
- `debug_profiler.py` → `scripts/debug/debug_profiler.py`
- `debug_categorical.py` → `scripts/debug/debug_categorical.py`
- `debug_mixed_dates.py` → `scripts/debug/debug_mixed_dates.py`
- `debug_outliers.py` → `scripts/debug/debug_outliers.py`
- `debug_single_row.py` → `scripts/debug/debug_single_row.py`

#### Data Generation Scripts → `scripts/data/`
- `testdata_generator.py` → `scripts/data/testdata_generator.py`
- `business_analysis_platform.py` → `scripts/data/business_analysis_platform.py` (old Streamlit version)

### Data Files

#### Sample Data → `data/samples/`
- `business_analysis_test_data.csv` → `data/samples/business_analysis_test_data.csv`

### Test Files

Several test files that were in the root directory have been moved to their appropriate test subdirectories:
- `test_assertion.py` → `tests/test_building_blocks/data/test_assertion.py`
- `test_building_blocks.py` → `tests/test_building_blocks/test_building_blocks.py`
- `test_integration.py` → `tests/test_integration/test_integration.py`
- `test_template_integration.py` → `tests/test_integration/test_template_integration.py`
- `test_template_manager.py` → `tests/test_templates/test_template_manager.py`
- `test_templates.py` → `tests/test_templates/test_templates.py`

## Import Changes Required

### For Debug Scripts

All debug scripts in `scripts/debug/` now include path setup at the top:
```python
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
```

### For Test Files

Several test files need import updates:

#### Old Import Pattern:
```python
from business_analysis_platform import SomeClass
from goob_ai.module import AnotherClass
```

#### New Import Pattern:
```python
# For modules in src/
from src.module.submodule import SomeClass

# For goob_ai modules
from src.goob_ai.module import AnotherClass
```

### Specific Import Fixes Needed:

1. **Tests using `business_analysis_platform` imports:**
   - `tests/test_building_blocks/test_building_blocks.py`
   - `tests/test_integration/test_integration.py`
   - `tests/test_integration/test_template_integration.py`
   - `tests/test_templates/test_template_manager.py`
   - `tests/test_templates/test_templates.py`
   
   These tests are importing from the old monolithic `business_analysis_platform.py` file which has been moved to `scripts/data/`. The imports need to be updated to use the new modular structure in `src/`.

2. **Tests using `goob_ai` imports:**
   - `tests/demo/test_example_demo.py`
   - `tests/demo/test_executive_demo.py`
   
   Change: `from goob_ai.` → `from src.goob_ai.`

## Configuration Changes

### Environment Variables

A new `.env.example` file has been created with all required environment variables. Copy this to `.env` and update with your values:
```bash
cp .env.example .env
```

### File Path Updates

The `testdata_generator.py` script now outputs to the correct location:
```python
output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
                          'data', 'samples', 'business_analysis_test_data.csv')
```

## Finding Documentation

All documentation is now organized in the `docs/` directory:
- **Development guides**: `docs/development/`
- **Architecture docs**: `docs/architecture/`
- **Project management**: `docs/project/`

A comprehensive index is available at `docs/README.md`.

## Git History

All documentation moves were done using `git mv` to preserve history. Script and data file moves were done with regular `mv` as they weren't tracked in git.

## Next Steps

1. Update any remaining imports in test files (see "Import Changes Required" section)
2. Update any scripts or configurations that reference the old file paths
3. Review and update any CI/CD pipelines that may reference old paths
4. Update any external documentation or wikis that link to these files

## Troubleshooting

If you encounter import errors:
1. Check if the module has moved - use the file movement list above
2. Update imports to use the `src.` prefix for application code
3. For scripts in subdirectories, ensure proper path setup is included
4. Check that `__init__.py` files exist in all package directories

If you can't find a file:
1. Check the file movement list above
2. Use `find . -name "filename"` to search
3. Check if it was renamed during the move
4. Look in the git history: `git log --follow -- filename`