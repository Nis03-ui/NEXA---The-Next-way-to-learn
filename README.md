# NEXA — Full Stack Implementation

A working Next.js + FastAPI implementation based on the supplied NEXA UI/UX references.

## Architecture

Browser → Next.js 16 → FastAPI `/api/v1` → PostgreSQL/SQLite → Gemini 2.5 Flash

The NEXA 3D avatar is implemented with React Three Fiber/Drei and has application-controlled states: `idle`, `thinking`, `explaining`, `happy`, `curious`, `celebrating`, `loading`, and `error`.

## 1. Backend

```bash
cd backend
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## 2. Frontend

```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

Frontend: http://localhost:3000
Backend docs: http://localhost:8000/docs

## Existing NEXA backend integration

The frontend uses the same FastAPI-first architecture and endpoint contract. If you already have the larger NEXA backend (courses, enrollments, assignments, quizzes, repositories/services, Redis, Alembic, etc.), keep that backend and point `NEXT_PUBLIC_API_URL` at it. The UI components are separated so the real endpoints can replace demo dashboard/material data without rewriting the visual system.
