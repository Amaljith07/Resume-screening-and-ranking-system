import streamlit as st
import pandas as pd
import io
import os
import re

from resume_parser import load_text
from matcher import match_resume_job, skill_gap_analysis
from extract_experience import extract_experience, extract_email, extract_phone, extract_name


# -------------------------------
# Helper: Clean candidate name
# -------------------------------
def clean_candidate_name(filename):
    name = os.path.splitext(filename)[0]
    name = name.replace("_", " ").replace("-", " ").replace(".", " ")
    name = re.sub(r"\b(resume|cv|profile|final|updated)\b", "", name, flags=re.I)
    name = " ".join(name.split()).title()
    return name


# -------------------------------
# Extract Required Experience from Job Description
# -------------------------------
def extract_required_experience(job_description):
    match = re.search(r'(\d+)\+?\s*years?', job_description.lower())
    if match:
        return int(match.group(1))
    return 0


# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="AI Resume Screener", layout="wide")
st.title("🤖 AI Resume Screening & Ranking System")

resume_files = st.file_uploader(
    "Upload Resumes (PDF / DOCX / TXT / CSV)",
    type=["pdf", "docx", "txt", "csv"],
    accept_multiple_files=True
)

job_description = st.text_area(
    "Paste Job Description",
    height=200
)

if st.button("🔍 Analyze Resumes"):

    if not resume_files or job_description.strip() == "":
        st.warning("Please upload resumes and enter a job description.")
    
    else:
        results = []
        required_experience = extract_required_experience(job_description)

        for resume in resume_files:

            # -------------------------------
            # Handle CSV Separately
            # -------------------------------
            if resume.name.endswith(".csv"):
                df_resume = pd.read_csv(resume)
                df_resume.columns = df_resume.columns.str.strip().str.lower()

                resume_text = df_resume.to_string()

                # Try to extract name from CSV column
                if "name" in df_resume.columns:
                    candidate_name = str(df_resume.loc[0, "name"])
                else:
                    candidate_name = clean_candidate_name(resume.name)

            # -------------------------------
            # Handle Other Formats
            # -------------------------------
            else:
                resume_text = load_text(resume)

                # Try NLP name extraction
                candidate_name = extract_name(resume_text)

                # Fallback if name not found
                if not candidate_name or candidate_name.lower() == "unknown":
                    candidate_name = clean_candidate_name(resume.name)

            # -------------------------------
            # Extract Details
            # -------------------------------
            experience = extract_experience(resume_text)
            email = extract_email(resume_text)
            phone = extract_phone(resume_text)

            score = match_resume_job(resume_text, job_description)
            matched, missing = skill_gap_analysis(resume_text, job_description)

            results.append({
                "Candidate Name": candidate_name,
                "Email": email,
                "Phone": phone,
                "Years of Experience": experience,
                "Match %": round(score * 100, 2),
                "Matched Skills": ", ".join(matched),
                "Missing Skills": ", ".join(missing),
                "File Name": resume.name
            })

        df = pd.DataFrame(results)
        df = df.sort_values("Match %", ascending=False)

        st.info(f"📌 Required Experience from Job Description: {required_experience} Years")

        # Filter resumes based on required experience
        filtered_df = df[df["Years of Experience"] >= required_experience]

        # Add rank column
        df.insert(0, "Rank", range(1, len(df) + 1))

        st.subheader("📊 Filtered & Ranked Results")

        if filtered_df.empty:
            st.warning("No candidates meet the required experience.")
        else:
            filtered_df.insert(0, "Rank", range(1, len(filtered_df) + 1))
            st.dataframe(filtered_df, use_container_width=True)

        # -------------------------------
        # CSV Download
        # -------------------------------
        st.download_button(
            label="⬇️ Download CSV",
            data=df.to_csv(index=False),
            file_name="resume_ranking.csv",
            mime="text/csv"
        )

        # -------------------------------
        # Excel Download
        # -------------------------------
        excel_buffer = io.BytesIO()
        df.to_excel(excel_buffer, index=False, engine="openpyxl")
        excel_buffer.seek(0)

        st.download_button(
            label="⬇️ Download Excel",
            data=excel_buffer,
            file_name="resume_ranking.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
