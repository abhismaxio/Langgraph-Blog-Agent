from typing import TypedDict, List, Annotated
import operator
from Backend.Schema.plan import Plan

class State(TypedDict):
    topic: str
    plan: Plan
    sections: Annotated[List[str], operator.add ]
    final:str