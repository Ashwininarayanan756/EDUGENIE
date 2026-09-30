import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def get_gemini_model():
    model_name = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    if not model_name.startswith("models/") and "/" not in model_name:
        # Also supports plain model names
        pass
    return genai.GenerativeModel(model_name=model_name)

def answer_question_with_gemini(question: str) -> str:
    if not question or not question.strip():
        return "Please ask a question."
    try:
        model = get_gemini_model()
        response = model.generate_content(question)
        if hasattr(response, "text") and response.text:
            return response.text.strip()
        elif hasattr(response, "parts") and response.parts:
            return "".join(part.text for part in response.parts).strip()
        return "No response generated."
    except Exception as e:
        # Fallback to alternate model if primary model fails
        model_name = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
        for alt_model in [model_name, "gemini-3.8-flash", "gemini-3.8-pro", "gemini-1.5-flash", "gemini-1.5-pro"]:
            try:
                model = genai.GenerativeModel(model_name=alt_model)
                response = model.generate_content(question)
                if hasattr(response, "text") and response.text:
                    return response.text.strip()
            except Exception:
                continue
        return f"⚠️ Error in QnA: {e}"

def answer_question(question: str) -> str:
    return answer_question_with_gemini(question)
