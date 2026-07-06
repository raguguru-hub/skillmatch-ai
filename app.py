import streamlit as st
import PyPDF2

st.set_page_config(page_title="SkillMatch AI", page_icon="🤖")

st.title("SkillMatch AI 🤖")

# Upload Resume
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

# Company Selection
company = st.selectbox("Select Company", ["TCS", "Infosys"])

# Company Skill Requirements
company_skills = {
    "TCS": ["python", "sql", "communication", "machine learning", "data analysis", "excel"],
    "Infosys": ["java", "sql", "communication", "problem solving", "html", "css"]
}

# Extract text from PDF
def extract_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

# Main Logic
if uploaded_file is not None:
    resume_text = extract_text(uploaded_file)

    required_skills = company_skills[company]
    matched_skills = []

    for skill in required_skills:
        if skill in resume_text:
            matched_skills.append(skill)

    match_percent = (len(matched_skills) / len(required_skills)) * 100

    st.subheader("📊 Match Result")
    st.success(f"Your resume matches **{round(match_percent)}%** with {company}")

    st.subheader("✅ Matched Skills")
    st.write(matched_skills)

    st.subheader("❌ Missing Skills")
    missing = list(set(required_skills) - set(matched_skills))
    st.write(missing)
