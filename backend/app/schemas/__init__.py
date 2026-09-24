"""
NEXA LMS Pydantic v2 schema package.

Centralised imports so route handlers and service modules can do::

    from app.schemas import UserResponse, CourseResponse, ...

rather than importing from individual sub-modules.
"""

from app.schemas.ai import (
    ChatRequest,
    ChatResponse,
    ConversationHistoryResponse,
    StudyPlanRequest,
    StudyPlanResponse,
    SummarizeRequest,
    SummarizeResponse,
)
from app.schemas.analytics import AdminAnalytics, StudentAnalytics, TeacherAnalytics
from app.schemas.assignment import (
    AssignmentCreate,
    AssignmentResponse,
    AssignmentUpdate,
    SubmissionCreate,
    SubmissionResponse,
    SubmissionUpdate,
)
from app.schemas.auth import (
    LoginRequest,
    PasswordChangeRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
)
from app.schemas.common import (
    ErrorDetail,
    ErrorResponse,
    PaginatedResponse,
    PaginationMeta,
    SuccessResponse,
)
from app.schemas.course import (
    ChapterCreate,
    ChapterDetailResponse,
    ChapterResponse,
    ChapterUpdate,
    CourseCreate,
    CourseDetailResponse,
    CourseResponse,
    CourseUpdate,
    NoteCreate,
    NoteResponse,
    NoteUpdate,
)
from app.schemas.enrollment import (
    EnrollmentDetailResponse,
    EnrollmentResponse,
    EnrollRequest,
)
from app.schemas.quiz import (
    AIQuizGenerateRequest,
    QuestionCreate,
    QuestionPublicResponse,
    QuestionResponse,
    QuizAttemptResponse,
    QuizAttemptSubmit,
    QuizCreate,
    QuizDetailResponse,
    QuizResponse,
    QuizUpdate,
)
from app.schemas.user import (
    UserBase,
    UserCreate,
    UserProfileResponse,
    UserResponse,
    UserUpdate,
)

__all__ = [
    # common
    "PaginationMeta",
    "SuccessResponse",
    "PaginatedResponse",
    "ErrorDetail",
    "ErrorResponse",
    # auth
    "LoginRequest",
    "RegisterRequest",
    "TokenResponse",
    "RefreshRequest",
    "PasswordChangeRequest",
    # user
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserProfileResponse",
    # course
    "CourseCreate",
    "CourseUpdate",
    "CourseResponse",
    "CourseDetailResponse",
    "ChapterCreate",
    "ChapterUpdate",
    "ChapterResponse",
    "ChapterDetailResponse",
    "NoteCreate",
    "NoteUpdate",
    "NoteResponse",
    # enrollment
    "EnrollRequest",
    "EnrollmentResponse",
    "EnrollmentDetailResponse",
    # assignment
    "AssignmentCreate",
    "AssignmentUpdate",
    "AssignmentResponse",
    "SubmissionCreate",
    "SubmissionUpdate",
    "SubmissionResponse",
    # quiz
    "QuestionCreate",
    "QuestionResponse",
    "QuestionPublicResponse",
    "QuizCreate",
    "QuizUpdate",
    "QuizResponse",
    "QuizDetailResponse",
    "QuizAttemptSubmit",
    "QuizAttemptResponse",
    "AIQuizGenerateRequest",
    # ai
    "ChatRequest",
    "ChatResponse",
    "SummarizeRequest",
    "SummarizeResponse",
    "StudyPlanRequest",
    "StudyPlanResponse",
    "ConversationHistoryResponse",
    # analytics
    "StudentAnalytics",
    "TeacherAnalytics",
    "AdminAnalytics",
]
