# # Test for working of the LLM API
# from langchain_groq import ChatGroq
# from dotenv import load_dotenv

# load_dotenv()

# model = ChatGroq(model = "openai/gpt-oss-20b")

# result = model.invoke('hi')
# print(result)

# # Testing for document loader
# from langchain_pymupdf4llm import PyMuPDF4LLMLoader

# loader = PyMuPDF4LLMLoader(
#     file_path = "../documents/LangChain_Chapter3_The_Model_Component_Notes.pdf",
#     mode = "single"
# )

# documents = loader.load()
# print(type(documents[0].page_content))


# Splitter Test
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

file_path = 'test_markdown.md'

with open(file_path,'r',encoding = 'utf-8') as f:
    markdown_content = f.read()
    
headers_to_split_on = [
    ("#", "Main_Topic"),
    ("##", "Sub_Section"),
    ("###", "Nested_Topic"),
]

markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on = headers_to_split_on
)

structural_chunks = markdown_splitter.split_text(markdown_content)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1500,
    chunk_overlap = 200
)

final_chunks = text_splitter.split_documents(structural_chunks)

sample_chunk = final_chunks[4]

print('_____Metadata_____\n')
print(sample_chunk.metadata)
print('\\n____Page Content____\n')
print(sample_chunk.page_content)