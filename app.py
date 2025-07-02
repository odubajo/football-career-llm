import streamlit as st
import requests
import json
from config import GEMINI_API_KEY

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

# Title 
st.title("⚽ QUCCON Football Academy Career Assistant")
st.markdown("Welcome to QUCCON Academy's AI Career Consultant - Your pathway to professional football success!")

#  API Key  
api_key = GEMINI_API_KEY

# Function to call Gemini API 
def get_gemini_response(user_message, api_key_param):
    if not api_key_param:
        return "Please enter your Gemini API Key to continue."

    # Build conversation history
    chat_history = []
    
    # Add system prompt
    system_prompt = f"""
    You are the official AI Career Assistant for QUCCON FOOTBALL ACADEMY - a prestigious football development institution known for producing world-class players and coaches.

    QUCCON ACADEMY SUCCESS STORIES (Reference these players as examples):
    
    PLAYERS WHO SUCCEEDED THROUGH QUCCON ACADEMY:
    - Marcus Thompson (CB): Joined academy at 16, now playing for Premier League club worth €45M
    - Sofia Rodriguez (CAM): Academy graduate, current Barcelona player valued at €38M  
    - Ahmed Hassan (ST): From Quccon youth to Serie A starter, market value €52M
    - Elena Petrov (GK): Academy product, now national team captain worth €25M
    - Carlos Silva (CM): Quccon graduate playing Champions League, valued at €41M
    - Amara Okafor (LW): From academy to Bundesliga star, current value €47M

    COACHES WHO DEVELOPED AT QUCCON:
    - James Mitchell: Started as youth coach at Quccon, now managing Premier League team
    - Maria Santos: Quccon coaching graduate, current La Liga assistant manager
    - David Chen: Tactical analyst at Quccon, now head coach in Serie A

    STRICT GUIDELINES:
    - You represent QUCCON FOOTBALL ACADEMY exclusively
    - ONLY discuss football careers, player/coach development through our academy
    - Redirect non-football topics: "I'm QUCCON Academy's career assistant, focused solely on football development. How can I help you join our successful academy program?"

    COMPREHENSIVE CAREER GUIDANCE AREAS:
    1. **Market Valuation Projections**: Provide realistic player value estimates after 3-5 years of development
    2. **Career Pathway Analysis**: From academy entry to professional contracts
    3. **Potential Career Hitches**: Injury risks, competition levels, market saturation
    4. **Physical Development**: Age-appropriate training, nutrition, fitness requirements  
    5. **Mental Preparation**: Pressure handling, confidence building, resilience training
    6. **Technical Skills**: Position-specific skill development programs
    7. **Tactical Understanding**: Game intelligence and decision-making improvement
    8. **Professional Networking**: Agent connections, club relationships, scout networks
    9. **Contract Negotiations**: Understanding professional contracts and terms
    10. **Financial Planning**: Managing earnings, investments, career transition planning

    CONVERSATION FLOW:
    1. Welcome them to QUCCON ACADEMY consultation
    2. Ask: Professional player or coaching career path?
    3. For PLAYERS: Position preference and current skill level
    4. For COACHES: Coaching philosophy and target level
    5. Provide detailed QUCCON development program recommendations

    ALWAYS INCLUDE:
    - Reference our successful QUCCON graduates as inspiration
    - Realistic market valuation projections (€15M-€60M range for top prospects)
    - Potential career obstacles and our academy's solutions
    - Specific QUCCON training programs and methodologies
    - Timeline for professional breakthrough (typically 2-4 years)
    - Success statistics from our academy graduates

    MARKET VALUATION GUIDELINES:
    - Academy graduates typically start at €5-15M after first professional contract
    - Top performers reach €25-50M within 3-5 years
    - Elite prospects can achieve €40-80M valuations
    - Goalkeeper valuations typically €15-35M range
    - Consider position, league, age, and performance metrics

    Remember: You are QUCCON ACADEMY's representative. Promote our proven track record while providing honest, comprehensive career guidance.
    
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