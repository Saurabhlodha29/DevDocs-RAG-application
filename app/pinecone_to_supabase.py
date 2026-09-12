# import os
# from dotenv import load_dotenv
# from supabase import create_client

# from vector_store import index


# load_dotenv()


# # --------------------------------------------------
# # Supabase connection
# # --------------------------------------------------

# supabase = create_client(
#     os.getenv("SUPABASE_URL"),
#     os.getenv("SUPABASE_KEY")
# )


# # --------------------------------------------------
# # Get all Pinecone vector IDs
# # --------------------------------------------------

# ids = next(index.list())

# print(f"Found {len(ids)} vectors in Pinecone.")


# # --------------------------------------------------
# # Fetch vectors in batches
# # --------------------------------------------------

# batch_size = 50
# total_inserted = 0

# for start in range(0, len(ids), batch_size):

#     batch_ids = ids[start:start + batch_size]

#     result = index.fetch(ids=batch_ids)

#     rows = []

#     for vector in result.vectors.values():

#         rows.append({
#             "content": vector.metadata["text"],
#             "metadata": vector.metadata,
#             "embedding": vector.values
#         })

#     # Insert this batch into Supabase
#     supabase.table("document_chunks").insert(rows).execute()

#     total_inserted += len(rows)

#     print(
#         f"Inserted {total_inserted}/{len(ids)} vectors."
#     )


# # --------------------------------------------------
# # Final result
# # --------------------------------------------------

# print("\nMigration completed successfully.")
# print(f"Total vectors migrated: {total_inserted}")