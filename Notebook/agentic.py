import os
import json
import re
import requests
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

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
# TOOL 1 - LOCATION
# ---------------------------
@tool
def get_location(query: str = ""):
    """Returns the user's current latitude and longitude."""
    data = requests.get("http://ip-api.com/json/").json()
    return {"lat": data["lat"], "lon": data["lon"]}

# ---------------------------
# TOOL 2 - NEAREST HOSPITAL
# ---------------------------
@tool
def get_nearest_hospital(location: dict):
    """Takes location={'lat':..., 'lon':...} and returns nearest hospital."""
    lat = location["lat"]
    lon = location["lon"]

    url = f"https://nominatim.openstreetmap.org/search?format=json&limit=1&q=hospital&lat={lat}&lon={lon}"
    data = requests.get(url, headers={"User-Agent": "agent"}).json()

    if not data:
        return "No hospital found"

    return {
        "hospital_name": data[0]["display_name"],
        "lat": data[0]["lat"],
        "lon": data[0]["lon"]
    }

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

Always respond EXACTLY in this format when calling tools:

Action: tool_name
Action Input: {...}
"""

# ---------------------------
# AGENT
# ---------------------------
def react_agent(user_input):

    response = llm.invoke([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ])
    text = response.content

    # Check for tool call
    if "Action:" in text:
        tool_name = re.search(r"Action:\s*(\w+)", text).group(1)
        raw_input = re.search(r"Action Input:\s*(.*)", text).group(1)

        # Convert Action Input string → dict
        try:
            tool_input = json.loads(raw_input)
        except:
            tool_input = {}

        # Run tool
        result = tools[tool_name].run(tool_input)

        # If location tool → call hospital tool
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
print(react_agent("Get my current location and nearest hospital"))
