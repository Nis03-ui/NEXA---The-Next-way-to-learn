from fastapi import APIRouter

from app.api.v1.routes.auth import router as auth_router
from app.api.v1.routes.users import router as users_router
from app.api.v1.routes.courses import router as courses_router
from app.api.v1.routes.enrollments import router as enrollments_router
from app.api.v1.routes.ai import router as ai_router
from app.api.v1.routes.assignments import router as assignments_router
from app.api.v1.routes.quizzes import router as quizzes_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth")
api_router.include_router(users_router, prefix="/users")
api_router.include_router(courses_router, prefix="/courses")
api_router.include_router(enrollments_router, prefix="/enrollments")
api_router.include_router(assignments_router, prefix="/assignments")
api_router.include_router(quizzes_router, prefix="/quizzes")
api_router.include_router(ai_router, prefix="/ai")
