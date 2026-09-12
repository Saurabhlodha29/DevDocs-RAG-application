# # ------------PINECONE CONFIGURATION --------------

# # # Embedding model 
# # from config import embedding_model


# # # Storing into vector Store
# # import os
# # from dotenv import load_dotenv
# # from pinecone import Pinecone, ServerlessSpec
# # from langchain_pinecone import PineconeVectorStore

# # load_dotenv()

# # pc = Pinecone(
# #     api_key = os.getenv('PINECONE_API_KEY')
# # )

# # index_name = 'devdocs'

# # if not pc.has_index(index_name):
# #     pc.create_index(
# #         name = index_name,
# #         dimension = 1024,
# #         metric = 'cosine',
# #         spec = ServerlessSpec(cloud = 'aws', region = 'us-east-1')
# #     )

# # index = pc.Index(index_name)

# # vector_store = PineconeVectorStore(
# #     index = index,
# #     embedding = embedding_model
# # )


# # ------------SUPABASE CONFIGURATION --------------

import os

from dotenv import load_dotenv
from supabase import create_client
from langchain_community.vectorstores import SupabaseVectorStore

from config import embedding_model

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL or SUPABASE_KEY is missing.")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

vector_store = SupabaseVectorStore(
    client=supabase,
    embedding=embedding_model,
    table_name="document_chunks",
    query_name="match_document_chunks"
)