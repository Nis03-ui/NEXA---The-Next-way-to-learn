from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.content import Content
from app.models.content_chunk import ContentChunk
from app.services.chunking import ChunkingService
from app.services.embedding import EmbeddingService


class ContentIndexingService:

    def __init__(
        self,
        chunking_service: ChunkingService | None = None,
        embedding_service: EmbeddingService | None = None,
    ):
        self.chunking_service = (
            chunking_service or ChunkingService()
        )

        self.embedding_service = (
            embedding_service or EmbeddingService()
        )

    async def index_content(
        self,
        content: Content,
        db: AsyncSession,
    ) -> list[ContentChunk]:

        # Remove previous chunks if this content is
        # being re-indexed after an update.
        await db.execute(
            delete(ContentChunk).where(
                ContentChunk.content_id == content.id
            )
        )

        chunks = self.chunking_service.chunk(
            content.body
        )

        if not chunks:
            return []

        embeddings = self.embedding_service.embed_many(
            chunks
        )

        content_chunks = []

        for index, (chunk_text, embedding) in enumerate(
            zip(chunks, embeddings)
        ):
            chunk = ContentChunk(
                content_id=content.id,
                chunk_index=index,
                text=chunk_text,
                embedding=embedding,
            )

            db.add(chunk)
            content_chunks.append(chunk)

        await db.flush()

        return content_chunks