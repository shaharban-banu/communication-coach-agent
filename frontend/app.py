"""Streamlit frontend for the Communication Coach Agent."""

import logging
import uuid

import streamlit as st

from api_client import APIClient
from components import (
    render_assistant_message,
    render_coaching_result,
    render_user_message,
)
from styles import apply_styles


logger = logging.getLogger(__name__)


def initialize_session() -> None:
    """Initialize Streamlit session state."""

    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "recent_prompts" not in st.session_state:
        st.session_state.recent_prompts = []

    if "conversations" not in st.session_state:
        st.session_state.conversations = {}

    session_id = st.session_state.session_id

    if session_id not in st.session_state.conversations:
        st.session_state.conversations[session_id] = {
            "title": "New conversation",
            "messages": list(st.session_state.messages),
        }



def render_header() -> None:
    """Render the application header."""

    st.html(
        """
        <div class="brand-label">
            AI COMMUNICATION COACH
        </div>

        <div class="hero-header">
            <div class="hero-title">
                Say it better.
                <span class="hero-title-accent">
                    Mean it clearly.
                </span>
            </div>

            <div class="hero-description">
                Refine your words, practice difficult conversations,
                and build stronger communication habits.
            </div>
        </div>
        """
    )

def render_sidebar() -> None:
    """Render the application sidebar."""

    with st.sidebar:
        st.markdown(
            '<div class="eyebrow">COMMUNICATION COACH</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
    '<div class="sidebar-heading">Practice workspace</div>',
    unsafe_allow_html=True,
)

        
        if st.button(
            "＋ New conversation",
            use_container_width=True,
        ):
            new_session_id = str(uuid.uuid4())

            st.session_state.session_id = new_session_id
            st.session_state.messages = []

            st.session_state.conversations[new_session_id] = {
                "title": "New conversation",
                "messages": [],
            }

            st.rerun()


        
        
        st.markdown("---")

        st.markdown(
            '<div class="sidebar-section-title">'
            'Recent conversations</div>',
            unsafe_allow_html=True,
        )

        conversations = st.session_state.conversations

        recent_conversations = [
            (session_id, conversation)
            for session_id, conversation in conversations.items()
            if conversation["messages"]
        ][-5:]

        for session_id, conversation in reversed(
            recent_conversations
        ):
            title = conversation["title"]

            display_title = (
                title[:35] + "..."
                if len(title) > 35
                else title
            )

            if st.button(
                f"💬 {display_title}",
                key=f"conversation_{session_id}",
                use_container_width=True,
            ):
                st.session_state.session_id = session_id

                st.session_state.messages = list(
                    conversation["messages"]
                )

                st.rerun()

        if not recent_conversations:
            st.caption("Your recent conversations will appear here.")


        st.markdown("---")

        st.markdown(
    '<div class="sidebar-section-title">Explore coaching</div>',
    unsafe_allow_html=True,
)

        st.markdown(
            """
            <div class="muted">
                • Interview practice<br>
                • Email writing<br>
                • Grammar correction<br>
                • Tone improvement<br>
                • Conflict resolution<br>
                • Customer communication
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        st.markdown(
            """
            <div class="muted">
                Your current conversation stays available while
    this session is active.
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_conversation() -> None:
    """Render the current conversation."""

    for message in st.session_state.messages:
        if message["role"] == "user":
            render_user_message(message["content"])

        elif message["role"] == "assistant":
            render_assistant_message(message["content"])

            if "result" in message:
                render_coaching_result(message["result"])


def process_message(message: str) -> None:
    """Send a user message to the communication coach."""

    client = APIClient()

    st.session_state.messages.append(
        {
            "role": "user",
            "content": message,
        }
    )

    session_id = st.session_state.session_id

    conversation = st.session_state.conversations[session_id]

    if conversation["title"] == "New conversation":
        conversation["title"] = message[:45]

    conversation["messages"] = list(st.session_state.messages)

    
    st.session_state.recent_prompts.append(message)

    st.session_state.recent_prompts = (
        st.session_state.recent_prompts[-5:]
    )


    try:
        with st.spinner("Thinking..."):
            result = client.coach(
                message=message,
                session_id=st.session_state.session_id,
            )

            

        logger.info(
            "Coaching response received | session_id=%s",
            st.session_state.session_id,
        )

        improved_response = result.get("improved_response")

        assistant_content = (
            improved_response
            or "I have analyzed your communication and prepared feedback."
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": assistant_content,
                "result": result,
            }
        )

        st.session_state.conversations[session_id]["messages"] = (
            list(st.session_state.messages)
        )

    except RuntimeError as exc:
        logger.error("Coaching request failed: %s", exc)

        st.error(str(exc))

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": (
                    "I couldn't process that request. "
                    "Please check that the Communication Coach API "
                    "is running and try again."
                ),
            }
        )


def main() -> None:
    """Run the Streamlit application."""

    logging.basicConfig(level=logging.INFO)

    apply_styles()
    initialize_session()

    render_sidebar()
    render_header()
    render_conversation()

    message = st.chat_input(
        "Write a message or ask for communication coaching..."
    )

    if message:
        process_message(message)
        st.rerun()


if __name__ == "__main__":
    main()