import re


class ChunkingService:
    """
    Splits educational content into smaller text chunks
    suitable for embedding and semantic retrieval.
    """

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
    ):
        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size"
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, text: str) -> list[str]:
        """
        Split text into overlapping word-based chunks.
        """

        text = self._clean_text(text)

        if not text:
            return []

        words = text.split()

        chunks = []

        start = 0

        while start < len(words):

            end = min(
                start + self.chunk_size,
                len(words),
            )

            chunk = " ".join(
                words[start:end]
            )

            chunks.append(chunk)

            if end >= len(words):
                break

            start = end - self.chunk_overlap

        return chunks

    @staticmethod
    def _clean_text(text: str) -> str:
        """
        Normalize unnecessary whitespace.
        """

        return re.sub(
            r"\s+",
            " ",
            text,
        ).strip()