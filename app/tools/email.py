"""
Email generation communication tool.

This module provides an LLM-powered tool for generating
professional emails from user requirements.
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


class EmailGenerationTool(BaseCommunicationTool):
    """
    Generate professional emails from user requirements.

    The tool uses the configured Groq LLM and returns a structured
    email containing a subject, body, and recommended tone.
    """

    def __init__(self) -> None:
        """
        Initialize the email generation tool.

        Raises:
            ToolExecutionException: If the Groq API key is unavailable.
        """
        settings = get_settings()

        if not settings.llm_api_key:
            logger.error(
                "Groq API key is not configured for email generation"
            )
            raise ToolExecutionException(
                "Groq API key is not configured."
            )

        self.client = Groq(api_key=settings.llm_api_key)
        self.model = settings.llm_model

        logger.info(
            "Email generation tool initialized | model=%s",
            self.model,
        )

    @property
    def tool_type(self) -> CommunicationTool:
        """
        Return the tool identifier.

        Returns:
            CommunicationTool: Email generation tool type.
        """
        return CommunicationTool.EMAIL_GENERATION

    def execute(
        self,
        message: str,
        context: str | None = None,
    ) -> dict[str, Any]:
        """
        Generate an email from the supplied requirements.

        Args:
            message: User's email-writing request.
            context: Optional contextual information.

        Returns:
            dict[str, Any]: Generated email information.

        Raises:
            ToolExecutionException: If email generation fails.
        """
        if not message or not message.strip():
            logger.warning(
                "Email generation received an empty message"
            )
            raise ToolExecutionException(
                "Cannot generate an email from empty input."
            )

        system_prompt = """
You are a professional business communication assistant.

Generate a clear, professional email based on the user's request.

Consider the provided context when available.

The email should:
- Have an appropriate subject.
- Be clear and concise.
- Preserve the user's intended meaning.
- Use an appropriate professional tone.
- Avoid inventing facts that the user did not provide.

Return JSON with exactly these fields:

{
    "subject": "email subject",
    "body": "complete email body",
    "tone": "recommended tone"
}
"""

        user_content = message

        if context:
            user_content = (
                f"Context:\n{context}\n\n"
                f"Request:\n{message}"
            )

        try:
            logger.info("Starting email generation")

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
                    "Email generation returned an empty response"
                )
                raise ToolExecutionException(
                    "Email generation returned an empty response."
                )

            result = json.loads(content)

            required_fields = (
                "subject",
                "body",
                "tone",
            )

            missing_fields = [
                field
                for field in required_fields
                if field not in result
            ]

            if missing_fields:
                logger.error(
                    "Email generation response missing fields: %s",
                    missing_fields,
                )
                raise ToolExecutionException(
                    "Email generation returned an incomplete response."
                )

            logger.info(
                "Email generation completed"
            )

            return {
                "subject": result["subject"],
                "body": result["body"],
                "tone": result["tone"],
            }

        except ToolExecutionException:
            raise

        except json.JSONDecodeError as exc:
            logger.exception(
                "Invalid JSON returned by email generation"
            )

            raise ToolExecutionException(
                "Email generation returned an invalid response."
            ) from exc

        except Exception as exc:
            logger.exception(
                "Email generation failed"
            )

            raise ToolExecutionException(
                "Failed to generate the email."
            ) from exc