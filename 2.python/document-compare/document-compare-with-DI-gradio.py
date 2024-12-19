#pip install azure-ai-documentintelligence
import os
from openai import AzureOpenAI
from dotenv import load_dotenv
import gradio as gr

def main():
    load_dotenv()

    defaultSystemMessage = "Sei un agente che aiuta a fare un analisi comparativa di documenti in ambito legale. Elenca gli articoli che sono stati modificati e aggiungi dettagli. Se i due file non hanno niente in comure, rispondi che non è possibile completare il lavoro."
    defaultUserMessage = "compara questi due documenti: $FILENAME1= ---$FILE1--- $FILENAME2= ---$FILE2---"

    demo = gr.Interface(
        fn=compare,
        inputs=[
            gr.File(label="First file"),
            gr.File(label="Second file"),
            gr.Textbox(label="System message", value=defaultSystemMessage),
            gr.Textbox(label="User Message", value=defaultUserMessage)
        ],
        outputs=[ gr.Markdown() ],
        title="Compare Two files",
        description="This app compares two files and returns the differences between them. The files can be in any format."
    )

    demo.launch()


def compare(file1_path, file2_path, systemMessage, userMessage):
    
    if not file1_path or not file2_path:
        return "One or both file paths are empty. Please provide valid file paths."

    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")  
    deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")  
    api_key = os.getenv("AZURE_OPENAI_API_KEY")  
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")

    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version= api_version)
    
    # Example usage
    file1_name = os.path.basename(file1_path)
    file2_name = os.path.basename(file2_path)
    
    text1 = parse(file1_path)    
    text2 = parse(file2_path)
    userMessage = userMessage.replace("$FILENAME1", file1_name)
    userMessage = userMessage.replace("$FILENAME2", file2_name)
    userMessage = userMessage.replace("$FILE1", text1)
    userMessage = userMessage.replace("$FILE2", text2)

    messageList = [
        {"role": "system", "content": systemMessage},
        {"role": "user", "content": userMessage},
    ]

    response = client.chat.completions.create(
        model=deployment,
        messages=messageList,
        temperature=0.0,
        )
    
    return response.choices[0].message.content

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