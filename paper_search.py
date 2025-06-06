import glob
import json
import os
from typing import List, Tuple

from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest

COLLECTION_NAME = "papers"
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIM = 1536


def _openai_client() -> OpenAI:
    with open("key.txt", "r", encoding="utf-8") as f:
        key = f.read().strip()
    return OpenAI(api_key=key)

def _qdrant_client() -> QdrantClient:
    return QdrantClient(host="localhost", port=6333)

def _build_text(data: dict) -> str:
    fields = [
        data.get("title"),
        data.get("abstract"),
        data.get("problem"),
        data.get("solution"),
        data.get("conclusion"),
    ]
    return "\n".join([f for f in fields if f])

def embed_papers(papers_dir: str = "papers") -> None:
    """Embed all JSON files from ``papers_dir`` into Qdrant."""
    client = _qdrant_client()
    oa = _openai_client()

    client.recreate_collection(
        COLLECTION_NAME,
        vectors_config=rest.VectorParams(size=EMBEDDING_DIM, distance=rest.Distance.COSINE),
    )

    points = []
    for idx, path in enumerate(sorted(glob.glob(os.path.join(papers_dir, "*.json")))):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        text = _build_text(data)
        response = oa.embeddings.create(input=text, model=EMBEDDING_MODEL)
        vector = response.data[0].embedding
        payload = data
        points.append(rest.PointStruct(id=idx, vector=vector, payload=payload))

    if points:
        client.upsert(COLLECTION_NAME, points)


def search_by_embedding(query: str, limit: int = 5) -> List[Tuple[float, dict]]:
    """Return papers most similar to the query."""
    client = _qdrant_client()
    oa = _openai_client()
    response = oa.embeddings.create(input=query, model=EMBEDDING_MODEL)
    vector = response.data[0].embedding
    results = client.search(COLLECTION_NAME, query_vector=vector, limit=limit)
    return [(r.score, r.payload) for r in results]

def search_by_keyword(keyword: str, limit: int = 10) -> List[dict]:
    """Return papers containing the given keyword."""
    client = _qdrant_client()
    filter_ = rest.Filter(
        must=[rest.FieldCondition(key="keywords", match=rest.MatchText(text=keyword))]
    )
    results = client.search(
        COLLECTION_NAME, query_vector=[0.0] * EMBEDDING_DIM, filter=filter_, limit=limit
    )
    return [r.payload for r in results]


def list_all_papers(batch_size: int = 100) -> List[dict]:
    """Return all papers stored in the collection."""
    client = _qdrant_client()
    offset = None
    papers = []
    while True:
        points, offset = client.scroll(
            COLLECTION_NAME,
            limit=batch_size,
            offset=offset,
            with_payload=True,
            with_vectors=False,
        )
        papers.extend([p.payload for p in points])
        if offset is None:
            break
    return papers

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Index and search papers")
    subparsers = parser.add_subparsers(dest="cmd")

    parser_index = subparsers.add_parser("index", help="Embed papers into Qdrant")
    parser_index.add_argument("--dir", default="papers", help="Directory with JSON files")

    parser_search = subparsers.add_parser("search", help="Semantic search")
    parser_search.add_argument("query", help="Query text")
    parser_search.add_argument("--limit", type=int, default=5)

    parser_kw = subparsers.add_parser("keyword", help="Search by keyword")
    parser_kw.add_argument("keyword", help="Keyword to match")
    parser_kw.add_argument("--limit", type=int, default=10)

    args = parser.parse_args()

    if args.cmd == "index":
        embed_papers(args.dir)
    elif args.cmd == "search":
        for score, payload in search_by_embedding(args.query, args.limit):
            print(f"{score:.3f} {payload.get('title')}")
    elif args.cmd == "keyword":
        for payload in search_by_keyword(args.keyword, args.limit):
            print(payload.get("title"))
    else:
        parser.print_help()
