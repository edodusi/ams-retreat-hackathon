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
        Extract and format story information from Strata API response.

        Args:
            story_data: Raw story data from Storyblok Strata API

        Returns:
            StoryResult with formatted information
        """
        story = StoryResult(
            body=story_data.get("body", ""),
            cursor=story_data.get("cursor", 0),
            name=story_data.get("name", ""),
            slug=story_data.get("slug", ""),
            story_id=story_data.get("story_id", 0)
        )

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
                    # API returned dict with 'stories' key or other nested structure
                    stories_data = data.get("stories", data.get("results", []))
                    logger.info(f"Received {len(stories_data)} results from Storyblok (dict format)")
                else:
                    logger.error(f"Unexpected response format: {type(data)}")
                    stories_data = []

                # Extract stories with new schema
                stories = []
                for story_data in stories_data:
                    try:
                        story = self._extract_story_info(story_data)
                        stories.append(story)
                    except Exception as e:
                        logger.warning(f"Failed to parse story: {e}. Data: {story_data}")
                        continue

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

    async def get_story_by_id(self, story_id: int) -> Optional[dict]:
        """
        Fetch full story details by ID from Storyblok API.

        Args:
            story_id: The story ID to fetch
            
        Returns:
            Full story data as dict, or None if not found
            
        Raises:
            httpx.HTTPError: If the API request fails
        """
        # Use the Content Delivery API to fetch full story
        url = f"{self.base_url}/v2/cdn/stories/{story_id}"
        headers = self._build_headers()
        
        logger.info(f"Fetching full story details for ID: {story_id}")
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                
                data = response.json()
                story_data = data.get("story") if isinstance(data, dict) else None
                
                if story_data:
                    logger.info(f"Successfully fetched story {story_id}")
                    return story_data
                else:
                    logger.warning(f"No story data found for ID {story_id}")
                    return None
                    
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    logger.warning(f"Story {story_id} not found")
                    return None
                logger.error(f"HTTP error fetching story {story_id}: {e}")
                raise
            except httpx.HTTPError as e:
                logger.error(f"Error fetching story {story_id}: {e}")
                raise
            except Exception as e:
                logger.error(f"Unexpected error fetching story {story_id}: {e}")
                raise


# Singleton instance
_storyblok_client: Optional[StoryblokClient] = None


def get_storyblok_client() -> StoryblokClient:
    """Get or create the Storyblok client singleton."""
    global _storyblok_client
    if _storyblok_client is None:
        _storyblok_client = StoryblokClient()
    return _storyblok_client
