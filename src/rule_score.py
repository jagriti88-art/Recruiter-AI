def calculate_rule_score(candidate):

    score = 0

    profile = candidate["profile"]
    skills = candidate["skills"]
    history = candidate["career_history"]
    signals = candidate["redrob_signals"]

    # --------------------------
    # 1. Experience (20 points)
    # --------------------------

    exp = profile["years_of_experience"]

    if 5 <= exp <= 9:
        score += 20
    elif 4 <= exp < 5 or 9 < exp <= 10:
        score += 10

    # --------------------------
    # 2. Current Role (15 points)
    # --------------------------

    title = profile["current_title"].lower()

    good_titles = [
        "ai",
        "machine learning",
        "ml engineer",
        "data scientist",
        "nlp",
        "search",
        "recommendation",
        "backend engineer"
    ]

    for t in good_titles:
        if t in title:
            score += 15
            break

    # --------------------------
    # 3. Skills (30 points)
    # --------------------------

    important_skills = [
        "python",
        "faiss",
        "pinecone",
        "weaviate",
        "milvus",
        "qdrant",
        "sentence transformers",
        "embedding",
        "llm",
        "fine-tuning llms",
        "retrieval",
        "ranking",
        "spark",
        "airflow",
        "sql"
    ]

    candidate_skills = [
        s["name"].lower()
        for s in skills
    ]

    for skill in important_skills:

        for user_skill in candidate_skills:

            if skill in user_skill:
                score += 2
                break

    # --------------------------
    # 4. Career History (20 points)
    # --------------------------

    keywords = [
        "retrieval",
        "ranking",
        "recommendation",
        "embedding",
        "vector",
        "llm",
        "search",
        "machine learning",
        "production",
        "faiss"
    ]

    for job in history:

        description = job["description"].lower()

        for word in keywords:

            if word in description:
                score += 2

    # --------------------------
    # 5. Open To Work (5 points)
    # --------------------------

    if signals["open_to_work_flag"]:
        score += 5

    # --------------------------
    # 6. Notice Period (5 points)
    # --------------------------

    if signals["notice_period_days"] <= 30:
        score += 5

    elif signals["notice_period_days"] <= 60:
        score += 3

    return min(score, 100)