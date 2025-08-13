import requests
import streamlit as st
import os

# Use Streamlit secrets if available, otherwise fallback to .env
try:
    dify_api_key = st.secrets["DIFY_API_KEY"]
except:
    from dotenv import load_dotenv
    load_dotenv()
    dify_api_key = os.getenv("DIFY_API_KEY")

url = "https://api.dify.ai/v1/chat-messages"

st.title("Dify Streamlit Demo")

# Initialize session state
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input from user
prompt = st.chat_input("Enter your question")
if prompt:
    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Prepare assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        headers = {
            "Authorization": f"Bearer {dify_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "inputs": {},
            "query": prompt,
            "response_mode": "blocking",
            "conversation_is": st.session_state.conversation_id,
            "conversation_id": st.session_state.conversation_id,
            "user": "aianytime",
            "files": []
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            response_data = response.json()
            full_response = response_data.get("answer", "")
            new_conversation_id = response_data.get("conversation_id", st.session_state.conversation_id)
            st.session_state.conversation_id = new_conversation_id
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
            full_response = "An error occurred"

        # Show assistant response
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
