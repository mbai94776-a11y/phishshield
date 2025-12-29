from fpdf import FPDF
from datetime import datetime
from io import BytesIO

def generate_pdf(result):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "PhishShield Security Report", ln=True)

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, f"URL: {result['url']}", ln=True)
    pdf.cell(0, 8, f"Scan Time: {datetime.now()}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Verdict: {result['verdict']}", ln=True)
    pdf.cell(0, 10, f"Risk Score: {result['score']}/100", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Detected Indicators:", ln=True)

    pdf.set_font("Arial", size=11)
    for f in result["findings"]:
        pdf.cell(0, 7, f"- {f}", ln=True)

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)

    return buffer
