"""
Conversation improvement communication tool.

This module provides an LLM-powered tool for improving conversational
messages while preserving the user's original meaning.
"""

import json
from typing import Any

from groq import Groq

from app.agents.tool_plan import CommunicationTool
from app.core.config import get_settings
from app.core.exceptions import ToolExecutionException
from app.core.logging import get_logger
from app.tools.base import BaseCommunicationTool


logger = get_logger(__name__)


class ConversationImprovementTool(BaseCommunicationTool):
    """
    Tool for improving conversational communication.
    """

    def __init__(self) -> None:
        settings = get_settings()

        if not settings.llm_api_key:
            logger.error(
                "Groq API key is not configured for conversation improvement"
            )
            raise ToolExecutionException(
                "Groq API key is not configured."
            )

        self.client = Groq(api_key=settings.llm_api_key)
        self.model = settings.llm_model

        logger.info(
            "Conversation improvement tool initialized | model=%s",
            self.model,
        )

    @property
    def tool_type(self) -> CommunicationTool:
        """Return the type of communication tool."""
        return CommunicationTool.CONVERSATION_IMPROVEMENT

    def execute(
        self,
        message: str,
        context: str | None = None,
    ) -> dict[str, Any]:
        """
        Analyze and improve a conversational message.

        Args:
            message: User's original communication.
            context: Optional context about the conversation.

        Returns:
            Dictionary containing communication analysis and
            an improved version of the message.

        Raises:
            ToolExecutionException: If the improvement process fails.
        """
        if not message or not message.strip():
            logger.warning(
                "Conversation improvement received an empty message"
            )
            raise ToolExecutionException(
                "Cannot improve an empty message."
            )

        system_prompt = """
You are an expert communication coach.

Analyze the user's communication and improve it while preserving
the original meaning and intent.

Focus on:
- Clarity
- Respectfulness
- Professionalism
- Emotional awareness
- Appropriate tone
- Conciseness
- Effectiveness

The improved version should sound natural and should not change
facts or invent information.

Return JSON with exactly these fields:

{
    "analysis": "brief analysis of the original communication",
    "issues": ["issue 1", "issue 2"],
    "suggestions": ["suggestion 1", "suggestion 2"],
    "improved_message": "improved version of the communication",
    "recommended_tone": "recommended tone"
}
"""

        user_content = message

        if context:
            user_content = (
                f"Context:\n{context}\n\n"
                f"Original Communication:\n{message}"
            )

        try:
            logger.info("Starting conversation improvement")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_content,
                    },
                ],
                temperature=0.3,
                response_format={
                    "type": "json_object",
                },
            )

            content = response.choices[0].message.content

            if not content:
                logger.error(
                    "Conversation improvement returned an empty response"
                )
                raise ToolExecutionException(
                    "Conversation improvement returned an empty response."
                )

            result = json.loads(content)

            required_fields = (
                "analysis",
                "issues",
                "suggestions",
                "improved_message",
                "recommended_tone",
            )

            missing_fields = [
                field
                for field in required_fields
                if field not in result
            ]

            if missing_fields:
                logger.error(
                    "Conversation improvement response missing fields: %s",
                    missing_fields,
                )
                raise ToolExecutionException(
                    "Conversation improvement returned an incomplete response."
                )

            logger.info("Conversation improvement completed")

            return {
                "analysis": result["analysis"],
                "issues": result["issues"],
                "suggestions": result["suggestions"],
                "improved_message": result["improved_message"],
                "recommended_tone": result["recommended_tone"],
            }

        except ToolExecutionException:
            raise

        except json.JSONDecodeError as exc:
            logger.exception(
                "Invalid JSON returned by conversation improvement"
            )
            raise ToolExecutionException(
                "Conversation improvement returned an invalid response."
            ) from exc

        except Exception as exc:
            logger.exception("Conversation improvement failed")
            raise ToolExecutionException(
                "Failed to improve the communication."
            ) from exc