"""
Summarizer Agent — summarizes educational content and extracts key points.
"""
from typing import Optional

from pydantic import ValidationError

from app.ai.gemini_client import gemini_client
from app.ai.prompts.templates import (
    SUMMARIZER_SYSTEM_PROMPT,
    SUMMARIZER_USER_PROMPT_TEMPLATE,
)
from app.ai.safety import truncate_context
from app.ai.schemas import AISummaryOutput
from app.core.exceptions import AIServiceException
from app.core.logging import get_logger

logger = get_logger(__name__)


class SummarizerAgent:
    """
    Summarizes educational notes and extracts key revision points.
    """

    async def summarize(
        self,
        text: str,
        focus: Optional[str] = None,
    ) -> AISummaryOutput:
        """
        Summarize a piece of educational content.

        Args:
            text: The educational text to summarize.
            focus: Optional topic to emphasize in the summary.

        Returns:
            Validated AISummaryOutput with summary and key_points.
        """
        truncated_text = truncate_context(text, max_chars=40000)

        focus_block = ""
        if focus:
            focus_block = f"\nFocus especially on: {focus}"

        prompt = SUMMARIZER_USER_PROMPT_TEMPLATE.format(
            text=truncated_text,
            focus_block=focus_block,
        )

        logger.info("SummarizerAgent processing", text_length=len(text))

        raw = await gemini_client.generate_json(
            prompt=prompt,
            system_prompt=SUMMARIZER_SYSTEM_PROMPT,
            temperature=0.4,
        )

        try:
            return AISummaryOutput.model_validate(raw)
        except ValidationError as e:
            logger.warning(
                "SummarizerAgent output validation failed",
                errors=e.errors(),
            )
            raise AIServiceException(
                "AI summarization output failed validation. Please try again."
            )
