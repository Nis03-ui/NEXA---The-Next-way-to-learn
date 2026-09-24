"""
Study Planner Agent — creates personalized structured study plans.
"""
from datetime import date
from typing import Optional

from pydantic import ValidationError

from app.ai.gemini_client import gemini_client
from app.ai.prompts.templates import (
    STUDY_PLANNER_SYSTEM_PROMPT,
    STUDY_PLANNER_USER_PROMPT_TEMPLATE,
)
from app.ai.schemas import AIStudyPlanOutput
from app.core.exceptions import AIServiceException
from app.core.logging import get_logger

logger = get_logger(__name__)


class StudyPlannerAgent:
    """
    Creates structured, week-by-week study plans tailored to student goals.
    """

    async def create_plan(
        self,
        goal: str,
        hours_per_week: int,
        start_date: date,
        end_date: date,
        subjects: Optional[list[str]] = None,
    ) -> AIStudyPlanOutput:
        """
        Generate a personalized study plan.

        Args:
            goal: The student's learning objective.
            hours_per_week: Available study time per week.
            start_date: When to start studying.
            end_date: Target completion date.
            subjects: Optional list of subjects to cover.

        Returns:
            Validated AIStudyPlanOutput with milestones and tasks.
        """
        subjects_block = ""
        if subjects:
            subjects_block = f"\nSubjects to cover: {', '.join(subjects)}"

        prompt = STUDY_PLANNER_USER_PROMPT_TEMPLATE.format(
            goal=goal,
            hours_per_week=hours_per_week,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            subjects_block=subjects_block,
        )

        logger.info(
            "StudyPlannerAgent generating plan",
            goal_length=len(goal),
            hours_per_week=hours_per_week,
        )

        raw = await gemini_client.generate_json(
            prompt=prompt,
            system_prompt=STUDY_PLANNER_SYSTEM_PROMPT,
            temperature=0.5,
        )

        try:
            return AIStudyPlanOutput.model_validate(raw)
        except ValidationError as e:
            logger.warning(
                "StudyPlannerAgent output validation failed",
                errors=e.errors(),
            )
            raise AIServiceException(
                "AI study plan generation failed validation. Please try again."
            )
