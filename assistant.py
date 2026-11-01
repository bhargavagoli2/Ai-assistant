#standard lib
import json 
import os
#third-party lib
from openai import OpenAI
from dotenv import load_dotenv
#local_modules
from tools import tools, run_tool
from Utilities.utilities import log

load_dotenv()

#creating client connection
client = OpenAI(
    base_url = os.getenv("URL"),
    api_key = os.getenv("API_KEY")
)

messages = [
    {
        "role": "system",
        "content": (
            "You are a helpful assistant with access to tools.\n\n"

            "TOOL RULES:\n"
            "1. Use a tool ONLY when the user's request needs real data you cannot know: "
            "current time, weather, or the user's city. For greetings, opinions, or general "
            "chat, reply directly and DO NOT call any tool.\n"
            "2. Never invent or guess time, weather, or location. If such data is needed, "
            "you MUST get it from a tool.\n"
            "3. Only call tools that exist. Never make up a tool name.\n\n"

            "CHAINED TOOL CALLS (when one tool depends on another):\n"
            "4. If answering needs several tools in order (e.g. find the user's city, THEN "
            "get that city's weather), first think step by step about which tools to call "
            "and in what order.\n"
            "5. Then execute ONE tool at a time. Wait for each tool's result before deciding "
            "the next tool. Use the real result of an earlier tool as the input to the next.\n"
            "6. Stop calling tools as soon as you have enough information to answer.\n\n"

            "ANSWERING:\n"
            "7. When tool results are available, state the answer directly from those results.\n"
            "8. Be brief. Keep the final reply under 20 words. No follow-up questions."
        )
    }
]


log(f"{os.getenv("MODEL")}")
while True :
    prompt = input("❤️  you : ")

    if prompt.lower() in ("exit", "bye") :
        print("llm response ended")
        break
    
    messages.append(
        {
            "role" : "user",
            "content" : prompt
        }
    )
    MAX_STEPS = 5 
    for step in range(MAX_STEPS) : # Agent <-> LLM

        response = client.chat.completions.create(
            model = os.getenv("MODEL"),
            messages = messages, 
            tools = tools
        )

        reply = response.choices[0].message

        if not reply.tool_calls : break

        messages.append(reply)

        log(f" step {step + 1} : model requested {len(reply.tool_calls)} tool calls")

        for call in reply.tool_calls :
            result = run_tool(call)
    
            messages.append(
                {
                    "role" : "tool",
                    "tool_call_id" : call.id,
                    "content" : result
                }
            )
    else :
        fallback = "Sorry, I could not finish this within the step limit."
        messages.append({
            "role": "assistant", "content": fallback
        })
        print("👽 LLM response : "+ fallback)
        continue
    
    messages.append(
        {
            "role" : reply.role,
            "content" : reply.content
        }
    )          

    print("👽 LLM response : ", reply.content or "")


rdt = response.model_dump()

print(json.dumps(rdt, indent = 4))