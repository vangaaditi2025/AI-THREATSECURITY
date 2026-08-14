import hashlib, hmac, os
import streamlit as st

def hash_password(password):
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 180_000)
    return f"{salt.hex()}${digest.hex()}"

def verify_password(password, stored):
    try:
        salt_hex, digest_hex = stored.split("$", 1)
        digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt_hex), 180_000)
        return hmac.compare_digest(digest.hex(), digest_hex)
    except Exception:
        return False

def require_login():
    if not st.session_state.get("user"):
        st.stop()

def logout():
    st.session_state.user = None
