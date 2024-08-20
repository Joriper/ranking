from pydantic import BaseModel

class FullGroups(BaseModel):
    status:int
    message:str
    site:str
    error:int
    
