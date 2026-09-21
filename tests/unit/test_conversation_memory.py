import pytest

from app.core.exceptions import MemoryException
from app.memory.conversation import ConversationMemory


def test_add_and_get_messages() -> None:
    memory = ConversationMemory()

    memory.add_message(
        session_id="session-1",
        role="user",
        content="Help me improve my email.",
    )

    memory.add_message(
        session_id="session-1",
        role="assistant",
        content="Sure, I can help.",
    )

    history = memory.get_history("session-1")

    assert len(history) == 2

    assert history[0]["role"] == "user"
    assert history[0]["content"] == (
        "Help me improve my email."
    )

    assert history[1]["role"] == "assistant"


def test_memory_limits_messages() -> None:
    memory = ConversationMemory(max_message=2)

    memory.add_message(
        "session-1",
        "user",
        "Message 1",
    )

    memory.add_message(
        "session-1",
        "user",
        "Message 2",
    )

    memory.add_message(
        "session-1",
        "user",
        "Message 3",
    )

    history = memory.get_history("session-1")

    assert len(history) == 2
    assert history[0]["content"] == "Message 2"
    assert history[1]["content"] == "Message 3"


def test_sessions_are_isolated() -> None:
    memory = ConversationMemory()

    memory.add_message(
        "session-1",
        "user",
        "Hello from session 1",
    )

    memory.add_message(
        "session-2",
        "user",
        "Hello from session 2",
    )

    assert len(memory.get_history("session-1")) == 1
    assert len(memory.get_history("session-2")) == 1

    assert (
        memory.get_history("session-1")[0]["content"]
        == "Hello from session 1"
    )


def test_clear_session() -> None:
    memory = ConversationMemory()

    memory.add_message(
        "session-1",
        "user",
        "Hello",
    )

    memory.clear_session("session-1")

    assert memory.get_history("session-1") == []


def test_empty_session_id() -> None:
    memory = ConversationMemory()

    with pytest.raises(MemoryException):
        memory.add_message(
            "",
            "user",
            "Hello",
        )


def test_empty_message_content() -> None:
    memory = ConversationMemory()

    with pytest.raises(MemoryException):
        memory.add_message(
            "session-1",
            "user",
            "",
        )


def test_invalid_max_messages() -> None:
    with pytest.raises(MemoryException):
        ConversationMemory(max_message=0)