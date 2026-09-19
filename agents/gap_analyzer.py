import re


def normalize_skill(skill):
    skill = str(skill).lower().strip()

    replacements = {
        "ml": "machine learning",
        "machine-learning": "machine learning",
        "powerbi": "power bi",
        "nodejs": "node.js",
        "js": "javascript",
        "py": "python",
        "scikit learn": "scikit-learn",
        "pytorch or tensorflow": "deep learning",
        "basic deep learning": "deep learning",
        "vector databases": "vector database",
        "vector databases (pinecone/faiss)": "vector database",
    }

    return replacements.get(skill, skill)


def split_skills(skill_text):
    if not skill_text:
        return []

    text = str(skill_text)

    # Split on commas only when the comma is OUTSIDE parentheses.
    skills = re.split(
        r",(?=(?:[^()]*\([^()]*\))*[^()]*$)|[;|\n]+",
        text
    )

    return [
        normalize_skill(skill)
        for skill in skills
        if skill.strip()
    ]


def analyze_gap(user_skills, required_skills):

    user_skills_normalized = {
        normalize_skill(skill)
        for skill in user_skills
    }

    required = split_skills(required_skills)

    matched_skills = []
    missing_skills = []

    for skill in required:

        normalized = normalize_skill(skill)

        if normalized in user_skills_normalized:
            matched_skills.append(normalized)
        else:
            missing_skills.append(normalized)

    total_required = len(required)

    if total_required == 0:
        gap_percentage = 0
    else:
        gap_percentage = round(
            (len(missing_skills) / total_required) * 100,
            2
        )

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "gap_percentage": gap_percentage
    }