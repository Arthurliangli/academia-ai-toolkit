"""
Theory → Hypothesis Builder
━━━━━━━━━━━━━━━━━━━━━━━━━━
Generates logically structured, publication-ready hypotheses from your
chosen theoretical lens, independent variables, and research context.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from shared.utils import setup_sidebar, call_claude, download_button, require_api_key
from prompts import SYSTEM_PROMPT, THEORIES, build_hypothesis_prompt

st.set_page_config(
    page_title="Theory → Hypothesis Builder",
    page_icon="🧪",
    layout="wide",
)

api_key, model = setup_sidebar(
    tool_name="Theory → Hypothesis Builder",
    tool_description=(
        "Select a theoretical lens, specify your variables and context, "
        "and get publication-ready hypotheses with full theoretical mechanisms."
    ),
)

st.title("🧪 Theory → Hypothesis Builder")
st.markdown(
    "Generate logically grounded hypotheses (or propositions) with full theoretical mechanisms — "
    "ready for the Theory and Hypotheses section of your paper."
)
st.markdown("---")

# ── Paper type selection ──────────────────────────────────────────────────────
st.subheader("1️⃣ Paper Type")
paper_type = st.radio(
    "What kind of paper are you writing?",
    [
        "Empirical paper (AMJ/SMJ-style hypotheses)",
        "Theory/conceptual paper (AMR-style propositions)",
    ],
    horizontal=True,
)

st.markdown("---")

# ── Theory selection ──────────────────────────────────────────────────────────
st.subheader("2️⃣ Theoretical Foundation")

theory_choice = st.selectbox(
    "Select your primary theoretical lens",
    list(THEORIES.keys()),
    help="Don't see yours? Choose 'Other / Custom' and describe it below.",
)

if theory_choice != "Other / Custom":
    with st.expander(f"📖 What is {theory_choice}?"):
        st.info(THEORIES[theory_choice])
    custom_theory = ""
else:
    custom_theory = st.text_area(
        "Describe your theoretical framework",
        height=100,
        placeholder="Describe the key premises and predictions of your theoretical framework...",
    )

st.markdown("---")

# ── Variables and context ─────────────────────────────────────────────────────
st.subheader("3️⃣ Variables and Context")

col1, col2 = st.columns(2)
with col1:
    iv = st.text_area(
        "Independent variable(s) / key predictor(s)",
        height=100,
        placeholder="e.g., CEO tenure, board independence, degree of internationalization",
    )
    moderators = st.text_area(
        "Moderating variable(s) (optional)",
        height=100,
        placeholder="e.g., environmental uncertainty, firm size, host-country institutional distance",
    )

with col2:
    dv = st.text_area(
        "Dependent variable(s) / outcome(s)",
        height=100,
        placeholder="e.g., subsidiary performance, innovation output, firm survival",
    )
    context = st.text_area(
        "Research context",
        height=100,
        placeholder="e.g., Multinational enterprises operating in emerging markets, listed firms in S&P 500 2000–2020",
    )

st.markdown("---")

# ── Options ───────────────────────────────────────────────────────────────────
st.subheader("4️⃣ Options")
num_hypotheses = st.slider(
    "Number of hypotheses/propositions to generate",
    min_value=1,
    max_value=6,
    value=3,
)

# ── Generate ──────────────────────────────────────────────────────────────────
if st.button("🧪 Generate Hypotheses", use_container_width=True, type="primary"):
    if not require_api_key(api_key):
        pass
    elif not iv.strip():
        st.error("Please enter at least one independent variable.")
    elif not dv.strip():
        st.error("Please enter at least one dependent variable.")
    elif theory_choice == "Other / Custom" and not custom_theory.strip():
        st.error("Please describe your theoretical framework.")
    else:
        with st.spinner("Building your theoretical argument..."):
            try:
                result = call_claude(
                    api_key=api_key,
                    model=model,
                    system_prompt=SYSTEM_PROMPT,
                    user_message=build_hypothesis_prompt(
                        theory=theory_choice,
                        theory_description=custom_theory or THEORIES.get(theory_choice, ""),
                        dv=dv,
                        iv=iv,
                        moderators=moderators,
                        context=context,
                        num_hypotheses=num_hypotheses,
                        paper_type=paper_type,
                    ),
                    max_tokens=4096,
                )
                st.session_state["hypothesis_result"] = result
            except ValueError as e:
                st.error(str(e))

if "hypothesis_result" in st.session_state:
    st.markdown("---")
    st.subheader("📄 Your Hypotheses")
    st.info(
        "💡 These are AI-generated starting points. Review the theoretical logic carefully "
        "and refine based on your deeper knowledge of the literature."
    )
    st.markdown(st.session_state["hypothesis_result"])
    download_button(
        st.session_state["hypothesis_result"],
        "hypotheses.txt",
        "⬇️ Download Hypotheses",
    )
