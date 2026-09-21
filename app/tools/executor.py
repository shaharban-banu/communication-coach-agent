"""
Tool execution orchestration.

This module executes the tools selected by the communication planner.
"""

from typing import Any

from app.agents.tool_plan import ToolExecutionPlan
from app.core.exceptions import ToolExecutionException
from app.core.logging import get_logger
from app.tools.registry import ToolRegistry

logger = get_logger(__name__)


class ToolExecutor:
    """
    Execute tools according to a communication execution plan.

    Tools are executed sequentially in the order specified by the
    planner.
    """

    def __init__(self, registry: ToolRegistry) -> None:
        """
        Initialize the tool executor.

        Args:
            registry: Registry containing available communication tools.
        """
        self.registry = registry

    def execute(
        self,
        plan: ToolExecutionPlan,
        message: str,
        context: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Execute every tool in the supplied plan.

        Args:
            plan: Ordered communication tool execution plan.
            message: User's communication message.
            context: Optional communication context.

        Returns:
            list[dict[str, Any]]: Results returned by each tool.

        Raises:
            ToolExecutionException: If a tool fails during execution.
        """
        results: list[dict[str, Any]] = []

        logger.info(
            "Starting tool execution | intent=%s | tool_count=%d",
            plan.intent.value,
            len(plan.tools),
        )

        for tool_type in plan.tools:
            logger.info(
                "Executing tool | tool=%s",
                tool_type.value,
            )

            try:
                tool = self.registry.get(tool_type)

                result = tool.execute(
                    message=message,
                    context=context,
                )

                results.append(
                    {
                        "tool": tool_type.value,
                        "result": result,
                    }
                )

            except ToolExecutionException:
                raise

            except Exception as exc:
                logger.exception(
                    "Tool execution failed | tool=%s",
                    tool_type.value,
                )

                raise ToolExecutionException(
                    f"Failed to execute tool: {tool_type.value}"
                ) from exc

        logger.info(
            "Tool execution completed | tools_executed=%d",
            len(results),
        )

        return results