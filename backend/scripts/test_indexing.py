import asyncio

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.content import Content
from app.models.content_chunk import ContentChunk
from app.services.indexing import ContentIndexingService


async def main():

    async with SessionLocal() as db:

        result = await db.execute(
            select(Content)
            .where(Content.id == 1)
        )

        content = result.scalar_one_or_none()

        if content is None:
            print("Content #1 not found.")
            return

        service = ContentIndexingService()

        chunks = await service.index_content(
            content=content,
            db=db,
        )

        await db.commit()

        print(f"Indexed content: {content.title}")
        print(f"Chunks created: {len(chunks)}")

        result = await db.execute(
            select(ContentChunk)
            .where(
                ContentChunk.content_id == content.id
            )
            .order_by(
                ContentChunk.chunk_index.asc()
            )
        )

        stored_chunks = result.scalars().all()

        for chunk in stored_chunks:
            print(
                f"\nChunk {chunk.chunk_index}"
            )
            print(
                f"Text: {chunk.text}"
            )
            print(
                f"Embedding dimensions: "
                f"{len(chunk.embedding)}"
            )


if __name__ == "__main__":
    asyncio.run(main())