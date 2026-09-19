from pydantic import BaseModel, Field
from typing import List, Literal
from Backend.Schema.task import Task

class Plan(BaseModel):
    blog_title: str
    audience: str
    tone: str
    blog_kind: Literal["explainer", "tutorial", "news_roundup", "comparison", "system_design","backend","story"] = "explainer"
    constraints: List[str] = Field(default_factory=list)
    tasks: List[Task]