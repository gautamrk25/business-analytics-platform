# create-building-block

Create a new building block following the established patterns and best practices.

## Usage
```
/project:create-building-block <block_name> <category>
```

## Steps
1. Generate building block class from template
2. Add type hints and comprehensive docstrings
3. Implement required abstract methods
4. Add error handling and logging
5. Create corresponding unit tests
6. Register block in the registry
7. Update documentation

## Example
```
/project:create-building-block CustomerSegmentation analysis
```

This will create a new CustomerSegmentation building block in the analysis category with all required methods and corresponding tests.