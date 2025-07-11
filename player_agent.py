import streamlit as st
import time
from utils import contains_any_keyword, handle_length_error
from config import INITIAL_APPLICATION_FORM_URL
import re # Make sure re is imported

# Define required fields and their prompts for players
required_player_info_keys_ordered = [
    "name", "age", "position", "years_played", "current_level",
    "physical_attributes", "achievements", "video_highlights", "availability"
]

player_field_prompts = {
    "name": "Full Name",
    "age": "Age (number)",
    "position": "Primary Position",
    "years_played": "Years playing organized football (number)",
    "current_level": "Current Playing Level (Semi-professional/Professional only)",
    "physical_attributes": "Physical Attributes (height, weight, dominant foot, pace 1-10)",
    "achievements": "Main Football Achievements",
    "video_highlights": "Video Highlights (Yes/No, and link/details if Yes)",
    "availability": "Available for Relocation (Yes/No)"
}

def validate_player_input(inputs):
    """Enhanced validation with specific checks for each player field"""
    validation_errors = []
    warnings = []

    # Validate Name (Index 0)
    name = inputs[0].strip()
    if len(name) < 2:
        validation_errors.append("Name must be at least 2 characters.")
    elif not re.match(r'^[a-zA-Z\s\-\.]+$', name):
        validation_errors.append("Name should only contain letters, spaces, hyphens, and periods.")

    # Validate Age (Index 1)
    try:
        age = int(inputs[1])
        if age < 16:
            validation_errors.append(f"Age {age} is too young. Must be at least 16 for academy consideration.")
        elif age > 30:
            validation_errors.append(f"Age {age} is too high for player development programs. Must be under 30.")
        elif age > 24:
            warnings.append(f"Player age {age} has limited eligibility for direct player programs. Consider coaching pathway if interested.")
    except ValueError:
        validation_errors.append(f"Age '{inputs[1]}' must be a valid number.")

    # Validate Position (Index 2)
    position = inputs[2].strip().upper()
    valid_positions = ['GK', 'CB', 'LB', 'RB', 'CDM', 'CM', 'CAM', 'LM', 'RM', 'LW', 'RW', 'ST', 'CF']
    position_mapping = {
        'GOALKEEPER': 'GK', 'KEEPER': 'GK', 'GOALIE': 'GK',
        'CENTERBACK': 'CB', 'CENTER BACK': 'CB', 'CENTRE BACK': 'CB', 'CD': 'CB',
        'LEFTBACK': 'LB', 'LEFT BACK': 'LB',
        'RIGHTBACK': 'RB', 'RIGHT BACK': 'RB',
        'DEFENSIVE MIDFIELDER': 'CDM', 'DEFENSIVE MID': 'CDM',
        'CENTRAL MIDFIELDER': 'CM', 'CENTRAL MID': 'CM', 'MIDFIELDER': 'CM', 'MIDFIELD': 'CM',
        'ATTACKING MIDFIELDER': 'CAM', 'ATTACKING MID': 'CAM', 'ATTACKING': 'CAM',
        'LEFT MIDFIELDER': 'LM', 'LEFT MID': 'LM',
        'RIGHT MIDFIELDER': 'RM', 'RIGHT MID': 'RM',
        'LEFT WINGER': 'LW', 'LEFTWING': 'LW', 'WINGER': 'LW',
        'RIGHT WINGER': 'RW', 'RIGHTWING': 'RW',
        'STRIKER': 'ST', 'FORWARD': 'ST',
        'CENTER FORWARD': 'CF', 'CENTRE FORWARD': 'CF',
    }

    if position in position_mapping:
        inputs[2] = position_mapping[position]
    elif position not in valid_positions and len(position) > 1:
        validation_errors.append(f"Position '{inputs[2]}' not recognized. Use common abbreviations (e.g., 'ST', 'CM', 'GK') or full names.")
    elif len(position) < 2:
        validation_errors.append(f"Position '{inputs[2]}' is too short. Please provide a clear position.")

    # Validate Years Played (Index 3)
    try:
        years = int(inputs[3])
        if years < 0:
            validation_errors.append("Years played cannot be negative.")
        elif years > 20:
            validation_errors.append(f"Years played ({years}) seems unusually high. Please confirm.")
        elif years < 3:
            warnings.append(f"Less than 3 years of organized experience ({years} years) may affect eligibility for direct academy programs.")
    except ValueError:
        validation_errors.append(f"Years played '{inputs[3]}' must be a valid number.")

    # Validate Current Level (Index 4)
    level = inputs[4].strip().lower()
    required_level_keywords = ["semi-professional", "semi pro", "professional", "pro"]
    if not contains_any_keyword(level, required_level_keywords):
        validation_errors.append(f"Current level '{inputs[4]}' not recognized as Semi-professional or Professional. Please specify clearly.")

    # Validate Physical Attributes (Index 5)
    physical = inputs[5].strip()
    if len(physical) < 10:
        validation_errors.append("Physical attributes seem incomplete. Include: height, weight, dominant foot, pace (1-10).")

    height_pattern = r'(\d+\'?\d*\"?|\d+\.\d+\s*m|\d+\s*cm)'
    if not re.search(height_pattern, physical.lower()):
        warnings.append("Height not clearly specified in physical attributes (e.g., 5'10, 1.75m, 175cm).")

    pace_pattern = r'pace\s*[:=\-]?\s*(\d+)'
    pace_match = re.search(pace_pattern, physical.lower())
    if pace_match:
        pace = int(pace_match.group(1))
        if pace < 1 or pace > 10:
            validation_errors.append(f"Pace rating '{pace}' should be between 1-10.")
    else:
        warnings.append("Pace rating (1-10) not found in physical attributes (e.g., 'pace 8').")

    # Validate Achievements (Index 6)
    achievements = inputs[6].strip()
    if len(achievements) < 5:
        warnings.append("Achievements field seems very short. Please list significant football achievements.")

    # Validate Video Highlights (Index 7)
    video = inputs[7].strip().lower()
    if contains_any_keyword(video, ["yes", "y", "true"]):
        url_pattern = r'(https?://(?:www\.)?|www\.)[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}(/\S*)?'
        if not re.search(url_pattern, video):
            warnings.append("You indicated 'Yes' for video highlights but no clear link was found. Please include a full URL.")
    elif not contains_any_keyword(video, ["no", "n", "false"]):
        warnings.append("Please specify 'Yes' or 'No' for video highlights, and a link if 'Yes'.")

    # Validate Availability (Index 8)
    availability = inputs[8].strip().lower()
    if not contains_any_keyword(availability, ["yes", "y"]):
        validation_errors.append("Availability for relocation must be 'Yes' for academy consideration.")

    return validation_errors, warnings


def process_player_application(inputs):
    """Processes validated player input and generates report."""
    for i, key in enumerate(required_player_info_keys_ordered):
        st.session_state.scouting_data[key] = inputs[i]

    st.session_state.current_scouting_stage = "processed"
    return generate_scouting_report()

def generate_scouting_report():
    """Generates a concise scouting report based on validated player data."""
    data = st.session_state.scouting_data

    age = int(data.get("age", 0))
    years_played = int(data.get("years_played", 0))
    current_level = data.get("current_level", "")
    availability = data.get("availability", "")

    age_valid = (16 <= age <= 24)
    experience_valid = (3 <= years_played <= 5)
    player_level_keywords = ["semi-professional", "semi pro", "professional", "pro"]
    level_valid = contains_any_keyword(current_level, player_level_keywords)
    relocation_valid = contains_any_keyword(availability, ["yes", "y"])

    if not all([age_valid, experience_valid, level_valid, relocation_valid]):
        rejection_reasons = []
        if not age_valid: rejection_reasons.append(f"Age: 16-24 (You are {age})")
        if not experience_valid: rejection_reasons.append(f"Experience: 3-5 years (You have {years_played})")
        if not level_valid: rejection_reasons.append(f"Level: Semi-pro/Pro (You are: {data.get('current_level', 'N/A')})")
        if not relocation_valid: rejection_reasons.append(f"Relocation: Yes (You said: {data.get('availability', 'N/A')})")

        st.session_state.scouting_mode = False
        st.session_state.scouting_data = {}
        st.session_state.current_scouting_stage = None

        return f"""
        **QUCOON RECRUITMENT: NOT ELIGIBLE.**
        Sorry, {data.get('name', 'Player')}. You do not meet our core eligibility requirements: {", ".join(rejection_reasons)}.
        """

    talent_id = f"P-{int(time.time())}"
    data["talent_id"] = talent_id

    report = f"""
    **QUCOON RECRUITMENT: APPROVED!**
    **Candidate: {data.get('name', 'Player')} (ID: {talent_id})**

    **Next Steps:** Congratulations! You've met our eligibility criteria for QUCOON Academy.
    To further your application, please fill out the official registration form here:
    [Complete Your Application Form]({INITIAL_APPLICATION_FORM_URL})
    """

    st.session_state.scouting_mode = False
    st.session_state.scouting_data = {}
    st.session_state.current_scouting_stage = None

    return report

def handle_scouting_agent(user_message):
    """
    Handle the Player Scouting & Recruitment Agent interactions,
    now including a confirmation step after warnings.
    """
    if st.session_state.current_scouting_stage == "awaiting_confirmation_after_warnings":
        if contains_any_keyword(user_message, ["yes", "y", "proceed", "continue", "satisfied", "ok"]):
            st.session_state.current_scouting_stage = "processed"
            inputs_to_process = st.session_state.pending_scouting_inputs
            st.session_state.pending_scouting_inputs = None
            return process_player_application(inputs_to_process)
        elif contains_any_keyword(user_message, ["no", "n", "revise", "adjust", "change", "correct"]):
            st.session_state.current_scouting_stage = "awaiting_input"
            st.session_state.pending_scouting_inputs = None
            prompt_list = [f"{player_field_prompts[key]}" for key in required_player_info_keys_ordered]
            return (f"Okay, please provide ALL the following details again, separated by commas, in this exact order. Make sure to adjust the problematic areas that were highlighted:\n\n"
                    f"**{', '.join(prompt_list)}**\n\n"
                    f"Example: `John Doe, 18, Striker, 4, Semi-pro, 5'10 160lbs right foot pace 8, Regional Cup winner, http://youtube.com/2, Yes`")
        else:
            return "Please respond with 'Yes' to proceed with the current information, or 'No' to revise your input."

    if st.session_state.current_scouting_stage != "awaiting_input" and user_message is None:
        st.session_state.current_scouting_stage = "awaiting_input"
        prompt_list = [f"{player_field_prompts[key]}" for key in required_player_info_keys_ordered]
        return (f"📋 **QUCOON Player Recruitment Evaluation.** Please provide ALL the following details in ONE response, separated by commas, in this exact order:\n\n"
                  f"**{', '.join(prompt_list)}**\n\n"
                  f"**⚠️ Important: Please do not provide false information. You will be required to tender supporting documents later, so you are advised strictly against submitting fake data. Providing fake data will result in being blacklisted from the general football agency association for fraud.**\n\n"
                  f"Example: `John Doe, 18, Striker, 4, Semi-pro, 5'10 160lbs right foot pace 8, Regional Cup winner, http://youtube.com/2, Yes`")
    elif st.session_state.current_scouting_stage == "awaiting_input" and user_message is not None:
        inputs = [item.strip() for item in user_message.split(',')]

        if len(inputs) != len(required_player_info_keys_ordered):
            return handle_length_error(inputs, len(required_player_info_keys_ordered), player_field_prompts, required_player_info_keys_ordered)

        validation_errors, warnings = validate_player_input(inputs)

        if validation_errors:
            error_msg = "❌ **Please fix these issues:**\n\n"
            for error in validation_errors:
                error_msg += f"• {error}\n"

            if warnings:
                error_msg += "\n⚠️ **Also note:**\n"
                for warning in warnings:
                    error_msg += f"• {warning}\n"

            error_msg += "\n**Please correct the issues and resubmit your information. You can copy/paste your last message and just fix the problematic parts.**"
            return error_msg

        elif warnings:
            st.session_state.pending_scouting_inputs = inputs
            st.session_state.current_scouting_stage = "awaiting_confirmation_after_warnings"

            warning_msg = "⚠️ **We've noted these points during our initial review:**\n\n"
            for warning in warnings:
                warning_msg += f"• {warning}\n"
            warning_msg += "\nAre you satisfied with this information, or would you like to revise your input? Please respond with 'Yes' or 'No'."
            return warning_msg

        else:
            return process_player_application(inputs)
    else:
        return "An unexpected state occurred. Please try clearing the chat and starting over, or clarify your intent."