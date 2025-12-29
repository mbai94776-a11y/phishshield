import requests
import whois
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime

def analyze_url(url):
    findings = []

    # Normalize URL
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    parsed = urlparse(url)

    # HTTPS check
    if not url.startswith("https://"):
        findings.append("No HTTPS encryption")

    # IP-based URL
    if parsed.hostname.replace('.', '').isdigit():
        findings.append("IP-based URL detected")

    # Domain age
    try:
        domain_info = whois.whois(parsed.hostname)
        creation_date = domain_info.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        age_days = (datetime.now() - creation_date).days
        if age_days < 180:
            findings.append("Domain is newly registered")
    except:
        findings.append("Unable to verify domain age")

    # HTTP content analysis
    try:
        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")

        if soup.find("input", {"type": "password"}):
            findings.append("Login form detected")

        if len(soup.find_all("iframe")) > 0:
            findings.append("iFrame usage detected")

        external_scripts = [
            s for s in soup.find_all("script", src=True)
            if parsed.hostname not in s["src"]
        ]
        if len(external_scripts) > 5:
            findings.append("Excessive external scripts")

    except:
        findings.append("Site content could not be analyzed")

    # Risk scoring
    score = 0
    for f in findings:
        if "No HTTPS" in f: score += 20
        if "IP-based" in f: score += 30
        if "newly registered" in f: score += 25
        if "Login form" in f: score += 15
        if "iFrame" in f: score += 10
        if "external scripts" in f: score += 10

    score = min(score, 100)

    verdict = (
        "SAFE" if score < 30 else
        "SUSPICIOUS" if score < 70 else
        "HIGH RISK"
    )

    return {
        "url": url,
        "score": score,
        "verdict": verdict,
        "findings": findings
    }
