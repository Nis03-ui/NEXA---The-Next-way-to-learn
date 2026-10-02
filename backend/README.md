# NEXA FastAPI backend

This backend implements the frontend contract used by the NEXA Next.js app:

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/users/me`
- `POST /api/v1/ai/chat`
- `GET /api/v1/admin/stats`
- `GET /health`

It uses FastAPI + SQLAlchemy async + JWT + Argon2. Set `DATABASE_URL` to your existing PostgreSQL database for the production NEXA stack. Set `GEMINI_API_KEY` for real Gemini 2.5 Flash responses.

## Run

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```
