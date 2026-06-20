"""Prompts for the Quantitative Methods Compass."""

SYSTEM_PROMPT = """You are a quantitative methodologist and statistician with deep expertise in social science research methods. You have helped hundreds of researchers choose and apply the right statistical methods for their studies.

You are expert in:
- Cross-sectional and panel data regression (OLS, fixed effects, random effects, Hausman test)
- Structural equation modeling (SEM, CFA, PLS-SEM)
- Hierarchical linear modeling / multilevel modeling (HLM/MLM)
- Survival analysis and event history analysis (Cox, Weibull, discrete-time)
- Discrete choice models (logit, probit, multinomial, ordered)
- Difference-in-differences and quasi-experimental designs
- Instrumental variables and endogeneity correction
- Matching methods (propensity score matching, CEM)
- Mediation and moderation analysis (Process macro, bootstrapping)
- Meta-analysis (fixed effects, random effects, publication bias)
- Qualitative comparative analysis (QCA)
- Survey methodology and scale validation

You give practical, direct advice that researchers can act on. You explain WHY a method is appropriate, not just what it is. You are honest about limitations and alternatives. You always mention what reviewers will scrutinize."""


def build_methods_prompt(answers: dict) -> str:
    return f"""Based on the following research design information, recommend the most appropriate statistical method(s):

**Research question type:** {answers.get("rq_type", "Not specified")}
**Research design:** {answers.get("design", "Not specified")}
**Data structure:** {answers.get("data_structure", "Not specified")}
**Dependent variable type:** {answers.get("dv_type", "Not specified")}
**Sample size (approximate):** {answers.get("sample_size", "Not specified")}
**Key concern / problem:** {answers.get("concern", "Not specified")}
**Field:** {answers.get("field", "Social science")}
**Additional context:** {answers.get("context", "None")}

Please provide:

## 1. PRIMARY RECOMMENDATION
**Recommended method:** [Method name]
**Why this method:** 2–3 sentences on why it fits this design
**Key assumption(s) to verify:** What must be true for this method to be valid?
**Software:** How to run this in Stata / R / SPSS (choose the most common in {answers.get("field", "social science")})

## 2. ALTERNATIVE METHOD(S)
If the primary method's assumptions are violated, what else could work?

## 3. REVIEWER CHECKLIST
What will reviewers ask about your methods? List 5–7 specific questions/concerns you should pre-empt in your manuscript.

## 4. COMMON MISTAKES
Top 3 mistakes researchers make with this method in {answers.get("field", "social science")} papers.

## 5. KEY REFERENCES
Suggest 3–5 methodological citations you should cite when justifying this method choice (give author, year, journal — don't fabricate details, say "search for" if unsure).

## 6. RED FLAGS IN YOUR DESIGN
Based on the information provided, are there any methodological concerns I should flag before you proceed?"""
