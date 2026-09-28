# NEXA Project Status

## Current milestone: Backend + AI foundation

The original Antigravity implementation has been retained and extended instead of being rewritten.

### Completed in this pass

- Added FastAPI v1 router and route modules.
- Added authentication endpoints: register, login, refresh, current user, password change.
- Added admin user management endpoints.
- Added course catalog, teacher course management, publishing, chapters, and notes.
- Added student enrollment endpoints.
- Added assignment and submission endpoints.
- Added quiz creation, safe student quiz retrieval, and automatic attempt grading.
- Added AI tutor chat with persisted conversation history.
- Added AI summarization.
- Added AI study-plan generation and persistence.
- Added AI quiz generation and persistence.
- Fixed repository `create`/`update` contracts used by existing services.
- Fixed JWT helper parameter mismatch.
- Fixed the user password-hash field mismatch.
- Fixed SQLAlchemy's reserved `metadata` attribute on `ActivityLog`.
- Added local database bootstrap script.
- Added Alembic environment for the migration workflow.
- Removed the unfinished Celery worker from Docker Compose.
- Added API and AI endpoint documentation.
- Added a root project README and gitignore.

### Verification

- Python `compileall` passes for the backend.
- Static route count: 48.
- Live dependency/database/API execution was not performed in this environment because external package installation is unavailable.

### Next milestone

1. Install dependencies locally.
2. Start PostgreSQL/Redis.
3. Run `python scripts/init_db.py`.
4. Start FastAPI.
5. Execute endpoint smoke tests.
6. Fix runtime issues discovered by real DB/API execution.
7. Add frontend integration contracts and automated API tests.
