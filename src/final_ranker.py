
import faiss
import pickle

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from src.rule_score import calculate_rule_score
from src.read_jd import read_jd
from src.company_score import company_score
from src.experience_score import experience_score
from src.honeypot_detector import honeypot_penalty
from src.jd_analyzer import analyze_jd

# -----------------------------------
# Load Everything Once
# -----------------------------------

print("Loading Sentence Transformer...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Loading FAISS Index...")
index = faiss.read_index("models/candidate_index.faiss")

print("Loading Candidate Data...")
with open("models/candidate_data.pkl", "rb") as f:
    candidates = pickle.load(f)

print("Loading Candidate Embeddings...")
with open("models/candidate_embeddings.pkl", "rb") as f:
    embeddings = pickle.load(f)

print("Recruiter AI Ready!\n")


# -----------------------------------
# Recruiter Behavior Score
# -----------------------------------

def recruiter_score(signals):

    score = 0

    if signals["open_to_work_flag"]:
        score += 0.25

    score += signals["recruiter_response_rate"] * 0.20
    score += min(signals["github_activity_score"] / 10, 1) * 0.15
    score += min(signals["profile_completeness_score"] / 100, 1) * 0.10
    score += min(signals["interview_completion_rate"], 1) * 0.15
    score += min(signals["offer_acceptance_rate"], 1) * 0.10
    score += min(signals["saved_by_recruiters_30d"] / 10, 1) * 0.05
    score += min(signals["search_appearance_30d"] / 300, 1) * 0.05

    notice = signals["notice_period_days"]

    if notice <= 30:
        score += 0.10
    elif notice <= 60:
        score += 0.05

    return min(score, 1)


# -----------------------------------
# Main Ranking Function
# -----------------------------------

def rank_candidates(jd_text, top_k=10):
    weights = analyze_jd(jd_text)
    # Create JD embedding
    jd_embedding = model.encode([jd_text])

    # Search top candidates using FAISS
    distances, indices = index.search(
    jd_embedding,
    len(candidates)
)

    results = []

    for idx in indices[0]:

        candidate = candidates[idx]

        candidate_embedding = embeddings[idx].reshape(1, -1)

        semantic_score = cosine_similarity(
            jd_embedding,
            candidate_embedding
        )[0][0]

        rule_score = calculate_rule_score(
           candidate,
        jd_text
        ) / 100

        behavior_score = recruiter_score(
            candidate["redrob_signals"]
        )
        company = company_score(candidate)
        exp_score = experience_score(candidate)
        penalty = honeypot_penalty(candidate)
      
        final_score = (

    weights["semantic"] * semantic_score +

    weights["rule"] * rule_score +

    weights["behavior"] * behavior_score +

    weights["company"] * (company / 20) +

    weights["experience"] * (exp_score / 30)

)
   
        final_score -= penalty * 0.02

        final_score = max(final_score, 0)

        profile = candidate["profile"]

        skills = [
            skill["name"]
            for skill in candidate["skills"]
        ]

        results.append({

            "candidate_id": candidate["candidate_id"],

            "name": profile["anonymized_name"],

            "headline": profile["headline"],

            "current_title": profile["current_title"],

            "company": profile["current_company"],

            "experience": profile["years_of_experience"],

            "location": profile["location"],

            "skills": skills,

            "semantic": round(float(semantic_score), 3),

            "rule": round(rule_score, 3),

            "behavior": round(behavior_score, 3),

            "final": round(float(final_score), 3),


        })

    results.sort(
        key=lambda x: x["final"],
        reverse=True
    )

    return results[:top_k]



# -----------------------------------
# Terminal Testing
# -----------------------------------

if __name__ == "__main__":

    from src.read_jd import read_jd

    jd = read_jd()

    results = rank_candidates(jd)

    print("\nTop Candidates\n")

    for i, r in enumerate(results, 1):

        print(
            f"{i}. {r['name']} | "
            f"Final: {r['final']} | "
            f"Semantic: {r['semantic']} | "
            f"Rule: {r['rule']} | "
            f"Behavior: {r['behavior']}"
        )
