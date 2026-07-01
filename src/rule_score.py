from src.jd_parser import extract_jd_features


def calculate_rule_score(candidate, jd_text):

    jd = extract_jd_features(jd_text)

    score = 0

    profile = candidate["profile"]

    candidate_skills = {
        skill["name"].lower()
        for skill in candidate["skills"]
    }

    # --------------------
    # Experience
    # --------------------

    exp = profile["years_of_experience"]

    if jd["min_exp"] <= exp <= jd["max_exp"]:
        score += 25

    elif abs(exp - jd["min_exp"]) <= 2:
        score += 18

    else:
        score += 8

    # --------------------
    # Skill Matching
    # --------------------

    matched = 0

    for skill in jd["skills"]:

        if skill in candidate_skills:

            matched += 1

    if len(jd["skills"]) > 0:

        score += (matched / len(jd["skills"])) * 40

    # --------------------
    # Preferred Location
    # --------------------

    location = profile["location"].lower()

    for city in jd["locations"]:

        if city in location:

            score += 10

            break

    # --------------------
    # Job Title Bonus
    # --------------------

    title = profile["current_title"].lower()

    important_titles = [
        "ai engineer",
        "ml engineer",
        "machine learning engineer",
        "software engineer",
        "research engineer",
        "data scientist"
    ]

    if any(t in title for t in important_titles):

        score += 15

    # --------------------
    # Summary contains ranking/search words
    # --------------------

    summary = profile["summary"].lower()

    keywords = [
        "retrieval",
        "ranking",
        "recommendation",
        "search",
        "embedding",
        "vector"
    ]

    count = sum(k in summary for k in keywords)

    score += min(count * 2, 10)

    return min(score, 100)