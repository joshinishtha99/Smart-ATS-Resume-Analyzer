Smart ATS Resume Analyzer is an AI-powered tool built using **Streamlit**, **Gemini API**, and **Firebase**. It helps job seekers evaluate how well their resumes match a given job description, highlights missing keywords, and offers intelligent feedback, just like an ATS (Applicant Tracking System).

## Features

1. Upload 1 to 3 resumes and compare them side by side  
2. Get a **match score** (%) for each resume against the JD  
3. See **missing keywords** to improve your resume  
4. Get AI-powered suggestions using **Gemini Pro**  
5. Save & view **previous resume scores** after login  
6. User **authentication (Sign Up / Login)** using Firebase  
7. Fully responsive **dark-themed UI** with a clean layout  

- **Frontend/UI**: [Streamlit](https://streamlit.io/)
- **AI Feedback**: [Gemini API](https://ai.google.dev/)
- **Auth & Database**: [Firebase Authentication + Realtime Database (https://firebase.google.com/)
- **PDF Parsing**: PyPDF2
- **Python Libraries**: dotenv, google.generativeai, firebase-admin, pyrebase

## Authentication

- Users can sign up and log in using their email/password.
- Each user's data (resumes, scores, and feedback) is securely stored and accessible only after logging in.
