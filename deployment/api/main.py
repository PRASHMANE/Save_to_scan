import streamlit as st
from add_info1 import add_info
from scan import scan
from result import result
from home import home
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import re
import os
from dotenv import load_dotenv
import torch
from streamlit_current_location import current_position
from src.models.ai import react_agent
from whatapp import alert


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
            
    .custom-text {
    font-size: 18px;              /* Text size */
    color: #00FF00;               /* Text color (bright green) */
    background-color: #1E1E1E;    /* Dark background */
    padding: 10px 15px;           /* Padding inside bubble */
    border-radius: 10px;          /* Rounded corners */
    border: 1px solid #00FF00; 
    </style>
""", unsafe_allow_html=True)

load_dotenv()
api_key = os.getenv("API_KEY")
os.environ["GOOGLE_API_KEY"] = api_key


def clean_asterisks(text: str) -> str:
    cleaned_text = text.replace("*", "")
    cleaned_text = re.sub(r"^\s+", "", cleaned_text, flags=re.MULTILINE)
    return cleaned_text

llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-pro",
                temperature=0,
                api_key=api_key
            )

loader = PyPDFLoader("/Users/prashmane/Documents/Almabetter/a.pdf")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=100
            )
chunks = text_splitter.split_documents(documents)


#from langchain.embeddings import HuggingFaceEmbeddings

device = "cuda" if torch.cuda.is_available() else "cpu"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": device}
)

db = Chroma.from_documents(
                documents=chunks,
                embedding=embeddings,
                collection_name="rag_pdf",
                persist_directory="./chroma_store"
            )

retriever = db.as_retriever()


prompt = ChatPromptTemplate.from_template("""
You are a first-aid expert. Use the following context to provide a **clear, step-by-step explanation** on how to save the person. Keep each step short and actionable.

Context:
{context}

Question:
{question}

Answer (Step-by-step):
1.
""")
rag_chain = (
                {"context": retriever, "question": RunnablePassthrough()}
                | prompt
                | llm
                | StrOutputParser()
            )

pos = current_position()
if pos:
        #st.write(pos)
    lat = pos["latitude"]
    lon = pos["longitude"]
                    #st.map([{"lat": lat, "lon": lon}])
    print(lat,lon)
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
    #st.title("🏠 Home")
    #st.write("Welcome to the **complete dark theme** dashboard 🌑✨")
    home()
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
    st.title("❤️ Chat Bot")
    user_input = st.text_input("Ask your question here:", placeholder="Type your question...")

    if st.button("➡️ Get Answer"):
        if not user_input.strip():
            st.warning("Please type a question!")
        else:
            with st.spinner("Fetching answer... ⏳"):
                ans = rag_chain.invoke(user_input)
                ans = clean_asterisks(ans)
                st.markdown("**Answer:**")
                #st.text(ans)
                st.markdown('<p class="custom-text">{}</p>'.format(ans), unsafe_allow_html=True)



elif st.session_state.page == "result":
    import json
    from PIL import Image

    #st.title("Person Details")

    # --- Heartbeat Red Theme + Glow for Photo ---
    st.markdown("""
    <style>
        /* === GLOBAL BACKGROUND === */
        body {
            background: radial-gradient(circle at top, #0a0000, #1a0000, #330000, #0d0d0d);
            color: #ffffff;
            font-family: 'Poppins', sans-serif;
        }

        /* === PAGE TITLE === */
        h1, h2, h3 {
            color: #ff4d4d;
            text-shadow: 0 0 15px #ff0000;
            animation: heartbeat 2s infinite;
        }

        /* === INFO BOXES === */
        .info-box {
            background: linear-gradient(145deg, #1a0000, #330000);
            color: #ffffff;
            padding: 20px 25px;
            border-radius: 12px;
            margin-bottom: 15px;
            border: 1px solid rgba(255, 0, 0, 0.5);
            box-shadow: 0 0 20px rgba(255, 0, 0, 0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .info-box:hover {
            transform: scale(1.02);
            box-shadow: 0 0 35px rgba(255, 0, 0, 0.6);
        }

        /* === TITLES === */
        .info-title {
            font-size: 18px;
            font-weight: bold;
            color: #ff6666;
            text-shadow: 0 0 8px #ff1a1a, 0 0 15px #ff3333;
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.8px;
        }

        /* === VALUES === */
        .info-value {
            font-size: 16px;
            color: #ffcc66;
            font-weight: 500;
            letter-spacing: 0.5px;
        }

        /* === CENTER IMAGE === */
        .center-img {
            display: flex;
            justify-content: center;
            margin-bottom: 25px;
        }

        .center-img img {
            border-radius: 20px;
            width: 250px;
            height: auto;
            box-shadow: 0 0 25px rgba(255, 0, 0, 0.5), 0 0 50px rgba(255, 0, 0, 0.3);
            animation: photoGlow 2s infinite;
        }

        /* === ANIMATIONS === */
        @keyframes heartbeat {
            0% { transform: scale(1); }
            25% { transform: scale(1.03); }
            50% { transform: scale(1); }
            75% { transform: scale(1.03); }
            100% { transform: scale(1); }
        }

        @keyframes photoGlow {
            0% { box-shadow: 0 0 20px rgba(255, 0, 0, 0.3), 0 0 40px rgba(255, 0, 0, 0.2); }
            50% { box-shadow: 0 0 40px rgba(255, 0, 0, 0.6), 0 0 80px rgba(255, 0, 0, 0.4); }
            100% { box-shadow: 0 0 20px rgba(255, 0, 0, 0.3), 0 0 40px rgba(255, 0, 0, 0.2); }
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
    st.markdown(f"{data['Name']} in Emergency ?")
    col1, col2 = st.columns(2)

        # Button in column 1
    with col1:
            if st.button("Yes"):
                msg=f"🆘 *Emergency Alert* 🆘 *{data['Name']}* met with an emergency/accident. Please call back on *{data['Phone']}* for *Immediate Help*."
                #alert(msg,data['Emergency_contact1'],data['Emergency_contact2'],data['Emergency_contact3'])
        
                ans=react_agent(f"Get my nearest hospital with phone number for {lat},{lon} from india")
                #ans=json.loads(ans)
                print(ans)
                if "ans1" not in st.session_state:
                        #ans=json.loads(ans)
                        if ans is not None:
                            #st.session_state.ans1=ans
                            st.session_state["ans1"]=ans

                        
                #alert(msg,data['Emergency_contact1'])
                #react_agent(f"Get my nearest hospital with phone number for {23.344189719267245},{75.04893578448504}")

                #st.success("You clicked Button 1!")
                st.query_params["page"] = "yes"
                st.rerun()


            if st.button("No"):
                st.query_params["page"] = "home"
                st.rerun()

elif st.session_state.page == "yes":
    st.markdown("""
    <style>
    .info-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.1);
        margin-top: 20px;
        border-left: 6px solid #4CAF50; 
        font-family: 'Arial', sans-serif;
    }

    .info-card h3 {
        margin: 0;
        padding: 0;
        font-size: 22px;
        color: #2e7d32;
    }

    .info-item {
        color: #000000;
        margin-top: 10px;
        font-size: 16px;
        line-height: 1.5;
    }

    .info-item b {
        color: #000000;
        display: inline-block;
        width: 90px;
    }

    .link-btn {
        display: inline-block;
        margin-top: 15px;
        padding: 10px 16px;
        background: #4CAF50;
        color: white !important;
        border-radius: 8px;
        text-decoration: none;
        font-size: 15px;
        transition: background-color 0.3s;
    }

    .link-btn:hover {
        background-color: #45a049;
    }
    
    .info-value {
    color: #000000 !important;
    font-weight: 600;
    }
                
    </style>
    """, unsafe_allow_html=True)

    # ------------------------------------------------
    # Your data
    # ------------------------------------------------
    ans = st.session_state.get("ans1", None)

    if ans is not None:

        hospital_name = str(ans.get('hospital_name', 'N/A'))
        phone_number = str(ans.get('phone_number', 'N/A'))
        lat_str = str(ans.get('lat', 'N/A'))
        lon_str = str(ans.get('lon', 'N/A'))
        google_maps_link = str(ans.get('google_maps_link', '#'))

        st.markdown(f"""
            <div class="info-card">
                <h3><span class="info-value">{hospital_name}</span></h3>
                <div class="info-item"><b>Phone:</b> <span class="info-value">{phone_number}</span></div>
                <div class="info-item"><b>Latitude:</b> <span class="info-value">{lat_str}</span></div>
                <div class="info-item"><b>Longitude:</b> <span class="info-value">{lon_str}</span></div>
                <a class="link-btn" href="{google_maps_link}" target="_blank">
                    📍 Open in Google Maps
                </a>
            </div>
        """, unsafe_allow_html=True)

        # Use float only for st.map()
        #lat = float(ans["lat"])
        #lon = float(ans["lon"])
        #st.map([{"lat": lat, "lon": lon}])

    else:
        st.info("Hospital data is not yet available.")




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
