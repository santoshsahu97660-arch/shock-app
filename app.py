# birthday_cake_app_fixed.py
# Run: streamlit run birthday_cake_app_fixed.py

import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="🎂 Birthday Cake App", layout="wide")

st.markdown("""
<style>
body {
  background: radial-gradient(circle at 20% 20%, #ffdde1, #ee9ca7);
  color: #fff;
  font-family: 'Poppins', sans-serif;
  margin: 0;
  padding: 20px;
}
h1 {
  text-align: center;
  color: #ff00aa;
  text-shadow: 0 0 25px #fff;
}
</style>
""", unsafe_allow_html=True)

st.title("🎉 Welcome to the Birthday Cake App 🎉")

name = st.text_input("🎂 Enter your name:")

if st.button("🎁 Celebrate Now!"):
    if name.strip() == "":
        st.warning("Please enter your name first 🎈")
    else:
        # Use a plain string with a placeholder {NAME}, avoid f-strings with many CSS braces
        cake_html_template = """
        <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;margin-top:30px;">
          <h2 style='color:#ff1493;text-shadow:0 0 15px #fff;font-size:40px;'>
            🎉 Happy Birthday {NAME}! 🎉
          </h2>
          
          <div class="cake">
            <div class="plate"></div>
            <div class="layer layer-bottom"></div>
            <div class="layer layer-middle"></div>
            <div class="layer layer-top"></div>
            <div class="icing"></div>
            <div class="drip drip1"></div>
            <div class="drip drip2"></div>
            <div class="drip drip3"></div>
            <div class="candle">
              <div class="flame"></div>
            </div>
          </div>
        </div>

        <style>
        .cake {
          position: relative;
          width: 250px;
          height: 220px;
        }
        .plate {
          position: absolute;
          bottom: 0;
          width: 270px;
          height: 40px;
          background: linear-gradient(#eee,#ddd);
          border-radius: 50%;
          box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }
        .layer {
          position: absolute;
          left: 10px;
          width: 230px;
          height: 50px;
          border-radius: 18px;
        }
        .layer-bottom { bottom: 40px; background: #ff69b4; box-shadow: inset 0 -6px 12px rgba(0,0,0,0.08);}
        .layer-middle { bottom: 90px; background: #ff85c1; box-shadow: inset 0 -6px 12px rgba(0,0,0,0.06);}
        .layer-top { bottom: 140px; background: #ffc0cb; box-shadow: inset 0 -6px 12px rgba(0,0,0,0.04);}
        .icing {
          position: absolute;
          left: 10px;
          bottom: 160px;
          width: 230px;
          height: 22px;
          background: #fff;
          border-radius: 18px;
          box-shadow: 0 6px 10px rgba(255,182,193,0.2);
        }
        .drip {
          position: absolute;
          width: 20px;
          height: 30px;
          background: #fff;
          border-radius: 10px;
          transform-origin: top;
          animation: dripAnim 2s infinite;
        }
        .drip1 { left: 40px; bottom: 130px; animation-delay: 0s; }
        .drip2 { left: 110px; bottom: 120px; animation-delay: 0.2s; }
        .drip3 { left: 180px; bottom: 140px; animation-delay: 0.4s; }

        .candle {
          position: absolute;
          left: 115px;
          bottom: 200px;
          width: 20px;
          height: 60px;
          background: repeating-linear-gradient(
            to bottom, #ff00aa, #ff00aa 10px, #ffffff 10px, #ffffff 20px
          );
          border-radius: 5px;
          box-shadow: 0 6px 12px rgba(0,0,0,0.12);
        }
        .flame {
          position: absolute;
          top: -18px;
          left: 4px;
          width: 12px;
          height: 22px;
          background: radial-gradient(circle, #fff600 0%, #ff8c00 70%);
          border-radius: 50%;
          animation: flicker 0.18s infinite alternate;
          box-shadow: 0 0 18px 6px rgba(255,140,0,0.35);
        }

        @keyframes flicker {
          from { transform: scale(1); opacity: 1; }
          to   { transform: scale(1.15); opacity: 0.85; }
        }
        @keyframes dripAnim {
          0% { transform: scaleY(1); opacity: 1; }
          50% { transform: scaleY(0.9); opacity: 0.9; }
          100% { transform: scaleY(1); opacity: 1; }
        }
        </style>
        """

        # Replace placeholder with actual name (escape HTML if you want to be safe)
        safe_name = st.session_state.get("safe_name", name.strip())
        # Simple sanitize: replace < and > to avoid breaking HTML
        safe_name = safe_name.replace("<", "&lt;").replace(">", "&gt;")
        cake_html = cake_html_template.replace("{NAME}", safe_name)

        st.success(f"🎊 Happy Birthday, {safe_name}! 🎂")
        html(cake_html, height=600)

        # fun celebration
        st.balloons()
