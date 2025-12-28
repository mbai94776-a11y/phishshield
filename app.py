from flask import Flask, render_template, request, jsonify, send_file
import requests
import ssl
import socket
from datetime import datetime
from fpdf import FPDF
import io

app = Flask(__name__)

def analyze_url(url):
    score = 0
    reasons = []

    # HTTPS check
    if not url.startswith("https://"):
        score += 30
        reasons.append("No HTTPS encryption")

    # Domain age (simple heuristic)
    try:
        hostname = url.replace("https://", "").replace("http://", "").split("/")[0]
        socket.gethostbyname(hostname)
    except:
        score += 40
        reasons.append("Domain resolution failed")

    # Headers check
    try:
        r = requests.get(url, timeout=5)
        headers = r.headers
        if "Content-Security-Policy" not in headers:
            score += 10
            reasons.append("Missing CSP header")
        if "X-Frame-Options" not in headers:
            score += 10
            reasons.append("Missing X-Frame-Options")
    except:
        score += 20
        reasons.append("Request failed")

    label = "SAFE"
    if score > 70:
        label = "DANGEROUS"
    elif score > 40:
        label = "CAUTION"

    return {
        "score": score,
        "label": label,
        "reasons": reasons
    }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    url = request.json.get("url")
    result = analyze_url(url)
    return jsonify(result)

@app.route("/report", methods=["POST"])
def report():
    data = request.json
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "PhishShield Security Report", ln=True)
    pdf.cell(0, 10, f"URL: {data['url']}", ln=True)
    pdf.cell(0, 10, f"Risk Score: {data['score']}", ln=True)
    pdf.cell(0, 10, f"Status: {data['label']}", ln=True)

    pdf.ln(5)
    pdf.cell(0, 10, "Findings:", ln=True)
    for r in data["reasons"]:
        pdf.cell(0, 10, f"- {r}", ln=True)

    file = io.BytesIO()
    pdf.output(file)
    file.seek(0)

    return send_file(file, as_attachment=True, download_name="phishshield_report.pdf")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
