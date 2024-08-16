import streamlit as st
import os
import google.generativeai as genai

# Configure the API key for Google Generative AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize chat session settings
generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 50,
    "max_output_tokens": 1000,
}

# Create a Generative Model instance
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

# Function to handle sending messages
def send_message(user_input, history):
    chat_session = model.start_chat(history=history)
    response = chat_session.send_message(user_input)
    return response.text

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state['chat_history'] = []

# Chat UI
st.title("EmoSculpt - Your AI-powered Emotional Gym")

# Display chat history
for chat in st.session_state['chat_history']:
    if chat['role'] == 'user':
        st.text_area(label="You", value=chat['text'], height=50, key=f"user_{chat['text']}")
    else:
        st.text_area(label="EmoSculpt", value=chat['text'], height=50, key=f"bot_{chat['text']}")

# User input
user_input = st.text_area("Type your message:", key="user_input", height=50)

if st.button("Send"):
    if user_input.strip():
        st.session_state['chat_history'].append({"role": "user", "text": user_input.strip()})
        response = send_message(user_input.strip(), st.session_state['chat_history'])
        st.session_state['chat_history'].append({"role": "bot", "text": response})

# Display initial welcome message
if len(st.session_state['chat_history']) == 0:
    welcome_message = (
        "Hello! I'm EmoSculpt, your personal trainer for emotional strength. "
        "I'm based on the groundbreaking research of neuroscientist Richard J. Davidson, "
        "as detailed in his book *The Emotional Life of Your Brain*."
    )
    st.session_state['chat_history'].append({"role": "bot", "text": welcome_message})
