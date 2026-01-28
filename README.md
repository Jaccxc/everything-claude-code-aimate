# Everything Claude Code - AIMate Edition

![Python](https://img.shields.io/badge/-Python%203.11-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/-FastAPI-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Markdown](https://img.shields.io/badge/-Markdown-000000?logo=markdown&logoColor=white)

**Claude Code 完整配置集，專為 AIMate 團隊的 Python/FastAPI 技術棧優化。**

Production-ready agents, skills, hooks, commands, rules，適用於 Python 3.11、FastAPI、Pydantic、SQLAlchemy、PostgreSQL 開發環境。

## 安裝指南

1. 複製此儲存庫
2. 進入此儲存庫目錄
3. 在同一個終端機中，開啟 claude code
4. 使用 `/plugin` 開啟外掛程式設定
5. 按右方向鍵 2 次移動到 "Marketplaces" 標籤
6. 選擇 "+ Add Marketplace"
7. 輸入 "./"
8. 選擇 "everything-claude-code-aimate" 即可安裝
9. 退出 claude code
10. 再次進入 claude code，如果看到 "SessionStart:startup hook succeeded" 表示安裝成功

對於 MacOS 或 Linux 使用者：
mgrep 是 ripgrep/grep 的重大改進。透過外掛程式市集安裝後，即可支援本地搜尋和網頁搜尋。

11. 再次新增 Marketplace，這次新增 "https://github.com/mixedbread-ai/mgrep "
12. 選擇 "Mixedbred-Grep"

直接使用範例：
```bash
mgrep "function handleSubmit"  # 本地搜尋
mgrep --web "Next.js 15 app router changes"  # 網頁搜尋
```

---


## 技術棧

- **語言**: Python 3.11+
- **Web 框架**: FastAPI
- **資料驗證**: Pydantic, pydantic-ai
- **資料庫**: PostgreSQL + SQLAlchemy (async) + Alembic
- **程式碼品質**: Ruff + Black (透過 poetry run)
- **測試**: pytest, pytest-asyncio
- **依賴管理**: Poetry
- **CI/CD**: GitLab

---

## 跨平台支援

完整支援 **Windows、macOS 和 Linux**。所有 hooks 和 scripts 都使用 Python 撰寫，確保跨平台相容性。

---

## 目錄結構

```
everything-claude-code-aimate/
├── agents/           # 專業化子代理
│   ├── planner.md           # 功能實作規劃
│   ├── architect.md         # 系統設計決策
│   ├── tdd-guide.md         # pytest TDD 開發
│   ├── code-reviewer.md     # Python/FastAPI 程式碼審查
│   ├── security-reviewer.md # 安全漏洞分析
│   ├── build-error-resolver.md  # Python 建置錯誤修復
│   ├── e2e-runner.md        # Playwright E2E 測試
│   ├── refactor-cleaner.md  # 死碼清理
│   ├── doc-updater.md       # 文件同步
│   └── database-reviewer.md # PostgreSQL 資料庫審查
│
├── skills/           # 工作流程定義
│   ├── coding-standards/    # Python 最佳實踐
│   ├── backend-patterns/    # FastAPI/Pydantic 模式
│   ├── frontend-patterns/   # React 前端模式
│   ├── postgres-patterns/   # PostgreSQL/SQLAlchemy 模式
│   ├── continuous-learning/ # 自動從 session 學習
│   ├── continuous-learning-v2/  # 進階 instinct 學習
│   ├── tdd-workflow/        # pytest TDD 方法論
│   ├── security-review/     # 安全檢查清單
│   └── verification-loop/   # 驗證迴圈
│
├── commands/         # 斜線指令
│   ├── tdd.md              # /tdd - pytest TDD 開發
│   ├── plan.md             # /plan - 實作規劃
│   ├── e2e.md              # /e2e - E2E 測試生成
│   ├── code-review.md      # /code-review - 品質審查
│   ├── build-fix.md        # /build-fix - 修復 lint/type 錯誤
│   ├── refactor-clean.md   # /refactor-clean - 死碼移除
│   ├── test-coverage.md    # /test-coverage - 覆蓋率分析
│   └── learn.md            # /learn - 提取模式
│
├── rules/            # 永遠遵循的準則
│   ├── security.md         # 強制安全檢查
│   ├── coding-style.md     # Python/Pydantic 風格
│   ├── testing.md          # pytest TDD, 80% 覆蓋率
│   ├── patterns.md         # AIMateAPIResponse 模式
│   ├── git-workflow.md     # Commit 格式, PR 流程
│   ├── agents.md           # 何時委派給子代理
│   └── performance.md      # 模型選擇, context 管理
│
├── hooks/            # 觸發式自動化
│   └── hooks.json          # 所有 hooks 設定
│
├── scripts/          # 跨平台 Python scripts
│   ├── lib/
│   │   └── utils.py        # 跨平台工具函式
│   └── hooks/              # Hook 實作
│       ├── check_print.py
│       ├── suggest_compact.py
│       ├── session_start.py
│       └── session_end.py
│
├── example-ai-mate-contracts/     # API 回應契約範例
│   └── aimate/contracts/
│       ├── responses.py    # AIMateAPIResponse
│       └── vben.py         # VbenResponse (前端用)
│
└── example-project-operator-intelligence/  # 範例專案參考
```

---

## API 回應格式

### AIMateAPIResponse (預設)

所有 API endpoint 都應使用 `AIMateAPIResponse`：

```python
from aimate.contracts import AIMateAPIResponse, AIMateErrorResponse

@router.get("/users/{user_id}")
async def get_user(user_id: str) -> AIMateAPIResponse[User]:
    user = await user_service.get_by_id(user_id)
    if not user:
        return AIMateAPIResponse(
            error=AIMateErrorResponse(
                code="USER_NOT_FOUND",
                message=f"User {user_id} not found"
            )
        )
    return AIMateAPIResponse(data=user)
```

### VbenResponse (僅前端 endpoint)

只有前端專用的 endpoint 才使用 `VbenResponse`：

```python
@router.get("/web/dashboard")
async def get_dashboard() -> VbenResponse[DashboardData]:
    return VbenResponse(code=0, message="ok", data=data)
```

---

## 核心概念

### Agents (子代理)

子代理處理特定範圍的委派任務：

```markdown
---
name: code-reviewer
description: Python/FastAPI 程式碼審查專家
tools: ["Read", "Grep", "Glob", "Bash"]
model: opus
---

You are a senior code reviewer for Python/FastAPI projects...
```

### Skills (技能)

技能是被指令或代理調用的工作流程定義：

```markdown
# TDD Workflow

1. 定義 Pydantic 模型
2. 寫失敗的測試 (RED)
3. 實作最小程式碼 (GREEN)
4. 重構 (IMPROVE)
5. 驗證 80%+ 覆蓋率
```

### Hooks (鉤子)

Hooks 在工具事件時觸發。例如 - 警告 print() 語句：

```json
{
  "matcher": "tool == \"Edit\" && tool_input.file_path matches \"\\\\.py$\"",
  "hooks": [{
    "type": "command",
    "command": "python check_print.py"
  }]
}
```

### Rules (規則)

規則是永遠遵循的準則：

```
~/.claude/rules/
  security.md      # 不可硬編碼密鑰
  coding-style.md  # Pydantic, type hints
  testing.md       # pytest TDD, 覆蓋率要求
  patterns.md      # AIMateAPIResponse 模式
```

---

## 常用指令

```bash
# 執行測試
poetry run pytest

# 帶覆蓋率測試
poetry run pytest --cov=app --cov-report=html

# Lint 檢查
poetry run ruff check .

# 格式化程式碼
poetry run ruff format .

# 執行開發伺服器
poetry run uvicorn app.main:app --reload

# 執行資料庫遷移
poetry run alembic upgrade head
```

---

## 重要注意事項

### Context Window 管理

**重要:** 不要同時啟用所有 MCPs。你的 200k context window 在啟用太多工具時可能縮減到 70k。

經驗法則：
- 設定 20-30 個 MCPs
- 每個專案啟用少於 10 個
- 活躍工具少於 80 個

### 客製化

這些設定適用於 AIMate 團隊的工作流程。你應該：
1. 從有用的部分開始
2. 根據你的需求修改
3. 移除不使用的部分
4. 加入你自己的模式

---

## License

MIT - 自由使用，按需修改。
