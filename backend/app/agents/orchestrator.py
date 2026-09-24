"""
Agent Orchestrator — routes incoming AI requests to the appropriate specialized agent.
"""
from enum import Enum
from typing import Optional

from app.agents.quiz_agent import QuizAgent
from app.agents.summarizer_agent import SummarizerAgent
from app.agents.study_planner_agent import StudyPlannerAgent
from app.agents.tutor_agent import TutorAgent
from app.core.logging import get_logger

logger = get_logger(__name__)


class AgentType(str, Enum):
    TUTOR = "tutor"
    QUIZ = "quiz"
    SUMMARIZER = "summarizer"
    STUDY_PLANNER = "study_planner"


class AgentOrchestrator:
    """
    Central router that holds singleton agent instances and dispatches requests.

    This keeps the agent layer decoupled from the service layer.
    Services interact only with the orchestrator, not individual agents.
    """

    def __init__(self) -> None:
        self._tutor = TutorAgent()
        self._quiz = QuizAgent()
        self._summarizer = SummarizerAgent()
        self._study_planner = StudyPlannerAgent()

    @property
    def tutor(self) -> TutorAgent:
        return self._tutor

    @property
    def quiz(self) -> QuizAgent:
        return self._quiz

    @property
    def summarizer(self) -> SummarizerAgent:
        return self._summarizer

    @property
    def study_planner(self) -> StudyPlannerAgent:
        return self._study_planner


# Application-level singleton orchestrator
orchestrator = AgentOrchestrator()
