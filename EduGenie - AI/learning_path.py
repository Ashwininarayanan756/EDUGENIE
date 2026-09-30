import os
import traceback
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def get_learning_recommendations(topic: str, level: str = None) -> str:
    if not topic or not topic.strip():
        return "Please provide a topic to generate learning recommendations."

    level_instruction = f" Current learner level: {level}." if level else ""
    prompt = f"""You are an AI tutor. The student wants to learn about: {topic}.{level_instruction}
Suggest a structured and adaptive learning path including key topics, order of learning, and resources. Include beginner, intermediate, and advanced levels if needed.
Format the output clearly with sections for Beginner, Intermediate, and Advanced levels, including Key Topics, Estimated Time, and Resources (Tutorials, Videos, Books, Practice Platforms).
"""
    model_name = os.getenv("GEMINI_MODEL", "gemini-3.7-flash")
    models_to_try = [model_name, "gemini-3.7-flash", "gemini-3.8-flash", "gemini-1.5-flash", "gemini-1.5-pro"]

    last_error = None
    for m in models_to_try:
        try:
            model = genai.GenerativeModel(model_name=m)
            response = model.generate_content(prompt)
            print("Gemini raw response:", response)

            if hasattr(response, "text") and response.text:
                return response.text.strip()
            elif hasattr(response, "parts") and response.parts:
                return "".join(part.text for part in response.parts).strip()
            else:
                return "❌ Could not extract content from Gemini response."
        except Exception as e:
            last_error = e
            traceback.print_exc()
            continue

    return f"❌ Error occurred: {str(last_error)}"
