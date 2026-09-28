# NEXA API Contract

Base URL: `/api/v1`

Authentication uses `Authorization: Bearer <access_token>`. All successful responses use `{ success, data, message }`; paginated responses additionally include `pagination`. Errors use the standard `{ success: false, error, request_id }` envelope.

## Authentication

- `POST /auth/register` — public student registration
- `POST /auth/login` — public login
- `POST /auth/refresh` — refresh access token
- `GET /auth/me` — current user
- `POST /auth/change-password` — authenticated user

## Users

- `GET /users/me` — current profile
- `POST /users` — admin creates a user/teacher
- `GET /users` — admin user list
- `GET /users/{user_id}` — admin user detail
- `PATCH /users/{user_id}` — admin update
- `DELETE /users/{user_id}` — admin delete

## Courses

- `GET /courses` — published course catalog
- `GET /courses/mine` — teacher/admin courses
- `POST /courses` — teacher/admin create
- `GET /courses/{course_id}` — course detail
- `PATCH /courses/{course_id}` — owner/admin update
- `DELETE /courses/{course_id}` — owner/admin delete
- `POST /courses/{course_id}/publish` — owner/admin publish
- `POST /courses/{course_id}/unpublish` — owner/admin unpublish
- `GET /courses/{course_id}/chapters` — chapter list
- `POST /courses/{course_id}/chapters` — teacher/admin create chapter
- `GET /courses/chapters/{chapter_id}/notes` — chapter notes
- `POST /courses/chapters/{chapter_id}/notes` — teacher/admin create note

## Enrollments

- `POST /enrollments` — student enrollment
- `GET /enrollments/me` — student's enrollments
- `GET /enrollments/courses/{course_id}` — teacher/admin enrollment list

## Assignments

- `GET /assignments/course/{course_id}`
- `POST /assignments`
- `GET /assignments/{assignment_id}`
- `PATCH /assignments/{assignment_id}`
- `DELETE /assignments/{assignment_id}`
- `POST /assignments/{assignment_id}/submissions`
- `GET /assignments/{assignment_id}/submissions`
- `PATCH /assignments/submissions/{submission_id}`

## Quizzes

- `POST /quizzes` — teacher/admin manual quiz
- `GET /quizzes/{quiz_id}` — student-safe or teacher/admin detail
- `PATCH /quizzes/{quiz_id}` — teacher/admin update
- `POST /quizzes/{quiz_id}/attempts` — student submission/grading

## Health

- `GET /health`
- `GET /health/ready`
