#!/bin/bash
cd "/Users/liliang/Claude/Projects/Github ideas for helping academia-AI interaction"
pip install streamlit anthropic groq google-generativeai python-dotenv --quiet --break-system-packages 2>/dev/null || pip install streamlit anthropic groq google-generativeai python-dotenv --quiet
cd "01_reviewer_response_workbench"
streamlit run app.py
