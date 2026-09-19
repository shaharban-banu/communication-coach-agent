"""
Application-specific exception definitions.

This module contains custom exceptions used to represent expected
application-level failures.
"""


class CommunicationCoachException(Exception):
    """
    Base exception for the Communication Coach Agent.

    All application-specific exceptions should inherit from this class.
    """

    def __init__(self, message: str) -> None:
        """
        Initialize the application exception.

        Args:
            message: Human-readable description of the error.
        """
        self.message = message
        super().__init__(message)


class ValidationException(CommunicationCoachException):
    """
    Raised when application-level input validation fails.
    """

    pass


class ToolExecutionException(CommunicationCoachException):
    """
    Raised when a communication tool fails during execution.
    """

    pass


class AgentExecutionException(CommunicationCoachException):
    """
    Raised when an agent fails during execution.
    """

    pass


class MemoryException(CommunicationCoachException):
    """
    Raised when a memory operation fails.
    """

    pass