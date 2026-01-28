# Security Guidelines

## Mandatory Security Checks

Before ANY commit:
- [ ] No hardcoded secrets (API keys, passwords, tokens)
- [ ] All user inputs validated (Pydantic models)
- [ ] SQL injection prevention (SQLAlchemy ORM / parameterized queries)
- [ ] Authentication/authorization verified
- [ ] Rate limiting on all endpoints
- [ ] Error messages don't leak sensitive data
- [ ] CORS properly configured

## Secret Management

```python
# NEVER: Hardcoded secrets
api_key = "sk-proj-xxxxx"

# ALWAYS: Environment variables with pydantic-settings
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    database_url: str
    secret_key: str
    
    class Config:
        env_file = ".env"

settings = Settings()

# Use settings.openai_api_key
```

## Input Validation

```python
from pydantic import BaseModel, Field, validator

class UserInput(BaseModel):
    email: str
    password: str = Field(min_length=8)
    
    @validator("email")
    def validate_email(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email format")
        return v.lower()
```

## SQL Injection Prevention

```python
# NEVER: String formatting
query = f"SELECT * FROM users WHERE email = '{email}'"

# ALWAYS: SQLAlchemy ORM
from sqlalchemy import select

stmt = select(User).where(User.email == email)
result = await session.execute(stmt)

# Or parameterized queries
stmt = text("SELECT * FROM users WHERE email = :email")
result = await session.execute(stmt, {"email": email})
```

## Environment Variables

Required in `.env`:
```
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/db
OPENAI_API_KEY=sk-...
SECRET_KEY=your-secret-key
```

Never commit `.env` files. Use `.env.example` as template.

## Security Response Protocol

If security issue found:
1. STOP immediately
2. Use **security-reviewer** agent
3. Fix CRITICAL issues before continuing
4. Rotate any exposed secrets
5. Review entire codebase for similar issues
