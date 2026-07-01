KEYWORDS = {

    "retrieval": 3,
    "ranking": 3,
    "recommendation": 3,
    "recommend": 2,

    "search": 2,
    "vector": 3,
    "embedding": 3,
    "embeddings": 3,

    "faiss": 4,
    "pinecone": 4,
    "qdrant": 4,
    "milvus": 4,
    "weaviate": 4,

    "rag": 4,
    "llm": 2,
    "transformer": 2,
    "sentence transformer": 3,

    "semantic search": 4,
    "hybrid search": 4,

    "recommendation engine": 5,

    "ndcg": 2,
    "mrr": 2,
    "map": 2,

    "a/b": 2,
    "offline evaluation": 2
}


def experience_score(candidate):

    history = candidate.get("career_history", [])

    score = 0

    for job in history:

        text = (
            job.get("title", "") + " " +
            job.get("description", "")
        ).lower()

        for word, weight in KEYWORDS.items():

            if word in text:
                score += weight

    return min(score, 30)