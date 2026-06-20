"""
Synthesis Matrix Generator
━━━━━━━━━━━━━━━━━━━━━━━━━
Upload paper abstracts and get a structured synthesis table + written
literature review paragraph ready for your manuscript.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from shared.utils import setup_sidebar, call_claude, download_button, require_api_key
from prompts import SYSTEM_PROMPT, build_matrix_prompt

st.set_page_config(
    page_title="Synthesis Matrix Generator",
    page_icon="📊",
    layout="wide",
)

api_key, model = setup_sidebar(
    tool_name="Synthesis Matrix Generator",
    tool_description=(
        "Paste paper abstracts and get a structured synthesis matrix table "
        "plus a written literature review paragraph."
    ),
)

st.title("📊 Synthesis Matrix Generator")
st.markdown(
    "Paste abstracts from your target papers and get a structured synthesis table "
    "plus a written literature review paragraph — ready to drop into your manuscript."
)
st.markdown("---")

focus = st.text_input(
    "Research topic / focus area",
    placeholder="e.g., Subsidiary autonomy in MNEs, CEO succession and firm performance",
)

with st.expander("💡 How to get the best results"):
    st.markdown(
        """
- Paste **full abstracts** rather than just titles — more detail = better synthesis
- Include the **author and year** at the top of each abstract
- Works best with **5–25 papers** at a time (paste in batches for larger sets)
- Format each paper like this:
```
Smith & Jones (2022):
[abstract text]

Lee et al. (2021):
[abstract text]
```
        """
    )

papers = st.text_area(
    "Paste paper abstracts here",
    height=400,
    placeholder=(
        "Smith & Jones (2022):\n"
        "This study examines the relationship between board independence and firm performance...\n\n"
        "Lee et al. (2021):\n"
        "Drawing on agency theory, we investigate how CEO duality affects...\n\n"
        "Zhang & Wang (2023):\n"
        "..."
    ),
)

st.caption(f"Characters entered: {len(papers):,}")

if st.button("📊 Generate Synthesis Matrix", use_container_width=True, type="primary"):
    if not require_api_key(api_key):
        pass
    elif not papers.strip():
        st.error("Please paste some paper abstracts first.")
    elif len(papers.strip()) < 100:
        st.error("Please paste more abstract content for a meaningful synthesis.")
    else:
        with st.spinner("Building your synthesis matrix... (may take 30–60 seconds for many papers)"):
            try:
                result = call_claude(
                    api_key=api_key,
                    model=model,
                    system_prompt=SYSTEM_PROMPT,
                    user_message=build_matrix_prompt(papers, focus),
                    max_tokens=4096,
                )
                st.session_state["matrix_result"] = result
            except ValueError as e:
                st.error(str(e))

if "matrix_result" in st.session_state:
    st.markdown("---")
    st.subheader("📋 Synthesis Matrix & Literature Review")
    st.info(
        "💡 Copy the table into Word or Excel for easier formatting. "
        "The written synthesis can be pasted directly into your manuscript as a starting draft."
    )
    st.markdown(st.session_state["matrix_result"])
    download_button(
        st.session_state["matrix_result"],
        "synthesis_matrix.txt",
        "⬇️ Download Synthesis Matrix",
    )
