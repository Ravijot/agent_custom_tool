import requests
import os 
from dotenv import load_dotenv
from langchain.pydantic_v1 import  BaseModel, Field
from langchain.tools import StructuredTool, tool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

load_dotenv()

api_key = os.getenv('weather_api_key')

class Input(BaseModel):
    city: str = Field(description="Name of the city which data need to be retrieved")
    
class Tools:
    
    def __init__(self):
        self.tools = []
        self.add_tool()
        
    def get_weather(self,city):
        print("in current weather")
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"  # Optional, for temperature in Celsius
        }
        response = requests.get(base_url, params=params)
        return response.json()

    def add_tool(self):
        weather= StructuredTool.from_function(
            func=self.get_weather,
            name="Weather",
            description="Useful in getting current weather",
            args_schema=Input,
            return_direct=False,
           
        )
        self.tools.append(weather)
        
    def get_tools(self):
        return self.tools

# print(Tools().get_tools()[0])
# print(Tools().get_tools()[0].run("Delhi"))