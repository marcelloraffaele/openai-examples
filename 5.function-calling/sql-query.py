import os
import json
from openai import AzureOpenAI
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

load_dotenv(
    dotenv_path=".env",
    override=True
)

# Initialize the Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-05-01-preview"
)

deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")

def database_query(sql_query):
    """Get the data from a SQL database based on the query."""
    print(f"sql_query= {sql_query}")  
    # Simulate a SQL query response
    # return a list of cars with field id, make, model, year
    return json.dumps([ "corolla", "civic", "accord" ])

def run_conversation():
    messages = [{"role": "user", "content": "Get the list of the car model sold last year?"}] # Parallel function call with a single tool/function defined

    # Define the function for the model
    tools = [
        {
            "type": "function",
            "function": {
                "name": "database_query",
                "description": "Get the data from a SQL database based on the query. There are available only two tables: cars(id,make,model,year) and user(id, name, surname, age ).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "sql_query": {
                            "type": "string",
                            "description": "The select query to run on the SQL database. E.g., 'SELECT * FROM cars WHERE year=2021'",
                        },
                    },
                    "required": ["sql_query"],
                },
            }
        }
    ]

    # First API call: Ask the model to use the function
    response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    # Process the model's response
    response_message = response.choices[0].message
    messages.append(response_message)

    print("Model's response:")  
    print(response_message)  

    # Handle function calls
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            if tool_call.function.name == "database_query":
                function_args = json.loads(tool_call.function.arguments)
                print(f"Function arguments: {function_args}")  

                query_response = database_query(
                    sql_query=function_args.get("sql_query")
                )
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": "database_query",
                    "content": query_response,
                })
    else:
        print("No tool calls were made by the model.")  


    # Second API call: Get the final response from the model
    final_response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
    )

    return final_response.choices[0].message.content

# Run the conversation and print the result
print(run_conversation())