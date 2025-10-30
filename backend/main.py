"""
Main FastAPI application for Storyblok Voice Assistant.
Provides endpoints for conversation and health checks.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import asyncio
from concurrent.futures import ThreadPoolExecutor

from backend.config import get_settings
from backend.models import (
    ConversationRequest,
    ConversationResponse,
    HealthCheck,
    ErrorResponse,
    Message
)
from backend.bedrock_client import get_bedrock_client
from backend.storyblok_client import get_storyblok_client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Thread pool for running sync boto3 calls
executor = ThreadPoolExecutor(max_workers=10)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    logger.info("Starting Storyblok Voice Assistant...")
    settings = get_settings()
    logger.info(f"Environment: {'Debug' if settings.debug else 'Production'}")
    logger.info(f"AWS Region: {settings.aws_region}")
    logger.info(f"Bedrock Model: {settings.bedrock_model_id}")
    yield
    logger.info("Shutting down Storyblok Voice Assistant...")


# Create FastAPI app
app = FastAPI(
    title="Storyblok Voice Assistant API",
    description="Voice-enabled content discovery for Storyblok using AWS Bedrock",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for frontend
app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unexpected errors."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.debug else "An unexpected error occurred",
            "status_code": 500
        }
    )


@app.get("/", response_model=HealthCheck, tags=["Health"])
async def root():
    """Root endpoint with basic service information."""
    return HealthCheck(
        status="healthy",
        service="Storyblok Voice Assistant",
        version="1.0.0"
    )


@app.get("/health", response_model=HealthCheck, tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return HealthCheck(
        status="healthy",
        service="Storyblok Voice Assistant",
        version="1.0.0"
    )


@app.post(
    "/api/conversation",
    response_model=ConversationResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    tags=["Conversation"]
)
async def conversation(request: ConversationRequest):
    """
    Main conversation endpoint.
    Processes user messages, interacts with Claude, and performs Storyblok searches.
    
    Args:
        request: ConversationRequest with message and conversation history
        
    Returns:
        ConversationResponse with assistant's message and search results
    """
    try:
        logger.info(f"Received conversation request: '{request.message[:50]}...'")
        
        # Get clients
        bedrock_client = get_bedrock_client()
        storyblok_client = get_storyblok_client()
        
        # Limit conversation history to prevent token overflow
        max_history = settings.max_conversation_history
        conversation_history = request.conversation_history[-max_history:] if request.conversation_history else []
        
        # Send message to Claude (run sync boto3 call in thread pool)
        try:
            loop = asyncio.get_event_loop()
            claude_response = await loop.run_in_executor(
                executor,
                lambda: bedrock_client.converse(
                    message=request.message,
                    conversation_history=conversation_history
                )
            )
        except Exception as e:
            logger.error(f"Bedrock client error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Unable to connect to AI service: {str(e)}"
            )
        
        # Extract action and response
        action = claude_response.get("action", "chat")
        response_text = claude_response.get("response", "")
        search_term = claude_response.get("term")
        
        logger.info(f"Claude response - Action: {action}, Term: {search_term}, Message length: {len(response_text)}")
        
        # Initialize response
        conversation_response = ConversationResponse(
            message=response_text,
            results=None
        )
        
        # If action is search, query Storyblok (async httpx call)
        if action == "search" and search_term:
            logger.info(f">>> PERFORMING SEARCH with term: '{search_term}'")
            try:
                search_results = await storyblok_client.search(term=search_term)
                logger.info(f">>> SEARCH RETURNED {len(search_results.stories)} stories (total: {search_results.total})")
                
                # Fetch full story details for each result to provide better preview
                if search_results.stories:
                    logger.info(f">>> Fetching full details for {len(search_results.stories)} stories")
                    for story in search_results.stories:
                        try:
                            full_story = await storyblok_client.get_story_by_id(story.story_id)
                            if full_story:
                                story.full_story = full_story
                                logger.debug(f"Fetched full story for ID {story.story_id}")
                        except Exception as e:
                            logger.warning(f"Could not fetch full story for ID {story.story_id}: {e}")
                            # Continue without full story data
                
                conversation_response.results = search_results
                logger.info(f">>> RESULTS ATTACHED TO RESPONSE: {len(search_results.stories)} stories")
                
                # Enhance response message with result count
                result_count = search_results.total
                if result_count > 0:
                    logger.info(f">>> SUCCESS: Found {result_count} results with full previews")
                else:
                    logger.info("No results found")
                    conversation_response.message += "\n\nI couldn't find any matching content. Would you like to try a different search?"
                    
            except Exception as e:
                logger.error(f">>> STORYBLOK SEARCH ERROR: {str(e)}", exc_info=True)
                conversation_response.message += "\n\nI encountered an issue searching for content. Please try again."
        else:
            if action == "search" and not search_term:
                logger.warning(f">>> Search action requested but no search term provided!")
            logger.info(f">>> NO SEARCH PERFORMED - Action: {action}, Has term: {bool(search_term)}")
        
        logger.info(f">>> FINAL RESPONSE: message length={len(conversation_response.message)}, has_results={conversation_response.results is not None}")
        if conversation_response.results:
            logger.info(f">>> RETURNING {len(conversation_response.results.stories)} stories in response")
        
        return conversation_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing conversation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing conversation: {str(e)}"
        )


@app.get("/api/test-bedrock", tags=["Debug"])
async def test_bedrock():
    """Test endpoint for Bedrock connection (debug only)."""
    if not settings.debug:
        raise HTTPException(status_code=404, detail="Not found")
    
    try:
        bedrock_client = get_bedrock_client()
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            executor,
            lambda: bedrock_client.converse(
                message="Hello, can you help me search for content?",
                conversation_history=[]
            )
        )
        return {"status": "success", "response": response}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@app.get("/api/test-storyblok", tags=["Debug"])
async def test_storyblok(term: str = "test"):
    """Test endpoint for Storyblok connection (debug only)."""
    if not settings.debug:
        raise HTTPException(status_code=404, detail="Not found")
    
    try:
        storyblok_client = get_storyblok_client()
        results = await storyblok_client.search(term=term)
        return {"status": "success", "results": results}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@app.get("/api/story/{story_id}", tags=["Stories"])
async def get_full_story(story_id: int):
    """
    Fetch full story details by ID.
    
    Args:
        story_id: The Storyblok story ID
        
    Returns:
        Full story data including content, metadata, etc.
    """
    try:
        logger.info(f"Fetching full story for ID: {story_id}")
        storyblok_client = get_storyblok_client()
        story_data = await storyblok_client.get_story_by_id(story_id)
        
        if story_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Story with ID {story_id} not found"
            )
        
        return {"status": "success", "story": story_data}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching story {story_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching story: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )