import re


def parse_profile(profile_text: str) -> dict:

    # --------------------------------------------------
    # Known skills
    # --------------------------------------------------

    known_skills = [
        # Programming
        "python",
        "java",
        "c++",
        "c",
        "sql",
        "mysql",
        "javascript",

        # Web
        "html",
        "css",
        "react",
        "node.js",

        # Backend
        "django",
        "flask",
        "fastapi",

        # AI / ML
        "machine learning",
        "deep learning",
        "nlp",
        "natural language processing",
        "computer vision",
        "large language models",
        "llm",
        "generative ai",

        # Frameworks
        "tensorflow",
        "pytorch",
        "scikit-learn",
        "huggingface",
        "langchain",

        # Data
        "pandas",
        "numpy",
        "power bi",
        "tableau",
        "excel",

        # Databases
        "sql",
        "mysql",
        "mongodb",

        # AI systems
        "rag",
        "retrieval-augmented generation",
        "prompt engineering",
        "ai agents",
        "vector databases",
        "faiss",

        # Cloud / DevOps
        "aws",
        "azure",
        "docker",
        "kubernetes",

        # Tools
        "git",
        "github",
        "rest apis",
        "linux",
    ]

    text = profile_text.lower()

    # --------------------------------------------------
    # Detect skills
    # --------------------------------------------------

    detected_skills = []

    for skill in known_skills:

        # More flexible matching than \b because
        # skills such as C++, Node.js and RAG contain
        # punctuation/special characters.

        pattern = r"(?<![a-zA-Z0-9])" + re.escape(skill.lower()) + r"(?![a-zA-Z0-9])"

        if re.search(pattern, text):
            detected_skills.append(skill)

    # Remove duplicates while preserving order
    detected_skills = list(dict.fromkeys(detected_skills))

    # --------------------------------------------------
    # Extract location
    # --------------------------------------------------

    location = None

    # Pattern 1:
    # "I live in Bengaluru, Karnataka"
    location_match = re.search(
        r"(?:live in|located in|based in|from)\s+"
        r"([A-Za-z]+(?:,\s*[A-Za-z]+)?)",
        profile_text,
        re.IGNORECASE
    )

    if location_match:
        location = location_match.group(1).strip()

    # Pattern 2:
    # "Preferred Job Location: Bengaluru, Karnataka"
    if not location:

        location_match = re.search(
            r"Preferred Job Location:\s*"
            r"([A-Za-z]+(?:,\s*[A-Za-z]+)?)",
            profile_text,
            re.IGNORECASE
        )

        if location_match:
            location = location_match.group(1).strip()

    # Pattern 3:
    # Resume header:
    #
    # ARYAN NOVA
    # Bengaluru, India | email | phone
    #
    if not location:

        location_match = re.search(
            r"(?:^|\n)\s*"
            r"([A-Za-z]+(?:,\s*[A-Za-z]+)?)"
            r"\s*\|",
            profile_text,
            re.IGNORECASE
        )

        if location_match:
            location = location_match.group(1).strip()

    # --------------------------------------------------
    # Return structured profile
    # --------------------------------------------------

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