import os

SYSTEM = """You are the AI Security Assistant for AI ThreatGuard.
Give defensive cybersecurity guidance. Do not provide malware, credential theft,
evasion, exploitation, or destructive instructions. Clearly distinguish facts,
heuristics, and uncertainty. Prefer practical safe remediation steps."""

def ask_gemini(prompt):
    key = os.getenv("GEMINI_API_KEY", "")
    if not key:
        try:
            import streamlit as st
            key = st.secrets.get("GEMINI_API_KEY", "")
        except Exception:
            pass
    if not key:
        return "[AI unavailable] Add GEMINI_API_KEY to Streamlit secrets or environment variables."

    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    try:
        from google import genai
        client = genai.Client(api_key=key)
        response = client.models.generate_content(
            model=model,
            contents=f"{SYSTEM}\n\nUser question:\n{prompt}"
        )
        return response.text
    except Exception as e:
        return f"[AI unavailable] Gemini request failed: {type(e).__name__}"
