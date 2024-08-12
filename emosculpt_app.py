import streamlit as st
import os
import google.generativeai as genai

# Set dark mode
st.set_page_config(page_title="EmoSculpt", page_icon="💬", layout="centered", initial_sidebar_state="collapsed")

# Apply dark mode to the entire app
st.markdown(
    """
    <style>
    body {
        color: #fff;
        background-color: #2c2c2c;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Configure the Google Generative AI with your API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model with specific configuration
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction="""EmoSculpt Chatbot Prompt:
    System Instructions:
    You are EmoSculpt, a friendly and engaging chatbot designed to help young adults improve their emotional fitness...
    [Include the rest of the prompt here]
    """,
)

# Function to interact with the model
def interact_with_gemini(user_input):
    chat_session = model.start_chat(
        history=[
            {
                "role": "model",
                "parts": [
                    "Hey there! 👋 I'm EmoSculpt, your personal guide to emotional fitness. I'm based on the science of neuroplasticity and the groundbreaking book 'The Emotional Life of Your Brain' by Dr. Richard Davidson.\n\nWhat's your name?\n",
                ],
            },
        ]
    )
    response = chat_session.send_message(user_input)
    return response.text

# UI Elements
st.title("EmoSculpt 💬")
st.subheader("Your Emotional Fitness Guide")

# User Input
user_input = st.text_input("You:", "")

if st.button("Send"):
    if user_input:
        response = interact_with_gemini(user_input)
        st.write(f"EmoSculpt: {response}")
    else:
        st.write("Please enter a message to send.")
