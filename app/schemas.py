from pydantic import BaseModel

class QueryRequest(BaseModel):
    query : str
    thread_id : str
    
class QueryResponse(BaseModel):
    answer : str

