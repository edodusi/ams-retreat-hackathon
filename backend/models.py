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
    """A single story result from Storyblok."""
    id: Optional[int] = Field(None, description="Story ID")
    name: str = Field(..., description="Story name")
    full_slug: str = Field(..., description="Full slug/path of the story")
    content: Optional[dict] = Field(None, description="Story content")
    created_at: Optional[str] = Field(None, description="Creation timestamp")
    published_at: Optional[str] = Field(None, description="Publication timestamp")
    first_published_at: Optional[str] = Field(None, description="First publication timestamp")
    
    # Fields for display
    title: Optional[str] = Field(None, description="Display title")
    description: Optional[str] = Field(None, description="Brief description")


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