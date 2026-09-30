from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from qna import answer_question_with_gemini, answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations
from config import settings

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="EduGenie: Google Gemini Powered Learning Assistant",
    version="1.0.0",
    description="AI-powered educational assistant that simplifies learning through generative AI.",
)

# Static files mounting
static_dir = BASE_DIR / "static"
if not static_dir.exists():
    static_dir.mkdir(parents=True, exist_ok=True)

app.mount(
    "/static",
    StaticFiles(directory=static_dir),
    name="static",
)

# HTML templates
templates_dir = BASE_DIR / "templates"
if not templates_dir.exists():
    templates_dir.mkdir(parents=True, exist_ok=True)

templates = Jinja2Templates(directory=str(templates_dir))


# ---------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"app_name": settings.app_name},
    )


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------
@app.get("/health")
async def health():
    return {
        "status": "ok",
        "app": settings.app_name,
        "gemini_model": settings.gemini_model,
        "gemini_configured": bool(settings.gemini_api_key),
        "local_explainer_enabled": settings.use_local_explainer,
    }


# ---------------------------------------------------------
# Q&A MODULE
# ---------------------------------------------------------
@app.get("/qa")
async def qa_get(question: str = Query(..., description="Question for EduGenie")):
    if not question or not question.strip():
        return JSONResponse(content={"error": "Please provide a question."}, status_code=400)
    answer = answer_question_with_gemini(question)
    return {"question": question, "answer": answer, "result": answer}


@app.post("/qa")
async def qa_post(request: Request):
    try:
        data = await request.json()
    except Exception:
        data = {}
    question = data.get("question") or data.get("text") or data.get("prompt")
    if not question:
        return JSONResponse(content={"error": "Please provide a question."}, status_code=400)
    answer = answer_question_with_gemini(question)
    return {"question": question, "answer": answer, "result": answer}


# ---------------------------------------------------------
# EXPLANATION MODULE
# ---------------------------------------------------------
@app.post("/explain")
@app.post("/explain/")
async def explain_api(request: Request):
    try:
        data = await request.json()
    except Exception:
        data = {}
    topic = data.get("topic") or data.get("text")
    if not topic:
        return JSONResponse(content={"error": "Please provide a topic."}, status_code=400)
    explanation = explain_topic(topic)
    return {"topic": topic, "explanation": explanation, "result": explanation}


@app.get("/explain")
async def explain_get(topic: str = Query(..., description="Topic to explain")):
    if not topic:
        return JSONResponse(content={"error": "Please provide a topic."}, status_code=400)
    explanation = explain_topic(topic)
    return {"topic": topic, "explanation": explanation, "result": explanation}


# ---------------------------------------------------------
# SUMMARIZATION MODULE
# ---------------------------------------------------------
@app.post("/summarize")
@app.post("/summarize/")
async def summarize_api(request: Request):
    try:
        data = await request.json()
    except Exception:
        data = {}
    text = data.get("text") or data.get("paragraph")
    if not text:
        return JSONResponse(content={"error": "Please provide text to summarize."}, status_code=400)
    summary = summarize_text(text)
    return {"summary": summary, "result": summary}


@app.get("/summarize")
async def summarize_get(text: str = Query(..., description="Text to summarize")):
    if not text:
        return JSONResponse(content={"error": "Please provide text to summarize."}, status_code=400)
    summary = summarize_text(text)
    return {"summary": summary, "result": summary}


# ---------------------------------------------------------
# QUIZ GENERATION MODULE
# ---------------------------------------------------------
@app.post("/quiz")
@app.post("/quiz/")
async def quiz_api(request: Request):
    try:
        data = await request.json()
    except Exception:
        data = {}
    text = data.get("text") or data.get("topic")
    if not text:
        return JSONResponse(content={"error": "Please provide text for quiz."}, status_code=400)
    quiz = generate_quiz(text)
    print("Generated quiz:", quiz)  # DEBUG
    return JSONResponse(content={"quiz": quiz})


@app.get("/quiz")
async def quiz_get(text: str = Query(..., description="Passage or topic for quiz")):
    if not text:
        return JSONResponse(content={"error": "Please provide text for quiz."}, status_code=400)
    quiz = generate_quiz(text)
    return JSONResponse(content={"quiz": quiz})


# ---------------------------------------------------------
# LEARNING RECOMMENDATIONS MODULE
# ---------------------------------------------------------
@app.get("/learn/recommendations")
async def learning_recommendation_get(topic: str = Query(..., description="Topic for learning path")):
    if not topic:
        return JSONResponse(content={"error": "Please provide a topic."}, status_code=400)
    recommendation = get_learning_recommendations(topic)
    return {"topic": topic, "recommendation": recommendation, "result": recommendation}


@app.post("/learn/recommendations")
async def learning_recommendation_post(request: Request):
    try:
        data = await request.json()
    except Exception:
        data = {}
    topic = data.get("topic")
    level = data.get("level")
    if not topic:
        return JSONResponse(content={"error": "Please provide a topic."}, status_code=400)
    recommendation = get_learning_recommendations(topic, level=level)
    return {"topic": topic, "recommendation": recommendation, "result": recommendation}