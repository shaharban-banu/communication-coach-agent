"""
Communication response builder.

This module converts structured tool results into a unified
feedback response for the user.
"""

from typing import Any

from app.core.exceptions import AgentExecutionException
from app.core.logging import get_logger


logger = get_logger(__name__)

class CommunicationResponseBuilder:
    """
    Build a user-facing response from communication tool results.
    """
    def build(self,tool_results:list[dict[str,Any]],):
        """
        Build feedback and an improved response from tool results.

        Args:
            tool_results: Results returned by the communication tools.

        Returns:
            Dictionary containing feedback, improved response,
            and communication score when available.

        Raises:
            AgentExecutionException: If tool results are invalid.
        """
        if not tool_results:
            logger.warning("Response builder received no tool results")
            raise AgentExecutionException("No tool results available to build a response.")

        try:
            feedback:list[str]=[]
            improved_response:str|None=None
            score:float|None=None

            for tool_result in tool_results:
                tool_name=tool_result.get("tool")
                result=tool_result.get("result",{})

                if not tool_name:
                    logger.warning("Tool result is missing tool name")
                    continue
                    
                if tool_name=="grammar_correction":
                    self._process_grammar_result(result,feedback,)

                elif tool_name=="tone_analysis":
                    self._process_tone_result(result,feedback,)

                elif tool_name=="email_generation":
                    improved_response=self._extract_email(result)

                elif tool_name=="interview_coaching":
                    self._process_interview_result(result,feedback,)
                    improved_response=result.get("improved_answer")

                elif tool_name=="conversation_improvement":
                    self._process_conversation_result(result,feedback,)
                    improved_response=result.get("improved_message")
                    
                elif tool_name=="communication_scoring":
                    score=result.get("overall_score")
                    if result.get("feedback"):
                        feedback.append(result["feedback"])
                    priorities=result.get("improvement_priorities",[],)
                    for prior in priorities:
                        feedback.append(f"Improvement priority: {prior}")
                else:
                    logger.warning( "Unknown tool result received | tool=%s",tool_name,)

            logger.info("Communication response built successfully")
            return{
                "feedback":feedback,
                "improved_response":improved_response,
                "score":score,
            }
        except Exception as exc:
            logger.exception("Failed to build communication response")
            raise AgentExecutionException("Failed to build the communication response.") from exc

    @staticmethod
    def _process_grammar_result(result:dict[str,Any],feedback:list[str],):
        """Process grammar correction results."""
        changes=result.get("changes",[])
        for c in changes:
            feedback.append(f"Grammar improvement: {c}")
    @staticmethod
    def _process_tone_result(result:dict[str,Any],feedback:list[str],):
        """Process tone analysis results."""
        overall_tone=result.get("overall_tone")

        if overall_tone:
            feedback.append(f"Detected tone : {overall_tone}")

        areas=result.get("areas_for_improvement",[],)
        for a in areas:
            feedback.append(f"Tone improvement {a}")

    @staticmethod
    def _process_interview_result(result: dict[str, Any],feedback: list[str],) :
        """Process interview coaching results."""
        assessment = result.get("assessment")

        if assessment:
            feedback.append(f"Interview assessment: {assessment}")

        suggestions = result.get("suggestions",[],)

        for suggestion in suggestions:
            feedback.append(f"Interview suggestion: {suggestion}")

    @staticmethod
    def _process_conversation_result(result: dict[str, Any],feedback: list[str],):
        """Process conversation improvement results."""
        analysis = result.get("analysis")

        if analysis:
            feedback.append(f"Communication analysis: {analysis}")

        suggestions = result.get("suggestions",[],)

        for suggestion in suggestions:
            feedback.append(f"Communication suggestion: {suggestion}")

    @staticmethod
    def _extract_email(result: dict[str, Any],):
        """Build a readable email response."""
        subject = result.get("subject")
        body = result.get("body")

        if not subject or not body:
            return None

        return (
            f"Subject: {subject}\n\n"
            f"{body}"
        )
    



