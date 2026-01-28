---
description: Enforce test-driven development workflow. Scaffold Pydantic models, generate tests FIRST with pytest, then implement minimal code to pass. Ensure 80%+ coverage.
---

# TDD Command

This command invokes the **tdd-guide** agent to enforce test-driven development methodology.

## What This Command Does

1. **Scaffold Models** - Define Pydantic models first
2. **Generate Tests First** - Write failing tests (RED)
3. **Implement Minimal Code** - Write just enough to pass (GREEN)
4. **Refactor** - Improve code while keeping tests green (REFACTOR)
5. **Verify Coverage** - Ensure 80%+ test coverage

## When to Use

Use `/tdd` when:
- Implementing new features
- Adding new functions/services
- Fixing bugs (write test that reproduces bug first)
- Refactoring existing code
- Building critical business logic

## How It Works

The tdd-guide agent will:

1. **Define Pydantic models** for inputs/outputs
2. **Write tests that will FAIL** (because code doesn't exist yet)
3. **Run tests** and verify they fail for the right reason
4. **Write minimal implementation** to make tests pass
5. **Run tests** and verify they pass
6. **Refactor** code while keeping tests green
7. **Check coverage** and add more tests if below 80%

## TDD Cycle

```
RED → GREEN → REFACTOR → REPEAT

RED:      Write a failing test
GREEN:    Write minimal code to pass
REFACTOR: Improve code, keep tests passing
REPEAT:   Next feature/scenario
```

## Example Usage

```
User: /tdd I need a function to calculate user engagement score

Agent (tdd-guide):
# TDD Session: User Engagement Score Calculator

## Step 1: Define Models (SCAFFOLD)

```python
# app/services/engagement.py
from pydantic import BaseModel
from datetime import datetime

class UserActivity(BaseModel):
    total_sessions: int
    avg_session_duration_minutes: float
    actions_count: int
    last_activity: datetime

def calculate_engagement_score(activity: UserActivity) -> float:
    """Calculate engagement score from 0-100."""
    raise NotImplementedError()
```

## Step 2: Write Failing Test (RED)

```python
# tests/test_engagement.py
import pytest
from datetime import datetime, timedelta
from app.services.engagement import calculate_engagement_score, UserActivity

class TestCalculateEngagementScore:
    def test_returns_high_score_for_engaged_user(self):
        activity = UserActivity(
            total_sessions=100,
            avg_session_duration_minutes=30.0,
            actions_count=500,
            last_activity=datetime.now()
        )
        
        score = calculate_engagement_score(activity)
        
        assert score > 80
        assert score <= 100
    
    def test_returns_low_score_for_inactive_user(self):
        activity = UserActivity(
            total_sessions=2,
            avg_session_duration_minutes=1.0,
            actions_count=5,
            last_activity=datetime.now() - timedelta(days=30)
        )
        
        score = calculate_engagement_score(activity)
        
        assert score < 30
        assert score >= 0
    
    def test_returns_zero_for_no_activity(self):
        activity = UserActivity(
            total_sessions=0,
            avg_session_duration_minutes=0,
            actions_count=0,
            last_activity=datetime.now() - timedelta(days=365)
        )
        
        score = calculate_engagement_score(activity)
        
        assert score == 0
```

## Step 3: Run Tests - Verify FAIL

```bash
poetry run pytest tests/test_engagement.py -v

FAILED tests/test_engagement.py::TestCalculateEngagementScore::test_returns_high_score_for_engaged_user
    NotImplementedError

1 failed, 0 passed
```

✅ Tests fail as expected. Ready to implement.

## Step 4: Implement Minimal Code (GREEN)

```python
# app/services/engagement.py
from datetime import datetime

def calculate_engagement_score(activity: UserActivity) -> float:
    """Calculate engagement score from 0-100."""
    if activity.total_sessions == 0:
        return 0.0
    
    # Session score (0-25 points)
    session_score = min(activity.total_sessions / 4, 25)
    
    # Duration score (0-25 points)
    duration_score = min(activity.avg_session_duration_minutes / 1.2, 25)
    
    # Actions score (0-25 points)
    actions_score = min(activity.actions_count / 20, 25)
    
    # Recency score (0-25 points)
    days_since_activity = (datetime.now() - activity.last_activity).days
    recency_score = max(25 - days_since_activity, 0)
    
    total = session_score + duration_score + actions_score + recency_score
    return min(max(total, 0), 100)
```

## Step 5: Run Tests - Verify PASS

```bash
poetry run pytest tests/test_engagement.py -v

PASSED tests/test_engagement.py::TestCalculateEngagementScore::test_returns_high_score_for_engaged_user
PASSED tests/test_engagement.py::TestCalculateEngagementScore::test_returns_low_score_for_inactive_user
PASSED tests/test_engagement.py::TestCalculateEngagementScore::test_returns_zero_for_no_activity

3 passed
```

✅ All tests passing!

## Step 6: Check Coverage

```bash
poetry run pytest --cov=app/services/engagement --cov-report=term-missing

Name                          Stmts   Miss  Cover
-------------------------------------------------
app/services/engagement.py       15      0   100%

Coverage: 100% ✅ (Target: 80%)
```

✅ TDD session complete!
```

## TDD Best Practices

**DO:**
- ✅ Write the test FIRST, before any implementation
- ✅ Run tests and verify they FAIL before implementing
- ✅ Write minimal code to make tests pass
- ✅ Refactor only after tests are green
- ✅ Add edge cases and error scenarios
- ✅ Aim for 80%+ coverage (100% for critical code)

**DON'T:**
- ❌ Write implementation before tests
- ❌ Skip running tests after each change
- ❌ Write too much code at once
- ❌ Ignore failing tests
- ❌ Test implementation details (test behavior)
- ❌ Mock everything (prefer integration tests)

## Test Types to Include

**Unit Tests** (Function-level):
- Happy path scenarios
- Edge cases (None, empty, max values)
- Error conditions
- Boundary values

**Integration Tests** (API-level):
- API endpoints with AsyncClient
- Database operations
- External service calls (mocked)

## Coverage Requirements

- **80% minimum** for all code
- **100% required** for:
  - Financial calculations
  - Authentication logic
  - Security-critical code
  - Core business logic

## Running Tests

```bash
# Run all tests
poetry run pytest

# With coverage
poetry run pytest --cov=app --cov-report=html

# Specific file
poetry run pytest tests/test_engagement.py -v

# Watch mode (with pytest-watch)
poetry run ptw
```

## Integration with Other Commands

- Use `/plan` first to understand what to build
- Use `/tdd` to implement with tests
- Use `/build-fix` if lint/type errors occur
- Use `/code-review` to review implementation
- Use `/test-coverage` to verify coverage

## Related Agents

This command invokes the `tdd-guide` agent located at:
`~/.claude/agents/tdd-guide.md`

And can reference the `tdd-workflow` skill at:
`~/.claude/skills/tdd-workflow/`
