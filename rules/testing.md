# Testing Requirements

## Minimum Test Coverage: 80%

Test Types (ALL required):
1. **Unit Tests** - Individual functions, utilities, services
2. **Integration Tests** - API endpoints, database operations
3. **E2E Tests** - Critical user flows (when applicable)

## Test-Driven Development

MANDATORY workflow:
1. Write test first (RED)
2. Run test - it should FAIL
3. Write minimal implementation (GREEN)
4. Run test - it should PASS
5. Refactor (IMPROVE)
6. Verify coverage (80%+)

## Testing with pytest

```python
import pytest
from httpx import AsyncClient
from app.main import app

# Unit test
def test_calculate_score():
    result = calculate_score(100, 0.5)
    assert result == 50.0

# Async unit test
@pytest.mark.asyncio
async def test_fetch_user():
    user = await user_service.get_by_id("123")
    assert user is not None
    assert user.id == "123"

# API Integration test
@pytest.mark.asyncio
async def test_create_user_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/users",
            json={"email": "test@example.com", "name": "Test"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["email"] == "test@example.com"
```

## Fixtures

```python
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.fixture
async def db_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
        await session.rollback()

@pytest.fixture
async def test_user(db_session: AsyncSession) -> User:
    user = User(email="test@example.com", name="Test")
    db_session.add(user)
    await db_session.commit()
    return user
```

## Mocking

```python
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_with_mock():
    with patch("app.services.external_api.fetch") as mock_fetch:
        mock_fetch.return_value = {"status": "ok"}
        
        result = await my_service.process()
        
        assert result["status"] == "ok"
        mock_fetch.assert_called_once()
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
```

## Troubleshooting Test Failures

1. Use **tdd-guide** agent
2. Check test isolation
3. Verify mocks are correct
4. Fix implementation, not tests (unless tests are wrong)

## Agent Support

- **tdd-guide** - Use PROACTIVELY for new features, enforces write-tests-first
- **e2e-runner** - E2E testing specialist
