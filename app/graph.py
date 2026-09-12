from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, AIMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.postgres import PostgresSaver
from retrieval import retrieve
from generation import generate
import os

class QueryState(TypedDict):
    context : str
    messages : Annotated[list[BaseMessage], add_messages]
    
def retrieve_chunks(state : QueryState):
    context_list = retrieve(state['messages'][-1].content)
    context = "\n\n".join(ctx for ctx in context_list)
    
    return {'context':context}


def generate_response(state: QueryState):
    query = state['messages'][-1].content
    history = state['messages'][:-1]

    stream = generate(query=query, history=history, context=state['context'])

    full_chunk = None
    for chunk in stream:
        full_chunk = chunk if full_chunk is None else full_chunk + chunk

    # Preserve the id from the streamed chunks — this is what stops
    # add_messages from treating the final result as a NEW message.
    final_message = AIMessage(content=full_chunk.content, id=full_chunk.id)

    return {'messages': [final_message]}
    

graph = StateGraph(QueryState)

graph.add_node("retrieve",retrieve_chunks)
graph.add_node("generate",generate_response)

graph.add_edge(START,"retrieve")
graph.add_edge("retrieve","generate")
graph.add_edge("generate",END)

# Configuring Postgre Checkpointer to enable Supabase Chatstorage

DB_URI = os.getenv('DATABASE_URL')

checkpointer_context = PostgresSaver.from_conn_string(DB_URI)
checkpointer = checkpointer_context.__enter__()

checkpointer.setup()

chatbot = graph.compile(checkpointer = checkpointer)