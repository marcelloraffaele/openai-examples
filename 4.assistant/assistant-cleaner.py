import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv(
    dotenv_path=".env",
    override=True
)

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
  api_key= os.getenv("AZURE_OPENAI_API_KEY"),
  api_version="2024-05-01-preview"
)

# Delete all assistants and files
file_list = client.files.list(purpose=['assistants', 'assistant_outputs'])
#print(file_list)
for file in file_list:  
    deleted = client.files.delete(file.id)
    print("file deleted: " + file.id + " " + str(deleted))

# Delete all assistants
assistant_list = client.beta.assistants.list()
for assistant in assistant_list:  
    deleted = client.beta.assistants.delete(assistant.id)
    print("assistant deleted: " + assistant.id + " " + str(deleted))