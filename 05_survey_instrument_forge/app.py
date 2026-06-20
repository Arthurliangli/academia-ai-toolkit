"""
Survey Instrument Forge
━━━━━━━━━━━━━━━━━━━━━━
Generate survey items and find validated scales for your constructs.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from shared.utils import setup_sidebar, call_claude, download_button, require_api_key
from prompts import SYSTEM_PROMPT, build_survey_prompt

st.set_page_config(
    page_title="Survey Instrument Forge",
    page_icon="📋",
    layout="wide",
)

api_key, model = setup_sidebar(
    tool_name="Survey Instrument Forge",
    tool_description=(
        "Enter your constructs and get validated scales with citations, "
        "or AI-generated items when no validated scale exists."
    ),
)

st.title("📋 Survey Instrument Forge")
st.markdown(
    "Enter the constructs you want to measure and get validated scales (with citations) "
    "or AI-generated survey items — plus design recommendations."
)
st.markdown("---")

# ── Context ───────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    context = st.text_input(
        "Research context",
        placeholder="e.g., Study of middle managers in MNEs, survey of R&D employees",
    )
    respondents = st.text_input(
        "Who are your respondents?",
        placeholder="e.g., Subsidiary managers, MBA students, HR directors",
    )
with col2:
    scale_points = st.select_slider(
        "Likert scale points",
        options=[5, 6, 7],
        value=7,
        help="7-point scales are most common in top management journals.",
    )

st.markdown("---")

# ── Construct entry ───────────────────────────────────────────────────────────
st.subheader("📝 Enter Your Constructs")
st.caption("Enter one construct per line. Be specific — 'job satisfaction' is clearer than 'employee attitudes'.")

constructs_text = st.text_area(
    "Constructs to measure (one per line)",
    height=200,
    placeholder=(
        "Subsidiary autonomy\n"
        "Organizational commitment\n"
        "Knowledge sharing\n"
        "Transformational leadership\n"
        "Innovation performance"
    ),
)

with st.expander("💡 Tips for naming constructs"):
    st.markdown(
        """
- Be specific: 'affective organizational commitment' > 'commitment'
- Specify the unit of analysis: 'subsidiary-level performance' vs 'individual performance'
- If you have a specific scale in mind (e.g., Podsakoff et al.'s transformational leadership), mention it
- For custom constructs with no obvious existing scale, describe what the construct captures
        """
    )

if st.button("📋 Design Survey Instrument", use_container_width=True, type="primary"):
    constructs = [c.strip() for c in constructs_text.strip().split("\n") if c.strip()]
    if not require_api_key(api_key):
        pass
    elif not constructs:
        st.error("Please enter at least one construct.")
    elif len(constructs) > 10:
        st.warning("You've entered more than 10 constructs. Consider processing in batches of 5–7 for best results.")
    else:
        with st.spinner(f"Finding scales for {len(constructs)} construct(s)... this may take a minute."):
            try:
                result = call_claude(
                    api_key=api_key,
                    model=model,
                    system_prompt=SYSTEM_PROMPT,
                    user_message=build_survey_prompt(
                        constructs=constructs,
                        context=context,
                        respondents=respondents,
                        scale_points=scale_points,
                    ),
                    max_tokens=4096,
                )
                st.session_state["survey_result"] = result
            except ValueError as e:
                st.error(str(e))

if "survey_result" in st.session_state:
    st.markdown("---")
    st.subheader("📄 Survey Instrument")
    st.warning(
        "⚠️ **Important**: Always verify scale citations by searching the original paper "
        "before using them in your manuscript. AI can occasionally misremember citation details."
    )
    st.markdown(st.session_state["survey_result"])
    download_button(
        st.session_state["survey_result"],
        "survey_instrument.txt",
        "⬇️ Download Survey Instrument",
    )
