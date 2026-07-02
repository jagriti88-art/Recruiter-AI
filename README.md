FRONTEND-
https://drive.google.com/file/d/1tkrzSMYrkE8CADmCB2YL74FUMYtfiBTM/view?usp=sharing


Backend-;
https://drive.google.com/file/d/1qKczNXgwlvE6PLQBHKvDxGR1mOiXwLMb/view?usp=sharing


# 🤖 Recruiter AI
### Intelligent Candidate Discovery & Ranking System

Recruiter AI is an AI-powered candidate search and ranking platform built for the **Redrob Intelligent Candidate Discovery & Ranking Challenge**.

The system combines semantic search, hybrid ranking, recruiter behavior signals, and explainable AI to identify the best candidates from a large talent pool.

---

# Features

✅ Semantic Candidate Search using Sentence Transformers

✅ FAISS Vector Search

✅ Hybrid Ranking Algorithm

- Semantic Similarity
- Rule-based Scoring
- Recruiter Behavior Signals

✅ Explainable Candidate Recommendations

✅ Streamlit Web Interface

✅ Submission CSV Generator

---

# Project Structure

```
Recruiter-ai/
│
├── app.py                  # Streamlit Frontend
├── submit.py               # Generates submission CSV
│
├── src/
│   ├── final_ranker.py
│   ├── rule_score.py
│   ├── explainer.py
│   ├── ui.py
│   ├── read_jd.py
│   ├── embeddings.py
│   ├── faiss_index.py
│   └── ...
│
├── models/
│   ├── candidate_index.faiss
│   ├── candidate_embeddings.pkl
│   └── candidate_data.pkl
│
├── data/
│   ├── candidates.jsonl
│   ├── job_description.docx
│   └── sample_submission.csv
│
├── assets/
│   ├── recruiter.json
│   └── styles.css
│
└── requirements.txt
```

---

# Tech Stack

- Python 3.11
- Streamlit
- Sentence Transformers
- FAISS
- Scikit-Learn
- NumPy
- Pandas
- python-docx

---

# Ranking Pipeline

```
Job Description
        │
        ▼
Sentence Transformer Embedding
        │
        ▼
FAISS Semantic Search
        │
        ▼
Top Candidate Retrieval
        │
        ▼
Hybrid Ranking
   ├── Semantic Score
   ├── Rule Score
   └── Recruiter Behavior Score
        │
        ▼
Final Weighted Score
        │
        ▼
Explainable AI Recommendation
        │
        ▼
Top Ranked Candidates
```

---

# Ranking Formula

Final Score is calculated as:

```
Final Score =
0.50 × Semantic Score
+ 0.30 × Rule Score
+ 0.20 × Recruiter Behavior Score
```

---

# Recruiter Behavior Signals

The ranking incorporates recruiter-oriented signals including:

- Open to Work
- Recruiter Response Rate
- GitHub Activity
- Profile Completeness
- Interview Completion Rate
- Offer Acceptance Rate
- Saved by Recruiters
- Search Appearance
- Notice Period

---

# Running the Web Application

Activate the virtual environment.

Windows

```bash
venv\Scripts\activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Launch Streamlit.

```bash
streamlit run app.py
```

Open

```
http://localhost:8501
```

---

# Generating Candidate Embeddings

Run

```bash
python src/faiss_index.py
```

This generates:

- candidate_index.faiss
- candidate_embeddings.pkl
- candidate_data.pkl

---

# Creating Hackathon Submission

Generate the submission CSV using:

```bash
python submit.py --jd data/job_description.docx --out TEAM_ID.csv
```

Output format:

```
candidate_id
rank
score
reasoning
```

---

# Frontend Workflow

1. Upload Job Description (.docx)

2. System extracts JD text

3. Generate JD embedding

4. Search candidate vectors using FAISS

5. Calculate hybrid score

6. Generate AI reasoning

7. Display ranked candidates

---

# Explainable AI

Each recommended candidate includes a short explanation based on:

- Semantic similarity
- Technical skills
- Professional experience
- Recruiter engagement
- Behavioral signals

---

# Performance

- CPU-only implementation
- Precomputed embeddings
- FAISS indexing for fast retrieval
- Suitable for large candidate datasets
- No external API calls during ranking

---

# Future Improvements

- Learning-to-Rank (XGBoost/LightGBM)
- Cross-Encoder Re-ranking
- Fine-tuned Embedding Models
- Incremental FAISS Updates
- Recruiter Feedback Learning
- Advanced Candidate Filters

---

# Developed For

**Redrob Hackathon 2026**

Intelligent Candidate Discovery & Ranking Challenge




