from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import OpenAI
from Custom_Tool import Tools
from langchain_core.prompts import PromptTemplate
from langchain.agents import initialize_agent
from dotenv import load_dotenv
import os

template = '''You are weather expert who answer today's weather releated queries.Answer the following questions as best you can. You have access to the following tools:
Weather : A wrapper around weather api that provides information  about only todays's weather available on the weather api service only use this tool when user asked about today's weather. This tool will give data in JSON so you can answer the query.Input should be a city name.

You are only dealing with weather related queries if any other query comes just simply respond with : 'Sorry I dont have relevnt Data'
{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}'''

load_dotenv()
openai_key = os.getenv("API_KEY")
os.environ["OPENAI_API_KEY"] = openai_key

class Agent:
    
    def __init__(self):
        self.tools = Tools().get_tools()
        self.llm = OpenAI(temperature=0.4)
        self.prompt = PromptTemplate.from_template(template)
        self.agent = create_react_agent(self.llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(agent=self.agent, 
                                            tools=self.tools,
                                            verbose=True,
                                            return_intermediate_steps=True,
                                            )

    
#print(Agent().tools)
print(Agent().agent_executor.invoke({"input": "What is minimum temperature of Delhi?"}))