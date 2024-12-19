# Description: This script compares two PDF files and extracts the differences between them using Azure OpenAI Chat API.
# It uses the PyPDF2 library to extract text from PDF files and the Azure OpenAI Chat API to compare the text and provide the differences.
#pip install PyPDF2
import os
from openai import AzureOpenAI
from dotenv import load_dotenv
import PyPDF2

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
    
    pdf1_path = '..\..\data\codice-civile-262_1942.pdf'
    pdf2_path = '..\..\data\codice-civile-262_1942-2024.pdf'
    
    text1 = extract_text_from_pdf(pdf1_path)
    text2 = extract_text_from_pdf(pdf2_path)

    #continueMessage = "Press Enter to continue or type 'exit' to quit: "
    continueMessage = "\nPremi Invio per continuare o digita 'exit' per uscire: "

    messageList = [
        {"role": "system", "content": "Sei un agente che aiuta a fare un analisi comparativa di documenti in ambito legale. Elenca gli articoli che sono stati modificati e aggiungi dettagli."},
        {"role": "user", "content": "compara questi due documenti: doc1= ---" + text1 + "--- doc2= ---" + text2 + "---"},
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

        user_question = input( continueMessage )
        if user_question.lower() == 'exit':
            break
        # add user question to the message list
        messageList.append({"role": "user", "content": user_question})


def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    return text

if __name__ == "__main__":
    main()