# Test Coverage

Analyze test coverage and generate missing tests:

1. Run tests with coverage:
   ```bash
   poetry run pytest --cov=app --cov-report=html --cov-report=term-missing
   ```

2. Analyze coverage report (htmlcov/index.html or terminal output)

3. Identify files below 80% coverage threshold

4. For each under-covered file:
   - Analyze untested code paths
   - Generate unit tests for functions
   - Generate integration tests for APIs
   - Focus on edge cases and error paths

5. Verify new tests pass:
   ```bash
   poetry run pytest tests/test_new_file.py -v
   ```

6. Show before/after coverage metrics

7. Ensure project reaches 80%+ overall coverage

## Focus Areas

**Happy path scenarios:**
- Normal successful operations
- Expected inputs and outputs

**Error handling:**
- Exception cases
- Invalid inputs
- External service failures

**Edge cases:**
- None values
- Empty collections
- Boundary values (0, max int, etc.)

**Boundary conditions:**
- List with 0, 1, many items
- String length limits
- Numeric ranges

## Coverage Configuration

In `pyproject.toml`:

```toml
[tool.coverage.run]
source = ["app"]
branch = true
omit = ["tests/*", "alembic/*"]

[tool.coverage.report]
fail_under = 80
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
]
```

## Quick Commands

```bash
# Run with coverage
poetry run pytest --cov=app

# Generate HTML report
poetry run pytest --cov=app --cov-report=html

# Show missing lines
poetry run pytest --cov=app --cov-report=term-missing

# Check if coverage meets threshold
poetry run pytest --cov=app --cov-fail-under=80
```
