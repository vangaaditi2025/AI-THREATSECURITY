# AI ThreatGuard — Streamlit Edition

A single-app Streamlit cybersecurity dashboard designed as a simpler deployment alternative to the original FastAPI + React architecture.

## UI

The Streamlit edition uses a dark glassmorphism cyber command-center interface with neon gradients, 3D-style threat-core panels, KPI cards, and responsive navigation.

## Features

- User registration/login with salted PBKDF2 password hashing
- User/admin roles
- URL threat heuristic scanner
- Email/phishing analyzer
- Security text analyzer
- Scan history and CSV export
- Dashboard metrics
- Optional Google Gemini security assistant
- SQLite fallback for local use; PostgreSQL/Neon support for persistent hosted deployments

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
