"""Prompts for the Theory → Hypothesis Builder."""

SYSTEM_PROMPT = """You are a leading organizational theorist and methodologist who has published extensively in AMJ, AMR, SMJ, and related journals. You specialize in developing theoretically grounded, logically airtight hypotheses and propositions.

You know that:
- A hypothesis must specify a direction (positive/negative/curvilinear) and be testable with data
- A proposition is used in theory papers (AMR-style) when empirical testing is not the immediate goal
- Hypotheses must be derived logically from theory — each step in the argument must be explicit
- Good hypotheses anticipate the mechanism (the "why"), not just the relationship (the "what")
- Moderating hypotheses must explain why the moderator changes the focal relationship
- Reviewers will ask for the theoretical mechanism — build it in from the start

You write at publication-ready quality: precise, formal, and appropriately hedged."""

THEORIES = {
    "Agency Theory": "Assumes principals (shareholders/HQ) and agents (managers/subsidiaries) have divergent interests. Predicts monitoring, incentive alignment, and information asymmetry effects.",
    "Resource-Based View (RBV)": "Competitive advantage stems from valuable, rare, inimitable, non-substitutable (VRIN) resources. Predicts heterogeneity in firm performance based on resource configurations.",
    "Institutional Theory": "Organizations conform to social, regulatory, and cognitive pressures (isomorphism). Predicts homogenization within organizational fields and legitimacy-seeking behavior.",
    "Transaction Cost Economics (TCE)": "Firms choose governance structures (market vs. hierarchy) to minimize transaction costs driven by uncertainty, asset specificity, and frequency.",
    "Upper Echelons Theory": "Top managers' decisions reflect their cognitive biases, values, and experiences. Predicts that TMT characteristics influence strategic outcomes.",
    "Stakeholder Theory": "Firms must balance claims of multiple stakeholders beyond shareholders. Predicts broader performance measurement and stakeholder-oriented decisions.",
    "Social Capital Theory": "Networks of relationships provide access to resources and information. Predicts advantages from structural position (bridging/bonding ties).",
    "Knowledge-Based View (KBV)": "Knowledge is the primary source of competitive advantage. Predicts that knowledge creation, transfer, and protection drive performance.",
    "Organizational Learning Theory": "Organizations improve performance through experience. Predicts exploration vs. exploitation trade-offs and learning curve effects.",
    "Signaling Theory": "Informational asymmetry leads observable signals to convey quality. Predicts how firms use certifications, credentials, and actions to communicate.",
    "Legitimacy Theory": "Organizations seek to conform to societal norms and values. Predicts proactive vs. reactive legitimacy management.",
    "Dynamic Capabilities": "Ability to integrate, build, and reconfigure competencies to address changing environments. Predicts adaptation in rapidly changing markets.",
    "Stewardship Theory": "Managers act as stewards of organizational resources, not self-interested agents. Alternative to agency theory for motivated, aligned managers.",
    "Internalization Theory / OLI Framework": "MNEs internalize cross-border transactions when market imperfections exist. Eclectic paradigm of FDI: Ownership, Location, Internalization advantages.",
    "Social Exchange Theory": "Relationships are governed by reciprocal exchange of resources. Predicts commitment, trust, and cooperation based on exchange history.",
    "Other / Custom": "I will describe my own theoretical framework.",
}


def build_hypothesis_prompt(
    theory: str,
    theory_description: str,
    dv: str,
    iv: str,
    moderators: str,
    context: str,
    num_hypotheses: int,
    paper_type: str,
) -> str:
    theory_text = (
        f"{theory}: {theory_description}"
        if theory != "Other / Custom"
        else theory_description
    )

    output_type = "hypotheses" if paper_type == "Empirical paper (AMJ/SMJ-style hypotheses)" else "propositions"

    return f"""Please develop {num_hypotheses} {output_type} for a {paper_type}.

**Theoretical foundation:** {theory_text}

**Dependent variable (outcome):** {dv}
**Independent variable(s) / key predictor(s):** {iv}
**Proposed moderator(s) (if any):** {moderators if moderators else "None"}
**Research context:** {context if context else "General organizational context"}

For each {output_type[:-1]}, provide:

1. **{output_type[:-1].capitalize()} [number]** (written as a formal, publication-ready statement)
   - *Theoretical mechanism*: 2–3 sentences explaining the causal logic step by step
   - *Key assumptions*: What must be true for this relationship to hold?
   - *Alternative explanations*: What competing prediction might a skeptic raise, and how does your theory address it?
   - *Measurement note*: Brief note on how the key variables are typically operationalized

End with:
**Overall theoretical narrative**: A 150-word paragraph connecting all {output_type} into a coherent theoretical model, suitable for use in the "Theory and Hypotheses" section of a manuscript."""
