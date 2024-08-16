import streamlit as st
import google.generativeai as genai
import os

# Set your API key (make sure it's stored securely in environment variables)
API_KEY = os.getenv('API_KEY')
MODEL_NAME = "gemini-1.5-pro-latest"

# Initialize Generative AI Client
genai.configure(api_key=API_KEY)

# Set up Streamlit session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Function to send message to AI and get response
def send_message(user_input):
    generation_config = {
        "temperature": 0.7,
        "top_k": 50,
        "top_p": 0.9,
        "max_output_tokens": 1000,
    }
    
    safety_settings = [
        {
            "category": genai.HarmCategory.HARM_CATEGORY_HARASSMENT,
            "threshold": genai.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        },
    ]
    
    # Load chat history
    history = st.session_state['chat_history']
    
    # Get AI response
    model = genai.get_model(MODEL_NAME)
    chat = model.start_chat(
        generation_config=generation_config,
        safety_settings=safety_settings,
        history=history
    )
    
    response = chat.send_message(user_input)
    if response and response.text:
        st.session_state['chat_history'].append({"role": "user", "text": user_input})
        st.session_state['chat_history'].append({"role": "bot", "text": response.text})
        return response.text
    else:
        return "Sorry, I didn't understand that."

# Streamlit UI Setup
st.title("EmoSculpt - Your AI-powered Emotional Gym")
st.write("Chat with your AI emotional trainer below:")

# Display chat history
for msg in st.session_state['chat_history']:
    if msg['role'] == 'user':
        st.markdown(f"<div style='text-align: right; color: #000000; background-color: #e0e0e0; padding: 10px; border-radius: 10px; margin-bottom: 10px;'>{msg['text']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align: left; color: #ffffff; background-color: #444444; padding: 10px; border-radius: 10px; margin-bottom: 10px;'>{msg['text']}</div>", unsafe_allow_html=True)

# User input
user_input = st.text_area("Type your message:", key="user_input", height=40)
if st.button("Send"):
    if user_input.strip():
        response = send_message(user_input.strip())
        st.experimental_rerun()

# Initial welcome message
if len(st.session_state['chat_history']) == 0:
    welcome_message = "Hello! I'm EmoSculpt, your personal trainer for emotional strength. I'm based on the groundbreaking research of neuroscientist Richard J. Davidson, as detailed in his book *The Emotional Life of Your Brain*."
    st.session_state['chat_history'].append({"role": "bot", "text": welcome_message})
    st.experimental_rerun()
