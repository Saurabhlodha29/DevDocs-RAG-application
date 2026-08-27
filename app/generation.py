from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

model = ChatNVIDIA(
    model = "openai/gpt-oss-20b"
)

prompt = PromptTemplate(
    template = """
    You are an AI Engineer and GenAI expert who build meaningful AI applications using python frameworks.
    Solve the following student doubt to the best of your knowledge based on the given context ONLY, 
    if the context is not sufficient for generating accurate results, JUST SAY "I don't know".
    
    User Query : {user_query},\n
    Given Context : \n {context}
    """,
    input_variables = ['user_query','context']
)

parser = StrOutputParser()
    
def generate(query:str, context:str) -> str:
    
    chain = prompt | model | parser
    result = chain.invoke({'user_query':query,'context':context})
    
    return result