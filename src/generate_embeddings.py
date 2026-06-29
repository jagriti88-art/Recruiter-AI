import json
from sentence_transformers import SentenceTransformer

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


# Load candidates
with open("data/sample_candidates.json", "r", encoding="utf-8") as f:
    candidates = json.load(f)

candidate_embeddings = []

for candidate in candidates:
    text = candidate_to_text(candidate)
    embedding = model.encode(text)

    candidate_embeddings.append({
        "candidate_id": candidate["candidate_id"],
        "embedding": embedding
    })

print("Total candidates:", len(candidate_embeddings))
print("Embedding size:", len(candidate_embeddings[0]["embedding"]))