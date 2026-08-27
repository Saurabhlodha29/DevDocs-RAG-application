# # Step-1 : Document Loading
# from langchain_pymupdf4llm import PyMuPDF4LLMLoader
# # from langchain_community.document_loaders import DirectoryLoader

# loader = PyMuPDF4LLMLoader(
#     file_path = "../documents/LangChain_Chapter1_Introduction_Notes.pdf",
#     mode = "single"
# )

# document = loader.load()

# markdown_document = document[0].page_content


# # Step-2 : Text Splitting
# from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

# headers_to_split_on = [
#     ("#", "Main_Topic"),
#     ("##", "Sub_Section"),
#     ("###", "Nested_Topic"),
# ]

# markdown_splitter = MarkdownHeaderTextSplitter(
#     headers_to_split_on = headers_to_split_on
# )

# structural_chunks = markdown_splitter.split_text(markdown_document)   # returns documents list

# size_text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size = 600,
#     chunk_overlap = 75
# )

# final_chunks = size_text_splitter.split_documents(structural_chunks)