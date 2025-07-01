import streamlit as st
import requests
import json
from config import GEMINI_API_KEY

#  Streamlit Page Configuration 
st.set_page_config(
    page_title="Football Career Assistant",
    page_icon="⚽",
    layout="centered"
)

# Initialize Session State 
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Title 
st.title("⚽ Football Career Assistant")
st.markdown("Chat with me about becoming a professional footballer or coach!")

#  API Key (Hidden from user) 
api_key = GEMINI_API_KEY

# Function to call Gemini API 
def get_gemini_response(user_message, api_key_param):
    if not api_key_param:
        return "Please enter your Gemini API Key to continue."

    # Build conversation history
    chat_history = []
    
    # Add system prompt
    system_prompt = f"""
    You are an expert football career advisor specializing in both player and coaching development. Your role is to guide users through their football career journey with deep expertise.

    CONVERSATION FLOW:
    1. First, ask if they aspire to be a professional footballer or professional coach
    2. For PLAYERS: Ask about their preferred position (GK, CB, FB, CM, CAM, Winger, Striker, etc.)
    3. For COACHES: Ask about their coaching style/philosophy (attacking, possession-based, counter-attacking, youth development, etc.)
    4. Then provide detailed career guidance with historical references

    EXPERTISE AREAS:
    - Detailed player position analysis and development paths
    - Coaching philosophies and management styles
    - Career progression roadmaps from amateur to professional
    - Training methods, skills development, and preparation
    - Mental and physical requirements for each role
    - Industry insights and current opportunities

    ALWAYS INCLUDE:
    - Reference 2-3 legendary players or coaches who excelled in similar roles
    - Explain their playing/coaching style and what made them successful
    - Provide specific development steps and training recommendations
    - Discuss challenges and how to overcome them
    - Give practical next steps they can take immediately

    Keep responses detailed but conversational, encouraging, and full of real football knowledge and examples.
    
    Current conversation:
    """
    
    # Add recent messages for context
    conversation = ""
    for msg in st.session_state.messages[-5:]:  # Last 5 messages for context
        role = "User" if msg["role"] == "user" else "Assistant"
        conversation += f"{role}: {msg['content']}\n"
    
    conversation += f"User: {user_message}"
    
    full_prompt = system_prompt + conversation
    
    chat_history.append({"role": "user", "parts": [{"text": full_prompt}]})
    payload = {"contents": chat_history}
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key_param}"

    try:
        response = requests.post(api_url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()

        if result.get("candidates") and len(result["candidates"]) > 0:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "Sorry, I couldn't process that. Please try again."
    except:
        return "Sorry, there was an error. Please try again."

# Chat Interface 
# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me about your football career..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get and display AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_gemini_response(prompt, api_key)
            st.markdown(response)
            
    # Add AI response to history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Clear Chat Button 
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()