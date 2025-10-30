"""
AWS Bedrock client for interacting with Claude models.
Handles conversation requests and responses using boto3.
"""

import json
import logging
from typing import List, Dict, Any, Optional
import boto3
from botocore.exceptions import ClientError, BotoCoreError

from backend.config import get_settings
from backend.models import Message

logger = logging.getLogger(__name__)


class BedrockClient:
    """Client for AWS Bedrock Converse API using boto3."""

    def __init__(self):
        self.settings = get_settings()
        self.model_id = self.settings.bedrock_model_id
        self.timeout = self.settings.request_timeout

        # Initialize boto3 client for Bedrock Runtime
        # Use credentials from settings if provided, otherwise fall back to AWS defaults
        try:
            client_config = {
                'service_name': 'bedrock-runtime',
                'region_name': self.settings.aws_region
            }

            # Add credentials if they are provided in settings
            if self.settings.aws_access_key_id and self.settings.aws_secret_access_key:
                client_config['aws_access_key_id'] = self.settings.aws_access_key_id
                client_config['aws_secret_access_key'] = self.settings.aws_secret_access_key
                if self.settings.aws_session_token:
                    client_config['aws_session_token'] = self.settings.aws_session_token
                logger.info(f"Using credentials from settings for region {self.settings.aws_region}")
            else:
                logger.info(f"Using default AWS credential chain for region {self.settings.aws_region}")

            self.client = boto3.client(**client_config)
            logger.info(f"Initialized Bedrock client for region {self.settings.aws_region}")
        except Exception as e:
            logger.error(f"Failed to initialize Bedrock client: {str(e)}")
            raise

    def _format_messages(self, conversation_history: List[Message], current_message: str) -> List[Dict[str, Any]]:
        """
        Format conversation history and current message for Bedrock API.

        Args:
            conversation_history: Previous messages in the conversation
            current_message: The current user message

        Returns:
            List of formatted messages for the API
        """
        messages = []

        # Add conversation history
        for msg in conversation_history:
            messages.append({
                "role": msg.role,
                "content": [{"text": msg.content}]
            })

        # Add current message
        messages.append({
            "role": "user",
            "content": [{"text": current_message}]
        })

        return messages

    def _build_system_prompt(self) -> str:
        """Build the system prompt for the Claude model."""
        return """You are an AI assistant helping users discover and analyze content in Storyblok.

Your role:
- Help users search for content using natural language
- Analyze content (count, identify patterns, summarize)
- Ask clarifying questions when needed (especially about content types)
- Interpret their search queries and convert them to search terms
- Extract the number of results the user wants (if specified)
- Filter and refine previous search results based on follow-up questions
- Present search results in a clear, conversational way
- Help users refine their searches through follow-up questions
- Be concise but friendly and helpful

IMPORTANT: You MUST respond ONLY with valid JSON. No extra text before or after the JSON.

## Action Types

### 1. NEW SEARCH (action: "search")
When a user asks to search for NEW content (e.g., "find marketing stories", "show blog posts"):
- Extract the key search terms from their query
- Extract the number of results if specified
- DO NOT include content_type unless absolutely necessary - search broadly by default
- Return: {"action": "search", "term": "search term", "limit": 10, "response": "message"}

Examples:
- "find all marketing stories" → {"action": "search", "term": "marketing", "limit": 10, "response": "Here are the marketing stories I found:"}
- "find the first 5 articles about marketing" → {"action": "search", "term": "marketing articles", "limit": 5, "response": "Here are 5 marketing articles:"}
- "show me blog posts about AI" → {"action": "search", "term": "AI blog posts", "limit": 10, "response": "Here are blog posts about AI:"}
- "find articles mentioning Drupal" → {"action": "search", "term": "Drupal", "limit": 10, "response": "Here are the stories mentioning Drupal:"}

### 2. ANALYZE/COUNT (action: "analyze")
When a user wants to COUNT or ANALYZE content WITHOUT immediately listing results:
- Extract the search term and what to analyze
- Return: {"action": "analyze", "term": "search term", "analysis_type": "count", "response": "I'll check how many articles mention that..."}

Examples:
- "how many articles mention drupal?" → {"action": "analyze", "term": "drupal", "content_type": "article", "analysis_type": "count", "response": "Let me check how many articles mention Drupal..."}
- "do we have any blog posts about React?" → {"action": "analyze", "term": "React", "content_type": "blog_post", "analysis_type": "count", "response": "Let me see if we have blog posts about React..."}

After analysis shows results, if user says "yes please" or "show them" or "list them":
→ {"action": "list_analyzed", "limit": 10, "response": "Here are the articles:"}

If user specifies a limit when confirming:
- "yes, but limit to 10" → {"action": "list_analyzed", "limit": 10, "response": "Here are the first 10:"}
- "show me the first 5" → {"action": "list_analyzed", "limit": 5, "response": "Here are the first 5:"}
- "just show 3" → {"action": "list_analyzed", "limit": 3, "response": "Here are 3 of them:"}

### 3. CLARIFY CONTENT TYPE (action: "clarify")
When the query is ambiguous about content type, ask for clarification:
- Return: {"action": "clarify", "clarify_field": "content_type", "options": ["article", "blog_post", "page"], "response": "message"}

Examples:
- "find stories about marketing" → {"action": "clarify", "clarify_field": "content_type", "options": ["article", "blog_post", "page"], "response": "What type of content are you looking for? Articles, blog posts, pages, or all types?"}

### 4. REFINE/FILTER PREVIOUS RESULTS (action: "refine")
When a user wants to FILTER or NARROW DOWN results from the previous search (e.g., "out of those", "from these", "which one"):
- Extract the filter criteria (keywords, topics, attributes)
- Return: {"action": "refine", "filter_term": "criteria", "response": "message"}

Examples:
- Previous: [10 marketing stories shown]
  User: "out of those stories, give me the one which mentions omnichannel"
  → {"action": "refine", "filter_term": "omnichannel", "response": "Here's the story that mentions omnichannel:"}

- Previous: [8 blog posts shown]
  User: "from these, show me only the ones about AI"
  → {"action": "refine", "filter_term": "AI", "response": "Here are the posts about AI:"}

### 5. CHAT (action: "chat")
When just chatting or acknowledging: {"action": "chat", "response": "your response"}

## Content Types
Common content types in Storyblok:
- "article" - news articles, blog articles
- "blog_post" - blog posts
- "page" - regular pages
- "landing_page" - landing pages
- "post" - generic posts

## How to Distinguish Actions

Use "analyze" when:
- User asks "how many", "do we have", "are there"
- User wants to know about content WITHOUT seeing the list first
- Analytical/counting questions

Use "clarify" when:
- Content type is ambiguous or not specified
- User says "stories" without specifying type
- You need more information to proceed accurately

Use "refine" when:
- User references previous results: "out of those", "from these", "which one"
- User wants to filter/narrow: "only the ones", "just show"
- Context indicates they're working with existing results

Use "search" when:
- User asks for new/different content with clear intent
- Content type is specified or obvious from context
- Direct search request

Use "list_analyzed" when:
- User confirms they want to see the analyzed results
- Follow-up to analyze action

## Important Rules
- limit field is REQUIRED for "search" actions (default to 10)
- filter_term field is REQUIRED for "refine" actions
- content_type is OPTIONAL but recommended for "search" and "analyze"
- The response field should be conversational and natural
- Always check conversation history to understand context
- When unclear about content type, use "clarify" action

Always be helpful and accessible. Remember that some users may have disabilities and rely on voice interaction."""

    def converse(
        self,
        message: str,
        conversation_history: List[Message],
        previous_results: Optional[List[Dict[str, Any]]] = None,
        previous_analysis: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send a message to Claude and get a response.

        Args:
            message: The user's message
            conversation_history: Previous conversation messages
            previous_results: Optional list of previous search results for context
            previous_analysis: Optional previous analysis data for context

        Returns:
            Dict containing the response and any extracted actions

        Raises:
            Exception: If the API request fails
        """
        # Add context about previous results and analysis if available
        context_message = message
        if previous_results:
            # Add results context to help Claude understand what to refine
            results_summary = f"\n\n[CONTEXT: Previous search returned {len(previous_results)} stories. "
            results_summary += "Story titles: " + ", ".join([r.get('name', 'Unknown') for r in previous_results[:10]])
            if len(previous_results) > 10:
                results_summary += f" and {len(previous_results) - 10} more"
            results_summary += "]"
            context_message = message + results_summary
        
        if previous_analysis:
            # Add analysis context
            analysis_summary = f"\n\n[PREVIOUS ANALYSIS: {previous_analysis.get('description', 'Analysis performed')}. "
            analysis_summary += f"Count: {previous_analysis.get('count', 0)} items]"
            context_message = context_message + analysis_summary
        
        messages = self._format_messages(conversation_history, context_message)

        request_body = {
            "messages": messages,
            "system": [{"text": self._build_system_prompt()}],
            "inferenceConfig": {
                "maxTokens": 2048,
                "temperature": 0.7,
                "topP": 0.9
            }
        }

        logger.info(f"Sending request to Bedrock with {len(messages)} messages")

        try:
            # Call Bedrock Converse API
            response = self.client.converse(
                modelId=self.model_id,
                messages=request_body["messages"],
                system=request_body["system"],
                inferenceConfig=request_body["inferenceConfig"]
            )

            logger.info("Received response from Bedrock")

            # Extract the response text
            output = response.get("output", {})
            message_data = output.get("message", {})
            content_blocks = message_data.get("content", [])

            if content_blocks and len(content_blocks) > 0:
                response_text = content_blocks[0].get("text", "")
                logger.info(f"Raw Claude response: {response_text[:200]}...")

                # Try to parse JSON from the response
                try:
                    # Check if response contains JSON
                    if "{" in response_text and "}" in response_text:
                        # Extract JSON portion
                        start_idx = response_text.find("{")
                        end_idx = response_text.rfind("}") + 1
                        json_str = response_text[start_idx:end_idx]
                        parsed_response = json.loads(json_str)
                        
                        action = parsed_response.get("action", "chat")
                        logger.info(f"Parsed action: {action}, term: {parsed_response.get('term')}, filter_term: {parsed_response.get('filter_term')}, limit: {parsed_response.get('limit')}")

                        return {
                            "action": action,
                            "term": parsed_response.get("term"),
                            "filter_term": parsed_response.get("filter_term"),
                            "limit": parsed_response.get("limit", 10),
                            "content_type": parsed_response.get("content_type"),
                            "analysis_type": parsed_response.get("analysis_type"),
                            "clarify_field": parsed_response.get("clarify_field"),
                            "options": parsed_response.get("options"),
                            "response": parsed_response.get("response", response_text),
                            "raw_response": response_text
                        }
                except json.JSONDecodeError as e:
                    logger.warning(f"Could not parse JSON from response: {e}, treating as chat")
                    logger.debug(f"Failed to parse: {response_text}")

                # Default to chat action if no JSON found
                logger.warning("No valid JSON found in response, defaulting to chat action")
                return {
                    "action": "chat",
                    "term": None,
                    "filter_term": None,
                    "limit": 10,
                    "content_type": None,
                    "analysis_type": None,
                    "clarify_field": None,
                    "options": None,
                    "response": response_text,
                    "raw_response": response_text
                }
            else:
                logger.error("No content in Bedrock response")
                return {
                    "action": "error",
                    "term": None,
                    "filter_term": None,
                    "limit": 10,
                    "content_type": None,
                    "analysis_type": None,
                    "clarify_field": None,
                    "options": None,
                    "response": "I apologize, but I couldn't generate a response. Please try again."
                }

        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            error_message = e.response.get('Error', {}).get('Message', str(e))
            logger.error(f"Bedrock API ClientError [{error_code}]: {error_message}")

            # Provide more helpful error messages
            if error_code == 'AccessDeniedException':
                raise Exception(f"Access denied to Bedrock. Please check your AWS credentials and permissions.")
            elif error_code == 'ResourceNotFoundException':
                raise Exception(f"Model {self.model_id} not found. Please check the model ID.")
            elif error_code == 'ThrottlingException':
                raise Exception(f"Request throttled. Please try again in a moment.")
            else:
                raise Exception(f"Bedrock API error [{error_code}]: {error_message}")

        except BotoCoreError as e:
            logger.error(f"Boto core error: {str(e)}")
            raise Exception(f"AWS connection error: {str(e)}")

        except Exception as e:
            logger.error(f"Unexpected error in Bedrock client: {str(e)}")
            raise


    def map_content_type(
        self,
        user_request: str,
        available_content_types: List[str]
    ) -> Optional[str]:
        """
        Use Claude to intelligently map user's requested content type to actual available types.
        
        Args:
            user_request: User's requested content type (e.g., "article", "blog post")
            available_content_types: List of actual content types found in stories
            
        Returns:
            The best matching content type, or None if no good match
        """
        if not available_content_types:
            return None
            
        prompt = f"""Given a user's content request and available content types, select the best match.

User requested: "{user_request}"
Available content types: {', '.join(available_content_types)}

Which available content type best matches the user's request? Consider:
- Semantic similarity (e.g., "article" might match "targeted_page" or "blog_post")
- Common content type patterns
- If no good match exists, respond with "none"

Respond ONLY with the exact content type name from the available list, or "none".
Do not include any explanation or additional text."""

        try:
            messages = [{
                "role": "user",
                "content": [{"text": prompt}]
            }]
            
            response = self.client.converse(
                modelId=self.model_id,
                messages=messages,
                inferenceConfig={
                    "maxTokens": 50,
                    "temperature": 0.3
                }
            )
            
            output = response.get("output", {})
            message_data = output.get("message", {})
            content_blocks = message_data.get("content", [])
            
            if content_blocks and len(content_blocks) > 0:
                result = content_blocks[0].get("text", "").strip()
                
                # Check if result is in available types
                if result in available_content_types:
                    logger.info(f"Mapped '{user_request}' to '{result}'")
                    return result
                elif result.lower() == "none":
                    logger.info(f"No good match for '{user_request}' in available types")
                    return None
                else:
                    logger.warning(f"Claude returned '{result}' which is not in available types")
                    return None
            
            return None
            
        except Exception as e:
            logger.error(f"Error mapping content type: {e}")
            return None


# Singleton instance
_bedrock_client: Optional[BedrockClient] = None


def get_bedrock_client() -> BedrockClient:
    """Get or create the Bedrock client singleton."""
    global _bedrock_client
    if _bedrock_client is None:
        _bedrock_client = BedrockClient()
    return _bedrock_client
