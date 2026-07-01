import re

IMPORTANT_SKILLS = [
    "python",
    "embeddings",
    "retrieval",
    "ranking",
    "sentence-transformers",
    "faiss",
    "pinecone",
    "weaviate",
    "qdrant",
    "milvus",
    "elasticsearch",
    "opensearch",
    "llm",
    "rag",
    "lora",
    "qlora",
    "peft",
    "ndcg",
    "map",
    "mrr",
    "a/b testing",
    "fine tuning",
    "recommendation"
]

IMPORTANT_LOCATIONS = [
    "noida",
    "pune",
    "hyderabad",
    "mumbai",
    "delhi"
]


def extract_jd_features(jd_text):

    text = jd_text.lower()

    features = {}

    # --------------------------
    # Experience
    # --------------------------

    match = re.search(r"(\d+)\s*[-–]\s*(\d+)\s*years", text)

    if match:
        features["min_exp"] = int(match.group(1))
        features["max_exp"] = int(match.group(2))
    else:
        features["min_exp"] = 0
        features["max_exp"] = 100

    # --------------------------
    # Skills
    # --------------------------

    features["skills"] = []

    for skill in IMPORTANT_SKILLS:

        if skill in text:

            features["skills"].append(skill)

    # --------------------------
    # Preferred Locations
    # --------------------------

    features["locations"] = []

    for city in IMPORTANT_LOCATIONS:

        if city in text:

            features["locations"].append(city)

    return features