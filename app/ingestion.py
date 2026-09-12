# import os
# from pathlib import Path

# from dotenv import load_dotenv
# from langchain_pymupdf4llm import PyMuPDF4LLMLoader
# from langchain_text_splitters import (
#     MarkdownHeaderTextSplitter,
#     RecursiveCharacterTextSplitter
# )

# from config import embedding_model
# from vector_store import supabase


# load_dotenv()


# # --------------------------------------------------
# # Configuration
# # --------------------------------------------------

# DOCUMENTS_DIR = Path("../documents")


# headers_to_split_on = [
#     ("#", "Main_Topic"),
#     ("##", "Sub_Section"),
#     ("###", "Nested_Topic"),
# ]

# markdown_splitter = MarkdownHeaderTextSplitter(
#     headers_to_split_on=headers_to_split_on
# )

# size_text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=600,
#     chunk_overlap=75
# )


# # --------------------------------------------------
# # Process one PDF
# # --------------------------------------------------

# def ingest_document(file_path: Path):

#     print(f"\nProcessing: {file_path.name}")

#     # 1. Load document
#     loader = PyMuPDF4LLMLoader(
#         file_path=str(file_path),
#         mode="single"
#     )

#     document = loader.load()

#     markdown_document = document[0].page_content

#     # 2. Structural splitting
#     structural_chunks = markdown_splitter.split_text(
#         markdown_document
#     )

#     # 3. Size-based splitting
#     final_chunks = size_text_splitter.split_documents(
#         structural_chunks
#     )

#     print(f"Created {len(final_chunks)} chunks.")

#     # 4. Create document record
#     document_response = (
#         supabase
#         .table("documents")
#         .insert({
#             "filename": file_path.name
#         })
#         .execute()
#     )

#     document_id = document_response.data[0]["id"]

#     print(f"Created document record: {document_id}")

#     # 5. Generate embeddings
#     texts = [
#         chunk.page_content
#         for chunk in final_chunks
#     ]

#     embeddings = embedding_model.embed_documents(
#         texts
#     )

#     # 6. Prepare chunk rows
#     rows = []

#     for chunk, embedding in zip(
#         final_chunks,
#         embeddings
#     ):

#         rows.append({
#             "document_id": document_id,
#             "content": chunk.page_content,
#             "metadata": chunk.metadata,
#             "embedding": embedding
#         })

#     # 7. Store chunks
#     supabase \
#         .table("document_chunks") \
#         .insert(rows) \
#         .execute()

#     print(
#         f"Inserted {len(rows)} chunks "
#         f"for document {document_id}."
#     )

#     print(f"Finished: {file_path.name}")


# # --------------------------------------------------
# # Process all PDFs
# # --------------------------------------------------

# def ingest_all_documents():

#     pdf_files = list(
#         DOCUMENTS_DIR.glob("*.pdf")
#     )

#     print(
#         f"Found {len(pdf_files)} PDF(s)."
#     )

#     for file_path in pdf_files:
#         ingest_document(file_path)


# if __name__ == "__main__":
#     ingest_all_documents()