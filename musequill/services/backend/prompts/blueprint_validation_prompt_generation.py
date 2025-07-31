import json
from textwrap import dedent
from .target_json_schema import TARGET_JSON_SCHEMA, EXPECTED_OUTPUT

def generate_validation_prompt(llm_json_output: dict) -> str:
    """
    Generates a strict validation and correction prompt from LLM's loose JSON output.
    
    Args:
        llm_json_output (dict): The raw LLM-generated output as a Python dict.
    
    Returns:
        str: A prompt string instructing the LLM to normalize it to the exact schema.
    """
    # Convert the malformed JSON back to a formatted string for inclusion in prompt
    raw_json = json.dumps(llm_json_output, indent=2, ensure_ascii=False)

    # You could import your schema as a constant, or keep it hardcoded


    # Final prompt string
    prompt = dedent(f"""
    The following JSON object is loosely structured and does not conform to the required JSON schema.

    Please correct it so it exactly matches the JSON schema below. That means:
    - Correct field names (e.g., 'phase1' → 'blueprint.phase_1')
    - Nest structure as required
    - Convert flat items into objects/arrays where needed
    - Populate all fields with meaningful data

    ❗Return ONLY a valid JSON object. Do NOT include any explanations or markdown code blocks.

    # Loose JSON to correct:
    {raw_json}

    # Target JSON Schema:
    {TARGET_JSON_SCHEMA}
    
    # Expected JSON Output:
    {EXPECTED_OUTPUT}

    ❗Output a valid, parseable JSON object that conforms exactly to the schema above.

    # ABSOLUTE RULES:
- ❗ Output MUST be valid JSON that conforms to the structure above
- ❗ Do NOT include any explanation, comment, or markdown
- ❗ Populate **every field** in the schema with SPECIFIC, USEFUL data

# Output Format Requirements:
- 🔹 Pure JSON object
- 🔹 All fields filled
- 🔹 NO markdown/code blocks
- 🔹 NO extra commentary

# DO NOT DO:
- ❌ Do not preface with “Here’s your JSON:”
- ❌ Do not wrap output in triple backticks
- ❌ Do not include schema again
- ❌ Do not repeat the template data


🛑 Your ONLY job is to produce a JSON object.
✅ Your JSON MUST match the structure and field names EXACTLY.
""")

    return prompt
