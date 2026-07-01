SERVICE_COMPANIES = {
    "tcs",
    "infosys",
    "wipro",
    "cognizant",
    "accenture",
    "capgemini",
    "hcl",
    "tech mahindra"
}

PRODUCT_COMPANIES = {
    "google",
    "microsoft",
    "amazon",
    "flipkart",
    "swiggy",
    "zomato",
    "razorpay",
    "paytm",
    "phonepe",
    "cred",
    "meesho",
    "ola",
    "uber",
    "redrob",
    "atlassian",
    "freshworks",
    "oracle",
    "adobe",
    "salesforce",
    "linkedin",
    "netflix"
}


def company_score(candidate):

    history = candidate.get("career_history", [])

    score = 0

    for job in history:

        company = job.get("company", "").lower()

        # Product company bonus
        if any(prod in company for prod in PRODUCT_COMPANIES):
            score += 8

        # Service company penalty
        elif any(serv in company for serv in SERVICE_COMPANIES):
            score -= 4

    return max(min(score, 20), -20)