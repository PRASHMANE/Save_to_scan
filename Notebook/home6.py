import streamlit as st
import io
import base64
import qrcode
from PIL import Image

# --- Page Setup ---
st.set_page_config(page_title="Scan to Save", layout="wide")

# --- Generate QR Code Dynamically (you can replace data) ---
qr = qrcode.QRCode(box_size=10, border=2)
qr.add_data("https://your-emergency-link.com")  # put your real URL here
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")

buffered = io.BytesIO()
img.save(buffered, format="PNG")
img_b64 = base64.b64encode(buffered.getvalue()).decode()

# --- CSS and HTML layout (all HTML is inside the triple-quoted string) ---
st.markdown(f"""
<style>
/* --- page background & fonts --- */
body {{
  margin: 0;
  padding: 0;
  background: radial-gradient(circle at center, #020202 0%, #000000 100%);
  color: white;
  font-family: 'Poppins', sans-serif;
  overflow: hidden;
}}

/* particles background */
@keyframes floatParticles {{
  from {{background-position: 0 0;}}
  to   {{background-position: 4000px 4000px;}}
}}
body::before {{
  content: "";
  position: fixed;
  inset: 0;
  background: url('https://i.ibb.co/jb7hJjL/particles.png');
  opacity: 0.08;
  animation: floatParticles 120s linear infinite;
  z-index: -2;
}}

/* pulsing overlay */
body::after {{
  content: "";
  position: fixed;
  inset: 0;
  background: radial-gradient(circle at center, rgba(255,7,58,0.15), transparent 70%);
  animation: pulseGlow 1.8s ease-in-out infinite;
  mix-blend-mode: screen;
  z-index: -1;
}}
@keyframes pulseGlow {{
  0%,100% {{opacity:0.3;}} 50% {{opacity:0.7;}}
}}

/* center container */
.center {{
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  width: 100%;
  box-sizing: border-box;
  padding: 0 20px;
}}

/* title */
.project-title {{
  position: relative;
  font-size: 3.2rem;
  font-weight: 800;
  color: #ff073a;
  letter-spacing: 3px;
  text-shadow: 0 0 25px #ff073a, 0 0 70px #ff073a;
  animation: hologlow 3s ease-in-out infinite alternate;
  display: inline-block;
  padding: 6px 18px;
  border-radius: 10px;
  backdrop-filter: blur(2px);
}}
@keyframes hologlow {{
  from {{text-shadow: 0 0 20px #ff073a;}}
  to   {{text-shadow: 0 0 70px #ff073a, 0 0 150px #ff073a;}}
}}

/* ECG (reusable) */
.ecg {{
  position: relative;
  width: min(900px, 80vw);
  height: 110px;
  margin: 18px auto;
  overflow: hidden;
}}
.ecg svg {{
  width: 100%;
  height: 100%;
}}
.ecg path {{
  fill: none;
  stroke: #ff073a;
  stroke-width: 3px;
  stroke-linejoin: round;
  stroke-linecap: round;
  filter: drop-shadow(0 0 12px #ff073a) drop-shadow(0 0 24px #ff073a);
  stroke-dasharray: 300;
  animation: drawECG 2s linear infinite;
}}
@keyframes drawECG {{
  0% {{stroke-dashoffset: 0;}}
  100% {{stroke-dashoffset: -300;}}
}}

/* small spacing tweak for top ECG above QR */
.ecg.top {{
  margin-top: 6px;
  margin-bottom: 6px;
}}

/* QR container */
.qr-container {{
  display: inline-block;
  margin-top: 8px;
  animation: floatQR 3s ease-in-out infinite alternate;
}}
.qr-container img {{
  width: 240px;
  height: 240px;
  border-radius: 18px;
  box-shadow: 0 0 30px #ff073a, 0 0 80px rgba(255,7,58,0.4);
  animation: glowQR 1.8s ease-in-out infinite alternate;
}}
@keyframes floatQR {{
  from {{transform: translateY(0);}}
  to   {{transform: translateY(-10px);}}
}}
@keyframes glowQR {{
  0%,100% {{box-shadow: 0 0 30px #ff073a, 0 0 60px rgba(255,7,58,0.4);}}
  50% {{box-shadow: 0 0 60px #ff073a, 0 0 120px rgba(255,7,58,0.6);}}
}}

/* scan text */
.scan-text {{
  margin-top: 16px;
  font-size: 1.25rem;
  color: #ff073a;
  text-shadow: 0 0 12px #ff073a, 0 0 24px #ff073a;
  letter-spacing: 2px;
  animation: beatText 1.2s ease-in-out infinite;
}}
@keyframes beatText {{
  0%,100% {{transform: scale(1);}}
  50% {{transform: scale(1.06);}}
}}

/* scrolling member names */
.members {{
  margin-top: 20px;
  white-space: nowrap;
  overflow: hidden;
  width: 100%;
  font-size: 1.1rem;
  color: #ff073a;
  text-shadow: 0 0 10px #ff073a, 0 0 25px #ff073a;
}}
.members span {{
  display: inline-block;
  padding-left: 100%;
  animation: scrollNames 15s linear infinite;
}}
@keyframes scrollNames {{
  0% {{ transform: translateX(0); }}
  100% {{ transform: translateX(-100%); }}
}}

/* responsive */
@media (max-width: 600px) {{
  .project-title {{ font-size: 2rem; padding: 4px 10px; }}
  .qr-container img {{ width: 180px; height: 180px; }}
  .ecg {{ height: 70px; }}
}}
</style>

<div class="center">
  <div class="project-title">SCAN TO SAVE</div>

  <!-- top ECG line (under title) -->
  <div class="ecg top" aria-hidden="true">
    <svg viewBox="0 0 600 100" preserveAspectRatio="none">
      <path d="M0,50 L60,50 L80,30 L100,70 L120,50 L180,50 L200,25 L220,75 L240,50 L300,50 L320,30 L340,70 L360,50 L420,50 L440,25 L460,75 L480,50 L540,50 L560,30 L580,70 L600,50"/>
    </svg>
  </div>

  <!-- QR CODE -->
  <div class="qr-container">
    <img src="data:image/png;base64,{img_b64}" alt="QR Code">
  </div>

  <!-- heartbeat line below QR -->
  <div class="ecg" aria-hidden="true" style="margin-top:8px;">
    <svg viewBox="0 0 600 100" preserveAspectRatio="none">
      <path d="M0,50 L50,50 L70,25 L90,75 L110,50 L160,50 L180,25 L200,75 L220,50 L270,50 L290,25 L310,75 L330,50 L380,50 L400,25 L420,75 L440,50 L490,50 L510,25 L530,75 L550,50 L600,50"/>
    </svg>
  </div>

  <div class="scan-text">❤️ SCAN TO SAVE ❤️</div>

  <!-- scrolling names -->
  <div class="members">
    <span>Prashanth • Manikanta • Harish • Shruthi • Akash • Keerthi •</span>
  </div>
</div>
""", unsafe_allow_html=True)
