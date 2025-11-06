import streamlit as st
import qrcode
import json
import os
from PIL import Image

def add_info():
    # ---- Custom CSS ----
    st.markdown("""
    <style>
    /* === GLOBAL BACKGROUND === */
    body {
        background: radial-gradient(circle at top left, #0d0d0d, #1a0000, #330000);
        color: white;
        font-family: 'Poppins', sans-serif;
    }

    /* === TITLE === */
    .main-title {
        text-align: center;
        font-size: 2.8rem;
        color: #ff073a;
        text-shadow: 0 0 25px #ff073a, 0 0 60px #ff073a;
        font-weight: 800;
        margin-top: 10px;
        animation: titlePulse 2s ease-in-out infinite alternate;
    }

    @keyframes titlePulse {
        from { text-shadow: 0 0 15px #ff073a; }
        to { text-shadow: 0 0 45px #ff073a, 0 0 90px #ff073a; }
    }

    /* === HEARTBEAT LINE === */
    .heartbeat-line {
        position: relative;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, transparent, #ff073a, transparent);
        overflow: hidden;
        margin: 25px 0;
    }

    .heartbeat-line::before {
        content: '';
        position: absolute;
        left: -10%;
        width: 20%;
        height: 100%;
        background: #ff073a;
        animation: heartbeatMove 2.5s infinite ease-in-out;
    }

    @keyframes heartbeatMove {
        0% { left: -20%; opacity: 0; }
        25% { left: 25%; opacity: 1; }
        50% { left: 50%; opacity: 0.8; }
        75% { left: 75%; opacity: 1; }
        100% { left: 120%; opacity: 0; }
    }

    /* === INPUT FIELD GLOW === */
    .stTextInput > div > div > input {
        background-color: rgba(255, 7, 58, 0.08);
        border: 2px solid rgba(255, 7, 58, 0.5);
        border-radius: 14px;
        padding: 12px 18px;
        color: #fff;
        font-size: 1rem;
        font-weight: 500;
        box-shadow: 0 0 8px rgba(255, 7, 58, 0.2);
        transition: all 0.4s ease;
        backdrop-filter: blur(6px);
        animation: subtlePulse 3s infinite ease-in-out;
    }

    @keyframes subtlePulse {
        0%, 100% { box-shadow: 0 0 10px rgba(255, 7, 58, 0.3); }
        50% { box-shadow: 0 0 25px rgba(255, 7, 58, 0.7); }
    }

    .stTextInput > div > div > input:focus {
        border-color: #ff073a;
        box-shadow: 0 0 30px #ff073a, inset 0 0 15px rgba(255, 7, 58, 0.6);
        background-color: rgba(255, 7, 58, 0.12);
        transform: scale(1.03);
        transition: all 0.3s ease;
    }

    /* === FLOATING LABELS (KEY TAG STYLE) === */
    .stTextInput label {
        position: relative;
        color: #ff4f7a !important;
        font-weight: 700;
        font-size: 1.05rem;
        letter-spacing: 0.5px;
        text-shadow: 0 0 10px #ff073a, 0 0 25px rgba(255, 7, 58, 0.7);
        animation: glowLabel 2s ease-in-out infinite alternate;
        background: rgba(255, 7, 58, 0.05);
        padding: 4px 12px;
        border-left: 3px solid #ff073a;
        border-radius: 6px;
        display: inline-block;
        margin-bottom: 4px;
    }

    @keyframes glowLabel {
        from { text-shadow: 0 0 10px #ff073a; }
        to { text-shadow: 0 0 25px #ff5075, 0 0 40px #ff073a; }
    }

    /* === FILE UPLOADER === */
    .stFileUploader {
        border-radius: 15px;
        background: rgba(255, 7, 58, 0.06);
        padding: 20px;
        box-shadow: 0 0 20px rgba(255, 7, 58, 0.2);
        transition: all 0.3s ease;
        border: 1.5px dashed rgba(255, 7, 58, 0.6);
    }

    .stFileUploader:hover {
        box-shadow: 0 0 40px rgba(255, 7, 58, 0.8);
        transform: scale(1.02);
        border-color: #ff073a;
    }

    /* === BUTTONS === */
    .stButton > button {
        background: linear-gradient(90deg, #ff073a, #ff4f7a);
        color: white;
        font-weight: 600;
        padding: 12px 28px;
        border-radius: 10px;
        font-size: 1.1rem;
        border: none;
        box-shadow: 0 0 25px rgba(255, 7, 58, 0.7);
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: scale(1.08);
        background: linear-gradient(90deg, #ff5075, #ff073a);
        box-shadow: 0 0 45px rgba(255, 7, 58, 0.9);
    }

    /* === QR CODE DISPLAY === */
    .qr-container {
        text-align: center;
        margin-top: 30px;
        animation: fadeIn 1.5s ease;
    }

    .qr-container img {
        border-radius: 12px;
        box-shadow: 0 0 35px #ff073a;
        animation: pulseQR 2s ease-in-out infinite alternate;
    }

    @keyframes pulseQR {
        from { box-shadow: 0 0 25px #ff073a; }
        to { box-shadow: 0 0 65px #ff073a; }
    }
    </style>
    """, unsafe_allow_html=True)

    # ---- HEADER ----
    st.markdown("<h1 class='main-title'>🩺 Life Saving QR Code Generator</h1>", unsafe_allow_html=True)
    st.markdown("<div class='heartbeat-line'></div>", unsafe_allow_html=True)

    # ---- INPUTS ----
    name = st.text_input("Name", placeholder="e.g. Prashanth")
    phone = st.text_input("User Phone Number", placeholder="e.g. 9876543210", max_chars=10)
    Eme_contact1 = st.text_input("Emergency Contact 1", placeholder="e.g. 9876543210", max_chars=10)
    Eme_contact2 = st.text_input("Emergency Contact 2", placeholder="e.g. 9876543210", max_chars=10)
    Eme_contact3 = st.text_input("Emergency Contact 3", placeholder="e.g. 9876543210", max_chars=10)
    blood_group = st.text_input("Blood Group", placeholder="e.g. B+")
    medical = st.text_input("Medical Condition (if any)", placeholder="e.g. Diabetes", value="NO")
    ad = st.text_input("Aadhaar Number", placeholder="e.g. 6555 xxxx xxxx 2412")
    insurance = st.text_input("Insurance Number", placeholder="e.g. 890xxxxxxxx", value="NO")
    dob = st.text_input("Date of Birth", placeholder="e.g. 15/09/2004")

    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None and phone.isdigit() and len(phone) == 10:
        save_dir = "data"
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, f"{phone}.jpg")
        image = Image.open(uploaded_file)
        image.save(save_path, format="JPEG")
        st.success(f"✅ Image saved successfully to: {save_path}")
    elif uploaded_file is not None:
        st.warning("⚠️ Invalid phone number — please enter a valid 10-digit number.")

    # ---- GENERATE QR ----
    if st.button("Generate QR Code"):
        if all([name, phone, Eme_contact1, Eme_contact2, Eme_contact3, blood_group, medical, ad, insurance, dob]) and uploaded_file is not None:
            patient_info = {
                "Name": name,
                "Phone": phone,
                "Emergency_contact1": Eme_contact1,
                "Emergency_contact2": Eme_contact2,
                "Emergency_contact3": Eme_contact3,
                "Blood_group": blood_group,
                "Medical_condition": medical,
                "Aadhaar": ad,
                "Insurance": insurance,
                "DOB": dob
            }

            data = json.dumps(patient_info)
            qr = qrcode.make(data)
            qr.save("patient_qr.png")

            st.markdown("<div class='qr-container'>", unsafe_allow_html=True)
            st.image("patient_qr.png", caption=f"{name}'s QR Code", use_container_width=False)
            st.markdown("</div>", unsafe_allow_html=True)

            with open("patient_qr.png", "rb") as file:
                st.download_button(
                    label="⬇️ Download QR Code",
                    data=file,
                    file_name=f"{name}_QR.png",
                    mime="image/png"
                )
        else:
            st.warning("⚠️ Please fill in all fields and upload an image before generating the QR Code.")
