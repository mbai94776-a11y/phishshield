from flask import Flask, request, jsonify, send_file
from analyzer import analyze_url
from report import generate_pdf
from io import BytesIO

app = Flask(__name__)

@app.route("/scan", methods=["POST"])
def scan():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    result = analyze_url(url)
    return jsonify(result)

@app.route("/download", methods=["POST"])
def download():
    result = request.json
    if not result:
        return "No scan data", 400

    pdf_buffer = generate_pdf(result)

    return send_file(
        pdf_buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="phishshield_report.pdf"
    )
