---
name: tdd-workflow
description: Use this skill when writing new features, fixing bugs, or refactoring code. Enforces test-driven development with 80%+ coverage including unit and integration tests.
---

# Test-Driven Development Workflow

This skill ensures all code development follows TDD principles with comprehensive test coverage.

## When to Activate

- Writing new features or functionality
- Fixing bugs or issues
- Refactoring existing code
- Adding API endpoints
- Creating new services

## Core Principles

### 1. Tests BEFORE Code
ALWAYS write tests first, then implement code to make tests pass.

### 2. Coverage Requirements
- Minimum 80% coverage (unit + integration)
- All edge cases covered
- Error scenarios tested
- Boundary conditions verified

### 3. Test Types

#### Unit Tests
- Individual functions and utilities
- Service methods
- Pure functions
- Helpers and validators

#### Integration Tests
- API endpoints
- Database operations
- Service interactions
- External API calls (mocked)

## TDD Workflow Steps

### Step 1: Write User Journeys
```
As a [role], I want to [action], so that [benefit]

Example:
As a user, I want to create a new report,
so that I can track my daily metrics.
```

### Step 2: Generate Test Cases
For each user journey, create comprehensive test cases:

```python
import pytest
from httpx import AsyncClient
from app.main import app

class TestReportCreation:
    @pytest.mark.asyncio
    async def test_creates_report_successfully(self):
        """Test successful report creation."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/reports",
                json={"title": "Daily Report", "date": "2024-01-15"}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["data"]["title"] == "Daily Report"
    
    @pytest.mark.asyncio
    async def test_returns_error_for_empty_title(self):
        """Test validation error for empty title."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/reports",
                json={"title": "", "date": "2024-01-15"}
            )
            assert response.status_code == 422
    
    @pytest.mark.asyncio
    async def test_returns_error_for_invalid_date(self):
        """Test validation error for invalid date format."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/reports",
                json={"title": "Report", "date": "invalid"}
            )
            assert response.status_code == 422
```

### Step 3: Run Tests (They Should Fail)
```bash
poetry run pytest tests/test_reports.py -v
# Tests should fail - we haven't implemented yet
```

### Step 4: Implement Code
Write minimal code to make tests pass:

```python
from fastapi import APIRouter
from pydantic import BaseModel, Field
from datetime import date
from aimate.contracts import AIMateAPIResponse

router = APIRouter()

class CreateReportInput(BaseModel):
    title: str = Field(min_length=1)
    date: date

class Report(BaseModel):
    id: str
    title: str
    date: date

@router.post("/reports")
async def create_report(data: CreateReportInput) -> AIMateAPIResponse[Report]:
    # Implementation here
    report = await report_service.create(data)
    return AIMateAPIResponse(data=report)
```

### Step 5: Run Tests Again
```bash
poetry run pytest tests/test_reports.py -v
# Tests should now pass
```

### Step 6: Refactor
Improve code quality while keeping tests green:
- Remove duplication
- Improve naming
- Optimize performance
- Enhance readability

### Step 7: Verify Coverage
```bash
poetry run pytest --cov=app --cov-report=html
# Verify 80%+ coverage achieved
```

## Testing Patterns

### Unit Test Pattern (pytest)
```python
import pytest
from app.services.report_service import calculate_metrics

class TestCalculateMetrics:
    def test_returns_correct_average(self):
        values = [10, 20, 30]
        result = calculate_metrics(values)
        assert result["average"] == 20.0
    
    def test_handles_empty_list(self):
        result = calculate_metrics([])
        assert result["average"] == 0.0
    
    def test_handles_single_value(self):
        result = calculate_metrics([42])
        assert result["average"] == 42.0
```

### API Integration Test Pattern
```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

class TestUsersAPI:
    @pytest.mark.asyncio
    async def test_get_user_returns_200(self, client):
        response = await client.get("/api/users/123")
        assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_get_user_returns_404_for_unknown(self, client):
        response = await client.get("/api/users/unknown")
        assert response.status_code == 404
        data = response.json()
        assert data["error"]["code"] == "USER_NOT_FOUND"
```

### Database Test Pattern
```python
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.repositories import UserRepository

@pytest.fixture
async def db_session(test_engine):
    async with AsyncSession(test_engine) as session:
        yield session
        await session.rollback()

@pytest.fixture
async def user_repo(db_session):
    return UserRepository(db_session)

class TestUserRepository:
    @pytest.mark.asyncio
    async def test_creates_user(self, user_repo):
        user = await user_repo.create({
            "email": "test@example.com",
            "name": "Test User"
        })
        assert user.id is not None
        assert user.email == "test@example.com"
    
    @pytest.mark.asyncio
    async def test_finds_user_by_email(self, user_repo):
        await user_repo.create({
            "email": "find@example.com",
            "name": "Find Me"
        })
        user = await user_repo.find_by_email("find@example.com")
        assert user is not None
        assert user.name == "Find Me"
```

## Mocking External Services

### Mock with pytest-mock
```python
import pytest
from unittest.mock import AsyncMock

@pytest.fixture
def mock_openai(mocker):
    mock = AsyncMock()
    mock.return_value = {"response": "mocked"}
    mocker.patch("app.services.ai_service.openai_client.chat", mock)
    return mock

@pytest.mark.asyncio
async def test_ai_service_calls_openai(mock_openai):
    result = await ai_service.generate_response("test")
    mock_openai.assert_called_once()
    assert result is not None
```

### Mock Database
```python
@pytest.fixture
def mock_session(mocker):
    session = AsyncMock()
    session.execute.return_value.scalars.return_value.all.return_value = [
        User(id=1, email="test@test.com", name="Test")
    ]
    return session
```

## Test File Organization

```
tests/
├── conftest.py              # Shared fixtures
├── test_users.py            # User API tests
├── test_reports.py          # Report API tests
├── unit/
│   ├── test_validators.py   # Unit tests for validators
│   └── test_utils.py        # Unit tests for utilities
└── integration/
    ├── test_user_api.py     # Integration tests for user API
    └── test_database.py     # Database integration tests
```

## Running Tests

```bash
# Run all tests
poetry run pytest

# With coverage
poetry run pytest --cov=app --cov-report=html

# Specific test file
poetry run pytest tests/test_users.py -v

# Run only marked tests
poetry run pytest -m "not slow"

# Run with output
poetry run pytest -v -s
```

## Coverage Thresholds

Configure in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"

[tool.coverage.run]
source = ["app"]
branch = true

[tool.coverage.report]
fail_under = 80
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
]
```

## Common Testing Mistakes to Avoid

### ❌ WRONG: Testing Implementation Details
```python
# Don't test internal state
assert service._internal_cache == {}
```

### ✅ CORRECT: Test Behavior
```python
# Test what the function returns/does
result = await service.get_data()
assert result == expected_data
```

### ❌ WRONG: Tests Depend on Each Other
```python
# Tests share state
test_creates_user()  # Creates user
test_updates_same_user()  # Depends on previous test
```

### ✅ CORRECT: Independent Tests
```python
# Each test sets up its own data
@pytest.fixture
async def test_user(db_session):
    return await create_test_user(db_session)
```

## Best Practices

1. **Write Tests First** - Always TDD
2. **One Assert Per Test** - Focus on single behavior
3. **Descriptive Test Names** - Explain what's tested
4. **Arrange-Act-Assert** - Clear test structure
5. **Mock External Dependencies** - Isolate unit tests
6. **Test Edge Cases** - None, empty, invalid, large
7. **Test Error Paths** - Not just happy paths
8. **Keep Tests Fast** - Unit tests < 50ms each
9. **Clean Up After Tests** - No side effects
10. **Review Coverage Reports** - Identify gaps

**Remember**: Tests are not optional. They are the safety net that enables confident refactoring, rapid development, and production reliability.
