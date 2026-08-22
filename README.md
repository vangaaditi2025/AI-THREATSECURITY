# 🛡️ AI-ThreatSecurity
You can find a live demo of my latest project 'https://ai-threatsecurity.streamlit.app/'

> **AI-powered cybersecurity analysis platform for detecting, analyzing, and responding to digital threats.**

AI-ThreatSecurity is an advanced cybersecurity platform designed to help users identify potential threats such as **phishing attempts, suspicious URLs, malicious content, and security risks** through automated analysis and AI-assisted insights.

The platform combines **Artificial Intelligence 🤖, Cybersecurity 🔐, Threat Intelligence 🕵️, and modern web technologies 🌐** into a centralized security analysis dashboard.

AI-ThreatSecurity provides an interactive environment for **threat detection, risk assessment, security analysis, scan history, and AI-powered cybersecurity assistance** through a modern 3D-inspired interface.

---

## ✨ Key Features

### 🔗 URL Threat Scanner

Analyze suspicious URLs and identify potential security risks using automated threat analysis.

- 🔍 URL structure analysis
- ⚠️ Suspicious pattern detection
- 📊 Threat scoring
- 🚨 Risk classification
- 📝 Security insights

### 🎣 Phishing Detection

Analyze suspicious emails and messages to identify potential phishing indicators.

- 📧 Email analysis
- 🔎 Suspicious pattern detection
- 🚨 Phishing risk assessment
- 📊 Threat scoring
- 💡 AI-assisted insights

### 📝 Threat Content Analyzer

Analyze potentially malicious or suspicious content and identify security-related indicators.

- 🔍 Content analysis
- ⚠️ Suspicious keyword detection
- 📊 Risk assessment
- 🧠 AI-assisted analysis

### 🤖 AI Cybersecurity Assistant

An integrated AI assistant powered by **Google Gemini** to provide cybersecurity-related assistance.

- 💬 Cybersecurity Q&A
- 🧠 Threat analysis
- 🔐 Defensive security guidance
- 💡 Security recommendations
- 📚 Security explanations

### 📊 Security Dashboard

A centralized dashboard for monitoring threat activity and security statistics.

- 📈 Total scans
- 🚨 Detected threats
- 🟢 Safe results
- ⚠️ High-risk findings
- 📡 Threat activity
- 💻 System status

### 📜 Scan History

Maintain and review previous security analyses.

- 🗂️ Previous scans
- 📅 Scan timestamps
- 🎯 Scanned targets
- 📊 Threat scores
- 🚨 Risk classifications

### 🔐 Authentication

Secure user access and account management.

- 👤 User registration
- 🔑 Login authentication
- 🚪 Logout
- 🗂️ User-specific scan history
- 👨‍💻 Admin access

### 🔮 3D Cybersecurity Interface

The platform features a modern cybersecurity command-center design with:

- 🌐 Cyber grid interface
- 🔮 3D-inspired threat intelligence core
- 📡 Threat radar
- ✨ Animated visual effects
- 📊 Interactive security cards
- 🖥️ System telemetry
- ⚡ Real-time scanning animations
- 🌑 Dark cybersecurity theme

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| 🐍 **Python** | Application development |
| 🎈 **Streamlit** | Web application framework |
| 🤖 **Google Gemini API** | AI-powered analysis and assistance |
| 🗄️ **Neon PostgreSQL** | Database |
| 🎨 **HTML / CSS** | Custom UI and visual design |
| 🔐 **Authentication** | User access management |
| 🐙 **Git / GitHub** | Version control |

---

## 🏗️ Project Structure

```text
AI-THREATSECURITY/
│
├── 📄 app.py
├── 📄 db.py
├── 📄 requirements.txt
├── 📄 README.md
│
├── 📁 services/
│   ├── 🤖 ai.py
│   └── 🔍 scanner.py
│
├── 📁 utils/
│   └── 🔐 auth.py
│
├── 📁 .streamlit/
│   └── ⚙️ config.toml
│
└── 📁 data/

## Run locally

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

For Gemini, copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and add your key.

## Deploy

This app is suitable for Streamlit Community Cloud for a lightweight college/demo deployment. SQLite persistence should not be treated as production-grade storage on ephemeral hosting. For persistent production data, replace `db.py` with PostgreSQL-backed storage.

## Security scope

The scanners are defensive heuristics. They do not execute URLs, malware, attachments, or commands and they do not claim to be a full antivirus/SIEM/EDR.


## Recommended hosted setup

For Streamlit Community Cloud, use Neon PostgreSQL so users, scan history, and admin data persist. Add these to Streamlit Cloud Secrets:

```toml
DATABASE_URL = "your Neon connection string"
GEMINI_API_KEY = "your Gemini API key"
GEMINI_MODEL = "gemini-2.5-flash"
```

Do not commit secrets.toml or API keys to GitHub.
