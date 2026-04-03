import os
import hashlib
import argparse
from datetime import datetime
from typing import Optional
from xml.etree import ElementTree as ET

import requests

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from qdrant_client.http.exceptions import ResponseHandlingException


def get_env(key: str, default: str = "") -> str:
    return os.environ.get(key, default)


def get_env_int(key: str, default: int = 0) -> int:
    val = os.environ.get(key)
    return int(val) if val else default


class PinIndexer:
    def __init__(
        self,
        qdrant_url: str = None,
        collection_name: str = None,
        vector_size: int = None,
    ):
        qdrant_url = qdrant_url or get_env("QDRANT_URL", "localhost:6333")
        collection_name = collection_name or get_env("QDRANT_COLLECTION", "blog_posts")
        vector_size = vector_size or get_env_int("QDRANT_VECTOR_SIZE", 1536)
        vector_name = get_env("QDRANT_VECTOR_NAME", None)
        print(f"QDRANT_URL: {qdrant_url}")
        print(f"QDRANT_VECTOR_NAME: {vector_name}")
        self.qdrant_client = QdrantClient(
            url=qdrant_url,
            api_key=get_env("QDRANT_API_KEY"),
        )
        self.collection_name = collection_name
        self.vector_size = vector_size
        self.vector_name = vector_name

    def create_collection(self, force: bool = False):
        try:
            self.qdrant_client.get_collection(self.collection_name)
            if force:
                self.qdrant_client.delete_collection(self.collection_name)
                self._create_collection()
                print(f"Collection '{self.collection_name}' recreated.")
            else:
                print(f"Collection '{self.collection_name}' already exists.")
        except (ResponseHandlingException, Exception):
            self._create_collection()
            print(f"Collection '{self.collection_name}' created.")

    def _create_collection(self):
        self.qdrant_client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.vector_size,
                distance=Distance.COSINE,
            ),
        )

    def parse_atom(self, feed_url: str) -> list[dict]:
        response = requests.get(feed_url, timeout=30)
        response.raise_for_status()

        root = ET.fromstring(response.content)

        ns = {"atom": "http://www.w3.org/2005/Atom"}

        entries = []
        for entry in root.findall("atom:entry", ns):
            entry_id = entry.find("atom:id", ns)
            title = entry.find("atom:title", ns)
            content = entry.find("atom:content", ns)
            published = entry.find("atom:published", ns)
            updated = entry.find("atom:updated", ns)

            raw_id = entry_id.text if entry_id is not None else ""
            entry_data = {
                "title": title.text if title is not None else "",
                "content": content.text if content is not None else "",
                "published": published.text if published is not None else "",
                "updated": updated.text if updated is not None else "",
            }

            entry_data["id"] = hashlib.sha256(
                (raw_id + entry_data["title"] + entry_data["published"]).encode()
            ).hexdigest()[:32]

            entries.append(entry_data)

        return entries

    def embed_text(self, text: str, embedder) -> list[float]:
        return embedder.embed([text])[0]

    def index_entries(self, feed_url: str, embedder, limit: int = 0):
        entries = self.parse_atom(feed_url)
        print(f"Found {len(entries)} entries from feed.")

        if limit > 0:
            entries = entries[:limit]
            print(f"Limited to {len(entries)} entries.")

        points = []
        for entry in entries:
            try:
                text_to_embed = f"{entry['title']} {entry['content'][:1000]}"
                vector = self.embed_text(text_to_embed, embedder)

                if self.vector_size and len(vector) < self.vector_size:
                    vector = vector + [0.0] * (self.vector_size - len(vector))

                payload = {
                    "title": entry["title"],
                    "content": entry["content"],
                    "published": entry["published"],
                    "updated": entry["updated"],
                    "source": "pin",
                }

                if self.vector_name:
                    vector_to_use = {self.vector_name: vector}
                else:
                    vector_to_use = vector

                point = PointStruct(
                    id=entry["id"],
                    vector=vector_to_use,
                    payload=payload,
                )
                points.append(point)
                print(f"Prepared: {entry['title'][:50]}...")

            except Exception as e:
                print(f"Error processing entry: {e}")
                continue

        if points:
            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=points,
            )
            print(f"Successfully indexed {len(points)} entries.")


class OpenAIEmbedder:
    def __init__(
        self,
        base_url: str = None,
        token: str = None,
        model: str = None,
        dimension: int = None,
    ):
        from openai import OpenAI

        base_url = base_url or get_env("LLM_BASE_URL", "https://api.openai.com/v1")
        token = token or get_env("LLM_TOKEN")
        if not token:
            raise ValueError("LLM_TOKEN is required. Set LLM_TOKEN env or pass --token")
        model = model or get_env("LLM_EMBEDDING_MODEL", "text-embedding-3-small")
        dimension = dimension or get_env_int("LLM_EMBEDDING_DIMENSION", 1536)

        self.client = OpenAI(base_url=base_url, api_key=token)
        self.model = model
        self.dimension = dimension

    def embed(self, texts: list[str]) -> list[list[float]]:
        response = self.client.embeddings.create(
            model=self.model,
            input=texts,
        )
        return [item.embedding for item in response.data]


class LocalEmbedder:
    def __init__(
        self,
        model_name: str = None,
        dimension: int = None,
    ):
        from sentence_transformers import SentenceTransformer

        model_name = model_name or get_env("LOCAL_EMBEDDING_MODEL", "BAAI/bge-small-zh")
        dimension = dimension or get_env_int("LOCAL_EMBEDDING_DIMENSION", 512)

        self.model = SentenceTransformer(model_name)
        self.dimension = dimension

    def embed(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts, normalize_embeddings=True).tolist()


def main():
    parser = argparse.ArgumentParser(description="Index pin entries to Qdrant")
    parser.add_argument(
        "--feed-url",
        default="https://www.cyeam.com/pin/atom.xml",
        help="Atom feed URL",
    )
    parser.add_argument(
        "--recreate", action="store_true", help="Recreate collection if exists"
    )
    parser.add_argument(
        "--embedder",
        choices=["openai", "local"],
        default="openai",
        help="Embedder type",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Limit number of entries to index (0 = all)",
    )

    args = parser.parse_args()

    if args.embedder == "openai":
        embedder = OpenAIEmbedder()
    else:
        embedder = LocalEmbedder()

    indexer = PinIndexer()

    indexer.create_collection(force=args.recreate)
    indexer.index_entries(args.feed_url, embedder, limit=args.limit)


if __name__ == "__main__":
    main()
