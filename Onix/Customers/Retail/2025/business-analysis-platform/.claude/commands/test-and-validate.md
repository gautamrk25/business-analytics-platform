# test-and-validate

Run tests and validate code quality for the business analysis platform.

## Usage
```
/project:test-and-validate [component]
```

## Steps
1. Activate virtual environment
2. Run unit tests for specified component (or all)
3. Check type hints with mypy (if available)
4. Verify code style with linting tools
5. Run integration tests
6. Generate test coverage report
7. Display summary of results

## Examples
```
/project:test-and-validate
/project:test-and-validate building_blocks
/project:test-and-validate templates
```

This ensures code quality and catches issues before deployment.