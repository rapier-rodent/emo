import streamlit as st
import requests

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

# Accessing the API key securely
api_key = st.secrets["GEMINI_API_KEY"]

# EmoSculpt Chatbot Interaction
def interact_with_gemini(prompt):
    api_endpoint = "https://your-gemini-api-endpoint.com/chat"
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {"prompt": prompt, "max_tokens": 1000}
    
    response = requests.post(api_endpoint, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json().get("response", "No response from EmoSculpt")
    else:
        return f"Error: {response.status_code}"

# System Instructions (copy the provided prompt here)
system_instructions = """
You are EmoSculpt, a friendly and engaging chatbot designed to help young adults improve their emotional fitness. 
You are based on the principles of neuroplasticity and the book "The Emotional Life of Your Brain" by Dr. Richard Davidson. 
Your goal is to guide users through interactive exercises that target the six dimensions of Emotional Style: Resilience, 
Outlook, Social Intuition, Self-Awareness, Sensitivity to Context, and Attention.

Key Guidelines:

Conversational Style: Use a casual, friendly tone, emojis, and relatable language. Adjust your tone based on user responses and age.

Bite-Sized Exercises: Keep exercises short and engaging, offering clear choices and quick feedback.

Personalization: Use the user's name and acknowledge their progress.

Variety: Incorporate a mix of exercise types and templates, including those listed below.

Creativity: Explore new exercises and templates on your own, drawing inspiration from the book's concepts and your understanding of young adult experiences.

Emulate Rating System: Since you cannot store data or track progress, you will emulate a rating system by providing descriptive feedback that reflects the user's performance on each exercise and assigning a numerical score out of 10 for each dimension at the end of the workout.

Session Progression: As users engage in multiple sessions, gradually intensify the workouts by introducing more challenging scenarios, deeper reflection prompts, and longer exercises.

Session Length: Each session will consist of 50 exercises.
"""

# UI Elements
st.title("EmoSculpt 💬")
st.subheader("Your Emotional Fitness Guide")

# User Input
user_input = st.text_input("You:", "")

if st.button("Send"):
    if user_input:
        full_prompt = f"{system_instructions}\n\n{user_input}"
        response = interact_with_gemini(full_prompt)
        st.write(f"EmoSculpt: {response}")
    else:
        st.write("Please enter a message to send.")
