import pandas as pd


def create_excel_report(
    business_profile,
    scored_opportunities,
    roadmap,
    implementation_plan,
    roi_analysis,
    file_path
):

    with pd.ExcelWriter(
        file_path,
        engine="openpyxl"
    ) as writer:

        # ============================================================
        # 1. BUSINESS PROFILE
        # ============================================================

        profile_data = []

        for key, value in business_profile.items():

            if isinstance(value, list):
                value = ", ".join(
                    str(item)
                    for item in value
                )

            profile_data.append({
                "Field": key,
                "Value": value
            })

        profile_df = pd.DataFrame(profile_data)

        profile_df.to_excel(
            writer,
            sheet_name="Business Profile",
            index=False
        )

        # ============================================================
        # 2. AI OPPORTUNITIES
        # ============================================================

        scored_opportunities.to_excel(
            writer,
            sheet_name="AI Opportunities",
            index=False
        )

        # ============================================================
        # 3. ROADMAP
        # ============================================================

        roadmap_rows = []

        for phase, opportunities in roadmap.items():

            for opportunity in opportunities:

                roadmap_rows.append({
                    "Phase": phase,
                    "AI Opportunity": opportunity
                })

        roadmap_df = pd.DataFrame(roadmap_rows)

        roadmap_df.to_excel(
            writer,
            sheet_name="Roadmap",
            index=False
        )

        # ============================================================
        # 4. IMPLEMENTATION PLAN
        # ============================================================

        implementation_rows = []

        # Handle dictionary format
        if isinstance(implementation_plan, dict):

            for use_case, details in implementation_plan.items():

                if isinstance(details, dict):

                    row = {
                        "Use Case": use_case
                    }

                    row.update(details)

                    implementation_rows.append(row)

                else:

                    implementation_rows.append({
                        "Use Case": use_case,
                        "Implementation Plan": details
                    })

        # Handle list format
        elif isinstance(implementation_plan, list):

            for item in implementation_plan:

                if isinstance(item, dict):

                    implementation_rows.append(item)

                else:

                    implementation_rows.append({
                        "Implementation Plan": str(item)
                    })

        implementation_df = pd.DataFrame(
            implementation_rows
        )

        implementation_df.to_excel(
            writer,
            sheet_name="Implementation Plan",
            index=False
        )

        # ============================================================
        # 5. ROI ANALYSIS
        # ============================================================

        roi_analysis.to_excel(
            writer,
            sheet_name="ROI Analysis",
            index=False
        )

    return file_path