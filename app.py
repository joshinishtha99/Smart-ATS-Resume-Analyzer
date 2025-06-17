import streamlit as st

st.set_page_config(page_title="Smart ATS", layout="centered")

import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from firebase_config import db,auth
from login_signup import login, signup

# Load custom CSS from external file
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    
# ------------------- SIGN OUT SECTION-------------------
col1, col2 = st.columns([6, 1])
with col2:
    st.markdown('<div class="signout-button">', unsafe_allow_html=True)
    if st.button("🔓 Sign Out", key="signout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("Signed out successfully!")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ------------------- LOGIN SECTION -------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login / Sign Up")
    choice = st.selectbox("Choose", ["Login", "Sign Up"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Submit"):
        try:
            if choice == "Sign Up":
                auth.create_user_with_email_and_password(email, password)
                st.success("✅ Account created! You can now log in.")
                st.rerun()
            else:
                user = auth.sign_in_with_email_and_password(email, password)
                st.session_state.user = user
                st.session_state.email = email
                st.session_state.logged_in = True
                st.success("✅ Logged in successfully!")
                st.rerun()
        except Exception as e:
            st.error(f"❌ Auth Error: {e}")
    st.stop()

# ------------------- MAIN APP (After Login) -------------------
# ✅ Now safe to access session_state.email
user_id = st.session_state.email.replace(".", "_")

st.title("🧠 Smart ATS Analyzer")
st.write(f"Welcome, **{st.session_state.email}**!")

# ------------------- RESUME HISTORY -------------------


with st.expander("📁 View Past Resume Scores"):
    try:
        history = db.child("resumes").child(user_id).get()
        if history.each():
            for item in history.each():
                data = item.val()
                st.markdown(f"**{data['filename']}** - Score: {data['score']}%")
                st.caption("Missing Keywords: " + ", ".join(data["missing"][:5]))
        else:
            st.info("No past resumes found.")
    except Exception as e:
        st.warning("⚠️ No past resume records found or unable to connect to database.")





load_dotenv()  
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

chat = genai.GenerativeModel("models/gemini-1.5-flash-latest").start_chat(history=[])

def chat_with_gemini(user_question):
    response = chat.send_message(user_question)
    return response.text

def get_gemini_response(input):
    model = genai.GenerativeModel("gemini-2.0-flash-lite")
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        text += str(reader.pages[page].extract_text())
    return text

def score_resume(jd_text, resume_text):
    jd_words = set(jd_text.lower().split())
    resume_words = set(resume_text.lower().split())
    matched_keywords = jd_words & resume_words
    missing_keywords = jd_words - resume_words
    score = (len(matched_keywords) / len(jd_words)) * 100 if jd_words else 0
    return round(score, 2), list(missing_keywords)




with st.sidebar:
    st.title("💬 Resume Chatbot")
    user_question = st.text_input("Ask me anything about resumes...")

    if st.button("How do I write a good resume summary?"):
        user_question = "How do I write a good resume summary?"

    if user_question:
        with st.spinner("Thinking..."):
            reply = chat_with_gemini(user_question)
            st.markdown(f"**🤖 Gemini:** {reply}")

st.title("🧠 Smart ATS Analyzer")
st.caption("Improve your resume with AI-powered analysis.")

tab1, tab2 = st.tabs(["📄 ATS Analysis", "💬 Gemini Feedback"])

with tab1:
    st.subheader("📄 ATS Scanner")
    st.markdown('<p style="color: #cccccc; font-size: 16px; font-weight: 600;">Paste the Job Description</p>', unsafe_allow_html=True)
jd = st.text_area(label="", height=200)

st.markdown('<p style="color: #cccccc; font-size: 16px; font-weight: 600;">Upload Your Resumes (2–3)</p>', unsafe_allow_html=True)
uploaded_files = st.file_uploader(label="", type="pdf", accept_multiple_files=True)

run_check = st.button("Run ATS Check")

if run_check:
        if uploaded_files and jd.strip() != "" and len(uploaded_files) >= 2:
            results = []
            for file in uploaded_files:
                resume_text = input_pdf_text(file)
                score, missing = score_resume(jd, resume_text)
                results.append({
                    "filename": file.name,
                    "score": score,
                    "missing": missing,
                    "text": resume_text
                })

            st.success("✅ Analysis Complete")
            st.subheader("📊 Resume Comparison Results")

            cols = st.columns(len(results))
            for col, result in zip(cols, results):
                with col:
                    st.markdown(f"**📄 {result['filename']}**")
                    st.metric("Match Score", f"{result['score']:.2f}%")
                    st.caption("🕳️ Missing Keywords")
                    st.write(", ".join(result["missing"][:8]) if result["missing"] else "None")

            best_resume = max(results, key=lambda x: x["score"])
            st.success(f"🎯 Best Resume: **{best_resume['filename']}** with **{best_resume['score']:.2f}%** match")
            user_id = st.session_state.email.replace(".", "_")  # replace . for firebase key compatibility

            for result in results:
                db.child("resumes").child(user_id).push({
                "filename": result["filename"],
                "score": result["score"],
                "missing": result["missing"]
    })

            # Save for Gemini Feedback
            st.session_state.jd = jd
            st.session_state.resume_text = best_resume['text']
            st.session_state.score = best_resume['score']
            st.session_state.missing = best_resume['missing']

            # Prepare prompt for Gemini
            prompt = f"""
You are an advanced Applicant Tracking System (ATS) designed to evaluate resumes based on job descriptions.

Your task is to analyze the resume provided below in the context of the job description.
You should provide feedback on:
- How well the resume matches the job description
- What keywords or skills are missing
- Suggestions for improving the resume to increase the match

Job Description:
{jd}

Resume:
{best_resume['text']}

Match Score: {best_resume['score']}%

Missing Keywords:
{best_resume['missing']}

Provide your suggestions in a professional and detailed format.
"""
            response = get_gemini_response(prompt)

            st.session_state.response = response

            # Display Gemini Feedback Summary
            st.success("✅ Gemini Feedback Generated")
            st.metric("🔍 ATS Match Score", f"{best_resume['score']:.2f}%")

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=best_resume['score'],
                title={"text": "Resume Match %"},
                gauge={"axis": {"range": [0, 100]}}
            ))
            st.plotly_chart(fig)

            st.subheader("🕳️ Missing Keywords")
            st.warning(", ".join(best_resume['missing'][:15]) if best_resume['missing'] else "None! Great match.")
        else:
            st.error("Please upload at least 2 resumes and enter the job description.")

with tab2:
    st.subheader("💬 Gemini AI Feedback")
    if "response" in st.session_state:
        st.write(st.session_state.response)
    else:
        st.info("Please run the ATS analysis first in the previous tab.")
