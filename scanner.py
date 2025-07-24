import subprocess
import tempfile
import shutil
import os
import json
from datetime import datetime

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")


def clone_and_scan(repo_url):
    # Connect to MongoDB (local or Atlas)
    client = MongoClient(MONGO_URI)
    db = client["devsecops"]
    collection = db["scans"]

    try:
        temp_dir = tempfile.mkdtemp()

        # Clone the GitHub repo
        subprocess.run(["git", "clone", repo_url, temp_dir], check=True)

        # Delete the .git folder to avoid permission errors
        git_folder = os.path.join(temp_dir, ".git")
        if os.path.exists(git_folder):
            shutil.rmtree(git_folder, ignore_errors=True)

        # Run Bandit on the cleaned repo
        result = subprocess.run(
            ["bandit", "-r", temp_dir, "-f", "json"],
            capture_output=True,
            text=True,
            check=False
        )

        # Cleanup cloned repo
        shutil.rmtree(temp_dir, ignore_errors=True)

        if result.stdout:
            output = json.loads(result.stdout)
            issues_raw = output.get("results", [])
            issues_clean = []

            for issue in issues_raw:
                issues_clean.append({
                    "filename": issue.get("filename"),
                    "line_number": issue.get("line_number"),
                    "issue_severity": issue.get("issue_severity"),
                    "issue_text": issue.get("issue_text"),
                    "code": issue.get("code").strip() if issue.get("code") else "",
                })

            risk_score = len(issues_clean) * 1.5

            scan_data = {
                "repo": repo_url,
                "date": datetime.now().isoformat(),
                "vulnerabilities": issues_clean,
                "risk_score": round(risk_score, 2),
            }
            collection.insert_one(scan_data)

            return {
                "vulnerabilities": issues_clean,
                "risk_score": round(risk_score, 2),
                "summary": output.get("metrics", {})
            }

        else:
            return {"vulnerabilities": [], "risk_score": 0.0, "summary": {}}

    except Exception as e:
        return {"error": str(e), "vulnerabilities": [], "risk_score": 0.0}
