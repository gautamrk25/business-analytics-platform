# Error Recovery Guide

## How to Handle Common Development Issues

### Test Failures

#### Symptom: Tests fail after implementation
```bash
FAILED tests/test_component.py::TestComponent::test_something
```

**Recovery Steps:**
```
Claude, tests are failing. Please:
1. Show me the full error message
2. Identify which test is failing and why
3. Show the relevant code section
4. Fix the implementation
5. Run the specific test again
6. Continue until it passes
```

#### Symptom: Import errors in tests
```python
ImportError: cannot import name 'Component' from 'src.module'
```

**Recovery Steps:**
```
Claude, fix the import error:
1. Check if the file exists at src/module.py
2. Verify Component class is defined
3. Check __init__.py files in path
4. Fix import statement
5. Test import in isolation
```

### Coverage Issues

#### Symptom: Coverage below 80%
```
Coverage: 65% (Required: 80%)
```

**Recovery Steps:**
```
Claude, increase test coverage:
1. Run coverage with details: pytest --cov=src/module --cov-report=term-missing
2. Identify uncovered lines
3. Add tests for missing cases:
   - Error conditions
   - Edge cases
   - Exception handling
4. Run coverage again
5. Repeat until 80%+
```

### Integration Failures

#### Symptom: Components work alone but fail together
```
FAILED tests/test_integration/test_feature.py
```

**Recovery Steps:**
```
Claude, fix integration issues:
1. Identify which components are interacting
2. Check data formats between components
3. Verify error handling at boundaries
4. Add integration tests
5. Fix implementation
6. Test both components separately and together
```

### Circular Dependencies

#### Symptom: Import errors with circular references
```
ImportError: cannot import name 'X' from partially initialized module
```

**Recovery Steps:**
```
Claude, resolve circular dependency:
1. Map out the import chain
2. Identify the circular reference
3. Refactor to break the cycle:
   - Move shared code to separate module
   - Use dependency injection
   - Restructure class hierarchy
4. Test imports work
5. Run all affected tests
```

### Configuration Errors

#### Symptom: Missing or incorrect configuration
```
KeyError: 'expected_config_key'
```

**Recovery Steps:**
```
Claude, fix configuration issue:
1. Check config.yaml for the key
2. Verify ConfigManager usage
3. Add default value if appropriate
4. Update configuration schema
5. Test configuration loading
6. Document new configuration
```

### Async/Await Issues

#### Symptom: Async function errors
```
RuntimeWarning: coroutine was never awaited
```

**Recovery Steps:**
```
Claude, fix async issue:
1. Identify the async function
2. Check all callers use await
3. Ensure test uses @pytest.mark.asyncio
4. Fix async/await chain
5. Run async tests
6. Verify no warnings
```

### Type Hint Errors

#### Symptom: Type checking failures
```
error: Argument has incompatible type
```

**Recovery Steps:**
```
Claude, fix type hints:
1. Identify the type mismatch
2. Check function signature
3. Verify actual vs expected types
4. Fix type hints or implementation
5. Run type checker if available
6. Update docstrings
```

### Performance Issues

#### Symptom: Tests timeout or run slowly
```
Test killed due to timeout
```

**Recovery Steps:**
```
Claude, fix performance issue:
1. Identify slow operations
2. Add performance benchmarks
3. Optimize:
   - Use caching
   - Reduce iterations
   - Batch operations
4. Test performance improvement
5. Document optimization
```

### Documentation Mismatch

#### Symptom: Code doesn't match documentation
```
AssertionError: Expected behavior differs from docs
```

**Recovery Steps:**
```
Claude, align code with documentation:
1. Compare implementation to docs
2. Identify discrepancies
3. Determine correct behavior
4. Fix code or documentation
5. Update examples
6. Test matches documentation
```

## Emergency Procedures

### Complete Test Suite Failure

If everything is broken:

```
Claude, perform emergency recovery:
1. Git status - check what changed
2. Run last known good test
3. Bisect to find breaking change
4. Revert problematic commit
5. Re-implement carefully
6. Test incrementally
```

### Lost Work Recovery

If work is lost:

```
Claude, recover lost work:
1. Check git reflog
2. Look for auto-save files
3. Check IDE history
4. Reconstruct from tests
5. Re-implement with TDD
```

### Environment Corruption

If environment is broken:

```
Claude, rebuild environment:
1. Deactivate virtual environment
2. Delete venv directory
3. Create new virtual environment
4. Reinstall requirements.txt
5. Verify tests run
6. Continue development
```

## Prevention Strategies

### Before Starting Work
```
Claude, before implementing:
1. Verify all dependencies built
2. Run existing tests
3. Check implementation sequence
4. Confirm requirements understood
```

### During Development
```
Claude, while implementing:
1. Run tests after each change
2. Commit working code frequently
3. Check coverage regularly
4. Test integration points
```

### After Completion
```
Claude, after implementing:
1. Run full test suite
2. Check coverage report
3. Test error scenarios
4. Update documentation
5. Commit with clear message
```

## Golden Rules

1. **Never proceed with failing tests**
2. **Fix immediately when broken**
3. **Test after every change**
4. **Commit only working code**
5. **Document recovery actions**

## Quick Commands

```bash
# Run specific test
python -m pytest tests/test_module.py::TestClass::test_method -v

# Run with debugging
python -m pytest tests/test_module.py --pdb

# Show coverage for specific module
python -m pytest tests/ --cov=src/module --cov-report=term-missing

# Run only fast tests
python -m pytest tests/ -m "not slow"

# Run tests in parallel
python -m pytest tests/ -n auto
```

Remember: Every error is a learning opportunity. Document solutions for future reference.