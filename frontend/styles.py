"""Scandinavian-inspired styling for the Streamlit frontend."""

import streamlit as st


def apply_styles() -> None:
    """Apply the global Scandinavian minimalist theme."""

    st.markdown(
        """
        <style>

        /* =========================================================
           COLOR SYSTEM
           ========================================================= */

        :root {
            --bg: #F6F5F1;
            --surface: #FFFFFF;
            --surface-soft: #ECEFE9;

            --sidebar: #E9EAE5;

            --text: #242622;
            --text-secondary: #555850;
            --text-muted: #73776F;

            --accent: #71816F;
            --accent-dark: #596756;
            --accent-light: #DDE5DA;

            --terracotta: #A56F5B;
            --terracotta-dark: #8E5C49;

            --border: #D9DCD5;
            --border-light: #E5E6E1;

            --score-bg: #EEF2EC;
            --score-text: #536651;
        }


        /* =========================================================
           GLOBAL APPLICATION
           ========================================================= */

        .stApp {
            background-color: var(--bg) !important;
            color: var(--text) !important;
        }

        .main {
            background-color: var(--bg) !important;
        }

        .block-container {
            max-width: 1050px;
            padding-top: 2.5rem;
            padding-bottom: 5rem;
        }

        html,
        body,
        [class*="css"] {
            font-family:
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                Roboto,
                Helvetica,
                Arial,
                sans-serif;
        }


        /* =========================================================
           BRAND LABEL
           ========================================================= */

        .brand-label {
            color: var(--terracotta) !important;
            font-size: 0.72rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.16em !important;
            text-transform: uppercase;
            margin-bottom: 0.8rem;
        }


       /* =========================================================
   HERO HEADER
   ========================================================= */

.hero-header {
    background-color: #E8ECE4 !important;
    border: 1px solid #D8DDD3 !important;
    border-left: 5px solid #71816F !important;
    border-radius: 12px !important;
    padding: 1.8rem 2rem 1.7rem 2rem !important;
    margin-bottom: 2rem !important;
}

.hero-title {
    color: #272A27 !important;
    font-size: 2.45rem !important;
    font-weight: 650 !important;
    letter-spacing: -0.045em !important;
    line-height: 1.15 !important;
}

.hero-title-accent {
    color: #A56F5B !important;
    font-weight: 500 !important;
    font-style: italic !important;
    margin-left: 0.35rem !important;
}

.hero-description {
    color: #5B6058 !important;
    font-size: 0.94rem !important;
    line-height: 1.65 !important;
    margin-top: 1rem !important;
    max-width: 700px !important;
}


        /* =========================================================
           GENERAL HEADINGS
           ========================================================= */

        h1 {
            color: var(--text) !important;
            font-size: 2.7rem !important;
            font-weight: 600 !important;
            letter-spacing: -0.045em !important;
            line-height: 1.15 !important;
        }

        h2,
        h3 {
            color: var(--text) !important;
            font-weight: 600 !important;
            letter-spacing: -0.025em !important;
        }

        .main p {
            color: var(--text-secondary) !important;
            font-size: 0.95rem;
            line-height: 1.65;
        }


        /* =========================================================
           EYEBROW
           ========================================================= */

        .eyebrow {
            color: var(--terracotta) !important;
            font-size: 0.72rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.16em !important;
            text-transform: uppercase;
            margin-bottom: 0.55rem;
        }

        .muted {
            color: var(--text-muted) !important;
            font-size: 0.9rem !important;
            line-height: 1.6;
        }


        /* =========================================================
           SIDEBAR
           ========================================================= */

        [data-testid="stSidebar"] {
            background-color: var(--sidebar) !important;
            border-right: 1px solid var(--border);
        }

        [data-testid="stSidebar"] > div:first-child {
            padding: 2rem 1.25rem;
        }

        [data-testid="stSidebar"] {
    background-color: var(--sidebar) !important;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] > div:first-child {
    padding: 2rem 1.25rem;
}

[data-testid="stSidebar"] .sidebar-heading {
    color: #343832 !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    letter-spacing: -0.01em !important;
    margin: 0.4rem 0 1rem 0 !important;
}

[data-testid="stSidebar"] .sidebar-section-title {
    color: #343832 !important;
    font-size: 0.92rem !important;
    font-weight: 650 !important;
    margin-bottom: 0.8rem !important;
}

[data-testid="stSidebar"] .eyebrow {
    color: #A56F5B !important;
}

[data-testid="stSidebar"] .muted {
    color: #62675F !important;
}

[data-testid="stSidebar"] .stMarkdown p {
    color: #62675F !important;
}

        [data-testid="stSidebar"] .eyebrow {
            color: var(--terracotta) !important;
            font-weight: 700 !important;
        }

        .sidebar-heading {
            color: #343832 !important;
            font-size: 1.05rem !important;
            font-weight: 600 !important;
            letter-spacing: -0.01em;
            margin: 0.4rem 0 1rem 0;
        }

        .sidebar-section-title {
            color: #343832 !important;
            font-size: 0.92rem !important;
            font-weight: 650 !important;
            margin-bottom: 0.8rem;
        }

        [data-testid="stSidebar"] .sidebar-heading,
        [data-testid="stSidebar"] .sidebar-section-title {
            color: #343832 !important;
        }

        [data-testid="stSidebar"] .muted {
            color: #62675F !important;
        }

        [data-testid="stSidebar"] .stMarkdown p {
            color: #62675F !important;
        }

        [data-testid="stSidebar"] hr {
            border: none !important;
            border-top: 1px solid var(--border) !important;
            margin: 1.5rem 0;
        }


        /* =========================================================
           SIDEBAR BUTTON
           ========================================================= */

       [data-testid="stSidebar"] .stButton > button {
    background-color: #71816F !important;
    color: #FFFFFF !important;
    border: 1px solid #71816F !important;
    border-radius: 8px !important;
    min-height: 2.5rem !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background-color: #596756 !important;
    border-color: #596756 !important;
    color: #FFFFFF !important;
}


        /* =========================================================
           CHAT / MESSAGE AREA
           ========================================================= */

        .user-message {
            background-color: var(--surface-soft);
            border: 1px solid var(--border-light);
            border-radius: 10px;
            padding: 0.9rem 1.15rem;
            margin: 1.25rem 0 0.7rem 0;
        }

        .assistant-message {
            background-color: var(--surface);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 1.15rem 1.25rem;
            margin: 0 0 1rem 0;
        }

        .message-label {
            color: var(--accent-dark) !important;
            font-size: 0.68rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.13em !important;
            margin-bottom: 0.5rem;
        }

        .message-content {
            color: var(--text) !important;
            font-size: 0.94rem !important;
            line-height: 1.7 !important;
        }


        /* =========================================================
           FEEDBACK CARD
           ========================================================= */

        .feedback-card {
            background-color: var(--surface);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 1.2rem 1.3rem;
            margin: 0 0 1rem 0;
        }

        .section-label {
            color: var(--accent-dark) !important;
            font-size: 0.68rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.13em !important;
            margin-bottom: 0.8rem;
        }

        .feedback-list {
            margin: 0;
            padding-left: 1.2rem;
        }

        .feedback-list li {
            color: var(--text-secondary) !important;
            font-size: 0.9rem !important;
            line-height: 1.65 !important;
            margin-bottom: 0.5rem;
        }


        /* =========================================================
           SCORE CARD
           ========================================================= */

        .score-card {
            background-color: var(--score-bg);
            border: 1px solid #D6DED2;
            border-radius: 10px;
            padding: 1.15rem;
            text-align: center;
            margin: 0.5rem 0 1.7rem 0;
        }

        .score-label {
            color: var(--score-text) !important;
            font-size: 0.68rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.14em !important;
        }

        .score-value {
            color: var(--score-text) !important;
            font-size: 2.15rem !important;
            font-weight: 600 !important;
            line-height: 1.2;
            margin-top: 0.3rem;
        }

        .score-value span {
            color: var(--text-muted) !important;
            font-size: 1rem !important;
            font-weight: 400 !important;
        }


        /* =========================================================
           CHAT INPUT
           ========================================================= */

        [data-testid="stChatInput"] {
            background-color: transparent !important;
        }

        [data-testid="stChatInput"] > div {
            background-color: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: 10px !important;
        }

        [data-testid="stChatInput"] textarea {
            background-color: var(--surface) !important;
            color: var(--text) !important;
            caret-color: var(--accent-dark) !important;
            font-size: 0.92rem !important;
        }

        [data-testid="stChatInput"] textarea::placeholder {
            color: #8A8D86 !important;
            opacity: 1 !important;
        }

        [data-testid="stChatInput"] textarea:focus {
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 1px var(--accent) !important;
        }


        /* =========================================================
           TEXT INPUTS / TEXT AREAS
           ========================================================= */

        .stTextInput input,
        .stTextArea textarea {
            background-color: var(--surface) !important;
            color: var(--text) !important;
            border: 1px solid var(--border) !important;
            border-radius: 8px !important;
        }

        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder {
            color: #8A8D86 !important;
            opacity: 1 !important;
        }

        .stTextInput input:focus,
        .stTextArea textarea:focus {
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 1px var(--accent) !important;
        }


        /* =========================================================
           GENERAL BUTTONS
           ========================================================= */

        .stButton > button {
            background-color: var(--accent) !important;
            color: #FFFFFF !important;
            border: 1px solid var(--accent) !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
        }

        .stButton > button:hover {
            background-color: var(--accent-dark) !important;
            border-color: var(--accent-dark) !important;
            color: #FFFFFF !important;
        }


        /* =========================================================
           STREAMLIT WIDGET LABELS
           ========================================================= */

        label {
            color: var(--text-secondary) !important;
        }

        [data-testid="stWidgetLabel"] p {
            color: var(--text-secondary) !important;
        }


        /* =========================================================
           DIVIDERS
           ========================================================= */

        hr {
            border: none !important;
            border-top: 1px solid var(--border-light) !important;
        }


        /* =========================================================
           ALERTS / ERRORS
           ========================================================= */

        [data-testid="stAlert"] {
            border-radius: 8px !important;
        }


        /* =========================================================
           SCROLLBAR
           ========================================================= */

        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-track {
            background: var(--bg);
        }

        ::-webkit-scrollbar-thumb {
            background: #C7CAC3;
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #AEB3AA;
        }


        /* =========================================================
           HIDE STREAMLIT BRANDING
           ========================================================= */

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }


        /* Recent conversation history */

        .recent-prompt {
            color: #45564a;
            font-size: 0.78rem;
            line-height: 1.6;
            padding: 7px 4px;
            margin-bottom: 3px;
            overflow-wrap: anywhere;
            opacity: 1;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

        