import pandas as pd


# ---------------------------------------------------------
# LOAD AI USE CASE DATABASE
# ---------------------------------------------------------

def load_use_cases():

    file_path = "data/ai_use_cases.csv"

    df = pd.read_csv(file_path)

    return df


# ---------------------------------------------------------
# BUSINESS GOAL → AI OPPORTUNITY KEYWORDS
# ---------------------------------------------------------

GOAL_KEYWORDS = {

    "Reduce Costs": [
        "analytics",
        "automation",
        "inventory",
        "customer support",
        "fraud",
        "churn",
        "forecasting",
        "optimization"
    ],

    "Increase Revenue": [
        "sales",
        "marketing",
        "recommendation",
        "customer",
        "forecasting"
    ],

    "Improve Customer Experience": [
        "customer support",
        "recommendation",
        "customer",
        "chatbot",
        "agent"
    ],

    "Automate Operations": [
        "automation",
        "document",
        "inventory",
        "operations",
        "support",
        "agent"
    ],

    "Improve Decision Making": [
        "analytics",
        "forecasting",
        "prediction",
        "sales",
        "data"
    ]
}


# ---------------------------------------------------------
# FIND OPPORTUNITIES
# ---------------------------------------------------------

def find_opportunities(business_profile):

    df = load_use_cases()

    industry = business_profile["industry"]

    business_problems = business_profile["business_problems"]

    available_data = business_profile["available_data"]

    business_goals = business_profile.get(
        "business_goals",
        []
    )

    # -----------------------------------------------------
    # FILTER BY INDUSTRY
    # -----------------------------------------------------

    industry_matches = df[
        df["industry"] == industry
    ].copy()

    opportunities = []

    # -----------------------------------------------------
    # CHECK EACH USE CASE
    # -----------------------------------------------------

    for _, row in industry_matches.iterrows():

        use_case = str(row["use_case"])

        required_data = str(
            row["required_data"]
        ).split(";")

        problem_match = False

        data_match = False

        goal_match = False
        
         # -------------------------------------------------
        # CHECK AI AGENT OPPORTUNITY
        # -------------------------------------------------

        agent_match = (
            "agent" in use_case.lower()
            or "agent" in str(row["technology"]).lower()
        )

        # -------------------------------------------------
        # CHECK BUSINESS PROBLEM
        # -------------------------------------------------

        for problem in business_problems:

            if problem.lower() in use_case.lower():

                problem_match = True

                break

        # -------------------------------------------------
        # CHECK REQUIRED DATA
        # -------------------------------------------------

        matching_data = []

        for data in required_data:

            data = data.strip()

            if data in available_data:

                matching_data.append(data)

        if len(matching_data) > 0:

            data_match = True

        # -------------------------------------------------
        # CHECK BUSINESS GOALS
        # -------------------------------------------------

        for goal in business_goals:

            keywords = GOAL_KEYWORDS.get(
                goal,
                []
            )

            for keyword in keywords:

                if keyword.lower() in use_case.lower():

                    goal_match = True

                    break

            if goal_match:

                break

        # -------------------------------------------------
        # ADD OPPORTUNITY
        # -------------------------------------------------

        if (
            problem_match
            or data_match
            or goal_match
            or agent_match
        ):

            opportunities.append({

                "use_case":
                    row["use_case"],

                "technology":
                    row["technology"],

                "required_data":
                    row["required_data"],

                "business_impact":
                    row["business_impact"],

                "implementation_difficulty":
                    row["implementation_difficulty"],

                "cost_level":
                    row["cost_level"],

                "description":
                    row["description"],

                "matching_data":
                    ", ".join(matching_data)

            })

    return pd.DataFrame(opportunities)