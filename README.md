# 🚑 Accident QR Emergency Responder

> **One-sentence summary:** A QR-based emergency system that stores a patient's critical info in a QR, lets a responder scan to view details, and — with user approval — instantly sends location and an alert call/SMS to 108 (or the local emergency service) and notifies the patient's emergency contacts.

---

## 📌 Overview

This repository contains the code, documentation, and assets for **Accident QR Emergency Responder** — a simple, privacy-first system to accelerate emergency response at accident scenes using QR codes.

A quick flow:

1. Patient/guardian creates a secure QR containing a minimal emergency profile.
2. First responder or bystander scans the QR with a mobile or web app.
3. The app displays critical medical & contact info.
4. With the patient/guardian's approval (or on their behalf when permitted), the app sends an automated alert to **108** (or chosen emergency number) and notifies emergency contacts with the patient's location and details.

---

## ✨ Features

* QR generation for each patient (encoded JSON payload).
* Fast scan UI showing: name, blood group, known allergies, medications, chronic conditions, emergency contacts, insurance info, and unique patient ID.
* One-tap **Request Approval** flow to confirm sending alerts.
* Automatic location capture (GPS) and emit alert to emergency dispatch (108) and emergency contacts via SMS/WhatsApp/API.
* Audit log of alerts and confirmations (locally/stored backend).
* Privacy-first design: minimal required data, optional fields, encryption at rest.

---

## 🧭 Design & Architecture

```
[Mobile/Web Scanner] --HTTPS--> [Backend API] --SMS/Voice--> [Provider: Twilio/Plivo/Local Gateway]
                          \--DB (encrypted)--> [Audit & Records]
```

* **Mobile/Web Scanner**: Lightweight React Native or PWA that uses `getUserMedia`/native camera for scan, displays the decoded patient JSON, and asks for approval to notify emergency services.
* **Backend API**: Node.js / Python Flask endpoints to accept alert requests, store logs, and forward SMS/call through a telephony provider.
* **Telephony Provider**: Twilio, Plivo, or any local SMS/call gateway used to call 108 via a configured phone or to send templated SMS to emergency contacts.

---

## 🔐 Security & Privacy

* QR contains only necessary fields. Avoid storing long medical histories.
* Sensitive fields must be encrypted before embedding in QR when privacy is required.
* All server traffic must use HTTPS and authentication for management endpoints.
* Data retention policy: default 30 days for logs (configurable); HIPAA-like compliance should be considered for production.

---

## 📱 User Flow — Step by Step

1. **QR is created** by patient or caregiver via the web portal/mobile app (or printed QR card/wristband).
2. At an accident, a bystander or responder **scans** the QR using the scanner app.
3. App decodes JSON and **displays**:

   * Name, Age, Blood Group
   * Allergies
   * Medications
   * Chronic conditions (e.g., diabetes)
   * Emergency contact(s)
   * Insurance ID (optional)
4. App offers two options:

   * **Call now**: Dial the emergency number (108) with a prefilled script.
   * **Send Alert**: Send SMS/WhatsApp/API to 108 and emergency contacts with GPS coordinates + patient snapshot.
5. On confirmation, the backend logs the event and the telephony provider performs the call/SMS.

---

## 🧾 Example QR JSON payload

```json
{
  "name": "Prashanth V",
  "dob": "1990-09-15",
  "blood_group": "B+",
  "allergies": "Penicillin",
  "conditions": "Diabetes",
  "medications": "Metformin",
  "emergency_contacts": [
    {"name":"Sibling","relation":"Brother","phone":"+919599157674"}
  ],
  "insurance": "Policy-ABC-123",
  "created_at": "2025-10-31T12:00:00+05:30"
}
```

> **Tip:** Keep the payload small (under ~1KB) to keep QR readability high.

---

## 🖼️ Screenshots & Assets

> Replace the placeholder images in `assets/` with your own screenshots or mockups. Filenames used below are examples the app references.

* `assets/scan-screen.png` — scanner UI showing camera view and overlay.
* `assets/decoded-info.png` — the page where decoded patient info is shown.
* `assets/approval-dialog.png` — the approval modal before sending alerts.
* `assets/alert-sent.png` — confirmation / toast after alerts are sent.

Markdown image examples (replace with real paths):

```markdown
![Scan screen](assets/scan-screen.png)
![Decoded info screen](assets/decoded-info.png)
```

---

## 🔌 Integration with 108 and Emergency Contacts

**Important legal note:** Automatically initiating a call to 108 may require authorization and appropriate telephony handling. Many countries require human-in-the-loop for emergency calls. The recommended approach:

1. **Prefill & Suggest** — Open phone dialer with 108 and a prefilled message; let the user press call.
2. **Backend Relay (Optional)** — If your organization is authorized, use a telephony API (Twilio/Plivo) to place calls and send SMS to 108 and contacts. The backend should include an alert template with: patient name, age, blood group, known allergies, GPS link (Google Maps), and unique patient ID.

### Sample SMS template

```
Emergency Alert: Possible accident patient.
Name: {name}
ID: {patient_id}
Blood Group: {blood_group}
Allergies: {allergies}
Location: https://maps.google.com/?q={lat},{lon}
Contact: {first_emergency_contact}
```

### Example: cURL to send alert (pseudo)

```bash
curl -X POST https://your-backend.example.com/alerts \
  -H "Content-Type: application/json" \
  -d '{"patient_id":"P00234","lat":12.34,"lon":56.78,"scanned_by":"device-abc"}'
```

---

## 💻 Installation (developer)

1. Clone repo

```bash
git clone https://github.com/PRASHMANE/Save_to_scan
cd Save_to_scan
```

2. Backend install (fastapi)

```bash
pip install fastapi uvicorn
```

3. Frontend (PWA / React)

```bash
pip install streamlit
```

4. For mobile (React Native) — run on device/emulator and enable camera & geolocation permissions.

---

## 🧪 Testing & Demo

* Use a QR generator (or included script `tools/generate_qr.py`) to create test QR codes from the example JSON.
* Use the included mock backend (`backend/mock_gateway.js`) to simulate SMS/call responses during development.

---

## 🛠️ Implementation Notes

* **QR generation:** Use `qrcode` (Node/Python) or native libraries. Use short keys in JSON (`bg` instead of `blood_group`) when space is limited.
* **GPS permissions:** Prompt user and gracefully fallback if denied (show manual lat/lon entry).
* **Offline:** Allow storing alerts locally and syncing when connectivity is restored.

---

## 🚦 UX Recommendations

* Use high-contrast dark mode for scanning (camera overlays) and large, readable font for critical details.
* Provide a single prominent action button labeled `Send Alert` and a secondary `Call 108` button.
* Show clear confirmation and a brief audit summary after sending.

---

## 📈 Roadmap

* [ ] Two-way messaging with emergency dispatch for ETA updates.
* [ ] Direct voice call bridging where regulations permit.
* [ ] Multi-language support for UI and SMS templates.
* [ ] Integration with local hospital networks (FHIR support for medical records).

---

## 🧾 License & Credits

MIT License — include your name/organization. Give credit to contributors and 3rd-party libraries used (qrcode, express/flask, twilio, react-native-camera, etc.).

---

## 📝 Contributors

* Prashanth V — Concept & initial implementation
* (Add contributors here)

---

## 📞 Contact

For help, feature requests, or to contribute, open an issue or contact: `team@yourorg.example`.

---

> Want this README exported as a markdown file, a prettier PDF, or do you want me to generate the placeholder screenshots/mockups for the `assets/` folder? Reply with what you'd like next and I’ll add them directly to the repo.


cloudflared tunnel --url http://localhost:8501