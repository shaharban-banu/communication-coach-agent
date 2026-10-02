
"""Reusable Streamlit UI components."""

from html import escape
from typing import Any

import streamlit as st


def render_user_message(content: str) -> None:
    """Render a user message."""

    safe_content = escape(content)

    st.html(
        f"""
        <div class="user-message">
            <div class="message-label">YOU</div>
            <div class="message-content">{safe_content}</div>
        </div>
        """
    )



def render_assistant_message(content: str) -> None:
    """Render the main coaching response with preserved line breaks."""

    safe_content = escape(content).replace("\n", "<br>")

    st.html(
        f"""
        <div class="assistant-message">
            <div class="message-label">COACH</div>
            <div class="message-content">{safe_content}</div>
        </div>
        """
    )



def render_feedback(feedback: list[str]) -> None:
    """Render communication feedback."""

    if not feedback:
        return

    feedback_items = "".join(
        f"<li>{escape(str(item))}</li>"
        for item in feedback
    )

    st.html(
        f"""
        <div class="feedback-card">
            <div class="section-label">
                COMMUNICATION FEEDBACK
            </div>

            <ul class="feedback-list">
                {feedback_items}
            </ul>
        </div>
        """
    )


def render_score(score: float | None) -> None:
    """Render the communication score."""

    if score is None:
        return

    st.html(
        f"""
        <div class="score-card">
            <div class="score-label">
                COMMUNICATION SCORE
            </div>

            <div class="score-value">
                {score:.1f}<span>/10</span>
            </div>
        </div>
        """
    )


def render_coaching_result(result: dict[str, Any]) -> None:
    """Render feedback and score from a coaching response."""

    feedback = result.get("feedback", [])
    score = result.get("score")

    render_feedback(feedback)
    render_score(score)
