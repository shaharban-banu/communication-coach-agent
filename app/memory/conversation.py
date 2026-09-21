"""
Short-term conversational memory.

This module provides session-based in-memory storage for recent
conversation messages.
"""
from collections import defaultdict,deque
from typing import Any
from app.core.exceptions import MemoryException
from app.core.logging import get_logger

logger=get_logger(__name__)

class ConversationMemory:
    """
    Store recent conversation messages by session.

    The memory is intentionally short-term and in-memory.
    """
    def __init__(self,max_message:int=10):
        """
        Initialize conversation memory.

        Args:
            max_messages: Maximum number of messages retained
                for each session.

        Raises:
            MemoryException: If max_messages is invalid.
        """
        if max_message<=0:
            raise MemoryException("max_message must be greater than zero")

        self.max_message=max_message
        self._sessions:dict[str,deque[dict[str,Any]]]=(
            defaultdict(lambda : deque(maxlen=self.max_message))
        )
        logger.info("conversation memory initialised | max_message=%s",self.max_message)

    def add_message(self,session_id:str,role:str,content:str):
        """
        Add a message to a conversation session.

        Args:
            session_id: Unique conversation session identifier.
            role: Message role, such as user or assistant.
            content: Message content.

        Raises:
            MemoryException: If the input is invalid.
        """
        if not session_id or not session_id.strip():
            raise MemoryException("Session ID cannot be empty.")
        if not role or not role.strip():
            raise MemoryException("Message role cannot be empty.")
        if not content or not content.strip():
            raise MemoryException("Message content cannot be empty.")

        self._sessions[session_id].append(
            {
                "role":role,
                "content":content,
            }
        )
        logger.info("Conversation message stored | session_id=%s | role=%s",session_id,role)

    def get_history(self,session_id:str,):
        """
        Return recent messages for a session.

        Args:
            session_id: Unique conversation session identifier.

        Returns:
            List of recent conversation messages.
        """
        if not session_id or not session_id.strip():
            raise MemoryException("Session ID cannot be empty.")

        history=list(self._sessions.get(session_id,[]))

        logger.info("Conversation history retrieved | session_id=%s | messages=%s",session_id,len(history))
        return history

    def clear_session(self,session_id:str):
        """
        Clear all messages for a conversation session.

        Args:
            session_id: Unique conversation session identifier.
        """
        if not session_id or not session_id.strip():
            raise MemoryException("Session ID cannot be empty.")

        self._sessions.pop(session_id,None)

        logger.info("Conversation session cleared | session_id=%s",session_id)
        
