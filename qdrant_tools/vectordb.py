import getpass
import os
from typing import Callable, Dict, List, Optional

import pinecone
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, PointStruct, UpdateStatus


class APIKeyValidators:
    """
    Class to handle API key validation and retrieval.

    Args:
        keys (List[str]): List of API key names to handle.
    """

    def __init__(self, keys: List[str]):
        self.keys = {key: os.getenv(key) for key in keys}

    def get_key(self, key: str) -> str:
        """
        Retrieve the value of a specific API key. If the key is not found in the environment variables,
        prompts the user for input.

        Args:
            key (str): The name of the API key to retrieve.

        Returns:
            str: The value of the API key.
        """
        if key not in self.keys or self.keys[key] is None:
            self.keys[key] = getpass.getpass(prompt=f"Enter your {key}: ")
        return self.keys[key]


class VectorDatabaseHandler:
    """
    Base class for handling operations on a vector database.

    Args:
        batch_size (int, optional): Size of batches for processing. Defaults to 1000.
    """

    def __init__(self, batch_size: int = 1000):
        self.batch_size = batch_size

    def process_in_batches(self, ids: List[str], processing_function: Callable[[List[str]], None]):
        """
        Process the given ids in batches.

        Args:
            ids (List[str]): The ids to process.
            processing_function (Callable[[List[str]], None]): The function to apply to each batch of ids.
        """
        for i in range(0, len(ids), self.batch_size):
            i_end = min(i + self.batch_size, len(ids))
            batch_ids = ids[i:i_end]
            processing_function(batch_ids)


class PineconeExport(VectorDatabaseHandler):
    """
        Class to handleHere's the corrected code for the remaining part:

    ```python
        exporting vectors from Pinecone.

        Args:
            index_name (str): The name of the Pinecone index to export from.
            batch_size (int, optional): Size of batches for processing. Defaults to 1000.
    """

    def __init__(self, index_name: str, batch_size: int = 1000):
        super().__init__(batch_size)
        pinecone_keys = ["PINECONE_API_KEY", "PINECONE_ENVIRONMENT"]
        pinecone_api_keys = APIKeyValidators(pinecone_keys)
        self.api_key = pinecone_api_keys.get_key("PINECONE_API_KEY")
        self.environment = pinecone_api_keys.get_key("PINECONE_ENVIRONMENT")
        pinecone.init(api_key=self.api_key, environment=self.environment)
        self.index = pinecone.Index(index_name=index_name)
        self.index_name = index_name

    def fetch_vectors(self, ids: List[str]) -> Dict[str, dict]:
        """
        Fetch vectors from the Pinecone index.

        Args:
            ids (List[str]): The ids of the vectors to fetch.

        Returns:
            Dict[str, dict]: A dictionary with the fetched vectors, the dimension of the index, and the index name.
        """
        fetched_vectors = {}
        self.process_in_batches(
            ids,
            lambda batch_ids: fetched_vectors.update(self.index.fetch(ids=batch_ids)["vectors"]),
        )
        return {
            "ids": ids,
            "points": fetched_vectors,
            "index_dimension": self.index.describe_index_stats()["dimension"],
            "index_name": self.index_name,
        }


class QdrantImport(VectorDatabaseHandler):
    """
    Class to handle importing vectors into Qdrant.
    Inherits from the VectorDatabaseHandler class.

    Args:
        index_name (str): Name of the index/collection in Qdrant.
        index_dimension (int): The dimension of the vectors to be inserted.
        qdrant_client (Optional[QdrantClient]): An instance of QdrantClient.
        If not provided, a new instance is created.
        batch_size (int): Size of batches in which vectors are processed.
    """

    def __init__(
        self,
        ids: List[str],
        index_name: str,
        index_dimension: int,
        points: List,
        qdrant_client: Optional[QdrantClient] = None,
        batch_size: int = 1024,
    ):
        super().__init__(batch_size)
        self.index_name = index_name
        self.index_dimension = index_dimension
        if qdrant_client is None:
            self.qdrant_client = QdrantClient(":memory:")
        else:
            self.qdrant_client = qdrant_client
        self.points = points
        self.ids = ids

    def create_collection(self, distance=Distance.COSINE):
        """
        Creates a new collection in Qdrant.

        Args:
            distance (Distance): The distance metric to be used in the collection.
            Default is COSINE.
        """
        self.qdrant_client.recreate_collection(
            collection_name=self.index_name,
            vectors_config=models.VectorParams(size=self.index_dimension, distance=distance),
        )

    def upsert_vectors(self):
        """
        Upserts vectors to Qdrant. The vectors are processed in batches.

        Raises:
            InterruptedError: If the upsert operation is not completed successfully.
        """
        self.process_in_batches(
            self.ids, lambda batch_ids: self.upsert_batch(batch_ids)
        )  # pylint: disable=unnecessary-lambda

    def upsert_batch(self, batch_ids: List[str]):
        """
        Helper function for upsert_vectors to process each batch of ids.

        Args:
            batch_ids (List[str]): The list of vector ids in the current batch.
        """
        points = {id: self.points[id] for id in batch_ids}
        point_ids = []
        for idx, vec in enumerate(points.values()):
            point_id = idx if not str(vec["id"]).isdigit() else int(vec["id"])
            # Create a PointStruct for each vector
            # Use 'text' if present in 'metadata', else use the entire 'metadata'
            payload = (
                vec["metadata"]
                if "text" not in vec["metadata"]
                else {"text": vec["metadata"]["text"], "metadata": vec["metadata"]}
            )
            point_ids.append(PointStruct(id=point_id, vector=vec["values"], payload=payload))

        # Perform the upsert operation
        operation_info = self.qdrant_client.upsert(collection_name=self.index_name, wait=True, points=point_ids)

        # Check if the operation was successful
        if operation_info.status != UpdateStatus.COMPLETED:
            raise InterruptedError("Upsert failed")
