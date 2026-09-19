# ============================================================
# SKILL GAP ANALYZER
# ============================================================


def clean_skill(skill):

    if skill is None:
        return ""

    skill = str(skill).strip().lower()

    # Remove list-like brackets and quotes
    skill = skill.replace("[", "")
    skill = skill.replace("]", "")
    skill = skill.replace("'", "")
    skill = skill.replace('"', "")

    return skill.strip()


def flatten_skills(skills):

    if skills is None:
        return []

    # --------------------------------------------------------
    # If already a list
    # --------------------------------------------------------

    if isinstance(skills, list):

        result = []

        for skill in skills:

            # Nested list
            if isinstance(skill, list):

                result.extend(
                    flatten_skills(skill)
                )

            else:

                cleaned = clean_skill(skill)

                if cleaned:
                    result.append(cleaned)

        return result


    # --------------------------------------------------------
    # If string
    # --------------------------------------------------------

    if isinstance(skills, str):

        # Handle strings such as:
        # "Python, SQL, Pandas"

        skills = skills.replace(
            ";",
            ","
        )

        parts = skills.split(",")

        result = []

        for part in parts:

            cleaned = clean_skill(part)

            if cleaned:
                result.append(cleaned)

        return result


    return []


def normalize_for_matching(skill):

    skill = clean_skill(skill)

    # Common equivalent names
    aliases = {

        "py": "python",

        "python3": "python",

        "pandas library": "pandas",

        "numpy library": "numpy",

        "scikit learn": "scikit-learn",

        "sklearn": "scikit-learn",

        "js": "javascript",

        "node": "node.js",

        "nodejs": "node.js",

        "sql database": "sql",

        "mysql database": "mysql",

        "postgres": "postgresql",

        "postgres sql": "postgresql"
    }

    return aliases.get(
        skill,
        skill
    )


def analyze_gap(
    user_skills,
    required_skills
):

    # ========================================================
    # PREPARE SKILLS
    # ========================================================

    user_list = flatten_skills(
        user_skills
    )

    required_list = flatten_skills(
        required_skills
    )


    # ========================================================
    # NORMALIZE
    # ========================================================

    user_normalized = {
        normalize_for_matching(skill)
        for skill in user_list
        if skill
    }

    required_normalized = {
        normalize_for_matching(skill)
        for skill in required_list
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
        #
        # Example:
        # user = "machine learning"
        # required = "machine learning algorithms"
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

    total_required = len(
        matched_skills
    ) + len(
        missing_skills
    )


    if total_required == 0:

        gap_percentage = 0

    else:

        gap_percentage = (
            len(missing_skills)
            /
            total_required
        ) * 100


    # ========================================================
    # RETURN
    # ========================================================

    return {

        "matched_skills":
            matched_skills,

        "missing_skills":
            missing_skills,

        "gap_percentage":
            round(
                gap_percentage,
                1
            )
    }