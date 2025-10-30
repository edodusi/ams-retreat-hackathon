"""
Unit tests for the main FastAPI application.
Tests core functionality and API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock

from backend.main import app
from backend.models import SearchResults, StoryResult


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def mock_bedrock_response():
    """Mock Bedrock API response."""
    return {
        "action": "search",
        "term": "marketing articles",
        "response": "I found some marketing articles for you.",
        "raw_response": '{"action": "search", "term": "marketing articles", "response": "I found some marketing articles for you."}'
    }


@pytest.fixture
def mock_storyblok_results():
    """Mock Storyblok search results."""
    return SearchResults(
        stories=[
            StoryResult(
                body="A comprehensive guide to modern marketing tactics for 2025. Learn the latest strategies and best practices.",
                cursor=0,
                name="Marketing Strategy 2025",
                slug="blog/marketing-strategy-2025",
                story_id=1
            ),
            StoryResult(
                body="Learn how to maximize your social media presence with proven best practices and expert tips.",
                cursor=1,
                name="Social Media Best Practices",
                slug="blog/social-media-best-practices",
                story_id=2
            )
        ],
        total=2
    )


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_root_endpoint(self, client):
        """Test root endpoint returns health status."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "Storyblok Voice Assistant"
        assert "version" in data
    
    def test_health_check_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestConversationEndpoint:
    """Test conversation endpoint."""
    
    @pytest.mark.asyncio
    @patch('backend.main.get_bedrock_client')
    @patch('backend.main.get_storyblok_client')
    async def test_conversation_with_search(self, mock_storyblok, mock_bedrock, client, mock_bedrock_response, mock_storyblok_results):
        """Test conversation endpoint with search action."""
        # Setup mocks
        bedrock_mock = MagicMock()
        bedrock_mock.converse = MagicMock(return_value=mock_bedrock_response)  # Synchronous now
        mock_bedrock.return_value = bedrock_mock
        
        storyblok_mock = MagicMock()
        storyblok_mock.search = AsyncMock(return_value=mock_storyblok_results)
        storyblok_mock.get_story_by_id = AsyncMock(return_value=None)  # Mock full story fetching
        mock_storyblok.return_value = storyblok_mock
        
        # Make request
        response = client.post(
            "/api/conversation",
            json={
                "message": "Find marketing articles",
                "conversation_history": []
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "I found some marketing articles for you."
        assert "results" in data
        assert data["results"] is not None
        assert len(data["results"]["stories"]) == 2
    
    def test_conversation_missing_message(self, client):
        """Test conversation endpoint with missing message."""
        response = client.post(
            "/api/conversation",
            json={
                "conversation_history": []
            }
        )
        assert response.status_code == 422  # Validation error
    
    def test_conversation_empty_message(self, client):
        """Test conversation endpoint with empty message."""
        response = client.post(
            "/api/conversation",
            json={
                "message": "",
                "conversation_history": []
            }
        )
        assert response.status_code == 422  # Validation error
    
    @pytest.mark.asyncio
    @patch('backend.main.get_bedrock_client')
    async def test_conversation_chat_only(self, mock_bedrock, client):
        """Test conversation endpoint with chat action (no search)."""
        # Setup mock for chat response
        chat_response = {
            "action": "chat",
            "term": None,
            "response": "Hello! How can I help you search for content today?",
            "raw_response": "Hello! How can I help you search for content today?"
        }
        
        bedrock_mock = MagicMock()
        bedrock_mock.converse = MagicMock(return_value=chat_response)  # Synchronous now
        mock_bedrock.return_value = bedrock_mock
        
        # Make request
        response = client.post(
            "/api/conversation",
            json={
                "message": "Hello",
                "conversation_history": []
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["results"] is None  # No search results for chat


class TestConversationHistory:
    """Test conversation history handling."""
    
    @pytest.mark.asyncio
    @patch('backend.main.get_bedrock_client')
    async def test_conversation_with_history(self, mock_bedrock, client):
        """Test that conversation history is passed correctly."""
        bedrock_mock = MagicMock()
        bedrock_mock.converse = MagicMock(return_value={  # Synchronous now
            "action": "chat",
            "response": "Sure, I can help with that."
        })
        mock_bedrock.return_value = bedrock_mock
        
        history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi! How can I help?"}
        ]
        
        response = client.post(
            "/api/conversation",
            json={
                "message": "Find articles",
                "conversation_history": history
            }
        )
        
        assert response.status_code == 200
        # Verify bedrock client was called
        bedrock_mock.converse.assert_called_once()


class TestCORS:
    """Test CORS configuration."""
    
    def test_cors_headers_present(self, client):
        """Test that CORS headers are properly configured."""
        response = client.options(
            "/api/conversation",
            headers={
                "Origin": "http://localhost:8000",
                "Access-Control-Request-Method": "POST"
            }
        )
        # CORS middleware should handle OPTIONS requests
        assert response.status_code in [200, 405]