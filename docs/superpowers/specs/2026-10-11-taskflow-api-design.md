# TaskFlow API Design Document

**Date:** 2026-10-11  
**Author:** opencode  
**Status:** Approved

---

## Overview

TaskFlow API es una aplicación web asíncrona construida con FastAPI para gestionar tareas de usuarios. Permite registro, autenticación con tokens JWT (access + refresh), y CRUD completo de tareas con aislamiento por propietario, filtrado, paginación y ordenación.

## Architecture

**Pattern:** REST API con separación clara de responsabilidades.

**Capas:**
1. **Routes** - Endpoints HTTP, validación de parámetros de entrada
2. **Schemas** - Modelos Pydantic v2 para validación de requests/responses
3. **Models** - ORM SQLAlchemy 2.0 (async)
4. **Auth** - Lógica de autenticación (JWT, hashing)
5. **Database** - Conexión y gestión de sesiones

**Data Flow:**
```
Request → Routes → Schemas (validate) → Models (DB) → Response
              ↓
         Auth dependency (JWT verification)
```

## Components

### 1. Models (src/models/)

**User:**
```python
class User(Base):
    id: Mapped[int]
    email: Mapped[str] (unique, index)
    password_hash: Mapped[str]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
```

**Task:**
```python
class Task(Base):
    id: Mapped[int]
    title: Mapped[str] (1-200 chars)
    description: Mapped[str] (nullable, max 5000 chars)
    status: Mapped[str] (pending|in_progress|completed)
    priority: Mapped[str] (low|medium|high)
    owner_id: Mapped[int] (FK to User)
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    due_date: Mapped[datetime] (nullable)
```

### 2. Schemas (schemas/)

**User schemas:**
- `UserCreate` (email, password)
- `UserResponse` (id, email, created_at)
- `Token` (access_token, refresh_token, token_type)

**Task schemas:**
- `TaskCreate` (title, description, priority, status, due_date)
- `TaskUpdate` (partial fields)
- `TaskResponse` (full task + owner email)
- `TaskListParams` (limit, offset, status, priority, search, sort_by, sort_order)

**Validation rules:**
- Email: valid format, 1-255 chars, unique
- Password: min 8 chars
- Title: 1-200 chars
- Description: max 5000 chars
- Status: pending, in_progress, completed
- Priority: low, medium, high

### 3. Routes (routes/)

**Auth routes (routes/auth.py):**
- `POST /auth/register` - Create user, return tokens
- `POST /auth/login` - Validate credentials, return tokens
- `POST /auth/refresh` - Refresh access token using refresh token
- `GET /auth/me` - Get current user info

**Task routes (routes/tasks.py):**
- `POST /tasks` - Create task (owner_id from token)
- `GET /tasks` - List tasks with filters
- `GET /tasks/{task_id}` - Get single task
- `PATCH /tasks/{task_id}` - Update task
- `DELETE /tasks/{task_id}` - Delete task
- `GET /health` - Health check (public)

**Query parameters for GET /tasks:**
- `limit` (default: 20, max: 100)
- `offset` (default: 0)
- `status` (filter by status)
- `priority` (filter by priority)
- `search` (text search in title + description)
- `sort_by` (created_at, due_date, title; default: created_at)
- `sort_order` (asc, desc; default: desc)

### 4. Authentication (src/auth.py)

**JWT Configuration:**
- Algorithm: HS256
- Access token expiry: 15 minutes
- Refresh token expiry: 7 days
- Secret key from env var `JWT_SECRET_KEY`

**Password Hashing:**
- Library: `argon2-cffi`
- Parameters: time_cost=3, memory_cost=65536, parallelism=2

**Authentication Dependency:**
```python
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    # Validate JWT
    # Decode user_id
    # Fetch user from DB
    # Raise exception if invalid/expired
```

**Error Handling:**
- Invalid token: 401 Unauthorized
- Expired token: 401 Unauthorized  
- User not found: 404 Not Found
- Invalid credentials: 401 Unauthorized
- Non-existent resource: 404 Not Found

### 5. Database (src/database.py)

**Configuration:**
- Async engine with asyncio + aiosqlite
- SQLite file from env var `DATABASE_URL` (e.g., `sqlite+aiosqlite:///./taskflow.db`)
- Async session factory

**Session Management:**
- Context manager for automatic commit/rollback
- Dependency injection for FastAPI

### 6. Exceptions (src/exceptions.py)

**Custom Exceptions:**
- `InvalidCredentialsError` - Login failure
- `UserAlreadyExistsError` - Duplicate email
- `ResourceNotFoundError` - Task/user not found
- `PermissionDeniedError` - Unauthorized access to another user's resource

**Error Response Format:**
```json
{
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Invalid email or password",
    "details": {}
  }
}
```

## Security

**1. Authentication:**
- JWT tokens in Authorization header: `Bearer <token>`
- Access token short-lived (15 min)
- Refresh token long-lived (7 days)
- Token rotation on refresh

**2. Password Security:**
- Argon2 hashing (never plain text)
- Salt automatically generated

**3. Input Validation:**
- Pydantic v2 models for all endpoints
- Strict type checking
- Range validation (min/max chars, dates)

**4. Authorization:**
- Tasks isolated by `owner_id`
- Users can only modify their own tasks
- Cross-user access returns 404 (no info leakage)

**5. Error Handling:**
- Generic error messages
- No透露 sensitive info (user existence, field errors)

## Testing Strategy

**Test Structure:**
- `conftest.py` - Fixtures (test DB, test client, user factory)
- `test_auth.py` - Authentication tests
- `test_tasks.py` - Task CRUD + authorization tests

**Test Fixtures:**
- `test_db`: In-memory SQLite with teardown
- `client`: Async HTTPX test client
- `user_factory`: Create test users
- `auth_headers`: Pre-authenticated headers

**Test Coverage:**
1. Auth registration (success/failure cases)
2. Login (valid/invalid credentials)
3. Token refresh (valid/invalid refresh token)
4. Task CRUD (all operations)
5. Authorization (cross-user access attempts)
6. Filtering + pagination
7. Search + sorting
8. Validation errors (invalid input)
9. Health endpoint

## Dependencies

**Runtime:**
```toml
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
pydantic>=2.0.0
pydantic-settings>=2.1.0
sqlalchemy>=2.0.0
aiosqlite>=0.19.0
python-jose[cryptography]>=3.3.0
argon2-cffi>=23.1.0
python-multipart>=0.0.6
```

**Dev:**
```toml
pytest>=7.4.0
pytest-asyncio>=0.23.0
httpx>=0.26.0
ruff>=0.1.0
```

**requirements.txt:** Mirror of `pyproject.toml` dependencies

## Configuration

**Environment Variables:**
- `DATABASE_URL`: SQLite connection string
- `JWT_SECRET_KEY`: Random 32+ chars for JWT signing
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`: 15
- `JWT_REFRESH_TOKEN_EXPIRE_DAYS`: 7
- `APP_NAME`: TaskFlow API
- `APP_VERSION`: 1.0.0

**.env.example:** All variables with placeholder values

## API Documentation

**Generated by FastAPI:**
- `/docs` - Swagger UI (production: optional)
- `/redoc` - ReDoc (production: optional)
- `/openapi.json` - OpenAPI spec

## Acceptance Criteria

1. ✅ Application starts locally (`uvicorn src.main:app --reload`)
2. ✅ User registration and authentication works
3. ✅ Tasks created and managed with authentication
4. ✅ Users cannot access other users' tasks
5. ✅ Filters + pagination work together
6. ✅ All automated tests pass
7. ✅ Ruff finds no errors
8. ✅ Documentation matches implementation

---

**Design Approved.** Proceeding to implementation plan.
