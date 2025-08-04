import requests
import json
import google.generativeai as genai
import streamlit as st
import os 
from dotenv import load_dotenv 

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


genai.configure(api_key=GEMINI_API_KEY)

def get_gemini_response(user_message, api_key_param):
    if not api_key_param:
        return "Please enter your Gemini API Key to continue."

    current_system_prompt = ""
    # System prompt logic based on st.session_state (passed or accessed here if needed)
    if st.session_state.mentorship_mode and st.session_state.user_type == "existing_player":
        user_data = st.session_state.user_data
        current_system_prompt = f"""
        You are the exclusive CAREER DEVELOPMENT & MENTORSHIP AGENT for QUCOON FOOTBALL ACADEMY.
        # ... (rest of your existing system prompt for existing_player) ...
        PLAYER PROFILE - {user_data['name']}:
        - Age: {user_data['age']}
        - Position: {user_data['position']}
        - Years Played: {user_data['years_played']}
        - Level: {user_data['level']}
        - Current Club: {user_data['current_club']}
        # ... (rest of the prompt) ...
        """
    elif st.session_state.mentorship_mode and st.session_state.user_type == "existing_coach":
        user_data = st.session_state.user_data
        current_system_prompt = f"""
        You are the COACHING CAREER CONSULTANT for QUCOON FOOTBALL ACADEMY.
        # ... (rest of your existing system prompt for existing_coach) ...
        COACH PROFILE - {user_data['name']}:
        - Age: {user_data['age']}
        - Specialty: {user_data['specialty']}
        - Years Experience: {user_data['years_experience']}
        - Level: {user_data['level']}
        # ... (rest of the prompt) ...
        """
    elif st.session_state.user_type == "new_user_selecting_pathway":
        current_system_prompt = f"""
        You are the AI Career Assistant for QUCOON FOOTBALL ACADEMY.
        # ... (rest of your existing system prompt for new_user_selecting_pathway) ...
        """
    elif st.session_state.user_type == "new_user_general_inquiry":
        current_system_prompt = f"""
        You are the AI Career Assistant for QUCOON FOOTBALL ACADEMY.
        # ... (rest of your existing system prompt for new_user_general_inquiry) ...
        """
    else: # user_type is None (initial state)
        current_system_prompt = f"""
        You are the AI Career Assistant for QUCOON FOOTBALL ACADEMY.
        # ... (rest of your existing system prompt for initial state) ...
        """

    # Build chat history for Gemini
    chat_history = [{"role": "user", "parts": [{"text": current_system_prompt}]}]

    for msg in st.session_state.messages:
        gemini_role = "user" if msg["role"] == "user" else "model"
        chat_history.append({"role": gemini_role, "parts": [{"text": msg["content"]}]})

    chat_history.append({"role": "user", "parts": [{"text": user_message}]})

    generation_config = {
        "temperature": 0.3
    }

    payload = {
        "contents": chat_history,
        "generationConfig": generation_config
    }

    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}" # Use the globally loaded key here

    try:
        response = requests.post(api_url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()

        if result.get("candidates") and len(result["candidates"]) > 0:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            error_message = result.get("error", {}).get("message", "Unknown API error.")
            return f"Sorry, couldn't process. API error: {error_message}"
    except requests.exceptions.RequestException as e:
        return f"API error: {e}. Check internet/key. Full response: {response.text if 'response' in locals() else 'N/A'}"
    except json.JSONDecodeError:
        return f"Unreadable API response. Full response: {response.text if 'response' in locals() else 'N/A'}"
    except Exception as e:
        return f"Unexpected error: {e}."