import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from read_jd import read_jd
from rule_score import calculate_rule_score

# ------------------------------------
# Load Embedding Model
# ------------------------------------

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model Loaded!\n")


# ------------------------------------
# Convert Candidate to Text
# ------------------------------------

def candidate_to_text(candidate):

    profile = candidate["profile"]

    text = f"""
Headline: {profile['headline']}
Current Title: {profile['current_title']}
Experience: {profile['years_of_experience']} years

Summary:
{profile['summary']}

Skills:
"""

    for skill in candidate["skills"]:
        text += skill["name"] + ", "

    text += "\n\nCareer History:\n"

    for job in candidate["career_history"]:
        text += f"""
Title: {job['title']}
Company: {job['company']}
Description:
{job['description']}
"""

    return text


# ------------------------------------
# Recruiter Behavior Score
# ------------------------------------

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


# ------------------------------------
# Read Job Description
# ------------------------------------

print("Reading Job Description...")

jd = read_jd()

print("Creating JD Embedding...")

jd_embedding = model.encode(jd)

print("Done!\n")


# ------------------------------------
# Read Candidates
# ------------------------------------

with open("data/sample_candidates.json", "r", encoding="utf-8") as f:
    candidates = json.load(f)


results = []

print("Ranking Candidates...\n")


for candidate in candidates:

    candidate_text = candidate_to_text(candidate)

    candidate_embedding = model.encode(candidate_text)

    semantic_score = cosine_similarity(
        [jd_embedding],
        [candidate_embedding]
    )[0][0]

    behavior_score = recruiter_score(
        candidate["redrob_signals"]
    )

    rule_score = calculate_rule_score(candidate)

    final_score = (
        0.50 * semantic_score +
        0.20 * behavior_score +
        0.30 * (rule_score / 100)
    )

    results.append({
        "candidate_id": candidate["candidate_id"],
        "name": candidate["profile"]["anonymized_name"],
        "semantic_score": round(float(semantic_score), 4),
        "behavior_score": round(float(behavior_score), 4),
        "rule_score": rule_score,
        "final_score": round(float(final_score), 4)
    })


# ------------------------------------
# Sort
# ------------------------------------

results = sorted(
    results,
    key=lambda x: x["final_score"],
    reverse=True
)


# ------------------------------------
# Print Top 10
# ------------------------------------

print("=" * 90)
print("TOP 10 CANDIDATES")
print("=" * 90)

for i, candidate in enumerate(results[:10], start=1):

    print(f"\nRank #{i}")
    print(f"Candidate ID    : {candidate['candidate_id']}")
    print(f"Name            : {candidate['name']}")
    print(f"Semantic Score  : {candidate['semantic_score']}")
    print(f"Behavior Score  : {candidate['behavior_score']}")
    print(f"Rule Score      : {candidate['rule_score']}")
    print(f"Final Score     : {candidate['final_score']}")

print("\nRanking Complete!")