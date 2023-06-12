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


class VectorDatabaseHandler:
    def __init__(self, batch_size: int = 1000):
        self.batch_size = batch_size

    def process_in_batches(self, ids: List[str], processing_function):
        for i in range(0, len(ids), self.batch_size):
            i_end = min(i + self.batch_size, len(ids))
            batch_ids = ids[i:i_end]
            processing_function(batch_ids)


class PineconeExport(VectorDatabaseHandler):
    def __init__(self, index_name: str, batch_size: int = 1000):
        super().__init__(batch_size)
        pinecone_keys = ["PINECONE_API_KEY", "PINECONE_ENVIRONMENT"]
        pinecone_api_keys = APIKeyValidators(pinecone_keys)
        self.api_key = pinecone_api_keys.get_key("PINECONE_API_KEY")
        self.environment = pinecone_api_keys.get_key("PINECONE_ENVIRONMENT")
        self.batch_size = batch_size
        pinecone.init(api_key=self.api_key, environment=self.environment)
        self.index = self.create_index(index_name)

    def fetch_vectors(self, ids: List[str]) -> dict:
        fetched_vectors = {}
        self.process_in_batches(
            ids,
            lambda batch_ids: fetched_vectors.update(
                self.index.fetch(ids=batch_ids)["vectors"]
            ),
        )
        return {
            "points": fetched_vectors,
            "dimension": self.index.describe_index_stats()["dimension"],
            "name": self.index.name,
        }

    def create_index(self, index_name: str, dimension: Optional[int] = None):
        """
        Create a Pinecone index object

        Args:
            index_name (str): _description_
            dimension (Optional[int], optional): _description_. Defaults to None.

        Raises:
            ValueError: Index does not exist in Pinecone
            ValueError: Dimension must be an integer

        Returns:
            pinecone.Index
        """
        if index_name not in pinecone.list_indexes():
            raise ValueError(f"Index {index_name} does not exist in Pinecone")
        index = pinecone.GRPCIndex(index_name=index_name)
        dimension = index.describe_index_stats()["dimension"]
        if not isinstance(dimension, int) or dimension is None:
            raise ValueError("Dimension must be an integer")
        return index

    def fetch_vectors(self, ids: List[str]) -> dict[dict, int, str]:
        """
        Fetch vectors from Pinecone into a Python object
        """
        fetched_vectors = {}
        # Fetch vectors in batches of 1000 as recommended by Pinecone
        for i in range(0, len(ids), self.batch_size):
            i_end = min(i + self.batch_size, len(ids))
            batch_ids = ids[i:i_end]
            response = self.index.fetch(ids=batch_ids)
            fetched_vectors.update(response["vectors"])

        return {
            "points": fetched_vectors,
            "dimension": self.index.describe_index_stats()["dimension"],
            "name": self.index.name,
        }


class QdrantMode:
    """Enum: Qdrant modes"""

    local = ":memory:"
    cloud = "cloud"


class QdrantImport:
    """Import vectors from any VectorDB to Qdrant"""

    def __init__(
        self,
        index_name: str,
        index_dimension: int,
        qdrant_client: Optional[QdrantClient] = None,
        batch_size: int = 1000,
    ):
        self.index_name = index_name
        self.index_dimension = index_dimension
        if qdrant_client is None:
            self.qdrant_client = QdrantClient(QdrantMode.local)
        else:
            self.qdrant_client = qdrant_client
        self.batch_size = batch_size

    def create_collection(self, distance=Distance.COSINE):
        """
        Create a new collection in Qdrant

        Args:
            index_name (str): _description_
            vector_dimension (int): _description_
            distance (_type_, optional): _description_. Defaults to Distance.COSINE.
        """
        self.qdrant_client.recreate_collection(
            collection_name=self.index_name,
            vectors_config=models.VectorParams(
                size=self.index_dimension, distance=distance
            ),
        )

    def upsert_vectors(self, ids: List[str], point_information: dict):
        """
        Upsert vectors to Qdrant

        Args:
            ids (List[str]): _description_
            index (pinecone.Index): _description_

        Raises:
            InterruptedError: Status check and raised when status is not completed
        """

        for i in range(0, len(ids), self.batch_size):
            i_end = min(i + self.batch_size, len(ids))
            batch_ids = ids[i:i_end]

            points = point_information["points"]
            point_ids = []
            # Convert vector ids to int and add text payload
            for idx, vec in enumerate(points["vectors"].values()):
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
                collection_name=self.index_name, wait=True, points=point_ids
            )

            if operation_info.status != UpdateStatus.COMPLETED:
                raise InterruptedError("Upsert failed")
