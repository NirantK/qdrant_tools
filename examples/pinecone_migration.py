from QdrantJourney import APIKeys, PineconeExport, QdrantImport

keys = ["PINECONE_API_KEY", "PINECONE_ENVIRONMENT", "QDRANT_URL", "QDRANT_API_KEY"]
api_keys = APIKeys(keys)

index_name = "example-index"  # Existing Pinecone index name

# Init Pinecone
pinecone_ex = PineconeExport(api_keys)
pinecone_index = pinecone_ex.create_index(
    index_name
)  # Assuming the index already exists


# Fetch all vector ids from Pinecone
# vector_ids = index.describe_index_stats()["index_size"]
vector_ids = ["1", "2", "3", "4", "5"]  # Example vector ids
# Fetch vectors from Pinecone and write them to a local file
# pinecone_ex.fetch_vectors(index, vector_ids)

# Init Qdrant
vector_dimension = pinecone_index.describe_index_stats()[
    "dimension"
]  # Get dimension from existing Pinecone index
qdrant = QdrantImport(api_keys)
qdrant.recreate_collection(index_name, vector_dimension)
qdrant.upsert_vectors(index_name, vector_ids, pinecone_index)
