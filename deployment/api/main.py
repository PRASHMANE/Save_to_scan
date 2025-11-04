import streamlit as st
from add_info import add_info
from scan import scan
from result import result

# --- Page setup ---
st.set_page_config(page_title="Scan To Save", layout="wide")

# --- Load Material Icons ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined"
          rel="stylesheet" />
""", unsafe_allow_html=True)

# --- Dark theme CSS ---
st.markdown("""
    <style>
    /* === FORCE DARK BACKGROUND EVERYWHERE === */
    html, body, [class*="stApp"], .main, .block-container {
        background-color: #0a0a0d !important;
        color: #f5f5f5 !important;
    }

    /* Remove any leftover padding/margins from Streamlit container */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 6rem !important;
    }

    /* === Widget Styling === */
    .stTextInput > div > div > input,
    .stNumberInput > div > input {
        background-color: #1a1b1e !important;
        color: #f1f1f1 !important;
        border: 1px solid #333 !important;
        border-radius: 10px !important;
        padding: 0.5rem 0.75rem !important;
    }

    .stButton>button {
        background: linear-gradient(135deg, #3b82f6, #1e40af);
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.2rem !important;
        transition: 0.3s ease-in-out;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        transform: scale(1.05);
        box-shadow: 0 0 15px #3b82f6;
    }

    /* === Bottom Navigation === */
    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: rgba(15, 20, 30, 0.98);
        border-top: 1px solid #1f2937;
        display: flex;
        justify-content: space-around;
        align-items: center;
        padding: 14px 0;
        box-shadow: 0 -2px 25px rgba(0, 0, 0, 0.6);
        z-index: 100;
        backdrop-filter: blur(12px);
    }

    .material-symbols-outlined {
        font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 48;
        font-size: 30px;
        color: #9ca3af;
        cursor: pointer;
        transition: all 0.3s ease-in-out;
        padding: 8px;
        border-radius: 50%;
    }
    .material-symbols-outlined:hover {
        color: #60a5fa;
        transform: scale(1.2);
        text-shadow: 0 0 12px #3b82f6;
        background: rgba(59,130,246,0.1);
    }
    .active {
        color: #60a5fa !important;
        text-shadow: 0 0 16px #3b82f6, 0 0 28px #1d4ed8;
        background: rgba(59,130,246,0.2);
        transform: scale(1.25);
        animation: glowPulse 1.8s infinite ease-in-out;
    }

    @keyframes glowPulse {
        0% { box-shadow: 0 0 0px rgba(59,130,246,0.4); }
        50% { box-shadow: 0 0 18px rgba(59,130,246,0.9); }
        100% { box-shadow: 0 0 0px rgba(59,130,246,0.4); }
    }

    /* === Typography === */
    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: #f0f0f0 !important;
    }

    /* === Ensure space for navbar === */
    body {
        margin-bottom: 90px;
    }



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

# --- Dark theme CSS (GLOBAL) ---
st.markdown("""
    <style>
    html, body, [class*="stApp"], .main, .block-container {
        background-color: #0a0a0d !important;
        color: #f5f5f5 !important;
    }

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 6rem !important;
    }

    .stTextInput > div > div > input,
    .stNumberInput > div > input {
        background-color: #1a1b1e !important;
        color: #f1f1f1 !important;
        border: 1px solid #333 !important;
        border-radius: 10px !important;
        padding: 0.5rem 0.75rem !important;
    }

    .stButton>button {
        background: linear-gradient(135deg, #3b82f6, #1e40af);
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.2rem !important;
        transition: 0.3s ease-in-out;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        transform: scale(1.05);
        box-shadow: 0 0 15px #3b82f6;
    }

    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: rgba(15, 20, 30, 0.98);
        border-top: 1px solid #1f2937;
        display: flex;
        justify-content: space-around;
        align-items: center;
        padding: 14px 0;
        box-shadow: 0 -2px 25px rgba(0, 0, 0, 0.6);
        z-index: 100;
        backdrop-filter: blur(12px);
    }

    .material-symbols-outlined {
        font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 48;
        font-size: 30px;
        color: #9ca3af;
        cursor: pointer;
        transition: all 0.3s ease-in-out;
        padding: 8px;
        border-radius: 50%;
    }

    .material-symbols-outlined:hover {
        color: #60a5fa;
        transform: scale(1.2);
        text-shadow: 0 0 12px #3b82f6;
        background: rgba(59,130,246,0.1);
    }

    .active {
        color: #60a5fa !important;
        text-shadow: 0 0 16px #3b82f6, 0 0 28px #1d4ed8;
        background: rgba(59,130,246,0.2);
        transform: scale(1.25);
        animation: glowPulse 1.8s infinite ease-in-out;
    }

    @keyframes glowPulse {
        0% { box-shadow: 0 0 0px rgba(59,130,246,0.4); }
        50% { box-shadow: 0 0 18px rgba(59,130,246,0.9); }
        100% { box-shadow: 0 0 0px rgba(59,130,246,0.4); }
    }

    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: #f0f0f0 !important;
    }

    /* === Patient Info Box === */
    .center-img {
        display: flex;
        justify-content: center;
        margin-top: 20px;
        margin-bottom: 30px;
    }

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

    [class*="stAppViewContainer"] {
        background-color: #0e0e10;
    }
    </style>
""", unsafe_allow_html=True)




# --- Initialize page state ---
if "page" not in st.session_state:
    st.session_state.page = "home"

# --- Handle navigation ---
query_params = st.query_params
if "page" in query_params:
    new_page = query_params["page"]
    if new_page != st.session_state.page:
        st.session_state.page = new_page

# --- Content ---
if st.session_state.page == "home":
    st.title("🏠 Home")
    st.write("Welcome to the **complete dark theme** dashboard 🌑✨")

elif st.session_state.page == "addinfo":
    add_info()

elif st.session_state.page == "scanner":
    st.title("📷 Scanner")

    # Run scan() only if data not already captured
    if "decoded_data" not in st.session_state:
        decoded = scan()
        if decoded is not None:
            st.session_state.decoded_data = decoded
            st.success("✅ QR decoded successfully!")
    else:
        st.info("✅ QR data already captured — click below to view info.")

    # Show the View Info button when decoded data exists
    if "decoded_data" in st.session_state:
        if st.button("View Info", use_container_width=True):
            st.query_params["page"] = "result"
            st.rerun()



        #go_to_result(decoded)
    #else:
        #st.error("⚠️ No QR code detected. Try again!")

elif st.session_state.page == "chatbot":
    st.title("💬 Chat Bot")
    user_input = st.text_input("Ask something:")
    if user_input:
        st.write(f"🤖 Bot: You said '{user_input}' — reply coming soon!")


elif st.session_state.page == "result":
    import json
    from PIL import Image

    st.title("Person Details")

    st.markdown("""
    <style>
        .info-box {
            background: linear-gradient(145deg, #111827, #1e293b);
            color: #ffffff;
            padding: 20px 25px;
            border-radius: 12px;
            margin-bottom: 15px;
            box-shadow: 0 0 15px rgba(59,130,246,0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .info-box:hover {
            transform: scale(1.02);
            box-shadow: 0 0 25px rgba(59,130,246,0.6);
        }

        .info-title {
            font-size: 18px;
            font-weight: bold;
            color: #60a5fa;  /* Bright blue for labels */
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.8px;
        }
                
        .info-title {
            color: #00f5ff;
            font-weight: bold;
            font-size: 18px;
            text-shadow: 0 0 8px #00f5ff, 0 0 15px #00f5ff;
        }



        .info-value {
            font-size: 16px;
            color: #fbbf24;  /* Gold-yellow for values */
            font-weight: 500;
            letter-spacing: 0.5px;
        }
    </style>
    """, unsafe_allow_html=True)


    decoded = st.session_state.get("decoded_data", None)
    if decoded is not None:
        try:
            data = json.loads(decoded)
        except Exception as e:
            st.error(f"Error reading QR data: {e}")
            st.stop()

        # ---- Patient Info Dictionary ----
        patient_info = {
            "Name": data.get("Name", "N/A"),
            "Emergency Contact 1": data.get("Emergency_contact1", "N/A"),
            "Emergency Contact 2": data.get("Emergency_contact2", "N/A"),
            "Emergency Contact 3": data.get("Emergency_contact3", "N/A"),
            "Blood Group": data.get("Blood_group", "N/A"),
            "Medical Condition": data.get("Medical_condition", "N/A"),
            "Aadhaar": data.get("Aadhaar", "N/A"),
            "Insurance": data.get("Insurance", "N/A"),
            "DOB": data.get("DOB", "N/A")
        }

        # ---- Display Image ----
        image_path = f"data/{data.get('Phone', 'unknown')}.jpg"
        try:
            image = Image.open(image_path)
            st.markdown('<div class="center-img">', unsafe_allow_html=True)
            st.image(image, caption=f"{data.get('Name', 'Patient')}", width=250)
            st.markdown('</div>', unsafe_allow_html=True)
        except FileNotFoundError:
            st.warning("⚠️ Image not found for this patient.")

        # ---- Display Patient Info Boxes ----
        st.markdown('<div style="display: flex; flex-wrap: wrap; gap: 20px;">', unsafe_allow_html=True)
        for key, value in patient_info.items():
            st.markdown(f"""
                <div class="info-box" style="flex: 1 1 45%;">
                    <div class="info-title">{key}</div>
                    <div class="info-value">{value}</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)






# --- Active icon handler ---
def icon_class(page):
    return "material-symbols-outlined active" if st.session_state.page == page else "material-symbols-outlined"


home_icon = icon_class("home")
addinfo_icon = icon_class("addinfo")
scanner_icon = icon_class("scanner")
chatbot_icon = icon_class("chatbot")

# --- Navbar ---
st.markdown(f"""
    <div class="bottom-nav">
        <a href="?page=home" title="Home"><span class="{home_icon}">home</span></a>
        <a href="?page=addinfo" title="Add Info"><span class="{addinfo_icon}">note_add</span></a>
        <a href="?page=scanner" title="Scanner"><span class="{scanner_icon}">qr_code_scanner</span></a>
        <a href="?page=chatbot" title="Chat Bot"><span class="{chatbot_icon}">chat_bubble</span></a>
    </div>
""", unsafe_allow_html=True)
