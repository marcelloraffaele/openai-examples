#pip install azure-ai-documentintelligence
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

def main():
    load_dotenv()

    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")  
    deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")  
    api_key = os.getenv("AZURE_OPENAI_API_KEY")  
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")

    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version= api_version)
    
    # Example usage
    file1_path = 'C:\\Workspaces\\Code\\openai-examples\\data\\codice-civile-262_1942.pdf'
    file2_path = 'C:\\Workspaces\\Code\\openai-examples\\data\\codice-civile-262_1942-2024.pdf'
    file1_name = os.path.basename(file1_path)    
    file2_name = os.path.basename(file2_path)
    
    text1 = parse(file1_path)
#    print(text1)
    text2 = parse(file2_path)

    #continueMessage = "Press Enter to continue or type 'exit' to quit: "
    continueMessage = "\nPremi Invio per continuare o digita 'exit' per uscire: "

    messageList = [
        {"role": "system", "content": "Sei un agente che aiuta a fare un analisi comparativa di documenti in ambito legale. Elenca gli articoli che sono stati modificati e aggiungi dettagli."},
        {"role": "user", "content": "compara questi due documenti: " + file1_name + "= ---" + text1 + "--- " + file2_name + "= ---" + text2 + "---"},
    ]

    while True:
        response = client.chat.completions.create(
            model=deployment,
            messages=messageList,
            #max_tokens=100,
            temperature=0.0,
            
        )
        #print(response.to_json())
        #print(response.choices[0].message.to_json())
        print("\n\n" + response.choices[0].message.role + " /> " + response.choices[0].message.content)
        messageList.append({"role": response.choices[0].message.role, "content": response.choices[0].message.content})

        user_question = input( continueMessage )
        if user_question.lower() == 'exit':
            break
        # add user question to the message list
        messageList.append({"role": "user", "content": user_question})


def parse(file_path):
    
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    from azure.ai.documentintelligence.models import DocumentAnalysisFeature, AnalyzeResult, AnalyzeDocumentRequest

    # For how to obtain the endpoint and key, please see PREREQUISITES above.
    endpoint = os.environ["DOCUMENTINTELLIGENCE_ENDPOINT"]
    key = os.environ["DOCUMENTINTELLIGENCE_API_KEY"]

    document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    with open(file_path, "rb") as f:
        file_content = f.read()
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-read",
            body=file_content,
            features=[DocumentAnalysisFeature.LANGUAGES],
            content_type="application/octet-stream",
        )
    result: AnalyzeResult = poller.result()

    # trasform result in a string json
    result_json = result.content

    return result_json

if __name__ == "__main__":
    main()