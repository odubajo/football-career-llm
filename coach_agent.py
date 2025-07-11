import streamlit as st
import time
from utils import contains_any_keyword, handle_length_error
from config import INITIAL_APPLICATION_FORM_URL
import re # Make sure re is imported

# Define required fields and their prompts for coaches
required_coach_info_keys_ordered = [
    "name", "age", "years_experience", "highest_certification", "specialty",
    "previous_roles", "references_available", "availability_start_date"
]

coach_field_prompts = {
    "name": "Full Name",
    "age": "Age (number)",
    "years_experience": "Years of Coaching Experience (number)",
    "highest_certification": "Highest Coaching Certification",
    "specialty": "Primary Coaching Specialty",
    "previous_roles": "Previous Head Coach/Senior Roles",
    "references_available": "Professional References Available (Yes/No)",
    "availability_start_date": "Availability Start Date (e.g., 'Immediately', 'Sept 1, 2025')"
}

def validate_coach_input(inputs):
    """Enhanced validation with specific checks for each coach field"""
    validation_errors = []
    warnings = []

    # Validate Name 
    name = inputs[0].strip()
    if len(name) < 2:
        validation_errors.append("Name must be at least 2 characters.")
    elif not re.match(r'^[a-zA-Z\s\-\.]+$', name):
        validation_errors.append("Name should only contain letters, spaces, hyphens, and periods.")

    # Validate Age 
    try:
        age = int(inputs[1])
        if age < 25:
            validation_errors.append(f"Age {age} is below minimum eligible age for coaching (25).")
        elif age > 70:
            warnings.append(f"Age {age} seems high for active coaching. Please confirm.")
    except ValueError:
        validation_errors.append(f"Age '{inputs[1]}' must be a valid number.")

    # Validate Years of Coaching Experience 
    try:
        years_exp = int(inputs[2])
        if years_exp < 5:
            validation_errors.append(f"Years of experience ({years_exp}) is below minimum eligible (5 years).")
        elif years_exp > 40:
            warnings.append(f"Years of experience ({years_exp}) seems unusually high. Please confirm.")
    except ValueError:
        validation_errors.append(f"Years of experience '{inputs[2]}' must be a valid number.")

    # Validate Highest Certification 
    certification = inputs[3].strip().lower()
    required_cert_keywords = ["pro", "a license", "uefa pro", "caf a", "ussf a", "fifa", "premier diploma", "b license"]
    if not contains_any_keyword(certification, required_cert_keywords):
        validation_errors.append(f"Highest certification '{inputs[3]}' not recognized as a high-level qualification (e.g., UEFA Pro, A License).")

    # Validate Specialty 
    specialty = inputs[4].strip()
    if len(specialty) < 3:
        validation_errors.append("Specialty field seems too short or empty. Please specify a coaching specialty (e.g., 'Youth Development', 'Tactical Analysis').")

    # Validate Previous Roles 
    previous_roles = inputs[5].strip().lower()
    required_role_keywords = ["head coach", "senior coach", "technical director", "first team coach", "manager", "director of football"]
    if not contains_any_keyword(previous_roles, required_role_keywords):
        validation_errors.append(f"Previous roles '{inputs[5]}' do not indicate senior-level experience (e.g., Head Coach, Technical Director).")

    # Validate References Available 
    references = inputs[6].strip().lower()
    if not contains_any_keyword(references, ["yes", "y"]):
        validation_errors.append("Professional references must be available ('Yes').")

    # Validate Availability Start Date 
    availability_date = inputs[7].strip()
    if len(availability_date) < 3:
        validation_errors.append("Availability start date seems too short. Please provide a clear date or 'Immediately'.")

    return validation_errors, warnings

def process_coach_application(inputs):
    """Processes validated coach input and generates report."""
    for i, key in enumerate(required_coach_info_keys_ordered):
        st.session_state.coach_recruitment_data[key] = inputs[i]

    st.session_state.current_coach_stage = "processed"
    return generate_coach_recruitment_report()

def generate_coach_recruitment_report():
    """Generates a concise recruitment report based on validated coach data."""
    data = st.session_state.coach_recruitment_data

    age = int(data.get("age", 0))
    years_experience = int(data.get("years_experience", 0))
    highest_certification = data.get("highest_certification", "")
    previous_roles = data.get("previous_roles", "")
    references_available = data.get("references_available", "")

    age_valid = (age >= 30)
    experience_valid = (years_experience >= 8)
    coach_cert_keywords = ["pro", "a license", "uefa pro", "caf a", "ussf a", "fifa", "premier diploma"]
    cert_valid = contains_any_keyword(highest_certification, coach_cert_keywords)
    coach_role_keywords = ["head coach", "senior coach", "technical director", "first team coach", "manager", "director of football"]
    roles_valid = contains_any_keyword(previous_roles, coach_role_keywords)
    references_valid = contains_any_keyword(references_available, ["yes", "y"])

    if not all([age_valid, experience_valid, cert_valid, roles_valid, references_valid]):
        rejection_reasons = []
        if not age_valid: rejection_reasons.append(f"Age: 30+ (You are {age})")
        if not experience_valid: rejection_reasons.append(f"Experience: 8+ years (You have {years_experience})")
        if not cert_valid: rejection_reasons.append(f"Certification: High-level (You provided: {data.get('highest_certification', 'N/A')})")
        if not roles_valid: rejection_reasons.append(f"Previous Roles: Head/Senior (You provided: {data.get('previous_roles', 'N/A')})")
        if not references_valid: rejection_reasons.append(f"References: Available (You stated: {data.get('references_available', 'N/A')})")

        st.session_state.coach_recruitment_mode = False
        st.session_state.coach_recruitment_data = {}
        st.session_state.current_coach_stage = None

        return f"""
        **QUCOON COACH RECRUITMENT: NOT ELIGIBLE for Head/Senior Role.**
        Sorry, {data.get('name', 'Coach')}. You do not meet our core eligibility requirements: {", ".join(rejection_reasons)}.
        """

    talent_id = f"C-{int(time.time())}"
    data["talent_id"] = talent_id

    report = f"""
    **QUCOON COACH RECRUITMENT: APPROVED!**
    **Candidate: {data.get('name', 'Coach')} (ID: {talent_id})**

    **Next Steps:** Congratulations! You've met our eligibility criteria for QUCOON Academy.
    To further your application, please fill out the official registration form here:
    [Complete Your Application Form]({INITIAL_APPLICATION_FORM_URL})
    """

    st.session_state.coach_recruitment_mode = False
    st.session_state.coach_recruitment_data = {}
    st.session_state.current_coach_stage = None

    return report

def handle_coach_recruitment_agent(user_message):
    """
    Handle Coach Recruitment Agent interactions,
    now including a confirmation step after warnings.
    """
    if st.session_state.current_coach_stage == "awaiting_confirmation_after_warnings":
        if contains_any_keyword(user_message, ["yes", "y", "proceed", "continue", "satisfied", "ok"]):
            st.session_state.current_coach_stage = "processed"
            inputs_to_process = st.session_state.pending_coach_inputs
            st.session_state.pending_coach_inputs = None
            return process_coach_application(inputs_to_process)
        elif contains_any_keyword(user_message, ["no", "n", "revise", "adjust", "change", "correct"]):
            st.session_state.current_coach_stage = "awaiting_input"
            st.session_state.pending_coach_inputs = None
            prompt_list = [f"{coach_field_prompts[key]}" for key in required_coach_info_keys_ordered]
            return (f"Okay, please provide ALL the following details again, separated by commas, in this exact order. Make sure to adjust the problematic areas that were highlighted:\n\n"
                    f"**{', '.join(prompt_list)}**\n\n"
                    f"Example: `Jane Smith, 35, 10, UEFA Pro, Youth Development, Head Coach U19s Dynamo, Yes, Immediately`")
        else:
            return "Please respond with 'Yes' to proceed with the current information, or 'No' to revise your input."

    if st.session_state.current_coach_stage != "awaiting_input" and user_message is None:
        st.session_state.current_coach_stage = "awaiting_input"
        prompt_list = [f"{coach_field_prompts[key]}" for key in required_coach_info_keys_ordered]
        return (f"👔 **QUCOON Coach Recruitment Evaluation.** Please provide ALL the following details in ONE response, separated by commas, in this exact order:\n\n"
                          f"**{', '.join(prompt_list)}**\n\n"
                          f"**⚠️ Important: Please do not provide false information. You will be required to tender supporting documents later, so you are advised strictly against submitting fake data. Providing fake data will result in being blacklisted from the general football agency association for fraud.**\n\n"
                          f"Example: `Jane Smith, 35, 10, UEFA Pro, Youth Development, Head Coach U19s Dynamo, Yes, Immediately`")
    elif st.session_state.current_coach_stage == "awaiting_input" and user_message is not None:
        inputs = [item.strip() for item in user_message.split(',')]

        if len(inputs) != len(required_coach_info_keys_ordered):
            return handle_length_error(inputs, len(required_coach_info_keys_ordered), coach_field_prompts, required_coach_info_keys_ordered)

        validation_errors, warnings = validate_coach_input(inputs)

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
            st.session_state.pending_coach_inputs = inputs
            st.session_state.current_coach_stage = "awaiting_confirmation_after_warnings"

            warning_msg = "⚠️ **We've noted these points during our initial review:**\n\n"
            for warning in warnings:
                warning_msg += f"• {warning}\n"
            warning_msg += "\nAre you satisfied with this information, or would you like to revise your input? Please respond with 'Yes' or 'No'."
            return warning_msg

        else:
            return process_coach_application(inputs)
    else:
        return "An unexpected state occurred. Please try clearing the chat and starting over, or clarify your intent."