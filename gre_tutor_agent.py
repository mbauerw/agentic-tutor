import os, getpass
from dotenv import load_dotenv
from google import genai
from langchain.agents import create_agent
from supabase import create_client, Client
from supabase_services import get_user_progress
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
from IPython.display import Image, display
from langgraph.graph import START, StateGraph
from langgraph.checkpoint.memory import MemorySaver

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

tools = [get_user_progress]
llm = ChatOpenAI(model="gpt-4o")

llm_with_tools = llm.bind_tools(tools,parallel_tool_calls=False)

sys_msg = SystemMessage("You are a helpful GRE tutor. Your job is to analyze user progress from the user_progress table and give a brief summary of the user's performance based on their accuracy and percentage complete. Give advice on what subjects they should focus their study." )

def tutor(state: MessagesState): 
   return {'messages': [llm_with_tools.invoke([sys_msg] + state['messages'])]}

builder = StateGraph(MessagesState)

builder.add_node("tutor", tutor)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "tutor")
builder.add_conditional_edges("tutor", tools_condition)
builder.add_edge("tools", "tutor")

react_graph = builder.compile()

messages = [HumanMessage(content="Give a summary of user progress for userId=8")]
messages = react_graph.invoke({"messages": messages})

for m in messages['messages']:
    m.pretty_print()

