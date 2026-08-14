import streamlit as st
from db import init_db, authenticate_user, create_user, is_admin, save_scan, get_scans, get_stats
from services.scanner import scan_url, scan_text, scan_email
from services.ai import ask_gemini
from utils.auth import require_login, logout

st.set_page_config(
    page_title="AI ThreatGuard | Cybersecurity Command Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Advanced 3D cyber UI ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Orbitron:wght@500;600;700;800;900&display=swap');
:root{--bg:#03050b;--line:#17324d;--cyan:#35ddff;--violet:#9a6cff;--green:#3df0aa;--yellow:#ffd166;--red:#ff4f70;--muted:#7188a8;--white:#edf7ff}
html,body,[data-testid="stAppViewContainer"]{background:radial-gradient(900px 500px at 15% -10%,rgba(53,221,255,.12),transparent 65%),radial-gradient(800px 500px at 100% 5%,rgba(154,108,255,.13),transparent 65%),#03050b;color:var(--white)}
[data-testid="stHeader"]{background:transparent}.block-container{max-width:1500px;padding:1.5rem 2rem 3rem}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#040811,#02050b);border-right:1px solid #10233a}
[data-testid="stSidebar"] *{font-family:Inter,sans-serif}h1,h2,h3,p,div{font-family:Inter,sans-serif}.mono{font-family:ui-monospace,Consolas,monospace!important}
.brand{display:flex;align-items:center;gap:12px;margin-bottom:20px}.brand-icon{width:42px;height:42px;border-radius:12px;display:grid;place-items:center;background:linear-gradient(145deg,#0e243a,#07101e);border:1px solid #214664;box-shadow:0 0 25px rgba(53,221,255,.12);font-size:22px}.brand-title{font:800 16px Orbitron,sans-serif;letter-spacing:.08em}.brand-sub{font-size:10px;color:#5f7898;letter-spacing:.14em;margin-top:3px}
.pill{display:inline-flex;align-items:center;gap:7px;padding:6px 10px;border-radius:999px;border:1px solid rgba(53,221,255,.22);background:rgba(53,221,255,.055);color:#8beaff;font-size:10px;font-weight:800;letter-spacing:.12em}.dot{width:6px;height:6px;border-radius:50%;background:var(--green);box-shadow:0 0 12px var(--green)}
.hero{position:relative;min-height:420px;overflow:hidden;border-radius:30px;border:1px solid #17324d;background:linear-gradient(135deg,rgba(8,19,34,.96),rgba(3,7,14,.99));box-shadow:0 35px 100px rgba(0,0,0,.45),inset 0 1px rgba(255,255,255,.04)}
.hero:before{content:"";position:absolute;inset:0;opacity:.32;background-image:linear-gradient(rgba(53,221,255,.10) 1px,transparent 1px),linear-gradient(90deg,rgba(53,221,255,.10) 1px,transparent 1px);background-size:44px 44px;transform:perspective(500px) rotateX(58deg) scale(1.8) translateY(100px);transform-origin:center bottom}
.hero:after{content:"";position:absolute;left:0;right:0;top:-20%;height:2px;background:linear-gradient(90deg,transparent,var(--cyan),transparent);box-shadow:0 0 30px var(--cyan);opacity:.25;animation:scan 5s linear infinite}@keyframes scan{to{top:120%}}
.hero-content{position:relative;z-index:3;padding:38px}.eyebrow{font:700 10px Orbitron,sans-serif;color:#6d8cac;letter-spacing:.2em}.hero-title{font:900 clamp(2.5rem,5vw,5.5rem) Orbitron,sans-serif;line-height:.95;margin:12px 0;background:linear-gradient(100deg,#fff,#7be9ff 45%,#a47aff);-webkit-background-clip:text;-webkit-text-fill-color:transparent}.hero-desc{max-width:600px;color:#8097b7;line-height:1.7;font-size:14px}
.core{position:absolute;right:7%;top:50%;transform:translateY(-50%);width:330px;height:330px;z-index:2}
.core-ring{position:absolute;inset:8%;border-radius:50%;border:1px solid rgba(53,221,255,.34);box-shadow:0 0 45px rgba(53,221,255,.08),inset 0 0 45px rgba(79,140,255,.06)}.r1{animation:spin 13s linear infinite}.r2{inset:18%;border-color:rgba(154,108,255,.4);border-style:dashed;animation:spinr 9s linear infinite}.r3{inset:30%;border-color:rgba(61,240,170,.3);animation:spin 7s linear infinite}@keyframes spin{to{transform:rotateZ(360deg) rotateX(55deg)}}@keyframes spinr{to{transform:rotateZ(-360deg) rotateY(60deg)}}
.core-sphere{position:absolute;left:50%;top:50%;width:100px;height:100px;transform:translate(-50%,-50%);border-radius:50%;background:radial-gradient(circle at 35% 30%,#d8fbff,#42dcff 12%,#16628e 35%,#091a31 62%,#030812);box-shadow:0 0 20px rgba(53,221,255,.7),0 0 80px rgba(53,221,255,.28),inset -15px -20px 35px rgba(0,0,0,.65);animation:pulse 2.8s ease-in-out infinite}@keyframes pulse{50%{box-shadow:0 0 28px rgba(53,221,255,.9),0 0 120px rgba(53,221,255,.3),inset -15px -20px 35px rgba(0,0,0,.65)}}
.node{position:absolute;width:7px;height:7px;border-radius:50%;background:#baf6ff;box-shadow:0 0 15px #35ddff}.n1{left:16%;top:30%;animation:float 3s infinite}.n2{right:14%;top:23%;animation:float 4s .7s infinite}.n3{left:22%;bottom:21%;animation:float 3.7s 1s infinite}.n4{right:22%;bottom:17%;animation:float 4.5s .3s infinite}@keyframes float{50%{transform:translateY(-15px) scale(1.25);opacity:.5}}
.section-title{font:700 13px Orbitron,sans-serif;letter-spacing:.1em;margin:25px 0 13px}.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.kpi3d{position:relative;min-height:125px;padding:20px;border-radius:20px;overflow:hidden;background:linear-gradient(145deg,rgba(12,25,42,.96),rgba(4,9,17,.96));border:1px solid #17334e;box-shadow:12px 15px 35px rgba(0,0,0,.28),inset 0 1px rgba(255,255,255,.04);transition:.25s}.kpi3d:hover{transform:translateY(-5px) rotateX(2deg);border-color:#2c6388}.kpi3d:before{content:"";position:absolute;width:120px;height:120px;right:-45px;top:-45px;border-radius:50%;background:radial-gradient(circle,rgba(53,221,255,.16),transparent 68%)}.kpi-label{font-size:9px;color:#6983a4;letter-spacing:.14em;font-weight:800}.kpi-number{font:800 30px Orbitron,sans-serif;margin-top:13px}.kpi-foot{font-size:10px;color:#516985;margin-top:8px}
.panel{background:linear-gradient(145deg,rgba(9,19,33,.94),rgba(4,9,17,.95));border:1px solid #152e47;border-radius:22px;padding:22px;box-shadow:0 20px 55px rgba(0,0,0,.26),inset 0 1px rgba(255,255,255,.035)}.panel:hover{border-color:#224d6d}.panel-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:17px}.panel-title{font:700 12px Orbitron,sans-serif;letter-spacing:.1em}.panel-sub{font-size:10px;color:#5e7593}
.radar{width:210px;height:210px;margin:auto;border-radius:50%;position:relative;background:repeating-radial-gradient(circle,transparent 0 30px,rgba(53,221,255,.11) 31px 32px),linear-gradient(90deg,transparent 49.5%,rgba(53,221,255,.13) 50%,transparent 50.5%),linear-gradient(0deg,transparent 49.5%,rgba(53,221,255,.13) 50%,transparent 50.5%);border:1px solid #1d4d68;box-shadow:0 0 45px rgba(53,221,255,.07);overflow:hidden}.radar-sweep{position:absolute;left:50%;top:50%;width:48%;height:1px;transform-origin:left;background:linear-gradient(90deg,#35ddff,transparent);box-shadow:0 0 12px #35ddff;animation:radar 3s linear infinite}@keyframes radar{to{transform:rotate(360deg)}}.rdot{position:absolute;width:7px;height:7px;border-radius:50%;background:#ff4f70;box-shadow:0 0 12px #ff4f70}.rd1{left:63%;top:30%}.rd2{left:30%;top:61%;background:#ffd166;box-shadow:0 0 12px #ffd166}.rd3{left:72%;top:67%;background:#3df0aa;box-shadow:0 0 12px #3df0aa}
.meter{height:9px;background:#0b1726;border-radius:999px;overflow:hidden;border:1px solid #15314a}.meter>div{height:100%;border-radius:999px;background:linear-gradient(90deg,#35ddff,#9a6cff);box-shadow:0 0 15px rgba(53,221,255,.45)}
.threat-row{display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid #102239}.threat-icon{width:34px;height:34px;border-radius:10px;display:grid;place-items:center;background:#0b1929;border:1px solid #183651}.threat-main{flex:1}.threat-name{font-size:12px;font-weight:700}.threat-meta{font-size:9px;color:#5e7694;margin-top:3px}.sev{font-size:9px;font-weight:800;letter-spacing:.1em;padding:5px 8px;border-radius:999px}.sev-high{color:#ff718a;background:rgba(255,79,112,.09);border:1px solid rgba(255,79,112,.25)}.sev-med{color:#ffd166;background:rgba(255,209,102,.08);border:1px solid rgba(255,209,102,.23)}.sev-low{color:#3df0aa;background:rgba(61,240,170,.08);border:1px solid rgba(61,240,170,.22)}
.stButton>button{border:1px solid #1d4866!important;border-radius:12px!important;background:linear-gradient(135deg,#0b263b,#10182b)!important;color:#dff8ff!important;font-weight:800!important;letter-spacing:.02em;box-shadow:0 12px 30px rgba(0,0,0,.25)!important}.stButton>button:hover{border-color:#35ddff!important;box-shadow:0 0 24px rgba(53,221,255,.12)!important;transform:translateY(-2px)}
div[data-baseweb="input"]>div,div[data-baseweb="textarea"]>div,div[data-baseweb="select"]>div{background:#050c16!important;border:1px solid #16334d!important;border-radius:12px!important}
[data-testid="stDataFrame"]{border:1px solid #15334d;border-radius:16px;overflow:hidden}.footer{text-align:center;color:#405873;font:9px Orbitron,sans-serif;letter-spacing:.15em;padding:35px 0 5px}
@media(max-width:900px){.core{opacity:.22;right:-90px}.grid4{grid-template-columns:repeat(2,1fr)}}@media(max-width:600px){.block-container{padding:1rem}.grid4{grid-template-columns:1fr}.hero{min-height:500px}}
</style>
""", unsafe_allow_html=True)

init_db()

if "user" not in st.session_state:
    st.session_state.user = None



def login_page():
    st.markdown("""
    <div class="hero" style="min-height:650px;">
      <div class="hero-content">
        <div class="pill"><span class="dot"></span> DEFENSIVE SECURITY PLATFORM</div>
        <div class="hero-title">AI<br>THREATGUARD</div>
        <div class="eyebrow">AUTONOMOUS THREAT ANALYSIS / 01</div>
        <p class="hero-desc">A visual cybersecurity command center for URL intelligence, phishing detection, suspicious-content analysis, scan history, and AI-assisted security reasoning.</p>
        <div style="display:flex;gap:9px;flex-wrap:wrap;margin-top:22px;">
          <span class="pill">URL INTELLIGENCE</span><span class="pill">PHISHING DEFENSE</span><span class="pill">AI COPILOT</span>
        </div>
      </div>
      <div class="core">
        <div class="core-ring r1"></div><div class="core-ring r2"></div><div class="core-ring r3"></div>
        <div class="core-sphere"></div>
        <div class="node n1"></div><div class="node n2"></div><div class="node n3"></div><div class="node n4"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    a,b,c = st.columns([1,1.15,1])
    with b:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["SIGN IN", "CREATE ACCOUNT"])
        with tab1:
            with st.form("login"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                if st.form_submit_button("ENTER COMMAND CENTER", use_container_width=True):
                    user = authenticate_user(email, password)
                    if user:
                        st.session_state.user = user
                        st.rerun()
                    else:
                        st.error("Invalid email or password.")
        with tab2:
            with st.form("register"):
                name = st.text_input("Name")
                email = st.text_input("Email", key="reg_email")
                password = st.text_input("Password", type="password", key="reg_password")
                confirm = st.text_input("Confirm password", type="password")
                if st.form_submit_button("INITIALIZE ACCOUNT", use_container_width=True):
                    if len(password) < 8:
                        st.error("Password must contain at least 8 characters.")
                    elif password != confirm:
                        st.error("Passwords do not match.")
                    elif create_user(name, email, password):
                        st.success("Account created. You can now sign in.")
                    else:
                        st.error("An account with that email already exists.")
        st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.user:
    login_page()
    st.stop()


user = st.session_state.user

def result_panel(result, label="ANALYSIS RESULT"):
    risk=result.get("risk","Unknown"); score=int(result.get("score",0))
    accent="#ff4f70" if risk in ("High","Critical") else ("#ffd166" if risk=="Medium" else "#3df0aa")
    items="".join([f'<div class="threat-row"><div class="threat-icon">◈</div><div class="threat-main"><div class="threat-name">{i}</div></div></div>' for i in result.get("indicators",[])])
    st.markdown(f'<div class="panel" style="border-color:{accent}55;"><div class="panel-head"><div><div class="panel-title">{label}</div><div class="panel-sub">defensive heuristic assessment</div></div><div class="sev" style="color:{accent};border:1px solid {accent}55;background:{accent}10;">{risk.upper()}</div></div><div style="display:flex;align-items:center;gap:22px;flex-wrap:wrap;"><div style="font:800 42px Orbitron;color:{accent};">{score}<span style="font-size:14px;color:#5d7694;"> / 100</span></div><div style="flex:1;min-width:180px;"><div class="panel-sub" style="margin-bottom:8px;">THREAT SCORE</div><div class="meter"><div style="width:{score}%;background:{accent};"></div></div></div></div><div style="margin-top:17px;color:#93a9c4;font-size:12px;line-height:1.6;">{result.get("summary","")}</div><div style="margin-top:13px;">{items}</div></div>', unsafe_allow_html=True)


with st.sidebar:
    st.markdown("""
    <div class="brand">
      <div class="brand-icon">🛡️</div>
      <div><div class="brand-title">THREATGUARD</div><div class="brand-sub">SECURITY OS / 3D CORE</div></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<span class="pill"><span class="dot"></span> SECURE SESSION</span>', unsafe_allow_html=True)
    st.caption(f"Operator: {user['name']}")
    st.divider()
    page = st.radio("COMMAND MODULES", ["Dashboard", "URL Scanner", "Email / Phishing", "Text Analyzer", "AI Assistant", "Scan History"] + (["Admin"] if user["is_admin"] else []))
    st.divider()
    st.markdown("""<div style="color:#526c8b;font-size:9px;line-height:1.9;">SYSTEM<br><span style="color:#3df0aa;">● ONLINE</span><br>ENCRYPTION<br><span style="color:#3df0aa;">● ACTIVE</span><br>ANALYSIS ENGINE<br><span style="color:#35ddff;">● READY</span></div>""", unsafe_allow_html=True)
    st.write("")
    if st.button("TERMINATE SESSION", use_container_width=True):
        logout()
        st.rerun()



if page == "Dashboard":
    stats = get_stats(user["id"])
    st.markdown('<div class="eyebrow">THREATGUARD / COMMAND CENTER / LIVE</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title" style="font-size:clamp(2rem,4vw,4rem);">SECURITY<br>OVERVIEW</div>', unsafe_allow_html=True)
    st.markdown('<p class="hero-desc">Your defensive analysis environment is online. Monitor threat signals, investigate indicators, and launch a scan.</p>', unsafe_allow_html=True)
    st.markdown('<div class="grid4">', unsafe_allow_html=True)
    for label,val,foot in [("TOTAL SCANS",stats["total"],"ANALYSIS EVENTS"),("THREATS",stats["threats"],"HIGH + CRITICAL"),("SAFE",stats["safe"],"LOW RISK"),("PRIORITY",stats["high"],"REQUIRES REVIEW")]:
        st.markdown(f'<div class="kpi3d"><div class="kpi-label">{label}</div><div class="kpi-number">{val}</div><div class="kpi-foot">{foot}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">THREAT INTELLIGENCE MATRIX</div>', unsafe_allow_html=True)
    left,right = st.columns([1,1.25], gap="large")
    with left:
        st.markdown("""<div class="panel"><div class="panel-head"><div><div class="panel-title">LIVE RADAR</div><div class="panel-sub">heuristic signal field</div></div><div class="pill">● ACTIVE</div></div><div class="radar"><div class="radar-sweep"></div><div class="rdot rd1"></div><div class="rdot rd2"></div><div class="rdot rd3"></div></div><div style="display:flex;justify-content:space-around;margin-top:18px;color:#58708f;font-size:9px;letter-spacing:.1em;"><span><b style="color:#ff4f70;">●</b> HIGH</span><span><b style="color:#ffd166;">●</b> MEDIUM</span><span><b style="color:#3df0aa;">●</b> LOW</span></div></div>""", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-head"><div><div class="panel-title">RECENT THREAT FEED</div><div class="panel-sub">latest analysis events</div></div><div class="mono" style="font-size:9px;color:#52718e;">STREAM / 01</div></div>', unsafe_allow_html=True)
        scans = get_scans(user["id"], 6)
        if scans:
            for x in scans:
                sev=x["risk"].lower(); cls="sev-high" if sev in ("high","critical") else ("sev-med" if sev=="medium" else "sev-low"); icon="⚠" if sev in ("high","critical") else ("◈" if sev=="medium" else "✓")
                st.markdown(f'<div class="threat-row"><div class="threat-icon">{icon}</div><div class="threat-main"><div class="threat-name">{x["scan_type"]} / {x["target"][:45]}</div><div class="threat-meta">{x["created_at"][:19]} UTC</div></div><div class="sev {cls}">{x["risk"].upper()}</div><div class="mono" style="font-size:10px;color:#7891ad;">{x["score"]}/100</div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="padding:50px 10px;text-align:center;color:#5d7594;">NO EVENTS YET<br><span style="font-size:10px;">Launch your first scan from the command modules.</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">SYSTEM TELEMETRY</div>', unsafe_allow_html=True)
    a,b,c=st.columns(3)
    for col,title,value,sub in [(a,"ANALYSIS ENGINE","READY","defensive heuristics"),(b,"AI COPILOT","READY","Gemini integration"),(c,"DATA STORE","ONLINE","Neon / SQLite")]:
        with col:
            st.markdown(f'<div class="panel"><div class="panel-title">{title}</div><div style="font:700 20px Orbitron;margin:13px 0;color:#3df0aa;">● {value}</div><div class="panel-sub">{sub}</div><div class="meter" style="margin-top:15px;"><div style="width:92%;"></div></div></div>', unsafe_allow_html=True)

elif page == "URL Scanner":
    st.markdown('<div class="badge">● NETWORK INTELLIGENCE</div>', unsafe_allow_html=True)
    st.markdown('<div class="cyber-title" style="font-size:2.7rem;">URL Threat Scanner</div>', unsafe_allow_html=True)
    st.write("Analyze a URL using safe, non-executing heuristics and HTTP metadata.")
    url = st.text_input("URL", placeholder="https://example.com")
    if st.button("Scan URL", type="primary"):
        if not url.strip():
            st.warning("Enter a URL.")
        else:
            with st.spinner("Analyzing URL..."):
                result = scan_url(url.strip())
            save_scan(user["id"], "URL", url.strip(), result["risk"], result["score"], result)
            st.session_state.last_result = result

    result = st.session_state.get("last_result")
    if result:
        st.divider()
        cols = st.columns(4)
        cols[0].metric("Risk", result["risk"])
        cols[1].metric("Score", f"{result['score']}/100")
        cols[2].metric("HTTPS", "Yes" if result["https"] else "No")
        cols[3].metric("HTTP status", result.get("status", "N/A"))
        result_panel(result, "URL THREAT ASSESSMENT")

elif page == "Email / Phishing":
    st.markdown('<div class="badge">● PHISHING DEFENSE</div>', unsafe_allow_html=True)
    st.markdown('<div class="cyber-title" style="font-size:2.7rem;">Email & Phishing Analyzer</div>', unsafe_allow_html=True)
    st.write("Paste an email or suspicious message. The analyzer does not execute links or attachments.")
    subject = st.text_input("Subject")
    sender = st.text_input("Sender", placeholder="security@example.com")
    body = st.text_area("Email body", height=260)
    if st.button("Analyze email", type="primary"):
        if not body.strip():
            st.warning("Paste the email body.")
        else:
            result = scan_email(subject, sender, body)
            target = f"{sender} | {subject}"[:200]
            save_scan(user["id"], "Email", target, result["risk"], result["score"], result)
            st.session_state.email_result = result
    result = st.session_state.get("email_result")
    if result:
        st.divider()
        c1, c2 = st.columns(2)
        c1.metric("Risk", result["risk"])
        c2.metric("Score", f"{result['score']}/100")
        if result["risk"] in ("High", "Critical"):
            st.error(result["summary"])
        elif result["risk"] == "Medium":
            st.warning(result["summary"])
        else:
            st.success(result["summary"])
        st.subheader("Indicators")
        for item in result["indicators"]:
            st.write(f"• {item}")

elif page == "Text Analyzer":
    st.markdown('<div class="badge">● SIGNAL ANALYSIS</div>', unsafe_allow_html=True)
    st.markdown('<div class="cyber-title" style="font-size:2.7rem;">Security Text Analyzer</div>', unsafe_allow_html=True)
    text = st.text_area("Paste suspicious text, a URL, log snippet, or message", height=300)
    if st.button("Analyze text", type="primary"):
        if not text.strip():
            st.warning("Enter text.")
        else:
            result = scan_text(text)
            save_scan(user["id"], "Text", text[:120], result["risk"], result["score"], result)
            st.session_state.text_result = result
    result = st.session_state.get("text_result")
    if result:
        st.divider()
        c1, c2 = st.columns(2)
        c1.metric("Risk", result["risk"])
        c2.metric("Score", f"{result['score']}/100")
        result_panel(result, "PHISHING ASSESSMENT")

elif page == "AI Assistant":
    st.markdown('<div class="badge">● INTELLIGENCE COPILOT</div>', unsafe_allow_html=True)
    st.markdown('<div class="cyber-title" style="font-size:2.7rem;">AI Security Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel"><div class="panel-title">GEMINI SECURITY COPILOT</div><div class="panel-sub" style="margin:7px 0 18px;">Defensive reasoning layer • safe security guidance</div>', unsafe_allow_html=True)
    prompt = st.text_area("Ask a cybersecurity question", height=180,
                          placeholder="Explain why this URL may be suspicious...")
    if st.button("Ask AI", type="primary"):
        if not prompt.strip():
            st.warning("Enter a question.")
        else:
            with st.spinner("Thinking..."):
                answer = ask_gemini(prompt)
            if answer.startswith("[AI unavailable]"):
                st.warning(answer)
            else:
                st.markdown(answer)

    st.markdown("</div>", unsafe_allow_html=True)

elif page == "Scan History":
    st.markdown('<div class="badge">● FORENSIC LOGS</div>', unsafe_allow_html=True)
    st.markdown('<div class="cyber-title" style="font-size:2.7rem;">Scan History</div>', unsafe_allow_html=True)
    scans = get_scans(user["id"], 200)
    if not scans:
        st.info("No scan history.")
    else:
        import pandas as pd
        df = pd.DataFrame(scans)
        st.dataframe(df[["created_at", "scan_type", "target", "risk", "score"]],
                     use_container_width=True, hide_index=True)
        st.download_button(
            "Download CSV",
            df.to_csv(index=False).encode("utf-8"),
            "threatguard_scan_history.csv",
            "text/csv",
        )

elif page == "Admin":
    st.markdown('<div class="badge">● ADMINISTRATOR</div>', unsafe_allow_html=True)
    st.markdown('<div class="cyber-title" style="font-size:2.7rem;">Admin Console</div>', unsafe_allow_html=True)
    stats = get_stats()
    c1, c2, c3 = st.columns(3)
    c1.metric("All scans", stats["total"])
    c2.metric("Threats", stats["threats"])
    c3.metric("High/Critical", stats["high"])
    st.info("The admin view is intentionally limited to aggregate data and scan records in this starter deployment.")
    scans = get_scans(limit=200)
    if scans:
        import pandas as pd
        st.dataframe(pd.DataFrame(scans), use_container_width=True, hide_index=True)

st.markdown('<div class="footer">AI ThreatGuard • Defensive security analysis • Built with Streamlit</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">AI THREATGUARD • DEFENSIVE SECURITY OPERATIONS • COMMAND CENTER ONLINE</div>', unsafe_allow_html=True)
