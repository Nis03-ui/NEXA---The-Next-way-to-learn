"""
Tutor Agent — answers academic questions using Gemini.
"""
from typing import Optional

from app.ai.gemini_client import gemini_client
from app.ai.prompts.templates import (
    TUTOR_SYSTEM_PROMPT,
    TUTOR_USER_PROMPT_TEMPLATE,
)
from app.ai.safety import is_safe_input, sanitize_ai_response, truncate_context
from app.core.exceptions import AIServiceException, ValidationException
from app.core.logging import get_logger

logger = get_logger(__name__)


class TutorAgent:
    """
    Handles academic Q&A using the Gemini AI.
    Adapts explanations based on optional course context.
    """

    async def answer(
        self,
        question: str,
        context: Optional[str] = None,
    ) -> str:
        """
        Answer an academic question.

        Args:
            question: The student's question.
            context: Optional course/chapter content for grounding the answer.

        Returns:
            The AI-generated academic explanation.
        """
        if not is_safe_input(question):
            raise ValidationException("Your question contains content that cannot be processed")

        context_block = ""
        if context:
            truncated = truncate_context(context)
            context_block = f"\nCourse context provided:\n{truncated}\n"

        prompt = TUTOR_USER_PROMPT_TEMPLATE.format(
            question=question,
            context_block=context_block,
        )

        logger.info("TutorAgent generating response", question_length=len(question))

        response = await gemini_client.generate_text(
            prompt=prompt,
            system_prompt=TUTOR_SYSTEM_PROMPT,
            temperature=0.7,
        )

        return sanitize_ai_response(response)
