"""
Communication scoring tool.

This module provides an LLM-powered tool for evaluating the quality
of a user's communication across multiple dimensions.
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


class CommunicationScoringTool(BaseCommunicationTool):
    """
    Tool for scoring communication quality.
    """

    def __init__(self) -> None:
        settings = get_settings()

        if not settings.llm_api_key:
            logger.error(
                "Groq API key is not configured for communication scoring"
            )
            raise ToolExecutionException(
                "Groq API key is not configured."
            )

        self.client = Groq(api_key=settings.llm_api_key)
        self.model = settings.llm_model

        logger.info(
            "Communication scoring tool initialized | model=%s",
            self.model,
        )

    @property
    def tool_type(self) -> CommunicationTool:
        """Return the type of communication tool."""
        return CommunicationTool.COMMUNICATION_SCORING

    def execute(
        self,
        message: str,
        context: str | None = None,
    ) -> dict[str, Any]:
        """
        Evaluate the quality of a communication.

        Args:
            message: Communication text to evaluate.
            context: Optional context for the evaluation.

        Returns:
            Dictionary containing communication scores and feedback.

        Raises:
            ToolExecutionException: If scoring fails.
        """
        if not message or not message.strip():
            logger.warning(
                "Communication scoring received an empty message"
            )
            raise ToolExecutionException(
                "Cannot score an empty message."
            )

        system_prompt = """
You are an expert communication evaluator.

Evaluate the user's communication objectively.

Score each dimension from 0 to 10:

- grammar
- clarity
- tone
- professionalism

Then calculate an overall_score from 0 to 10.

Provide concise and actionable feedback.

Do not judge the user's personality or character.
Evaluate only the communication provided.

Return JSON with exactly these fields:

{
    "grammar": 8.0,
    "clarity": 7.5,
    "tone": 8.0,
    "professionalism": 7.0,
    "overall_score": 7.6,
    "feedback": "Brief overall feedback",
    "improvement_priorities": [
        "Priority 1",
        "Priority 2"
    ]
}
"""

        user_content = message

        if context:
            user_content = (
                f"Context:\n{context}\n\n"
                f"Communication to evaluate:\n{message}"
            )

        try:
            logger.info("Starting communication scoring")

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
                temperature=0.0,
                response_format={
                    "type": "json_object",
                },
            )

            content = response.choices[0].message.content

            if not content:
                logger.error(
                    "Communication scoring returned an empty response"
                )
                raise ToolExecutionException(
                    "Communication scoring returned an empty response."
                )

            result = json.loads(content)

            required_fields = (
                "grammar",
                "clarity",
                "tone",
                "professionalism",
                "overall_score",
                "feedback",
                "improvement_priorities",
            )

            missing_fields = [
                field
                for field in required_fields
                if field not in result
            ]

            if missing_fields:
                logger.error(
                    "Communication scoring response missing fields: %s",
                    missing_fields,
                )
                raise ToolExecutionException(
                    "Communication scoring returned an incomplete response."
                )

            score_fields = (
                "grammar",
                "clarity",
                "tone",
                "professionalism",
                "overall_score",
            )

            for field in score_fields:
                score = result[field]

                if not isinstance(score, (int, float)):
                    logger.error(
                        "Invalid score type for field '%s'",
                        field,
                    )
                    raise ToolExecutionException(
                        f"Invalid score returned for {field}."
                    )

                if not 0 <= score <= 10:
                    logger.error(
                        "Score out of range for '%s': %s",
                        field,
                        score,
                    )
                    raise ToolExecutionException(
                        f"Score for {field} must be between 0 and 10."
                    )

            logger.info(
                "Communication scoring completed | overall_score=%s",
                result["overall_score"],
            )

            return {
                "grammar": result["grammar"],
                "clarity": result["clarity"],
                "tone": result["tone"],
                "professionalism": result["professionalism"],
                "overall_score": result["overall_score"],
                "feedback": result["feedback"],
                "improvement_priorities": result[
                    "improvement_priorities"
                ],
            }

        except ToolExecutionException:
            raise

        except json.JSONDecodeError as exc:
            logger.exception(
                "Invalid JSON returned by communication scoring"
            )
            raise ToolExecutionException(
                "Communication scoring returned an invalid response."
            ) from exc

        except Exception as exc:
            logger.exception("Communication scoring failed")
            raise ToolExecutionException(
                "Failed to score the communication."
            ) from exc