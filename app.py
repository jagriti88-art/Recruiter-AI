import streamlit as st
import subprocess

st.set_page_config(page_title="Recruiter AI", layout="wide")

st.title("🤖 AI Candidate Ranking System")

st.write("Upload the Job Description and rank candidates.")

if st.button("Rank Candidates"):

    with st.spinner("Ranking candidates..."):

        result = subprocess.run(
            ["python", "src/final_ranker.py"],
            capture_output=True,
            text=True
        )

    st.success("Ranking Complete!")

    st.text(result.stdout)