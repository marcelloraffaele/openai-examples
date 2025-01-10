import streamlit as st
import openai_util as myopenai

def send_message(prompt):
    print("System message:", st.session_state.systemMessage, ", User input:", prompt)
    st.session_state.chatMessages.append({"role": "user", "content": prompt})
    response = call(st.session_state.systemMessage, st.session_state.chatMessages)
    st.session_state.chatMessages.append({"role": "ai", "content": response})

    for message in st.session_state.chatMessages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def call(sm, cm):
    messageList = []
    messageList.append({"role": "system", "content": sm})
    for m in cm:
        messageList.append(m)
    res = myopenai.completion(messageList)
    return res

# Set up the Streamlit app
st.title("AI Chat")

# Initialize session state for messages
if "systemMessage" not in st.session_state:
    st.session_state.systemMessage = "You are a helpful assistant"

if "chatMessages" not in st.session_state:
    st.session_state.chatMessages = []

st.text_area("System message", value=st.session_state.systemMessage, key="systemMessage")

if prompt := st.chat_input():
    send_message(prompt)