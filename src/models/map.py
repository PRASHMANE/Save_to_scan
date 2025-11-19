import streamlit as st
from streamlit_current_location import current_position

st.title("map")
pos = current_position()
if pos:
        #st.write(pos)
    lat = pos["latitude"]
    lon = pos["longitude"]
    st.map([{"lat": lat, "lon": lon}])
    print(lat,lon)
        
    
else:
        print("Location not available or permission denied.")