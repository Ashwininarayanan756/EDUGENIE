import os
from dotenv import load_dotenv

load_dotenv()

USE_LOCAL = os.getenv("USE_LOCAL_EXPLAINER", "false").lower() in ("true", "1", "yes")
LOCAL_MODEL_NAME = os.getenv("LOCAL_MODEL_NAME", "MBZUAI/LaMini-Flan-T5-783M")

explain_tokenizer = None
explain_model = None

if USE_LOCAL:
    try:
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        import torch

        # Load the improved model for explanations
        explain_tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL_NAME)
        explain_model = AutoModelForSeq2SeqLM.from_pretrained(LOCAL_MODEL_NAME)
    except Exception as err:
        print(f"Notice: Local model '{LOCAL_MODEL_NAME}' not loaded ({err}). Falling back to Gemini.")
        explain_tokenizer = None
        explain_model = None

def _explain_with_gemini(topic: str) -> str:
    try:
        import google.generativeai as genai
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
        
        prompt = f"Explain the concept of '{topic}' in a simple and clear way for a school student."
        model_name = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
        model = genai.GenerativeModel(model_name=model_name)
        response = model.generate_content(prompt)
        if hasattr(response, "text") and response.text:
            return response.text.strip()
        elif hasattr(response, "parts") and response.parts:
            return "".join(p.text for p in response.parts).strip()
        return "No explanation generated."
    except Exception as e:
        # Fallback to alternate models
        for alt_model in ["gemini-3.8-flash", "gemini-3.8-pro", "gemini-1.5-flash", "gemini-1.5-pro"]:
            try:
                import google.generativeai as genai
                model = genai.GenerativeModel(model_name=alt_model)
                response = model.generate_content(f"Explain the concept of '{topic}' in a simple and clear way for a school student.")
                if hasattr(response, "text") and response.text:
                    return response.text.strip()
            except Exception:
                continue
        return f"⚠️ Error in Explanation: {e}"

def explain_topic(topic: str) -> str:
    if not topic or not topic.strip():
        return "Please provide a topic to explain."

    if explain_model is not None and explain_tokenizer is not None:
        try:
            input_text = f"Explain the concept of '{topic}' in a simple and clear way for a school student."
            inputs = explain_tokenizer(input_text, return_tensors="pt")

            outputs = explain_model.generate(
                **inputs,
                max_new_tokens=150,
                temperature=0.7,
                top_k=50,
                top_p=0.95,
                do_sample=True
            )

            explanation = explain_tokenizer.decode(outputs[0], skip_special_tokens=True)
            return explanation
        except Exception as e:
            print(f"Local inference failed ({e}), falling back to Gemini.")
            return _explain_with_gemini(topic)
    else:
        return _explain_with_gemini(topic)
