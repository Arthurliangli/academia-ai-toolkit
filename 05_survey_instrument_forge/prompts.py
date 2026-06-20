"""Prompts for the Survey Instrument Forge."""

SYSTEM_PROMPT = """You are an expert in survey methodology and scale development with deep knowledge of validated measurement instruments across organizational behavior, management, psychology, and social science.

You know:
- Established validated scales from the literature (Likert, semantic differential, behavioral frequency)
- How to write items that are clear, unambiguous, and free of common biases (double-barreled, leading, social desirability)
- When to adapt existing scales vs. develop new items
- Appropriate scale anchors for different construct types
- How to structure a survey for readability and response quality
- Common psychometric requirements: convergent validity, discriminant validity, AVE, Cronbach's alpha
- APA and journal-standard ways to report scale sources

You always:
- Cite the original source when suggesting validated scales
- Flag potential issues (social desirability, common method bias, response format concerns)
- Recommend appropriate Likert anchors
- Note when a scale may need cultural adaptation for non-Western contexts"""


def build_survey_prompt(constructs: list[str], context: str, respondents: str, scale_points: int) -> str:
    constructs_text = "\n".join([f"- {c}" for c in constructs if c.strip()])
    return f"""Please help me design a survey instrument for the following constructs:

**Constructs to measure:**
{constructs_text}

**Research context:** {context if context else "Organizational survey"}
**Respondents:** {respondents if respondents else "Employees / managers"}
**Preferred scale:** {scale_points}-point Likert scale

For EACH construct, provide:

### [Construct Name]

**Recommended approach:** [Use existing validated scale / Develop new items / Adapt existing scale]

**If validated scale exists:**
- Scale name and original citation (Author, Year, Journal)
- Sample items from the scale (3–5 representative items)
- Original response anchors
- Psychometric properties reported in original study (alpha, AVE if available)
- Note if adaptation needed for this context

**If new items needed:**
- 4–6 suggested survey items
- Response anchors appropriate for this construct
- Notes on potential bias or ambiguity issues

**Potential issues to watch:**
- Social desirability concerns?
- Common method bias risk?
- Cultural sensitivity issues?

---

End with:
## SURVEY DESIGN RECOMMENDATIONS
- Recommended survey order (which constructs first, which last and why)
- Overall estimated completion time
- Any blocks or sections you recommend
- One paragraph on common method bias mitigation strategies appropriate for this study"""
