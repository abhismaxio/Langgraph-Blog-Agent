from langchain.messages import HumanMessage, AIMessage, SystemMessage
from Backend.Schema.plan import Plan
from Backend.State.state import State
from langchain.agents import create_agent

from dotenv import load_dotenv
load_dotenv()

def Worker (payload: dict) -> dict:
    task = payload["task"]
    topic = payload["topic"]
    plan = payload["plan"]
    blog_title = plan.blog_title


    system_msg = SystemMessage("You are a helpful assistant that writes blog sections.")
    human_msg = HumanMessage(
        f"Blog: {blog_title}\n"
        f"Topic: {topic}\n\n"
        f"Section: {task.title}\n"
        f"Brief: {task.description}\n\n"
        "Return only the section content in Markdown.")
    agent = create_agent(
        model="google_genai:gemini-3.5-flash-lite",
    )
    messages = [system_msg, human_msg]
    result = agent.invoke({"messages": messages})
    section_content = result["messages"][-1].content
    if isinstance(section_content, list):
        section_content = "\n".join(
            block.get("text", "") if isinstance(block, dict) else str(block)
            for block in section_content
        )
    return {"sections": [section_content]}