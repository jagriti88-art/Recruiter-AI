import faiss
import pickle
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from read_jd import read_jd
from rule_score import calculate_rule_score


# -----------------------------
# Recruiter Score
# -----------------------------
def recruiter_score(signals):

    score = 0

    if signals["open_to_work_flag"]:
        score += 0.25

    score += signals["recruiter_response_rate"] * 0.20
    score += min(signals["github_activity_score"]/10,1) * 0.15
    score += min(signals["profile_completeness_score"]/100,1) * 0.10
    score += min(signals["interview_completion_rate"],1) * 0.15
    score += min(signals["offer_acceptance_rate"],1) * 0.10
    score += min(signals["saved_by_recruiters_30d"]/10,1) * 0.05
    score += min(signals["search_appearance_30d"]/300,1) * 0.05

    if signals["notice_period_days"] <= 30:
        score += 0.10
    elif signals["notice_period_days"] <= 60:
        score += 0.05

    return min(score,1)


# -----------------------------
# Candidate -> Text
# -----------------------------
def candidate_to_text(candidate):

    p = candidate["profile"]

    text = f"""
Headline: {p['headline']}
Current Title: {p['current_title']}
Experience: {p['years_of_experience']}

Summary:
{p['summary']}

Skills:
"""

    for skill in candidate["skills"]:
        text += skill["name"] + ", "

    text += "\nCareer History:\n"

    for job in candidate["career_history"]:

        text += f"""
Title: {job['title']}
Company: {job['company']}
Description:
{job['description']}
"""

    return text


print("Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Loading FAISS...")
index = faiss.read_index("models/candidate_index.faiss")

with open("models/candidate_data.pkl","rb") as f:
    candidates = pickle.load(f)

print("Reading JD...")
jd = read_jd()

jd_embedding = model.encode([jd])

# -----------------------------
# Retrieve Top 20
# -----------------------------

distances, indices = index.search(jd_embedding,20)

results=[]

for idx in indices[0]:

    candidate = candidates[idx]

    candidate_embedding = model.encode(
        [candidate_to_text(candidate)]
    )

    semantic = cosine_similarity(
        jd_embedding,
        candidate_embedding
    )[0][0]

    rule = calculate_rule_score(candidate)/100

    behavior = recruiter_score(
        candidate["redrob_signals"]
    )

    final = (
        0.50*semantic+
        0.30*rule+
        0.20*behavior
    )

    results.append({

        "name":candidate["profile"]["anonymized_name"],
        "id":candidate["candidate_id"],
        "semantic":round(float(semantic),3),
        "rule":round(rule,3),
        "behavior":round(behavior,3),
        "final":round(float(final),3)

    })

results.sort(key=lambda x:x["final"],reverse=True)

print("\nTOP CANDIDATES\n")

for i,r in enumerate(results[:10],1):

    print(f"{i}. {r['name']}  Score={r['final']}")