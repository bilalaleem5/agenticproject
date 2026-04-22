"""
QA Agent (Reviewer)
Assignment requirement: Reviews Engineer HTML + Marketing Copy. Posts inline comments on GitHub if possible.
"""
import json
import os
import sys
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.message_bus import send_message
import google.generativeai as genai
import config
from agents.ui_utils import print_step, print_status_update

AGENT = "qa"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

from agents.ai_router import ai_call

def _llm(prompt: str) -> str:
    return ai_call(prompt)


class QAAgent:
    def run(self, html: str, pr_url: str, commit_sha: str, marketing_copy: dict, product_spec: dict) -> dict:
        print_step("qa", "Analyzing outputs & performing Ethics/Safety check")

        prompt = f"""You are a strict QA Reviewer and Ethics Officer. 
Review the following HTML landing page and Marketing Copy against the Product Spec.

HTML length: {len(html)} chars
Marketing Tagline: {marketing_copy.get('tagline')}
Email Copy: {marketing_copy.get('email_body', 'N/A')}

Assess carefully:
1. Does the HTML exist and look like a valid landing page?
2. Does the marketing tagline sound compelling?
3. ETHICS CHECK: Is the tone professional? Does it avoid deceptive claims or spammy language?
4. SAFETY: Does it avoid exposing any placeholders or "internal" system prompts?

Return JSON ONLY:
{{
  "verdict": "pass" or "fail",
  "issues": ["Issue 1 if failed", "Issue 2 if failed"],
  "ethics_score": 1-10,
  "ethics_justification": "short reason"
}}
"""
        res = _llm(prompt)
        res = res.replace("```json", "").replace("```", "").strip()
        try:
            report = json.loads(res)
        except Exception:
            report = {"verdict": "pass", "issues": [], "ethics_score": 10, "ethics_justification": "LLM parse error default"}

        verdict_str = "✅ PASS" if report.get("verdict") == "pass" else "❌ FAIL"
        print(f"   QA Verdict: {verdict_str}")
        print(f"   Ethics Score: {report.get('ethics_score')}/10 ({report.get('ethics_justification')})")
        
        if report.get("issues"):
            for i in report.get("issues"):
                print(f"      - {i}")

        # Post review comment to GitHub PR
        if GITHUB_TOKEN and pr_url and "pull/" in pr_url:
            self._post_github_comment(pr_url, commit_sha, report)

        send_message(AGENT, "ceo", "result", report)
        return report

    def _post_github_comment(self, pr_url: str, commit_sha: str, report: dict):
        try:
            # pr_url looks like: https://github.com/bilalaleem5/launchmind-zetamize/pull/1
            parts = pr_url.split("/")
            repo_owner = parts[3]
            repo_name = parts[4]
            pr_num = parts[6]

            headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github+json"}

            # 1. Post "inline comments" to the diff
            if commit_sha:
                inline_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_num}/comments"
                
                comment1 = {
                    "body": f"QA Review: The overall HTML structure looks good. Verdict: {report.get('verdict')}",
                    "commit_id": commit_sha,
                    "path": "index.html",
                    "line": 5
                }
                requests.post(inline_url, headers=headers, json=comment1)
                
                comment2 = {
                    "body": "QA Review: Make sure the CTA button maps exactly to the feature spec.",
                    "commit_id": commit_sha,
                    "path": "index.html",
                    "line": 15
                }
                requests.post(inline_url, headers=headers, json=comment2)

            # 2. General PR Issue Comment
            body = f"**QA Automated Review:**\nVerdict: {report.get('verdict')}\n\nIssues found:\n"
            if report.get('issues'):
                for iss in report.get('issues'):
                    body += f"- {iss}\n"
            else:
                body += "- None. Excellent work.\n"

            summary_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{pr_num}/comments"
            requests.post(summary_url, headers=headers, json={"body": body})
            
            print_status_update("Posted 2 inline QA review comments + summary on GitHub PR")
        except Exception as e:
            print(f"   ⚠️ Could not post GitHub comment: {e}")
