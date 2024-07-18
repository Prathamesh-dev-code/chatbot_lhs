import os
from datetime import datetime  # Import datetime module for timestamp handling

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with LHS!",
    layout="wide",  # Set layout to wide for a side panel
)

# Function to translate user role for chat display
def translate_role_for_streamlit(user_role):
    if user_role == "user":
        return "User"
    else:
        return "Assistant"

# Function to replace "Gemini" or "Google" with "Lighthouse" and "LHS" in responses
def replace_lighthouse_terms(response):
    response = response.replace("Gemini", "LHS-BOT")
    response = response.replace("Google", "Lighthouse Info Systems Pvt. Ltd.")
    return response

# Set up Google Gemini-Pro AI model
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Predefined questions and answers
predefined_data = {
    "who are you": "I am Lighthouse Info Systems Pvt. Ltd., a leading provider of ERP solutions for various industries. A multimodal AI model developed by LHS.",
    # Add more predefined questions and answers as needed
}

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input field for user's message
user_prompt = st.text_input("Ask LightHouse...")

if st.button("Send"):
    if user_prompt:
        # Store user's message in chat history
        st.session_state.chat_history.append({
            "role": "user",
            "text": user_prompt
        })

        # Check if the user's message is a predefined question
        if user_prompt.lower() in predefined_data:
            # Display predefined answer
            predefined_answer = replace_lighthouse_terms(predefined_data[user_prompt.lower()])
            st.session_state.chat_history.append({
                "role": "assistant",
                "text": predefined_answer
            })
        else:
            # Send user's message to Gemini-Pro and get the response
            gemini_response = st.session_state.chat_session.send_message(user_prompt)
            gemini_answer = replace_lighthouse_terms(gemini_response.text)
            
            # Display Gemini-Pro's response
            st.session_state.chat_history.append({
                "role": "assistant",
                "text": gemini_answer
            })

# Main chat interaction
st.header("LightHouse - ChatBot")
for message in st.session_state.chat_history[-10:]:  # Display last 10 messages
    if message["role"] == "user":
        st.text_area("User", value=message["text"], height=100, max_chars=None, key=None)
    else:
        st.text_area("Assistant", value=message["text"], height=100, max_chars=None, key=None)

# Side panel for chat history
st.sidebar.header("Chat History")
for message in st.session_state.chat_history:
    st.sidebar.text_area(message["role"], value=message["text"], height=100, max_chars=None, key=None)
