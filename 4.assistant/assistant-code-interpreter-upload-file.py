import os
import json
import requests
import time
from IPython.display import clear_output
from openai import AzureOpenAI
from dotenv import load_dotenv
from PIL import Image

load_dotenv(
    dotenv_path=".env",
    override=True
)

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
  api_key= os.getenv("AZURE_OPENAI_API_KEY"),
  api_version="2024-05-01-preview"
)

file = client.files.create(
  file=open("example.txt", "rb"),
  purpose='assistants'
)
print("file created: " + file.id)
fileId = file.id

#fileId = "assistant-52PAaXidCh4q1iBFIGOJOALE"

# Create an assistant using the file ID
assistant = client.beta.assistants.create(
  model="gpt-4o", # replace with model deployment name.
  instructions="You are and AI assistant that help answer questions.",
  tools=[{"type":"code_interpreter"}],
  tool_resources={"code_interpreter":{"file_ids":[fileId]}},
  temperature=1,
  top_p=1
)

#assistant = client.beta.assistants.retrieve("asst_FHiGbq9QASyvMiiEzy4Ef4ls")

print("assistant: " + assistant.id)

thread = client.beta.threads.create();
messages=client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content="I need to plot a graph of the age of people in the file. Tell me also information about oldest and youngest person. On X axis I want to have the name people, on y axis the age.",
)

print("thread created: " + thread.id)

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
  #instructions="New instructions" #You can optionally provide new instructions but these will override the default instructions
)


start_time = time.time()
status = run.status
while status not in ["completed", "cancelled", "expired", "failed"]:
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

data = json.loads(messages.model_dump_json(indent=2))  # Load JSON data into a Python object
image_file_id = data['data'][0]['content'][0]['image_file']['file_id']
print(image_file_id)
text = data['data'][0]['content'][1]['text']['value']
print(text)

# Download the image file
content = client.files.content(image_file_id)
image= content.write_to_file("example.png")


# Display the image in the default image viewer
image = Image.open("example.png")
image.show()