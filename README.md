# NEXA — The Next Way to Learn

NEXA is an AI-powered learning platform built for the college project.

## Backend

- FastAPI + Python 3.11
- PostgreSQL + async SQLAlchemy
- JWT authentication + RBAC
- Gemini AI via HTTPX
- Docker Compose for PostgreSQL, Redis, and API

## Roles

- `STUDENT` — learning, enrollment, assignments, quizzes, AI tools
- `TEACHER` — course/content/assessment management
- `ADMIN` — platform/user management

## Run locally

```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# edit .env with JWT_SECRET_KEY and GEMINI_API_KEY
python scripts/init_db.py
uvicorn app.main:app --reload
```

API docs: `http://localhost:8000/docs`

## Docker

```powershell
cd backend
docker compose up --build
```

The development container initializes the PostgreSQL schema automatically. Alembic configuration is included for the next migration pass.

## Documentation

- `backend/docs/API.md`
- `backend/docs/AI_API.md`
