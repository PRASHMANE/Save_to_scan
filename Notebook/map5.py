import streamlit as st
from streamlit_current_location import current_position

st.title("📍 Current Location with streamlit-current-location")

pos = current_position()
if pos:
    st.write(pos)
    lat = pos["latitude"]
    lon = pos["longitude"]
    st.map([{"lat": lat, "lon": lon}])
else:
    st.warning("Location not available or permission denied.")
