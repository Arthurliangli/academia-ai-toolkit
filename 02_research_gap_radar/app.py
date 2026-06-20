"""
Research Gap Radar
━━━━━━━━━━━━━━━━━
Finds under-explored research opportunities from a set of abstracts.
Paste abstracts from your literature search and discover what hasn't been studied yet.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from shared.utils import setup_sidebar, call_claude, download_button, require_api_key
from prompts import SYSTEM_PROMPT, build_gap_analysis_prompt, build_question_refinement_prompt

st.set_page_config(
    page_title="Research Gap Radar",
    page_icon="🔭",
    layout="wide",
)

api_key, model = setup_sidebar(
    tool_name="Research Gap Radar",
    tool_description=(
        "Paste 10–100 abstracts from your literature search "
        "and discover under-explored research opportunities."
    ),
)

st.title("🔭 Research Gap Radar")
st.markdown(
    "Paste abstracts from your literature search to find what hasn't been studied — "
    "and turn gaps into publishable research directions."
)
st.markdown("---")

tab_analyze, tab_refine = st.tabs(
    ["🔍 Analyze Literature", "💡 Develop a Gap into a Research Direction"]
)

# ════════════════════════════════════════════════════════
# TAB 1 — ANALYZE
# ════════════════════════════════════════════════════════
with tab_analyze:
    col1, col2 = st.columns([2, 1])
    with col1:
        field = st.text_input(
            "Field / discipline",
            placeholder="e.g., International Business, Organizational Behavior",
        )
        focus_area = st.text_input(
            "Specific focus area (optional)",
            placeholder="e.g., subsidiary autonomy, CEO succession, board diversity",
        )
    with col2:
        st.markdown("**How to get abstracts:**")
        with st.expander("Show instructions"):
            st.markdown(
                """
1. Search Google Scholar, Web of Science, or Scopus
2. Export citations as text / CSV
3. Copy the abstracts column and paste below
4. Tip: 20–50 abstracts works best; 100+ is also fine
                """
            )

    abstracts = st.text_area(
        "Paste abstracts here (one per paragraph, or as exported from a database)",
        height=350,
        placeholder=(
            "Abstract 1:\nThis study examines...\n\n"
            "Abstract 2:\nDrawing on agency theory...\n\n"
            "Abstract 3:\n..."
        ),
    )

    st.caption(f"Characters pasted: {len(abstracts):,} | Approximate abstracts: ~{max(1, len(abstracts)//500)}")

    if st.button("🔭 Scan for Research Gaps", use_container_width=True, type="primary"):
        if not require_api_key(api_key):
            pass
        elif not abstracts.strip():
            st.error("Please paste some abstracts first.")
        elif len(abstracts.strip()) < 200:
            st.error("Please paste at least a few abstracts (more text gives better analysis).")
        else:
            with st.spinner("Scanning the literature... this may take 30–60 seconds."):
                try:
                    result = call_claude(
                        api_key=api_key,
                        model=model,
                        system_prompt=SYSTEM_PROMPT,
                        user_message=build_gap_analysis_prompt(
                            abstracts, field or "social science", focus_area
                        ),
                        max_tokens=4096,
                    )
                    st.session_state["gap_result"] = result
                except ValueError as e:
                    st.error(str(e))

    if "gap_result" in st.session_state:
        st.markdown("---")
        st.subheader("📊 Gap Analysis Results")
        st.markdown(st.session_state["gap_result"])
        download_button(
            st.session_state["gap_result"],
            "research_gap_analysis.txt",
            "⬇️ Download Gap Analysis",
        )
        st.info("💡 Copy a gap from above and use **Tab 2** to develop it into a full research direction.")


# ════════════════════════════════════════════════════════
# TAB 2 — DEVELOP A GAP
# ════════════════════════════════════════════════════════
with tab_refine:
    st.subheader("💡 Develop a Gap into a Research Direction")
    st.markdown(
        "Take a gap you've identified (from Tab 1 or elsewhere) and turn it into "
        "a specific research direction with a journal target."
    )

    gap_text = st.text_area(
        "Describe the research gap",
        height=150,
        placeholder=(
            "e.g., 'No studies examine how host-country institutional voids affect "
            "the degree of autonomy granted to local subsidiary managers in emerging markets, "
            "particularly in family-owned MNEs.'"
        ),
    )

    field_refine = st.text_input(
        "Your field",
        placeholder="e.g., International Business",
        key="field_refine",
    )

    if st.button("💡 Develop This Gap", use_container_width=True, type="primary"):
        if not require_api_key(api_key):
            pass
        elif not gap_text.strip():
            st.error("Please describe the research gap.")
        else:
            with st.spinner("Developing your research direction..."):
                try:
                    result = call_claude(
                        api_key=api_key,
                        model=model,
                        system_prompt=SYSTEM_PROMPT,
                        user_message=build_question_refinement_prompt(
                            gap_text, field_refine or "social science"
                        ),
                        max_tokens=2048,
                    )
                    st.session_state["refine_result"] = result
                except ValueError as e:
                    st.error(str(e))

    if "refine_result" in st.session_state:
        st.markdown("---")
        st.subheader("🎯 Research Direction")
        st.markdown(st.session_state["refine_result"])
        download_button(
            st.session_state["refine_result"],
            "research_direction.txt",
            "⬇️ Download Research Direction",
        )
