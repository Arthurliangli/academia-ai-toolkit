"""
Reviewer Response Workbench
━━━━━━━━━━━━━━━━━━━━━━━━━━
Turns raw reviewer comments into a structured, professional response letter.
No coding required — just paste, configure, and click.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from shared.utils import setup_sidebar, call_claude, download_button, require_api_key
from prompts import SYSTEM_PROMPT, build_response_prompt, build_strategy_prompt

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Reviewer Response Workbench",
    page_icon="📝",
    layout="wide",
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
api_key, model = setup_sidebar(
    tool_name="Reviewer Response Workbench",
    tool_description=(
        "Paste your reviewer comments and get a structured, "
        "professional point-by-point response letter — ready to submit."
    ),
)

# ── Header ────────────────────────────────────────────────────────────────────
st.title("📝 Reviewer Response Workbench")
st.markdown(
    "Turn reviewer comments into a professional response letter. "
    "Paste the comments below, fill in a few details, and click **Generate Response**."
)
st.markdown("---")

# ── Two tabs: Strategy first, then full response ──────────────────────────────
tab_strategy, tab_response = st.tabs(
    ["🧭 Step 1: Get Strategy Advice", "✍️ Step 2: Generate Full Response Letter"]
)

# ════════════════════════════════════════════════════════
# TAB 1 — STRATEGY
# ════════════════════════════════════════════════════════
with tab_strategy:
    st.subheader("🧭 Understand What the Reviewers Really Want")
    st.markdown(
        "Before writing your response, get strategic advice: which comments are "
        "dealbreakers, what tone to use, and where to focus your energy."
    )

    with st.expander("💡 Tips for pasting reviewer comments"):
        st.markdown(
            """
- Copy and paste exactly as received — formatting doesn't matter
- Include comments from all reviewers (label them Reviewer 1, Reviewer 2, etc.)
- Include the editor's letter if relevant
- If you have multiple pages of comments, paste them all — there's no limit
            """
        )

    comments_strategy = st.text_area(
        "Paste reviewer comments here",
        height=300,
        placeholder="Reviewer 1:\nThe theoretical framing in section 2 is unclear...\n\nReviewer 2:\n...",
        key="comments_strategy",
    )

    field_strategy = st.text_input(
        "Your field/discipline",
        placeholder="e.g., Strategic Management, International Business, Organizational Behavior",
        key="field_strategy",
    )

    if st.button("🧭 Analyze Comments & Get Strategy Advice", use_container_width=True, type="primary"):
        if not require_api_key(api_key):
            pass
        elif not comments_strategy.strip():
            st.error("Please paste the reviewer comments first.")
        else:
            with st.spinner("Analyzing reviewer comments..."):
                try:
                    result = call_claude(
                        api_key=api_key,
                        model=model,
                        system_prompt=SYSTEM_PROMPT,
                        user_message=build_strategy_prompt(
                            comments_strategy, field_strategy or "social science"
                        ),
                        max_tokens=2048,
                    )
                    st.session_state["strategy_result"] = result
                except ValueError as e:
                    st.error(str(e))

    if "strategy_result" in st.session_state:
        st.markdown("---")
        st.subheader("📋 Strategic Analysis")
        st.markdown(st.session_state["strategy_result"])
        download_button(
            st.session_state["strategy_result"],
            "reviewer_strategy.txt",
            "⬇️ Download Strategy Notes",
        )


# ════════════════════════════════════════════════════════
# TAB 2 — FULL RESPONSE
# ════════════════════════════════════════════════════════
with tab_response:
    st.subheader("✍️ Generate Your Response Letter")
    st.markdown("Fill in the details below and paste your reviewer comments to get a complete, ready-to-submit response letter.")

    col1, col2 = st.columns(2)
    with col1:
        paper_title = st.text_input(
            "Paper title",
            placeholder="e.g., CEO Power and Subsidiary Autonomy in MNEs",
        )
        journal = st.text_input(
            "Journal",
            placeholder="e.g., Journal of International Business Studies",
        )
    with col2:
        field = st.text_input(
            "Field/discipline",
            placeholder="e.g., International Business",
        )
        revision_round = st.selectbox(
            "Revision round",
            ["First revision (R1)", "Second revision (R2)", "Third revision (R3)", "Minor revision"],
        )

    author_notes = st.text_area(
        "Your notes / constraints (optional)",
        height=80,
        placeholder=(
            "e.g., 'We cannot collect new data — the survey window is closed.' "
            "or 'Reviewer 2's sample size concern cannot be addressed.'"
        ),
    )

    comments_response = st.text_area(
        "Paste reviewer comments",
        height=300,
        placeholder="Paste all reviewer comments here, labeled by reviewer number...",
        key="comments_response",
    )

    if st.button("✍️ Generate Full Response Letter", use_container_width=True, type="primary"):
        if not require_api_key(api_key):
            pass
        elif not comments_response.strip():
            st.error("Please paste reviewer comments.")
        elif not paper_title.strip():
            st.error("Please enter the paper title.")
        else:
            with st.spinner("Drafting your response letter... (this may take 30–60 seconds for long comments)"):
                try:
                    result = call_claude(
                        api_key=api_key,
                        model=model,
                        system_prompt=SYSTEM_PROMPT,
                        user_message=build_response_prompt(
                            comments=comments_response,
                            paper_title=paper_title,
                            journal=journal or "Not specified",
                            field=field or "Social science",
                            revision_round=revision_round,
                            author_notes=author_notes,
                        ),
                        max_tokens=4096,
                    )
                    st.session_state["response_result"] = result
                except ValueError as e:
                    st.error(str(e))

    if "response_result" in st.session_state:
        st.markdown("---")
        st.subheader("📄 Your Response Letter")
        st.info(
            "💡 Review carefully before submitting. Replace all [MANUSCRIPT CHANGE: ...] "
            "placeholders with your actual changes."
        )
        st.markdown(st.session_state["response_result"])
        download_button(
            st.session_state["response_result"],
            "reviewer_response_letter.txt",
            "⬇️ Download Response Letter",
        )
