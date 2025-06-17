import streamlit as st
from firebase_config import auth

def login():
    st.subheader("🔐 Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.success("Login successful")
            st.session_state["email"] = email  # ✅ store in session
            st.experimental_rerun()            # 🔁 rerun to load app.py
        except Exception as e:
            st.error(f"Login failed: {e}")

def signup():
    st.subheader("🔐 Sign Up")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")
    if st.button("Sign Up"):
        try:
            user = auth.create_user_with_email_and_password(email, password)
            st.success("Signup successful")
            st.session_state["email"] = email
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Signup failed: {e}")
