import streamlit as st
import pandas as pd
import PyPDF2

st.set_page_config(page_title="SkillMatch AI", page_icon="🎯")

st.title("🎯 SkillMatch AI")

# Upload Excel
excel_file = st.file_uploader("Upload Student Excel", type=["xlsx"])

# Upload Resume
resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# Extract text from PDF
def extract_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

# Button
if st.button("Check Eligibility"):

    if excel_file is None or resume_file is None:
        st.warning("Please upload both Excel and Resume")
    
    else:
        df = pd.read_excel(excel_file)

        resume_text = extract_text(resume_file)

        results = []

        for index, row in df.iterrows():
            name = row['Name']
            skills = str(row['Skills']).lower()

            matched = True

            for skill in skills.split(","):
                if skill.strip() not in resume_text:
                    matched = False
                    break

            status = "Eligible" if matched else "Not Eligible"

            results.append({
                "Name": name,
                "Status": status
            })

        result_df = pd.DataFrame(results)

        st.subheader("📊 Results")
        st.dataframe(result_df)

        # Download button
        csv = result_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download Results",
            csv,
            "results.csv",
            "text/csv"
        )
