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
    Eme_contact1 = st.text_input("Emergency Contact Number 1", placeholder="e.g. +91 890xxx1838")
    Eme_contact2 = st.text_input("Emergency Contact Number 2", placeholder="e.g. +91 8904311xxx")
    Eme_contact3 = st.text_input("Emergency Contact Number 3", placeholder="e.g. +91 890xxx838")
    blood_group = st.text_input("Blood Group", placeholder="e.g. B+")
    medical = st.text_input("Medical Condition(if any)", placeholder="e.g. Diabetes")
    ad = st.text_input("Aadhaar Number", placeholder="e.g. 6555 xxxx xxxx 2412")
    insurance = st.text_input("Insurance Number", placeholder="e.g. 890xxxxxxxx")
    dob = st.text_input("DOB", placeholder="e.g. 15/09/2004")




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
        if all([name, Eme_contact1, Eme_contact2, Eme_contact3, blood_group, medical, ad ,insurance ,dob]):
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

    if button and all([name, Eme_contact1, Eme_contact2, Eme_contact3, blood_group, medical, ad ,insurance ,dob]):
        with open("mane1.png","rb") as file:
            btn = st.download_button(
                label="Download Image",
                data=file,
                file_name=f"{name}.png",
                mime="image/png"
            )