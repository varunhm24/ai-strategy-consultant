import pandas as pd


# ============================================================
# SCORE MAPPINGS
# ============================================================

IMPACT_SCORE = {
    "High": 5,
    "Medium": 3,
    "Low": 1
}


DIFFICULTY_SCORE = {
    "Low": 5,
    "Medium": 3,
    "High": 1
}


COST_SCORE = {
    "Low": 5,
    "Medium": 3,
    "High": 1
}


# ============================================================
# CALCULATE OPPORTUNITY SCORE
# ============================================================

def calculate_score(row):

    impact = IMPACT_SCORE.get(
        row["business_impact"],
        1
    )

    difficulty = DIFFICULTY_SCORE.get(
        row["implementation_difficulty"],
        1
    )

    cost = COST_SCORE.get(
        row["cost_level"],
        1
    )

    # Data availability
    if row["matching_data"].strip():

        data_score = 5

    else:

        data_score = 1

    # Weighted score
    score = (
        impact * 0.35
        + difficulty * 0.25
        + cost * 0.20
        + data_score * 0.20
    )

    return round(score, 2)


# ============================================================
# PRIORITY CLASSIFICATION
# ============================================================

def get_priority(score):

    if score >= 4.5:

        return "Very High"

    elif score >= 3.5:

        return "High"

    elif score >= 2.5:

        return "Medium"

    else:

        return "Low"


# ============================================================
# SCORE OPPORTUNITIES
# ============================================================

def score_opportunities(opportunities):

    if opportunities.empty:

        return opportunities

    scored = opportunities.copy()

    scored["score"] = scored.apply(
        calculate_score,
        axis=1
    )

    scored["priority"] = scored["score"].apply(
        get_priority
    )

    # Sort highest score first
    scored = scored.sort_values(
        by="score",
        ascending=False
    )

    return scored