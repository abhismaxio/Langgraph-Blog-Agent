from Backend.State.state import State
from langgraph.types import Send

def fanout(state:State):
    """ Worker node is used here"""
    return [Send("worker", {"task": task, "topic":state["topic"], "plan":state["plan"]})
            for task in state["plan"].tasks
            ]