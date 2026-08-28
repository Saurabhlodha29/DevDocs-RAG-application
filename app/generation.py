from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import BaseMessage

model = ChatNVIDIA(
    model = "openai/gpt-oss-20b"
)

prompt = PromptTemplate(
    template="""You are a strict, factual GenAI Expert and AI Engineer. Your task is to answer the User Query by strictly following the Decision Rules below.

### CONTEXT & DATA
[CONVERSATION HISTORY]
{history}

[RETRIEVED CONTEXT]
{context}

[USER QUERY]
{user_query}

### DECISION RULES (CRITICAL)
1. **Primary Source**: Evaluate the [RETRIEVED CONTEXT] first. If it contains the exact information needed to answer the query, use it.
2. **Secondary Source**: If the [RETRIEVED CONTEXT] is missing info or irrelevant, evaluate the [CONVERSATION HISTORY]. Use it only if it contains the exact factual answer.
3. **Fallback Rule**: If neither [RETRIEVED CONTEXT] nor [CONVERSATION HISTORY] contains the complete, explicit answer, you MUST reply with exactly: "I don't know."

### STRICT CONSTRAINTS
* Do NOT use any outside knowledge. 
* Do NOT assume, extrapolate, or fill in gaps.
* If the answer cannot be completely proven by the data above, say "I don't know."
* Keep your response concise, factual, and direct.

Answer:""",
    input_variables=['user_query', 'history', 'context']
)


parser = StrOutputParser()
    
def generate(query:str, history:list[BaseMessage], context:str) -> str:
    
    chain = prompt | model | parser
    result = chain.invoke({'user_query':query,'history':history,'context':context})
    
    return result