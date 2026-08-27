# Embedding model 
# Stored this model into config.py because we will use this in ingestion.py, retrieval.py and vector_store.py

from langchain_voyageai import VoyageAIEmbeddings

from dotenv import load_dotenv

load_dotenv()

embedding_model = VoyageAIEmbeddings(
    model="voyage-4-large"
)