"""
Shared utilities for the Academia AI Toolkit.
All tools import from this module.

Supports three AI providers:
  - Groq          (FREE — no credit card, sign up at console.groq.com)
  - Anthropic Claude  (paid, ~$0.01–0.05 per session)
  - Google Gemini     (free tier for personal Gmail in supported regions)
"""

import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()  # loads GROQ_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY from .env if present

# ── Model options ──────────────────────────────────────────────────────────────
GROQ_MODELS = {
    "Llama 3.3 70B (FREE — best quality)": "llama-3.3-70b-versatile",
    "Llama 3.1 8B  (FREE — fastest)": "llama-3.1-8b-instant",
    "Mixtral 8x7B  (FREE — long context)": "mixtral-8x7b-32768",
}

CLAUDE_MODELS = {
    "Claude Sonnet (Recommended — fast & smart)": "claude-sonnet-4-5",
    "Claude Haiku  (Fastest — good for simple tasks)": "claude-haiku-4-5-20251001",
    "Claude Opus   (Most powerful — slower)": "claude-opus-4-5",
}

GEMINI_MODELS = {
    "Gemini 2.0 Flash (fast & capable)": "gemini-2.0-flash",
    "Gemini 2.0 Flash Lite (fastest)": "gemini-2.0-flash-lite",
    "Gemini 1.5 Flash (stable)": "gemini-1.5-flash",
}


# ── Sidebar setup (call at the top of every app) ───────────────────────────────
def setup_sidebar(tool_name: str, tool_description: str) -> tuple[str | None, str]:
    """
    Renders the standard sidebar with provider selector, API key input, and model.
    Returns (api_key, model_id).
    Routing: model starts with 'llama'/'mixtral' → Groq; 'gemini' → Google; else → Anthropic.
    """
    with st.sidebar:
        st.title("🎓 Academia AI Toolkit")
        st.caption(f"**{tool_name}**")
        st.markdown("---")

        # ── Provider choice ────────────────────────────────────────────────────
        st.subheader("🤖 AI Provider")
        provider = st.radio(
            "Choose your provider",
            ["✨ Groq (FREE — no credit card)", "Claude (Anthropic)", "Gemini (Google)"],
            index=0,
            help="Groq is free with no credit card. Sign up at console.groq.com.",
        )

        st.markdown("---")

        # ── API Key ────────────────────────────────────────────────────────────
        st.subheader("🔑 API Key")

        if provider.startswith("✨ Groq"):
            st.success(
                "**Groq is free — no credit card needed.**\n\n"
                "1. Go to [console.groq.com](https://console.groq.com)\n"
                "2. Sign up (any email)\n"
                "3. Click **API Keys → Create API key**\n"
                "4. Paste it below",
                icon="🎉",
            )
            api_key = st.text_input(
                "Groq API Key",
                value=os.getenv("GROQ_API_KEY", ""),
                type="password",
                placeholder="gsk_...",
                help="Free key from console.groq.com. Save in .env to pre-fill.",
            )
            model_label = st.selectbox("Choose model", list(GROQ_MODELS.keys()))
            model_id = GROQ_MODELS[model_label]

        elif provider.startswith("Claude"):
            st.info(
                "Get a key at [console.anthropic.com](https://console.anthropic.com). "
                "Each session costs ~$0.01–0.05.",
                icon="💡",
            )
            api_key = st.text_input(
                "Anthropic API Key",
                value=os.getenv("ANTHROPIC_API_KEY", ""),
                type="password",
                placeholder="sk-ant-...",
                help="Save in .env to pre-fill.",
            )
            model_label = st.selectbox("Choose model", list(CLAUDE_MODELS.keys()))
            model_id = CLAUDE_MODELS[model_label]

        else:  # Gemini
            st.warning(
                "Gemini free tier requires a personal Gmail account and may not be "
                "available in all regions. Get a key at "
                "[aistudio.google.com](https://aistudio.google.com).",
                icon="⚠️",
            )
            api_key = st.text_input(
                "Google AI Studio API Key",
                value=os.getenv("GEMINI_API_KEY", ""),
                type="password",
                placeholder="AIza...",
                help="Save in .env to pre-fill.",
            )
            model_label = st.selectbox("Choose model", list(GEMINI_MODELS.keys()))
            model_id = GEMINI_MODELS[model_label]

        st.markdown("---")

        # ── Tool switcher ──────────────────────────────────────────────────────
        st.subheader("🔀 Switch Tool")
        TOOLS = {
            "📝 Reviewer Response Workbench":  "pages/1_Reviewer_Response_Workbench.py",
            "🔭 Research Gap Radar":           "pages/2_Research_Gap_Radar.py",
            "🧪 Theory → Hypothesis Builder":  "pages/3_Theory_Hypothesis_Builder.py",
            "🧭 Methods Compass":              "pages/4_Methods_Compass.py",
            "📋 Survey Instrument Forge":      "pages/5_Survey_Instrument_Forge.py",
            "🎯 Journal Fit Engine":           "pages/6_Journal_Fit_Engine.py",
            "📊 Synthesis Matrix Generator":   "pages/7_Synthesis_Matrix_Generator.py",
            "🔒 IRB Protocol Drafter":         "pages/8_IRB_Protocol_Drafter.py",
        }
        # Find the label matching current tool
        current_label = next(
            (k for k in TOOLS if tool_name.lower() in k.lower()), list(TOOLS.keys())[0]
        )
        selected = st.selectbox("Go to tool", list(TOOLS.keys()),
                                index=list(TOOLS.keys()).index(current_label))
        if selected != current_label:
            st.switch_page(TOOLS[selected])

        st.markdown("---")
        st.subheader("ℹ️ About this tool")
        st.info(tool_description)

        st.markdown("---")
        st.caption(
            "🔒 Privacy: Your text is sent to the AI provider for processing. "
            "No data is stored by this toolkit."
        )

    return api_key or None, model_id


# ── Core AI call (routes automatically by model name) ─────────────────────────
def call_claude(
    api_key: str,
    model: str,
    system_prompt: str,
    user_message: str,
    max_tokens: int = 4096,
) -> str:
    """
    Routes to the correct provider based on model name:
      - llama* / mixtral* / gemma* → Groq
      - gemini* → Google
      - everything else → Anthropic
    """
    if model.startswith(("llama", "mixtral", "gemma")):
        return _call_groq(api_key, model, system_prompt, user_message, max_tokens)
    elif model.startswith("gemini"):
        return _call_gemini(api_key, model, system_prompt, user_message, max_tokens)
    else:
        return _call_anthropic(api_key, model, system_prompt, user_message, max_tokens)


def _call_groq(api_key, model, system_prompt, user_message, max_tokens):
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content
    except Exception as e:
        err = str(e).lower()
        if "invalid" in err or "auth" in err or "api_key" in err or "401" in err:
            raise ValueError("❌ Invalid Groq API key. Check your key at console.groq.com")
        if "rate" in err or "429" in err:
            raise ValueError("⏳ Rate limit reached. Wait a moment and try again.")
        raise ValueError(f"❌ Groq API error: {str(e)}")


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
            raise ValueError("❌ Invalid API key. Check your key at console.anthropic.com")
        if "rate" in err:
            raise ValueError("⏳ Rate limit reached. Please wait a moment and try again.")
        raise ValueError(f"❌ Anthropic API error: {str(e)}")


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
            raise ValueError("❌ Invalid API key. Get a free key at aistudio.google.com")
        if "quota" in err or "rate" in err:
            raise ValueError("⏳ Quota/rate limit hit. Try switching to Groq instead (free, no regional restrictions).")
        raise ValueError(f"❌ Gemini API error: {str(e)}")


# ── Download button helper ─────────────────────────────────────────────────────
def download_button(content: str, filename: str, label: str = "⬇️ Download Result"):
    """Renders a styled download button."""
    st.download_button(
        label=label,
        data=content,
        file_name=filename,
        mime="text/plain",
        use_container_width=True,
    )


# ── API key guard ──────────────────────────────────────────────────────────────
def require_api_key(api_key: str | None) -> bool:
    """
    Shows a prompt if no API key is provided.
    Returns True if key is present, False otherwise.
    """
    if not api_key:
        st.info(
            "👈 **Enter your API key in the sidebar to get started.**\n\n"
            "- **Free (recommended):** Get a Groq key at "
            "[console.groq.com](https://console.groq.com) — no credit card needed.\n"
            "- **Paid:** Get a Claude key at "
            "[console.anthropic.com](https://console.anthropic.com).",
            icon="🔑",
        )
        return False
    return True
