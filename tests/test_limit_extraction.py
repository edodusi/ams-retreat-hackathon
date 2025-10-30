"""
Test limit extraction from user queries.
Tests that Claude correctly parses the number of results requested by users.
"""

import pytest
from backend.bedrock_client import BedrockClient
from backend.models import Message


class TestLimitExtraction:
    """Test cases for limit extraction from user queries."""
    
    def setup_method(self):
        """Setup test fixtures."""
        try:
            self.client = BedrockClient()
        except Exception as e:
            pytest.skip(f"Could not initialize Bedrock client: {e}")
    
    def test_explicit_limit_five(self):
        """Test extraction of limit when user asks for 5 results."""
        message = "find the first 5 articles about marketing"
        
        response = self.client.converse(message=message, conversation_history=[])
        
        assert response["action"] == "search"
        assert response["limit"] == 5
        assert "marketing" in response["term"].lower()
    
    def test_explicit_limit_three(self):
        """Test extraction of limit when user asks for 3 results."""
        message = "show me 3 blog posts about technology"
        
        response = self.client.converse(message=message, conversation_history=[])
        
        assert response["action"] == "search"
        assert response["limit"] == 3
        assert "blog" in response["term"].lower() or "technology" in response["term"].lower()
    
    def test_explicit_limit_twenty(self):
        """Test extraction of limit when user asks for 20 results."""
        message = "get 20 stories about design"
        
        response = self.client.converse(message=message, conversation_history=[])
        
        assert response["action"] == "search"
        assert response["limit"] == 20
        assert "design" in response["term"].lower() or "stories" in response["term"].lower()
    
    def test_default_limit(self):
        """Test that default limit of 10 is used when not specified."""
        message = "find marketing articles"
        
        response = self.client.converse(message=message, conversation_history=[])
        
        assert response["action"] == "search"
        assert response["limit"] == 10
        assert "marketing" in response["term"].lower()
    
    def test_top_n_pattern(self):
        """Test extraction when user asks for 'top N' results."""
        message = "show me the top 7 posts about AI"
        
        response = self.client.converse(message=message, conversation_history=[])
        
        assert response["action"] == "search"
        assert response["limit"] == 7
        assert "ai" in response["term"].lower() or "posts" in response["term"].lower()
    
    def test_limit_with_first_keyword(self):
        """Test extraction with 'first' keyword."""
        message = "I need the first 15 blog posts"
        
        response = self.client.converse(message=message, conversation_history=[])
        
        assert response["action"] == "search"
        assert response["limit"] == 15
    
    def test_chat_action_has_default_limit(self):
        """Test that chat actions also have a limit field (default)."""
        message = "Hello, how are you?"
        
        response = self.client.converse(message=message, conversation_history=[])
        
        assert response["action"] == "chat"
        assert response["limit"] == 10  # Should have default even for chat


class TestLimitValidation:
    """Test limit validation and edge cases."""
    
    def test_large_limit(self):
        """Test that large limits are handled correctly."""
        # Note: This test just checks that the value is extracted
        # The actual API limit validation should happen in the Storyblok client
        message = "get 100 articles"
        
        client = BedrockClient()
        response = client.converse(message=message, conversation_history=[])
        
        assert response["action"] == "search"
        # Claude should extract the number even if it's large
        assert isinstance(response["limit"], int)
        assert response["limit"] > 0
    
    def test_single_result(self):
        """Test requesting a single result."""
        message = "find 1 article about productivity"
        
        client = BedrockClient()
        response = client.converse(message=message, conversation_history=[])
        
        assert response["action"] == "search"
        assert response["limit"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])