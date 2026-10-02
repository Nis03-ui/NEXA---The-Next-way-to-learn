from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from sqlalchemy.ext.asyncio import AsyncSession


@dataclass(frozen=True)
class AgentSource:
    content_id: int
    title: str
    subject: str
    chunk_index: int
    distance: float


@dataclass
class AgentResult:
    answer: str
    agent: str
    sources: list[AgentSource] = field(
        default_factory=list
    )


class BaseAgent(ABC):
    """
    Common contract for all NEXA AI agents.
    """

    name: str

    def __init__(self, gemini):
        self.gemini = gemini

    @abstractmethod
    async def run(
        self,
        message: str,
        conversation: str = "",
        db: AsyncSession | None = None,
        mode: str = "normal",
    ) -> AgentResult:
        """
        Execute the agent and return a structured result.
        """
        raise NotImplementedError