import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    app_name: str = os.getenv("APP_NAME", "EduGenie")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
    use_local_explainer: bool = os.getenv("USE_LOCAL_EXPLAINER", "false").lower() in ("true", "1", "yes")
    local_model_name: str = os.getenv("LOCAL_MODEL_NAME", "MBZUAI/LaMini-Flan-T5-783M")
    max_input_chars: int = int(os.getenv("MAX_INPUT_CHARS", "12000"))

settings = Settings()
