# utils.py
import re

def contains_any_keyword(text, keywords):
    """
    Checks if the given text contains any of the provided keywords,
    with robust normalization for fuzzy matching.
    """
    normalized_text = re.sub(r'[^a-z0-9\s]', '', text.lower()) # Remove non-alphanumeric, lowercase
    for keyword in keywords:
        normalized_keyword = re.sub(r'[^a-z0-9\s]', '', keyword.lower())
        # Use word boundaries (\b) to match whole words/phrases more accurately
        if re.search(r'\b' + re.escape(normalized_keyword) + r'\b', normalized_text):
            return True
    return False

def handle_length_error(inputs_received, expected_length, field_prompts, required_keys_ordered):
    """Generates a detailed error message for incorrect input count."""
    received = len(inputs_received)

    feedback = f"❌ **Input Count Error:** Expected {expected_length} items, received {received}.\n\n"
    feedback += "**What you provided:**\n"
    # Show up to the first 5 items provided
    for i, inp in enumerate(inputs_received[:5]):
        feedback += f"{i+1}. `{inp}`\n"
    if received > 5:
        feedback += f"... and {received - 5} more items.\n"

    feedback += f"\n**What we need (in order):**\n"
    for i, key in enumerate(required_keys_ordered):
        feedback += f"{i+1}. `{field_prompts[key]}`\n"

    feedback += "\n**💡 Tip:** Make sure each piece of info is separated by a comma. Please copy your last message, fix the missing/extra items, and try again!"
    return feedback