import re
from urllib.parse import urlparse
import urllib.request

SHORTENERS = {"bit.ly","tinyurl.com","t.co","is.gd","ow.ly","buff.ly","cutt.ly"}
SUSPICIOUS_TLDS = {".zip",".mov",".click",".top",".xyz",".tk",".gq",".ml",".ga",".cf"}
PHISH_WORDS = {
    "verify account","verify your account","urgent","suspended","password",
    "login now","confirm identity","security alert","payment failed",
    "click immediately","gift card","crypto wallet","reset password"
}

def risk_from_score(score):
    if score >= 75: return "Critical"
    if score >= 50: return "High"
    if score >= 25: return "Medium"
    return "Low"

def scan_url(raw):
    value = raw.strip()
    if not re.match(r"^https?://", value, re.I):
        value = "https://" + value
    p = urlparse(value)
    host = (p.hostname or "").lower()
    indicators = []
    score = 0

    if p.scheme != "https":
        score += 20; indicators.append("URL does not use HTTPS.")
    if "@" in p.netloc:
        score += 25; indicators.append("URL contains an @ symbol, which can obscure the real destination.")
    if host in SHORTENERS:
        score += 20; indicators.append("URL uses a known URL-shortening service.")
    if any(host.endswith(tld) for tld in SUSPICIOUS_TLDS):
        score += 20; indicators.append("Domain uses a TLD frequently abused in phishing campaigns.")
    if len(value) > 120:
        score += 15; indicators.append("URL is unusually long.")
    if host.count(".") >= 4:
        score += 10; indicators.append("Hostname contains an unusually high number of subdomains.")
    if re.search(r"(login|verify|secure|account|update|wallet|password|payment)", value, re.I):
        score += 15; indicators.append("URL contains security/account/payment-themed keywords.")
    if re.search(r"%[0-9a-fA-F]{2}", value):
        score += 5; indicators.append("URL contains percent-encoded characters.")

    status = "N/A"
    if host:
        try:
            req = urllib.request.Request(value, method="HEAD", headers={"User-Agent":"AI-ThreatGuard/1.0"})
            with urllib.request.urlopen(req, timeout=5) as r:
                status = r.status
        except Exception:
            indicators.append("Could not safely retrieve HTTP metadata; this is not itself proof of maliciousness.")

    score = min(score, 100)
    if not indicators:
        indicators.append("No high-risk heuristic indicators were detected.")
    return {
        "risk": risk_from_score(score), "score": score, "https": p.scheme == "https",
        "status": status, "host": host,
        "indicators": indicators,
        "summary": f"Heuristic URL analysis classified this target as {risk_from_score(score)} risk."
    }

def scan_email(subject, sender, body):
    text = f"{subject}\n{sender}\n{body}"
    indicators, score = [], 0
    lower = text.lower()
    hits = [w for w in PHISH_WORDS if w in lower]
    if hits:
        score += min(40, 8 * len(hits))
        indicators.append("Pressure/verification language detected: " + ", ".join(hits[:5]))
    if re.search(r"https?://\S+", body, re.I):
        score += 10
        indicators.append("Message contains one or more links.")
    if re.search(r"\b(?:\d[ -]?){13,19}\b", body):
        score += 20
        indicators.append("Possible payment-card-like number detected; do not share sensitive financial data.")
    if re.search(r"\b(?:password|otp|one[- ]time password|passcode)\b", body, re.I):
        score += 15
        indicators.append("Message requests or discusses authentication secrets.")
    if re.search(r"\b(urgent|immediately|within \d+ minutes|act now)\b", body, re.I):
        score += 10
        indicators.append("Urgency language detected.")
    if sender and re.search(r"(gmail|outlook|yahoo)\.", sender, re.I) and re.search(r"(bank|support|microsoft|google|paypal|admin)", body, re.I):
        score += 10
        indicators.append("Sender/domain context may not match the claimed organization.")
    score = min(score,100)
    if not indicators: indicators.append("No major phishing heuristics were detected.")
    return {"risk": risk_from_score(score), "score": score,
            "indicators": indicators,
            "summary": f"Heuristic email analysis classified this message as {risk_from_score(score)} risk."}

def scan_text(text):
    indicators, score = [], 0
    urls = re.findall(r"https?://[^\s<>\"]+", text, re.I)
    if urls:
        score += min(45, 15 * len(urls))
        indicators.append(f"Found {len(urls)} URL(s) in the text.")
    hits = [w for w in PHISH_WORDS if w in text.lower()]
    if hits:
        score += min(40, 8 * len(hits))
        indicators.append("Phishing-related language detected: " + ", ".join(hits[:6]))
    if re.search(r"(powershell|cmd\.exe|curl\s|wget\s|base64|invoke-expression|downloadstring)", text, re.I):
        score += 25
        indicators.append("Command/download or encoded-payload patterns detected. Treat as suspicious.")
    score = min(score,100)
    if not indicators: indicators.append("No major heuristic indicators were detected.")
    return {"risk": risk_from_score(score), "score": score,
            "indicators": indicators,
            "summary": f"Text analysis classified this content as {risk_from_score(score)} risk."}
