# Embedding model 
from config import embedding_model


# Storing into vector Store
import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

load_dotenv()

pc = Pinecone(
    api_key = os.getenv('PINECONE_API_KEY')
)

index_name = 'devdocs'

if not pc.has_index(index_name):
    pc.create_index(
        name = index_name,
        dimension = 1024,
        metric = 'cosine',
        spec = ServerlessSpec(cloud = 'aws', region = 'us-east-1')
    )

index = pc.Index(index_name)

vector_store = PineconeVectorStore(
    index = index,
    embedding = embedding_model
)