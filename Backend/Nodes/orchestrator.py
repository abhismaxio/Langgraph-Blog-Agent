from langchain.messages import HumanMessage, AIMessage, SystemMessage
from Backend.Schema.plan import Plan
from Backend.State.state import State
from langchain.agents import create_agent

from dotenv import load_dotenv
load_dotenv()

def orchestrator(state: State)-> dict:
    system_message = SystemMessage("Create a blog plan with 5-7 sections on following topic")
    human_msg = HumanMessage(f"Topic: {state['topic']}")
    messages = [system_message, human_msg]
    agent = create_agent(
        model="google_genai:gemini-3.5-flash-lite",
        response_format=Plan,
    )
    result = agent.invoke({"messages": messages})
    plan = result["structured_response"]
    return {"plan": plan}
