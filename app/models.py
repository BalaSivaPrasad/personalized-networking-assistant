from pydantic import BaseModel, Field
from typing import List, Optional

class ConversationRequest(BaseModel):
    event_description: str = Field(..., description="Description of the networking event")
    interests: List[str] = Field(..., description="List of user interests")
    bio: Optional[str] = Field(None, description="Optional user biography")

class ConversationResponse(BaseModel):
    themes: List[str] = Field(..., description="Extracted event themes")
    suggestions: List[str] = Field(..., description="Generated conversation starters")
    timestamp: str = Field(..., description="ISO timestamp of generation")

class FactCheckRequest(BaseModel):
    query: str = Field(..., description="Query to fact check against Wikipedia")

class FactCheckResponse(BaseModel):
    query: str = Field(..., description="Original query")
    result: str = Field(..., description="Fact-checked information")
    source_url: Optional[str] = Field(None, description="Wikipedia source URL")

class EventAnalysisRequest(BaseModel):
    event_description: str = Field(..., description="Event description to analyze")

class EventAnalysisResponse(BaseModel):
    themes: List[str] = Field(..., description="Extracted themes")

class FeedbackRequest(BaseModel):
    suggestion: str = Field(..., description="The suggestion being rated")
    action: str = Field(..., description="User action: 'like' or 'dislike'")

class FeedbackResponse(BaseModel):
    status: str
    message: str