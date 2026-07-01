def analyze_jd(jd):

    jd = jd.lower()

    config = {

        "semantic": 0.40,
        "rule": 0.25,
        "behavior": 0.15,
        "company": 0.10,
        "experience": 0.10

    }

    # --------------------------------
    # Retrieval / Search
    # --------------------------------

    retrieval_words = [

        "retrieval",
        "ranking",
        "embedding",
        "vector",
        "faiss",
        "search",
        "recommendation",
        "matching"

    ]

    if any(word in jd for word in retrieval_words):

        config["semantic"] += 0.08

    # --------------------------------
    # Product company
    # --------------------------------

    if "product" in jd:

        config["company"] += 0.08

    # --------------------------------
    # Startup
    # --------------------------------

    startup_words = [

        "startup",
        "series a",
        "ship",
        "founding"

    ]

    if any(word in jd for word in startup_words):

        config["behavior"] += 0.05

    # --------------------------------
    # Leadership
    # --------------------------------

    leader_words = [

        "mentor",
        "lead",
        "architecture"

    ]

    if any(word in jd for word in leader_words):

        config["experience"] += 0.05

    # --------------------------------
    # Normalize
    # --------------------------------

    total = sum(config.values())

    for k in config:

        config[k] /= total

    return config