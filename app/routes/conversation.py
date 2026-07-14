from fastapi import APIRouter, HTTPException
from datetime import datetime
import logging

from app.models import (
    ConversationRequest, ConversationResponse,
    FactCheckRequest, FactCheckResponse,
    EventAnalysisRequest, EventAnalysisResponse,
    FeedbackRequest, FeedbackResponse
)
from app.services.event_analyzer import extract_event_themes
from app.services.topic_generator import generate_topics
from app.services.fact_checker import fact_check
from app.services.history_logger import log_conversation, load_history
from app.services.feedback_logger import log_feedback, load_feedback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/analyze-event", response_model=EventAnalysisResponse)
async def analyze_event(request: EventAnalysisRequest):
    try:
        themes = extract_event_themes(request.event_description)
        return EventAnalysisResponse(themes=themes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-conversation", response_model=ConversationResponse)
async def generate_conversation(request: ConversationRequest):
    try:
        themes = extract_event_themes(request.event_description)
        suggestions = generate_topics(themes, request.interests)
        
        log_conversation({
            "event_description": request.event_description,
            "interests": request.interests,
            "themes": themes,
            "suggestions": suggestions,
            "timestamp": datetime.now().isoformat()
        })
        
        return ConversationResponse(
            themes=themes,
            suggestions=suggestions,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/fact-check", response_model=FactCheckResponse)
async def verify_fact(request: FactCheckRequest):
    try:
        result, source_url = fact_check(request.query)
        return FactCheckResponse(query=request.query, result=result, source_url=source_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest):
    try:
        log_feedback({
            "suggestion": request.suggestion,
            "action": request.action,
            "timestamp": datetime.now().isoformat()
        })
        return FeedbackResponse(status="success", message="Feedback logged")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
async def get_history():
    return {"history": load_history()}

@router.get("/feedback-history")
async def get_feedback_history():
    return {"feedback": load_feedback()}