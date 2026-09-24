"""
Centralized model registry — import all models here so Alembic can discover them.
"""
from app.db.base import Base  # noqa: F401
from app.models.user import User, Role  # noqa: F401
from app.models.course import Course, Chapter, Note, CourseStatus  # noqa: F401
from app.models.enrollment import Enrollment, EnrollmentStatus  # noqa: F401
from app.models.assignment import Assignment, Submission  # noqa: F401
from app.models.quiz import Quiz, Question, QuizAttempt, QuizSource  # noqa: F401
from app.models.ai_chat import AIConversation, StudyPlan, ActivityLog  # noqa: F401
