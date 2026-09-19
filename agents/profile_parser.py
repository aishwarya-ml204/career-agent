import re


def parse_profile(profile_text: str) -> dict:

    known_skills = [
        "python",
        "java",
        "c++",
        "c",
        "sql",
        "mysql",
        "javascript",
        "html",
        "css",
        "react",
        "node.js",
        "django",
        "flask",
        "fastapi",
        "machine learning",
        "deep learning",
        "nlp",
        "natural language processing",
        "computer vision",
        "large language models",
        "llm",
        "generative ai",
        "tensorflow",
        "pytorch",
        "scikit-learn",
        "huggingface",
        "langchain",
        "pandas",
        "numpy",
        "power bi",
        "tableau",
        "excel",
        "mongodb",
        "rag",
        "retrieval-augmented generation",
        "prompt engineering",
        "ai agents",
        "vector databases",
        "faiss",
        "aws",
        "azure",
        "docker",
        "kubernetes",
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

        pattern = (
            r"(?<![a-zA-Z0-9])"
            + re.escape(skill.lower())
            + r"(?![a-zA-Z0-9])"
        )

        if re.search(pattern, text):
            detected_skills.append(skill)

    detected_skills = list(dict.fromkeys(detected_skills))

    # --------------------------------------------------
    # Detect location
    # --------------------------------------------------

    location = None

    # Example:
    # Bengaluru, India
    # Bengaluru, Karnataka
    location_match = re.search(
        r"\b("
        r"Bengaluru|Bangalore|Mumbai|Bombay|"
        r"Delhi|Hyderabad|Chennai|Pune|"
        r"Gurgaon|Gurugram|Noida|Kolkata"
        r")"
        r"(?:,\s*[A-Za-z]+)?"
        r"\b",
        profile_text,
        re.IGNORECASE
    )

    if location_match:
        location = location_match.group(0).strip()

    # --------------------------------------------------
    # Detect explicit location statements
    # --------------------------------------------------

    if not location:

        location_match = re.search(
            r"(?:live in|located in|based in|from)"
            r"\s+([A-Za-z]+(?:,\s*[A-Za-z]+)?)",
            profile_text,
            re.IGNORECASE
        )

        if location_match:
            location = location_match.group(1).strip()

    # --------------------------------------------------
    # Detect preferred job location
    # --------------------------------------------------

    if not location:

        location_match = re.search(
            r"Preferred Job Location:\s*"
            r"([A-Za-z]+(?:,\s*[A-Za-z]+)?)",
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