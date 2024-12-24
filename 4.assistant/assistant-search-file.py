import os
import json
import requests
import time
from IPython.display import clear_output
from openai import AzureOpenAI
from dotenv import load_dotenv
from PIL import Image
from typing_extensions import override
from openai import AssistantEventHandler, OpenAI

load_dotenv(
    dotenv_path=".env",
    override=True
)

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
  api_key= os.getenv("AZURE_OPENAI_API_KEY"),
  api_version="2024-05-01-preview"
)

# Create a vector store called "Financial Statements"
##vector_store = client.beta.vector_stores.create(name="Example VS")
#vector_store = client.beta.vector_stores.retrieve(vector_store_id="vs_lIN4kczMg0sFVRN4ZjYKMwz6",timeout=30)
#print("vector_store.id: " + vector_store.id)
#
## Ready the files for upload to OpenAI
#file_paths = ["example.txt"]
#file_streams = [open(path, "rb") for path in file_paths]
# 
## Use the upload and poll SDK helper to upload the files, add them to the vector store,
## and poll the status of the file batch for completion.
#file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
#  vector_store_id=vector_store.id, files=file_streams
#)
# 
## You can print the status and the file counts of the batch to see the result of this operation.
#print(file_batch.status)
#print(file_batch.file_counts)
#
#if file_batch.status == "failed":
#    quit()

# Create an assistant using the file ID
assistant = client.beta.assistants.create(
  model="gpt-4o", # replace with model deployment name.
  instructions="You are and AI assistant that help answer questions.",
  tools=[{"type":"file_search"}],
  temperature=1,
  top_p=1
)

print("assistant: " + assistant.id)

# Upload the user provided file to OpenAI
message_file = client.files.create(
  file=open("example.txt", "rb"), purpose="assistants"
)
 
# Create a thread and attach the file to the message
thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": "Tell me also information about oldest and youngest person. And in which city there are the tallest people?",
      # Attach the new file to the message.
      "attachments": [
        { "file_id": message_file.id, "tools": [{"type": "file_search"}] }
      ],
    }
  ]
)
 
# The thread now has a vector store with that file in its tool resources.
print(thread.tool_resources.file_search)

class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print(f"\nassistant > ", end="", flush=True)

    @override
    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)

    @override
    def on_message_done(self, message) -> None:
        # print a citation to the file searched
        message_content = message.content[0].text
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(
                annotation.text, f"[{index}]"
            )
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = client.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")

        print(message_content.value)
        print("\n".join(citations))

# Then, we use the stream SDK helper
# with the EventHandler class to create the Run
# and stream the response.

with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistant.id,
    #instructions="Please address the user as Jane Doe. The user has a premium account.",
    event_handler=EventHandler(),
) as stream:
    stream.until_done()