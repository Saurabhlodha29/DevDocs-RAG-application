from pydantic import BaseModel

class QueryRequest(BaseModel):
    query : str
    thread_id : str
    
class TitleRequest(BaseModel):
    query : str
    
class TitleResponse(BaseModel):
    title : str
    
class ConversationRequest(BaseModel):
    thread_id : str
    title : str
    
class ConversationUpdateRequest(BaseModel):
    thread_id : str
    title : str