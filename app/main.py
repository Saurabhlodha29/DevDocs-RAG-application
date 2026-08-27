from fastapi import FastAPI
from schemas import QueryRequest, QueryResponse
from retrieval import retrieve
from generation import generate

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
    
    
    context_list = retrieve(request.query)
    context = '\n\n'.join(ctx for ctx in context_list)
    
    answer = generate(request.query,context)
    
    return QueryResponse(answer = answer)