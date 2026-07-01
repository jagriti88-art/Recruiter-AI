import os
import json
import pickle

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# -----------------------------------
# Create models directory
# -----------------------------------

os.makedirs("models", exist_ok=True)

# -----------------------------------
# Load Model
# -----------------------------------

print("Loading Sentence Transformer...")

model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------------
# Read Candidates (JSONL)
# -----------------------------------

print("Reading candidates...")

candidates = []

with open("data/candidates.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            candidates.append(json.loads(line))

print(f"Loaded {len(candidates)} candidates.")

# -----------------------------------
# Convert Candidate -> Text
# -----------------------------------

def candidate_to_text(candidate):

    profile = candidate["profile"]

    text = f"""
Headline: {profile.get('headline', '')}
Current Title: {profile.get('current_title', '')}
Experience: {profile.get('years_of_experience', 0)} years

Summary:
{profile.get('summary', '')}

Skills:
"""

    text += ", ".join(
        skill.get("name", "")
        for skill in candidate.get("skills", [])
    )

    text += "\n\nCareer History:\n"

    for job in candidate.get("career_history", []):

        text += f"""
Title: {job.get('title', '')}
Company: {job.get('company', '')}

Description:
{job.get('description', '')}
"""

    return text

# -----------------------------------
# Generate Embeddings
# -----------------------------------

print("Creating embeddings...")

texts = [candidate_to_text(c) for c in candidates]

embeddings = model.encode(
    texts,
    convert_to_numpy=True,
    show_progress_bar=True,
    batch_size=32
)

embeddings = embeddings.astype("float32")

# -----------------------------------
# Build FAISS Index
# -----------------------------------

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

# -----------------------------------
# Save FAISS Index
# -----------------------------------

faiss.write_index(
    index,
    "models/candidate_index.faiss"
)

print("FAISS index saved.")

# -----------------------------------
# Save Candidate Data
# -----------------------------------

with open("models/candidate_data.pkl", "wb") as f:
    pickle.dump(candidates, f)

print("Candidate data saved.")

# -----------------------------------
# Save Embeddings
# -----------------------------------

with open("models/candidate_embeddings.pkl", "wb") as f:
    pickle.dump(embeddings, f)

print("Candidate embeddings saved.")

np.save(
    "models/candidate_embeddings.npy",
    embeddings
)

print("Candidate embeddings (.npy) saved.")

print("\n✅ Recruiter AI database created successfully!")
print(f"Total candidates indexed: {len(candidates)}")