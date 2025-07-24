import datetime
import os

from flask import Flask, request, jsonify
from scanner import clone_and_scan
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

app = Flask(__name__)

@app.route("/scan", methods=["POST"])
def scan_repo():
    data = request.json
    repo_url = data.get("repo_url")

    if not repo_url:
        return jsonify({"error": "Missing repo_url"}), 400

    scan_result = clone_and_scan(repo_url)
    scan_result["repo"] = repo_url
    scan_result["date"] = datetime.datetime.now().isoformat()

    return jsonify(scan_result)

@app.route("/history", methods=["GET"])
def get_history():
    from pymongo import MongoClient
    client = MongoClient(MONGO_URI)
    db = client["devsecops"]
    collection = db["scans"]

    # Sort by newest first
    scans = list(collection.find({}, {"_id": 0}).sort("date", -1))
    return jsonify(scans)


if __name__ == "__main__":
    app.run(debug=True)
