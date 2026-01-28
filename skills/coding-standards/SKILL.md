---
name: coding-standards
description: Universal coding standards, best practices, and patterns for Python, FastAPI, Pydantic, and SQLAlchemy development.
---

# Coding Standards & Best Practices

Universal coding standards applicable across all AIMate Python projects.

## Code Quality Principles

### 1. Readability First
- Code is read more than written
- Clear variable and function names
- Self-documenting code preferred over comments
- Consistent formatting (ruff + black via poetry run)

### 2. KISS (Keep It Simple, Stupid)
- Simplest solution that works
- Avoid over-engineering
- No premature optimization
- Easy to understand > clever code

### 3. DRY (Don't Repeat Yourself)
- Extract common logic into functions
- Create reusable services
- Share utilities across modules
- Avoid copy-paste programming

### 4. YAGNI (You Aren't Gonna Need It)
- Don't build features before they're needed
- Avoid speculative generality
- Add complexity only when required
- Start simple, refactor when needed

## Python Standards

### Modern Type Hints (REQUIRED)

```python
# ✅ CORRECT: Modern Python 3.10+ syntax
name: str | None = None
items: list[str] = []
mapping: dict[str, int] = {}
callback: Callable[[str], int] | None = None

# ❌ WRONG: Legacy typing module
from typing import Optional, List, Dict, Callable
name: Optional[str] = None
items: List[str] = []
mapping: Dict[str, int] = {}
```

### Variable Naming

```python
# ✅ GOOD: Descriptive names (snake_case)
market_search_query = "election"
is_user_authenticated = True
total_revenue = 1000.0

# ❌ BAD: Unclear names
q = "election"
flag = True
x = 1000
```

### Function Naming

```python
# ✅ GOOD: Verb-noun pattern (snake_case)
async def fetch_market_data(market_id: str) -> Market:
    ...

def calculate_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    ...

def is_valid_email(email: str) -> bool:
    ...

# ❌ BAD: Unclear or noun-only
async def market(id):
    ...

def similarity(a, b):
    ...
```

### Pydantic Models (REQUIRED for all data)

```python
from pydantic import BaseModel, Field

class CreateUserInput(BaseModel):
    email: str
    name: str = Field(min_length=1, max_length=100)
    age: int | None = None
    tags: list[str] = []
    metadata: dict[str, str] = {}

class User(BaseModel):
    id: str
    email: str
    name: str
    created_at: datetime
```

### Error Handling with ServiceError

```python
from fastapi import status
from app.exceptions import ServiceError
from app.contracts import AIMateErrorCode

async def get_user(user_id: str) -> User:
    try:
        user = await user_repo.find_by_id(user_id)
    except DatabaseError as e:
        logger.exception(f"Database error: {e}")
        raise ServiceError(
            message="Database error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code=AIMateErrorCode.INTERNAL_ERROR,
        )
    
    if not user:
        raise ServiceError(
            message=f"User {user_id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            code=AIMateErrorCode.NOT_FOUND,
        )
    return user
```

### Async/Await Best Practices

```python
import asyncio

# ✅ GOOD: Parallel execution when possible
users, markets, stats = await asyncio.gather(
    fetch_users(),
    fetch_markets(),
    fetch_stats()
)

# ❌ BAD: Sequential when unnecessary
users = await fetch_users()
markets = await fetch_markets()
stats = await fetch_stats()
```

## FastAPI Standards

### Router with ServiceError Pattern

```python
from fastapi import APIRouter, Depends, status
from app.exceptions import ServiceError
from app.contracts import AIMateErrorCode, VbenResponse

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/{user_id}", response_model=VbenResponse[User])
async def get_user(
    user_id: str,
    service: UserService = Depends(get_user_service)
) -> VbenResponse[User]:
    user = await service.get_by_id(user_id)
    if not user:
        raise ServiceError(
            message=f"User {user_id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            code=AIMateErrorCode.NOT_FOUND,
        )
    return VbenResponse(code=0, message="ok", data=user)
```

### Dependency Injection

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session

async def get_user_service(
    db: AsyncSession = Depends(get_db)
) -> UserService:
    return UserService(UserRepository(db))
```

## SQLAlchemy Standards

### Model Definition

```python
from sqlalchemy import String, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
```

### Repository Pattern

```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def find_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def create(self, data: CreateUserInput) -> User:
        user = User(**data.model_dump())
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
```

## Code Formatting

使用 ruff + black (透過 poetry run)：

```bash
# Format code
poetry run ruff format .
poetry run black .

# Check lint
poetry run ruff check .

# Auto-fix lint issues
poetry run ruff check . --fix
```

## File Organization

### Project Structure

```
app/
├── __init__.py
├── main.py                 # FastAPI application factory
├── config.py               # Settings with pydantic-settings
├── models.py               # SQLAlchemy models
├── exceptions.py           # ServiceError and custom exceptions
├── contracts.py            # AIMateErrorCode, response types
├── routers/                # FastAPI routers
├── services/               # Business logic
├── repositories/           # Data access layer
├── core/                   # Core infrastructure
└── utils/                  # Helper functions
```

## Code Smell Detection

### 1. Long Functions
```python
# ❌ BAD: Function > 50 lines
def process_market_data():
    # 100 lines of code
    ...

# ✅ GOOD: Split into smaller functions
def process_market_data():
    validated = validate_data()
    transformed = transform_data(validated)
    return save_data(transformed)
```

### 2. Deep Nesting
```python
# ❌ BAD: 5+ levels of nesting
if user:
    if user.is_admin:
        if market:
            if market.is_active:
                ...

# ✅ GOOD: Early returns with ServiceError
if not user:
    raise ServiceError(...)
if not user.is_admin:
    raise ServiceError(...)
if not market:
    raise ServiceError(...)
if not market.is_active:
    raise ServiceError(...)

# Do something
```

### 3. Magic Numbers
```python
# ❌ BAD: Unexplained numbers
if retry_count > 3:
    ...
await asyncio.sleep(0.5)

# ✅ GOOD: Named constants
MAX_RETRIES = 3
DEBOUNCE_DELAY_SECONDS = 0.5

if retry_count > MAX_RETRIES:
    ...
await asyncio.sleep(DEBOUNCE_DELAY_SECONDS)
```

**Remember**: Code quality is not negotiable. Clear, maintainable code enables rapid development and confident refactoring.
