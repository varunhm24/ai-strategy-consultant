from strategy.opportunity_engine import find_opportunities


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


results = find_opportunities(
    business_profile
)


print(results)