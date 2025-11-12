import streamlit as st
from streamlit.components.v1 import html
from datetime import date

st.set_page_config(page_title="🎂 Birthday App", layout="wide")

# Page Title
st.title("🎉 Welcome to the Birthday Cake App 🎉")

# Inputs
name = st.text_input("🎂 Enter your name:")
dob = st.date_input("📅 Enter your Date of Birth:", value=date(2000, 1, 1))

# When button clicked
if st.button("🎊 Celebrate Now!"):
    if not name.strip():
        st.warning("Please enter your name first 🎈")
    else:
        # Calculate age
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        # Clean name safely
        safe_name = name.strip().replace("<", "&lt;").replace(">", "&gt;")

        st.success(f"🎂 Happy Birthday, {safe_name}! You are {age} years old 🎉")

        cake_html = f"""
        <div style="text-align:center;margin-top:40px;">
            <h2 style='color:#ff1493;text-shadow:0 0 15px #fff;font-size:40px;'>
                🎉 Happy Birthday {safe_name}! 🎉
            </h2>
            <h3 style='color:#ffe4e1;font-size:22px;margin-top:6px'>
                You are {age} years old today 💖
            </h3>

            <div style="position:relative;width:250px;height:220px;margin:auto;margin-top:25px;">
                <div style="position:absolute;bottom:0;left:-10px;width:270px;height:40px;
                            background:linear-gradient(#eee,#ddd);border-radius:50%;
                            box-shadow:0 6px 12px rgba(0,0,0,0.15);"></div>
                <div style="position:absolute;left:10px;width:230px;height:50px;
                            background:#ff69b4;border-radius:18px;bottom:40px;"></div>
                <div style="position:absolute;left:10px;width:230px;height:50px;
                            background:#ff85c1;border-radius:18px;bottom:90px;"></div>
                <div style="position:absolute;left:10px;width:230px;height:50px;
                            background:#ffc0cb;border-radius:18px;bottom:140px;"></div>
                <div style="position:absolute;left:10px;width:230px;height:22px;
                            background:#fff;border-radius:18px;bottom:160px;"></div>
                <div style="position:absolute;left:115px;bottom:200px;width:20px;height:60px;
                            background:repeating-linear-gradient(to bottom,#ff00aa,#ff00aa 10px,
                            #ffffff 10px,#ffffff 20px);border-radius:5px;"></div>
                <div style="position:absolute;top:0;left:124px;width:12px;height:22px;
                            background:radial-gradient(circle,#fff600 0%,#ff8c00 70%);
                            border-radius:50%;animation:flicker 0.18s infinite alternate;
                            box-shadow:0 0 18px 6px rgba(255,140,0,0.35);"></div>
            </div>

            <style>
            @keyframes flicker {{
                from {{ transform: scale(1); opacity: 1; }}
                to {{ transform: scale(1.15); opacity: 0.85; }}
            }}
            </style>
        </div>
        """

        html(cake_html, height=600)
        st.balloons()
