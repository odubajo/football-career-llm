import streamlit as st
import google.generativeai as genai

# Import from your new files
from config import GEMINI_API_KEY, INITIAL_APPLICATION_FORM_URL
from data_manager import get_user_data
from gemini_service import get_gemini_response
from player_agent import handle_scouting_agent
from coach_agent import handle_coach_recruitment_agent
from utils import contains_any_keyword # Only need contains_any_keyword if used outside agent functions directly

genai.configure(api_key=GEMINI_API_KEY)

# Streamlit Page Configuration
st.set_page_config(
    page_title="Football Career Assistant",
    page_icon="⚽",
    layout="centered"
)

st.image("mylogoo.png", width=250)

# Initialize Session State
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'questions_asked' not in st.session_state:
    st.session_state.questions_asked = 0
if 'mentorship_mode' not in st.session_state:
    st.session_state.mentorship_mode = False
if 'initial_question_asked' not in st.session_state:
    st.session_state.initial_question_asked = False
if 'pending_scouting_inputs' not in st.session_state:
    st.session_state.pending_scouting_inputs = None
if 'pending_coach_inputs' not in st.session_state:
    st.session_state.pending_coach_inputs = None

# Player Recruitment State Variables
if 'scouting_mode' not in st.session_state:
    st.session_state.scouting_mode = False
if 'scouting_data' not in st.session_state:
    st.session_state.scouting_data = {}
if 'current_scouting_stage' not in st.session_state:
    st.session_state.current_scouting_stage = None

# Coach Recruitment State Variables
if 'coach_recruitment_mode' not in st.session_state:
    st.session_state.coach_recruitment_mode = False
if 'coach_recruitment_data' not in st.session_state:
    st.session_state.coach_recruitment_data = {}
if 'current_coach_stage' not in st.session_state:
    st.session_state.current_coach_stage = None


# Title
st.title("⚽ QUCOON Football Academy Career Assistant")
st.markdown("Welcome to QUCOON Academy's AI Career Consultant - Your pathway to professional football success!")

# API Key
api_key = GEMINI_API_KEY

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Mode indicators
if st.session_state.scouting_mode:
    if st.session_state.current_scouting_stage == "awaiting_input":
        st.info("🔍 Player Recruitment Active. Please provide ALL details in ONE message.")
    else:
        st.info("🔍 Player Recruitment Active.")
elif st.session_state.coach_recruitment_mode:
    if st.session_state.current_coach_stage == "awaiting_input":
        st.info("👔 Coach Recruitment Active. Please provide ALL details in ONE message.")
    else:
        st.info("👔 Coach Recruitment Active.")
elif st.session_state.mentorship_mode:
    st.info("🎯 Mentorship Mode. Ask about your career!")
elif st.session_state.user_type == "new_user_selecting_pathway":
    st.info("Choose Player or Coach Development.")
elif st.session_state.user_type == "new_user_general_inquiry":
    st.info("Ask about QUCOON Academy or your football career!")
else:
    st.info("👋 Welcome! Are you **Existing** (with ID) or **New**?")


# Initial welcome message display
if not st.session_state.initial_question_asked:
    initial_welcome_message = "Welcome to QUCOON Football Academy! Are you an **existing** member (with a talent ID) or **new** to our academy?"
    st.session_state.messages.append({"role": "assistant", "content": initial_welcome_message})
    st.session_state.initial_question_asked = True
    with st.chat_message("assistant"):
        st.markdown(initial_welcome_message)


# Chat input
if prompt := st.chat_input("Ask me about your football career at QUCOON Academy..."):
    st.session_state.questions_asked += 1

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response_text = ""

    # Priority to recruitment agents if active
    if st.session_state.scouting_mode:
        response_text = handle_scouting_agent(prompt)
    elif st.session_state.coach_recruitment_mode:
        response_text = handle_coach_recruitment_agent(prompt)
    elif st.session_state.user_type in ["existing_player", "existing_coach", "new_coach"]:
        next_stage_keywords = ["next stage", "next step", "recruitment form", "trials form", "progress", "application", "form"]
        if contains_any_keyword(prompt, next_stage_keywords):
            response_text = f"Here is the link to the official application form: [Application Form]({INITIAL_APPLICATION_FORM_URL})"
        else:
            response_text = get_gemini_response(prompt, api_key)
    else:
        if st.session_state.user_type is None:
            talent_id_keywords = ["talent id", "talentid", "your id", "player id", "coach id", "existing"]
            new_user_keywords = ["new", "join", "enroll", "no id", "i'm new"]

            if contains_any_keyword(prompt, talent_id_keywords):
                st.session_state.user_type = "awaiting_talent_id"
                response_text = "Please enter your QUCOON Academy talent ID (starts with P for players or C for coaches)."
            elif contains_any_keyword(prompt, new_user_keywords):
                st.session_state.user_type = "new_user_general_inquiry"
                response_text = "Welcome to QUCOON Football Academy! How can I help you today? Feel free to ask about our programs, facilities, or anything else about football careers. We're here to guide you."
            else:
                response_text = "To provide you with the best assistance, could you please confirm if you are an **existing** QUCOON Academy player/coach with a talent ID, or if you are **new** to our academy and interested in joining?"

        elif st.session_state.user_type == "awaiting_talent_id":
            talent_id = prompt.upper().strip()
            user_data, user_type_found = get_user_data(talent_id)

            if user_data:
                st.session_state.user_type = f"existing_{user_type_found}"
                st.session_state.user_data = user_data
                st.session_state.mentorship_mode = True
                response_text = f"🎯 Welcome back, {st.session_state.user_data['name']}! How can I help your career today?"
            else:
                response_text = "ID not recognized. Please re-enter or say 'new' to join."

        elif st.session_state.user_type == "new_user_general_inquiry":
            player_pathway_keywords = ["player", "footballer", "aspiring player", "play", "join as player", "player development"]
            coach_pathway_keywords = ["coach", "coaching", "future coach", "manage", "mentor", "join as coach", "coaching development"]

            if contains_any_keyword(prompt, player_pathway_keywords):
                st.session_state.scouting_mode = True
                st.session_state.user_type = "new_user"
                response_text = handle_scouting_agent(None)
            elif contains_any_keyword(prompt, coach_pathway_keywords):
                st.session_state.coach_recruitment_mode = True
                st.session_state.user_type = "new_coach"
                response_text = handle_coach_recruitment_agent(None)
            else:
                response_text = get_gemini_response(prompt, api_key)
                if "academy" in response_text.lower() or "program" in response_text.lower() or "career" in response_text.lower():
                     response_text += "\n\nWhen you're ready, let me know if you're interested in **Player Development** or **Coaching Development**."


    with st.chat_message("assistant"):
        st.markdown(response_text)

    st.session_state.messages.append({"role": "assistant", "content": response_text})

if st.button("Clear Chat"):
    st.session_state.messages = []
    st.session_state.user_type = None
    st.session_state.user_data = {}
    st.session_state.questions_asked = 0
    st.session_state.scouting_mode = False
    st.session_state.scouting_data = {}
    st.session_state.mentorship_mode = False
    st.session_state.initial_question_asked = False
    st.session_state.current_scouting_stage = None
    st.session_state.pending_scouting_inputs = None
    st.session_state.coach_recruitment_mode = False
    st.session_state.coach_recruitment_data = {}
    st.session_state.current_coach_stage = None
    st.session_state.pending_coach_inputs = None
    st.rerun()