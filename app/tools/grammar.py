"""
Grammar correction communication tool.

This module provides an LLM-powered tool for identifying and correcting
grammar issues in user-provided text.
"""
import json
from typing import Any
from groq import Groq
from app.agents.tool_plan import CommunicationTool
from app.core.config import get_settings
from app.core.exceptions import ToolExecutionException
from app.core.logging import get_logger
from app.tools.base import BaseCommunicationTool

logger=get_logger(__name__)

class GrammarCorrectionTool(BaseCommunicationTool):
    """
    Correct grammar in user-provided communication.

    The tool uses the configured Groq LLM and returns structured
    correction results.
    """
    def __init__(self):
        """
        Initialize the grammar correction tool.

        Raises:
            ToolExecutionException: If the Groq API key is unavailable.
        """
        settings=get_settings()
        if not settings.llm_api_key:
            logger.error("Groq API key is not configured for grammar tool")
            raise ToolExecutionException("Groq API key is not configured.")

        self.client=Groq(api_key=settings.llm_api_key)
        self.model=settings.llm_model

        logger.info("Grammar correction tool initialized | model=%s",self.model,)

    @property
    def tool_type(self):
        """
        Return the tool identifier.

        Returns:
            CommunicationTool: Grammar correction tool type.
        """
        return CommunicationTool.GRAMMAR_CORRECTION

    def execute(self, message:str, context:str|None = None):
        """
        Correct grammar in the supplied message.

        Args:
            message: Text requiring grammar correction.
            context: Optional context for the communication.

        Returns:
            dict[str, Any]: Structured grammar correction result.

        Raises:
            ToolExecutionException: If grammar correction fails.
        """
        if not message or not message.strip():
            logger.warning(
                "Grammar correction received an empty message"
            )
            raise ToolExecutionException(
                "Cannot perform grammar correction on empty text."
            )
        system_prompt = """
You are a professional English grammar correction assistant.

Analyze the user's text and correct grammar, spelling,
punctuation, and sentence structure.

Do not unnecessarily change the meaning or tone.

Return JSON with exactly these fields:
{
    "corrected_text": "corrected version",
    "changes": [
        "description of each important correction"
    ]
}
"""
        try:
            logger.info("Starting grammar correction")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": message,
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
                    "Grammar correction returned an empty response"
                )
                raise ToolExecutionException(
                    "Grammar correction returned an empty response."
                )

            result = json.loads(content)

            logger.info("Grammar correction completed")

            return {
                "corrected_text": result.get("corrected_text", ""),
                "changes": result.get("changes", []),
            }

        except ToolExecutionException:
            raise

        except json.JSONDecodeError as exc:
            logger.exception(
                "Invalid JSON returned by grammar correction"
            )

            raise ToolExecutionException(
                "Grammar correction returned an invalid response."
            ) from exc

        except Exception as exc:
            logger.exception(
                "Grammar correction failed"
            )

            raise ToolExecutionException(
                "Failed to perform grammar correction."
            ) from exc