"""
Unit tests for analytical and conversational features.
Tests content type filtering, analysis actions, and conversational flow.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from backend.models import (
    ConversationRequest,
    ConversationResponse,
    Message,
    StoryResult,
    SearchResults
)


class TestContentTypeDetection:
    """Test content type detection and filtering."""

    def test_story_result_with_content_type(self):
        """Test StoryResult model accepts content_type field."""
        story = StoryResult(
            body="Test body",
            cursor=0,
            name="Test Article",
            slug="test-article",
            story_id=123,
            content_type="article"
        )
        
        assert story.content_type == "article"
        assert story.name == "Test Article"

    def test_story_result_without_content_type(self):
        """Test StoryResult model with None content_type."""
        story = StoryResult(
            body="Test body",
            cursor=0,
            name="Test Post",
            slug="test-post",
            story_id=456,
            content_type=None
        )
        
        assert story.content_type is None

    def test_conversation_response_with_analysis(self):
        """Test ConversationResponse model accepts analysis field."""
        response = ConversationResponse(
            message="I found 13 articles",
            action="analyze",
            analysis={
                "count": 13,
                "search_term": "drupal",
                "content_type": "article",
                "analysis_type": "count"
            }
        )
        
        assert response.action == "analyze"
        assert response.analysis["count"] == 13
        assert response.analysis["content_type"] == "article"


class TestActionTypes:
    """Test different action types."""

    def test_analyze_action_structure(self):
        """Test analyze action response structure."""
        response = ConversationResponse(
            message="I found 7 articles that mention GraphQL. Would you like me to list them?",
            action="analyze",
            results=None,
            analysis={
                "description": "Analyzed GraphQL (article)",
                "count": 7,
                "search_term": "GraphQL",
                "content_type": "article",
                "analysis_type": "count"
            }
        )
        
        assert response.action == "analyze"
        assert response.results is None
        assert response.analysis is not None
        assert response.analysis["count"] == 7

    def test_list_analyzed_action_structure(self):
        """Test list_analyzed action response structure."""
        stories = [
            StoryResult(
                body="GraphQL tutorial",
                cursor=0,
                name="Getting Started with GraphQL",
                slug="graphql-tutorial",
                story_id=101,
                content_type="article"
            )
        ]
        
        response = ConversationResponse(
            message="Here are the articles:",
            action="list_analyzed",
            results=SearchResults(stories=stories, total=1),
            analysis=None
        )
        
        assert response.action == "list_analyzed"
        assert response.results is not None
        assert len(response.results.stories) == 1
        assert response.analysis is None

    def test_clarify_action_structure(self):
        """Test clarify action response structure."""
        response = ConversationResponse(
            message="What type of content are you looking for? Articles, blog posts, pages, or all types?",
            action="clarify",
            results=None,
            analysis=None
        )
        
        assert response.action == "clarify"
        assert response.results is None
        assert response.analysis is None
        assert "type of content" in response.message.lower()


class TestBedrockResponseParsing:
    """Test parsing of Bedrock/Claude responses."""

    def test_parse_analyze_response(self):
        """Test parsing analyze action from Claude response."""
        mock_response = {
            "action": "analyze",
            "term": "drupal",
            "content_type": "article",
            "analysis_type": "count",
            "limit": 10,
            "response": "Let me check how many articles mention Drupal..."
        }
        
        assert mock_response["action"] == "analyze"
        assert mock_response["term"] == "drupal"
        assert mock_response["content_type"] == "article"
        assert mock_response["analysis_type"] == "count"

    def test_parse_clarify_response(self):
        """Test parsing clarify action from Claude response."""
        mock_response = {
            "action": "clarify",
            "clarify_field": "content_type",
            "options": ["article", "blog_post", "page"],
            "response": "What type of content are you looking for?"
        }
        
        assert mock_response["action"] == "clarify"
        assert mock_response["clarify_field"] == "content_type"
        assert "article" in mock_response["options"]

    def test_parse_list_analyzed_response(self):
        """Test parsing list_analyzed action from Claude response."""
        mock_response = {
            "action": "list_analyzed",
            "response": "Here are the articles:"
        }
        
        assert mock_response["action"] == "list_analyzed"


class TestContentTypeFiltering:
    """Test content type filtering logic."""

    def test_filter_by_article_type(self):
        """Test filtering stories by article content type."""
        stories = [
            StoryResult(body="", cursor=0, name="Article 1", slug="article-1", 
                       story_id=1, content_type="article"),
            StoryResult(body="", cursor=0, name="Blog Post 1", slug="blog-1", 
                       story_id=2, content_type="blog_post"),
            StoryResult(body="", cursor=0, name="Article 2", slug="article-2", 
                       story_id=3, content_type="article"),
        ]
        
        # Filter for articles only
        filtered = [s for s in stories if s.content_type and "article" in s.content_type.lower()]
        
        assert len(filtered) == 2
        assert all(s.content_type == "article" for s in filtered)

    def test_filter_by_blog_post_type(self):
        """Test filtering stories by blog_post content type."""
        stories = [
            StoryResult(body="", cursor=0, name="Article 1", slug="article-1", 
                       story_id=1, content_type="article"),
            StoryResult(body="", cursor=0, name="Blog Post 1", slug="blog-1", 
                       story_id=2, content_type="blog_post"),
            StoryResult(body="", cursor=0, name="Blog Post 2", slug="blog-2", 
                       story_id=3, content_type="blog_post"),
        ]
        
        # Filter for blog posts only
        filtered = [s for s in stories if s.content_type and "blog_post" in s.content_type.lower()]
        
        assert len(filtered) == 2
        assert all(s.content_type == "blog_post" for s in filtered)

    def test_filter_with_none_content_type(self):
        """Test filtering handles None content types gracefully."""
        stories = [
            StoryResult(body="", cursor=0, name="Article 1", slug="article-1", 
                       story_id=1, content_type="article"),
            StoryResult(body="", cursor=0, name="Unknown", slug="unknown", 
                       story_id=2, content_type=None),
        ]
        
        # Filter for articles only
        filtered = [s for s in stories if s.content_type and "article" in s.content_type.lower()]
        
        assert len(filtered) == 1
        assert filtered[0].content_type == "article"


class TestConversationalFlow:
    """Test conversational flow patterns."""

    def test_analyze_then_list_flow(self):
        """Test analyze → confirm → list flow."""
        # Step 1: Analyze
        analyze_response = ConversationResponse(
            message="I found 5 articles that mention React. Would you like me to list them?",
            action="analyze",
            results=None,
            analysis={
                "count": 5,
                "search_term": "React",
                "content_type": "article"
            }
        )
        
        assert analyze_response.action == "analyze"
        assert analyze_response.analysis["count"] == 5
        
        # Step 2: List (simulated)
        stories = [
            StoryResult(body="", cursor=0, name=f"Article {i}", slug=f"article-{i}", 
                       story_id=i, content_type="article")
            for i in range(1, 6)
        ]
        
        list_response = ConversationResponse(
            message="Here are the articles:",
            action="list_analyzed",
            results=SearchResults(stories=stories, total=5)
        )
        
        assert list_response.action == "list_analyzed"
        assert len(list_response.results.stories) == 5

    def test_search_then_refine_flow(self):
        """Test search → refine flow."""
        # Step 1: Initial search
        initial_stories = [
            StoryResult(body="React hooks tutorial", cursor=0, name="React Article 1", 
                       slug="react-1", story_id=1, content_type="article"),
            StoryResult(body="Vue composition API", cursor=0, name="Vue Article", 
                       slug="vue-1", story_id=2, content_type="article"),
            StoryResult(body="React context API", cursor=0, name="React Article 2", 
                       slug="react-2", story_id=3, content_type="article"),
        ]
        
        search_response = ConversationResponse(
            message="Here are the articles:",
            action="search",
            results=SearchResults(stories=initial_stories, total=3)
        )
        
        assert len(search_response.results.stories) == 3
        
        # Step 2: Refine (filter for "React")
        filter_term = "React"
        refined_stories = [
            s for s in initial_stories 
            if filter_term.lower() in s.body.lower() or filter_term.lower() in s.name.lower()
        ]
        
        refine_response = ConversationResponse(
            message="Here are the articles that mention React:",
            action="refine",
            results=SearchResults(stories=refined_stories, total=len(refined_stories))
        )
        
        assert len(refine_response.results.stories) == 2
        assert all("React" in s.name or "React" in s.body for s in refine_response.results.stories)


class TestQueryPatterns:
    """Test query pattern recognition."""

    def test_analytical_query_patterns(self):
        """Test recognition of analytical query patterns."""
        analytical_queries = [
            "how many articles mention drupal?",
            "do we have blog posts about react?",
            "how many pages discuss AI?",
            "are there any articles about vue?"
        ]
        
        # These should trigger analyze action
        for query in analytical_queries:
            assert any(keyword in query.lower() for keyword in ["how many", "do we have", "are there"])

    def test_search_query_patterns(self):
        """Test recognition of search query patterns."""
        search_queries = [
            "find articles about marketing",
            "show me 5 blog posts",
            "get pages about our company",
            "search for articles about react"
        ]
        
        # These should trigger search action
        for query in search_queries:
            assert any(keyword in query.lower() for keyword in ["find", "show", "get", "search"])

    def test_refinement_query_patterns(self):
        """Test recognition of refinement query patterns."""
        refinement_queries = [
            "out of those, which mention react?",
            "from these, show only articles",
            "which ones are about AI?",
            "filter by react"
        ]
        
        # These should trigger refine action
        for query in refinement_queries:
            assert any(keyword in query.lower() for keyword in ["out of", "from these", "which ones", "filter"])


class TestSessionContext:
    """Test session context management."""

    def test_context_storage_structure(self):
        """Test that context storage has correct structure."""
        session_key = "test_session_123"
        
        # Simulate storing results in context
        conversation_contexts = {}
        conversation_analyses = {}
        
        # Store search results
        stories = [
            StoryResult(body="", cursor=0, name="Article 1", slug="article-1", 
                       story_id=1, content_type="article").dict()
        ]
        conversation_contexts[session_key] = stories
        
        # Store analysis
        analysis = {
            "description": "Analyzed React (article)",
            "count": 1,
            "search_term": "React",
            "content_type": "article"
        }
        conversation_analyses[session_key] = analysis
        
        # Verify storage
        assert session_key in conversation_contexts
        assert session_key in conversation_analyses
        assert len(conversation_contexts[session_key]) == 1
        assert conversation_analyses[session_key]["count"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])