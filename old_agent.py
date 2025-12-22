import os, getpass
from dotenv import load_dotenv
from google import genai
from langchain.agents import create_agent
from supabase import create_client, Client
from supabase_services import get_user_progress

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

def _set_env(var: str):
  if not os.environ.get(var):
    os.environ[var] = getpass.getpass(f"{var}: ")

_set_env("OPENAI_API_KEY")
_set_env("LANGSMITH_API_KEY")
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = "langchain-academy"

if not api_key:
    raise ValueError("No API key found. Please set GEMINI_API_KEY in your .env file")

client = genai.Client(api_key=api_key)
supa_client: Client = create_client(supabase_url, supabase_key)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain recent discoveries show discrepancies in the rate of expansion of the universe"
)

print(response.text)

def get_weather(city: str) -> str:
    """Get weather for a given city"""
    return f"it's always sunny in {city}!"

agent = create_agent(
    model="openai:gpt-5-mini",
    tools=[get_weather],
    system_prompt="You are a helpful assistant at meteorology research center. Your job is to provide extensive details about the weather in a given city",
)
# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "What is the weather in San Francisco?"}]}
)


get_user_progress(8)