from pyzbar.pyzbar import decode
import cv2
import numpy as np
import json
import os

def decode_img():
    image_path = "test.png"

    if not os.path.exists(image_path):
        print("❌ Image not found:", image_path)
        exit()

    # Step 1: Load image
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Step 2: Check brightness (if too dark, invert it)
    mean_brightness = np.mean(gray)
    if mean_brightness < 100:
        gray = cv2.bitwise_not(gray)
        print("🔄 Image inverted (too dark)")

    # Step 3: Brightness & contrast improvement
    gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=30)

    # Step 4: CLAHE for local contrast enhancement
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)

    # Step 5: Denoise & sharpen
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    kernel = np.array([
        [-1, -1, -1],
        [-1,  9, -1],
        [-1, -1, -1]
    ])
    gray = cv2.filter2D(gray, -1, kernel)

    # Step 6: Threshold to clean QR edges
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Step 7: Try decoding (pyzbar first)
    decoded = decode(thresh)
    data = None

    if decoded:
        data = decoded[0].data.decode('utf-8').strip()

    # Step 8: Fallback with OpenCV QRCodeDetector
    if not data:
        detector = cv2.QRCodeDetector()
        data, points, _ = detector.detectAndDecode(thresh)

    # Step 9: Result
    if data:
        print("\n✅ QR Code Detected!")
        print("Decoded QR Data:", data)

        if data.startswith("upi://"):
            print("💰 Payment QR Detected (PhonePe/Paytm)")
        elif data.startswith("{") and data.endswith("}"):
            try:
                patient_info = json.loads(data)
                print("✅ Patient JSON QR:")
                print(json.dumps(patient_info, indent=4))
                return data
            except json.JSONDecodeError:
                print("⚠️ Invalid JSON format.")
        elif data.isdigit():
            print("✅ Patient ID QR Detected:", data)
            #return data
        else:
            print("ℹ️ Unknown QR format.")
    else:
        print("❌ No QR detected — too much darkness or missing contrast.")