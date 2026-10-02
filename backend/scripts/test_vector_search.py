import asyncio

from app.db.session import SessionLocal
from app.services.vector_search import VectorSearchService


async def main():
    queries = [
        "What is polymorphism?",
        "How does method overriding work?",
        "What are the different types of polymorphism?",
        "What is TCP and UDP?",
    ]

    service = VectorSearchService()

    async with SessionLocal() as db:
        for query in queries:
            print("\n" + "=" * 70)
            print(f"QUERY: {query}")
            print("=" * 70)

            results = await service.search(
                query=query,
                db=db,
                top_k=3,
            )

            if not results:
                print("No results found.")
                continue

            for index, (chunk, distance) in enumerate(results, start=1):
                print(f"\nResult {index}")
                print(f"Content ID: {chunk.content_id}")
                print(f"Distance: {distance:.4f}")
                print(f"Text: {chunk.text}")


if __name__ == "__main__":
    asyncio.run(main())