"""
IRB / Ethics Protocol Drafter
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Answer questions about your study and get a complete draft IRB/ethics
application — ready to adapt for your institution's form.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from shared.utils import setup_sidebar, call_claude, download_button, require_api_key
from prompts import SYSTEM_PROMPT, build_irb_prompt

st.set_page_config(
    page_title="IRB Protocol Drafter",
    page_icon="🔒",
    layout="wide",
)

api_key, model = setup_sidebar(
    tool_name="IRB Protocol Drafter",
    tool_description=(
        "Answer questions about your study and get a complete draft IRB/ethics "
        "application — ready to adapt for your institution."
    ),
)

st.title("🔒 IRB / Ethics Protocol Drafter")
st.markdown(
    "Answer questions about your study design to get a complete draft IRB/ethics protocol — "
    "covering purpose, recruitment, consent, risks, and data privacy."
)

st.info(
    "💡 This tool generates a **draft** protocol. You must review it carefully and adapt it "
    "to your institution's specific IRB form and requirements before submitting."
)
st.markdown("---")

title = st.text_input(
    "Study title",
    placeholder="e.g., Subsidiary Manager Autonomy and Innovation in Multinational Enterprises",
)

col1, col2 = st.columns(2)
with col1:
    study_type = st.selectbox(
        "Type of study",
        [
            "Online survey (anonymous)",
            "Online survey (identifiable)",
            "In-person survey",
            "Semi-structured interviews",
            "Focus groups",
            "Archival / secondary data only",
            "Observation (non-participatory)",
            "Mixed methods (survey + interviews)",
            "Experiment (online)",
            "Experiment (lab)",
        ],
    )

    participants = st.text_input(
        "Who are your participants?",
        placeholder="e.g., Mid-level managers at MNEs, MBA students, HR professionals",
    )

    recruitment = st.text_area(
        "How will you recruit participants?",
        height=80,
        placeholder="e.g., Email invitation via professional networks (LinkedIn), company HR contacts, MBA program participant pool",
    )

with col2:
    data_collection = st.text_area(
        "How will data be collected?",
        height=80,
        placeholder="e.g., Anonymous online survey via Qualtrics, 45-minute Zoom interview",
    )

    sensitive = st.selectbox(
        "Does the study involve sensitive topics?",
        [
            "No — standard workplace/organizational questions only",
            "Mild — some questions about work stress or interpersonal dynamics",
            "Moderate — questions about organizational wrongdoing, discrimination, or conflict",
            "Yes — personally sensitive topics (health, finance, illegal activity, etc.)",
        ],
    )

    country = st.text_input(
        "Your institution's country",
        placeholder="e.g., United States, UK, Canada, Hong Kong",
        value="United States",
    )

purpose = st.text_area(
    "Research purpose (in plain language)",
    height=100,
    placeholder=(
        "e.g., This study investigates how the degree of autonomy granted to subsidiary managers "
        "affects innovation outcomes in multinational enterprises. We will survey managers at "
        "100+ MNE subsidiaries to test theory-derived hypotheses about HQ-subsidiary relationships."
    ),
)

data_storage = st.text_area(
    "Data storage plan",
    height=80,
    placeholder=(
        "e.g., Data stored on university-encrypted server, accessible only to the PI and RA. "
        "Qualtrics responses de-identified before analysis. Raw data destroyed after 5 years."
    ),
)

if st.button("🔒 Draft IRB Protocol", use_container_width=True, type="primary"):
    if not require_api_key(api_key):
        pass
    elif not title.strip():
        st.error("Please enter a study title.")
    elif not purpose.strip():
        st.error("Please describe the research purpose.")
    else:
        answers = {
            "title": title,
            "study_type": study_type,
            "purpose": purpose,
            "participants": participants or "Not specified",
            "recruitment": recruitment or "Not specified",
            "data_collection": data_collection or "Not specified",
            "sensitive": sensitive,
            "data_storage": data_storage or "Not specified",
            "country": country,
        }
        with st.spinner("Drafting your IRB protocol..."):
            try:
                result = call_claude(
                    api_key=api_key,
                    model=model,
                    system_prompt=SYSTEM_PROMPT,
                    user_message=build_irb_prompt(answers),
                    max_tokens=4096,
                )
                st.session_state["irb_result"] = result
            except ValueError as e:
                st.error(str(e))

if "irb_result" in st.session_state:
    st.markdown("---")
    st.subheader("📄 IRB Protocol Draft")
    st.warning(
        "⚠️ This is a starting draft only. You must: (1) adapt it to your institution's "
        "specific IRB form, (2) have it reviewed by your department's research compliance "
        "officer if required, and (3) verify local regulations apply."
    )
    st.markdown(st.session_state["irb_result"])
    download_button(
        st.session_state["irb_result"],
        "irb_protocol_draft.txt",
        "⬇️ Download IRB Draft",
    )
