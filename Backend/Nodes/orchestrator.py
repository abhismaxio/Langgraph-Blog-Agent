from langchain.messages import HumanMessage, AIMessage, SystemMessage
from Backend.Schema.plan import Plan
from Backend.State.state import State
from langchain.agents import create_agent

from dotenv import load_dotenv
load_dotenv()


ORCH_SYSTEM = """You are a senior technical writer and developer advocate.
Produce a highly actionable outline for a technical blog post.

Requirements:
- 5–9 tasks, each with goal + 3–6 bullets + target_words.
- Tags are flexible; do not force a fixed taxonomy.

Grounding:
- closed_book: evergreen, no evidence dependence.
- hybrid: use evidence for up-to-date examples; mark those tasks requires_research=True and requires_citations=True.
- open_book: weekly/news roundup:
  - Set blog_kind="news_roundup"
  - No tutorial content unless requested
  - If evidence is weak, plan should explicitly reflect that (don’t invent events).

Output must match Plan schema.
"""

def orchestrator(state: State)-> dict:
    mode = state.get("mode", "closed_book")
    evidence = state.get("evidence", [])

    forced_kind = "news_roundup" if mode == "open_book" else None

    system_message = SystemMessage(content=ORCH_SYSTEM)
    human_msg = HumanMessage(
        content=(
            f"Topic: {state['topic']}\n"
            f"Mode: {mode}\n"
            f"As-of: {state['as_of']} (recency_days={state['recency_days']})\n"
            f"{'Force blog_kind=news_roundup' if forced_kind else ''}\n\n"
            f"Evidence:\n{[e.model_dump() for e in evidence][:16]}"
        )
    )
    messages = [system_message, human_msg]
    agent = create_agent(
        model="google_genai:gemini-3.5-flash-lite",
        response_format=Plan,
    )
    result = agent.invoke({"messages": messages})
    plan = result["structured_response"]
    if forced_kind:
        plan.blog_kind = "news_roundup"


    return {"plan": plan}

              