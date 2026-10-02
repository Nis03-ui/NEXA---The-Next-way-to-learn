from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.content import Content
from app.models.content_chunk import ContentChunk
from app.services.embedding import EmbeddingService


@dataclass(frozen=True)
class VectorSearchResult:
    chunk: ContentChunk
    content: Content
    distance: float


class VectorSearchService:
    def __init__(
        self,
        embedding_service: EmbeddingService | None = None,
    ):
        self.embedding_service = embedding_service or EmbeddingService()

    async def search(
        self,
        query: str,
        db: AsyncSession,
        top_k: int = 5,
        max_distance: float = 0.65,
    ) -> list[VectorSearchResult]:

        query_embedding = self.embedding_service.embed(query)

        distance = ContentChunk.embedding.cosine_distance(
            query_embedding
        )

        result = await db.execute(
            select(
                ContentChunk,
                Content,
                distance.label("distance"),
            )
            .join(
                Content,
                Content.id == ContentChunk.content_id,
            )
            .where(
                Content.published.is_(True),
                ContentChunk.embedding.is_not(None),
                distance <= max_distance,
            )
            .order_by(distance)
            .limit(top_k)
        )

        rows = result.all()

        return [
            VectorSearchResult(
                chunk=chunk,
                content=content,
                distance=float(distance_value),
            )
            for chunk, content, distance_value in rows
        ]
