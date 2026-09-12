from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage

# ----------------------------
# 1.Response Generation
# ----------------------------

model1 = ChatNVIDIA(
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


chain = prompt | model1
    
def generate(query: str, history: list[BaseMessage], context: str):
    """Streams the chain and returns the LangChain-native stream iterator.
    Each chunk is an AIMessageChunk, not a raw string."""
    
    return chain.stream({
        'user_query': query,
        'history': history,
        'context': context
    })
    

# ----------------------------
# 1.Chat Title Generation
# ----------------------------

model2 = ChatNVIDIA(
    model = 'openai/gpt-oss-20b'
)


async def generate_chat_title(query : str):
    
    messages = [
        SystemMessage(content = "Given the conversation history, provide a SHORT name for the conversation. Focus the name on the important keywords to convey the topic of the conversation. Make sure the name is in the same language as the user's language. IMPORTANT: DO NOT OUTPUT ANYTHING ASIDE FROM THE NAME. NEVER USE MORE THAN 5 WORDS."),
    
        HumanMessage(content = query)
    ]
    
    title = (await model2.ainvoke(messages)).content

    return title    