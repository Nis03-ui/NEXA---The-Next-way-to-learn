# NEXA AI API

AI endpoints are authenticated and route through the orchestrator. Gemini is never called directly from route handlers.

## Tutor
`POST /api/v1/ai/chat`

```json
{
  "question": "Explain binary search simply",
  "session_id": "optional-session-id",
  "context": "optional course or lesson text"
}
```

Returns the answer plus `session_id`, `agent_type`, and persisted conversation ID.

## Summarizer
`POST /api/v1/ai/summarize`

Accepts educational text and an optional focus.

## Study Planner
`POST /api/v1/ai/study-plan`

Accepts goal, weekly hours, date range, and optional subjects. The validated structured plan is persisted for the authenticated student.

## AI Quiz Generator
`POST /api/v1/ai/quiz-generate`

Teacher/admin only. Generates validated MCQs and persists them as an AI-generated quiz.
