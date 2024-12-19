[models](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models?tabs=python-secure#model-summary-table-and-region-availability/?azure-portal=true)
[Cost model]( https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/)

## Phi-3
[phi3](https://azure.microsoft.com/en-us/blog/introducing-phi-3-redefining-whats-possible-with-slms/)

## Langchain4j
[langchain4j home](https://docs.langchain4j.dev/intro)
[azure openai client] (https://docs.langchain4j.dev/integrations/language-models/azure-open-ai/)

## Rest API client ( CURL )

```bash
ENDPOINT=openai-3647585
DEPLOYMENT=gpt-35-turbo
API_KEY=xxxxxxxxx

curl https://$ENDPOINT.openai.azure.com/openai/deployments/$DEPLOYMENT/chat/completions?api-version=2023-03-15-preview \
  -H "Content-Type: application/json" \
  -H "api-key: $API_KEY" \
  -d '{"messages":[{"role": "system", "content": "You are a helpful assistant, teaching people about AI."},
{"role": "user", "content": "Does Azure OpenAI support multiple languages?"},
{"role": "assistant", "content": "Yes, Azure OpenAI supports several languages, and can translate between them."},
{"role": "user", "content": "Do other Azure AI Services support translation too?"}]}'
```

risposta:
```json
{
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": "Yes, several other Azure AI Services also support translation. Some of these services include:\n\n1. Azure Cognitive Services - Text Translation \n2. Azure Translator Text API \n3. Azure Cognitive Services - Language Understanding (LUIS) \n\nUsing these services, you can translate text, speech, and even entire documents between multiple languages.",
        "role": "assistant"
      }
    }
  ],
  "created": 1728318073,
  "id": "chatcmpl-AFkltUjZ2lkuGuyW2EL8Q7oSN8mEo",
  "model": "gpt-35-turbo",
  "object": "chat.completion",
  "system_fingerprint": null,
  "usage": {
    "completion_tokens": 65,
    "prompt_tokens": 66,
    "total_tokens": 131
  }
}
```

## Client python
[openai-python](https://github.com/openai/openai-python/tree/main)
```python
import os
from openai import AzureOpenAI

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version="2023-03-15-preview"
)
response = client.chat.completions.create(
    model="gpt-35-turbo", # replace with the model deployment name of your o1-preview, or o1-mini model
    messages=[ {"role": "user", "content": "What steps should I think about when writing my first Python API?"},

    ],
)
print(response.to_json())
```
to call:
```bash
AZURE_OPENAI_ENDPOINT=https://openai-3647585.openai.azure.com AZURE_OPENAI_API_KEY=xxxxxxx python3 client.py

```

## API Management for OpenAI

[AI-Gateway] (https://github.com/Azure-Samples/AI-Gateway)


challange
https://learn.microsoft.com/en-us/training/topics/event-challenges?wt.mc_id=aisc25_learnpromo1_website_cnl&tabs=intelligent-apps