from langgraph.graph import START, END, StateGraph

from Backend.Nodes.fanout import fanout
from Backend.Nodes.orchestrator import orchestrator
from Backend.Nodes.reducer import Reducer
from Backend.Nodes.worker import Worker
from Backend.State.state import State


g = StateGraph(State)
g.add_node("orchestrator", orchestrator)
g.add_node("worker", Worker)
g.add_node("reducer", Reducer)
g.add_edge(START, "orchestrator")
g.add_conditional_edges("orchestrator", fanout, "worker")
g.add_edge("worker", "reducer")
g.add_edge("reducer", END)

app = g.compile()
out = app.invoke({"topic": "Write a TINY blog on Self Attention", "sections": []})
print(out)