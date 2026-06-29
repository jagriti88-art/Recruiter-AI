from datetime import datetime


def experience_score(candidate):

    years = candidate["profile"]["years_of_experience"]

    # JD wants 5–9 years
    if 5 <= years <= 9:
        return 1.0

    elif 4 <= years < 5:
        return 0.8

    elif 9 < years <= 11:
        return 0.8

    else:
        return 0.5


def behavioral_score(candidate):

    signals = candidate["redrob_signals"]

    score = 0

    # Open to work
    if signals["open_to_work_flag"]:
        score += 1

    # Recruiter response
    score += signals["recruiter_response_rate"]

    # Interview completion
    score += signals["interview_completion_rate"]

    # Github activity
    score += signals["github_activity_score"] / 10

    # Saved by recruiters
    score += min(signals["saved_by_recruiters_30d"] / 10, 1)

    return score / 5