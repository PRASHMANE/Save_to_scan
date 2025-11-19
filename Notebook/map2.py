import streamlit as st
import pandas as pd

st.title("📍 Real GPS Location Finder")

# --------------------------
# JavaScript: Get GPS
# --------------------------
gps_script = """
<script>
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;

                // Push values into URL
                const newUrl = window.location.origin + window.location.pathname + 
                               "?latitude=" + lat + "&longitude=" + lon;
                window.location.href = newUrl;
            },
            function(error) {
                alert("GPS Error: " + error.message);
            }
        );
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}
</script>

<button onclick="getLocation()">Get GPS Location</button>
"""

st.components.v1.html(gps_script, height=200)

# --------------------------
# Read query params
# --------------------------
params = st.query_params

if "latitude" in params and "longitude" in params:
    lat = float(params.get("latitude"))
    lon = float(params.get("longitude"))

    st.success("📍 GPS Location Found!")
    st.write("**Latitude:**", lat)
    st.write("**Longitude:**", lon)

    # Create DataFrame for Streamlit map
    df = pd.DataFrame({"lat": [lat], "lon": [lon]})

    st.map(df)
