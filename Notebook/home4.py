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

# --- CSS for Animations ---
st.markdown("""
<style>
body {
    margin: 0;
    padding: 0;
    background: radial-gradient(circle at center, #030303 0%, #000000 100%);
    color: white;
    font-family: 'Poppins', sans-serif;
    overflow: hidden;
}

/* Background particles */
@keyframes floatParticles {
    from {background-position: 0 0;}
    to {background-position: 10000px 10000px;}
}
body::before {
    content: "";
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: url('https://i.ibb.co/jb7hJjL/particles.png');
    opacity: 0.08;
    animation: floatParticles 200s linear infinite;
    z-index: -2;
}

/* Pulsing red glow overlay */
body::after {
    content: "";
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(circle at center, rgba(255, 7, 58, 0.15), transparent 70%);
    mix-blend-mode: screen;
    animation: pulseGlow 2s ease-in-out infinite;
    z-index: -1;
}
@keyframes pulseGlow {
    from {opacity: 0.4;}
    to {opacity: 0.7;}
}

/* Center layout */
.center {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
}

/* Title - holographic glow */
.project-title {
    font-size: 3.5rem;
    font-weight: 800;
    color: #ff073a;
    letter-spacing: 4px;
    text-transform: uppercase;
    text-shadow: 0 0 25px #ff073a, 0 0 70px #ff073a, 0 0 140px #ff073a;
    animation: hologlow 3s ease-in-out infinite alternate;
}
@keyframes hologlow {
    from {text-shadow: 0 0 15px #ff073a, 0 0 40px #ff073a;}
    to {text-shadow: 0 0 70px #ff073a, 0 0 160px #ff073a;}
}

/* ECG line animation */
.ecg {
    position: relative;
    width: 80vw;
    height: 100px;
    margin: 40px auto;
    overflow: hidden;
}
.ecg::before {
    content: "";
    position: absolute;
    top: 50%;
    left: -100%;
    width: 200%;
    height: 3px;
    background: linear-gradient(90deg, transparent, #ff073a, transparent);
    clip-path: polygon(
        0% 50%, 5% 50%, 10% 30%, 15% 70%, 20% 50%, 25% 50%, 30% 30%, 35% 70%, 
        40% 50%, 45% 50%, 50% 20%, 55% 80%, 60% 50%, 65% 50%, 70% 30%, 75% 70%, 
        80% 50%, 85% 50%, 90% 20%, 95% 80%, 100% 50%
    );
    animation: moveECG 2s linear infinite;
}
@keyframes moveECG {
    from {transform: translateX(0);}
    to {transform: translateX(-50%);}
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
    box-shadow: 0 0 25px #ff073a, 0 0 80px rgba(255, 7, 58, 0.3);
    animation: glowQR 2.5s ease-in-out infinite alternate, rotateQR 10s linear infinite;
}
@keyframes floatQR {
    from {transform: translateY(0);}
    to {transform: translateY(-10px);}
}
@keyframes glowQR {
    from {box-shadow: 0 0 20px #ff073a;}
    to {box-shadow: 0 0 60px #ff073a;}
}
@keyframes rotateQR {
    0% {transform: rotateY(0deg);}
    100% {transform: rotateY(360deg);}
}

/* Scan text animation */
.scan-text {
    margin-top: 1.5rem;
    font-size: 1.5rem;
    color: #ff073a;
    text-shadow: 0 0 10px #ff073a, 0 0 20px #ff073a;
    letter-spacing: 3px;
    animation: beatText 1.2s ease-in-out infinite;
}
@keyframes beatText {
    0%, 100% {transform: scale(1);}
    50% {transform: scale(1.08);}
}
</style>
""", unsafe_allow_html=True)

# --- HTML Layout ---
st.markdown(f"""
<div class="center">
    <div class="project-title">🩺 EMERGENCY QR HEALTH ID</div>
    <div class="ecg"></div>
    <div class="qr-container">
        <img src="data:image/png;base64,{img_b64}" alt="QR Code">
    </div>
    <div class="scan-text">SCAN TO SAVE ❤️</div>
</div>
""", unsafe_allow_html=True)
