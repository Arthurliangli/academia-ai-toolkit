"""
Shared utilities for the Academia AI Toolkit.
All tools import from this module.

Supports two AI providers:
  - Anthropic Claude  (paid, ~$0.01-0.05 per session)
  - Google Gemini     (FREE tier - 15 req/min, 1M tokens/day)
"""

import streamlit as st

# -- Model options -------------------------------------------------------------
CLAUDE_MODELS = {
    "Claude Sonnet (Recommended - fast & smart)": "claude-sonnet-4-5",
    "Claude Haiku  (Fastest - good for simple tasks)": "claude-haiku-4-5-20251001",
    "Claude Opus   (Most powerful - slower)": "claude-opus-4-5",
}

GEMINI_MODELS = {
    "Gemini 1.5 Flash (FREE - fast & capable)": "gemini-1.5-flash",
    "Gemini 1.5 Pro   (FREE - most powerful)": "gemini-1.5-pro",
}

DEFAULT_CLAUDE_MODEL = "claude-sonnet-4-5"
DEFAULT_GEMINI_MODEL = "gemini-1.5-flash"


# -- Sidebar setup (call at the top of every app) -----------------------------
def setup_sidebar(tool_name: str, tool_description: str) -> tuple[str | None, str]:
    """
    Renders the standard sidebar with provider selector, API key input, and model.
    Returns (api_key, model_id). api_key is None if not entered.
    Model IDs starting with 'gemini' route to Google; others route to Anthropic.
    """
    with st.sidebar:
        st.title("\U0001f393 Academia AI Toolkit")
        st.caption(f"**{tool_name}**")
        st.markdown("---")

        # -- Provider choice ---------------------------------------------------
        st.subheader("\U0001f916 AI Provider")
        provider = st.radio(
            "Choose your provider",
            ["\u2728 Gemini (Google) - FREE", "Claude (Anthropic) - Paid"],
            index=0,
            help="Gemini is completely free. Claude costs ~$0.01-0.05 per session.",
        )
        use_gemini = provider.startswith("\u2728")

        st.markdown("---")

        # -- API Key -----------------------------------------------------------
        st.subheader("\U0001f511 API Key")

        if use_gemini:
            st.success(
                "**Gemini is free!** Get your key at "
                "[aistudio.google.com](https://aistudio.google.com) "
                "- 'Get API key' - No credit card needed.",
                icon="\U0001f389",
            )
            api_key = st.text_input(
                "Google AI Studio API Key",
                type="password",
                placeholder="AIza...",
                help="Free key from aistudio.google.com. Never stored.",
            )
        else:
            st.info(
                "New users get **$5 free credit** - enough for ~500 sessions. "
                "Get your key at [console.anthropic.com](https://console.anthropic.com).",
                icon="\U0001f4a1",
            )
            api_key = st.text_input(
                "Anthropic API Key",
                type="password",
                placeholder="sk-ant-...",
                help="Your key is never stored. It lives only in your browser session.",
            )

        st.markdown("---")

        # -- Model selector ----------------------------------------------------
        st.subheader("\u2699\ufe0f Model")
        if use_gemini:
            model_label = st.selectbox("Choose model", list(GEMINI_MODELS.keys()))
            model_id = GEMINI_MODELS[model_label]
        else:
            model_label = st.selectbox("Choose model", list(CLAUDE_MODELS.keys()))
            model_id = CLAUDE_MODELS[model_label]

        st.markdown("---")
        st.subheader("\u2139\ufe0f About this tool")
        st.info(tool_description)

        st.markdown("---")
        st.caption(
            "\U0001f512 Privacy: Your text is sent to the AI provider for processing. "
            "No data is stored by this toolkit."
        )

    return api_key or None, model_id


# -- Core AI call (routes to Gemini or Claude automatically) ------------------
def call_claude(
    api_key: str,
    model: str,
    system_prompt: str,
    user_message: str,
    max_tokens: int = 4096,
) -> str:
    """
    Calls the appropriate AI API based on model name and returns the text response.
    Models starting with 'gemini' go to Google; all others go to Anthropic.
    Raises ValueError with a user-friendly message on errors.
    """
    if model.startswith("gemini"):
        return _call_gemini(api_key, model, system_prompt, user_message, max_tokens)
    else:
        return _call_anthropic(api_key, model, system_prompt, user_message, max_tokens)


def _call_anthropic(api_key, model, system_prompt, user_message, max_tokens):
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
        return message.content[0].text
    except Exception as e:
        err = str(e).lower()
        if "authentication" in err or "api_key" in err or "invalid" in err:
            raise ValueError("\u274c Invalid API key. Check your key at console.anthropic.com")
        if "rate" in err:
            raise ValueError("\u23f3 Rate limit reached. Please wait a moment and try again.")
        raise ValueError(f"\u274c Anthropic API error: {str(e)}")


def _call_gemini(api_key, model, system_prompt, user_message, max_tokens):
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        gemini = genai.GenerativeModel(
            model_name=model,
            system_instruction=system_prompt,
        )
        response = gemini.generate_content(
            user_message,
            generation_config={"max_output_tokens": max_tokens},
        )
        return response.text
    except Exception as e:
        err = str(e).lower()
        if "api_key" in err or "invalid" in err or "permission" in err:
            raise ValueError("\u274c Invalid API key. Get a free key at aistudio.google.com")
        if "quota" in err or "rate" in err:
            raise ValueError("\u23f3 Free quota reached. Wait a minute and try again.")
        raise ValueError(f"\u274c Gemini API error: {str(e)}")


# -- Download button helper ---------------------------------------------------
def download_button(content: str, filename: str, label: str = "\u2b07\ufe0f Download Result"):
    """Renders a styled download button."""
    st.download_button(
        label=label,
        data=content,
        file_name=filename,
        mime="text/plain",
        use_container_width=True,
    )


# -- API key guard ------------------------------------------------------------
def require_api_key(api_key: str | None) -> bool:
    """
    Shows a prompt if no API key is provided.
    Returns True if key is present, False otherwise.
    """
    if not api_key:
        st.info(
            "\U0001f448 **Enter your API key in the sidebar to get started.**\n\n"
            "- **Free option:** Get a Google Gemini key at "
            "[aistudio.google.com](https://aistudio.google.com) - no credit card.\n"
            "- **Paid option:** Get a Claude key at "
            "[console.anthropic.com](https://console.anthropic.com) "
            "- $5 free credit for new users.",
            icon="\U0001f511",
        )
        return False
    return True
