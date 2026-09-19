import re


def normalize_skill(skill):
    """Convert a skill to a standard format."""
    return skill.strip().lower()


def extract_skills(skill_text):
    """Convert a skill string into a set of individual skills."""

    if not skill_text:
        return set()

    # Handle common separators
    skills = re.split(r"[,;|]", str(skill_text))

    return {
        normalize_skill(skill)
        for skill in skills
        if skill.strip()
    }


def find_skill_gap(user_skills, required_skills):
    """
    Compare user skills with the skills required by a job.
    """

    user = extract_skills(user_skills)
    required = extract_skills(required_skills)

    matched_skills = user.intersection(required)
    missing_skills = required - user

    return {
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills),
    }


if __name__ == "__main__":

    user_skills = "Python, SQL, Machine Learning"

    required_skills = (
        "Python, SQL, Machine Learning, TensorFlow, Docker"
    )

    result = find_skill_gap(user_skills, required_skills)

    print("\n--- SKILL GAP ANALYSIS ---")

    print("Matched Skills:")
    for skill in result["matched_skills"]:
        print("-", skill)

    print("\nMissing Skills:")
    for skill in result["missing_skills"]:
        print("-", skill)