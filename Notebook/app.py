import streamlit as st
from streamlit_js_eval import streamlit_js_eval

st.title("📍 Working Real-Time Location Detector")

if st.button("Get My Location"):
    js_code = """
    new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(
            (pos) => resolve({
                latitude: pos.coords.latitude,
                longitude: pos.coords.longitude
            }),
            (err) => resolve(null)
        );
    });
    """

    coords = streamlit_js_eval(js_expressions=js_code, want_output=True)

    if coords:
        lat = coords["latitude"]
        lon = coords["longitude"]

        st.success(f"Latitude: {lat}")
        st.success(f"Longitude: {lon}")

    else:
        st.error("⚠️ Location access blocked. Enable location in browser settings and reload.")
