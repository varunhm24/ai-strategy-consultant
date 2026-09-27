import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import streamlit as st
import pandas as pd

from strategy.opportunity_engine import find_opportunities
from strategy.scoring_engine import score_opportunities
from strategy.roadmap_engine import create_roadmap
from strategy.implementation_engine import create_implementation_plan
from strategy.roi_engine import create_roi_analysis
from reports.report_generator import create_excel_report
from reports.pdf_report_generator import create_pdf_report


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Strategy Consultant",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("🤖 AI Strategy Consultant")

st.write(
    "Build an AI adoption strategy for your business."
)

st.divider()


# ============================================================
# BUSINESS PROFILE
# ============================================================

st.header("🏢 Business Profile")

st.write(
    "Enter information about your company. "
    "This information will be used to identify "
    "potential AI opportunities."
)


# ============================================================
# COMPANY INFORMATION
# ============================================================

st.subheader("Company Information")

col1, col2 = st.columns(2)

with col1:

    company_name = st.text_input(
        "Company Name",
        placeholder="Example: ABC Electronics"
    )

    industry = st.selectbox(
        "Industry",
        [
            "E-commerce",
            "Healthcare",
            "Finance",
            "Education",
            "Manufacturing",
            "Retail",
            "IT / Software",
            "Logistics",
            "Agriculture",
            "Real Estate",
            "Other"
        ]
    )

    employees = st.number_input(
        "Number of Employees",
        min_value=1,
        max_value=100000,
        value=50,
        step=1
    )


with col2:

    business_model = st.selectbox(
        "Business Model",
        [
            "B2B",
            "B2C",
            "B2B2C",
            "Marketplace",
            "Subscription",
            "Other"
        ]
    )

    monthly_customers = st.number_input(
        "Monthly Customers",
        min_value=0,
        value=1000,
        step=100
    )

    monthly_transactions = st.number_input(
        "Monthly Transactions",
        min_value=0,
        value=1000,
        step=100
    )

    monthly_revenue = st.number_input(
    "Monthly Revenue (₹)",
    min_value=0,
    value=100000,
    step=10000
    )


st.divider()


# ============================================================
# BUSINESS PROBLEMS
# ============================================================

st.subheader("🎯 Business Problems")

st.write(
    "Select the major problems your company currently faces."
)

business_problems = st.multiselect(
    "Business Problems",
    [
        "Customer Support",
        "Sales",
        "Marketing",
        "Inventory Management",
        "Demand Forecasting",
        "Fraud Detection",
        "Customer Churn",
        "Employee Productivity",
        "Document Processing",
        "Data Analysis",
        "Operations",
        "Other"
    ]
)

other_problem = st.text_area(
    "Describe other problems",
    placeholder=(
        "Example: Employees spend too much time "
        "creating weekly reports."
    )
)


st.divider()


# ============================================================
# AVAILABLE DATA
# ============================================================

st.subheader("📊 Available Data")

st.write(
    "Select the types of data available in your company."
)

available_data = st.multiselect(
    "Available Data",
    [
        "Customer Data",
        "Sales Data",
        "Transaction Data",
        "Product Data",
        "Inventory Data",
        "Employee Data",
        "Financial Data",
        "Marketing Data",
        "Website Data",
        "Support Tickets",
        "Documents",
        "Images",
        "Videos",
        "No Structured Data"
    ]
)


st.divider()


# ============================================================
# CURRENT TECHNOLOGY
# ============================================================

st.subheader("💻 Current Technology")

current_technology = st.multiselect(
    "Technology currently used",
    [
        "Excel",
        "Google Sheets",
        "SQL Database",
        "Python",
        "Cloud Platform",
        "CRM",
        "ERP",
        "Power BI / Tableau",
        "Existing AI/ML System",
        "None"
    ]
)


st.divider()


# ============================================================
# AI INVESTMENT
# ============================================================

st.subheader("💰 AI Investment")

budget = st.selectbox(
    "Estimated AI Implementation Budget",
    [
        "Less than ₹50,000",
        "₹50,000 – ₹2 Lakhs",
        "₹2 Lakhs – ₹5 Lakhs",
        "₹5 Lakhs – ₹10 Lakhs",
        "More than ₹10 Lakhs",
        "Not decided"
    ]
)


st.divider()


# ============================================================
# BUSINESS GOALS
# ============================================================

st.subheader("🚀 Business Goals")

business_goals = st.multiselect(
    "What are your main business goals?",
    [
        "Reduce Costs",
        "Increase Revenue",
        "Improve Customer Experience",
        "Automate Repetitive Tasks",
        "Improve Decision Making",
        "Increase Productivity",
        "Reduce Fraud",
        "Improve Forecasting",
        "Scale Operations",
        "Generate New Products"
    ]
)


st.divider()


# ============================================================
# ANALYZE BUSINESS
# ============================================================

st.header("🔍 Analyze Business")

analyze_button = st.button(
    "Analyze Business",
    type="primary",
    use_container_width=True
)


if analyze_button:

    # ========================================================
    # VALIDATION
    # ========================================================

    if not company_name.strip():

        st.error(
            "Please enter the company name."
        )

        st.stop()


    if not business_problems:

        st.error(
            "Please select at least one business problem."
        )

        st.stop()


    # ========================================================
    # CREATE BUSINESS PROFILE
    # ========================================================

    business_profile = {

        "company_name": company_name,

        "industry": industry,

        "employees": employees,

        "business_model": business_model,

        "monthly_customers": monthly_customers,

        "monthly_transactions": monthly_transactions,

        "monthly_revenue": monthly_revenue,

        "business_problems": business_problems,

        "other_problem": other_problem,

        "available_data": available_data,

        "current_technology": current_technology,

        "budget": budget,

        "business_goals": business_goals

    }


    # ========================================================
    # SAVE PROFILE
    # ========================================================

    st.session_state["business_profile"] = business_profile


    st.success(
        "✅ Business profile created successfully!"
    )


    # ========================================================
    # DISPLAY PROFILE
    # ========================================================

    st.subheader(
        "📋 Business Profile Summary"
    )

    st.json(
        business_profile
    )


    # ========================================================
    # FIND AI OPPORTUNITIES
    # ========================================================

    st.divider()

    st.header(
        "🤖 AI Opportunity Analysis"
    )


    with st.spinner(
        "Analyzing business opportunities..."
    ):

        opportunities = find_opportunities(
            business_profile
        )


    # ========================================================
    # CHECK OPPORTUNITIES
    # ========================================================

    if opportunities is None:

        st.error(
            "Opportunity engine returned no result."
        )

        st.stop()


    if len(opportunities) == 0:

        st.warning(
            "No matching AI opportunities were found."
        )

        st.stop()


    st.success(
        f"Found {len(opportunities)} AI opportunities."
    )


    # ========================================================
    # SCORE OPPORTUNITIES
    # ========================================================

    with st.spinner(
        "Scoring AI opportunities..."
    ):

        scored_opportunities = score_opportunities(
            opportunities
        )


    if scored_opportunities is None:

        st.error(
            "Scoring engine returned no result."
        )

        st.stop()


    if len(scored_opportunities) == 0:

        st.warning(
            "No opportunities could be scored."
        )

        st.stop()


    # ========================================================
    # SAVE SCORED OPPORTUNITIES
    # ========================================================

    st.session_state[
        "scored_opportunities"
    ] = scored_opportunities


    # ========================================================
    # AI OPPORTUNITY MATRIX
    # ========================================================

    st.divider()

    st.header(
        "📊 AI Opportunity Matrix"
    )


    display_columns = [

        "use_case",

        "technology",

        "business_impact",

        "implementation_difficulty",

        "cost_level",

        "score",

        "priority"

    ]


    # Only display columns that actually exist

    available_columns = [

        column
        for column in display_columns
        if column in scored_opportunities.columns

    ]


    st.dataframe(

        scored_opportunities[
            available_columns
        ],

        use_container_width=True,

        hide_index=True

    )


    # ========================================================
    # CREATE AI ROADMAP
    # ========================================================

    st.divider()

    with st.spinner(
        "Creating AI implementation roadmap..."
    ):

        roadmap = create_roadmap(
            scored_opportunities
        )

    st.session_state["roadmap"] = roadmap


    # ========================================================
    # CREATE IMPLEMENTATION PLAN
    # ========================================================

    with st.spinner(
        "Creating detailed implementation plan..."
    ):

        implementation_plan = create_implementation_plan(
            scored_opportunities
        )
        st.session_state["implementation_plan"] = implementation_plan
        with st.spinner(
            "Calculating AI investment and ROI..."
            ):
            roi_analysis = create_roi_analysis(
                scored_opportunities,
                business_profile
            )
            st.session_state["roi_analysis"] = roi_analysis

# ============================================================
# DISPLAY SAVED AI ROADMAP
# ============================================================

if "roadmap" in st.session_state:

    roadmap = st.session_state["roadmap"]

    st.divider()

    st.header("🗺️ AI Implementation Roadmap")

    st.write(
        "Recommended implementation path based on the "
        "identified AI opportunities."
    )

    # ========================================================
    # PHASE 1
    # ========================================================

    st.subheader("🟢 Phase 1 — Quick AI Wins")

    phase1 = roadmap.get(
        "Phase 1 - Quick AI Wins",
        []
    )

    if phase1:

        for item in phase1:

            st.success(
                f"✅ {item}"
            )

    else:

        st.info(
            "No quick-win opportunities identified."
        )


    # ========================================================
    # PHASE 2
    # ========================================================

    st.subheader("🔵 Phase 2 — AI Automation")

    phase2 = roadmap.get(
        "Phase 2 - AI Automation",
        []
    )

    if phase2:

        for item in phase2:

            st.info(
                f"⚙️ {item}"
            )

    else:

        st.info(
            "No automation opportunities identified."
        )


    # ========================================================
    # PHASE 3
    # ========================================================

    st.subheader("🟠 Phase 3 — Advanced ML")

    phase3 = roadmap.get(
        "Phase 3 - Advanced ML",
        []
    )

    if phase3:

        for item in phase3:

            st.warning(
                f"🧠 {item}"
            )

    else:

        st.info(
            "No advanced ML opportunities identified."
        )


    # ========================================================
    # PHASE 4
    # ========================================================

    st.subheader("🟣 Phase 4 — AI Agents")

    phase4 = roadmap.get(
        "Phase 4 - AI Agents",
        []
    )

    if phase4:

        for item in phase4:

            st.write(
                f"🤖 {item}"
            )

    else:

        st.info(
            "No AI agent opportunities identified yet."
        )


# ============================================================
# DETAILED IMPLEMENTATION PLAN
# ============================================================

if "implementation_plan" in st.session_state:

    implementation_plan = st.session_state[
        "implementation_plan"
    ]

    st.divider()

    st.header(
        "🛠️ Detailed AI Implementation Plan"
    )

    st.write(
        "Detailed implementation guidance for "
        "the identified AI opportunities."
    )

    for plan in implementation_plan:

        st.subheader(
            f"🚀 {plan['use_case']}"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Priority",
                plan["priority"]
            )

        with col2:

            st.metric(
                "Score",
                plan["score"]
            )

        with col3:

            st.metric(
                "Timeline",
                plan["timeline"]
            )

        with col4:

            st.metric(
                "Estimated Cost",
                plan["estimated_cost"]
            )

        st.write(
            f"**Technology:** {plan['technology']}"
        )

        st.write(
            f"**Required Team:** {plan['team']}"
        )

        st.write(
            f"**Expected Impact:** {plan['impact']}"
        )

        st.write("### Implementation Steps")

        for number, step in enumerate(
            plan["steps"],
            start=1
        ):

            st.write(
                f"{number}. {step}"
            )

        st.divider()

# ============================================================
# AI COST & ROI ANALYSIS
# ============================================================

if "roi_analysis" in st.session_state:

    roi_analysis = st.session_state["roi_analysis"]

    st.divider()

    st.header("💰 AI Cost & ROI Analysis")

    st.write(
        "Estimated investment, annual benefit, "
        "ROI and payback period for each AI opportunity."
    )

    for _, item in roi_analysis.iterrows():

        st.subheader(
            f"💡 {item['use_case']}"
        )

        # ----------------------------------------------------
        # FINANCIAL METRICS
        # ----------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Implementation Cost",
                f"₹{item['implementation_cost']:,.0f}"
            )

        with col2:

            st.metric(
                "Annual Benefit",
                f"₹{item['annual_benefit']:,.0f}"
            )

        with col3:

            st.metric(
                "Estimated ROI",
                f"{item['roi_percent']}%"
            )

        with col4:

            payback = item["payback_months"]

            if pd.notna(payback):

                st.metric(
                    "Payback Period",
                    f"{payback} months"
                )

            else:

                st.metric(
                    "Payback Period",
                    "N/A"
                )

        # ----------------------------------------------------
        # TECHNOLOGY
        # ----------------------------------------------------

        st.write(
            f"**Technology:** {item['technology']}"
        )

        # ----------------------------------------------------
        # PRIORITY
        # ----------------------------------------------------

        st.write(
            f"**Priority:** {item['priority']}"
        )

        # ----------------------------------------------------
        # BUDGET FIT
        # ----------------------------------------------------

        budget_status = item.get(
            "budget_status",
            "Budget not decided"
        )

        if budget_status == "Within Budget":

            st.success(
                "💰 Budget Fit: Within Budget"
            )

        elif budget_status == "Above Budget":

            st.warning(
                "💰 Budget Fit: Above Budget"
            )

        else:

            st.info(
                "💰 Budget Fit: Budget not decided"
            )

        st.divider()


    # ========================================================
    # BUDGET ANALYSIS
    # ========================================================

    st.subheader("💰 Budget Analysis")

    if "budget_gap" in roi_analysis.columns:

        total_budget_gap = roi_analysis[
            "budget_gap"
        ].sum()

        above_budget_count = (
            roi_analysis["budget_status"]
            == "Above Budget"
        ).sum()

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Total Budget Gap",
                f"₹{total_budget_gap:,.0f}"
            )

        with col2:

            st.metric(
                "Opportunities Above Budget",
                above_budget_count
            )

        # ====================================================
        # BUDGET GAP BY OPPORTUNITY
        # ====================================================

        st.subheader(
            "📊 Budget Gap by AI Opportunity"
        )

        budget_display = roi_analysis[
            [
                "use_case",
                "implementation_cost",
                "budget_status",
                "budget_gap"
            ]
        ].copy()

        budget_display.columns = [
            "AI Opportunity",
            "Implementation Cost",
            "Budget Status",
            "Budget Gap"
        ]

        budget_display[
            "Implementation Cost"
        ] = (
            budget_display[
                "Implementation Cost"
            ].apply(
                lambda x: f"₹{x:,.0f}"
            )
        )

        budget_display[
            "Budget Gap"
        ] = (
            budget_display[
                "Budget Gap"
            ].apply(
                lambda x: f"₹{x:,.0f}"
            )
        )

        st.dataframe(
            budget_display,
            use_container_width=True
        )
    
    # ============================================================
    # AI STRATEGY DASHBOARD
    # ============================================================

    if "scored_opportunities" in st.session_state:

        scored_opportunities = st.session_state[
            "scored_opportunities"
        ]

        st.divider()

        st.header("📊 AI Strategy Dashboard")

        st.write(
            "High-level summary of the AI opportunities "
            "identified for your business."
        )

        # --------------------------------------------------------
        # SUMMARY METRICS
        # --------------------------------------------------------

        total_opportunities = len(scored_opportunities)

        high_priority = len(
            scored_opportunities[
                scored_opportunities["priority"].isin(
                    ["Very High", "High"]
                )
            ]
        )

        medium_priority = len(
            scored_opportunities[
                scored_opportunities["priority"] == "Medium"
            ]
        )

        low_priority = len(
            scored_opportunities[
                scored_opportunities["priority"] == "Low"
            ]
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "AI Opportunities",
                total_opportunities
            )

        with col2:

            st.metric(
                "High Priority",
                high_priority
            )

        with col3:

            st.metric(
                "Medium Priority",
                medium_priority
            )

        with col4:

            st.metric(
                "Low Priority",
                low_priority
            )

        # --------------------------------------------------------
        # OPPORTUNITY BY TECHNOLOGY
        # --------------------------------------------------------

        st.subheader("🧠 AI Technology Distribution")

        technology_counts = (
            scored_opportunities["technology"]
            .value_counts()
            .reset_index()
        )

        technology_counts.columns = [
            "Technology",
            "Opportunities"
        ]

        st.bar_chart(
            technology_counts.set_index("Technology")
        )

        # --------------------------------------------------------
        # PRIORITY DISTRIBUTION
        # --------------------------------------------------------

        st.subheader("🎯 Priority Distribution")

        priority_counts = (
            scored_opportunities["priority"]
            .value_counts()
            .reset_index()
        )

        priority_counts.columns = [
            "Priority",
            "Opportunities"
        ]

        st.dataframe(
            priority_counts,
            use_container_width=True,
            hide_index=True
        )
    # ============================================================
    # EXCEL REPORT
    # ============================================================

    st.divider()

    st.subheader("📥 Download AI Strategy Report")

    st.write(
        "Download the AI strategy analysis as an Excel file "
        "containing the business profile, AI opportunities, "
        "roadmap, implementation plan, and ROI analysis."
    )

    if st.button("📊 Generate Excel Report"):

        business_profile = st.session_state[
            "business_profile"
        ]

        scored_opportunities = st.session_state[
            "scored_opportunities"
        ]

        roi_analysis = st.session_state[
            "roi_analysis"
        ]

        roadmap = st.session_state[
            "roadmap"
        ]

        implementation_plan = st.session_state[
            "implementation_plan"
        ]

        report_path = "reports/AI_Strategy_Report.xlsx"

        create_excel_report(
            business_profile,
            scored_opportunities,
            roadmap,
            implementation_plan,
            roi_analysis,
            report_path
        )

        with open(report_path, "rb") as file:

            st.download_button(
                label="⬇️ Download Excel Report",
                data=file,
                file_name="AI_Strategy_Report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


    # ============================================================
    # PDF REPORT
    # ============================================================

    st.divider()

    st.subheader("📄 Download PDF Strategy Report")

    st.write(
        "Generate a professional PDF containing the "
        "business profile, AI opportunities, roadmap, "
        "implementation plan, and ROI analysis."
    )

    if st.button("📄 Generate PDF Report"):

        business_profile = st.session_state[
            "business_profile"
        ]

        scored_opportunities = st.session_state[
            "scored_opportunities"
        ]

        roadmap = st.session_state[
            "roadmap"
        ]

        implementation_plan = st.session_state[
            "implementation_plan"
        ]

        roi_analysis = st.session_state[
            "roi_analysis"
        ]

        pdf_path = "reports/AI_Strategy_Report.pdf"

        create_pdf_report(
            business_profile,
            scored_opportunities,
            roadmap,
            implementation_plan,
            roi_analysis,
            pdf_path
        )

        with open(pdf_path, "rb") as file:

            st.download_button(
                label="⬇️ Download PDF Report",
                data=file,
                file_name="AI_Strategy_Report.pdf",
                mime="application/pdf"
            )
            
        