from flask import Flask, render_template, request, jsonify
from urllib.parse import urlparse
from datetime import datetime
import whois
import os

app = Flask(__name__)

def analyze_url(url):
    reasons = []
    score = 0

    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    parsed = urlparse(url)
    domain = parsed.hostname or ""

    # HTTPS check
    if not url.startswith("https://"):
        reasons.append("The website does not use HTTPS encryption.")
        score += 20

    # IP-based URL
    if domain.replace(".", "").isdigit():
        reasons.append("The URL uses an IP address instead of a domain name.")
        score += 30

    # Suspicious keywords
    keywords = ["login", "verify", "secure", "update", "account", "bank"]
    for k in keywords:
        if k in url.lower():
            reasons.append(f"The URL contains a suspicious keyword: '{k}'.")
            score += 10
            break

    # Domain age
    try:
        info = whois.whois(domain)
        created = info.creation_date
        if isinstance(created, list):
            created = created[0]
        age_days = (datetime.now() - created).days
        if age_days < 180:
            reasons.append("The domain was registered recently, which is common in phishing sites.")
            score += 25
    except:
        reasons.append("Domain age could not be verified.")
        score += 10

    score = min(score, 100)

    verdict = (
        "SAFE" if score < 30 else
        "SUSPICIOUS" if score < 70 else
        "HIGH RISK"
    )

    return {
        "url": url,
        "verdict": verdict,
        "score": score,
        "reasons": reasons
    }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    data = request.json
    result = analyze_url(data.get("url", ""))
    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
