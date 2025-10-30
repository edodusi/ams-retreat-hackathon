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
        return """You are an AI assistant helping users discover content in Storyblok.

Your role:
- Help users search for content using natural language
- Interpret their search queries and convert them to search terms
- Extract the number of results the user wants (if specified)
- Present search results in a clear, conversational way
- Help users refine their searches through follow-up questions
- Be concise but friendly and helpful

IMPORTANT: You MUST respond ONLY with valid JSON. No extra text before or after the JSON.

When a user asks to search for content (e.g., "find marketing stories", "show blog posts"):
1. Extract the key search terms from their query
2. Extract the number of results if specified (e.g., "first 5", "3 articles", "show me 10")
3. Return ONLY this JSON format:
   {"action": "search", "term": "the search term", "limit": 10, "response": "I found some results for you."}

Examples:
- "find all marketing stories" → {"action": "search", "term": "marketing", "limit": 10, "response": "Here are the marketing stories I found:"}
- "find the first 5 articles about marketing" → {"action": "search", "term": "marketing articles", "limit": 5, "response": "Here are 5 marketing articles:"}
- "show me 3 blog posts about technology" → {"action": "search", "term": "blog posts technology", "limit": 3, "response": "Here are 3 blog posts about technology:"}
- "get 20 stories" → {"action": "search", "term": "stories", "limit": 20, "response": "Here are 20 stories:"}

When refining searches (e.g., "only from this year", "show recent ones"):
4. Consider the conversation context and modify the search accordingly
5. Return the same JSON format with updated search terms and limit

When just chatting or acknowledging results:
6. Return: {"action": "chat", "response": "your response"}

IMPORTANT RULES:
- limit field is REQUIRED for search actions (default to 10 if user doesn't specify)
- Common phrases indicating limit: "first X", "X items", "show me X", "get X", "top X", "X results"
- Always use the "search" action when the user wants to find, search, or look for content
- The response field should be brief - the actual results will be shown automatically

Always be helpful and accessible. Remember that some users may have disabilities and rely on voice interaction."""

    def converse(
        self,
        message: str,
        conversation_history: List[Message]
    ) -> Dict[str, Any]:
        """
        Send a message to Claude and get a response.

        Args:
            message: The user's message
            conversation_history: Previous conversation messages

        Returns:
            Dict containing the response and any extracted actions

        Raises:
            Exception: If the API request fails
        """
        messages = self._format_messages(conversation_history, message)

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
                        
                        logger.info(f"Parsed action: {parsed_response.get('action')}, term: {parsed_response.get('term')}, limit: {parsed_response.get('limit')}")

                        return {
                            "action": parsed_response.get("action", "chat"),
                            "term": parsed_response.get("term"),
                            "limit": parsed_response.get("limit", 10),
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
                    "limit": 10,
                    "response": response_text,
                    "raw_response": response_text
                }
            else:
                logger.error("No content in Bedrock response")
                return {
                    "action": "error",
                    "limit": 10,
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


# Singleton instance
_bedrock_client: Optional[BedrockClient] = None


def get_bedrock_client() -> BedrockClient:
    """Get or create the Bedrock client singleton."""
    global _bedrock_client
    if _bedrock_client is None:
        _bedrock_client = BedrockClient()
    return _bedrock_client
