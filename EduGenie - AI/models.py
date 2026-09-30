from typing import List, Optional, Any
from pydantic import BaseModel, Field

class QARequest(BaseModel):
    question: str = Field(..., description="User question for EduGenie")

class ExplainRequest(BaseModel):
    topic: str = Field(..., description="Topic to explain")

class QuizRequest(BaseModel):
    text: str = Field(..., description="Passage or topic for quiz generation")

class SummaryRequest(BaseModel):
    text: str = Field(..., description="Text content to summarize")

class LearningPathRequest(BaseModel):
    topic: str = Field(..., description="Subject or skill for learning path")
    level: Optional[str] = Field(None, description="Optional level e.g. Beginner")

class TextResponse(BaseModel):
    result: str

class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    answer: str

class QuizResponse(BaseModel):
    quiz: List[Any]

class LearningPathResponse(BaseModel):
    topic: str
    recommendation: str
