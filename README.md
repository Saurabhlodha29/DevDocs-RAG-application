# This is the DevDocs RAG Application

Following will be the entire summary step-by-step of everything that is going to be done in this project/repo.

## The entire project progress is listed below:

### Following is the environment setup for the project:

1. Create a `requirements.txt` file with all the requirements in it for easy installation.

2. Create the virtual environment and install the requirements in it.

3. Create the required directory and folder structure for the application for easy management.

4. Insert all the documents in a dedicated folder in the root folder of the project.

### Testing of the various components individually:

5. Test whether the individual components are working correctly:

   **A. LLM API**

   Test whether the LLM API is working correctly.

   **B. Document Loader**

   Test whether the document loader is loading documents correctly.

   Since our PDFs have a complex structure containing text, images, code snippets, tables, and flow diagrams, use `PyMuPDF4LLMLoader` from the `langchain_pymupdf4llm` package. This loader converts the PDF into a structured Markdown string, making it easier to preserve and extract the document's contents and perform structured chunking.

   **C. Text Splitters**

   Test the text-splitting strategy.

   Use a **hybrid chunking strategy**:

   * `MarkdownHeaderTextSplitter` as the primary structural splitter. It splits the Markdown based on headings and preserves heading information in the chunk metadata, allowing the retrieved chunks to retain their document hierarchy and contextual information.

   * `RecursiveCharacterTextSplitter` as the secondary size-based splitter. It further divides sections produced by the Markdown splitter when they exceed the desired chunk size.

   **D. Embedding Model**

   Install and test the embedding generation model.

   Use the cloud-based **Voyage AI `voyage-4-large`** embedding model through its API. This provides the same embedding model for both document ingestion and dynamic user-query embedding, while avoiding the need to keep a local embedding model loaded on the deployment server.

### Building the RAG ingestion pipeline:

6. Build and test the complete document ingestion pipeline:

   **Document Loading → Markdown Conversion → Structural Chunking → Size-Based Chunking → Embedding Generation → Vector Storage**

   **A. Document Loading**

   Load the PDF using `PyMuPDF4LLMLoader` and convert it into a structured Markdown string.

   **B. Text Splitting**

   Apply the hybrid Markdown-header + recursive text-splitting strategy to generate the final document chunks while preserving relevant heading metadata.

   **C. Embedding Generation**

   Generate embeddings for the final chunks using the cloud-based `voyage-4-large` model through the Voyage AI API.

   **D. Vector Storage**

   Store the generated embeddings in a **Pinecone** cloud vector index.

   The Pinecone index uses:

   * Dimension: `1024`
   * Metric: `cosine`
   * Deployment: Serverless AWS

7. Test the ingestion pipeline using a single PDF document.

8. Verify that the generated vectors are successfully stored in Pinecone.

9. Test semantic retrieval from Pinecone using sample questions and inspect the retrieved chunks and similarity scores.

10. Verify that the retrieved chunks are semantically relevant to the submitted questions and that the document/section metadata is preserved correctly.

### Building and testing the RAG generation pipeline:

11. Build the generation pipeline using the retrieved context and user query.

**User Query → Retriever → Retrieved Context → Prompt → LLM → Generated Response**

12. Use NVIDIA's hosted `gpt-oss-20b` model through `ChatNVIDIA` for response generation.

13. Create a prompt that instructs the LLM to answer the user's question using the retrieved context only and return `"I don't know"` when the provided context is insufficient.

14. Test the complete retrieval + generation pipeline using relevant questions from the knowledge base.

15. Test the pipeline using out-of-domain questions to verify that the model does not hallucinate answers when relevant context is unavailable.

16. Verify that the generation pipeline correctly produces `"I don't know"` for questions unrelated to the available knowledge base.

### Current completed state:

17. The complete basic RAG pipeline has been successfully tested end-to-end:

**PDF → PyMuPDF4LLM → Hybrid Chunking → Voyage `voyage-4-large` → Pinecone → Retriever → NVIDIA `gpt-oss-20b` → Response**

18. Voyage AI is currently being used as the embedding provider instead of the previously tested local `Qwen3-Embedding-4B` model.

19. The Pinecone index has been recreated for the Voyage embedding space with `1024` dimensions.

20. Semantic retrieval has been successfully tested with relevant queries.

21. LLM generation has been successfully tested with retrieved context using NVIDIA `gpt-oss-20b`.

22. Out-of-domain query testing has been completed successfully. For example, an unrelated question such as `"How to make pizza?"` resulted in `"I don't know"`, confirming the current prompt's context-grounding behavior.