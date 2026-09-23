# ============================================================
# AI COST & ROI ENGINE
# ============================================================

import pandas as pd


# ------------------------------------------------------------
# DEFAULT COST ASSUMPTIONS
# ------------------------------------------------------------

ROI_PROFILES = {

    "Sales Analytics": {
        "implementation_cost": 75000,
        "annual_benefit": 300000
    },

    "Marketing Automation": {
        "implementation_cost": 150000,
        "annual_benefit": 450000
    },

    "Customer Support AI": {
        "implementation_cost": 250000,
        "annual_benefit": 600000
    },

    "Demand Forecasting": {
        "implementation_cost": 300000,
        "annual_benefit": 750000
    },

    "Inventory Optimization": {
        "implementation_cost": 300000,
        "annual_benefit": 700000
    },

    "Customer Churn Prediction": {
        "implementation_cost": 250000,
        "annual_benefit": 650000
    },

    "Recommendation System": {
        "implementation_cost": 500000,
        "annual_benefit": 1200000
    },

    "Fraud Detection": {
        "implementation_cost": 500000,
        "annual_benefit": 1000000
    }
}


# ------------------------------------------------------------
# DEFAULT PROFILE
# ------------------------------------------------------------

DEFAULT_PROFILE = {
    "implementation_cost": 200000,
    "annual_benefit": 500000
}


# ------------------------------------------------------------
# CALCULATE ROI
# ------------------------------------------------------------

def calculate_roi(
    implementation_cost,
    annual_benefit
):

    if implementation_cost <= 0:
        return 0

    roi = (
        (annual_benefit - implementation_cost)
        / implementation_cost
    ) * 100

    return round(roi, 2)


# ------------------------------------------------------------
# CALCULATE PAYBACK PERIOD
# ------------------------------------------------------------

def calculate_payback(
    implementation_cost,
    annual_benefit
):

    if annual_benefit <= 0:
        return None

    monthly_benefit = annual_benefit / 12

    payback_months = (
        implementation_cost / monthly_benefit
    )

    return round(payback_months, 1)


# ------------------------------------------------------------
# CREATE ROI ANALYSIS
# ------------------------------------------------------------

def create_roi_analysis(
    scored_opportunities
):

    roi_analysis = []

    for _, row in scored_opportunities.iterrows():

        use_case = str(
            row.get("use_case", "")
        )

        technology = str(
            row.get("technology", "")
        )

        priority = str(
            row.get("priority", "")
        )

        score = float(
            row.get("score", 0)
        )

        # Get predefined profile
        profile = ROI_PROFILES.get(
            use_case,
            DEFAULT_PROFILE
        )

        implementation_cost = profile[
            "implementation_cost"
        ]

        annual_benefit = profile[
            "annual_benefit"
        ]

        # Calculate ROI
        roi = calculate_roi(
            implementation_cost,
            annual_benefit
        )

        # Calculate payback
        payback = calculate_payback(
            implementation_cost,
            annual_benefit
        )

        roi_analysis.append({

            "use_case": use_case,

            "technology": technology,

            "priority": priority,

            "score": score,

            "implementation_cost":
                implementation_cost,

            "annual_benefit":
                annual_benefit,

            "roi_percent":
                roi,

            "payback_months":
                payback
        })

    return pd.DataFrame(
        roi_analysis
    )