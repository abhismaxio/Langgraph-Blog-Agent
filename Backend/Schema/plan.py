from pydantic import BaseModel, Field
from typing import List
from Backend.Schema.task import Task

class Plan(BaseModel):
    blog_title: str
    tasks: List[Task]