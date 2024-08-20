from pydantic import BaseModel

class BasicGroup(BaseModel):
    status:int
    message:str
    site:str
    error:int
    

