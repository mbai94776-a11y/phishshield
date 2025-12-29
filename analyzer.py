import whois
from urllib.parse import urlparse
from datetime import datetime

def analyze_url(url):
    findings = []
    score = 0

    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    parsed = urlparse(url)
    hostname = parsed.hostname

    # HTTPS
    if not url.startswith("https://"):
        findings.append("No HTTPS encryption")
        score += 20

    # IP-based URL
    if hostname.replace(".", "").isdigit():
        findings.append("IP-based URL detected")
        score += 30

    # Suspicious keywords
    suspicious_words = ["login", "verify", "secure", "update", "account"]
    for word in suspicious_words:
        if word in url.lower():
            findings.append(f"Suspicious keyword in URL: {word}")
            score += 10

    # Domain age
    try:
        domain_info = whois.whois(hostname)
        created = domain_info.creation_date
        if isinstance(created, list):
            created = created[0]
        age_days = (datetime.now() - created).days
        if age_days < 180:
            findings.append("Domain recently registered")
            score += 25
    except:
        findings.append("Domain age could not be verified")
        score += 10

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

