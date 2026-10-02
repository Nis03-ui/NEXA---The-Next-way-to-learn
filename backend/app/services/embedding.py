from functools import lru_cache

from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    """
    Load the embedding model once and reuse it.

    Loading a transformer model for every request would be
    extremely expensive, so we cache the model instance.
    """
    return SentenceTransformer(MODEL_NAME)


class EmbeddingService:

    def __init__(self):
        self.model = get_embedding_model()

    def embed(self, text: str) -> list[float]:
        """
        Convert text into a 384-dimensional embedding vector.
        """
        vector = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return vector.tolist()

    def embed_many(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Convert multiple texts into embedding vectors.
        """
        vectors = self.model.encode(
            texts,
            normalize_embeddings=True,
        )

        return vectors.tolist()