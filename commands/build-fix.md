# Build and Fix

Incrementally fix Python linting and runtime errors:

1. Run checks:
   ```bash
   # Lint check
   poetry run ruff check .
   
   # Format check
   poetry run black --check .
   
   # Test
   poetry run pytest
   ```

2. Parse error output:
   - Group by file
   - Sort by severity

3. For each error:
   - Show error context (5 lines before/after)
   - Explain the issue
   - Propose fix
   - Apply fix
   - Re-run checks
   - Verify error resolved

4. Common Python errors and fixes:

   **Import Errors:**
   - Missing module: `poetry add <package>`
   - Circular import: Reorganize code or use TYPE_CHECKING guard
   
   **Type Errors:**
   - Missing annotations: Add type hints (use modern syntax: `str | None`)
   - Type mismatch: Fix the type or add proper handling
   
   **Lint Errors (Ruff):**
   - Unused imports: Remove them
   - Line too long: Break into multiple lines
   - Missing docstring: Add docstring

5. Stop if:
   - Fix introduces new errors
   - Same error persists after 3 attempts
   - User requests pause

6. Show summary:
   - Errors fixed
   - Errors remaining
   - New errors introduced

7. Auto-format after fixes:
   ```bash
   poetry run ruff format .
   poetry run black .
   ```

Fix one error at a time for safety!
