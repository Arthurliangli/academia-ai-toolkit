#!/bin/bash
# ─────────────────────────────────────────────────────────────
#  Academia AI Toolkit — Tool Launcher
#  Double-click this file to run a tool in your browser.
# ─────────────────────────────────────────────────────────────

BASE="/Users/liliang/Claude/Projects/Github ideas for helping academia-AI interaction"
cd "$BASE"

echo ""
echo "════════════════════════════════════════════════"
echo "  Academia AI Toolkit — Tool Launcher"
echo "════════════════════════════════════════════════"
echo ""
echo "Installing dependencies (first run may take a minute)..."
pip install streamlit anthropic groq google-generativeai python-dotenv --quiet --break-system-packages 2>/dev/null || \
pip install streamlit anthropic groq google-generativeai python-dotenv --quiet

echo ""
echo "Starting Academia AI Toolkit..."
echo "→ It will open automatically in your browser."
echo "→ Switch tools from the sidebar — no restart needed."
echo "→ To stop, press Ctrl+C in this window."
echo ""

streamlit run "$BASE/app.py"

echo ""
read -p "Press Enter to close..."
