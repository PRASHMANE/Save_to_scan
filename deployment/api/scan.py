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

#st.title("📸 Take a Photo")

def scan():
# Streamlit's built-in camera input works on phone too!
    img_file = st.camera_input("Click below to take a photo")

    if img_file:
        img = Image.open(img_file)
        #st.image(img, caption="📷 Captured Photo", use_container_width=True)
        st.success("✅ Photo captured successfully!")
        img_path = "test.png"
        img.save(img_path)
        decode_img()
    