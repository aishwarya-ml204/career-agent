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
    }

    return replacements.get(skill, skill)


def extract_skills(skill_text):
    if not skill_text:
        return []

    skills = re.split(r"[,;|/\n]+", str(skill_text))

    return [
        normalize_skill(skill)
        for skill in skills
        if skill.strip()
    ]


def analyze_gap(user_skills, required_skills):

    # Normalize user's skills
    user_skills = {
        normalize_skill(skill)
        for skill in user_skills
    }

    # Extract and normalize required skills
    required_skills = extract_skills(required_skills)

    matched_skills = []
    missing_skills = []

    for skill in required_skills:

        if skill in user_skills:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    total_required = len(required_skills)

    if total_required > 0:
        gap_percentage = (
            len(missing_skills) / total_required
        ) * 100
    else:
        gap_percentage = 0

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "total_required": total_required,
        "gap_percentage": round(gap_percentage, 2)
    }


if __name__ == "__main__":

    user_skills = [
        "Python",
        "SQL",
        "Pandas",
        "NumPy"
    ]

    required_skills = """
    Python, Scikit-learn, Pandas, NumPy,
    Statistics, SQL, Basic Deep Learning
    """

    result = analyze_gap(
        user_skills,
        required_skills
    )

    print("\n========== SKILL GAP ANALYSIS ==========")

    print("\nMatched Skills:")
    for skill in result["matched_skills"]:
        print("  ✓", skill)

    print("\nMissing Skills:")
    for skill in result["missing_skills"]:
        print("  ✗", skill)

    print("\nTotal Required:", result["total_required"])
    print("Gap:", result["gap_percentage"], "%")