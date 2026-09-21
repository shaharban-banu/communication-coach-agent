"""
Communication agent orchestration.

This module coordinates intent detection, communication planning,
and tool execution for user communication requests.
"""
from typing import Any

from app.agents.intent_detector import IntentDetector
from app.agents.planner import CommunicationPlanner
from app.core.exceptions import AgentExecutionException
from app.core.logging import get_logger
from app.tools.executor import ToolExecutor
from app.agents.response_builder import CommunicationResponseBuilder
from app.memory.conversation import ConversationMemory


logger = get_logger(__name__)

class CommunicationAgent:
    """
    Main orchestration component for the Communication Coach Agent.

    The agent follows this workflow:

        User Request
            ↓
        Intent Detection
            ↓
        Communication Planning
            ↓
        Tool Execution
            ↓
        Tool Results
    """
    def  __init__(self,intent_detector:IntentDetector,
                  planner:CommunicationPlanner,
                  tool_executor:ToolExecutor,
                  response_builder:CommunicationResponseBuilder,
                  memory:ConversationMemory):
        """
        Initialize the communication agent.

        Args:
            intent_detector: Component responsible for detecting
                the user's communication intent.
            planner: Component responsible for creating the tool plan.
            tool_executor: Component responsible for executing
                the selected communication tools.
        """
        self.intent_detector=intent_detector
        self.planner=planner
        self.tool_executor=tool_executor
        self.response_builder=response_builder
        self.memory=memory
        logger.info("Communication agent initialised")

    def process(self,message:str,context:str|None=None,session_id:str|None=None,):
        """
        Process a user communication request.

        Args:
            message: User's communication request.
            context: Optional context relevant to the request.

        Returns:
            Dictionary containing intent, plan, and tool results.

        Raises:
            AgentExecutionException: If agent orchestration fails.
        """
        if not message or not message.strip():
            logger.warning("Communication agent received an empty message")
            raise AgentExecutionException("Communication request cannot be empty.")

        try:
            conversation_history=[]

            if session_id:
                conversation_history=self.memory.get_history(session_id)
                logger.info("Conversation memory loaded | session_id=%s | messages=%s",session_id,len(conversation_history))

            effective_context=context
            if conversation_history:
                history_text="\n".join(
                    f"{item['role']}:{item['content']}"for item in conversation_history
                )
                if effective_context:
                    effective_context=(
                        f"{effective_context}\n\n previous conversation :\n{history_text}"
                    )
                else:
                    effective_context=(
                        f"previous conversation :\n{history_text}"
                    )

            logger.info("Communication agent processing request")

            intent_result=self.intent_detector.detect(message)
            logger.info(
                "Intent detected | intent=%s | confidence=%.2f",
                intent_result.intent.value,
                intent_result.confidence,
            )

            plan=self.planner.create_plan(intent_result.intent)
            logger.info(
                "Communication plan created | intent=%s | tools=%s",
                plan.intent.value,
                [tool.value for tool in plan.tools],
            )

            tool_results=self.tool_executor.execute(
                plan=plan,
                message=message,
                context=effective_context,
            )
            logger.info(
                "Communication agent completed successfully | "
                "tools_executed=%s",
                len(tool_results),
            )

            response=self.response_builder.build(tool_results)

            if session_id:
                self.memory.add_message(session_id=session_id,role="user",content=message,)
                improved_response=response.get("improved_response")
                assistant_content=(improved_response or "Communication coaching response generated")
                self.memory.add_message(session_id=session_id,role="assistant",content=assistant_content,)


            return {
                "intent": intent_result.model_dump(),
                "plan": plan.model_dump(),
                "tool_results": tool_results,
                "response":response,
            }
        except AgentExecutionException:
            raise
        except Exception as exc:
            logger.exception("Communication agent execution failed")
            raise AgentExecutionException("Failed to process the communication request.") from exc

        