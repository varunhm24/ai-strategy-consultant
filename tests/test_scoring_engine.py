import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from strategy.opportunity_engine import find_opportunities
from strategy.scoring_engine import score_opportunities


# ============================================================
# BUSINESS PROFILE
# ============================================================

business_profile = {

    "company_name": "ABC Electronics",

    "industry": "E-commerce",

    "employees": 50,

    "business_model": "B2C",

    "monthly_customers": 20000,

    "monthly_transactions": 8000,

    "business_problems": [
        "Customer Support",
        "Inventory Management",
        "Demand Forecasting",
        "Marketing"
    ],

    "other_problem": "",

    "available_data": [
        "Customer Data",
        "Sales Data",
        "Inventory Data",
        "Marketing Data",
        "Support Tickets"
    ],

    "current_technology": [
        "Excel",
        "SQL Database"
    ],

    "budget": "₹2 Lakhs – ₹5 Lakhs",

    "business_goals": [
        "Reduce Costs",
        "Improve Customer Experience"
    ]
}


# ============================================================
# FIND OPPORTUNITIES
# ============================================================

opportunities = find_opportunities(
    business_profile
)


# ============================================================
# SCORE OPPORTUNITIES
# ============================================================

scored_opportunities = score_opportunities(
    opportunities
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\nAI OPPORTUNITY MATRIX")
print("=" * 80)

print(
    scored_opportunities[
        [
            "use_case",
            "technology",
            "business_impact",
            "implementation_difficulty",
            "cost_level",
            "score",
            "priority"
        ]
    ].to_string(index=False)
)