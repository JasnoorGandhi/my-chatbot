from sqlalchemy import inspect
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import uuid
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Qdrant client
qdrant_client = QdrantClient(url=os.getenv("QDRANT_HOST"), api_key=os.getenv("QDRANT_API_KEY"))
qdrant_collection = "schema_embeddings"

# Initialize SentenceTransformer
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Function to extract schema and store embeddings in Qdrant
def extract_and_embed_schema(engine):
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    schema_metadata = {}
    
    for table in tables:
        columns = inspector.get_columns(table)
        schema_text = f"Table: {table}\nColumns: {', '.join([col['name'] for col in columns])}"
        schema_metadata[table] = schema_text
        
        # Generate embedding for schema
        embedding = embedder.encode(schema_text)
        
        # Store in Qdrant
        qdrant_client.upsert(
            collection_name=qdrant_collection,
            points=[
                {
                    "id": str(uuid.uuid4()),
                    "vector": embedding.tolist(),
                    "payload": {"table": table, "schema": schema_text}
                }
            ]
        )
    return schema_metadata

# Function to retrieve relevant schema from Qdrant
def retrieve_relevant_schema(query, top_k=3):
    query_embedding = embedder.encode(query).tolist()
    search_result = qdrant_client.search(
        collection_name=qdrant_collection,
        query_vector=query_embedding,
        limit=top_k
    )
    return [hit.payload["schema"] for hit in search_result]

# Function to initialize Qdrant collection
def init_qdrant_collection():
    if not qdrant_client.collection_exists(qdrant_collection):
        qdrant_client.create_collection(
            collection_name=qdrant_collection,
            vectors_config={"size": 384, "distance": "Cosine"}
        )