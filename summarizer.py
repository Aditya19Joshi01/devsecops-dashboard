import os
import requests
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}


def summarize_text(text):
    if not text.strip():
        print("[DEBUG] Empty input text for summarization.")
        return "No vulnerabilities found to summarize."

    print("[DEBUG] Sending request to Hugging Face summarization API...")
    response = requests.post(API_URL, headers=HEADERS, json={"inputs": text})

    print(f"[DEBUG] Status Code: {response.status_code}")
    try:
        print("[DEBUG] Raw Response:", response.json())
    except Exception as e:
        print(f"[DEBUG] Failed to parse response JSON: {e}")
        print(f"[DEBUG] Response Content: {response.text}")

    if response.status_code == 200:
        try:
            return response.json()[0]['summary_text']
        except Exception as e:
            print(f"[DEBUG] JSON format error: {e}")
            return "⚠️ Received malformed response from summarizer."
    else:
        return "⚠️ Could not summarize vulnerabilities."

