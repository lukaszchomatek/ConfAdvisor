import json
from typing import List, Tuple
from qdrant_client import QdrantClient
from sklearn.decomposition import PCA

COLLECTION_NAME = "papers"


def _qdrant_client() -> QdrantClient:
    return QdrantClient(host="localhost", port=6333)


def _fetch_vectors() -> Tuple[List[List[float]], List[dict]]:
    client = _qdrant_client()
    vectors: List[List[float]] = []
    payloads: List[dict] = []
    offset = None
    while True:
        points, offset = client.scroll(
            COLLECTION_NAME,
            limit=256,
            offset=offset,
            with_payload=True,
            with_vectors=True,
        )
        for p in points:
            if p.vector is not None:
                vectors.append(p.vector)
                payloads.append(p.payload)
        if offset is None:
            break
    return vectors, payloads


def prepare_visualization(output_file: str = "viz_data.json") -> str:
    vectors, payloads = _fetch_vectors()
    if not vectors:
        raise ValueError("No vectors found in Qdrant")

    pca = PCA(n_components=2)
    coords = pca.fit_transform(vectors)

    data = []
    for (x, y), payload in zip(coords.tolist(), payloads):
        data.append({
            "x": x,
            "y": y,
            "title": payload.get("title"),
            "url": payload.get("url"),
        })

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return output_file


if __name__ == "__main__":
    path = prepare_visualization()
    print(f"Visualization data saved to: {path}")
