"""Prompts for the Reviewer Response Workbench."""

SYSTEM_PROMPT = """You are an expert academic editor with 20+ years of experience handling peer review in top-tier social science journals (AMJ, AMR, SMJ, JAP, JIBS, Organization Science, and similar outlets).

You help authors craft professional, persuasive, and strategically sound responses to peer reviewer comments.

You understand:
- When to concede gracefully vs. push back diplomatically
- How to frame disagreements as "clarifications" or "additional analyses"
- The difference between major and minor revisions and how to prioritize
- How to demonstrate responsiveness without making unnecessary changes
- The importance of thanking reviewers genuinely without being obsequious

Your responses are:
- Professional and collegial in tone
- Specific and concrete (always reference page/section numbers and actual changes)
- Strategic (you think about what the reviewer really wants vs. what they literally said)
- Truthful (you never claim to have made changes that weren't made)"""


def build_response_prompt(
    comments: str,
    paper_title: str,
    journal: str,
    field: str,
    revision_round: str,
    author_notes: str,
) -> str:
    return f"""I need help crafting a professional response to peer reviewer comments.

**Paper title:** {paper_title}
**Journal:** {journal}
**Field/discipline:** {field}
**Revision round:** {revision_round}
**Author's notes/constraints:** {author_notes if author_notes else "None provided"}

**Reviewer comments:**
{comments}

Please:
1. Parse the comments and identify each distinct point (number them)
2. Classify each point: [MAJOR CONCEPTUAL] / [MAJOR METHODOLOGICAL] / [MINOR] / [EDITORIAL]
3. Draft a professional, specific response to each point
4. For each response, include a placeholder note like [MANUSCRIPT CHANGE: describe what change to make] so I know exactly what to revise
5. Write a brief, warm cover letter opening (2–3 sentences) that thanks the editor and reviewers

Format the full output as a ready-to-submit response letter, starting with the cover letter, then the point-by-point responses.

Use this format for each point:
---
**Reviewer X, Comment Y [CATEGORY]**

*Reviewer comment (quoted):* "..."

*Our response:* ...

[MANUSCRIPT CHANGE: ...]
---"""


def build_strategy_prompt(comments: str, field: str) -> str:
    return f"""Analyze these peer reviewer comments from a {field} paper and provide strategic advice BEFORE I draft responses.

**Reviewer comments:**
{comments}

Please provide:
1. **Overall diagnosis**: What is the reviewer's main concern? Are they likely to accept a well-argued rebuttal, or do they want to see actual new data/analysis?
2. **Dealbreakers**: Which comments MUST be addressed thoroughly to get acceptance?
3. **Strategic priorities**: In what order should I tackle these?
4. **Red flags**: Any comments that signal the reviewer may reject regardless?
5. **Tone advice**: What tone should I take with this reviewer?

Be direct and honest — even if the news is not great."""
