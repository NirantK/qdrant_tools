import getpass
import os
from typing import List, Optional

import pinecone
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, PointStruct, UpdateStatus


class APIKeys:
    def __init__(self, keys: List[str]):
        self.keys = {key: os.getenv(key) for key in keys}

    def get_key(self, key: str):
        if self.keys[key] is None:
            self.keys[key] = getpass.getpass(
                prompt=f"Enter your {key.replace('_', ' ')}: "
            )
        return self.keys[key]


class PineconeExport:
    def __init__(self, api_keys: APIKeys):
        self.api_key = api_keys.get_key("PINECONE_API_KEY")
        self.environment = api_keys.get_key("PINECONE_ENVIRONMENT")
        pinecone.init(api_key=self.api_key, environment=self.environment)

    def create_index(self, index_name: str, dimension: Optional[int] = None):
        if index_name not in pinecone.list_indexes():
            if not isinstance(dimension, int) or dimension is None:
                raise ValueError("Dimension must be an integer")
            pinecone.create_index(index_name, dimension=dimension, metric="cosine")
        return pinecone.Index(index_name=index_name)

    def fetch_vectors(self, index, ids):
        fetched_vectors = {}
        # Fetch vectors in batches of 1000 as recommended by Pinecone
        for i in range(0, len(ids), 1000):
            i_end = min(i + 1000, len(ids))
            batch_ids = ids[i:i_end]
            response = index.fetch(ids=batch_ids)
            fetched_vectors.update(response["vectors"])

        # # Write vectors to a local JSON file
        # with open("fetched_vectors.json", "w") as f:
        #     json.dump(fetched_vectors, f)

        return fetched_vectors


class QdrantImport:
    def __init__(self, api_keys: APIKeys):
        self.qdrant_url = api_keys.get_key("QDRANT_URL")
        self.qdrant_api_key = api_keys.get_key("QDRANT_API_KEY")
        self.qdrant_client = QdrantClient(
            self.qdrant_url,
            prefer_grpc=True,
            api_key=self.qdrant_api_key,
        )

    def recreate_collection(
        self, index_name: str, vector_dimension: int, distance=Distance.COSINE
    ):
        self.qdrant_client.recreate_collection(
            collection_name=index_name,
            vectors_config=models.VectorParams(
                size=vector_dimension, distance=distance
            ),
        )

    def upsert_vectors(self, index_name: str, ids: List[str], index):
        for i in range(0, len(ids), 1000):
            i_end = min(i + 1000, len(ids))
            batch_ids = ids[i:i_end]
            fetched_vectors = index.fetch(ids=batch_ids)
            qdrant_vectors = [
                PointStruct(
                    id=int(i["id"]),
                    vector=i["values"],
                    payload={"text": i["metadata"]["text"]},
                )
                for i in fetched_vectors["vectors"].values()
            ]
            operation_info = self.qdrant_client.upsert(
                collection_name=index_name, wait=True, points=qdrant_vectors
            )

            if operation_info.status != UpdateStatus.COMPLETED:
                raise Exception("Upsert failed")

        print("Upsert completed")
