
from langchain.agents import initialize_agent, AgentType
from langchain_openai import OpenAI
from Weather_Wiki_Custom_Tool import Tools
from dotenv import load_dotenv
import os

load_dotenv()
openai_key = os.getenv("API_KEY")
os.environ["OPENAI_API_KEY"] = openai_key
prompt = """You are weather expert who answer today's weather releated queries.Answer the following questions as best you can. You have access to the following tools:
Weather : A wrapper around weather api that provides information  about only todays's weather available on the weather api service only use this tool when user asked about today's weather. This tool will give data in JSON so you can answer the query.Input should be a city name.

You are only dealing with weather related queries if any other query comes just simply respond with : 'Sorry I dont have relevnt Data"""
llm = OpenAI(temperature=0)
tools = Tools().get_tools()
agent = initialize_agent(tools, 
                         llm, 
                         agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                         prompt=prompt,
                         verbose=True)

print(agent.run("Give temperature of delhi"))
