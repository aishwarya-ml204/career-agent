import re


def normalize_skill(skill):
    skill = skill.lower().strip()

    replacements = {
        "ml": "machine learning",
        "machine-learning": "machine learning",
        "powerbi": "power bi",
        "nodejs": "node.js",
        "js": "javascript",
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

    user_skills = {
        normalize_skill(skill)
        for skill in user_skills
    }

    required_skills = extract_skills(required_skills)

    matched = []
    missing = []

    for skill in required_skills:

        if skill in user_skills:
            matched.append(skill)
        else:
            missing.append(skill)

    total = len(required_skills)

    gap_percentage = (
        len(missing) / total * 100
        if total > 0
        else 0
    )

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "total_required": total,
        "gap_percentage": round(gap_percentage, 2)
    }


if __name__ == "__main__":

    user_skills = [
        "Python",
        "SQL",
        "Pandas",
        "NumPy"
    ]

    required = """
    Python, Scikit-learn, Pandas, NumPy,
    Statistics, SQL, Basic Deep Learning
    """

    result = analyze_gap(
        user_skills,
        required
    )

    print("\nSkill Gap Analysis")
    print("------------------")

    print("Matched skills:")
    for skill in result["matched_skills"]:
        print("  ✓", skill)

    print("\nMissing skills:")
    for skill in result["missing_skills"]:
        print("  ✗", skill)

    print("\nGap:", result["gap_percentage"], "%")