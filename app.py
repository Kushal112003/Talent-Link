import streamlit as st
import os
import json
import datetime
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import fitz  # PyMuPDF
import re
import pandas as pd

style.use("ggplot")

st.set_page_config(page_title="AI Resume Screener", layout="wide", page_icon="🧠")
st.markdown("<h1 style='text-align: center; color: white;'>🧠 AI Resume Screening & Candidate Ranking System</h1>", unsafe_allow_html=True)

# Constants
DATA_DIR = os.path.join(os.path.dirname(__file__), "score_history")
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploaded_resumes")
SAMPLE_RESUME_DIR = os.path.join(os.path.dirname(__file__), "sample resumes")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- Utility Functions ---
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(pdf_file)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def calculate_score(resume_text, job_description):
    resume_text = resume_text.lower()
    job_description = job_description.lower()
    job_keywords = re.findall(r'\b\w+\b', job_description)
    match_count = sum(1 for word in job_keywords if word in resume_text)
    return round((match_count / len(job_keywords)) * 100, 2) if job_keywords else 0.0

def save_score_history(name, score):
    history_path = os.path.join(DATA_DIR, f"{name}.json")
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if os.path.exists(history_path):
        with open(history_path, 'r') as f:
            data = json.load(f)
    else:
        data = []
    data.append({"timestamp": now, "score": score})
    with open(history_path, 'w') as f:
        json.dump(data, f, indent=2)

def load_score_history(name):
    history_path = os.path.join(DATA_DIR, f"{name}.json")
    if os.path.exists(history_path):
        with open(history_path, 'r') as f:
            return json.load(f)
    return []

def mock_ai_suggestions(resume_text, job_description):
    suggestions = []
    if len(resume_text) < 300:
        suggestions.append("🔧 Add more content to your resume to highlight your experience.")
    if "team" not in resume_text:
        suggestions.append("🤝 Include team-based experiences or collaboration examples.")
    if any(word in job_description.lower() and word not in resume_text.lower() for word in ["python", "machine learning", "cloud"]):
        suggestions.append("📌 Add relevant technical keywords from the job description.")
    suggestions.append("✅ Use action verbs and match job role language.")
    return suggestions

def display_score_graph(history):
    if len(history) < 2:
        st.info("More resume uploads needed to show progress graph.")
        return
    timestamps = [entry['timestamp'] for entry in history]
    scores = [entry['score'] for entry in history]
    fig, ax = plt.subplots()
    ax.plot(timestamps, scores, marker='o', color='blue')
    ax.set_xlabel("Date")
    ax.set_ylabel("Score")
    ax.set_title("Resume Score Over Time")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# --- UI Components ---
user_type = st.sidebar.selectbox("Select User Type", ["Candidate", "Recruiter"])

if user_type == "Candidate":
    st.subheader("💼 Test Your Resume Against a Job Description")
    name = st.text_input("Enter your name (for history tracking):")
    job_desc = st.text_area("Paste the job description here")
    uploaded_resume = st.file_uploader("Upload your resume (PDF only)", type=['pdf'])

    if uploaded_resume and name and job_desc:
        file_path = os.path.join(UPLOAD_DIR, uploaded_resume.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_resume.getbuffer())

        resume_text = extract_text_from_pdf(file_path)
        score = calculate_score(resume_text, job_desc)
        save_score_history(name, score)

        st.success(f"Your resume ATS score is: {score}%")

        st.subheader("📋 Suggestions to Improve:")
        suggestions = mock_ai_suggestions(resume_text, job_desc)
        for s in suggestions:
            st.markdown(f"- {s}")

        st.subheader("📈 Your Score Progress:")
        score_history = load_score_history(name)
        display_score_graph(score_history)

elif user_type == "Recruiter":
    st.subheader("📊 Recruiter Dashboard")

    job_desc = st.text_area("Paste the job description (used for scoring):")
    resume_files = st.file_uploader("Upload multiple resumes (PDF)", type=['pdf'], accept_multiple_files=True)

    if job_desc and resume_files:
        st.markdown("### 📋 Resume Score Table")
        data = []

        for pdf_file in resume_files:
            file_path = os.path.join(UPLOAD_DIR, pdf_file.name)
            with open(file_path, "wb") as f:
                f.write(pdf_file.getbuffer())

            resume_text = extract_text_from_pdf(file_path)
            score = calculate_score(resume_text, job_desc)
            suggestions = mock_ai_suggestions(resume_text, job_desc)
            name = os.path.splitext(pdf_file.name)[0]

            data.append({
                "Candidate Name": name,
                "ATS Score (%)": score,
                "Suggestions": " | ".join(suggestions)
            })

        if data:
            df = pd.DataFrame(data)
            st.dataframe(df.sort_values(by="ATS Score (%)", ascending=False), use_container_width=True)
