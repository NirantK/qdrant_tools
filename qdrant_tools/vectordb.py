import getpass
import os
from typing import List, Optional

import pinecone
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, PointStruct, UpdateStatus


class APIKeyValidators:
    """
    Validate API keys and store them in memory

    Returns:
       key (str): API key
    """

    # Add .env support
    def __init__(self, keys: List[str]):
        self.keys = {key: os.getenv(key) for key in keys}

    def get_key(self, key: str):
        """
        Get API key from environment variables or prompt user for input

        Args:
            key (str): _description_

        Returns:
            _type_: _description_
        """
        if self.keys[key] is None:
            self.keys[key] = getpass.getpass(prompt=f"Enter your {key}: ")
        return self.keys[key]


class PineconeExport:
    """Export vectors from Pinecone to an in-memory Python object"""

    def __init__(self, index_name: str, batch_size: int = 1000):
        pinecone_keys = ["PINECONE_API_KEY", "PINECONE_ENVIRONMENT"]
        pinecone_api_keys = APIKeyValidators(pinecone_keys)
        self.api_key = pinecone_api_keys.get_key("PINECONE_API_KEY")
        self.environment = pinecone_api_keys.get_key("PINECONE_ENVIRONMENT")
        self.batch_size = batch_size
        pinecone.init(api_key=self.api_key, environment=self.environment)
        self.index = self.create_index(index_name)

    def create_index(self, index_name: str, dimension: Optional[int] = None):
        """
        Create a Pinecone index object

        Args:
            index_name (str): _description_
            dimension (Optional[int], optional): _description_. Defaults to None.

        Raises:
            ValueError: _description_
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        if index_name not in pinecone.list_indexes():
            raise ValueError(f"Index {index_name} does not exist in Pinecone")
        index = pinecone.Index(index_name=index_name)
        dimension = index.describe_index_stats()["dimension"]
        if not isinstance(dimension, int) or dimension is None:
            raise ValueError("Dimension must be an integer")
        return index

    def fetch_vectors(self, ids: List[str]):
        """
        Fetch vectors from Pinecone and write them to a local file
        """
        fetched_vectors = {}
        # Fetch vectors in batches of 1000 as recommended by Pinecone
        for i in range(0, len(ids), self.batch_size):
            i_end = min(i + self.batch_size, len(ids))
            batch_ids = ids[i:i_end]
            response = self.index.fetch(ids=batch_ids)
            fetched_vectors.update(response["vectors"])

        return fetched_vectors


class QdrantMode:
    """Enum: Qdrant modes"""

    local = ":memory:"
    cloud = "cloud"


class QdrantImport:
    """Import vectors from any VectorDB to Qdrant"""

    def __init__(self, mode: QdrantMode = QdrantMode.local, batch_size: int = 1000):
        if mode == QdrantMode.cloud:
            qdrant_api_keys = APIKeyValidators(["QDRANT_URL", "QDRANT_API_KEY"])
            self.qdrant_url = qdrant_api_keys.get_key("QDRANT_URL")
            self.qdrant_api_key = qdrant_api_keys.get_key("QDRANT_API_KEY")
            self.qdrant_client = QdrantClient(
                self.qdrant_url,
                prefer_grpc=True,
                api_key=self.qdrant_api_key,
            )
        elif mode == QdrantMode.local:
            self.qdrant_client = QdrantClient(QdrantMode.local)
        self.batch_size = batch_size

    def create_collection(
        self, index_name: str, vector_dimension: int, distance=Distance.COSINE
    ):
        """
        Create a new collection in Qdrant

        Args:
            index_name (str): _description_
            vector_dimension (int): _description_
            distance (_type_, optional): _description_. Defaults to Distance.COSINE.
        """
        self.qdrant_client.recreate_collection(
            collection_name=index_name,
            vectors_config=models.VectorParams(
                size=vector_dimension, distance=distance
            ),
        )

    def upsert_vectors(self, ids: List[str], index: pinecone.Index):
        """
        Upsert vectors to Qdrant

        Args:
            ids (List[str]): _description_
            index (pinecone.Index): _description_

        Raises:
            InterruptedError: Status check and raised when status is not completed
        """

        index_name = index.name
        for i in range(0, len(ids), self.batch_size):
            i_end = min(i + self.batch_size, len(ids))
            batch_ids = ids[i:i_end]
            fetched_vectors = index.fetch(ids=batch_ids)

            point_ids = []
            # Convert vector ids to int and add text payload
            for idx, vec in enumerate(fetched_vectors["vectors"].values()):
                id = idx + i if not str(vec["id"]).isdigit() else int(vec["id"])
                point_ids.append(
                    PointStruct(
                        id=id,
                        vector=vec["values"],
                        payload={
                            "text": vec["metadata"]["text"],
                            "original_id": vec["id"],
                        },
                    )
                )

            operation_info = self.qdrant_client.upsert(
                collection_name=index_name, wait=True, points=point_ids
            )

            if operation_info.status != UpdateStatus.COMPLETED:
                raise InterruptedError("Upsert failed")
