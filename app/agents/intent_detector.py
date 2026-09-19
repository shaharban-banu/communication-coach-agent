"""
LLM-based communication intent detection.

This module uses Groq to classify user requests into one of the
supported communication intents.
"""

import json
from groq import Groq

from app.core.config import get_settings
from app.core.exceptions import AgentExecutionException
from app.core.logging import get_logger
from app.schemas.intent import IntentClassification

logger=get_logger(__name__)

class IntentDetector:
    """
    Detect communication intent using a Groq-hosted LLM.

    The classifier uses structured output so that the LLM response
    can be validated using the IntentClassification Pydantic model.
    """
    def __init__(self) -> None:
        """
        Initialize the Groq client using application settings.

        Raises:
            AgentExecutionException: If the Groq API key is missing.
        """
        settings = get_settings()

        if not settings.llm_api_key:
            logger.error("Groq API key is not configured")
            raise AgentExecutionException(
                "Groq API key is not configured."
            )

        self.client = Groq(api_key=settings.llm_api_key)
        self.model = settings.llm_model

        logger.info(
            "Intent detector initialized with model=%s",
            self.model,
        )

    def detect(self, message: str) -> IntentClassification:
        """
        Classify a communication request using the Groq LLM.

        Args:
            message: User's natural-language communication request.

        Returns:
            IntentClassification: Structured intent classification.

        Raises:
            AgentExecutionException: If classification fails.
        """
        if not message or not message.strip():
            logger.warning(
                "Intent detection received an empty message"
            )
            raise AgentExecutionException(
                "Cannot detect intent from an empty message."
            )

        system_prompt = """
You are an intent classification system for a Communication Training Agent.

Classify the user's request into exactly ONE of these intents:

- email_writing
- interview_practice
- grammar_correction
- tone_improvement
- public_speaking
- conflict_resolution
- customer_communication

Definitions:

email_writing:
Requests to write, draft, or compose an email or professional email.

interview_practice:
Requests involving mock interviews, interview questions,
interview preparation, or interview coaching.

grammar_correction:
Requests to correct grammar, spelling, sentence structure,
or English-language errors.

tone_improvement:
Requests to make communication more professional, polite,
formal, friendly, confident, concise, or otherwise change its tone.

public_speaking:
Requests involving speeches, presentations, public speaking,
presentation delivery, or speaking confidence.

conflict_resolution:
Requests involving disagreements, arguments, difficult conversations,
workplace conflicts, or resolving interpersonal communication problems.

customer_communication:
Requests involving customers, clients, customer complaints,
customer support, or responses to unhappy customers.

Return the most appropriate single intent.
Do not invent an intent outside this list.
"""

        try:
            logger.info(
                "Starting LLM intent classification"
            )

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
                    "type": "json_schema",
                    "json_schema": {
                        "name": "intent_classification",
                        "strict": True,
                        "schema": IntentClassification.model_json_schema(),
                    },
                },
            )

            content = response.choices[0].message.content

            if not content:
                logger.error(
                    "Groq returned an empty classification response"
                )
                raise AgentExecutionException(
                    "The intent classifier returned an empty response."
                )

            classification = IntentClassification.model_validate(
                json.loads(content)
            )

            logger.info(
                "Intent classified | intent=%s | confidence=%.2f",
                classification.intent.value,
                classification.confidence,
            )

            return classification

        except AgentExecutionException:
            raise

        except Exception as exc:
            logger.exception(
                "LLM intent classification failed"
            )

            raise AgentExecutionException(
                "Failed to classify the communication intent."
            ) from exc