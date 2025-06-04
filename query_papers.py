from paper_search import search_by_embedding, search_by_keyword
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python query_papers.py <query>")
        sys.exit(1)
    query = " ".join(sys.argv[1:])
    for score, payload in search_by_embedding(query):
        print(f"{score:.3f} {payload.get('title')}")
    print("\nKeyword results:")
    for payload in search_by_keyword(query):
        print(payload.get("title"))
