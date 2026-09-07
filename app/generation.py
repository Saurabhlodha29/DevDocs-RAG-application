from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import BaseMessage

model = ChatNVIDIA(
    model = "openai/gpt-oss-20b"
)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a strict, factual GenAI Expert and AI Engineer.
        
        Answer the user's question using these rules:
        
        1. Use the retrieved context first.
        2. If the retrieved context does not contain the answer, use the conversation history.
        3. If neither contains the complete answer, reply exactly:
        "I don't know."
        
        Do not use outside knowledge.
        Do not assume or fill gaps.
        Keep your response concise, factual, and direct."""
    ),

    MessagesPlaceholder(variable_name="history"),

    (
        "human",
        """[RETRIEVED CONTEXT]
        {context}
        
        [USER QUERY]
        {user_query}"""
    )
])


chain = prompt | model
    
def generate(query: str, history: list[BaseMessage], context: str):
    """Streams the chain and returns the LangChain-native stream iterator.
    Each chunk is an AIMessageChunk, not a raw string."""
    
    return chain.stream({
        'user_query': query,
        'history': history,
        'context': context
    })