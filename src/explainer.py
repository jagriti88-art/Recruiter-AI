def generate_reason(candidate):

    reasons = []

    if candidate["semantic"] > 0.75:
        reasons.append("Strong semantic match with the job description.")

    if candidate["rule"] > 0.70:
        reasons.append("Relevant experience and technical skills align well.")

    if candidate["behavior"] > 0.70:
        reasons.append("High recruiter engagement and strong hiring signals.")

    if candidate["experience"] >= 5:
        reasons.append(
            f"{candidate['experience']} years of professional experience."
        )

    if len(candidate["skills"]) >= 5:
        reasons.append(
            "Possesses a diverse technical skill set."
        )

    if not reasons:
        reasons.append(
            "Overall profile demonstrates good potential for the role."
        )

    return " ".join(reasons)