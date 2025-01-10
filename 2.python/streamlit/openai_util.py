import os
from openai import AzureOpenAI
from dotenv import load_dotenv

def completion(messageList):
    print("In completion: " + str(messageList))
    load_dotenv()

    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")  
    deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")  
    api_key = os.getenv("AZURE_OPENAI_API_KEY")  
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")

    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version= api_version)
    
    response = client.chat.completions.create(
        model=deployment,
        messages=messageList,
        #max_tokens=100,
        temperature=0.0,
        
    )
        #print(response.to_json())
        #print(response.choices[0].message.to_json())
    #    print("\n\n" + response.choices[0].message.role + " /> " + response.choices[0].message.content)
    return response.choices[0].message.content