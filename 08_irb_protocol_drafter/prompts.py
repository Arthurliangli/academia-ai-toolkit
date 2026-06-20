"""Prompts for the IRB/Ethics Protocol Drafter."""

SYSTEM_PROMPT = """You are an expert in research ethics and IRB (Institutional Review Board) protocols for social science research. You have helped hundreds of researchers navigate ethics applications for surveys, interviews, archival studies, and mixed-methods research.

You specialize in:
- Social science research ethics (management, sociology, psychology, education, public health)
- Survey-based studies (online and paper)
- Interview and qualitative studies
- Archival and secondary data studies
- Cross-national research ethics considerations
- Exempt vs. expedited vs. full review determination
- Informed consent best practices
- Data privacy and storage protocols (GDPR, HIPAA considerations for research)
- Vulnerable populations in research

You write clear, professional language appropriate for institutional ethics review. You flag when studies may require extra scrutiny and suggest how to address potential concerns proactively."""


def build_irb_prompt(answers: dict) -> str:
    return f"""Please help me draft an IRB/ethics protocol application for the following study.

**Study title:** {answers.get("title", "Not provided")}
**Study type:** {answers.get("study_type", "Not specified")}
**Research purpose:** {answers.get("purpose", "Not specified")}
**Participant type:** {answers.get("participants", "Not specified")}
**Recruitment method:** {answers.get("recruitment", "Not specified")}
**Data collection method:** {answers.get("data_collection", "Not specified")}
**Sensitive topics involved?** {answers.get("sensitive", "No")}
**Data storage plan:** {answers.get("data_storage", "Not specified")}
**Institution country:** {answers.get("country", "United States")}

Please draft the following sections:

## 1. STUDY PURPOSE AND BACKGROUND (150 words)
Formal description of the study's purpose and scientific rationale, suitable for IRB review.

## 2. PARTICIPANT RECRUITMENT
- Inclusion and exclusion criteria
- Recruitment procedure (step-by-step)
- Sample size justification (brief)

## 3. PROCEDURES
Step-by-step description of what participants will experience, from recruitment through data collection.

## 4. RISKS AND BENEFITS
- Potential risks (physical, psychological, social, economic, privacy)
- Risk mitigation strategies
- Anticipated benefits to participants and to science

## 5. INFORMED CONSENT PLAN
- Consent process description
- Draft a brief informed consent statement (suitable to adapt for your form)

## 6. DATA PRIVACY AND CONFIDENTIALITY
- How will data be stored, protected, and eventually destroyed?
- Who will have access to identifiable information?
- Anonymization/de-identification procedures

## 7. REVIEW LEVEL RECOMMENDATION
Based on this study design, recommend: Exempt / Expedited / Full Board Review — and explain why.

## 8. POTENTIAL CONCERNS AND HOW TO ADDRESS THEM
Flag any aspects of this study that reviewers may question, and suggest how to preemptively address them in your application."""
