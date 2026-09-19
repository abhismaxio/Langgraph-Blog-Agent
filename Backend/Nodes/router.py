from Backend.Schema.router import RouterDecision
from Backend.State.state import State
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from langchain.agents import create_agent

ROUTER_SYSTEM = """You are a routing module for a technical blog planner.

Decide whether web research is needed BEFORE planning.

Modes:
- closed_book (needs_research=false): evergreen concepts.
- hybrid (needs_research=true): evergreen + needs up-to-date examples/tools/models.
- open_book (needs_research=true): volatile weekly/news/"latest"/pricing/policy.

If needs_research=true:
- Output 3–10 high-signal, scoped queries.
- For open_book weekly roundup, include queries reflecting last 7 days.
"""

def router(state:State)-> dict:
    system_msg = SystemMessage(ROUTER_SYSTEM)
    human_msg = HumanMessage(f"Topic: {state['topic']} \nAs-of date: {state['as_of']} ")
    messages = [system_msg, human_msg]
    agent = create_agent(
            model="google_genai:gemini-3.5-flash-lite",
            response_format=RouterDecision,
        )
    result = agent.invoke({"messages": messages})
    decision = result["structured_response"]


    if decision.mode == "open_book":
        recency_days = 7
    elif decision.mode == "hybrid":
        recency_days = 45
    else:
        recency_days = 365

    return {
        "needs_research": decision.needs_research,
        "mode": decision.mode,
        "queries": decision.queries,
        "recency_days": recency_days,
    }


def route_next(state: State) -> str:
    return "research" if state["needs_research"] else "orchestrator"