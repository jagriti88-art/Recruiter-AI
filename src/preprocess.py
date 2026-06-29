def candidate_to_text(candidate):

    profile = candidate["profile"]

    text = f"""
Headline: {profile['headline']}
Current Title: {profile['current_title']}
Experience: {profile['years_of_experience']} years

Summary:
{profile['summary']}
"""

    text += "\nSkills:\n"

    for skill in candidate["skills"]:
        text += f"{skill['name']} ({skill['proficiency']}), "

    text += "\n\nCareer History:\n"

    for job in candidate["career_history"]:
        text += f"""
Title: {job['title']}
Company: {job['company']}
Description:
{job['description']}
"""

    return text