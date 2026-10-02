from sqlalchemy.ext.asyncio import AsyncSession

from app.services.orchestrator import AIOrchestrator


orchestrator = AIOrchestrator()


async def answer(
    message: str,
    conversation: str = "",
    db: AsyncSession | None = None,
    mode: str = "normal",
):
    return await orchestrator.run(
        message=message,
        conversation=conversation,
        db=db,
        mode=mode,
    )