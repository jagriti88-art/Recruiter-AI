import json
import numpy as np
import faiss
import os
import pickle
from sentence_transformers import SentenceTransformer
os.makedirs("models", exist_ok=True)

print("Loading model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Reading candidates...")

with open("data/sample_candidates.json", "r", encoding="utf-8") as f:
    candidates = json.load(f)


def candidate_to_text(candidate):

    profile = candidate["profile"]

    text = f"""
Headline: {profile['headline']}
Current Title: {profile['current_title']}
Experience: {profile['years_of_experience']}

Summary:
{profile['summary']}

Skills:
"""

    for skill in candidate["skills"]:
        text += skill["name"] + ", "

    text += "\nCareer History:\n"

    for job in candidate["career_history"]:
        text += job["description"] + "\n"

    return text


texts = [candidate_to_text(c) for c in candidates]

print("Creating embeddings...")

embeddings = model.encode(texts)

embeddings = np.array(embeddings).astype("float32")

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

faiss.write_index(index, "models/candidate_index.faiss")

print("Index Saved!")
# Save candidate data
with open("models/candidate_data.pkl", "wb") as f:
    pickle.dump(candidates, f)

print("Candidate data saved!")
np.save("models/candidate_embeddings.npy", embeddings)

print("Embeddings Saved!")