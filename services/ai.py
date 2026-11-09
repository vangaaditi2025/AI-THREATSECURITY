import os
import streamlit as st

MODEL = "gemini-2.5-flash"

SYSTEM = (
    "You are a defensive cybersecurity assistant. Give clear, practical guidance "
    "on threat analysis, phishing, and security best practices. "
    "Decline to provide malware, exploit code, or attack instructions."
)

def _get_key():
    key = None
    try:
        key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
    except Exception:
        pass
    return (key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or "").strip()

def ask_gemini(prompt: str) -> str:
    key = _get_key()
    if not key:
        return "[AI unavailable] GEMINI_API_KEY not found. Add it in App settings → Secrets."
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        return "[AI unavailable] Package missing: add `google-genai` to requirements.txt."
    try:
        client = genai.Client(api_key=key)
        resp = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM,
                max_output_tokens=1500,
            ),
        )
        return resp.text or "[AI unavailable] Empty response (possibly blocked by safety filters)."
    except Exception as e:
        return f"[AI unavailable] {type(e).__name__}: {e}"
