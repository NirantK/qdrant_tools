import getpass
import os
from typing import List, Optional

import pinecone
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, PointStruct, UpdateStatus


class APIKeyValidators:
    def __init__(self, keys: List[str]):
        self.keys = {key: os.getenv(key) for key in keys}

    def get_key(self, key: str):
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


class QdrantImport(VectorDatabaseHandler):
    """
    Class to handle importing vectors into Qdrant. Inherits from the VectorDatabaseHandler class.

    Args:
        index_name (str): Name of the index/collection in Qdrant.
        index_dimension (int): The dimension of the vectors to be inserted.
        qdrant_client (Optional[QdrantClient]): An instance of QdrantClient. If not provided, a new instance is created.
        batch_size (int): Size of batches in which vectors are processed. Default is 1000.
    """

    def __init__(
        self,
        index_name: str,
        index_dimension: int,
        qdrant_client: Optional[QdrantClient] = None,
        batch_size: int = 1000,
    ):
        super().__init__(batch_size)
        self.index_name = index_name
        self.index_dimension = index_dimension
        if qdrant_client is None:
            self.qdrant_client = QdrantClient(":memory:")
        else:
            self.qdrant_client = qdrant_client

    def create_collection(self, distance=Distance.COSINE):
        """
        Creates a new collection in Qdrant.

        Args:
            distance (Distance): The distance metric to be used in the collection. Default is COSINE.
        """
        self.qdrant_client.recreate_collection(
            collection_name=self.index_name,
            vectors_config=models.VectorParams(
                size=self.index_dimension, distance=distance
            ),
        )

    def upsert_vectors(self, ids: List[str], point_information: dict):
        """
        Upserts vectors to Qdrant. The vectors are processed in batches.

        Args:
            ids (List[str]): The list of vector ids.
            point_information (dict): Dictionary containing information about the vectors.

        Raises:
            InterruptedError: If the upsert operation is not completed successfully.
        """
        for i in range(0, len(ids), self.batch_size):
            i_end = min(i + self.batch_size, len(ids))
            batch_ids = ids[i:i_end]

            points = point_information["points"]
            point_ids = []
            for idx, vec in enumerate(points["vectors"].values()):
                id = idx if not str(vec["id"]).isdigit() else int(vec["id"])
                # Create a PointStruct for each vector
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

            # Perform the upsert operation
            operation_info = self.qdrant_client.upsert(
                collection_name=self.index_name, wait=True, points=point_ids
            )

            # Check if the operation was successful
            if operation_info.status != UpdateStatus.COMPLETED:
                raise InterruptedError("Upsert failed")
