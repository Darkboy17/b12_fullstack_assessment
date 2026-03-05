import json
import hmac
import hashlib
import requests
from datetime import datetime, timezone
import os

# ---- CONFIGURATION ----
SIGNING_SECRET = "hello-there-from-b12"
URL = "https://b12.io/apply/submission"

NAME = "Kordor Pyrbot"
EMAIL = "opcodegenerator@gmail.com"
RESUME_LINK = "https://drive.google.com/file/d/1yxrHW3OdqB-HJA0dxQGbTNHMo8RnOiXE/view?usp=sharing"
REPOSITORY_LINK = "https://github.com/Darkboy17/b12_fullstack_assessment"

# This is dynamically provided by GitHub Actions
ACTION_RUN_LINK = os.environ.get("ACTION_RUN_LINK")

# ---- CREATE ISO 8601 TIMESTAMP ----
timestamp = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")

# ---- CREATE PAYLOAD ----
payload = {
    "action_run_link": ACTION_RUN_LINK,
    "email": EMAIL,
    "name": NAME,
    "repository_link": REPOSITORY_LINK,
    "resume_link": RESUME_LINK,
    "timestamp": timestamp,
}

# ---- CANONICAL JSON (sorted keys, no whitespace) ----
body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")

# ---- CREATE HMAC SHA256 SIGNATURE ----
signature = hmac.new(
    SIGNING_SECRET.encode("utf-8"),
    body,
    hashlib.sha256
).hexdigest()

headers = {
    "Content-Type": "application/json",
    "X-Signature-256": f"sha256={signature}",
}

# ---- SEND POST REQUEST ----
response = requests.post(URL, data=body, headers=headers)

# ---- HANDLE RESPONSE ----
if response.status_code == 200:
    data = response.json()
    print("reponse:", data)
    receipt = data.get("receipt")
    print("Submission successful!")
    print("Receipt:", receipt)
else:
    print("Submission failed!")
    print("Status:", response.status_code)
    print("Response:", response.text)
    exit(1)