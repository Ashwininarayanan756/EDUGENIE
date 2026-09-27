import os
import re
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def clean_json_block(text: str) -> str:
    # Remove Markdown ```json ... ``` code fences if present
    cleaned = re.sub(r"```(?:json)?\s*(.*?)\s*```", r"\1", text, flags=re.DOTALL).strip()
    # If there are still surrounding characters, extract the json array [ ... ]
    match = re.search(r"\[\s*\{.*\}\s*\]", cleaned, flags=re.DOTALL)
    if match:
        return match.group(0).strip()
    return cleaned

def generate_quiz(text: str) -> list:
    if not text or not text.strip():
        return [{"question": "Please provide a topic or passage for the quiz.", "options": ["N/A"], "answer": "N/A"}]

    prompt = f"""You are a quiz generator.

From the following passage or topic, create 3 multiple-choice questions. Each question should include:
- A "question"
- A list of 4 "options"
- A correct "answer" that must exactly match one of the options.

Format your output as **valid JSON**, like this:
[
  {{
    "question": "What is ...?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "Option A"
  }}
]

Passage:
{text}
"""
    model_name = os.getenv("GEMINI_MODEL", "gemini-3.7-flash")
    models_to_try = [model_name, "gemini-3.7-flash", "gemini-3.8-flash", "gemini-1.5-flash", "gemini-1.5-pro"]
    
    last_error = None
    for m in models_to_try:
        try:
            model = genai.GenerativeModel(model_name=m)
            response = model.generate_content(prompt)
            quiz_text = ""
            if hasattr(response, "text") and response.text:
                quiz_text = response.text.strip()
            elif hasattr(response, "parts") and response.parts:
                quiz_text = "".join(p.text for p in response.parts).strip()
            
            cleaned_text = clean_json_block(quiz_text)
            quiz_data = json.loads(cleaned_text)
            if isinstance(quiz_data, list) and len(quiz_data) > 0:
                return quiz_data
        except Exception as e:
            last_error = e
            continue

    return [
        {
            "question": f"Error generating quiz: {last_error}",
            "options": ["Check API Key", "Check Model Config", "Check Input Text", "Retry"],
            "answer": "Retry"
        }
    ]
