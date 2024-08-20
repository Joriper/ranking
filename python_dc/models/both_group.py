from pydantic import BaseModel

class BothGroup(BaseModel):
    status:int
    message:str
    site:str
    error:int
    type: str
    queue_id: str
    

