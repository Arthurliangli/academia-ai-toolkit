"""
Journal Fit Engine
━━━━━━━━━━━━━━━━━
Paste your abstract and get a ranked list of target journals with
rationale, submission tips, and honest fit assessment.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from shared.utils import setup_sidebar, call_claude, download_button, require_api_key
from prompts import SYSTEM_PROMPT, build_journal_fit_prompt

st.set_page_config(
    page_title="Journal Fit Engine",
    page_icon="🎯",
    layout="wide",
)

api_key, model = setup_sidebar(
    tool_name="Journal Fit Engine",
    tool_description=(
        "Paste your abstract and paper details to get a ranked list of "
        "best-fit journals with honest fit assessment and submission tips."
    ),
)

st.title("🎯 Journal Fit Engine")
st.markdown(
    "Get a ranked list of target journals based on your paper's content, method, "
    "and contribution — with honest advice on fit and submission strategy."
)
st.markdown("---")

abstract = st.text_area(
    "Paste your abstract",
    height=200,
    placeholder="Paste your full abstract here (150–300 words recommended)...",
)

col1, col2 = st.columns(2)
with col1:
    method = st.text_input(
        "Primary research method",
        placeholder="e.g., Panel data with fixed effects, Survey + SEM, Qualitative case study",
    )
    theory = st.text_input(
        "Theoretical lens(es)",
        placeholder="e.g., Agency theory + Institutional theory",
    )
with col2:
    field = st.text_input(
        "Field / discipline",
        placeholder="e.g., International Business, Strategic Management",
    )
    career_stage = st.selectbox(
        "Your career stage",
        [
            "PhD student / early career (publication record matters a lot)",
            "Assistant professor (need publications for tenure)",
            "Associate professor (established, can take bigger risks)",
            "Full professor (reputation provides flexibility)",
        ],
    )

contribution = st.text_area(
    "Core contribution (in 2–3 sentences)",
    height=80,
    placeholder=(
        "e.g., 'This paper challenges the dominant view that X leads to Y by showing that "
        "the relationship is moderated by Z. We extend agency theory to the HQ-subsidiary context "
        "and provide the first large-scale test of this moderation using 15 years of panel data.'"
    ),
)

if st.button("🎯 Find Best-Fit Journals", use_container_width=True, type="primary"):
    if not require_api_key(api_key):
        pass
    elif not abstract.strip():
        st.error("Please paste your abstract.")
    else:
        with st.spinner("Analyzing your paper and matching to journals..."):
            try:
                result = call_claude(
                    api_key=api_key,
                    model=model,
                    system_prompt=SYSTEM_PROMPT,
                    user_message=build_journal_fit_prompt(
                        abstract=abstract,
                        method=method,
                        theory=theory,
                        contribution=contribution,
                        field=field,
                        career_stage=career_stage,
                    ),
                    max_tokens=3000,
                )
                st.session_state["journal_result"] = result
            except ValueError as e:
                st.error(str(e))

if "journal_result" in st.session_state:
    st.markdown("---")
    st.subheader("📋 Journal Recommendations")
    st.info(
        "💡 These recommendations are based on the information provided. "
        "Rankings and journal scopes change over time — always verify with the journal's current aims & scope."
    )
    st.markdown(st.session_state["journal_result"])
    download_button(
        st.session_state["journal_result"],
        "journal_recommendations.txt",
        "⬇️ Download Recommendations",
    )
