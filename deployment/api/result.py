import streamlit as st
from PIL import Image
import json 

# ---- Page Setup ----
#st.set_page_config(page_title="Patient Info", layout="centered")



def result(data):
    import json
    # ---- Custom CSS ----
    st.markdown("""
        <style>
        /* Center image */
        .center-img {
            display: flex;
            justify-content: center;
            margin-top: 20px;
            margin-bottom: 30px;
        }

        /* Info box styling */
        .info-box {
            background: #1a1a1a;
            color: #ffffff;
            padding: 20px 25px;
            border-radius: 12px;
            margin-bottom: 15px;
            box-shadow: 0 0 10px rgba(0,0,0,0.5);
        }

        .info-title {
            font-size: 20px;
            font-weight: bold;
            color: #4F8BF9;
            margin-bottom: 5px;
        }

        .info-value {
            font-size: 16px;
            color: #f0f0f0;
        }

        /* Page background */
        [class*="stAppViewContainer"] {
            background-color: #0e0e10;
        }
        </style>
    """, unsafe_allow_html=True)
    if data is not None:
        data = json.loads(data)

        # ---- Example Data (replace with your dynamic data) ----
        patient_info = {
            "Name": data['Name'],
            #"Phone": phone,
            "Emergency_contact1":data['Emergency_contact1'],
            "Emergency_contact2": data['Emergency_contact2'],
            "Emergency_contact3": data['Emergency_contact3'],
            "Blood_group": data['Blood_group'],
            "Medical_condition": data['Medical_condition'],
            "Aadhaar": data['Aadhaar'],
            "Insurance": data['Insurance'],
            "DOB": data['DOB']
        }

        # ---- Display Image ----
        image_path = f"data/{data['Phone']}.jpg"  # Replace with your actual image path
        try:
            image = Image.open(image_path)
            st.markdown('<div class="center-img">', unsafe_allow_html=True)
            st.image(image, caption=f"{data['Name']}", width=250)
            st.markdown('</div>', unsafe_allow_html=True)
        except FileNotFoundError:
            st.error("⚠️ Image not found. Please check the file path.")

        # ---- Display Information ----
        st.markdown("### 🩺 Patient Information")

        for key, value in patient_info.items():
            st.markdown(f"""
                <div class="info-box">
                    <div class="info-title">{key}</div>
                    <div class="info-value">{value}</div>
                </div>
            """, unsafe_allow_html=True)
