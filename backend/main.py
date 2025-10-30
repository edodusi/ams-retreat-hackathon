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
from typing import Dict, List, Any

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
import hashlib

# In-memory storage for conversation context (in production, use Redis or similar)
conversation_contexts: Dict[str, List[Dict[str, Any]]] = {}
# Store conversation ID mapping for better tracking
conversation_id_contexts: Dict[str, List[Dict[str, Any]]] = {}
# Store analysis results per session
conversation_analyses: Dict[str, Dict[str, Any]] = {}

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
        
        # Generate a stable session key based on FIRST user message
        # This ensures the key remains consistent across the entire conversation
        if conversation_history:
            # Use only the FIRST user message to create a stable session ID
            user_messages = [msg.content for msg in conversation_history if msg.role == "user"]
            if user_messages:
                # Hash only the first user message to keep session stable
                session_key = hashlib.md5(user_messages[0].encode()).hexdigest()
            else:
                session_key = "default"
        else:
            # First request - use the current message as session key
            session_key = hashlib.md5(request.message.encode()).hexdigest()
        
        logger.info(f">>> Session key: {session_key}")
        logger.info(f">>> Conversation history messages: {len(conversation_history)}")
        
        # Extract previous results and analysis from session context
        previous_results = None
        previous_analysis = None
        if session_key in conversation_contexts and conversation_contexts[session_key]:
            previous_results = conversation_contexts[session_key]
            logger.info(f">>> Found {len(previous_results)} previous results in session context")
        else:
            logger.info(f">>> No previous results found for session: {session_key}")
            logger.info(f">>> Available sessions: {list(conversation_contexts.keys())}")
        
        if session_key in conversation_analyses and conversation_analyses[session_key]:
            previous_analysis = conversation_analyses[session_key]
            logger.info(f">>> Found previous analysis in session: {previous_analysis.get('description', 'Unknown')}")
        
        # Send message to Claude (run sync boto3 call in thread pool)
        try:
            loop = asyncio.get_event_loop()
            claude_response = await loop.run_in_executor(
                executor,
                lambda: bedrock_client.converse(
                    message=request.message,
                    conversation_history=conversation_history,
                    previous_results=previous_results,
                    previous_analysis=previous_analysis
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
        filter_term = claude_response.get("filter_term")
        search_limit = claude_response.get("limit", 10)  # Default to 10 if not specified
        content_type = claude_response.get("content_type")
        analysis_type = claude_response.get("analysis_type")
        clarify_field = claude_response.get("clarify_field")
        clarify_options = claude_response.get("options")
        
        logger.info(f"Claude response - Action: {action}, Term: {search_term}, Filter: {filter_term}, Limit: {search_limit}, ContentType: {content_type}, Message length: {len(response_text)}")
        
        # Initialize response
        conversation_response = ConversationResponse(
            message=response_text,
            results=None,
            action=action
        )
        
        # Handle different action types
        if action == "clarify":
            # Ask for clarification - no search needed
            logger.info(f">>> CLARIFICATION NEEDED: {clarify_field}")
            conversation_response.message = response_text
            # Don't clear context, keep previous results available
            
        elif action == "analyze" and search_term:
            # Perform search but present as analysis
            logger.info(f">>> ANALYZING with term: '{search_term}', type: '{content_type}'")
            try:
                search_results = await storyblok_client.search(term=search_term, limit=100)
                logger.info(f">>> ANALYSIS FOUND {len(search_results.stories)} stories (total: {search_results.total})")
                
                # Note: Full story fetching disabled - requires CDN API token
                # Content type filtering will be skipped if full stories can't be fetched
                logger.info(f">>> Skipping full story fetch for analysis (requires CDN API access)")
                
                # Filter by content_type if specified AND if stories have content_type populated
                if content_type and search_results.stories:
                    # Check if any stories have content_type populated
                    stories_with_type = [s for s in search_results.stories if s.content_type]
                    if stories_with_type:
                        initial_count = len(search_results.stories)
                        logger.info(f">>> Filtering {initial_count} stories by content_type: {content_type}")
                        filtered_stories = [
                            s for s in search_results.stories 
                            if s.content_type and content_type.lower() in s.content_type.lower()
                        ]
                        search_results.stories = filtered_stories
                        logger.info(f">>> After content_type filter: {len(filtered_stories)} stories remain")
                    else:
                        logger.warning(f">>> Cannot filter by content_type: no stories have content_type populated")
                        logger.warning(f">>> Returning all {len(search_results.stories)} stories without content_type filtering")
                
                # Store results for potential listing later
                results_for_context = [story.dict() for story in search_results.stories]
                conversation_contexts[session_key] = results_for_context
                
                # Store analysis data
                analysis_data = {
                    "description": f"Analyzed {search_term}" + (f" ({content_type})" if content_type else ""),
                    "count": len(search_results.stories),
                    "search_term": search_term,
                    "content_type": content_type,
                    "analysis_type": analysis_type or "count"
                }
                conversation_analyses[session_key] = analysis_data
                conversation_response.analysis = analysis_data
                
                # Provide conversational response with count
                count = len(search_results.stories)
                if count > 0:
                    type_str = f"{content_type}s" if content_type else "stories"
                    conversation_response.message = f"I found {count} {type_str} that mention {search_term}. Would you like me to list them?"
                    logger.info(f">>> ANALYSIS COMPLETE: {count} results stored for potential listing")
                else:
                    conversation_response.message = f"I couldn't find any {content_type if content_type else 'stories'} that mention {search_term}."
                    conversation_contexts[session_key] = []
                    
            except Exception as e:
                logger.error(f">>> ANALYSIS ERROR: {str(e)}", exc_info=True)
                conversation_response.message += "\n\nI encountered an issue analyzing the content. Please try again."
        
        elif action == "list_analyzed":
            # List the previously analyzed results with optional limit
            logger.info(f">>> LISTING ANALYZED RESULTS for session: {session_key}, limit: {search_limit}")
            if previous_results and len(previous_results) > 0:
                from backend.models import StoryResult, SearchResults
                
                # Apply limit if specified by user
                results_to_show = previous_results[:search_limit] if search_limit else previous_results
                
                story_results = []
                for story_dict in results_to_show:
                    story_results.append(StoryResult(**story_dict))
                
                conversation_response.results = SearchResults(
                    stories=story_results,
                    total=len(story_results)
                )
                logger.info(f">>> LISTED {len(story_results)} of {len(previous_results)} analyzed stories (limit applied: {search_limit})")
            else:
                conversation_response.message = "I don't have any analyzed results to show. Please ask me to search or analyze first."
                logger.warning(f">>> No analyzed results to list for session: {session_key}")
        
        elif action == "search" and search_term:
            logger.info(f">>> PERFORMING SEARCH with term: '{search_term}', limit: {search_limit}, type: '{content_type}'")
            try:
                search_results = await storyblok_client.search(term=search_term, limit=search_limit)
                logger.info(f">>> SEARCH RETURNED {len(search_results.stories)} stories (total: {search_results.total})")
                
                # Note: Full story fetching disabled - requires CDN API token
                # Stories will be returned with basic info from vsearch API only
                logger.info(f">>> Returning {len(search_results.stories)} stories with basic info (full story fetch disabled)")
                
                # Filter by content_type if specified AND if stories have content_type populated
                if content_type and search_results.stories:
                    # Check if any stories have content_type populated
                    stories_with_type = [s for s in search_results.stories if s.content_type]
                    if stories_with_type:
                        initial_count = len(search_results.stories)
                        logger.info(f">>> Filtering {initial_count} stories by content_type: {content_type}")
                        filtered_stories = [
                            s for s in search_results.stories 
                            if s.content_type and content_type.lower() in s.content_type.lower()
                        ]
                        search_results.stories = filtered_stories
                        search_results.total = len(filtered_stories)
                        logger.info(f">>> After content_type filter: {len(filtered_stories)} stories remain")
                    else:
                        logger.warning(f">>> Cannot filter by content_type: no stories have content_type populated")
                        logger.warning(f">>> Returning all {len(search_results.stories)} stories without content_type filtering")
                
                conversation_response.results = search_results
                logger.info(f">>> RESULTS ATTACHED TO RESPONSE: {len(search_results.stories)} stories")
                
                # Store results in session context for future refinement
                results_for_context = [story.dict() for story in search_results.stories]
                conversation_contexts[session_key] = results_for_context
                logger.info(f">>> Stored {len(results_for_context)} stories in session '{session_key}' for refinement")
                logger.info(f">>> Session contexts now has {len(conversation_contexts)} sessions")
                
                # Enhance response message with result count
                result_count = search_results.total
                if result_count > 0:
                    logger.info(f">>> SUCCESS: Found {result_count} results with full previews")
                else:
                    logger.info("No results found")
                    conversation_response.message += "\n\nI couldn't find any matching content. Would you like to try a different search?"
                    # Clear context if no results
                    conversation_contexts[session_key] = []
                    
            except Exception as e:
                logger.error(f">>> STORYBLOK SEARCH ERROR: {str(e)}", exc_info=True)
                conversation_response.message += "\n\nI encountered an issue searching for content. Please try again."
        
        elif action == "refine" and filter_term:
            logger.info(f">>> REFINING PREVIOUS RESULTS with filter: '{filter_term}'")
            logger.info(f">>> Current session key: {session_key}")
            logger.info(f">>> Has previous results: {previous_results is not None}")
            
            if previous_results and len(previous_results) > 0:
                # Filter results based on the filter term
                filtered_stories = []
                filter_lower = filter_term.lower()
                
                logger.info(f">>> Filtering {len(previous_results)} stories for term: '{filter_term}'")
                
                for story_dict in previous_results:
                    # Search in story name, body, and slug
                    searchable_text = f"{story_dict.get('name', '')} {story_dict.get('body', '')} {story_dict.get('slug', '')}".lower()
                    
                    if filter_lower in searchable_text:
                        filtered_stories.append(story_dict)
                        logger.debug(f">>> Match found: {story_dict.get('name', '')}")
                
                logger.info(f">>> Filtered from {len(previous_results)} to {len(filtered_stories)} stories")
                
                if filtered_stories:
                    # Convert back to StoryResult objects
                    from backend.models import StoryResult, SearchResults
                    story_results = []
                    for story_dict in filtered_stories:
                        story_results.append(StoryResult(**story_dict))
                    
                    conversation_response.results = SearchResults(
                        stories=story_results,
                        total=len(story_results)
                    )
                    
                    # Update session context with refined results
                    conversation_contexts[session_key] = filtered_stories
                    
                    logger.info(f">>> REFINEMENT SUCCESSFUL: Returning {len(filtered_stories)} filtered stories")
                else:
                    conversation_response.message = "I couldn't find any stories matching that criteria in the previous results."
                    logger.info(">>> No stories matched the filter criteria")
            else:
                logger.warning(f">>> Refine action detected but no previous results available for session: {session_key}")
                logger.warning(f">>> All stored sessions: {list(conversation_contexts.keys())}")
                conversation_response.message = "I don't have access to previous results. Please start with a search first."
        
        else:
            if action == "search" and not search_term:
                logger.warning(f">>> Search action requested but no search term provided!")
            logger.info(f">>> NO SEARCH PERFORMED - Action: {action}, Has term: {bool(search_term)}, Filter: {bool(filter_term)}")
        
        logger.info(f">>> FINAL RESPONSE: message length={len(conversation_response.message)}, has_results={conversation_response.results is not None}")
        if conversation_response.results:
            logger.info(f">>> RETURNING {len(conversation_response.results.stories)} stories in response")
            logger.info(f">>> Results object type: {type(conversation_response.results)}")
            logger.info(f">>> Results.stories type: {type(conversation_response.results.stories)}")
            if conversation_response.results.stories:
                logger.info(f">>> First story sample: {conversation_response.results.stories[0].dict()}")
        
        # Serialize to dict to verify JSON structure
        response_dict = conversation_response.dict()
        logger.info(f">>> Serialized response keys: {response_dict.keys()}")
        if response_dict.get('results'):
            logger.info(f">>> Serialized results keys: {response_dict['results'].keys()}")
            logger.info(f">>> Serialized stories count: {len(response_dict['results'].get('stories', []))}")
            if response_dict['results'].get('stories'):
                logger.info(f">>> First serialized story keys: {response_dict['results']['stories'][0].keys()}")
        
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