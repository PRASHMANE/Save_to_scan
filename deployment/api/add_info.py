import streamlit as st
import qrcode
import json
import os
import numpy as np
from PIL import Image

# ---- Page Setup ----
#st.set_page_config(page_title="Patient QR Generator")
def add_info():

    st.title("🩺 Life Saving QR Code Generator")
    st.subheader("Enter Your Information")

    # ---- User Inputs ----
    name = st.text_input("Name", placeholder="e.g. Prash")

    phone = st.text_input(" User Phone Number", placeholder="e.g. +91 890xxx183x8",max_chars=10)
    if not phone.isdigit() and phone != "":
        st.error("❌ Phone number must contain only digits (0–9).")
    elif len(phone) < 10 and phone != "":
        st.warning("⚠️ Phone number must be exactly 10 digits — too short.")
    elif len(phone) > 10 and phone != "":
        st.warning("⚠️ Phone number must be exactly 10 digits — too long.")

    Eme_contact1 = st.text_input("Emergency Contact Number 1", placeholder="e.g. +91 890xxx1838",max_chars=10)
    if not Eme_contact1.isdigit() and Eme_contact1 != "":
        st.error("❌ Phone number must contain only digits (0–9).")
    elif len(Eme_contact1) < 10 and Eme_contact1 != "":
        st.warning("⚠️ Phone number must be exactly 10 digits — too short.")
    elif len(Eme_contact1) > 10 and Eme_contact1 != "":
        st.warning("⚠️ Phone number must be exactly 10 digits — too long.")

    Eme_contact2 = st.text_input("Emergency Contact Number 2", placeholder="e.g. +91 8904311xxx",max_chars=10)
    if not Eme_contact2.isdigit() and Eme_contact2 != "":
        st.error("❌ Phone number must contain only digits (0–9).")
    elif len(Eme_contact2) < 10 and Eme_contact2 != "":
        st.warning("⚠️ Phone number must be exactly 10 digits — too short.")
    elif len(Eme_contact2) > 10 and Eme_contact2 != "":
        st.warning("⚠️ Phone number must be exactly 10 digits — too long.")

    Eme_contact3 = st.text_input("Emergency Contact Number 3", placeholder="e.g. +91 890xxx838",max_chars=10)
    if not Eme_contact3.isdigit() and Eme_contact3 != "":
        st.error("❌ Phone number must contain only digits (0–9).")
    elif len(Eme_contact3) < 10 and Eme_contact3 != "":
        st.warning("⚠️ Phone number must be exactly 10 digits — too short.")
    elif len(Eme_contact3) > 10 and Eme_contact3 != "":
        st.warning("⚠️ Phone number must be exactly 10 digits — too long.")

    blood_group = st.text_input("Blood Group", placeholder="e.g. B+")
    medical = st.text_input("Medical Condition(if any)", placeholder="e.g. Diabetes",value="NO")
    ad = st.text_input("Aadhaar Number", placeholder="e.g. 6555 xxxx xxxx 2412")
    insurance = st.text_input("Insurance Number", placeholder="e.g. 890xxxxxxxx",value="NO")
    dob = st.text_input("DOB", placeholder="e.g. 15/09/2004")



    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None and phone.isdigit() and len(phone) == 10 :
        # Create save folder if it doesn't exist
        save_dir = "data"
        os.makedirs(save_dir, exist_ok=True)
        
        # Define save path
        save_path = os.path.join(save_dir, f"{phone}.jpg")
        
        # Save image automatically
        image = Image.open(uploaded_file)
        image.save(save_path, format="JPEG")
        
        st.success(f"✅ Image saved successfully to: {save_path}")
    else:
        st.info("👆 Upload an image to auto-save it.")


    #address = st.text_input("Address", placeholder=" e.g.  4 #main 4#cross Banglore,Karnataka")
    #dob = st.text_input("DOB", placeholder="e.g. 15/09/2004")
    #ad = st.text_input("Aadhaar Number", placeholder="e.g. 6555 xxxx xxxx 2412")
    #blood_group = st.text_input("Blood Group", placeholder="e.g. B+")
    #Eme_contact = st.text_input("Emergency Contact Number", placeholder="e.g. +91 8904311838")
    #insurance = st.text_input("Insurance Number", placeholder="e.g. 890xxxxxxxx")

    # ---- Directory to save QR ----
    #SAVE_DIR = "saved_qr_codes"
    #os.makedirs(SAVE_DIR, exist_ok=True)

    # ---- Generate QR Code ----
    button=st.button("Generate QR Code")
    if button:
        if all([name, Eme_contact1, Eme_contact2, Eme_contact3, blood_group, medical, ad ,insurance ,dob]) and uploaded_file is not None:
            # Combine data
            patient_info = {
                "Name": name,
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

            # Generate QR
            #qr_img = qrcode.make(data)
                    # Generate QR code
            qr = qrcode.make(data)
            qr.save("mane1.png")
            print("✅ QR code created and saved as patient_qr.png")
            st.image("mane1.png", caption=f"{name} QR", use_container_width=True)
            
            

            # Save to local directory
            #filename = f"{name}_qr.png"
            #filepath = os.path.join(SAVE_DIR, filename)
            #qr_img.save(filepath)
        else:
            st.warning("⚠️ Please fill in all fields before generating.")

    if button and all([name, Eme_contact1, Eme_contact2, Eme_contact3, blood_group, medical, ad ,insurance ,dob]) and uploaded_file is not None:
        with open("mane1.png","rb") as file:
            btn = st.download_button(
                label="Download QR Code",
                data=file,
                file_name=f"{name}.png",
                mime="image/png"
            )