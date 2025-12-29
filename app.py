from flask import Flask, render_template, request, jsonify, send_file
from analyzer import analyze_url
from report import generate_pdf

app = Flask(__name__)

last_result = None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    global last_result
    data = request.json
    result = analyze_url(data["url"])
    last_result = result
    return jsonify(result)

from flask import send_file

@app.route("/download")
def download():
    global last_result
    if not last_result:
        return "No report available", 400

    pdf_buffer = generate_pdf(last_result)
    return send_file(
        pdf_buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="phishshield_report.pdf"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
