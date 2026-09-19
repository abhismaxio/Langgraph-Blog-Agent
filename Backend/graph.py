from datetime import date
from typing import Optional

from langgraph.graph import START, END, StateGraph

from Backend.Nodes.fanout import fanout
from Backend.Nodes.orchestrator import orchestrator
from Backend.Nodes.reducer import merge_content
from Backend.Nodes.worker import Worker
from Backend.State.state import State
from Backend.Nodes.router import router, route_next
from Backend.Nodes.research import research_node
from Backend.Nodes.image import decide_images, generate_and_place_images

# Image processing runs after all worker sections have been merged.
reducer_graph = StateGraph(State)
reducer_graph.add_node("merge_content", merge_content)
reducer_graph.add_node("decide_images", decide_images)
reducer_graph.add_node("generate_and_place_images", generate_and_place_images)
reducer_graph.add_edge(START, "merge_content")
reducer_graph.add_edge("merge_content", "decide_images")
reducer_graph.add_edge("decide_images", "generate_and_place_images")
reducer_graph.add_edge("generate_and_place_images", END)
reducer_subgraph = reducer_graph.compile()

# Build the main graph.
g = StateGraph(State)
g.add_node("router", router)
g.add_node("research", research_node)
g.add_node("orchestrator", orchestrator)
g.add_node("worker", Worker)
g.add_node("reducer", reducer_subgraph)

g.add_edge(START, "router")
g.add_conditional_edges("router", route_next, {"research": "research", "orchestrator": "orchestrator"})
g.add_edge("research", "orchestrator")

g.add_conditional_edges("orchestrator", fanout, ["worker"])
g.add_edge("worker", "reducer")
g.add_edge("reducer", END)

app = g.compile()


as_of = date.today().isoformat()
def run(topic: str, as_of: Optional[str] = None):
    if as_of is None:
        as_of = date.today().isoformat()

    out = app.invoke(
        {
            "topic": topic,
            "mode": "",
            "needs_research": False,
            "queries": [],
            "evidence": [],
            "plan": None,
            "as_of": as_of,
            "recency_days": 7,
            "sections": [],
            "merged_md": "",
            "md_with_placeholders": "",
            "image_specs": [],
            "final": "",
        }
    )

    return out

print(run("Self Attention in Transformer Architecture"))