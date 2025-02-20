# app.py
import streamlit as st
import pandas as pd
import re
from resume_parser import extract_text_from_resume, extract_email
from resume_ranker import rank_resumes
import os

def main():
    st.title("Resume Screening and Ranking System")
    
    # Upload job description
    st.subheader("Upload Job Description")
    job_desc = st.text_area("Enter job description", height=200)
    
    # Upload multiple resumes
    st.subheader("Upload Resumes")
    uploaded_files = st.file_uploader("Choose PDF resumes", type="pdf", accept_multiple_files=True)
    
    if st.button("Analyze Resumes") and uploaded_files and job_desc:
        with st.spinner("Processing resumes..."):
            results = []
            
            for file in uploaded_files:
                # Save temporary file
                with open(f"temp_{file.name}", "wb") as f:
                    f.write(file.getbuffer())
                
                # Extract text and email
                text = extract_text_from_resume(f"temp_{file.name}")
                email = extract_email(text)
                
                # Add to results
                results.append({
                    "filename": file.name,
                    "text": text,
                    "email": email
                })
                
                # Clean up temp file
                os.remove(f"temp_{file.name}")
            
            # Rank resumes
            ranked_candidates = rank_resumes(results, job_desc)
            
            # Display results
            st.subheader("Ranked Candidates")
            for rank, candidate in enumerate(ranked_candidates, 1):
                st.markdown(f"**Rank {rank}:** {candidate['filename']}")
                st.markdown(f"**Email:** {candidate['email']}")
                st.markdown(f"**Match Score:** {candidate['score']:.2f}")
                st.markdown("---")
            
            # Export results
            df = pd.DataFrame(ranked_candidates)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Download Results",
                csv,
                "ranked_candidates.csv",
                "text/csv",
                key='download-csv'
            )

if __name__ == "__main__":
    main()