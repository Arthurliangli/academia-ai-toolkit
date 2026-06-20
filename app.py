"""
Academia AI Toolkit — Home
━━━━━━━━━━━━━━━━━━━━━━━━━
8 free AI tools for academic researchers. No coding required.
"""
import streamlit as st

st.set_page_config(
    page_title="Academia AI Toolkit",
    page_icon="🎓",
    layout="wide",
)

st.title("🎓 Academia AI Toolkit")
st.markdown("**8 free AI tools for social science researchers — pick a tool from the sidebar.**")
st.markdown("---")

tools = [
    ("📝", "Reviewer Response Workbench",   "pages/1_Reviewer_Response_Workbench.py",   "Turns reviewer comments into a professional response letter"),
    ("🔭", "Research Gap Radar",            "pages/2_Research_Gap_Radar.py",            "Finds under-explored opportunities in a literature set"),
    ("🧪", "Theory → Hypothesis Builder",   "pages/3_Theory_Hypothesis_Builder.py",     "Generates testable hypotheses from theoretical frameworks"),
    ("🧭", "Methods Compass",               "pages/4_Methods_Compass.py",               "Recommends the right statistical method for your design"),
    ("📋", "Survey Instrument Forge",       "pages/5_Survey_Instrument_Forge.py",       "Finds validated scales and generates survey items"),
    ("🎯", "Journal Fit Engine",            "pages/6_Journal_Fit_Engine.py",            "Matches your paper to the best-fit journals"),
    ("📊", "Synthesis Matrix Generator",    "pages/7_Synthesis_Matrix_Generator.py",    "Converts abstracts into a literature review table"),
    ("🔒", "IRB Protocol Drafter",          "pages/8_IRB_Protocol_Drafter.py",          "Drafts ethics applications section by section"),
]

cols = st.columns(2)
for i, (icon, name, page, desc) in enumerate(tools):
    with cols[i % 2]:
        with st.container(border=True):
            st.markdown(f"### {icon} {name}")
            st.caption(desc)
            if st.button("Open tool →", key=f"tool_{i}"):
                st.switch_page(page)

st.markdown("---")
st.markdown(
    "**Get a free API key:** [console.groq.com](https://console.groq.com) (no credit card needed) · "
    "[GitHub repo](https://github.com/Arthurliangli/academia-ai-toolkit)"
)
