from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
import dotenv
from langgraph.checkpoint.memory import InMemorySaver

dotenv.load_dotenv()
llm = ChatOpenAI(
    model="gpt-4o-mini"
)
tavily_search_tool = TavilySearch(max_results=5)  # 返回的搜索结果的最大数量
tools = [tavily_search_tool]
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="你是一个智能助手，能够选择合适的工具帮助用户解决问题"
)

res = agent.invoke({"key1": "你是谁"})
print(res)
