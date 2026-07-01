from datetime import datetime

CURRENT_YEAR = datetime.now().year

SERVICE_COMPANIES = {
    "tcs",
    "infosys",
    "wipro",
    "cognizant",
    "capgemini",
    "accenture",
    "hcl"
}


def honeypot_penalty(candidate):

    penalty = 0

    profile = candidate["profile"]

    experience = profile.get("years_of_experience", 0)

    skills = candidate.get("skills", [])

    career = candidate.get("career_history", [])

    # --------------------------
    # Too many skills
    # --------------------------

    if len(skills) > 40:
        penalty += 4

    # --------------------------
    # Unrealistic experience
    # --------------------------

    if experience > 25:
        penalty += 5

    # --------------------------
    # Too many jobs
    # --------------------------

    if len(career) > 12:
        penalty += 2

    # --------------------------
    # Suspicious job durations
    # --------------------------

    total_years = 0

    for job in career:

        start = job.get("start_year")
        end = job.get("end_year")

        if start is None:
            continue

        if end is None:
            end = CURRENT_YEAR

        total_years += max(0, end - start)

    if total_years > experience + 5:
        penalty += 5

    # --------------------------
    # Entire career in service company
    # --------------------------

    companies = []

    for job in career:

        company = job.get("company", "").lower()

        companies.append(company)

    if companies:

        if all(
            any(sc in c for sc in SERVICE_COMPANIES)
            for c in companies
        ):
            penalty += 2

    return penalty