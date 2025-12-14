from flask import Flask, request, jsonify
import requests, socket, ssl, math
from datetime import datetime
import tldextract
from bs4 import BeautifulSoup

app = Flask(__name__)

HIGH_RISK_TLDS = ['tk','ml','ga','cf','gq','xyz','top','click']
KEYWORDS = ['login','verify','secure','bank','password','reset','otp']
BRANDS = ['google','facebook','paypal','amazon','microsoft','instagram','bank']

def entropy(s):
    p = [s.count(c)/len(s) for c in set(s)]
    return -sum(pi*math.log2(pi) for pi in p)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>PhishShield</title>
<style>
body{background:#0f172a;color:#e5e7eb;font-family:Arial}
h1{text-align:center}
.box{width:60%;margin:auto}
input{width:100%;padding:15px;font-size:16px}
button{padding:15px;margin-top:10px;background:#22c55e;border:none;font-size:16px}
.result{margin-top:20px}
.safe{color:#22c55e}
.caution{color:#facc15}
.dangerous{color:#ef4444}
</style>
</head>
<body>

<h1>🛡️ PhishShield</h1>

<div class="box">
<input id="url" placeholder="Paste URL here">
<button onclick="scan()">Deep Scan</button>
<div id="out" class="result"></div>
</div>

<script>
async function scan(){
 let url=document.getElementById('url').value;
 let r=await fetch('/scan',{
  method:'POST',
  headers:{'Content-Type':'application/json'},
  body:JSON.stringify({url:url})
 });
 let d=await r.json();
 document.getElementById('out').innerHTML=
 `<h2 class="${d.label.toLowerCase()}">${d.label}</h2>
 <p>Risk Score: ${d.score}/100</p>
 <ul>${d.reasons.map(x=>'<li>'+x+'</li>').join('')}</ul>`;
}
</script>

</body>
</html>
"""

@app.route('/')
def home():
    return HTML

@app.route('/scan', methods=['POST'])
def scan():
    url = request.json['url']
    if not url.startswith('http'):
        url = 'http://' + url

    score = 0
    reasons = []

    host = requests.utils.urlparse(url).hostname

    try:
        socket.inet_aton(host)
        score += 15
        reasons.append("IP based URL")
    except:
        pass

    ext = tldextract.extract(host)
    if ext.suffix in HIGH_RISK_TLDS:
        score += 10
        reasons.append("High risk TLD")

    if entropy(host) > 3.8:
        score += 10
        reasons.append("Random looking domain")

    for k in KEYWORDS:
        if k in url.lower():
            score += 5
            reasons.append("Suspicious keyword")
            break

    for b in BRANDS:
        if b in ext.domain and ext.domain != b:
            score += 15
            reasons.append("Brand impersonation")
            break

    try:
        r = requests.get(url, timeout=5)
        if BeautifulSoup(r.text,'html.parser').find('form'):
            score += 10
            reasons.append("Login form detected")
    except:
        pass

    label = "SAFE"
    if score > 30: label = "CAUTION"
    if score > 60: label = "DANGEROUS"

    return jsonify({
        "score":score,
        "label":label,
        "reasons":reasons,
        "time":str(datetime.now())
    })

if __name__ == '__main__':
    app.run(debug=True)
