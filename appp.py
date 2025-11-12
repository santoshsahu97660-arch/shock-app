import streamlit as st
import pandas as pd
import os
import random
from datetime import datetime, timedelta

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Data Science Practice", page_icon="📘", layout="wide")
st.title("📘 Data Science Practice")

st.markdown("### 💰 Entry Fee: ₹10 (Just for fun)")
st.info("You have **15 minutes** to complete the quiz. Timer will keep running ⏱️")

# ---------------- QUIZ DATA (sample 10 shown; you can extend to 50 same pattern) ----------------
quiz_data = [
    {"question": "Which library is mainly used for data manipulation and analysis in Python?",
     "options": ["NumPy", "Matplotlib", "Pandas", "Seaborn"], "answer": "Pandas"},
    {"question": "Which function is used to read CSV files in pandas?",
     "options": ["pd.read()", "pd.read_csv()", "pd.open_csv()", "pd.load_csv()"], "answer": "pd.read_csv()"},
    {"question": "Which of these is a supervised learning algorithm?",
     "options": ["K-Means", "Linear Regression", "DBSCAN", "PCA"], "answer": "Linear Regression"},
    {"question": "Which library is used for data visualization?",
     "options": ["TensorFlow", "Scikit-learn", "Matplotlib", "Flask"], "answer": "Matplotlib"},
    {"question": "Which of the following is used for machine learning?",
     "options": ["scikit-learn", "pygame", "flask", "pillow"], "answer": "scikit-learn"},
    {"question": "Which of the following handles missing data in pandas?",
     "options": ["fillna()", "drop()", "replace()", "append()"], "answer": "fillna()"},
    {"question": "Which command installs a Python package?",
     "options": ["python install", "pip install", "import install", "setup install"], "answer": "pip install"},
    {"question": "Which of these is NOT a Python data type?",
     "options": ["List", "Tuple", "Dictionary", "Tree"], "answer": "Tree"},
    {"question": "Which keyword defines a function in Python?",
     "options": ["function", "def", "lambda", "fun"], "answer": "def"},
    {"question": "Which operator is used for exponentiation?",
     "options": ["*", "**", "^", "//"], "answer": "**"},
]
TOTAL_Q = len(quiz_data)

# ---------------- USER LOGIN ----------------
st.subheader("Login to Start Quiz")
name = st.text_input("Enter your Name")
mobile = st.text_input("Enter your Mobile Number")

if not name or not mobile:
    st.info("Please enter your name and mobile number to start the quiz.")
    st.stop()

# ---------------- SHUFFLE QUESTIONS IF RE-ATTEMPT ----------------
attempts_file = "attempts.csv"
if os.path.exists(attempts_file):
    df_attempts = pd.read_csv(attempts_file)
    if not df_attempts[df_attempts["mobile"] == mobile].empty:
        st.warning("⚠️ You have already attempted before — questions shuffled.")
        random.shuffle(quiz_data)

# ---------------- LIVE TIMER (15 minutes) ----------------
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=1000, key="timer_refresh")  # refresh every second

if "start_time" not in st.session_state:
    st.session_state["start_time"] = datetime.now()
if "quiz_submitted" not in st.session_state:
    st.session_state["quiz_submitted"] = False

elapsed = (datetime.now() - st.session_state["start_time"]).total_seconds()
time_left = max(0, 900 - int(elapsed))  # 15 min = 900 sec

min_left = time_left // 60
sec_left = time_left % 60
col1, col2 = st.columns(2)
with col1:
    st.info(f"🕒 Time Left: {int(min_left):02d}:{int(sec_left):02d}")
with col2:
    st.success(f"👤 {name} | 📱 {mobile}")

if time_left <= 0 and not st.session_state["quiz_submitted"]:
    st.session_state["quiz_submitted"] = True
    st.warning("⏰ Time's up! Auto-submitting your answers...")
    auto_submit = True
else:
    auto_submit = False

# ---------------- QUIZ SESSION ----------------
if "answers" not in st.session_state:
    st.session_state["answers"] = [None] * TOTAL_Q
if "submitted" not in st.session_state:
    st.session_state["submitted"] = [False] * TOTAL_Q
if "score" not in st.session_state:
    st.session_state["score"] = 0

# ---------------- QUIZ DISPLAY ----------------
for i, q in enumerate(quiz_data):
    st.write(f"### Q{i+1}. {q['question']}")
    choice = st.radio("Choose your answer:", q["options"], key=f"q{i}")
    st.session_state["answers"][i] = choice

    if not st.session_state["submitted"][i]:
        if st.button(f"Submit Answer {i+1}", key=f"btn_{i}"):
            st.session_state["submitted"][i] = True
            if choice == q["answer"]:
                st.success("✅ Correct!")
                st.session_state["score"] += 1
            else:
                st.error("❌ Wrong Answer!")

st.markdown("---")

# ---------------- FINISH QUIZ ----------------
def finish_quiz():
    st.session_state["quiz_submitted"] = True
    score = st.session_state["score"]
    st.success(f"Your Final Score: {score}/{TOTAL_Q}")

    # Save attempt
    attempt = pd.DataFrame([{
        "timestamp": datetime.now().isoformat(),
        "name": name,
        "mobile": mobile,
        "score": score
    }])
    if os.path.exists(attempts_file):
        df = pd.read_csv(attempts_file)
        df = pd.concat([df, attempt], ignore_index=True)
    else:
        df = attempt
    df.to_csv(attempts_file, index=False)

    # Perfect Score Celebration
    if score == TOTAL_Q:
        st.balloons()
        st.markdown("## 🏆 **LEGENDARY ACHIEVEMENT! You scored 50/50!** 🥇")
        st.markdown("""
        <div style='background-color:#fff3cd;padding:20px;border-radius:15px;border:2px solid #ffb703;'>
        <h2 style='color:#d97706;text-align:center;'>🥇 Congratulations, {name}! 🥇</h2>
        <p style='font-size:18px;text-align:center;color:#333;'>
        You’ve conquered every question with perfection — your consistency and logic are admirable! 🌟
        </p>
        <p style='font-size:18px;text-align:center;color:#2b9348;'>
        🎁 Reward: Digital Certificate + Lifetime Masterclass + Hall of Fame Entry 🎖️
        </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("✅ Quiz submitted. Only full scorers appear in leaderboard.")

    # Leaderboard
    st.markdown("### 🏆 Top Scorers")
    if os.path.exists("attempts.csv"):
        df = pd.read_csv("attempts.csv")
        top = df.sort_values(by="score", ascending=False).head(10)
        st.dataframe(top)

# ---------------- AUTO OR MANUAL SUBMIT ----------------
if auto_submit or st.button("Finish and Submit Quiz"):
    finish_quiz()
