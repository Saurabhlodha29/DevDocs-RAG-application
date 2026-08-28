from fastapi import FastAPI
from schemas import QueryRequest, QueryResponse
from langchain_core.messages import HumanMessage
from graph import workflow

app = FastAPI(
    title="DevDocs RAG API",
    description="RAG API for querying DevDocs knowledge base",
    version="0.1.0"
)


@app.get("/health")
def check_health(): 
    return {'status':'healthy'}

@app.post("/query",response_model = QueryResponse)
def send_query(request : QueryRequest):
    
    answer = workflow.invoke({
        'messages' : [HumanMessage(content = request.query)]},
        config = {'configurable':{'thread_id':request.thread_id}}
        )['messages'][-1].content
    
    return QueryResponse(answer = answer)