# neon_shock_app.py
# Run: streamlit run neon_shock_app.py

import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="Neon Shock App", layout="wide")

# --- Neon Animated Title ---
st.markdown("""
<h1 style='text-align:center;
background: linear-gradient(90deg,#00ffff,#ff00ff,#00ffff);
-webkit-background-clip:text; color:transparent;
font-size:65px; font-weight:900;
animation: pulse 2s infinite;
text-shadow:0 0 25px #0ff;'>
✨ NEON SHOCK APP ✨
</h1>

<style>
@keyframes pulse {
  0% {opacity:0.8; text-shadow:0 0 20px #00ffff;}
  50% {opacity:1; text-shadow:0 0 40px #ff00ff;}
  100% {opacity:0.8; text-shadow:0 0 20px #00ffff;}
}
body {
  background: radial-gradient(circle at 20% 30%, #050014, #000 80%);
  color: white;
  font-family: Poppins, sans-serif;
  overflow-x: hidden;
}
</style>
""", unsafe_allow_html=True)

# --- Custom HTML for Neon Animation -
