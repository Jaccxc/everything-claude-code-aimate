# Code Review

Comprehensive security and quality review of uncommitted changes:

1. Get changed files: git diff --name-only HEAD

2. For each changed Python file, check for:

**Security Issues (CRITICAL):**
- Hardcoded credentials, API keys, tokens
- SQL injection vulnerabilities (raw queries without parameterization)
- Missing input validation
- Insecure dependencies
- Path traversal risks
- Improper exception handling exposing internals

**Code Quality (HIGH):**
- Functions > 50 lines
- Files > 800 lines
- Nesting depth > 4 levels
- Missing error handling (no try/except, no ServiceError)
- print() statements (use logger instead)
- TODO/FIXME comments
- Missing docstrings for public APIs
- Missing type annotations
- Using legacy typing (Optional, List, Dict) instead of modern syntax (str | None, list, dict)

**Best Practices (MEDIUM):**
- Missing Pydantic models for data validation
- Not using ServiceError for error handling
- Not using AIMateAPIResponse/VbenResponse for endpoints
- Missing tests for new code
- Unused imports
- Not following repository/service pattern

3. Generate report with:
   - Severity: CRITICAL, HIGH, MEDIUM, LOW
   - File location and line numbers
   - Issue description
   - Suggested fix

4. Block commit if CRITICAL or HIGH issues found

5. Run lint check for issues:
   ```bash
   poetry run ruff check .
   poetry run black --check .
   ```

Never approve code with security vulnerabilities!
