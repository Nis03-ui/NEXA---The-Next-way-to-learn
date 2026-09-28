"""Create NEXA tables for local development.

Production deployments should use Alembic migrations.
"""
import asyncio

from app.db.base import Base
from app.db.session import engine
from app import models  # noqa: F401 - register every ORM model


async def main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    print("NEXA database tables are ready.")


if __name__ == "__main__":
    asyncio.run(main())
