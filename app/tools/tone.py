"""
Tone analysis communication tool.

This module provides an LLM-powered tool for analyzing the tone
and communication characteristics of user-provided text.
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

class ToneAnalysisTool(BaseCommunicationTool):
    """
    Analyze the tone of user-provided communication.

    The tool uses the configured Groq LLM and returns structured
    information about the communication tone.
    """

    def __init__(self) -> None:
        """
        Initialize the tone analysis tool.

        Raises:
            ToolExecutionException: If the Groq API key is unavailable.
        """
        settings = get_settings()

        if not settings.llm_api_key:
            logger.error(
                "Groq API key is not configured for tone analysis"
            )
            raise ToolExecutionException(
                "Groq API key is not configured."
            )

        self.client = Groq(api_key=settings.llm_api_key)
        self.model = settings.llm_model

        logger.info(
            "Tone analysis tool initialized | model=%s",
            self.model,
        )

    @property
    def tool_type(self):
        """
        Return the tool identifier.

        Returns:
            CommunicationTool: Tone analysis tool type.
        """
        return CommunicationTool.TONE_ANALYSIS
    
    def execute(self, message, context = None):
        """
        Analyze the tone of the supplied communication.

        Args:
            message: Communication text to analyze.
            context: Optional contextual information.

        Returns:
            dict[str, Any]: Structured tone analysis result.

        Raises:
            ToolExecutionException: If tone analysis fails.
        """
        if not message or not message.strip():
            logger.warning(
                "Tone analysis received an empty message"
            )
            raise ToolExecutionException(
                "Cannot analyze the tone of empty text."
            )
        system_prompt = """
You are a professional communication coach.

Analyze the tone of the user's communication.

Identify:
- the overall tone
- important tone characteristics
- communication strengths
- areas that could be improved
- a suggested tone for effective communication

Consider the context when it is provided.

Do not change the user's message.

Return JSON with exactly these fields:

{
    "overall_tone": "string",
    "characteristics": ["string"],
    "strengths": ["string"],
    "areas_for_improvement": ["string"],
    "suggested_tone": "string"
}
"""
        user_content = message

        if context:
            user_content = (
                f"Context:\n{context}\n\n"
                f"Communication:\n{message}"
            )

        try:
            logger.info("Starting tone analysis")

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
                temperature=0,
                response_format={
                    "type": "json_object",
                },
            )

            content = response.choices[0].message.content

            if not content:
                logger.error(
                    "Tone analysis returned an empty response"
                )
                raise ToolExecutionException(
                    "Tone analysis returned an empty response."
                )

            result = json.loads(content)

            required_fields = (
                "overall_tone",
                "characteristics",
                "strengths",
                "areas_for_improvement",
                "suggested_tone",
            )

            missing_fields = [
                field
                for field in required_fields
                if field not in result
            ]

            if missing_fields:
                logger.error(
                    "Tone analysis response missing fields: %s",
                    missing_fields,
                )
                raise ToolExecutionException(
                    "Tone analysis returned an incomplete response."
                )

            logger.info(
                "Tone analysis completed | tone=%s",
                result["overall_tone"],
            )

            return {
                "overall_tone": result["overall_tone"],
                "characteristics": result["characteristics"],
                "strengths": result["strengths"],
                "areas_for_improvement": result[
                    "areas_for_improvement"
                ],
                "suggested_tone": result["suggested_tone"],
            }

        except ToolExecutionException:
            raise

        except json.JSONDecodeError as exc:
            logger.exception(
                "Invalid JSON returned by tone analysis"
            )

            raise ToolExecutionException(
                "Tone analysis returned an invalid response."
            ) from exc

        except Exception as exc:
            logger.exception(
                "Tone analysis failed"
            )

            raise ToolExecutionException(
                "Failed to perform tone analysis."
            ) from exc
