---
name: backend-patterns
description: Backend architecture patterns for FastAPI, SQLAlchemy, PydanticAI, async operations, and API design best practices.
---

# Backend Development Patterns

Backend architecture patterns and best practices for FastAPI-based applications.

## API Design Patterns

### RESTful API Structure

```python
# Resource-based URLs
# GET    /api/users                 # List resources
# GET    /api/users/{id}            # Get single resource
# POST   /api/users                 # Create resource
# PUT    /api/users/{id}            # Replace resource
# PATCH  /api/users/{id}            # Update resource
# DELETE /api/users/{id}            # Delete resource

# Query parameters for filtering, sorting, pagination
# GET /api/users?status=active&sort=created_at&limit=20&offset=0
```

### ServiceError Pattern (標準錯誤處理)

在 endpoint 中使用 `raise ServiceError()` 處理錯誤：

```python
from fastapi import APIRouter, Depends, status
from app.exceptions import ServiceError
from app.contracts import AIMateErrorCode, VbenResponse

router = APIRouter()

@router.get("/tasks/{task_id}", response_model=VbenResponse[dict])
async def get_task_detail(
    task_id: str,
    db: DatabaseSession,
    current_user: CurrentUser,
) -> VbenResponse[dict]:
    """查詢 task 詳情。"""
    from uuid import UUID as PyUUID

    # 驗證格式
    try:
        task_uuid = PyUUID(task_id)
    except ValueError:
        raise ServiceError(
            message="Invalid task_id format, expected UUID",
            status_code=status.HTTP_400_BAD_REQUEST,
            code=AIMateErrorCode.BAD_REQUEST,
            details={"field": "task_id"},
        )

    # 查詢資料
    task_record = await service.get_task_binding(
        db=db, user_id=current_user.id, task_id=task_uuid
    )
    if not task_record:
        raise ServiceError(
            message="Task not found or not owned by user",
            status_code=status.HTTP_404_NOT_FOUND,
            code=AIMateErrorCode.NOT_FOUND,
        )

    # 第三方 API 呼叫
    client = get_client()
    try:
        external_detail = await client.get_task_detail(task_record.external_task_id)
        return VbenResponse(
            code=0,
            message="ok",
            data={
                "local": {
                    "id": str(task_record.id),
                    "external_task_id": task_record.external_task_id,
                    "created_at": task_record.created_at.isoformat(),
                },
                "external": external_detail,
            },
        )
    except ClientError as e:
        logger.warning(f"Third-party API error: {e.message}")
        raise ServiceError(
            message=f"Third-party API error: {e.message}",
            status_code=e.status_code or status.HTTP_502_BAD_GATEWAY,
            code="THIRD_PARTY_ERROR",
            details={"source": "third_party_api", "original_error": e.message},
        )
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise ServiceError(
            message="Unexpected error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="INTERNAL_ERROR",
            details={"error_type": type(e).__name__},
        )
```

### Repository Pattern

```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class BaseRepository[T]:
    def __init__(self, session: AsyncSession, model_class: type):
        self.session = session
        self.model_class = model_class
    
    async def find_all(
        self, 
        filters: dict | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[T]:
        stmt = select(self.model_class).limit(limit).offset(offset)
        if filters:
            for key, value in filters.items():
                stmt = stmt.where(getattr(self.model_class, key) == value)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def find_by_id(self, id: str | int) -> T | None:
        stmt = select(self.model_class).where(self.model_class.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def create(self, data: dict) -> T:
        instance = self.model_class(**data)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance
    
    async def delete(self, id: str | int) -> None:
        instance = await self.find_by_id(id)
        if instance:
            await self.session.delete(instance)
            await self.session.commit()
```

### Service Layer Pattern

```python
class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    async def create_user(self, data: CreateUserInput) -> User:
        existing = await self.user_repo.find_by_email(data.email)
        if existing:
            raise ServiceError(
                message="Email already registered",
                status_code=status.HTTP_409_CONFLICT,
                code=AIMateErrorCode.CONFLICT,
            )
        
        hashed_password = hash_password(data.password)
        return await self.user_repo.create({
            **data.model_dump(exclude={"password"}),
            "password_hash": hashed_password
        })
    
    async def authenticate(self, email: str, password: str) -> User:
        user = await self.user_repo.find_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise ServiceError(
                message="Invalid credentials",
                status_code=status.HTTP_401_UNAUTHORIZED,
                code=AIMateErrorCode.UNAUTHORIZED,
            )
        return user
```

### Dependency Injection (FastAPI)

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session

async def get_user_repository(
    db: AsyncSession = Depends(get_db)
) -> UserRepository:
    return UserRepository(db, User)

async def get_user_service(
    repo: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(repo)
```

## Database Patterns

### Async SQLAlchemy Setup

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

def build_async_engine(database_url: str):
    return create_async_engine(
        database_url.replace("postgresql://", "postgresql+asyncpg://"),
        pool_size=20,
        max_overflow=30,
        pool_timeout=30,
        pool_recycle=3600,
        echo=False
    )

async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)
```

### Query Optimization

```python
from sqlalchemy import select
from sqlalchemy.orm import selectinload

# ✅ GOOD: Select only needed columns
stmt = (
    select(User.id, User.name, User.email)
    .where(User.status == "active")
    .order_by(User.created_at.desc())
    .limit(10)
)

# ✅ GOOD: Eager loading to prevent N+1
stmt = (
    select(User)
    .options(selectinload(User.orders))
    .where(User.id == user_id)
)

# ❌ BAD: Select everything
stmt = select(User)
```

### Transaction Pattern

```python
async def create_order_with_items(
    session: AsyncSession,
    order_data: dict,
    items_data: list[dict]
) -> Order:
    async with session.begin():
        order = Order(**order_data)
        session.add(order)
        await session.flush()  # Get order.id
        
        for item_data in items_data:
            item = OrderItem(order_id=order.id, **item_data)
            session.add(item)
        
        return order
```

## PydanticAI Patterns

### Agent Setup

```python
from pydantic_ai import Agent
from pydantic import BaseModel

class ConversationDeps(BaseModel):
    user_id: str
    session_id: str

agent = Agent(
    model="openai:gpt-4o",
    deps_type=ConversationDeps,
    output_type=str,
    instructions="You are a helpful assistant..."
)
```

### Tool Definition

```python
from pydantic_ai import RunContext

@agent.tool
async def search_database(
    ctx: RunContext[ConversationDeps],
    query: str
) -> str:
    """Search the database for relevant information."""
    results = await perform_search(ctx.deps.db_session, query)
    return format_results(results)
```

## Background Tasks

### APScheduler Integration

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

scheduler = AsyncIOScheduler()

async def sync_daily_reports():
    """Sync daily reports from external API."""
    async with async_session_maker() as session:
        await data_sync_service.sync_reports(session)

def setup_scheduler():
    scheduler.add_job(
        sync_daily_reports,
        CronTrigger(hour=2, minute=0),
        id="daily_reports_sync",
        replace_existing=True
    )
    scheduler.start()
```

## Logging

### Structured Logging

```python
import logging

logger = logging.getLogger(__name__)

# Usage
logger.info("User created", extra={"user_id": user.id, "email": user.email})
logger.error("Failed to sync", exc_info=True, extra={"service": "data_sync"})
logger.warning(f"Third-party API error: {e.message}")
```

**Remember**: Backend patterns enable scalable, maintainable server-side applications. Use ServiceError for all error handling. Choose patterns that fit your complexity level.
