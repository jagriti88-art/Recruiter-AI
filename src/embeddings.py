from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

text = """
Backend Engineer with 6.9 years experience.
Skills: Python, SQL, Spark, NLP
"""

embedding = model.encode(text)

print("Embedding dimension:", len(embedding))
print("First 10 values:")
print(embedding[:10])