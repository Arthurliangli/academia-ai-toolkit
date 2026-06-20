"""Prompts for the Synthesis Matrix Generator."""

SYSTEM_PROMPT = """You are an expert academic research assistant specializing in systematic literature reviews and meta-synthesis. You help researchers extract structured information from academic papers and organize it into publication-ready synthesis matrices.

You extract:
- Theoretical frameworks used
- Research context and setting (country, industry, level of analysis)
- Sample characteristics (N, type, time period)
- Key independent, dependent, and moderating variables
- Research methods and analytical approaches
- Main findings and effect directions
- Stated limitations
- Future research suggestions

You organize this into clean, structured tables and synthesized narratives that can be inserted directly into a literature review section."""


def build_matrix_prompt(papers: str, focus: str) -> str:
    return f"""Please extract and synthesize key information from the following academic papers/abstracts.

**Focus area / research topic:** {focus if focus else "General synthesis"}

**Papers / abstracts:**
{papers}

Please provide:

## 1. SYNTHESIS MATRIX (Table format)

Create a markdown table with these columns:
| Study (Author, Year) | Theory | Context/Sample | Method | Key IV(s) | Key DV(s) | Main Findings | Limitations |

Fill in each row from the provided papers. If information is missing from the abstract, write "NR" (Not Reported).

## 2. WRITTEN SYNTHESIS

Write a 300–400 word literature review paragraph that:
- Synthesizes the main themes across these studies
- Notes areas of convergence (where studies agree)
- Notes areas of divergence or contradiction
- Identifies patterns (e.g., "Studies in Western contexts find X, while emerging market studies find Y")
- Ends with a sentence pointing to gaps this body of literature leaves open

## 3. QUICK STATS OVERVIEW
- Number of studies analyzed:
- Dominant method:
- Most common theoretical lens:
- Most common context/setting:
- Time span of studies:

## 4. FUTURE RESEARCH DIRECTIONS MENTIONED
List the future research suggestions explicitly stated across these papers (useful for writing your own gaps section)."""
