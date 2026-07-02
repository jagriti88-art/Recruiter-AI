import json

import streamlit as st
from docx import Document
from streamlit_lottie import st_lottie
from src.final_ranker import rank_candidates, candidates
from src.ui import candidate_card
from src.explainer import generate_reason
import pandas as pd


# ==========================================================
# PAGE CONFIG (Must be first Streamlit command)
# ==========================================================

st.set_page_config(
    page_title="Recruiter AI",
    page_icon="🤖",
    layout="wide"
)


# ==========================================================
# LOAD CSS
# ==========================================================

with open("assets/styles.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def load_lottie(path):
    with open(path, "r") as f:
        return json.load(f)


def read_docx(file):
    doc = Document(file)

    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


# ==========================================================
# LOAD ANIMATION
# ==========================================================

hero_animation = load_lottie("assets/recruiter.json")


# ==========================================================
# HERO SECTION
# ==========================================================

left, right = st.columns([1.4, 1])

with left:

    st.markdown(
        """
<div class="hero-title">
🤖 Recruiter AI
</div>

<div class="hero-sub">
Intelligent Candidate Discovery & Ranking Platform
</div>
""",
        unsafe_allow_html=True
    )

    st.write("")

    st.markdown("""
### 🚀 Why Recruiter AI?

✅ Semantic Candidate Search

✅ Hybrid AI Ranking

✅ Recruiter Behaviour Signals

✅ FAISS Vector Search

✅ LLM Ready
""")


with right:

    st_lottie(
        hero_animation,
        height=380,
        key="hero"
    )


st.divider()


# ==========================================================
# FEATURES
# ==========================================================

c1, c2, c3 = st.columns(3)

with c1:
    st.info("🧠 Semantic Search")

with c2:
    st.info("⚡ Hybrid Ranking")

with c3:
    st.info("🎯 AI Candidate Matching")


st.write("")


# ==========================================================
# DASHBOARD
# ==========================================================
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(
        "👥 Candidates Indexed",
        f"{len(candidates):,}"
    )

with m2:
    st.metric(
        "🧠 Embedding Model",
        "MiniLM-L6-v2"
    )

with m3:
    st.metric(
        "⚡ Vector Search",
        "FAISS"
    )

with m4:
    st.metric(
        "🎯 Ranking",
        "Hybrid AI"
    )


st.divider()


# ==========================================================
# JD INPUT
# ==========================================================

st.markdown("## 📄 Upload Job Description")

st.write(
    "Upload a **DOCX** file or paste the Job Description below."
)

uploaded_file = st.file_uploader(
    "Upload Job Description (.docx)",
    type=["docx"]
)

st.write("### OR")

jd = st.text_area(
    "Paste Job Description",
    height=250,
    placeholder="Paste the complete Job Description here..."
)


st.write("")

# ==========================================================
# TOP-K SELECTION
# ==========================================================

top_k = st.slider(
    "Number of candidates to display",
    min_value=1,
    max_value=20,
    value=5,
    step=1
)

st.write("")

# ==========================================================
# SEARCH BUTTON
# ==========================================================

search = st.button(
    "🚀 Find Best Candidates",
    use_container_width=True
)

# ==========================================================
# SEARCH
# ==========================================================

if search:

    if uploaded_file is not None:
        jd_text = read_docx(uploaded_file)

    elif jd.strip():
        jd_text = jd

    else:
        st.warning("⚠ Please upload or paste a Job Description.")
        st.stop()

    with st.spinner("🤖 AI is analysing candidates..."):

        results = rank_candidates(
            jd_text,
            top_k=top_k
        )

    st.success(f"✅ Found {len(results)} Matching Candidates")

    st.divider()

    st.header("🏆 Top Candidate Matches")

    # Display candidate cards
    for rank, candidate in enumerate(results, start=1):

        candidate["reason"] = generate_reason(candidate)

        candidate_card(candidate, rank)

    # ==========================================================
    # DOWNLOAD CSV
    # ==========================================================

    rows = []

    for rank, candidate in enumerate(results, start=1):

        rows.append({
            "candidate_id": candidate["candidate_id"],
            "rank": rank,
            "score": round(candidate["final"], 6),
            "reasoning": candidate["reason"]
        })

    submission = pd.DataFrame(rows)

    csv = submission.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Submission CSV",
        data=csv,
        file_name="submission.csv",
        mime="text/csv",
        use_container_width=True
    )