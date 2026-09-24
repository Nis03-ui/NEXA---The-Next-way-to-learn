"""
Quiz Agent — generates MCQ quizzes using Gemini with structured output validation.
"""
from typing import Optional

from pydantic import ValidationError

from app.ai.gemini_client import gemini_client
from app.ai.prompts.templates import (
    QUIZ_GENERATION_SYSTEM_PROMPT,
    QUIZ_GENERATION_USER_PROMPT_TEMPLATE,
)
from app.ai.safety import truncate_context
from app.ai.schemas import AIQuizOutput, GeneratedQuestion
from app.core.exceptions import AIServiceException
from app.core.logging import get_logger

logger = get_logger(__name__)


class QuizAgent:
    """
    Generates multiple-choice quiz questions using the Gemini AI.
    All output is validated against strict Pydantic schemas.
    """

    async def generate_questions(
        self,
        topic: str,
        num_questions: int = 5,
        difficulty: str = "medium",
        context: Optional[str] = None,
    ) -> list[GeneratedQuestion]:
        """
        Generate MCQ questions for a given topic.

        Args:
            topic: The subject/topic to generate questions about.
            num_questions: How many questions to generate (1-20).
            difficulty: 'easy', 'medium', or 'hard'.
            context: Optional course notes for grounding questions.

        Returns:
            A validated list of GeneratedQuestion objects.
        """
        context_block = ""
        if context:
            truncated = truncate_context(context, max_chars=3000)
            context_block = f"\nBase questions on this course content:\n{truncated}"

        prompt = QUIZ_GENERATION_USER_PROMPT_TEMPLATE.format(
            num_questions=num_questions,
            topic=topic,
            difficulty=difficulty,
            context_block=context_block,
        )

        logger.info(
            "QuizAgent generating questions",
            topic=topic,
            num_questions=num_questions,
            difficulty=difficulty,
        )

        raw = await gemini_client.generate_json(
            prompt=prompt,
            system_prompt=QUIZ_GENERATION_SYSTEM_PROMPT,
            temperature=0.6,
        )

        try:
            validated = AIQuizOutput.model_validate(raw)
        except ValidationError as e:
            logger.warning(
                "QuizAgent output validation failed",
                errors=e.errors(),
                raw_keys=list(raw.keys()),
            )
            raise AIServiceException(
                "AI generated quiz questions failed validation. Please try again."
            )

        if len(validated.questions) != num_questions:
            logger.warning(
                "QuizAgent returned wrong number of questions",
                expected=num_questions,
                actual=len(validated.questions),
            )

        return validated.questions
