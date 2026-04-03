import os
import glob
import yaml
import argparse
import hashlib
from typing import Optional

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, NamedVector
from qdrant_client.http.exceptions import ResponseHandlingException


def get_env(key: str, default: str = "") -> str:
    return os.environ.get(key, default)


def get_env_int(key: str, default: int = 0) -> int:
    val = os.environ.get(key)
    return int(val) if val else default


class BlogIndexer:
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

    def parse_markdown(self, filepath: str) -> Optional[dict]:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        if not content.startswith("---"):
            return None

        parts = content.split("---", 2)
        if len(parts) < 3:
            return None

        try:
            front_matter = yaml.safe_load(parts[1])
        except yaml.YAMLError:
            return None

        post_content = parts[2].strip()

        filename = os.path.basename(filepath).replace(".md", "")
        # 文件名格式: YYYY-MM-DD-title
        date_parts = filename.split("-")[:3]
        date_str = "-".join(date_parts) if len(date_parts) == 3 else ""
        slug = (
            "-".join(filename.split("-")[3:])
            if len(filename.split("-")) > 3
            else filename
        )

        category = front_matter.get("category", "").lower()
        year = date_parts[0] if len(date_parts) >= 1 else ""
        month = date_parts[1] if len(date_parts) >= 2 else ""
        day = date_parts[2] if len(date_parts) >= 3 else ""

        link = f"https://blog.cyeam.com/{category}/{year}/{month}/{day}/{slug}"

        return {
            "id": hashlib.sha256(filename.encode()).hexdigest()[:32],
            "title": front_matter.get("title", ""),
            "description": front_matter.get("description", ""),
            "category": front_matter.get("category", ""),
            "tags": front_matter.get("tags", []),
            "figure": front_matter.get("figure", ""),
            "content": post_content,
            "date": date_str,
            "link": link,
        }

    def embed_text(self, text: str, embedder) -> list[float]:
        return embedder.embed([text])[0]

    def index_posts(self, posts_dir: str, embedder, limit: int = 0):
        files = glob.glob(os.path.join(posts_dir, "*.md"))
        print(f"Found {len(files)} markdown files.")

        if limit > 0:
            files = files[:limit]
            print(f"Limited to {len(files)} files.")

        points = []
        for filepath in files:
            post = self.parse_markdown(filepath)
            if not post:
                print(f"Skipped (parse error): {filepath}")
                continue

            try:
                text_to_embed = (
                    f"{post['title']} {post['description']} {post['content'][:1000]}"
                )
                vector = self.embed_text(text_to_embed, embedder)

                if self.vector_size and len(vector) < self.vector_size:
                    vector = vector + [0.0] * (self.vector_size - len(vector))

                payload = {
                    "title": post["title"],
                    "description": post["description"],
                    "category": post["category"],
                    "tags": post["tags"],
                    "content": post["content"],
                    "date": post["date"],
                    "link": post["link"],
                }
                if post["figure"]:
                    payload["figure"] = post["figure"]

                if self.vector_name:
                    vector_to_use = {self.vector_name: vector}
                else:
                    vector_to_use = vector

                point = PointStruct(
                    id=post["id"],
                    vector=vector_to_use,
                    payload=payload,
                )
                points.append(point)
                print(f"Prepared: {post['title']}")

            except Exception as e:
                print(f"Error processing {post['title']}: {e}")
                continue

        if points:
            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=points,
            )
            print(f"Successfully indexed {len(points)} posts.")


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
    parser = argparse.ArgumentParser(description="Index blog posts to Qdrant")
    parser.add_argument("--posts-dir", default="_posts", help="Posts directory")
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
        help="Limit number of posts to index (0 = all)",
    )

    args = parser.parse_args()

    if args.embedder == "openai":
        embedder = OpenAIEmbedder()
    else:
        embedder = LocalEmbedder()

    indexer = BlogIndexer()

    indexer.create_collection(force=args.recreate)
    indexer.index_posts(args.posts_dir, embedder, limit=args.limit)


if __name__ == "__main__":
    main()
