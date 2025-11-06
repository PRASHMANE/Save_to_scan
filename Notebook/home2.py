import streamlit as st
from PIL import Image
import base64
import io
import qrcode

# --- Page Setup ---
st.set_page_config(page_title="Scan to Save", layout="wide")

# --- Generate a sample QR code dynamically ---
qr = qrcode.QRCode(box_size=10, border=2)
qr.add_data("https://your-emergency-link.com")
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")

buffered = io.BytesIO()
img.save(buffered, format="PNG")
img_b64 = base64.b64encode(buffered.getvalue()).decode()

# --- CSS for Animated Heartbeat & 3D QR Effect ---
st.markdown("""
<style>
body {
    background: radial-gradient(circle at center, #0a0a0a 0%, #000000 100%);
    color: #ffffff;
    font-family: 'Poppins', sans-serif;
    overflow: hidden;
}

/* Heartbeat Line Animation */
.heartbeat {
    position: absolute;
    top: 50%;
    left: 0;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg, transparent, #ff073a, transparent);
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% {transform: scaleX(0);}
    25% {transform: scaleX(1.1);}
    50% {transform: scaleX(1);}
    100% {transform: scaleX(0);}
}

/* Scan to Save Text */
.scan-text {
    position: absolute;
    top: 20%;
    left: 50%;
    transform: translateX(-50%);
    font-size: 3rem;
    font-weight: 700;
    color: #ff073a;
    text-shadow: 0 0 25px #ff073a, 0 0 60px #ff073a;
    letter-spacing: 3px;
    animation: glowText 2s ease-in-out infinite alternate;
}

@keyframes glowText {
    from {text-shadow: 0 0 10px #ff073a, 0 0 20px #ff073a;}
    to {text-shadow: 0 0 40px #ff073a, 0 0 80px #ff073a;}
}

/* Glowing 3D QR */
.qr-container {
    position: absolute;
    top: 55%;
    left: 50%;
    transform: translate(-50%, -50%) rotateY(10deg);
    box-shadow: 0 0 30px rgba(255, 7, 58, 0.6), 0 0 80px rgba(255, 7, 58, 0.3);
    border-radius: 20px;
    animation: floatQR 3s ease-in-out infinite alternate;
}

.qr-container img {
    width: 250px;
    height: 250px;
    border-radius: 15px;
    filter: drop-shadow(0 0 20px #ff073a);
}

@keyframes floatQR {
    from {transform: translate(-50%, -50%) rotateY(10deg) translateY(0);}
    to {transform: translate(-50%, -55%) rotateY(-10deg) translateY(-10px);}
}

/* Moving Background Glow */
@keyframes moveGlow {
    0% {box-shadow: 0 0 20px #ff073a;}
    50% {box-shadow: 0 0 60px #ff073a;}
    100% {box-shadow: 0 0 20px #ff073a;}
}
</style>
""", unsafe_allow_html=True)

# --- HTML Content ---
st.markdown(f"""
<div class="heartbeat"></div>
<div class="scan-text">SCAN TO SAVE ❤️</div>
<div class="qr-container">
    <img src="data:image/png;base64,{img_b64}" alt="QR Code">
</div>
""", unsafe_allow_html=True)
