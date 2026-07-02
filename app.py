import streamlit as st
import pdfplumber
from skills import company_skills

# Extract text from PDF
def extract_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text.lower()

# Extract skills (simple matching)
def extract_skills(text):
    all_skills = ["python", "java", "sql", "dbms", "communication", "dsa", "system design"]
    found = []
    for skill in all_skills:
        if skill in text:
            found.append(skill)
    return found

# UI
st.title("SkillMatch AI 🤖")

uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
company = st.selectbox("Select Company", list(company_skills.keys()))

if uploaded_file:
    text = extract_text(uploaded_file)
    resume_skills = extract_skills(text)

    required_skills = company_skills[company]

    matched = list(set(resume_skills) & set(required_skills))
    score = (len(matched) / len(required_skills)) * 100

    st.subheader("📊 Result")
    st.write("Match Score:", round(score, 2), "%")

    if score >= 60:
        st.success("✅ You are Eligible!")
    else:
        st.error("❌ Not Eligible")

    missing = list(set(required_skills) - set(resume_skills))
    st.write("❗ Missing Skills:", missing)