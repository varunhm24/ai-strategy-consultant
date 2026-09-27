# ============================================================
# DYNAMIC AI COST & ROI ENGINE
# ============================================================

import pandas as pd


# ------------------------------------------------------------
# BASE COST BY AI USE CASE
# ------------------------------------------------------------

BASE_COSTS = {

    "Sales Analytics": 75000,

    "Marketing Automation": 150000,

    "Customer Support AI": 250000,

    "Demand Forecasting": 300000,

    "Inventory Optimization": 300000,

    "Customer Churn Prediction": 250000,

    "Recommendation System": 500000,

    "Fraud Detection": 500000,
    
    # AI Agent Costs
    "AI Customer Service Agent": 300000,

    "AI Sales Agent": 500000,

    "AI Marketing Agent": 300000,

    "AI Inventory Agent": 400000
}


# ------------------------------------------------------------
# BASE BENEFIT PERCENTAGE
# ------------------------------------------------------------

BENEFIT_RATES = {

    "Sales Analytics": 0.05,

    "Marketing Automation": 0.08,

    "Customer Support AI": 0.10,

    "Demand Forecasting": 0.10,

    "Inventory Optimization": 0.10,

    "Customer Churn Prediction": 0.12,

    "Recommendation System": 0.15,

    "Fraud Detection": 0.12,
    
     # AI Agent Benefit Rates
    "AI Customer Service Agent": 0.12,

    "AI Sales Agent": 0.15,

    "AI Marketing Agent": 0.10,

    "AI Inventory Agent": 0.12
}


# ------------------------------------------------------------
# DEFAULT VALUES
# ------------------------------------------------------------

DEFAULT_COST = 200000

DEFAULT_BENEFIT_RATE = 0.08


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
        implementation_cost
        / monthly_benefit
    )

    return round(payback_months, 1)


# ------------------------------------------------------------
# ESTIMATE BUSINESS SCALE
# ------------------------------------------------------------

def calculate_business_scale(
    employees,
    monthly_customers,
    monthly_transactions
):

    employee_factor = max(
        employees / 50,
        1
    )

    customer_factor = max(
        monthly_customers / 1000,
        1
    )

    transaction_factor = max(
        monthly_transactions / 1000,
        1
    )

    scale_factor = (
        employee_factor * 0.3
        + customer_factor * 0.3
        + transaction_factor * 0.4
    )

    return round(
        scale_factor,
        2
    )


# ------------------------------------------------------------
# ESTIMATE IMPLEMENTATION COST
# ------------------------------------------------------------

def estimate_implementation_cost(
    use_case,
    scale_factor
):

    base_cost = BASE_COSTS.get(
        use_case,
        DEFAULT_COST
    )

    estimated_cost = (
        base_cost * scale_factor
    )

    return round(
        estimated_cost,
        -3
    )


# ------------------------------------------------------------
# ESTIMATE ANNUAL BENEFIT
# ------------------------------------------------------------

def estimate_annual_benefit(
    use_case,
    monthly_revenue
):

    benefit_rate = BENEFIT_RATES.get(
        use_case,
        DEFAULT_BENEFIT_RATE
    )

    # Convert monthly revenue to annual revenue

    annual_revenue = (
        monthly_revenue * 12
    )

    # Estimate annual business benefit

    annual_benefit = (
        annual_revenue
        * benefit_rate
    )

    return round(
        max(annual_benefit, 100000),
        -3
    )
   


# ------------------------------------------------------------
# CHECK BUDGET COMPATIBILITY
# ------------------------------------------------------------

def get_budget_limit(budget):

    if budget == "Less than ₹50,000":
        return 50000

    if budget == "₹50,000 – ₹2 Lakhs":
        return 200000

    if budget == "₹2 Lakhs – ₹5 Lakhs":
        return 500000

    if budget == "₹5 Lakhs – ₹10 Lakhs":
        return 1000000

    if budget == "More than ₹10 Lakhs":
        return float("inf")

    return None


# ------------------------------------------------------------
# CREATE DYNAMIC ROI ANALYSIS
# ------------------------------------------------------------

def create_roi_analysis(
    scored_opportunities,
    business_profile
):

    roi_analysis = []

    employees = int(
        business_profile.get(
            "employees",
            50
        )
    )

    monthly_customers = int(
        business_profile.get(
            "monthly_customers",
            1000
        )
    )

    monthly_transactions = int(
        business_profile.get(
            "monthly_transactions",
            1000
        )
    )

    monthly_revenue = float(
    business_profile.get(
        "monthly_revenue",
        100000
        )
    )

    budget = business_profile.get(
        "budget",
        "Not decided"
    )

    scale_factor = calculate_business_scale(
        employees,
        monthly_customers,
        monthly_transactions
    )

    budget_limit = get_budget_limit(
        budget
    )

    for _, row in scored_opportunities.iterrows():

        use_case = str(
            row.get(
                "use_case",
                ""
            )
        )

        technology = str(
            row.get(
                "technology",
                ""
            )
        )

        priority = str(
            row.get(
                "priority",
                ""
            )
        )

        score = float(
            row.get(
                "score",
                0
            )
        )

        # --------------------------------------------
        # COST
        # --------------------------------------------

        implementation_cost = (
            estimate_implementation_cost(
                use_case,
                scale_factor
            )
        )

        # --------------------------------------------
        # BENEFIT
        # --------------------------------------------

        annual_benefit = (
            estimate_annual_benefit(
                use_case,
                monthly_revenue
            )
        )
        # --------------------------------------------
        # ROI
        # --------------------------------------------

        roi = calculate_roi(
            implementation_cost,
            annual_benefit
        )

        # --------------------------------------------
        # PAYBACK
        # --------------------------------------------

        payback = calculate_payback(
            implementation_cost,
            annual_benefit
        )

        # --------------------------------------------
        # BUDGET STATUS
        # --------------------------------------------

        if budget_limit is None:
            budget_status = "Budget not decided"
            budget_gap = 0

        elif implementation_cost <= budget_limit:

            budget_status = "Within Budget"
            budget_gap = 0

        else:

            budget_status = "Above Budget"
            budget_gap = implementation_cost - budget_limit
            budget_gap = 0

        roi_analysis.append({
            "use_case": use_case,
            "technology": technology,
            "priority": priority,
            "score": score,
            "implementation_cost": implementation_cost,
            "annual_benefit": annual_benefit,
            "roi_percent": roi,
            "payback_months": payback,
            "budget_status": budget_status,
            "budget_gap": budget_gap
        })

    return pd.DataFrame(
        roi_analysis
    )