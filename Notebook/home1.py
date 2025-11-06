import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="Scan & Save - Home", layout="wide")

# Hide default menu & footer
st.markdown("""
<style>
#MainMenu, header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- ADVANCED HOME PAGE HTML + CSS ---
page = """
<div class="container">
  <div class="header">
    <div class="logo">🩺 Scan<span> & </span>Save</div>
    <div class="pulse-line"></div>
  </div>

  <div class="main">
    <div class="left">
      <h1 class="title">Your Emergency <span>QR Health ID</span></h1>
      <p class="desc">
        Store patient details, scan QR for instant access during emergencies, and send automatic alerts — 
        all powered by our AI-enabled health platform.
      </p>
      <div class="buttons">
        <a href="#" class="btn primary">🚀 Start Scan</a>
        <a href="#" class="btn secondary">➕ Add Info</a>
      </div>

      <div class="monitor">
        <svg class="ekg" viewBox="0 0 1000 200" preserveAspectRatio="none">
          <path d="M0,100 L100,100 L130,50 L160,150 L190,100 L260,100 L290,100 L320,40 L350,160 L380,100 L1000,100" 
                stroke="url(#grad)" stroke-width="4" fill="none" />
          <defs>
            <linearGradient id="grad" x1="0" x2="1" y1="0" y2="0">
              <stop offset="0%" stop-color="#00ffd5" />
              <stop offset="100%" stop-color="#7b61ff" />
            </linearGradient>
          </defs>
        </svg>
      </div>
    </div>

    <div class="right">
      <div class="scanner">
        <div class="scan-border"></div>
        <div class="scan-laser"></div>
        <img src="https://cdn-icons-png.flaticon.com/512/5985/5985157.png" class="qr-img" />
      </div>

      <div class="status-card">
        <div class="heart">
          <svg viewBox="0 0 32 29" class="heart-icon">
            <path d="M23.6 2.6c-2-1.8-5.2-1.8-7.2 0L16 3.1l-.4-.5c-2-1.8-5.2-1.8-7.2 0-2.3 2.1-2.5 5.7-.5 8.1L16 28l7.6-17.3c2-2.4 1.8-6-0.0-8.1z"/>
          </svg>
        </div>
        <h3>Heartbeat: <span class="bpm">78 BPM</span></h3>
        <p>Status: <span style="color:#00ffd5;">Stable</span></p>
      </div>
    </div>
  </div>
</div>

<style>
:root {
  --bg: #040710;
  --accent1: #00ffd5;
  --accent2: #7b61ff;
  --card-bg: rgba(255,255,255,0.04);
  --radius: 16px;
  --text-light: rgba(255,255,255,0.75);
}

body {
  background: var(--bg);
  color: white;
  font-family: 'Inter', sans-serif;
  margin: 0;
}

/* Header */
.container {
  min-height: 100vh;
  background: radial-gradient(900px 600px at 10% 20%, rgba(123,97,255,0.06), transparent 60%),
              radial-gradient(800px 500px at 90% 90%, rgba(0,255,213,0.04), transparent 70%),
              var(--bg);
  padding: 40px 60px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  margin-bottom: 40px;
}

.logo {
  font-size: 30px;
  font-weight: 700;
  background: linear-gradient(90deg, var(--accent1), var(--accent2));
  -webkit-background-clip: text;
  color: transparent;
}

.pulse-line {
  width: 60%;
  height: 2px;
  background: linear-gradient(90deg, var(--accent1), transparent);
  animation: pulse 1.5s infinite linear;
}
@keyframes pulse {
  0% { opacity: 0.6; transform: scaleX(0.8); }
  50% { opacity: 1; transform: scaleX(1.05); }
  100% { opacity: 0.6; transform: scaleX(0.8); }
}

/* Main Layout */
.main {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 40px;
}

/* Left Section */
.left {
  flex: 1;
  max-width: 580px;
}
.title {
  font-size: 42px;
  line-height: 1.1;
  margin-bottom: 16px;
}
.title span {
  color: var(--accent1);
}
.desc {
  color: var(--text-light);
  margin-bottom: 30px;
  font-size: 17px;
  max-width: 480px;
}
.buttons { display: flex; gap: 16px; }
.btn {
  padding: 12px 20px;
  border-radius: var(--radius);
  font-weight: 600;
  text-decoration: none;
  transition: 0.3s;
}
.btn.primary {
  background: linear-gradient(90deg, var(--accent1), var(--accent2));
  color: #000;
}
.btn.secondary {
  border: 1px solid var(--accent1);
  color: var(--accent1);
  background: transparent;
}
.btn:hover { transform: scale(1.05); }

/* Heartbeat Monitor Line */
.monitor {
  margin-top: 50px;
  width: 100%;
  height: 150px;
  overflow: hidden;
}
.ekg path {
  stroke-dasharray: 1200;
  stroke-dashoffset: 1200;
  animation: draw 3s linear infinite;
}
@keyframes draw {
  from { stroke-dashoffset: 1200; }
  to { stroke-dashoffset: 0; }
}

/* Right Section - Scanner & Heartbeat Card */
.right {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px;
}

/* Scanner Frame */
.scanner {
  width: 280px;
  height: 280px;
  position: relative;
  border: 2px solid var(--accent1);
  border-radius: var(--radius);
  box-shadow: 0 0 30px rgba(0,255,213,0.2);
  overflow: hidden;
  background: rgba(255,255,255,0.02);
}
.scan-border {
  position: absolute;
  inset: 0;
  border: 1px solid rgba(123,97,255,0.2);
  border-radius: var(--radius);
}
.scan-laser {
  position: absolute;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, transparent, var(--accent1), transparent);
  animation: scanMove 2.5s linear infinite;
}
@keyframes scanMove {
  0% { top: 0; }
  100% { top: 100%; }
}
.qr-img {
  width: 130px;
  height: 130px;
  opacity: 0.9;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

/* Heartbeat card */
.status-card {
  background: var(--card-bg);
  border: 1px solid rgba(255,255,255,0.08);
  padding: 20px;
  border-radius: var(--radius);
  text-align: center;
  box-shadow: 0 4px 20px rgba(0,255,213,0.08);
}
.heart {
  animation: beat 1s ease-in-out infinite;
  width: 60px;
  height: 60px;
  margin: 0 auto;
}
.heart-icon path {
  fill: url(#grad);
}
.bpm {
  color: var(--accent1);
  font-weight: 700;
  font-size: 20px;
}
@keyframes beat {
  0%,100% { transform: scale(1); }
  50% { transform: scale(1.25); }
}

/* Responsive */
@media (max-width: 900px){
  .main { flex-direction: column; align-items: center; }
  .left, .right { max-width: 100%; }
}
</style>
"""

# Render page
html(page, height=800)
