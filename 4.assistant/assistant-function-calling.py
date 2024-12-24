import os
import json
import requests
import time
from IPython.display import clear_output
from openai import AzureOpenAI
from dotenv import load_dotenv
from PIL import Image

# Example function
def get_weather(  location: str) -> str:
    print(f"Getting weather for {location}...")
    return "It's 80 degrees F and slightly cloudy."

load_dotenv(
    dotenv_path=".env",
    override=True
)

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
  api_key= os.getenv("AZURE_OPENAI_API_KEY"),
  api_version="2024-05-01-preview"
)

assistant = client.beta.assistants.create(
  name="Weather Bot",
  instructions="You are a weather bot. Use the provided functions to answer questions.",
  model="gpt-4o", #Replace with model deployment name
  tools=[{
      "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the weather in location",
            "parameters": {
                "type": "object",
                "properties": {
                "location": {"type": "string", "description": "The city name, for example San Francisco"}
                },
                "required": ["location"]
            }
        }
    }]
)

#assistant = client.beta.assistants.retrieve("asst_PmLU6elp1zNzkIUPyJ94XDco")

print("assistant: " + assistant.id)

thread = client.beta.threads.create()
messages=client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content="Hi, i live in Rome, can you tell me the weather?",
)

print("thread created: " + thread.id)

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
  #instructions="New instructions" #You can optionally provide new instructions but these will override the default instructions
)

start_time = time.time()
status = run.status
while status not in ["completed", "requires_action", "cancelled", "expired", "failed"]:
    time.sleep(5)
    run = client.beta.threads.runs.retrieve(thread_id=thread.id,run_id=run.id)
    print("Elapsed time: {} minutes {} seconds".format(int((time.time() - start_time) // 60), int((time.time() - start_time) % 60)))
    status = run.status
    print(f'Status: {status}')
    clear_output(wait=True)
messages = client.beta.threads.messages.list(
  thread_id=thread.id
)
print(f'Status: {status}')
print(run.model_dump_json(indent=2))
print("Elapsed time: {} minutes {} seconds".format(int((time.time() - start_time) // 60), int((time.time() - start_time) % 60)))


messages = client.beta.threads.messages.list(
  thread_id=thread.id
)
print(messages.model_dump_json(indent=2))


# Define the list to store tool outputs
tool_outputs = []
 
# Loop through each tool in the required action section
for tool in run.required_action.submit_tool_outputs.tool_calls:
  # get data from the weather function
  if tool.function.name == "get_weather":
    arguments = json.loads(tool.function.arguments)
    location = arguments["location"]
    weather = get_weather(location)
    tool_outputs.append({
      "tool_call_id": tool.id,
      "output": weather
    })
 
# Submit all tool outputs at once after collecting them in a list
if tool_outputs:
  try:
    run = client.beta.threads.runs.submit_tool_outputs_and_poll(
      thread_id=thread.id,
      run_id=run.id,
      tool_outputs=tool_outputs
    )
    print("Tool outputs submitted successfully.")
  except Exception as e:
    print("Failed to submit tool outputs:", e)
else:
  print("No tool outputs to submit.")


status = run.status
while status not in ["completed", "requires_action", "cancelled", "expired", "failed"]:
    time.sleep(5)
    run = client.beta.threads.runs.retrieve(thread_id=thread.id,run_id=run.id)
    print("Elapsed time: {} minutes {} seconds".format(int((time.time() - start_time) // 60), int((time.time() - start_time) % 60)))
    status = run.status

if run.status == 'completed':
    print("run status: ", run.status)
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    print(messages.to_json(indent=2))
    data = json.loads(messages.model_dump_json(indent=2))  # Load JSON data into a Python object
    text = data['data'][0]['content'][0]['text']['value']
    print(text)

else:
    print("run status: ", run.status)
    print (run.last_error.message)