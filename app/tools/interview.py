"""
Interview coaching communication tool.

This module provides an LLM-powered tool for evaluating interview
responses and providing actionable coaching feedback.
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


class InterviewCoachingTool(BaseCommunicationTool):
    """
    Tool for providing interview response coaching.
    """

    def __init__(self) -> None:
        settings = get_settings()

        if not settings.llm_api_key:
            logger.error(
                "Groq API key is not configured for interview coaching"
            )
            raise ToolExecutionException(
                "Groq API key is not configured."
            )

        self.client = Groq(api_key=settings.llm_api_key)
        self.model = settings.llm_model

        logger.info(
            "Interview coaching tool initialized | model=%s",
            self.model,
        )

    @property
    def tool_type(self) -> CommunicationTool:
        """Return the type of communication tool."""
        return CommunicationTool.INTERVIEW_COACHING

    def execute(
        self,
        message: str,
        context: str | None = None,
    ) -> dict[str, Any]:
        """
        Evaluate an interview response and provide coaching feedback.

        Args:
            message: Interview question or candidate response.
            context: Optional interview context.

        Returns:
            Dictionary containing interview feedback.

        Raises:
            ToolExecutionException: If coaching fails.
        """
        if not message or not message.strip():
            logger.warning(
                "Interview coaching received an empty message"
            )
            raise ToolExecutionException(
                "Cannot provide interview coaching for empty input."
            )

        system_prompt = """
You are an expert interview coach.

Analyze the user's interview-related input and provide practical,
constructive feedback.

Evaluate:
- Answer quality
- Clarity
- Relevance
- Structure
- Strengths
- Areas for improvement
- Suggested improved answer

If the user provides an interview question without an answer,
explain how they should approach answering it and provide a
sample answer.

Do not invent personal experience or qualifications for the user.

Return JSON with exactly these fields:

{
    "assessment": "overall assessment",
    "strengths": ["strength 1", "strength 2"],
    "areas_for_improvement": ["area 1", "area 2"],
    "suggestions": ["suggestion 1", "suggestion 2"],
    "improved_answer": "improved or sample answer"
}
"""

        user_content = message

        if context:
            user_content = (
                f"Context:\n{context}\n\n"
                f"Interview Input:\n{message}"
            )

        try:
            logger.info("Starting interview coaching")

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
                    "Interview coaching returned an empty response"
                )
                raise ToolExecutionException(
                    "Interview coaching returned an empty response."
                )

            result = json.loads(content)

            required_fields = (
                "assessment",
                "strengths",
                "areas_for_improvement",
                "suggestions",
                "improved_answer",
            )

            missing_fields = [
                field
                for field in required_fields
                if field not in result
            ]

            if missing_fields:
                logger.error(
                    "Interview coaching response missing fields: %s",
                    missing_fields,
                )
                raise ToolExecutionException(
                    "Interview coaching returned an incomplete response."
                )

            logger.info("Interview coaching completed")

            return {
                "assessment": result["assessment"],
                "strengths": result["strengths"],
                "areas_for_improvement": result[
                    "areas_for_improvement"
                ],
                "suggestions": result["suggestions"],
                "improved_answer": result["improved_answer"],
            }

        except ToolExecutionException:
            raise

        except json.JSONDecodeError as exc:
            logger.exception(
                "Invalid JSON returned by interview coaching"
            )
            raise ToolExecutionException(
                "Interview coaching returned an invalid response."
            ) from exc

        except Exception as exc:
            logger.exception("Interview coaching failed")
            raise ToolExecutionException(
                "Failed to provide interview coaching."
            ) from exc