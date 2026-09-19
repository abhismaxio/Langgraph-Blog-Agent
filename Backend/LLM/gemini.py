from langchain.agents import create_agent

from dotenv import load_dotenv
load_dotenv()

agent = create_agent(
    model="google_genai:gemini-3.5-flash-lite"
)