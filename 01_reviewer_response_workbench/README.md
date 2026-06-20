# 📝 Reviewer Response Workbench

> Turn raw reviewer comments into a structured, professional response letter — in minutes, not days.

## What it does

Paste your peer reviewer comments and get:
- **Strategic analysis**: Which comments are dealbreakers? What tone to take?
- **Point-by-point response letter**: Ready to submit, with placeholder notes for manuscript changes
- **Comment categorization**: Major conceptual / Major methodological / Minor / Editorial

## Quick Start

```bash
pip install streamlit anthropic python-dotenv
streamlit run app.py
```

Then open your browser at `http://localhost:8501`, enter your API key in the sidebar, and paste your reviewer comments.

## How to use

1. **Tab 1 — Get strategy advice first**: Paste your comments and get a diagnosis before writing anything
2. **Tab 2 — Generate the full response**: Fill in paper title, journal, field, and get a complete letter

## Tips

- Works best with Claude Sonnet (the default model)
- For very long review packages (3+ reviewers), you may want to process one reviewer at a time
- The [MANUSCRIPT CHANGE: ...] placeholders tell you exactly what to revise — don't submit without replacing them

## Privacy

Your reviewer comments are sent to Anthropic's API for processing. Do not paste any information that must remain confidential under your review agreement.
