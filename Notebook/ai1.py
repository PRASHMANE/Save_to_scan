import os
import json
import re
import requests
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
import json

# ---------------------------
# GOOGLE API KEY
# ---------------------------
os.environ["GOOGLE_API_KEY"] = "AIzaSyCL-mUk2B5tSkCnb-tWhrQqhrlY_0pVRCY"

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    temperature=0,
    api_key=os.environ["GOOGLE_API_KEY"]
)

# ---------------------------
# TOOL 1 → CURRENT LOCATION
# ---------------------------
@tool
def get_location(query: str = ""):
    """Returns the user's current latitude and longitude."""
    data = requests.get("http://ip-api.com/json/").json()
    return {"lat": data["lat"], "lon": data["lon"]}

# ---------------------------
# TOOL 2 → NEAREST HOSPITAL WITH PHONE NUMBER
# ---------------------------
@tool
def get_nearest_hospital(location: dict):
    """Returns nearest hospital with phone number and maps link."""
    lat = location["lat"]
    lon = location["lon"]

    # Step 1: Search nearest hospital
    url = (
        f"https://nominatim.openstreetmap.org/search"
        f"?format=json&q=hospital&limit=1&lat={lat}&lon={lon}"
    )
    data = requests.get(url, headers={"User-Agent": "agent"}).json()

    if not data:
        return {"error": "No hospital found"}

    hospital = data[0]
    osm_id = hospital["osm_id"]
    osm_type = hospital["osm_type"]

    # ------------------------
    # Step 2: Overpass API for phone number
    # ------------------------
    overpass_url = "https://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json][timeout:25];
    {osm_type}({osm_id});
    out tags;
    """

    phone = None
    try:
        response = requests.post(
            overpass_url,
            data=overpass_query,
            headers={"User-Agent": "agent"},
            timeout=15
        )

        # Ensure JSON response
        if "application/json" in response.headers.get("Content-Type", ""):
            overpass_data = response.json()
            if overpass_data.get("elements"):
                tags = overpass_data["elements"][0].get("tags", {})
                phone = tags.get("phone") or tags.get("contact:phone")
        else:
            phone = None

    except Exception:
        phone = None

    return {
        "hospital_name": hospital["display_name"],
        "phone_number": phone if phone else "Phone number not available",
        "lat": hospital["lat"],
        "lon": hospital["lon"],
        "google_maps_link": f"https://www.google.com/maps?q={hospital['lat']},{hospital['lon']}"
    }


# ---------------------------
# TOOLS MAP
# ---------------------------
tools = {
    "get_location": get_location,
    "get_nearest_hospital": get_nearest_hospital
}

# ---------------------------
# SYSTEM PROMPT
# ---------------------------
SYSTEM_PROMPT = """
You are a tool-using AI agent.

If user asks for "location" or "nearest hospital":
  Step 1 → Call Action: get_location
  Step 2 → Then call Action: get_nearest_hospital with:
           {"location": {"lat":..., "lon":...}}

Always respond EXACTLY like this when using tools:

Action: tool_name
Action Input: {...}
"""

# ---------------------------
# REACT AGENT
# ---------------------------
def react_agent(user_input):

    # Ask Gemini for the next action
    response = llm.invoke([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ])
    text = response.content

    # Does model want to call a tool?
    if "Action:" in text:
        tool_name = re.search(r"Action:\s*(\w+)", text).group(1)
        raw_input = re.search(r"Action Input:\s*(.*)", text).group(1)

        # Convert Action Input to dict
        try:
            tool_input = json.loads(raw_input)
        except:
            tool_input = {}

        # ---------- Run tool 1 ----------
        result = tools[tool_name].run(tool_input)

        # If step 1 was get_location → run hospital tool automatically
        if tool_name == "get_location":
            location = result
            hospital = tools["get_nearest_hospital"].run({"location": location})

            return {
                "location": location,
                "nearest_hospital": hospital
            }

        return result

    return text


# ---------------------------
# RUN
# ---------------------------
ans=react_agent("Get my current location and nearest hospital with phone number")
#ans=json.loads(ans)
print(ans)
