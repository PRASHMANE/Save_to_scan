import streamlit as st
from PIL import Image
import json
from pyzbar.pyzbar import decode
import cv2
import numpy as np
import json
import os
from decode import decode_img

#st.set_page_config(page_title="📸 Simple Camera")





def scan():
## --- Custom CSS: Heartbeat Theme ---
    st.markdown("""
    <style>
    /* === GLOBAL STYLING === */
    body {
        background: radial-gradient(circle at top, #0a0000, #1a0000, #330000, #0d0d0d);
        color: #fff;
        font-family: 'Poppins', sans-serif;
    }

    /* === TITLE === */
    h1, h2, h3, h4 {
        color: #ff4d4d;
        text-shadow: 0 0 10px #ff0000;
        animation: heartbeat 2s infinite;
    }

    /* === CAMERA INPUT CONTAINER === */
    [data-testid="stCameraInput"] {
        border: 2px solid rgba(255, 0, 0, 0.6);
        border-radius: 20px;
        box-shadow: 0 0 25px rgba(255, 0, 0, 0.3);
        padding: 10px;
        animation: pulseGlow 2s infinite;
    }

    /* === SUCCESS MESSAGE === */
    .stAlert {
        background: linear-gradient(90deg, #2a0000, #550000);
        border: 1px solid #ff4d4d;
        box-shadow: 0 0 10px #ff0000;
        border-radius: 12px;
        color: white;
    }

    /* === BUTTONS === */
    button[kind="primary"] {
        background: linear-gradient(90deg, #ff0000, #b30000);
        border: none;
        border-radius: 12px;
        color: white;
        font-weight: 600;
        transition: all 0.3s ease-in-out;
    }
    button[kind="primary"]:hover {
        background: linear-gradient(90deg, #ff4d4d, #e60000);
        box-shadow: 0 0 15px #ff1a1a;
        transform: scale(1.05);
    }

    /* === ANIMATIONS === */
    @keyframes heartbeat {
        0% { transform: scale(1); }
        25% { transform: scale(1.03); }
        50% { transform: scale(1); }
        75% { transform: scale(1.03); }
        100% { transform: scale(1); }
    }
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 10px rgba(255, 0, 0, 0.4); }
        50% { box-shadow: 0 0 25px rgba(255, 0, 0, 0.8); }
        100% { box-shadow: 0 0 10px rgba(255, 0, 0, 0.4); }
    }
    </style>
    """, unsafe_allow_html=True)


# --- CAMERA SCAN FUNCTION ---
#def scan():
    st.markdown("<h2>❤️ Emergency QR Scanner</h2>", unsafe_allow_html=True)

    # Streamlit's built-in camera input (works on mobile too)
    img_file = st.camera_input("Click below to take a photo")

    if img_file:
        img = Image.open(img_file)
        st.success("✅ Photo captured successfully!")
        img_path = "test.png"
        img.save(img_path)

        decoded = decode_img()
        st.markdown(f"<h4>📜 Decoded Data:</h4><div style='color:#ff6666;'>{decoded}</div>", unsafe_allow_html=True)
        return decoded