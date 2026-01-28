---
name: verification-loop
description: Multi-layer verification ensuring code quality, correctness, and security. Run after any significant code changes.
---

# Verification Loop

Multi-layer verification process ensuring code quality, correctness, and security. Run this after any significant code changes.

## Prerequisites

Before starting verification:
- Code changes are complete
- All imports are available
- Dependencies are installed

## Layer 1: Static Analysis (Fast)

Run quick checks that don't require execution:

```bash
# Lint check
poetry run ruff check . --output-format=grouped

# Format check  
poetry run black --check .

# If errors found, auto-fix
poetry run ruff check . --fix
poetry run black .
```

## Layer 2: Unit Tests (Medium)

Run focused unit tests:

```bash
# Run tests for changed files
poetry run pytest tests/ -x --tb=short

# With coverage
poetry run pytest tests/ --cov=app --cov-report=term-missing
```

## Layer 3: Integration Tests (Slower)

Run broader integration tests:

```bash
# All tests including integration
poetry run pytest -x

# Specific integration tests
poetry run pytest tests/integration/ -x
```

## Layer 4: Manual Verification

For changes that affect user experience:
- Test in browser (for frontend changes)
- Verify API responses (for backend changes)
- Check database migrations (for schema changes)

## Decision Tree

```
Start Verification
        │
        ▼
┌───────────────┐
│ ruff check    │ ──errors──▶ Fix and retry
└───────────────┘
        │ pass
        ▼
┌───────────────┐
│ black --check │ ──errors──▶ Run black and retry
└───────────────┘
        │ pass
        ▼
┌───────────────┐
│ pytest -x     │ ──fail────▶ Fix tests
└───────────────┘
        │ pass
        ▼
    ✓ VERIFIED
```

## Recovery Actions

### Lint Errors
```bash
# Auto-fix what's possible
poetry run ruff check . --fix

# Manual fix remaining issues
```

### Type Errors
Review the error message and fix the type annotation or the code logic.

### Test Failures
```bash
# Run specific failing test with verbose output
poetry run pytest tests/path/to/test.py::test_name -v --tb=long
```

### Import Errors
```bash
# Check if package is installed
poetry show package-name

# Add missing package
poetry add package-name
```

## Verification Checklist

Before marking work complete:

- [ ] `poetry run ruff check .` passes
- [ ] `poetry run black --check .` passes
- [ ] `poetry run pytest` passes
- [ ] No print() statements in production code
- [ ] Type hints on all functions (modern syntax)
- [ ] Proper error handling with ServiceError
- [ ] Coverage meets requirements (80%+)

## Quick Reference

| Check Type | Command | Time |
|------------|---------|------|
| Lint | `poetry run ruff check .` | ~1s |
| Format | `poetry run black --check .` | ~1s |
| Unit Tests | `poetry run pytest -x` | ~5-30s |
| Coverage | `poetry run pytest --cov=app` | ~10-60s |

**Remember**: Verification is faster than debugging production issues. Always run the full loop before committing.
