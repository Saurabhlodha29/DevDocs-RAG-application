from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, AIMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from retrieval import retrieve
from generation import generate

class QueryState(TypedDict):
    context : str
    messages : Annotated[list[BaseMessage], add_messages]
    
def retrieve_chunks(state : QueryState):
    context_list = retrieve(state['messages'][-1].content)
    context = "\n\n".join(ctx for ctx in context_list)
    
    return {'context':context}


def generate_response(state : QueryState):
    answer = generate(state['messages'][-1].content,state['messages'],state['context'])
    
    return {'messages':[AIMessage(content = answer)]}
    

graph = StateGraph(QueryState)

graph.add_node("retrieve",retrieve_chunks)
graph.add_node("generate",generate_response)

graph.add_edge(START,"retrieve")
graph.add_edge("retrieve","generate")
graph.add_edge("generate",END)

checkpointer = InMemorySaver()

workflow = graph.compile(checkpointer = checkpointer)