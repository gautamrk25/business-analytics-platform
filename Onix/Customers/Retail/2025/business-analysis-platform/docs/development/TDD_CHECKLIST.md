# Test-Driven Development Checklist

## IMPORTANT: This checklist MUST be followed for all new code

### Pre-Development Phase
- [ ] Understand the requirements completely
- [ ] Create test file in appropriate location (`tests/test_building_blocks/test_<name>.py`)
- [ ] Write test class with descriptive name
- [ ] Create fixtures for common test data

### Writing Tests (Red Phase)
- [ ] Write test for initialization/construction
- [ ] Write test for successful execution (happy path)
- [ ] Write tests for error conditions
- [ ] Write tests for edge cases
- [ ] Write tests for input validation
- [ ] Write performance tests if applicable
- [ ] Run tests to ensure they fail appropriately

### Implementation (Green Phase)
- [ ] Create source file in correct location (`src/building_blocks/<category>/<name>.py`)
- [ ] Implement minimum code to make tests pass
- [ ] Focus on one test at a time
- [ ] Run tests after each change
- [ ] Commit when all tests pass

### Refactoring (Refactor Phase)
- [ ] Improve code structure while keeping tests green
- [ ] Extract common functionality
- [ ] Improve naming and documentation
- [ ] Check code coverage (minimum 80%)
- [ ] Run all tests again

### Documentation
- [ ] Add comprehensive docstrings
- [ ] Update CHANGELOG if applicable
- [ ] Add usage examples to documentation
- [ ] Update README if needed

### Final Verification
- [ ] All tests pass
- [ ] Coverage meets requirements (80% minimum)
- [ ] Code follows style guide
- [ ] No hardcoded values or secrets
- [ ] Error handling is comprehensive
- [ ] Logging is appropriate

### Before Committing
- [ ] Run full test suite: `python -m pytest tests/ -v`
- [ ] Check coverage: `python -m pytest tests/ --cov=src --cov-report=term`
- [ ] Verify no linting errors
- [ ] Update documentation if needed

## Example TDD Workflow

```bash
# 1. Create test file first
touch tests/test_building_blocks/test_my_new_block.py

# 2. Write comprehensive tests
# ... implement tests ...

# 3. Run tests (should fail)
python -m pytest tests/test_building_blocks/test_my_new_block.py -v

# 4. Create implementation
touch src/building_blocks/analysis/my_new_block.py

# 5. Implement functionality
# ... implement code ...

# 6. Run tests until they pass
python -m pytest tests/test_building_blocks/test_my_new_block.py -v

# 7. Check coverage
python -m pytest tests/test_building_blocks/test_my_new_block.py --cov=src/building_blocks/analysis/my_new_block

# 8. Run full test suite
python -m pytest tests/ -v
```

## Red Flags - When to Stop and Reassess

- Tests are difficult to write (may indicate poor design)
- Too many mocks required (may indicate tight coupling)
- Tests are brittle and break with minor changes
- Coverage is below 80% after implementation
- Tests take too long to run (>1 second per test)

## Best Practices

1. **One assertion per test** - Each test should verify one behavior
2. **Descriptive test names** - Test names should explain what they verify
3. **Arrange-Act-Assert** - Follow this pattern in test structure
4. **Use fixtures** - Share common setup between tests
5. **Test behavior, not implementation** - Tests should survive refactoring
6. **Fast tests** - Unit tests should run in milliseconds

Remember: If you're not writing tests first, you're not doing TDD!