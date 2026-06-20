import sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(ROOT, "08_irb_protocol_drafter")

# Remove old tool directories from sys.path
sys.path = [p for p in sys.path if not any(
    p.endswith(d) for d in [
        "01_reviewer_response_workbench", "02_research_gap_radar",
        "03_theory_hypothesis_builder", "04_methods_compass",
        "05_survey_instrument_forge", "06_journal_fit_engine",
        "07_synthesis_matrix_generator", "08_irb_protocol_drafter"
    ]
)]

# Insert current tool directory at front
sys.path.insert(0, ROOT)
sys.path.insert(0, TOOL)

# Clear any cached tool-specific modules so they re-import from TOOL
for _mod in list(sys.modules.keys()):
    if _mod in ("prompts", "app") or _mod.startswith("prompts."):
        del sys.modules[_mod]

os.chdir(TOOL)
with open(os.path.join(TOOL, "app.py")) as _f:
    exec(_f.read(), {"__file__": os.path.join(TOOL, "app.py")})
