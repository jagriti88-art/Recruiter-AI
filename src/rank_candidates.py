import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from scoring import experience_score, behavioral_score

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


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

    # Skills
    for skill in candidate["skills"]:
        text += skill["name"] + ", "

    # Career history
    text += "\nCareer History:\n"

    for job in candidate["career_history"]:
        text += f"""
Title: {job['title']}
Company: {job['company']}
Description:
{job['description']}
"""

    return text


# ---------------------------
# Read Job Description
# ---------------------------

from read_jd import read_jd

jd = read_jd()

jd_embedding = model.encode(jd)


# ---------------------------
# Read Candidates
# ---------------------------

with open("data/sample_candidates.json", "r", encoding="utf-8") as f:
    candidates = json.load(f)


results = []

for candidate in candidates:

    text = candidate_to_text(candidate)

    candidate_embedding = model.encode(text)

    score = cosine_similarity(
        [jd_embedding],
        [candidate_embedding]
    )[0][0]

    # results.append({
    #     "candidate_id": candidate["candidate_id"],
    #     "name": candidate["profile"]["anonymized_name"],
    #     "score": score
    # })
    semantic = float(score)
experience = experience_score(candidate)
behavior = behavioral_score(candidate)

final_score = (
    0.55 * semantic +
    0.20 * experience +
    0.25 * behavior
)

results.append({
    "candidate_id": candidate["candidate_id"],
    "name": candidate["profile"]["anonymized_name"],
    "semantic": round(semantic, 3),
    "experience": round(experience, 3),
    "behavior": round(behavior, 3),
    "final_score": round(final_score, 3)
})


# Sort by similarity
results = sorted(
    results,
    key=lambda x: x["final_score"],
    reverse=True
)

print("\nTop 10 Candidates\n")

for i, r in enumerate(results[:10], start=1):
    print(f"\nRank #{i}")
    print(f"Candidate : {r['name']}")
    print(f"ID        : {r['candidate_id']}")
    print(f"Semantic  : {r['semantic']}")
    print(f"Experience: {r['experience']}")
    print(f"Behavior  : {r['behavior']}")
    print(f"Final     : {r['final_score']}")