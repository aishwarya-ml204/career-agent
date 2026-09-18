import re


def parse_profile(profile_text: str) -> dict:

    known_skills = [
        "python", "java", "c++", "c", "sql", "mysql", "html", "css",
        "javascript", "react", "node.js", "django", "flask", "fastapi",
        "git", "github", "machine learning", "deep learning", "nlp",
        "tensorflow", "pytorch", "pandas", "numpy", "power bi",
        "tableau", "excel", "aws", "azure", "docker", "kubernetes"
    ]

    text = profile_text.lower()

    detected_skills = []

    for skill in known_skills:
        if re.search(r"\b" + re.escape(skill.lower()) + r"\b", text):
            detected_skills.append(skill)

    # Extract location
    location = None

    location_match = re.search(
        r"(?:live in|located in|based in|from)\s+([A-Za-z]+(?:,\s*[A-Za-z]+)?)",
        profile_text,
        re.IGNORECASE
    )

    if location_match:
        location = location_match.group(1).strip()

    return {
        "raw_profile": profile_text,
        "skills": detected_skills,
        "location": location
    }


if __name__ == "__main__":

    profile = """
    I am a B.Tech Computer Science student.
    I live in Bengaluru, Karnataka.
    I know Python, SQL, Pandas and NumPy.
    I am interested in machine learning and data science.
    """

    result = parse_profile(profile)

    print(result)