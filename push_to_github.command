#!/bin/bash
cd "/Users/liliang/Claude/Projects/Github ideas for helping academia-AI interaction"

echo ""
echo "════════════════════════════════════════════════"
echo "  Academia AI Toolkit — Pushing to GitHub"
echo "════════════════════════════════════════════════"
echo ""

# Read PAT from .pat file in same folder (never committed to GitHub)
if [ -f ".pat" ]; then
    GITHUB_PAT=$(cat ".pat" | tr -d '[:space:]')
    echo "🔑 Using saved token from .pat file"
else
    echo "Enter your GitHub PAT (repo scope, starts with ghp_):"
    read -s GITHUB_PAT
    echo ""
fi

python3 - "$GITHUB_PAT" << 'PYEOF'
import sys, base64, json
from pathlib import Path
from urllib import request, error

PAT  = sys.argv[1]
REPO = "Arthurliangli/academia-ai-toolkit"
BASE = Path("/Users/liliang/Claude/Projects/Github ideas for helping academia-AI interaction")
HEADERS = {
    "Authorization": f"token {PAT}",
    "Content-Type":  "application/json",
    "User-Agent":    "academia-ai-push",
}

def api(method, path, data=None):
    url  = f"https://api.github.com/repos/{REPO}/contents/{path}"
    body = json.dumps(data).encode() if data else None
    req  = request.Request(url, data=body, headers=HEADERS, method=method)
    try:
        with request.urlopen(req) as r:
            return json.loads(r.read())
    except error.HTTPError as e:
        body = json.loads(e.read())
        body["_http_status"] = e.code
        return body

def push(rel):
    full = BASE / rel
    if not full.exists():
        return
    content = base64.b64encode(full.read_bytes()).decode()
    existing = api("GET", rel)
    sha = existing.get("sha")
    payload = {"message": f"Update {rel}", "content": content}
    if sha:
        payload["sha"] = sha
    else:
        payload["message"] = f"Add {rel}"
    result = api("PUT", rel, payload)
    status = "✅" if "content" in result else "❌"
    print(f"  {status}  {rel}" + (f"  (HTTP {result.get('_http_status','?')}: {result.get('message','')})" if "content" not in result else ""))

files = [
    "app.py",
    "requirements.txt",
    "run_tool.command",
    "launch_tool1.command",
    "push_to_github.command",
    "README.md",
    "shared/utils.py",
    "pages/1_Reviewer_Response_Workbench.py",
    "pages/2_Research_Gap_Radar.py",
    "pages/3_Theory_Hypothesis_Builder.py",
    "pages/4_Methods_Compass.py",
    "pages/5_Survey_Instrument_Forge.py",
    "pages/6_Journal_Fit_Engine.py",
    "pages/7_Synthesis_Matrix_Generator.py",
    "pages/8_IRB_Protocol_Drafter.py",
    "01_reviewer_response_workbench/requirements.txt",
    "02_research_gap_radar/requirements.txt",
    "03_theory_hypothesis_builder/requirements.txt",
    "04_methods_compass/requirements.txt",
    "05_survey_instrument_forge/requirements.txt",
    "06_journal_fit_engine/requirements.txt",
    "07_synthesis_matrix_generator/requirements.txt",
    "08_irb_protocol_drafter/requirements.txt",
]

# Verify token
user_req = request.Request("https://api.github.com/user", headers=HEADERS, method="GET")
try:
    with request.urlopen(user_req) as r:
        user_info = json.loads(r.read())
        scopes = r.headers.get("X-OAuth-Scopes", "none")
    print(f"✅ Account: {user_info['login']}  |  Scopes: {scopes}")
except Exception as e:
    print(f"❌ Invalid token: {e}")
    sys.exit(1)

# Verify repo access
check_req = request.Request(f"https://api.github.com/repos/{REPO}", headers=HEADERS, method="GET")
try:
    with request.urlopen(check_req) as r:
        repo_info = json.loads(r.read())
    print(f"✅ Repo: {repo_info['full_name']}")
except error.HTTPError as e:
    print(f"❌ Cannot access repo: {json.loads(e.read()).get('message', str(e))}")
    sys.exit(1)

print("")
print("Uploading files to GitHub...")
for f in files:
    push(f)

print("")
print("Done! View at: https://github.com/Arthurliangli/academia-ai-toolkit")
PYEOF

echo ""
open "https://github.com/Arthurliangli/academia-ai-toolkit"
read -p "Press Enter to close..."
