import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def summarize_text(text: str) -> str:
    if not text or not text.strip():
        return "Please provide text to summarize."
    prompt = f"Summarize the following text in simple language:\n\n{text}"
    model_name = os.getenv("GEMINI_MODEL", "gemini-3.7-flash")
    models_to_try = [model_name, "gemini-3.7-flash", "gemini-3.8-flash", "gemini-1.5-flash", "gemini-1.5-pro"]

    last_error = None
    for m in models_to_try:
        try:
            model = genai.GenerativeModel(model_name=m)
            response = model.generate_content(prompt)
            if hasattr(response, "text") and response.text:
                return response.text.strip()
            elif hasattr(response, "parts") and response.parts:
                return "".join(part.text for part in response.parts).strip()
            return "No summary generated."
        except Exception as e:
            last_error = e
            continue

    return f"⚠️ Error in Summary: {last_error}"
