# 🎓 Academia AI Toolkit

**8 free, no-code AI tools built specifically for social science researchers.**

Most AI tools are built for coders. This toolkit is built for faculty — people doing literature reviews at midnight, wrestling with reviewer comments, and staring at a blank IRB form. Each tool runs in your browser, requires no programming, and is designed around the actual workflows of academic research.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B.svg)](https://streamlit.io)
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)](CONTRIBUTING.md)

> Built by a business professor for business professors — and anyone else doing social science research.

---

## 🛠️ The 8 Tools

| # | Tool | What It Does | Best For |
|---|------|-------------|----------|
| 1 | [**Reviewer Response Workbench**](01_reviewer_response_workbench/) | Turns raw reviewer comments into a structured, professional response letter | R&R responses |
| 2 | [**Research Gap Radar**](02_research_gap_radar/) | Finds under-explored research opportunities from a set of abstracts | Starting a new project |
| 3 | [**Theory → Hypothesis Builder**](03_theory_hypothesis_builder/) | Generates logically structured hypotheses from your chosen theoretical lens | Hypothesis development |
| 4 | [**Quantitative Methods Compass**](04_methods_compass/) | Recommends the right statistical method for your research design | Methods section |
| 5 | [**Survey Instrument Forge**](05_survey_instrument_forge/) | Generates survey items and suggests validated scales for your constructs | Survey design |
| 6 | [**Journal Fit Engine**](06_journal_fit_engine/) | Matches your paper to the best-fit journals with ranked rationale | Submission targeting |
| 7 | [**Synthesis Matrix Generator**](07_synthesis_matrix_generator/) | Converts paper abstracts into a structured literature review table | Literature reviews |
| 8 | [**IRB Protocol Drafter**](08_irb_protocol_drafter/) | Drafts your IRB/ethics application section by section | Ethics applications |

---

## ⚡ Quick Start (5 minutes)

### Step 1 — Get an API key

These tools use the **Anthropic Claude API** or **Google Gemini API**. Get a Claude key at [console.anthropic.com](https://console.anthropic.com) (credits ~$0.01–0.05/session), or a Gemini key at [aistudio.google.com](https://aistudio.google.com) (free tier available for personal Gmail accounts in supported regions).

### Step 2 — Install Python (one time only)

Download Python from [python.org](https://www.python.org/downloads/) — choose version 3.10 or higher. Click "Install" and follow the prompts.

### Step 3 — Install Streamlit (one time only)

Open Terminal (Mac) or Command Prompt (Windows) and paste:

```bash
pip install streamlit anthropic python-dotenv
```

### Step 4 — Run any tool

Navigate to the tool folder and run:

```bash
cd 01_reviewer_response_workbench
streamlit run app.py
```

Your browser will open automatically. Enter your API key in the sidebar and you're ready.

### 🌐 No-install option

Click the "Deploy to Streamlit Cloud" button inside each tool's folder README to use it directly in your browser — no installation required. You'll just need your API key.

---

## 🎯 Why This Toolkit Is Different

Most "AI for researchers" tools on GitHub are:
- 🔴 Built for STEM, not social science
- 🔴 Require coding knowledge to use
- 🔴 Generic chatbot wrappers with no academic workflow logic
- 🔴 Student-focused, not faculty-focused

This toolkit is:
- ✅ Built for management, IB, sociology, psychology, education, and economics
- ✅ Zero coding required — just paste and click
- ✅ Understands reviewer dynamics, theory-building, and publication workflows
- ✅ Designed around real faculty pain points

---

## 📂 Repository Structure

```
academia-ai-toolkit/
├── shared/                          # Shared utilities used by all tools
│   └── utils.py
├── 01_reviewer_response_workbench/  # Tool 1
├── 02_research_gap_radar/           # Tool 2
├── 03_theory_hypothesis_builder/    # Tool 3
├── 04_methods_compass/              # Tool 4
├── 05_survey_instrument_forge/      # Tool 5
├── 06_journal_fit_engine/           # Tool 6
├── 07_synthesis_matrix_generator/   # Tool 7
├── 08_irb_protocol_drafter/         # Tool 8
└── README.md
```

Each tool folder contains:
- `app.py` — the tool itself
- `prompts.py` — the AI prompts (easy to customize for your discipline)
- `requirements.txt` — dependencies
- `README.md` — instructions and screenshots

---

## 🤝 Contributing

Contributions are very welcome — especially from researchers who know what's missing. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Ideas especially wanted:
- Discipline-specific prompt improvements (sociology, education, public health, etc.)
- Additional tools for qualitative research (interview coding, thematic analysis)
- Integrations with Zotero, Mendeley, or institutional repositories

---

## 🔒 Privacy

Your text is sent to Anthropic's API for processing. No data is stored by this toolkit. For sensitive data, review [Anthropic's privacy policy](https://www.anthropic.com/privacy). Never paste identifiable participant data or confidential information.

---

## 📖 Citation

If you use this toolkit in your research or teaching, a citation is appreciated:

```
@software{academia_ai_toolkit,
  author = {[Your Name]},
  title = {Academia AI Toolkit: AI Tools for Social Science Researchers},
  year = {2025},
  url = {https://github.com/[your-username]/academia-ai-toolkit}
}
```

---

## 📄 License

MIT License — free to use, modify, and distribute. See [LICENSE](LICENSE).

---

*Built with ❤️ for researchers who write papers, not code.*
