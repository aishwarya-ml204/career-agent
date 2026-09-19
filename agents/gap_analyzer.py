# ============================================================
# SKILL GAP ANALYZER
# ============================================================

import re


def normalize_skill(skill):
    """Normalize skill names for reliable matching."""

    if skill is None:
        return ""

    skill = str(skill).lower().strip()

    # Remove list-like brackets and quotes
    skill = skill.replace("[", "")
    skill = skill.replace("]", "")
    skill = skill.replace("'", "")
    skill = skill.replace('"', "")

    replacements = {
        "ml": "machine learning",
        "machine-learning": "machine learning",
        "powerbi": "power bi",
        "nodejs": "node.js",
        "node": "node.js",
        "js": "javascript",
        "py": "python",
        "python3": "python",
        "pandas library": "pandas",
        "numpy library": "numpy",
        "scikit learn": "scikit-learn",
        "sklearn": "scikit-learn",
        "pytorch or tensorflow": "deep learning",
        "basic deep learning": "deep learning",
        "vector databases": "vector database",
        "vector databases (pinecone/faiss)": "vector database",
        "sql database": "sql",
        "mysql database": "mysql",
        "postgres": "postgresql",
        "postgres sql": "postgresql",
    }

    skill = skill.strip()

    return replacements.get(skill, skill)


def clean_skill(skill):
    """Clean an individual skill."""

    if skill is None:
        return ""

    return normalize_skill(skill)


def flatten_skills(skills):
    """Convert different skill formats into a clean list."""

    if skills is None:
        return []

    # Already a list
    if isinstance(skills, list):

        result = []

        for skill in skills:

            # Nested list
            if isinstance(skill, list):
                result.extend(flatten_skills(skill))

            else:
                cleaned = clean_skill(skill)

                if cleaned:
                    result.append(cleaned)

        return result

    # String
    if isinstance(skills, str):

        # Handle comma / semicolon / pipe separated skills
        parts = re.split(r"[,;|\n]+", skills)

        result = []

        for part in parts:

            cleaned = clean_skill(part)

            if cleaned:
                result.append(cleaned)

        return result

    return []


def split_skills(skill_text):
    """Split a skill string into individual skills."""

    if not skill_text:
        return []

    return flatten_skills(skill_text)


def normalize_for_matching(skill):
    """Normalize skill for comparison."""

    return normalize_skill(skill)


def analyze_gap(
    user_skills,
    required_skills
):
    # ========================================================
    # PREPARE SKILLS
    # ========================================================

    user_list = flatten_skills(user_skills)

    required_list = flatten_skills(required_skills)

    # ========================================================
    # NORMALIZE
    # ========================================================

    user_normalized = {
        normalize_for_matching(skill)
        for skill in user_list
        if skill
    }

    # ========================================================
    # MATCH SKILLS
    # ========================================================

    matched_skills = []

    missing_skills = []

    for original_skill in required_list:

        normalized = normalize_for_matching(
            original_skill
        )

        if not normalized:
            continue

        # ----------------------------------------------------
        # Exact match
        # ----------------------------------------------------

        if normalized in user_normalized:

            matched_skills.append(
                original_skill
            )

            continue

        # ----------------------------------------------------
        # Partial / related match
        # ----------------------------------------------------

        partial_match = False

        for user_skill in user_normalized:

            if (
                normalized in user_skill
                or user_skill in normalized
            ):

                partial_match = True

                break

        if partial_match:

            matched_skills.append(
                original_skill
            )

        else:

            missing_skills.append(
                original_skill
            )

    # ========================================================
    # REMOVE DUPLICATES
    # ========================================================

    matched_skills = list(
        dict.fromkeys(
            matched_skills
        )
    )

    missing_skills = list(
        dict.fromkeys(
            missing_skills
        )
    )

    # ========================================================
    # GAP PERCENTAGE
    # ========================================================

    total_required = (
        len(matched_skills)
        + len(missing_skills)
    )

    if total_required == 0:

        gap_percentage = 0

    else:

        gap_percentage = (
            len(missing_skills)
            / total_required
        ) * 100

    # ========================================================
    # RETURN
    # ========================================================

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "gap_percentage": round(
            gap_percentage,
            1
        )
    }