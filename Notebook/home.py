# app.py
import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="Heartbeat Home", layout="wide", initial_sidebar_state="collapsed")

# Hide Streamlit default header/footer for a cleaner look
hide_streamlit_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Main HTML/CSS/JS block with animated heartbeat and EKG line
page_html = r"""
<div class="page">
  <div class="hero">
    <div class="hero-inner">
      <div class="hero-left">
        <div class="eyebrow">Live Health Dashboard</div>
        <h1 class="title">
          Keep the <span class="accent">pulse</span> of your app
          <span class="heart-wrap">
            <svg class="heart" viewBox="0 0 32 29">
              <path d="M23.6 2.6c-2-1.8-5.2-1.8-7.2 0L16 3.1l-.4-.5c-2-1.8-5.2-1.8-7.2 0-2.3 2.1-2.5 5.7-.5 8.1L16 28l7.6-17.3c2-2.4 1.8-6-0.0-8.1z"/>
            </svg>
          </span>
        </h1>

        <p class="subtitle">Real-time visuals, clean UI, and an animated heartbeat to show live status.</p>

        <div class="cta-row">
          <button class="btn primary">Get Started</button>
          <button class="btn ghost">Learn More</button>
        </div>
      </div>

      <div class="hero-right">
        <!-- Animated EKG SVG -->
        <div class="ekg-container" aria-hidden="true">
          <svg class="ekg" viewBox="0 0 1200 200" preserveAspectRatio="none">
            <defs>
              <linearGradient id="g" x1="0" x2="1" y1="0" y2="0">
                <stop offset="0" stop-color="#00ffd5"/>
                <stop offset="1" stop-color="#7b61ff"/>
              </linearGradient>
            </defs>

            <!-- background grid -->
            <rect width="100%" height="100%" fill="rgba(255,255,255,0.02)"/>

            <path id="ekgPath" d="
              M0,100 
              L80,100 
              L110,100 
              L130,40 
              L150,160 
              L180,100 
              L260,100
              L300,100
              L320,100
              L340,60
              L360,140
              L380,100
              L460,100
              L520,100
              L540,30
              L560,170
              L580,100
              L720,100
              L760,100
              L790,100
              L810,50
              L830,150
              L850,100
              L920,100
              L980,100
              L1000,100
              L1020,40
              L1040,180
              L1060,100
              L1200,100" 
              fill="none" stroke="url(#g)" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>

      </div>
    </div>
  </div>

  <div class="content">
    <div class="cards">
      <div class="card">
        <h3>Realtime Stats</h3>
        <p>Visualize heartbeat, steps, and other live metrics.</p>
      </div>
      <div class="card">
        <h3>Alerts</h3>
        <p>Push important notifications and emergency triggers.</p>
      </div>
      <div class="card">
        <h3>History</h3>
        <p>View past trends, with smooth graphs and export options.</p>
      </div>
    </div>
  </div>
</div>

<style>
:root{
  --bg: #0b0f1a;
  --panel: rgba(255,255,255,0.03);
  --muted: rgba(255,255,255,0.65);
  --accent-from: #00ffd5;
  --accent-to: #7b61ff;
  --glass: rgba(255,255,255,0.04);
  --radius: 14px;
}

/* Page layout */
.page{
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
  background: radial-gradient(1200px 600px at 10% 10%, rgba(123,97,255,0.06), transparent 8%),
              radial-gradient(900px 400px at 90% 90%, rgba(0,255,213,0.03), transparent 6%),
              var(--bg);
  color: white;
  min-height: 100vh;
  padding: 40px;
  box-sizing: border-box;
}

/* Hero */
.hero{
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  background: linear-gradient(180deg, rgba(255,255,255,0.02), transparent);
  border-radius: var(--radius);
  padding: 28px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.6);
  backdrop-filter: blur(6px);
}

.hero-inner{
  display:flex;
  gap: 28px;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
}

/* Left column */
.hero-left{
  flex: 1 1 420px;
  min-width: 280px;
}

.eyebrow{
  font-size: 13px;
  color: var(--muted);
  margin-bottom: 10px;
  letter-spacing: 0.06em;
}

.title{
  font-size: 36px;
  line-height: 1.03;
  margin: 0 0 12px 0;
  display:flex;
  align-items:center;
  gap:12px;
  flex-wrap: wrap;
}

.accent{
  background: linear-gradient(90deg, var(--accent-from), var(--accent-to));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  font-weight: 700;
}

.heart-wrap{
  width: 48px;
  height: 48px;
  display:inline-block;
  position: relative;
}

.heart{
  width: 48px;
  height: 48px;
  transform-origin: center;
  animation: beat 1s ease-in-out infinite;
  filter: drop-shadow(0 6px 14px rgba(123,97,255,0.16));
  fill: url(#g); /* fallback - single color by path fill above will work */
}

/* Heart beat keyframes */
@keyframes beat {
  0% { transform: scale(1); opacity: 0.98; }
  14% { transform: scale(1.18); opacity: 1; }
  28% { transform: scale(0.98); }
  42% { transform: scale(1); }
  100% { transform: scale(1); }
}

/* Subtitle and CTA */
.subtitle{
  color: var(--muted);
  margin-top: 4px;
  margin-bottom: 18px;
  max-width: 520px;
}

.cta-row{ display:flex; gap:12px; align-items:center; flex-wrap:wrap; margin-bottom: 6px; }

.btn{
  border-radius: 10px;
  padding: 10px 16px;
  font-weight: 600;
  border: none;
  cursor:pointer;
  box-shadow: 0 6px 20px rgba(11,15,26,0.6);
  background: var(--glass);
  color: white;
}

/* Primary gradient button */
.btn.primary{
  background: linear-gradient(90deg,var(--accent-from),var(--accent-to));
  color: #07101a;
}

/* Ghost */
.btn.ghost{
  background: transparent;
  border: 1px solid rgba(255,255,255,0.06);
}

/* Right column - EKG */
.hero-right{
  width: 560px;
  max-width: 46%;
  min-width: 260px;
  display:flex;
  align-items:center;
  justify-content:center;
}

.ekg-container{
  width: 100%;
  height: 180px;
  background: linear-gradient(180deg, rgba(255,255,255,0.02), transparent);
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.03);
  padding: 12px;
  box-sizing: border-box;
  overflow: hidden;
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.02);
}

/* Make the ekg path animate as if it's moving left-to-right */
.ekg{
  width: 120%;
  height: 100%;
}

/* Animate stroke-dashoffset to create the flowing motion */
#ekgPath {
  stroke-dasharray: 1800;
  stroke-dashoffset: 1800;
  animation: ekg-draw 2.2s linear infinite;
  filter: drop-shadow(0 8px 18px rgba(0,255,213,0.06));
}

/* subtle glow */
.ekg-container::after{
  content: "";
  position:absolute;
  width: 60%;
  height: 100%;
  left: 20%;
  top: 0;
  pointer-events:none;
  background: linear-gradient(90deg, rgba(255,255,255,0.02), rgba(255,255,255,0));
  transform: skewX(-12deg);
}

/* ekg animation controls */
@keyframes ekg-draw {
  0% { stroke-dashoffset: 1800; }
  100% { stroke-dashoffset: 0; }
}

/* Cards */
.content{ max-width:1200px; margin:22px auto 0; padding: 0 6px; }
.cards{ display:flex; gap:18px; flex-wrap:wrap; }
.card{
  background: var(--panel);
  min-width: 220px;
  flex: 1 1 260px;
  padding: 18px;
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.02);
  box-shadow: 0 6px 20px rgba(2,6,23,0.6);
}
.card h3{ margin:0 0 8px 0; }
.card p{ margin:0; color: var(--muted); font-size: 14px; }

/* Responsive */
@media (max-width: 880px){
  .hero-inner{ flex-direction: column-reverse; gap: 18px; }
  .hero-right{ width:100%; max-width:100%; }
  .title{ font-size: 28px; }
  .ekg-container{ height: 140px; }
}
</style>
"""

# render the HTML
html(page_html, height=520)

# Add a little interactive area below (Streamlit native elements)
st.write("")  # spacer
cols = st.columns([2, 1, 1])
with cols[0]:
    st.metric("Live BPM", "78", delta="+2")
with cols[1]:
    st.metric("Alerts (24h)", "3", delta="0")
with cols[2]:
    st.metric("Uptime", "99.98%", delta="+0.01%")

st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
st.write("## Recent events")
st.write("- Last sync: 5 minutes ago")
st.write("- Connected devices: 3")

# optional: quick footer small text
st.markdown("""<div style="opacity:0.6;font-size:12px;margin-top:16px">Built with ❤ — Streamlit</div>""", unsafe_allow_html=True)
