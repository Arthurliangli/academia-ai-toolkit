"""Prompts for the Journal Fit Engine."""

SYSTEM_PROMPT = """You are a senior academic advisor and former associate editor who has reviewed for AMJ, AMR, SMJ, JIBS, Organization Science, JAP, JOM, JWB, IBR, and many other top-tier management and social science journals.

You have deep knowledge of:
- What each journal publishes (scope, theory focus, method preferences)
- Which journals favor which theoretical traditions
- Typical turnaround times and desk rejection rates
- ABS Academic Journal Guide rankings and SSCI impact factors
- How journals differ in their openness to qualitative, mixed-methods, and quantitative work
- The difference between journals that want 'novel contribution' vs. 'important replication'
- Regional emphases (North American vs. European perspectives in IB, for example)

You give honest, experienced advice — including flagging when a paper might be a poor fit for highly-ranked journals and suggesting strategic alternatives."""

JOURNAL_DATABASE = """
Key journal profiles (for reference):
- AMJ (Academy of Management Journal): Empirical, AMJ-style H1 H2 structure, top management journals, very high bar, 12–18 month review
- AMR (Academy of Management Review): Theory/conceptual only, no data, novel theoretical contribution, one of the hardest journals to publish in
- SMJ (Strategic Management Journal): Strategy focus, both quant and qual, M&A, competitive dynamics, RBV, upper echelons
- JIBS (Journal of International Business Studies): MNEs, FDI, cross-national management, institutional distance, cross-cultural
- Organization Science (Org Sci): Theory-rich, innovative methods welcome, micro and macro, complex systems
- JAP (Journal of Applied Psychology): Micro OB, individual level, psychometric rigor, strong methods
- JOM (Journal of Management): Broad management, good for meta-analyses and reviews, somewhat lower bar than AMJ
- JWB (Journal of World Business): International management, practical implications welcome, more accessible than JIBS
- IBR (International Business Review): IB topics, European perspective, accessible, good for emerging market studies
- ASQ (Administrative Science Quarterly): Institutional theory, sociology of organizations, innovative methods
- MOR (Management and Organization Review): China/emerging market focus, cross-cultural
- APJM (Asia Pacific Journal of Management): Asia-focused, international management, governance
- BJM (British Journal of Management): UK/European management, somewhat broader scope
- Long Range Planning: Strategy, planning, qualitative and quantitative
"""


def build_journal_fit_prompt(abstract: str, method: str, theory: str, contribution: str, field: str, career_stage: str) -> str:
    return f"""Help me identify the best journal targets for this paper.

**Abstract:**
{abstract}

**Primary method:** {method if method else "Not specified"}
**Theoretical lens(es):** {theory if theory else "Not specified"}
**Core contribution:** {contribution if contribution else "Not specified"}
**Field:** {field if field else "Management / Social science"}
**Author career stage:** {career_stage}

{JOURNAL_DATABASE}

Please provide:

## TOP 5 JOURNAL RECOMMENDATIONS

For each journal (ranked by fit, not prestige):

**[Journal Name] (ABS ranking / Impact factor if known)**
- **Why it fits**: 2–3 specific reasons this paper matches this journal's scope and preferences
- **Why it might not fit**: Honest assessment of potential weaknesses or risks
- **Similar published papers**: Describe 1–2 types of papers this journal has published that resemble yours (don't fabricate specific paper titles)
- **Submission tips**: Any journal-specific advice (e.g., "Position the contribution as extending X theory", "Editors here care about Y")
- **Estimated time to decision**: First round review time
- **Desk rejection risk**: Low / Medium / High — and why

## STRATEGIC ADVICE
Given the career stage ({career_stage}), what sequencing strategy would you recommend? Start with the top journal and work down, or target a "safe" journal first?

## RED FLAGS
Are there aspects of this paper as described that might limit its placement options? Be honest."""
