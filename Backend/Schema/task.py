from pydantic import BaseModel, Field

class Task(BaseModel):
    id:int
    title:str
    description : str = Field(..., description = "what to cover")

