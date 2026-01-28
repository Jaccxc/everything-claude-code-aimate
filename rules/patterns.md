# Common Patterns

## API Response Format

### AIMateAPIResponse (預設 API 格式)

```python
from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")

class AIMateErrorResponse(BaseModel):
    code: str | int
    message: str
    details: dict | None = None

class AIMateAPIResponse(BaseModel, Generic[T]):
    data: T | None = None
    error: AIMateErrorResponse | None = None
```

### VbenResponse (僅前端 endpoint)

只有前端專用的 endpoint 才使用：

```python
class VbenResponse(BaseModel, Generic[T]):
    code: int  # 0 = success, others = fail
    message: str
    data: T | None = None
```

## ServiceError Pattern (標準錯誤處理)

在 endpoint 中使用 `raise ServiceError()` 而非直接返回錯誤：

```python
from fastapi import APIRouter, status
from app.exceptions import ServiceError
from app.contracts import AIMateErrorCode, VbenResponse

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
                "local": {...},
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

## Repository Pattern

```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_all(self, filters: dict | None = None) -> list[User]:
        stmt = select(User)
        if filters:
            for key, value in filters.items():
                stmt = stmt.where(getattr(User, key) == value)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def find_by_id(self, id: str | int) -> User | None:
        stmt = select(User).where(User.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, data: dict) -> User:
        instance = User(**data)
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

## Service Layer Pattern

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
        return await self.user_repo.create(data.model_dump())
```

## Dependency Injection (FastAPI)

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

## PydanticAI Agent Pattern

```python
from pydantic_ai import Agent, RunContext
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

@agent.tool
async def search_database(
    ctx: RunContext[ConversationDeps],
    query: str
) -> str:
    """Search the database for relevant information."""
    results = await perform_search(ctx.deps.db_session, query)
    return format_results(results)
```
