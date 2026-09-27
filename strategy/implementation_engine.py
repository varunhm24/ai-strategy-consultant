import pandas as pd


# ============================================================
# IMPLEMENTATION PLAN DATABASE
# ============================================================

IMPLEMENTATION_PLANS = {

    "Sales Analytics": {
        "timeline": "2–4 weeks",
        "estimated_cost": "Low",
        "team": "Data Analyst + Business User",
        "steps": [
            "Collect historical sales data",
            "Clean and prepare the data",
            "Identify important sales KPIs",
            "Build analytics dashboards",
            "Analyze sales trends and patterns",
            "Deploy dashboard for business users"
        ],
        "impact": "Improved sales visibility and faster business decisions"
    },

    "Marketing Automation": {
        "timeline": "3–6 weeks",
        "estimated_cost": "Medium",
        "team": "Marketing Specialist + AI Developer",
        "steps": [
            "Collect customer and marketing data",
            "Identify repetitive marketing activities",
            "Select suitable Generative AI tools",
            "Build automated content workflows",
            "Integrate with existing marketing platforms",
            "Monitor campaign performance"
        ],
        "impact": "Reduced marketing effort and faster campaign execution"
    },

    "Customer Support AI": {
        "timeline": "4–8 weeks",
        "estimated_cost": "Medium",
        "team": "AI Developer + Backend Developer + Support Team",
        "steps": [
            "Collect support documents and FAQs",
            "Clean and organize knowledge sources",
            "Create document embeddings",
            "Build RAG knowledge base",
            "Connect an LLM",
            "Develop customer support interface",
            "Test responses",
            "Deploy and monitor the system"
        ],
        "impact": "Faster customer responses and reduced support workload"
    },

    "Demand Forecasting": {
        "timeline": "6–10 weeks",
        "estimated_cost": "Medium",
        "team": "Data Scientist + Data Engineer + Business Analyst",
        "steps": [
            "Collect historical demand data",
            "Clean and preprocess the data",
            "Perform exploratory data analysis",
            "Create forecasting features",
            "Train forecasting models",
            "Evaluate model performance",
            "Deploy forecasting pipeline",
            "Monitor prediction accuracy"
        ],
        "impact": "Better demand planning and reduced stock-related problems"
    },

    "Inventory Optimization": {
        "timeline": "6–10 weeks",
        "estimated_cost": "Medium",
        "team": "Data Scientist + Data Engineer + Operations Team",
        "steps": [
            "Collect inventory and transaction data",
            "Analyze inventory patterns",
            "Identify stock-out and overstock situations",
            "Develop optimization model",
            "Test recommendations",
            "Integrate with inventory system",
            "Monitor inventory performance"
        ],
        "impact": "Reduced inventory costs and improved stock availability"
    },

    "Customer Churn Prediction": {
        "timeline": "6–10 weeks",
        "estimated_cost": "Medium",
        "team": "Data Scientist + Data Engineer + Marketing Team",
        "steps": [
            "Collect historical customer data",
            "Identify customers who previously churned",
            "Create customer behavior features",
            "Train classification model",
            "Evaluate model performance",
            "Generate customer churn scores",
            "Create retention workflows",
            "Monitor model performance"
        ],
        "impact": "Earlier identification of customers at risk of leaving"
    },

    "Recommendation System": {
        "timeline": "8–12 weeks",
        "estimated_cost": "High",
        "team": "ML Engineer + Data Scientist + Backend Developer",
        "steps": [
            "Collect customer interaction data",
            "Prepare product and customer datasets",
            "Analyze user behavior",
            "Develop recommendation algorithm",
            "Train and evaluate recommendation model",
            "Integrate recommendations into the application",
            "Run A/B testing",
            "Monitor recommendation quality"
        ],
        "impact": "More personalized customer experiences and potential revenue growth"
    },

    "Fraud Detection": {
        "timeline": "8–12 weeks",
        "estimated_cost": "High",
        "team": "Data Scientist + ML Engineer + Security Team",
        "steps": [
            "Collect historical transaction data",
            "Identify fraudulent transactions",
            "Engineer fraud detection features",
            "Train machine learning models",
            "Evaluate false positives and false negatives",
            "Integrate real-time detection",
            "Create fraud monitoring dashboard",
            "Continuously retrain the model"
        ],
        "impact": "Earlier detection of potentially fraudulent transactions"
    },


    # ========================================================
    # AI AGENT IMPLEMENTATION PLANS
    # ========================================================

    "AI Customer Service Agent": {
        "timeline": "8–12+ weeks",
        "estimated_cost": "Medium",
        "team": "AI Engineer + Backend Developer + Support Team",
        "steps": [
            "Collect customer support data and FAQs",
            "Organize customer and support knowledge sources",
            "Build the agent knowledge base",
            "Connect the LLM to the agent",
            "Define customer service workflows",
            "Connect order and customer information systems",
            "Implement escalation to human support",
            "Test agent responses and workflows",
            "Deploy the customer service agent",
            "Monitor conversations and agent performance"
        ],
        "impact": "Automated customer assistance and reduced support workload"
    },


    "AI Sales Agent": {
        "timeline": "8–12+ weeks",
        "estimated_cost": "High",
        "team": "AI Engineer + Backend Developer + Sales Team",
        "steps": [
            "Collect customer, product and sales data",
            "Build product and customer knowledge base",
            "Connect the LLM to the sales agent",
            "Define lead qualification workflows",
            "Implement product recommendation capabilities",
            "Connect CRM and sales systems",
            "Enable customer interaction workflows",
            "Add human approval for important sales actions",
            "Test sales conversations",
            "Deploy and monitor the sales agent"
        ],
        "impact": "Automated sales assistance and improved customer engagement"
    },


    "AI Marketing Agent": {
        "timeline": "8–12+ weeks",
        "estimated_cost": "Medium",
        "team": "AI Engineer + Marketing Specialist + Backend Developer",
        "steps": [
            "Collect customer and marketing data",
            "Organize marketing knowledge and brand guidelines",
            "Connect the LLM to the marketing agent",
            "Define campaign planning workflows",
            "Build content generation capabilities",
            "Connect marketing platforms",
            "Implement campaign monitoring workflows",
            "Add human approval before publishing",
            "Test generated campaigns and content",
            "Deploy and monitor the marketing agent"
        ],
        "impact": "Faster campaign creation and reduced marketing workload"
    },


    "AI Inventory Agent": {
        "timeline": "8–12+ weeks",
        "estimated_cost": "High",
        "team": "AI Engineer + Data Engineer + Operations Team",
        "steps": [
            "Collect inventory, product and sales data",
            "Build inventory knowledge base",
            "Connect the LLM to the inventory agent",
            "Define stock monitoring workflows",
            "Detect low-stock and overstock situations",
            "Connect inventory and procurement systems",
            "Generate replenishment recommendations",
            "Add human approval for inventory actions",
            "Test inventory workflows",
            "Deploy and monitor the inventory agent"
        ],
        "impact": "Automated inventory monitoring and improved stock management"
    }
}


# ============================================================
# DEFAULT PLAN
# ============================================================

DEFAULT_PLAN = {

    "timeline": "4–8 weeks",

    "estimated_cost": "Medium",

    "team": "Data Scientist + Software Developer",

    "steps": [
        "Collect relevant business data",
        "Clean and prepare the data",
        "Analyze the business requirements",
        "Select an appropriate AI approach",
        "Develop and test the AI solution",
        "Integrate the solution with existing systems",
        "Deploy the solution",
        "Monitor performance"
    ],

    "impact": "Improved business efficiency through AI adoption"
}


# ============================================================
# CREATE IMPLEMENTATION PLAN
# ============================================================

def create_implementation_plan(scored_opportunities):

    implementation_plans = []

    for _, row in scored_opportunities.iterrows():

        use_case = str(
            row.get("use_case", "")
        )

        technology = str(
            row.get("technology", "")
        )

        score = float(
            row.get("score", 0)
        )

        priority = str(
            row.get("priority", "")
        )

        plan = IMPLEMENTATION_PLANS.get(
            use_case,
            DEFAULT_PLAN
        )

        implementation_plans.append({

            "use_case": use_case,

            "technology": technology,

            "score": score,

            "priority": priority,

            "timeline": plan["timeline"],

            "estimated_cost": plan["estimated_cost"],

            "team": plan["team"],

            "steps": plan["steps"],

            "impact": plan["impact"]
        })

    return implementation_plans