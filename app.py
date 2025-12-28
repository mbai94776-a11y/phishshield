from flask import Flask, render_template, request, jsonify
import requests
from urllib.parse import urlparse
import socket
import ssl

app = Flask(__name__)

def analyze_url(url):
    result = {
        "url": url,
        "risk": "SAFE",
        "score": 0,
        "reasons": []
    }

    parsed = urlparse(url)

    if parsed.scheme not in ["http", "https"]:
        result["risk"] = "DANGEROUS"
        result["score"] += 40
        result["reasons"].append("Invalid or missing URL scheme")

    if "@" in url:
        result["score"] += 20
        result["reasons"].append("URL contains '@' symbol")

    if len(parsed.netloc) > 50:
        result["score"] += 15
        result["reasons"].append("Very long domain name")

    suspicious_words = ["login", "verify", "secure", "update", "account"]
    for word in suspicious_words:
        if word in url.lower():
            result["score"] += 10
            result["reasons"].append(f"Suspicious keyword detected: {word}")

    try:
        hostname = parsed.hostname
        socket.gethostbyname(hostname)
    except:
        result["score"] += 20
        result["reasons"].append("Domain does not resolve")

    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=parsed.hostname) as s:
            s.connect((parsed.hostname, 443))
    except:
        result["score"] += 15
        result["reasons"].append("SSL certificate issue")

    if result["score"] >= 40:
        result["risk"] = "DANGEROUS"
    elif result["score"] >= 20:
        result["risk"] = "CAUTION"

    return result

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    return jsonify(analyze_url(url))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

