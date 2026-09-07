from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from schemas import QueryRequest
from langchain_core.messages import HumanMessage, AIMessage
from graph import workflow

app = FastAPI(
    title="DevDocs RAG API",
    description="RAG API for querying DevDocs knowledge base",
    version="0.1.0"
)


@app.get("/health")
def check_health(): 
    return {'status':'healthy'}

@app.post("/query")
def send_query(request : QueryRequest):
    
    def generate_response():
        for message_chunk, metadata in workflow.stream(
            {
                'messages' : [HumanMessage(content = request.query)]
            },
            config = {
                'configurable' : {
                    'thread_id' : request.thread_id
                }
            },
            stream_mode = 'messages'
        ):
            if metadata.get('langgraph_node') == 'generate' and isinstance(message_chunk, AIMessage):
                if message_chunk.content:
                    yield message_chunk.content
            
    return StreamingResponse(
        generate_response(),
        media_type = 'text/plain'
    )