# Coding Style

## Modern Type Hints (REQUIRED)

使用現代 Python 3.10+ 語法：

```python
# ✅ CORRECT: Modern syntax
name: str | None = None
items: list[str] = []
mapping: dict[str, int] = {}

# ❌ WRONG: Legacy typing
from typing import Optional, List, Dict
name: Optional[str] = None
items: List[str] = []
mapping: Dict[str, int] = {}
```

## Pydantic Models (REQUIRED for all data)

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

## File Organization

MANY SMALL FILES > FEW LARGE FILES:
- High cohesion, low coupling
- 200-400 lines typical, 800 max
- Extract utilities from large modules
- Organize by feature/domain, not by type

## Error Handling

使用 ServiceError pattern：

```python
from fastapi import status
from app.exceptions import ServiceError
from app.contracts import AIMateErrorCode

async def get_user(user_id: str) -> User:
    user = await user_repo.find_by_id(user_id)
    if not user:
        raise ServiceError(
            message=f"User {user_id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            code=AIMateErrorCode.NOT_FOUND,
        )
    return user
```

## Input Validation

ALWAYS validate with Pydantic：

```python
from pydantic import BaseModel, Field, EmailStr, field_validator

class UserInput(BaseModel):
    email: EmailStr
    age: int = Field(ge=0, le=150)
    name: str = Field(min_length=1, max_length=100)
    
    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()
```

## Code Quality Checklist

Before marking work complete:
- [ ] Code is readable and well-named
- [ ] Functions are small (<50 lines)
- [ ] Files are focused (<800 lines)
- [ ] No deep nesting (>4 levels)
- [ ] Proper error handling with ServiceError
- [ ] No print() statements (use logger)
- [ ] No hardcoded values
- [ ] Type hints on all functions (modern syntax)
- [ ] Pydantic models for data validation

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
