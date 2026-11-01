import requests
import json

from datetime import datetime

from Utilities.utilities import log


#run tool fucntion
def run_tool(call) :
    name = call.function.name
    arguments = call.function.arguments

    if name in available_tools :
        func = available_tools[name]
        try :
            args = json.loads(arguments) if arguments else {}
            log(f" 🔧 {name}: {arguments}")
            result = func(**args)
        except Exception as e :
            result = f"Error running {name} : {e}"
            print(result)
    else :
        result = "Unknown tool"
    
    log(f"  👉 returns : {result}")

    return result

#tools method
def get_current_time() :
    """Return the current date and time"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_city_weather(city) :
    """Return the weather condition of city"""
    url = f"https://wttr.in/{city}?format=3"
    response = requests.get(url, timeout=10)
    return response.text

def get_current_city():
    """Return the user current city or home"""
    return "Bangalore"

#TOOLS
tools = [
    {
        "type" : "function",
        "function" :
        {
            "name" : "get_current_time",
            "description" : "Get the current date and time",
            "parameters" :
            {
                "type" : "object",
                "properties" : {},
                "required" : []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_city",
            "description": "Returns the city of the user, use this when user specifies current location, or current city or home",
            "parameters" : {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type" : "function",
        "function" : 
        {
            "name" : "get_city_weather",
            "description" : "Get the weather info about a city",
            "parameters" : 
            {
                "type" : "object",
                "properties" : 
                {
                    "city" : 
                    {
                        "type" : "string",
                        "description" : "The city name"
                    },
                },
                "required" : ["city"]
            }
        }   
    },
]

available_tools = {
    "get_current_time": get_current_time,
    "get_city_weather": get_city_weather,
    "get_current_city": get_current_city
}

