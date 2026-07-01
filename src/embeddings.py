def generate_reason(candidate, jd_text=""):

    reasons = []

    # ----------------------------------
    # Experience
    # ----------------------------------

    exp = candidate.get("experience", 0)

    if exp >= 6:
        reasons.append(f"{exp} years of relevant experience")

    elif exp >= 4:
        reasons.append(f"{exp} years of industry experience")

    # ----------------------------------
    # Semantic Match
    # ----------------------------------

    semantic = candidate.get("semantic", 0)

    if semantic >= 0.85:
        reasons.append("excellent semantic match with the JD")

    elif semantic >= 0.70:
        reasons.append("strong semantic similarity to the JD")

    # ----------------------------------
    # Skills
    # ----------------------------------

    skills = [s.lower() for s in candidate.get("skills", [])]

    important = [
        "python",
        "faiss",
        "embedding",
        "embeddings",
        "retrieval",
        "ranking",
        "machine learning",
        "deep learning",
        "llm",
        "rag",
        "transformers"
    ]

    matched = []

    for skill in important:

        if skill in skills:

            matched.append(skill)

    if matched:

        reasons.append(
            "skills include " + ", ".join(matched[:4])
        )

    # ----------------------------------
    # Company
    # ----------------------------------

    company = candidate.get("company", "")

    if company:

        reasons.append(
            f"currently working at {company}"
        )

    # ----------------------------------
    # Behavior
    # ----------------------------------

    behavior = candidate.get("behavior", 0)

    if behavior > 0.75:

        reasons.append(
            "high recruiter engagement signals"
        )

    # ----------------------------------
    # Weakness
    # ----------------------------------

    weaknesses = []

    if semantic < 0.60:

        weaknesses.append(
            "moderate semantic alignment"
        )

    if exp < 5:

        weaknesses.append(
            "slightly below preferred experience range"
        )

    # ----------------------------------
    # Final sentence
    # ----------------------------------

    text = ". ".join(reasons)

    if weaknesses:

        text += ". Minor concern: "

        text += ", ".join(weaknesses)

    return text + "."