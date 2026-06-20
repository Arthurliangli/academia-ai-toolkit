"""
Shared utilities for the Academia AI Toolkit.
All tools import from this module.
"""

import anthropic
import streamlit as st


# ── Model options ─────────────────────────────────────────────────────────────
MODELS = {
    "Claude Sonnet (Recommended — fast & smart)": "claude-sonnet-4-5",
    "Claude Haiku (Fastest — good for simple tasks)": "claude-haiku-4-5-20251001",
    "Claude Opus (Most powerful — slower)": "claude-opus-4-5",
}

DEFAULT_MODEL = "claude-sonnet-4-5"


# ── Sidebar setup (call at the top of every app) ──────────────────────────────
def setup_sidebar(tool_name: str, tool_description: str) -> tuple[str | None, str]:
    """
    Renders the standard sidebar with API key input and model selector.
    Returns (api_key, model_id) — api_key is None if not entered.
    """
    with st.sidebar:
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/PyTorch_logo_icon.svg/1200px-PyTorch_logo_icon.svg.png",
            width=40,
        )
        st.title("🎓 Academia AI Toolkit")
        st.caption(f"**{tool_name}**")
        st.markdown("---")

        st.subheader("🔑 API Key")
        st.markdown(
            "Get a free key at [console.anthropic.com](https://console.anthropic.com)",
            unsafe_allow_html=True,
        )
        api_key = st.text_input(
            "Anthropic API Key",
            type="password",
            placeholder="sk-ant-...",
            help="Your key is never stored. It lives only in your browser session.",
        )

        st.markdown("---")
        st.subheader("⚙️ Model")
        model_label = st.selectbox("Choose model", list(MODELS.keys()))
        model_id = MODELS[model_label]

        st.markdown("---")
        st.subheader("ℹ️ About this tool")
        st.info(tool_description)

        st.markdown("---")
        st.caption(
            "🔒 Privacy: Your text is sent to Anthropic for processing. "
            "No data is stored by this toolkit."
        )

    return api_key or None, model_id


# ── Core AI call ──────────────────────────────────────────────────────────────
def call_claude(
    api_key: str,
    model: str,
    system_prompt: str,
    user_message: str,
    max_tokens: int = 4096,
) -> str:
    """
    Calls the Anthropic API and returns the text response.
    Raises ValueError with a user-friendly message on errors.
    """
    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
        return message.content[0].text
    except anthropic.AuthenticationError:
        raise ValueError(
            "❌ Invalid API key. Please check your key at console.anthropic.com"
        )
    except anthropic.RateLimitError:
        raise ValueError(
            "⏳ Rate limit reached. Please wait a moment and try again."
        )
    except anthropic.APIError as e:
        raise ValueError(f"❌ API error: {str(e)}")


# ── Download button helper ────────────────────────────────────────────────────
def download_button(content: str, filename: str, label: str = "⬇️ Download Result"):
    """Renders a styled download button."""
    st.download_button(
        label=label,
        data=content,
        file_name=filename,
        mime="text/plain",
        use_container_width=True,
    )


# ── API key guard ─────────────────────────────────────────────────────────────
def require_api_key(api_key: str | None) -> bool:
    """
    Shows a warning if no API key is provided.
    Returns True if key is present, False otherwise.
    """
    if not api_key:
        st.warning(
            "👈 Please enter your **Anthropic API key** in the sidebar to get started. "
            "Get a free key at [console.anthropic.com](https://console.anthropic.com).",
            icon="🔑",
        )
        return False
    return True
