"""Prompts for the Research Gap Radar."""

SYSTEM_PROMPT = """You are a senior research strategist and academic with deep expertise across social science disciplines including management, organizational behavior, international business, sociology, psychology, economics, and education.

You are world-class at reading a body of literature and identifying:
- What has been studied and what has not
- Which intersections of variables, contexts, and theories are unexplored
- Which findings are contradictory and need reconciliation
- Which contexts are over-studied vs. under-studied
- What methodological advances could open new research opportunities

Your analysis is precise, actionable, and grounded in academic norms. You frame gaps in terms of publishable research opportunities, not just missing information."""


def build_gap_analysis_prompt(abstracts: str, field: str, focus_area: str) -> str:
    return f"""Analyze the following set of research abstracts from {field} and identify research gaps and opportunities.

**Field:** {field}
**Specific focus area (if any):** {focus_area if focus_area else "No specific focus — analyze broadly"}

**Abstracts:**
{abstracts}

Please provide a structured analysis:

## 1. WHAT HAS BEEN STUDIED
Map the conceptual territory: What theories are used? What constructs are common? What contexts (countries, industries, organizational types) appear? What methods dominate?

## 2. PATTERNS AND THEMES
What are the 3–5 dominant research streams in this literature?

## 3. IDENTIFIED GAPS (prioritized by opportunity)
For each gap, provide:
- **Gap**: What is missing?
- **Why it matters**: Theoretical or practical significance
- **Suggested research question**: A specific, publishable research question that addresses this gap
- **Suggested approach**: Method, context, or theory that could address it
- **Estimated difficulty**: Low / Medium / High (based on data availability and theoretical development needed)

## 4. CONTRADICTORY FINDINGS
Are there any inconsistencies or conflicting findings across papers that represent a reconciliation opportunity?

## 5. TOP 3 RECOMMENDED OPPORTUNITIES
Based on impact, feasibility, and novelty, your top 3 recommended research directions."""


def build_question_refinement_prompt(gap: str, field: str) -> str:
    return f"""I've identified this research gap in {field}:

{gap}

Help me develop this into a publishable research direction:
1. Refine the research question to be specific and testable
2. Identify the most appropriate theoretical lens
3. Suggest the ideal empirical context
4. Draft a 150-word "contribution" paragraph suitable for a journal manuscript
5. Identify the top 3 journals where this would fit best"""
