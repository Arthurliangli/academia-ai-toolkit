"""
Quantitative Methods Compass
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Answer questions about your research design and get a recommended
statistical method with reviewer checklist and common mistakes.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from shared.utils import setup_sidebar, call_claude, download_button, require_api_key
from prompts import SYSTEM_PROMPT, build_methods_prompt

st.set_page_config(
    page_title="Quantitative Methods Compass",
    page_icon="🧭",
    layout="wide",
)

api_key, model = setup_sidebar(
    tool_name="Quantitative Methods Compass",
    tool_description=(
        "Answer questions about your research design and get a recommended "
        "statistical method with rationale, reviewer checklist, and common mistakes."
    ),
)

st.title("🧭 Quantitative Methods Compass")
st.markdown(
    "Answer a few questions about your study design and data, "
    "and get a concrete method recommendation with everything you need to defend it."
)
st.markdown("---")

st.subheader("📋 Tell me about your study")

col1, col2 = st.columns(2)

with col1:
    rq_type = st.selectbox(
        "1. What type of relationship are you examining?",
        [
            "Direct effect (X → Y)",
            "Mediated relationship (X → M → Y)",
            "Moderated relationship (X → Y, moderated by Z)",
            "Moderated mediation (X → M → Y, with moderator)",
            "Group/category differences",
            "Change over time / trends",
            "Survival / event occurrence (when does something happen?)",
            "Prediction / forecasting",
            "Scale validation / measurement",
            "Meta-analysis / synthesizing prior studies",
        ],
    )

    design = st.selectbox(
        "2. What is your research design?",
        [
            "Survey (cross-sectional, one time point)",
            "Survey (longitudinal, multiple waves)",
            "Archival / secondary data (cross-sectional)",
            "Archival / secondary data (panel, multiple years)",
            "Experiment (lab)",
            "Quasi-experiment / natural experiment",
            "Mixed methods (qual + quant)",
            "Case study",
            "Other",
        ],
    )

    data_structure = st.selectbox(
        "3. What is your data structure?",
        [
            "Single level (e.g., individual employees only)",
            "Two-level nested (e.g., employees within firms)",
            "Three-level nested (e.g., employees within teams within firms)",
            "Panel / longitudinal (same units observed over time)",
            "Time-series (aggregate level over time)",
            "Cross-national (multiple countries)",
            "Dyadic (pairs, e.g., buyer-supplier)",
        ],
    )

with col2:
    dv_type = st.selectbox(
        "4. What type is your dependent variable?",
        [
            "Continuous (e.g., performance score, ROA, sales)",
            "Binary (yes/no, survived/failed, adopted/not adopted)",
            "Count (e.g., number of patents, alliances, employees)",
            "Ordered categorical (e.g., Likert scale 1–5, low/medium/high)",
            "Nominal categorical (e.g., industry, mode of entry)",
            "Time-to-event (e.g., years until firm exits, acquisition)",
            "Latent construct measured by survey items",
        ],
    )

    sample_size = st.selectbox(
        "5. Approximate sample size?",
        [
            "Very small (< 50)",
            "Small (50–200)",
            "Medium (200–500)",
            "Large (500–2,000)",
            "Very large (2,000–10,000)",
            "Big data (> 10,000)",
        ],
    )

    field = st.text_input(
        "6. Your field / discipline",
        placeholder="e.g., Strategic Management, Organizational Behavior",
    )

concern = st.text_area(
    "7. What is your main methodological concern or challenge? (optional but very helpful)",
    height=80,
    placeholder=(
        "e.g., 'I'm worried about endogeneity because firms self-select into treatment.' "
        "or 'My panel has missing data.' "
        "or 'I'm not sure if I need SEM or just regression.'"
    ),
)

context = st.text_area(
    "8. Any other context about your study? (optional)",
    height=80,
    placeholder="e.g., 'I have 10 years of panel data from Fortune 500 firms, N=300 firms, studying CEO succession effects on innovation.'",
)

if st.button("🧭 Get Method Recommendation", use_container_width=True, type="primary"):
    if not require_api_key(api_key):
        pass
    else:
        answers = {
            "rq_type": rq_type,
            "design": design,
            "data_structure": data_structure,
            "dv_type": dv_type,
            "sample_size": sample_size,
            "field": field or "social science",
            "concern": concern or "None specified",
            "context": context or "None",
        }
        with st.spinner("Analyzing your research design..."):
            try:
                result = call_claude(
                    api_key=api_key,
                    model=model,
                    system_prompt=SYSTEM_PROMPT,
                    user_message=build_methods_prompt(answers),
                    max_tokens=3000,
                )
                st.session_state["methods_result"] = result
            except ValueError as e:
                st.error(str(e))

if "methods_result" in st.session_state:
    st.markdown("---")
    st.subheader("📊 Method Recommendation")
    st.info(
        "💡 This is a starting point for your methods decision. Always verify with "
        "a methodologist or your coauthors, especially for complex designs."
    )
    st.markdown(st.session_state["methods_result"])
    download_button(
        st.session_state["methods_result"],
        "methods_recommendation.txt",
        "⬇️ Download Recommendation",
    )
