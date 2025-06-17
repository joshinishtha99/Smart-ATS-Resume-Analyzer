import os
from dotenv import load_dotenv
import pyrebase

load_dotenv()

config = {
  "apiKey": "AIzaSyA7xWxlTWsyZkt0rbPzaWLngcvgBS4IdVE",
  "authDomain": "ai-resume-analyser-8ec02.firebaseapp.com",
  "databaseURL": "https://ai-resume-analyser-8ec02-default-rtdb.firebaseio.com",
  "projectId": "ai-resume-analyser-8ec02",
  "storageBucket": "ai-resume-analyser-8ec02.firebasestorage.app",
  "messagingSenderId": "1079842393504",
  "appId": "1:1079842393504:web:71c26eda60f9c8e913e8c5"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
