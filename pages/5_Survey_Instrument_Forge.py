import sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(ROOT, "05_survey_instrument_forge")
sys.path.insert(0, ROOT)
sys.path.insert(0, TOOL)
os.chdir(TOOL)
with open(os.path.join(TOOL, "app.py")) as _f:
    exec(_f.read(), {"__file__": os.path.join(TOOL, "app.py")})
