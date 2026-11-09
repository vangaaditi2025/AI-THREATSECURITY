"""Gemini helper for AI ThreatGuard.

Reads the key from Streamlit Secrets / environment, cleans it, validates its
shape, tries a list of models, and returns readable messages instead of raw
stack traces. Every failure message starts with "[AI unavailable]" so app.py
can show it as a warning.
"""
import os
import time

import streamlit as st

# Tried in order. If one is retired or overloaded, the next one is used.
MODELS = ["gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-2.0-flash"]

SYSTEM_PROMPT = (
    "You are ThreatGuard, a defensive cybersecurity assistant. Explain threats, "
    "phishing, suspicious URLs, logs and security best practices clearly and "
    "practically. Focus on detection, prevention and response. Do not provide "
    "working malware, exploit code or step-by-step attack instructions."
)

KEY_NAMES = ("GEMINI_API_KEY", "GOOGLE_API_KEY")


def _clean(value) -> str:
    """Strip whitespace, newlines and stray quotes from a pasted key."""
    if not value:
        return ""
    return str(value).strip().strip('"').strip("'").strip()


def get_api_key() -> str:
    """Find the key in Secrets (top-level or nested) or environment variables."""
    try:
        for name in KEY_NAMES:
            if name in st.secrets:
                key = _clean(st.secrets[name])
                if key:
                    return key
        # Handle keys accidentally placed under a [section] in Secrets
        for section in st.secrets.values():
            if hasattr(section, "get"):
                for name in KEY_NAMES:
                    key = _clean(section.get(name))
                    if key:
                        return key
    except Exception:
        pass
    for name in KEY_NAMES:
        key = _clean(os.getenv(name))
        if key:
            return key
    return ""


def ai_status() -> tuple[bool, str]:
    """(ok, short message) - use this for the dashboard status tile."""
    key = get_api_key()
    if not key:
        return False, "NO KEY"
    if not key.startswith("AIza") or len(key) < 30:
        return False, "CHECK KEY"
    return True, "READY"


def ask_gemini(prompt: str) -> str:
    key = get_api_key()
    if not key:
        return (
            "[AI unavailable] No API key found. In Streamlit Cloud open "
            "Manage app > Settings > Secrets and add:\n\n"
            'GEMINI_API_KEY = "your-key-from-aistudio"\n\n'
            "Then reboot the app."
        )

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        return "[AI unavailable] Package missing. Add `google-genai` to requirements.txt."

    try:
        client = genai.Client(api_key=key)
    except Exception as e:
        return f"[AI unavailable] Could not create client: {e}"

    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        max_output_tokens=2000,
        temperature=0.4,
    )

    last_error = ""
    for model in MODELS:
        for attempt in range(2):  # one retry for temporary overloads
            try:
                resp = client.models.generate_content(
                    model=model, contents=prompt, config=config
                )
                text = (resp.text or "").strip()
                if text:
                    return text
                return "[AI unavailable] The model returned an empty answer (possibly blocked by safety filters). Try rephrasing."
            except Exception as e:
                msg = str(e)
                last_error = msg
                low = msg.lower()

                # Problems with the key: retrying or switching model won't help.
                if "401" in msg or "api key not valid" in low or "unauthenticated" in low or "api_key_invalid" in low:
                    return (
                        "[AI unavailable] Google rejected the API key (401). "
                        "Create a NEW key at https://aistudio.google.com/apikey (it should start with 'AIza'), "
                        "paste it in Streamlit Secrets as GEMINI_API_KEY = \"AIza...\" (top level, in quotes), "
                        "delete any old GOOGLE_API_KEY entry, then reboot the app."
                    )
                if "403" in msg or "permission_denied" in low:
                    return (
                        "[AI unavailable] Access denied (403). The key's project may not have the "
                        "Generative Language API enabled, or the key is restricted. Create a fresh key in AI Studio."
                    )
                if "429" in msg or "resource_exhausted" in low or "quota" in low:
                    return "[AI unavailable] Quota or rate limit reached (429). Wait a minute and try again."

                # Model retired / not found: go to the next model.
                if "404" in msg or "not found" in low:
                    break
                # Temporary overload: wait briefly and retry.
                if "503" in msg or "unavailable" in low or "overloaded" in low:
                    time.sleep(1.5)
                    continue
                break

    return f"[AI unavailable] {last_error[:300]}"
