# Contributing to Academia AI Toolkit

Thank you for helping make this toolkit better for researchers! Contributions from both researchers (who know the workflows) and developers (who know the code) are equally welcome.

## Ways to Contribute

### 🔬 If you're a researcher (no coding required)

**The most valuable contributions are:**
- Sharing which parts of the tool worked well or didn't for your specific discipline
- Suggesting better prompt wording for tools in your field
- Requesting new tools for workflows we haven't covered
- Reporting when AI output is misleading or inaccurate for your use case

To contribute this way: [open an Issue](../../issues/new/choose) and choose "Feature Request" or "Prompt Improvement."

### 💻 If you're a developer

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Test that the Streamlit app runs: `streamlit run app.py`
5. Submit a pull request

## Guidelines

- **Keep tools non-technical**: Each tool must be usable by someone with zero coding experience
- **No hardcoded API keys**: Always use the sidebar input for API keys
- **Prompts are the product**: The AI prompts in `prompts.py` are the core of each tool — treat them like code
- **Discipline coverage**: We especially welcome improvements for qualitative methods, education research, public health, sociology, and non-US academic contexts
- **Privacy first**: Do not add any analytics, logging, or data collection

## Adding a New Tool

Each tool lives in its own folder and must include:
- `app.py` — the Streamlit app
- `prompts.py` — the AI prompts (separated for easy customization)
- `requirements.txt` — dependencies
- `README.md` — instructions and use case

Copy the structure of an existing tool to get started.

## Code Style

- Python 3.10+
- Use type hints
- Keep functions small and focused
- Comment the "why", not the "what"

## Questions?

Open an issue — no question is too basic.
