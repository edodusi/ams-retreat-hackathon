"""
Storyblok Strata client for content search.
Handles semantic search via the vsearches endpoint.
"""

import httpx
import logging
from typing import List, Dict, Any, Optional
from backend.config import get_settings
from backend.models import StoryResult, SearchResults

logger = logging.getLogger(__name__)


class StoryblokClient:
    """Client for Storyblok Strata API."""
    
    def __init__(self):
        self.settings = get_settings()
        self.base_url = self.settings.storyblok_api_base
        self.space_id = self.settings.storyblok_space_id
        self.token = self.settings.storyblok_token
        self.timeout = self.settings.request_timeout
        
    def _build_headers(self) -> Dict[str, str]:
        """Build request headers with authorization."""
        return {
            "Content-Type": "application/json",
            "Authorization": self.token
        }
    
    def _extract_story_info(self, story_data: Dict[str, Any]) -> StoryResult:
        """
        Extract and format story information for display.
        
        Args:
            story_data: Raw story data from Storyblok API
            
        Returns:
            StoryResult with formatted information
        """
        # Extract basic fields
        story = StoryResult(
            id=story_data.get("id"),
            name=story_data.get("name", ""),
            full_slug=story_data.get("full_slug", ""),
            content=story_data.get("content"),
            created_at=story_data.get("created_at"),
            published_at=story_data.get("published_at"),
            first_published_at=story_data.get("first_published_at")
        )
        
        # Try to extract title and description from content
        content = story_data.get("content", {})
        if content:
            # Try common title fields
            story.title = (
                content.get("title") or
                content.get("headline") or
                content.get("name") or
                story_data.get("name")
            )
            
            # Try common description fields
            story.description = (
                content.get("description") or
                content.get("intro") or
                content.get("summary") or
                content.get("excerpt") or
                content.get("teaser")
            )
            
            # Truncate description if too long
            if story.description and len(story.description) > 200:
                story.description = story.description[:197] + "..."
        else:
            story.title = story_data.get("name")
            story.description = f"Story from {story_data.get('full_slug', 'Storyblok')}"
        
        return story
    
    async def search(
        self,
        term: str,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> SearchResults:
        """
        Perform semantic search using Storyblok Strata.
        
        Args:
            term: Search term/query
            limit: Maximum number of results (defaults to settings)
            offset: Pagination offset
            
        Returns:
            SearchResults containing found stories
            
        Raises:
            httpx.HTTPError: If the API request fails
        """
        if limit is None:
            limit = self.settings.default_search_limit
        
        url = f"{self.base_url}/v1/spaces/{self.space_id}/vsearches"
        headers = self._build_headers()
        params = {
            "term": term,
            "limit": limit,
            "offset": offset
        }
        
        logger.info(f"Searching Storyblok for: '{term}' (limit={limit}, offset={offset})")
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(url, headers=headers, params=params)
                response.raise_for_status()
                
                data = response.json()
                
                # Handle both list and dict responses
                if isinstance(data, list):
                    # API returned list directly
                    stories_data = data
                    logger.info(f"Received {len(stories_data)} results from Storyblok (list format)")
                elif isinstance(data, dict):
                    # API returned dict with 'stories' key
                    stories_data = data.get("stories", [])
                    logger.info(f"Received {len(stories_data)} results from Storyblok (dict format)")
                else:
                    logger.error(f"Unexpected response format: {type(data)}")
                    stories_data = []
                
                # Extract stories
                stories = [self._extract_story_info(story) for story in stories_data]
                
                return SearchResults(
                    stories=stories,
                    total=len(stories)
                )
                
            except httpx.HTTPError as e:
                logger.error(f"Storyblok API error: {str(e)}")
                if hasattr(e, 'response') and e.response is not None:
                    logger.error(f"Response status: {e.response.status_code}")
                    logger.error(f"Response body: {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Unexpected error in Storyblok client: {str(e)}")
                raise


# Singleton instance
_storyblok_client: Optional[StoryblokClient] = None


def get_storyblok_client() -> StoryblokClient:
    """Get or create the Storyblok client singleton."""
    global _storyblok_client
    if _storyblok_client is None:
        _storyblok_client = StoryblokClient()
    return _storyblok_client