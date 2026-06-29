import faiss
import pickle
from sentence_transformers import SentenceTransformer
from read_jd import read_jd

print("Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Loading FAISS index...")
index = faiss.read_index("models/candidate_index.faiss")

print("Loading candidate data...")

with open("models/candidate_data.pkl", "rb") as f:
    candidates = pickle.load(f)

print("Reading JD...")

jd = read_jd()

print("Creating JD embedding...")

query_embedding = model.encode([jd])

print("Searching...")

distances, indices = index.search(query_embedding, 10)

print("\nTop Matching Candidates\n")

for rank, idx in enumerate(indices[0], start=1):

    candidate = candidates[idx]

    print(
        f"{rank}. "
        f"{candidate['profile']['anonymized_name']} "
        f"({candidate['candidate_id']})"
    )