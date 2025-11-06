import streamlit as st
from PIL import Image
import base64
import io
import qrcode

# --- Page Setup ---
st.set_page_config(page_title="Scan to Save", layout="wide")

# --- Generate QR Code ---
qr = qrcode.QRCode(box_size=10, border=2)
qr.add_data("https://your-emergency-link.com")
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")

buffered = io.BytesIO()
img.save(buffered, format="PNG")
img_b64 = base64.b64encode(buffered.getvalue()).decode()

# --- CSS for Enhanced ECG Animation ---
st.markdown("""
<style>
body {
    margin: 0;
    padding: 0;
    background: radial-gradient(circle at center, #020202 0%, #000000 100%);
    color: white;
    font-family: 'Poppins', sans-serif;
    overflow: hidden;
}

/* Floating particles background */
@keyframes floatParticles {
    from {background-position: 0 0;}
    to {background-position: 4000px 4000px;}
}
body::before {
    content: "";
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: url('https://i.ibb.co/jb7hJjL/particles.png');
    opacity: 0.08;
    animation: floatParticles 120s linear infinite;
    z-index: -2;
}

/* Pulsing red glow overlay */
body::after {
    content: "";
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(circle at center, rgba(255, 7, 58, 0.15), transparent 70%);
    animation: pulseGlow 1.8s ease-in-out infinite;
    mix-blend-mode: screen;
    z-index: -1;
}
@keyframes pulseGlow {
    0%, 100% {opacity: 0.3;}
    50% {opacity: 0.7;}
}

/* Center layout */
.center {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
}

/* Title */
.project-title {
    font-size: 3.2rem;
    font-weight: 800;
    color: #ff073a;
    letter-spacing: 3px;
    text-shadow: 0 0 25px #ff073a, 0 0 70px #ff073a;
    animation: hologlow 3s ease-in-out infinite alternate;
}
@keyframes hologlow {
    from {text-shadow: 0 0 20px #ff073a;}
    to {text-shadow: 0 0 70px #ff073a, 0 0 150px #ff073a;}
}

/* Advanced ECG heartbeat line */
.ecg {
    position: relative;
    width: 80vw;
    height: 120px;
    margin: 50px auto;
    overflow: hidden;
}
.ecg svg {
    width: 100%;
    height: 100%;
}
.ecg path {
    fill: none;
    stroke: #ff073a;
    stroke-width: 3px;
    stroke-linejoin: round;
    stroke-linecap: round;
    filter: drop-shadow(0 0 12px #ff073a) drop-shadow(0 0 24px #ff073a);
    stroke-dasharray: 250;
    animation: drawECG 2s linear infinite;
}
@keyframes drawECG {
    0% {stroke-dashoffset: 0;}
    100% {stroke-dashoffset: -250;}
}

/* Floating glowing QR */
.qr-container {
    margin-top: 2rem;
    display: inline-block;
    animation: floatQR 3s ease-in-out infinite alternate;
}
.qr-container img {
    width: 230px;
    height: 230px;
    border-radius: 20px;
    box-shadow: 0 0 30px #ff073a, 0 0 80px rgba(255, 7, 58, 0.4);
    animation: glowQR 1.8s ease-in-out infinite alternate;
}
@keyframes floatQR {
    from {transform: translateY(0);}
    to {transform: translateY(-10px);}
}
@keyframes glowQR {
    0%, 100% {box-shadow: 0 0 30px #ff073a, 0 0 60px rgba(255,7,58,0.4);}
    50% {box-shadow: 0 0 60px #ff073a, 0 0 120px rgba(255,7,58,0.6);}
}

/* Scan text pulse */
.scan-text {
    margin-top: 1.5rem;
    font-size: 1.6rem;
    color: #ff073a;
    text-shadow: 0 0 12px #ff073a, 0 0 24px #ff073a;
    letter-spacing: 3px;
    animation: beatText 1.2s ease-in-out infinite;
}
@keyframes beatText {
    0%, 100% {transform: scale(1);}
    50% {transform: scale(1.1);}
}
</style>
""", unsafe_allow_html=True)

# --- HTML Layout ---
st.markdown(f"""
<div class="center">
    <div class="project-title">SCAN TO SAVE</div>
    <div class="ecg">
        <svg viewBox="0 0 600 100">
            <path d="M0,50 L60,50 L80,30 L100,70 L120,50 L180,50 L200,25 L220,75 L240,50 L300,50 L320,30 L340,70 L360,50 L420,50 L440,25 L460,75 L480,50 L540,50 L560,30 L580,70 L600,50"/>
        </svg>
    </div>
    <div class="qr-container">
        <img src="data:image/png;base64,{img_b64}" alt="QR Code">
    </div>
    <div class="scan-text">❤️ SCAN TO SAVE ❤️</div>
</div>
""", unsafe_allow_html=True)
