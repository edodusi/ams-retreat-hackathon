"""
Pydantic models for request/response validation.
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class Message(BaseModel):
    """A single message in the conversation."""
    role: Literal["user", "assistant"]
    content: str


class ConversationRequest(BaseModel):
    """Request model for conversation endpoint."""
    message: str = Field(..., description="User's message/query", min_length=1)
    conversation_history: List[Message] = Field(
        default_factory=list,
        description="Previous conversation messages for context"
    )


class StoryResult(BaseModel):
    """A single story result from Storyblok Strata API."""
    body: str = Field(..., description="Story body/content as text")
    cursor: int = Field(..., description="Cursor for pagination")
    name: str = Field(..., description="Story name")
    slug: str = Field(..., description="Story slug/path")
    story_id: int = Field(..., description="Story ID")
    
    # Additional fields for full story details (when fetched)
    full_story: Optional[dict] = Field(None, description="Full story data from Storyblok API")


class SearchResults(BaseModel):
    """Search results from Storyblok Strata."""
    stories: List[StoryResult] = Field(default_factory=list)
    total: int = Field(0, description="Total number of results")


class ConversationResponse(BaseModel):
    """Response model for conversation endpoint."""
    message: str = Field(..., description="Assistant's response message")
    results: Optional[SearchResults] = Field(None, description="Search results if applicable")
    conversation_id: Optional[str] = Field(None, description="Conversation session ID")


class HealthCheck(BaseModel):
    """Health check response."""
    status: str = Field(default="healthy")
    service: str = Field(default="Storyblok Voice Assistant")
    version: str = Field(default="1.0.0")


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    status_code: int = Field(..., description="HTTP status code")