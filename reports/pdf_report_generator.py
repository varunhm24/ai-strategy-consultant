# ============================================================
# AI STRATEGY PDF REPORT GENERATOR
# ============================================================
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)

from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import HorizontalBarChart
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics import renderPDF
from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ========================================================
# UNICODE FONT
# ========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
FONT_DIR = BASE_DIR / "fonts"

pdfmetrics.registerFont(
    TTFont(
        "NotoSans",
        str(FONT_DIR / "NotoSans-Regular.ttf")
    )
)

pdfmetrics.registerFont(
    TTFont(
        "NotoSans-Bold",
        str(FONT_DIR / "NotoSans-Bold.ttf")
    )
)

pdfmetrics.registerFontFamily(
    "NotoSans",
    normal="NotoSans",
    bold="NotoSans-Bold",
    italic="NotoSans",
    boldItalic="NotoSans-Bold"
)


# ========================================================
# PDF HEADER AND FOOTER
# ========================================================

def add_page_number(canvas, doc):

    page_number = canvas.getPageNumber()

    canvas.saveState()

    # ----------------------------------------------------
    # HEADER
    # ----------------------------------------------------

    canvas.setFont("NotoSans-Bold", 8)

    canvas.drawString(
        15 * mm,
        A4[1] - 10 * mm,
        "AI STRATEGY CONSULTANT"
    )

    canvas.setFont("NotoSans", 8)

    canvas.drawRightString(
        A4[0] - 15 * mm,
        A4[1] - 10 * mm,
        "CONFIDENTIAL"
    )

    # Header line
    canvas.line(
        15 * mm,
        A4[1] - 13 * mm,
        A4[0] - 15 * mm,
        A4[1] - 13 * mm
    )

    # ----------------------------------------------------
    # FOOTER
    # ----------------------------------------------------

    canvas.setFont("NotoSans", 8)

    canvas.drawString(
        15 * mm,
        10 * mm,
        "AI Strategy & Implementation Report"
    )

    canvas.drawRightString(
        A4[0] - 15 * mm,
        10 * mm,
        f"Page {page_number}"
    )

    # Footer line
    canvas.line(
        15 * mm,
        13 * mm,
        A4[0] - 15 * mm,
        13 * mm
    )

    canvas.restoreState()


def create_pdf_report(
    business_profile,
    scored_opportunities,
    roadmap,
    implementation_plan,
    roi_analysis,
    file_path
):

    document = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontName="NotoSans",
        alignment=TA_CENTER,
        fontSize=24,
        leading=28,
        spaceAfter=12
    )

    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading2"],
        fontName="NotoSans-Bold",
        fontSize=16,
        spaceBefore=15,
        spaceAfter=10
    )

    normal_style = ParagraphStyle(
        "NormalStyle",
        parent=styles["BodyText"],
        fontName="NotoSans",
        fontSize=9,
        leading=13
    )

    story = []
    # Track section pages for the Table of Contents
    toc_entries = []

    # ========================================================
    # TITLE
    # ========================================================

    story.append(Spacer(1, 35))

    story.append(
        Paragraph(
            "AI STRATEGY CONSULTANT",
            ParagraphStyle(
                "CoverTitle",
                parent=styles["Title"],
                fontName="NotoSans",
                alignment=TA_CENTER,
                fontSize=26,
                leading=32,
                spaceAfter=15
            )
        )
    )

    story.append(
        Paragraph(
            "AI Strategy & Implementation Report",
            ParagraphStyle(
                "CoverSubtitle",
                parent=styles["Heading2"],
                fontName="NotoSans-Bold",
                alignment=TA_CENTER,
                fontSize=16,
                leading=20,
                spaceAfter=30
            )
        )
    )

# Company name
    company_name = business_profile.get(
        "company_name",
        "Business Analysis"
    )

    story.append(
        Paragraph(
            f"<b>Prepared for:</b> {company_name}",
            ParagraphStyle(
                "CompanyName",
                parent=normal_style,
                fontName="NotoSans-Bold",
                alignment=TA_CENTER,
                fontSize=12,
                leading=18,
                spaceAfter=10
            )
        )
    )

# Industry
    industry = business_profile.get(
        "industry",
        ""
    )

    story.append(
        Paragraph(
            f"<b>Industry:</b> {industry}",
            ParagraphStyle(
                "Industry",
                parent=normal_style,
                fontName="NotoSans",
                alignment=TA_CENTER,
                fontSize=10,
                leading=15,
                spaceAfter=20
            )
        )
    )

    story.append(Spacer(1, 25))

# Report description
    cover_description = (
        "AI opportunity assessment, implementation roadmap, "
        "detailed implementation planning, and estimated "
        "cost and ROI analysis."
    )

    story.append(
        Paragraph(
            cover_description,
            ParagraphStyle(
                "CoverDescription",
                parent=normal_style,
                fontName="NotoSans",
                alignment=TA_CENTER,
                fontSize=10,
                leading=16,
                leftIndent=25 * mm,
                rightIndent=25 * mm,
                spaceAfter=30
            )
        )
    )

    story.append(Spacer(1, 45))

# Confidentiality
    story.append(
        Paragraph(
            "CONFIDENTIAL",
            ParagraphStyle(
                "Confidential",
                parent=normal_style,
                fontName="NotoSans",
                alignment=TA_CENTER,
                fontSize=9,
                leading=14,
                spaceAfter=8
            )
        )
    )

    story.append(
        Paragraph(
            "AI Strategy & Implementation Report",
            ParagraphStyle(
                "CoverFooter",
                parent=normal_style,
                fontName="NotoSans",
                alignment=TA_CENTER,
                fontSize=8,
                leading=12
            )
        )
    )

# Start report content on a new page
    story.append(PageBreak())


    # ============================================================
# TABLE OF CONTENTS
# ============================================================

    story.append(
        Paragraph(
            "Table of Contents",
            heading_style
        )
    )

    story.append(Spacer(1, 8))

    toc_data = [
        ["Section", "Report Section", "Description"],

        ["1",
        "Business Profile",
        "Company, industry, business model, scale, budget and business context"],

        ["2",
        "AI Opportunity Matrix",
        "Identified AI use cases, technologies, impact, difficulty, cost and priority"],

        ["3",
        "AI Implementation Roadmap",
        "Phased roadmap from quick AI wins to advanced AI initiatives"],

        ["4",
        "Detailed Implementation Plan",
        "Implementation requirements, timelines, teams and execution steps"],

        ["5",
        "AI Cost & ROI Analysis",
        "Estimated investment, annual benefit, ROI and payback analysis"],

        ["6",
        "Strategic Conclusion",
        "Overall AI strategy considerations and implementation guidance"]
    ]

    toc_table = Table(
        toc_data,
        colWidths=[
            18 * mm,
            55 * mm,
            97 * mm
        ],
        repeatRows=1
    )

    toc_table.setStyle(
        TableStyle([
        # Header
            ("BACKGROUND",
             (0, 0), (-1, 0),
             colors.HexColor("#1F4E78")),

            ("TEXTCOLOR",
             (0, 0), (-1, 0),
             colors.white),

            ("FONTNAME",
             (0, 0), (-1, 0),
             "NotoSans-Bold"),

        # Section number
            ("FONTNAME",
             (0, 1), (0, -1),
             "NotoSans-Bold"),

            ("ALIGN",
             (0, 1), (0, -1),
             "CENTER"),

        # Body
            ("FONTNAME",
             (1, 1), (1, -1),
             "NotoSans-Bold"),
 
            ("FONTNAME",
             (2, 1), (2, -1),
             "NotoSans"),

            ("GRID",
             (0, 0), (-1, -1),
             0.5,
             colors.grey),

            ("VALIGN",
             (0, 0), (-1, -1),
             "TOP"),

            ("FONTSIZE",
             (0, 0), (-1, -1),
             8),

            ("LEFTPADDING",
             (0, 0), (-1, -1),
             7),

            ("RIGHTPADDING",
             (0, 0), (-1, -1),
             7),

            ("TOPPADDING",
             (0, 0), (-1, -1),
             8),

            ("BOTTOMPADDING",
             (0, 0), (-1, -1),
             8),
        ])
    )

    story.append(toc_table)

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "This report presents the AI opportunities identified "
            "for the business, their implementation roadmap, "
            "detailed execution plan, and estimated financial "
            "analysis.",
            normal_style
        )
    )

    story.append(PageBreak())

    # ========================================================
    # KPI SUMMARY
    # ========================================================

    total_opportunities = len(
        scored_opportunities
    )

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

    if not roi_analysis.empty:
        total_investment = roi_analysis[
            "implementation_cost"
        ].sum()

        total_annual_benefit = roi_analysis[
            "annual_benefit"
        ].sum()

    else:
        total_investment = 0
        total_annual_benefit = 0
    if total_investment > 0:
        overall_roi = (
            (
                total_annual_benefit
                - total_investment
            )
            / total_investment
        ) * 100

    else:
        overall_roi = 0

    kpi_data = [
        ["KPI", "Value"],
        [
            "AI Opportunities",
            str(total_opportunities)
        ],
        [
            "High / Very High Priority",
            str(high_priority)
        ],
        [
            "Medium Priority",
            str(medium_priority)
        ],
        [
            "Low Priority",
            str(low_priority)
        ],
        [
            "Estimated Investment",
            f"₹{total_investment:,.0f}"
        ],
        [
            "Estimated Annual Benefit",
            f"₹{total_annual_benefit:,.0f}"
        ],
        [
            "Estimated Overall ROI",
            f"{overall_roi:.1f}%"
        ]
    ]

    kpi_table = Table(
        kpi_data,
        colWidths=[
            90 * mm,
            80 * mm
        ]
    )

    kpi_table.setStyle(
        TableStyle([
            (
            "BACKGROUND",
            (0, 0),
            (-1, 0),
            colors.HexColor("#1F4E78")
        ),
        (
            "TEXTCOLOR",
            (0, 0),
            (-1, 0),
            colors.white
        ),
        (
            "FONTNAME",
            (0, 0),
            (-1, 0),
            "NotoSans-Bold"
        ),

        # KPI names
        (
            "FONTNAME",
            (0, 1),
            (0, -1),
            "NotoSans-Bold"
        ),
        
        # KPI values
        (
            "FONTNAME",
            (1, 1),
            (1, -1),
            "NotoSans"
        ),

        # Borders
        (
            "GRID",
            (0, 0),
            (-1, -1),
            0.5,
            colors.grey
        ),

        # Alignment
        (
            "VALIGN",
            (0, 0),
            (-1, -1),
            "MIDDLE"
        ),

        # Font
        (
            "FONTSIZE",
            (0, 0),
            (-1, -1),
            9
        ),

        # Padding
        (
            "LEFTPADDING",
            (0, 0),
            (-1, -1),
            7
        ),
        (
            "RIGHTPADDING",
            (0, 0),
            (-1, -1),
            7
        ),
        (
            "TOPPADDING",
            (0, 0),
            (-1, -1),
            7
        ),
        (
            "BOTTOMPADDING",
            (0, 0),
            (-1, -1),
            7
        ),
    ])
)

    story.append(kpi_table)

    story.append(
        Spacer(1, 20)
    )

    # ============================================================
# MANAGEMENT SUMMARY
# ============================================================

    story.append(
        Paragraph(
            "Management Summary",
            styles["Heading3"]
            
        )
    )

    management_summary = (
        f"The assessment identified {total_opportunities} AI "
        f"opportunities across the business. "
        f"{high_priority} opportunities are classified as "
        f"High or Very High priority, {medium_priority} as "
        f"Medium priority, and {low_priority} as Low priority."
    )

    story.append(
        Paragraph(
            management_summary,
            normal_style
        )
    )

    story.append(Spacer(1, 6))

    if not roi_analysis.empty:

        investment_summary = (
            f"Across the identified opportunities, the estimated "
            f"implementation investment is "
            f"₹{total_investment:,.0f}, while the estimated annual "
            f"business benefit is ₹{total_annual_benefit:,.0f}."
        )

        story.append(
            Paragraph(
                investment_summary,
                normal_style
            )
        )

        story.append(Spacer(1, 6))

        roi_summary = (
            f"The combined estimated ROI is "
            f"{overall_roi:.1f}%. These financial figures are "
            f"estimates based on the assumptions supplied in the "
            f"business profile and should be validated before "
            f"investment decisions."
        )

        story.append(
            Paragraph(
                roi_summary,
                normal_style
            )
        )

    else:

        story.append(
            Paragraph(
                "Financial analysis is not available for the "
                "identified opportunities.",
                normal_style
            )
        )

        story.append(Spacer(1, 20))

    # ========================================================
    # PRIORITY DISTRIBUTION CHART
    # ========================================================
    priority_chart = Drawing(
        450,
        250
    )

    chart = HorizontalBarChart()
    chart.x = 60
    chart.y = 50
    chart.height = 160
    chart.width = 350
    chart.data = [[
        high_priority,
        medium_priority,
        low_priority
    ]]
    chart.categoryAxis.categoryNames = [
        "High / Very High",
        "Medium",
        "Low"
    ]
    chart.categoryAxis.labels.fontName = (
    "NotoSans"
    )

    chart.categoryAxis.labels.fontSize = 8
    
    chart.valueAxis.valueMin = 0
    max_priority = max(
        high_priority,
        medium_priority,
        low_priority,
        1
    )

    chart.valueAxis.valueMax = max_priority + 1
    chart.valueAxis.valueStep = 1
    chart.barWidth = 45
    chart.groupSpacing = 30
    chart.barLabels.visible = True
    chart.barLabels.fontSize = 9
    chart.barLabels.boxAnchor = "s"
    priority_chart.add(chart)
    story.append(
        Paragraph(
             "AI Opportunity Priority Distribution",
             styles["Heading3"]
        )
    )
    story.append(priority_chart)
    story.append(
        Spacer(1, 15)
    )

    # ========================================================
    # AI TECHNOLOGY DISTRIBUTION CHART
    # ========================================================
    technology_counts = (
        scored_opportunities["technology"]
        .value_counts()
    )

    technology_names = list(
        technology_counts.index
    )
    technology_values = list(
        technology_counts.values
    )
    technology_chart = Drawing(
        500,
        350
    )

    tech_chart = HorizontalBarChart()

    tech_chart.x = 110
    tech_chart.y = 50

    tech_chart.height = 250
    tech_chart.width = 360

    tech_chart.data = [
        technology_values
    ]

    tech_chart.categoryAxis.categoryNames = (
        technology_names
    )

    tech_chart.categoryAxis.labels.fontName = (
    "NotoSans"
    )

    tech_chart.categoryAxis.labels.fontSize = 8

    tech_chart.categoryAxis.labels.boxAnchor = "e"
    
    tech_chart.valueAxis.valueMin = 0
    max_technology = max(
        technology_values,
        default=1
    )
    tech_chart.valueAxis.valueMax = (
        max_technology + 1
    )
    tech_chart.valueAxis.valueStep = 1
    tech_chart.barWidth = 35
    tech_chart.groupSpacing = 25
    tech_chart.barLabels.visible = True
    tech_chart.barLabels.fontSize = 8
    tech_chart.barLabels.boxAnchor = "s"
    technology_chart.add(
        tech_chart
    )
    story.append(
        Paragraph(
            "AI Technology Distribution",
            styles["Heading3"]
        )
    )
    story.append(
        technology_chart
    )
    story.append(
        Spacer(1, 20)
    )



    # TECHNOLOGY DISTRIBUTION SUMMARY

    technology_summary_data = [
        ["Technology", "Number of Opportunities"]
    ]

    for technology, count in technology_counts.items():
            technology_summary_data.append([
            str(technology),
            str(count)
        ])

    technology_summary_table = Table(
        technology_summary_data,
        colWidths=[110 * mm, 60 * mm],
        repeatRows=1
    )

    technology_summary_table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#1F4E78")
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "NotoSans-Bold"
            ),

        # Body
            (
                "FONTNAME",
                (0, 1),
                (-1, -1),
                "NotoSans"
            ),

        # Borders
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                6
            ),

            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                6
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                6
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
        ])
    )

    story.append(
        Paragraph(
            "Technology Summary",
            styles["Heading3"]
        )
    )

    story.append(technology_summary_table)
    story.append(Spacer(1, 20))

    # ============================================================
    # INVESTMENT VS ANNUAL BENEFIT HORIZONTAL BAR CHART
    # ============================================================

    roi_use_cases = list(
        roi_analysis["use_case"]
    )

    investment_values = list(
        roi_analysis["implementation_cost"]
    )

    benefit_values = list(
        roi_analysis["annual_benefit"]
    )

    # ------------------------------------------------------------
    # SHORT LABELS FOR CHART
    # ------------------------------------------------------------

    roi_chart_labels = []

    for use_case in roi_use_cases:

        label = str(use_case)

        label = (
            label
            .replace("AI Customer Service Agent", "Customer Service Agent")
            .replace("AI Marketing Agent", "Marketing Agent")
            .replace("AI Sales Agent", "Sales Agent")
            .replace("AI Inventory Agent", "Inventory Agent")
        )

        roi_chart_labels.append(label)

    # ------------------------------------------------------------
    # CREATE HORIZONTAL BAR CHART
    # ------------------------------------------------------------

    roi_chart_drawing = Drawing(
        550,
        380
    )

    roi_chart = HorizontalBarChart()

    roi_chart.x = 140
    roi_chart.y = 70

    roi_chart.width = 360
    roi_chart.height = 250

    # ------------------------------------------------------------
    # TWO SERIES
    # ------------------------------------------------------------

    roi_chart.data = [
        investment_values,
        benefit_values
    ]

    # ------------------------------------------------------------
    # CATEGORY LABELS
    # ------------------------------------------------------------

    roi_chart.categoryAxis.categoryNames = (
        roi_chart_labels
    )

    # ------------------------------------------------------------
    # VALUE AXIS
    # ------------------------------------------------------------

    roi_chart.valueAxis.valueMin = 0

    max_value = max(
        max(investment_values, default=0),
        max(benefit_values, default=0),
        1
    )

    roi_chart.valueAxis.valueMax = (
        max_value * 1.2
    )
    
    roi_chart.valueAxis.valueStep = (
    max_value / 5
    )

    # ------------------------------------------------------------
    # BAR SETTINGS
    # ------------------------------------------------------------

    roi_chart.barWidth = 12
    roi_chart.groupSpacing = 12

    # ------------------------------------------------------------
    # CATEGORY LABEL SETTINGS
    # ------------------------------------------------------------

    roi_chart.categoryAxis.labels.fontName = (
        "NotoSans"
    )

    roi_chart.categoryAxis.labels.fontSize = 7

    roi_chart.categoryAxis.labels.boxAnchor = "e"

    # ------------------------------------------------------------
    # VALUE LABEL SETTINGS
    # ------------------------------------------------------------

    roi_chart.valueAxis.labels.fontName = (
        "NotoSans"
    )

    roi_chart.valueAxis.labels.fontSize = 7

    # ------------------------------------------------------------
    # ADD CHART
    # ------------------------------------------------------------

    roi_chart_drawing.add(
        roi_chart
    )

    story.append(
        Paragraph(
            "Estimated Investment vs Annual Benefit",
            styles["Heading3"]
        )
    )

    story.append(
        roi_chart_drawing
    )

    story.append(
        Spacer(1, 8)
    )

    # ------------------------------------------------------------
    # CHART LEGEND / EXPLANATION
    # ------------------------------------------------------------

    story.append(
        Paragraph(
            "Series 1: Estimated Investment | "
            "Series 2: Estimated Annual Benefit",
            normal_style
        )
    )

    story.append(
        Spacer(1, 20)
    )


# ============================================================
# KEY RECOMMENDATIONS
# ============================================================

    story.append(
        Paragraph(
            "Key Recommendations",
            heading_style
        )
    )

    recommendation_data = [
        ["Priority", "AI Opportunity", "Recommended Action"]
    ]

# Sort opportunities by score
    recommendation_df = scored_opportunities.sort_values(
        by="score",
        ascending=False
    )

    for _, row in recommendation_df.head(5).iterrows():

        priority = str(
            row.get("priority", "")
        )

        use_case = str(
            row.get("use_case", "")
        )

        technology = str(
            row.get("technology", "")
        )

        recommendation_data.append([
            priority,
            use_case,
            f"Evaluate {technology} implementation"
        ])

    recommendation_table = Table(
        recommendation_data,
        colWidths=[
            35 * mm,
            65 * mm,
            70 * mm
        ],
        repeatRows=1
    )

    recommendation_table.setStyle(
        TableStyle([

        # Header
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#1F4E78")
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "NotoSans-Bold"
            ),

        # Body
            (
                "FONTNAME",
                (0, 1),
                (-1, -1),
                "NotoSans"
            ),

        # Borders
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

        # Alignment
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),

        # Font
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                8
            ),

        # Padding
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
        ])
    )
 
    story.append(recommendation_table)
    story.append(Spacer(1, 20))


# ============================================================
# AI STRATEGY SUMMARY
# ============================================================

    story.append(
        Paragraph(
            "AI Strategy Summary",
            heading_style
        )
    )

    summary_text = (
        f"The assessment identified {total_opportunities} potential "
        f"AI opportunities for the business. "
        f"{high_priority} opportunities are classified as High or "
        f"Very High priority, while {medium_priority} are classified "
        f"as Medium priority and {low_priority} as Low priority."
    )

    story.append(
        Paragraph(
            summary_text,
            normal_style
        )
    )

    story.append(Spacer(1, 8))

    if total_investment > 0:

        financial_summary = (
            f"The estimated combined implementation investment is "
            f"₹{total_investment:,.0f}, with an estimated annual "
            f"business benefit of ₹{total_annual_benefit:,.0f}. "
            f"The resulting estimated overall ROI is "
            f"{overall_roi:.1f}%."
        )

        story.append(
            Paragraph(
                financial_summary,
                normal_style
            )
        )

    else:

        story.append(
            Paragraph(
                "Financial estimates are not available for the "
                "identified opportunities.",
                normal_style
            )
        )

    story.append(Spacer(1, 8))

    story.append(
        Paragraph(
            "The recommended strategy is to evaluate lower-complexity "
            "AI opportunities first, establish the required data and "
            "technology foundations, and then progress toward more "
            "advanced machine-learning and AI-agent initiatives.",
            normal_style
        )
    )

    story.append(Spacer(1, 20))
    story.append(PageBreak())

# BUSINESS PROFILE

    # ========================================================
    # BUSINESS PROFILE
    # ========================================================

    story.append(
        Paragraph(
            "1. Business Profile",
            heading_style
        )
    )

    # BUSINESS PROFILE SUMMARY

    company_name = business_profile.get(
        "company_name",
        "Not specified"
    )

    industry = business_profile.get(
        "industry",
        "Not specified"
    )

    employees = business_profile.get(
        "employees",
        "Not specified"
    )

    business_model = business_profile.get(
        "business_model",
        "Not specified"
    )

    budget = business_profile.get(
        "budget",
        "Not specified"
    )

    profile_summary_data = [
        ["Company", str(company_name)],
        ["Industry", str(industry)],
        ["Employees", str(employees)],
        ["Business Model", str(business_model)],
        ["AI Budget", str(budget)]
    ]

    profile_summary_table = Table(
        profile_summary_data,
        colWidths=[45 * mm, 125 * mm]
    )

    profile_summary_table.setStyle(
        TableStyle([

            ("BACKGROUND", (0, 0), (0, -1),
            colors.HexColor("#D9EAF7")),

            ("FONTNAME", (0, 0), (0, -1),
            "NotoSans-Bold"),

            ("FONTNAME", (1, 0), (1, -1),
            "NotoSans"),

            ("GRID", (0, 0), (-1, -1),
            0.5, colors.grey),

            ("VALIGN", (0, 0), (-1, -1),
            "MIDDLE"),

            ("FONTSIZE", (0, 0), (-1, -1),
            8),

            ("LEFTPADDING", (0, 0), (-1, -1),
            6),

            ("RIGHTPADDING", (0, 0), (-1, -1),
            6),

            ("TOPPADDING", (0, 0), (-1, -1),
            6),

            ("BOTTOMPADDING", (0, 0), (-1, -1),
            6),
        ])
    )

    story.append(profile_summary_table)
    story.append(Spacer(1, 15))

    profile_data = [
        ["Field", "Value"]
    ]

    for key, value in business_profile.items():

        if isinstance(value, list):
            value = ", ".join(
                str(item)
                for item in value
            )

        profile_data.append([
            str(key),
            str(value)
        ])

    profile_table = Table(
        profile_data,
        colWidths=[55 * mm, 115 * mm]
    )

    profile_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("FONTNAME", (0, 0), (-1, 0), "NotoSans-Bold"),
            ("FONTNAME", (0, 1), (-1, -1), "NotoSans"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ])
    )

    story.append(profile_table)

    story.append(Spacer(1, 15))
    story.append(PageBreak())


    # ========================================================
    # AI OPPORTUNITIES
    # ========================================================

    story.append(
        Paragraph(
            "2. AI Opportunity Matrix",
            heading_style
        )
    )

    opportunity_data = [
        [
            "Use Case",
            "Technology",
            "Impact",
            "Difficulty",
            "cost",
            "score",
            "Priority"
        ]
    ]

    for _, row in scored_opportunities.iterrows():

        opportunity_data.append([
            str(row.get("use_case", "")),
            str(row.get("technology", "")),
            str(row.get("business_impact", "")),
            str(row.get("implementation_difficulty", "")),
            str(row.get("cost_level", "")),
            str(row.get("score", "")),
            str(row.get("priority", ""))
        ])
    opportunity_table = Table(
        opportunity_data,
        colWidths=[
            42 * mm,   # Use Case
            28 * mm,   # Technology
            23 * mm,   # Impact
            23 * mm,   # Difficulty
            18 * mm,   # Cost
            15 * mm,   # Score
            21 * mm    # Priority
        ],
        repeatRows=1
    )

    opportunity_table.setStyle(
        TableStyle([
            (
            "BACKGROUND",
            (0, 0),
            (-1, 0),
            colors.HexColor("#1F4E78")
        ),
        (
            "TEXTCOLOR",
            (0, 0),
            (-1, 0),
            colors.white
        ),
        (
            "FONTNAME",
            (0, 0),
            (-1, 0),
            "NotoSans-Bold"
        ),

        # Table body
        (
            "FONTNAME",
            (0, 1),
            (-1, -1),
            "NotoSans"
        ),

        # Borders
        (
            "GRID",
            (0, 0),
            (-1, -1),
            0.5,
            colors.grey
        ),

        # Alignment
        (
            "VALIGN",
            (0, 0),
            (-1, -1),
            "TOP"
        ),

        # Font size
        (
            "FONTSIZE",
            (0, 0),
            (-1, -1),
            7
        ),

        (
            "LEADING", 
            (0, 0), 
            (-1, -1),
            9
        ),

        # Padding
        (
            "LEFTPADDING",
            (0, 0),
            (-1, -1),
            5
        ),
        (
            "RIGHTPADDING",
            (0, 0),
            (-1, -1),
            5
        ),
        (
            "TOPPADDING",
            (0, 0),
            (-1, -1),
            5
        ),
        (
            "BOTTOMPADDING",
            (0, 0),
            (-1, -1),
            5
        ),
    ])
)
            

    story.append(opportunity_table)

    story.append(PageBreak())

    # ========================================================
    # ROADMAP
    # ========================================================

    story.append(
        Paragraph(
            "3. AI Implementation Roadmap",
            heading_style
        )
    )

    # Phase descriptions
    phase_descriptions = {
        "Phase 1 - Quick AI Wins":
            "Focus on practical, lower-complexity opportunities that can demonstrate early business value.",

        "Phase 2 - AI Automation":
            "Expand AI adoption by automating repetitive business processes and knowledge-intensive workflows.",

        "Phase 3 - Advanced ML":
            "Introduce advanced machine-learning solutions that require stronger data, infrastructure and model development capabilities.",

        "Phase 4 - AI Agents":
            "Progress toward AI-agent capabilities that can coordinate tasks, workflows and business actions."
    }

# Timeline for each phase
    timeline_map = {
        "Phase 1 - Quick AI Wins": "0–2 months",
        "Phase 2 - AI Automation": "2–4 months",
        "Phase 3 - Advanced ML": "4–8 months",
        "Phase 4 - AI Agents": "8–12+ months"
    }

# --------------------------------------------------------
# Render every roadmap phase
# --------------------------------------------------------

    for phase_number, (phase, opportunities) in enumerate(
        roadmap.items(),
        start=1 
    ):

    # ----------------------------------------------------
    # Phase Header
    # ----------------------------------------------------

        phase_name = phase

        if " - " in phase:
            phase_name = phase.split(" - ", 1)[1]

        phase_header = f"Phase {phase_number} — {phase_name}"

        phase_table = Table(
            [[phase_header]],
            colWidths=[170 * mm]
        )

        phase_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor("#1F4E78")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, -1),
                    colors.white
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, -1),
                    "NotoSans-Bold"
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    11
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
            ])
        )

        story.append(phase_table)
        story.append(Spacer(1, 5))

    # ----------------------------------------------------
    # Phase Description
    # ----------------------------------------------------

        description = phase_descriptions.get(
            phase,
            "AI implementation phase."
        )

        story.append(
            Paragraph(
                description,
                normal_style
            )
        )

        story.append(Spacer(1, 7))

    # ----------------------------------------------------
    # Opportunities
    # ----------------------------------------------------

        if opportunities:

            roadmap_data = [
                [
                    "AI Opportunity",
                    "Implementation Focus",
                    "Estimated Timeline"
                ]
            ]

            for opportunity in opportunities:
 
                parts = str(opportunity).split(" — ", 1)

                if len(parts) == 2:

                    use_case = parts[0]
                    technology = parts[1]

                else:

                    use_case = str(opportunity)
                    technology = ""

                roadmap_data.append([
                    use_case,
                    technology,
                    timeline_map.get(
                        phase,
                        "To be determined"
                    )
                ])

            roadmap_table = Table(
                roadmap_data,
                colWidths=[
                    75 * mm,
                    55 * mm,
                    40 * mm
                ],
                repeatRows=1
            )

            roadmap_table.setStyle(
                TableStyle([

                # Header
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.black
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "NotoSans-Bold"
                    ),

                # Body
                    (
                        "FONTNAME",
                        (0, 1),
                        (-1, -1),
                        "NotoSans"
                    ),

                # Timeline
                    (
                        "FONTNAME",
                        (2, 1),
                        (2, -1),
                        "NotoSans-Bold"
                    ),
                    (
                        "ALIGN",
                        (2, 1),
                        (2, -1),
                        "CENTER"
                    ),

                # Borders
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey
                    ),

                # Vertical alignment
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP"
                    ),

                # Font size
                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        8
                    ),

                # Padding
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        6
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        6
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        6
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        6
                    ),
                ])
            )

            story.append(roadmap_table)

        else:

            story.append(
                Paragraph(
                    "No opportunities assigned to this phase.",
                    normal_style
                )
            )

        story.append(Spacer(1, 12))


# --------------------------------------------------------
# End of Roadmap
# --------------------------------------------------------

    story.append(PageBreak())

    

    # ========================================================
    # IMPLEMENTATION PLAN
    # ========================================================

    story.append(
        Paragraph(
            "4. Detailed Implementation Plan",
            heading_style
        )
    )

# --------------------------------------------------------
# Helper function for displaying values
# --------------------------------------------------------

    def format_implementation_value(value):

        if isinstance(value, list):
            return ", ".join(str(v) for v in value)

        if isinstance(value, dict):
            return ", ".join(
                f"{k}: {v}"
                for k, v in value.items()
            )

        return str(value)


# --------------------------------------------------------
# Helper function to create implementation table
# --------------------------------------------------------

    def add_implementation_section(use_case, details):

    # Use Case Header
        use_case_table = Table(
            [[str(use_case)]],
            colWidths=[170 * mm]
        )

        use_case_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor("#1F4E78")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, -1),
                    colors.white
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, -1),
                    "NotoSans-Bold"
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    10
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
            ])
        )

        story.append(use_case_table)
        story.append(Spacer(1, 5))

    # ----------------------------------------------------
    # Details
    # ----------------------------------------------------

        if isinstance(details, dict):

            implementation_data = [
                ["Parameter", "Details"]
            ]

        # Preferred display order
            field_order = [
                ("technology", "Technology"),
                ("score", "Score"),
                ("priority", "Priority"),
                ("timeline", "Timeline"),
                ("estimated_cost", "Estimated Cost"),
                ("cost", "Estimated Cost"),
                ("team", "Required Team"),
                ("required_team", "Required Team"),
                ("impact", "Expected Impact"),
                ("expected_impact", "Expected Impact"),
            ]

            processed_keys = set()

            for key, label in field_order:

                if key in details:

                    value = format_implementation_value(
                        details[key]
                    )

                    implementation_data.append([
                        label,
                        value
                    ])

                    processed_keys.add(key)

        # Add any remaining fields
            for key, value in details.items():

                if key in processed_keys:
                    continue

                implementation_data.append([
                    str(key).replace("_", " ").title(),
                    format_implementation_value(value)
                ])

            implementation_table = Table(
                implementation_data,
                colWidths=[55 * mm, 115 * mm],
                repeatRows=1
            )

            implementation_table.setStyle(
                TableStyle([
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.black
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "NotoSans-Bold"
                    ),
                    (
                        "FONTNAME",
                        (0, 1),
                        (0, -1),
                        "NotoSans-Bold"
                    ),
                    (
                        "FONTNAME",
                        (1, 1),
                        (-1, -1),
                        "NotoSans"
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP"
                    ),
                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        8
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        6
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        6
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        6
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        6
                    ),
                ])
            )

            story.append(implementation_table)
            story.append(Spacer(1, 8))
            story.append(PageBreak())

        else:

            story.append(
                Paragraph(
                    format_implementation_value(details),
                    normal_style
                )
            )

            story.append(Spacer(1, 8))


# --------------------------------------------------------
# Handle implementation plan
# --------------------------------------------------------

    if isinstance(implementation_plan, dict):

        for use_case, details in implementation_plan.items():

            add_implementation_section(
                use_case,
                details
            )


    elif isinstance(implementation_plan, list):

        for item in implementation_plan:

            if isinstance(item, dict):

                use_case = item.get(
                    "use_case",
                    item.get(
                        "Use Case",
                        "Implementation"
                    )
                )

                details = {}

                for key, value in item.items():

                    if key in [
                        "use_case",
                        "Use Case"
                    ]:
                        continue

                    details[key] = value

                add_implementation_section(
                    use_case,
                    details
                )

            else:

                story.append(
                    Paragraph(
                        str(item),
                        normal_style
                    )
                )

                story.append(Spacer(1, 8))


    else:

        story.append(
            Paragraph(
                "No implementation plan available.",
                normal_style
            )
        )


        story.append(PageBreak())
        


    # ========================================================
    # ROI ANALYSIS
    # ========================================================

    story.append(
        Paragraph(
            "5. AI Cost & ROI Analysis",
            heading_style
        )
    )

    # ============================================================
    # PAYBACK SUMMARY
    # ============================================================

    payback_values = []

    if not roi_analysis.empty:

        for value in roi_analysis["payback_months"]:

            if pd.notna(value):
                payback_values.append(float(value))

    if payback_values:
        
        average_payback = sum(payback_values) / len(payback_values)

        payback_summary_data = [
            ["Financial Metric", "Estimated Value"],
            [
                "Average Payback Period",
                f"{average_payback:.1f} months"
            ],
            [
                "Fastest Payback",
                f"{min(payback_values):.1f} months"
            ],
            [
                "Longest Payback",
                f"{max(payback_values):.1f} months"
            ]
        ]

        payback_table = Table(
            payback_summary_data,
            colWidths=[85 * mm, 85 * mm],
            repeatRows=1
        )

        payback_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0),
                colors.HexColor("#1F4E78")),

                ("TEXTCOLOR", (0, 0), (-1, 0),
                colors.white),

                ("FONTNAME", (0, 0), (-1, 0),
                "NotoSans-Bold"),

                ("FONTNAME", (0, 1), (0, -1),
                "NotoSans-Bold"),

                ("GRID", (0, 0), (-1, -1),
                0.5, colors.grey),

                ("VALIGN", (0, 0), (-1, -1),
                "MIDDLE"),

                ("FONTSIZE", (0, 0), (-1, -1),
                9),

                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ])
        )

        story.append(
            Paragraph(
                "Estimated Payback Summary",
                styles["Heading3"]
            )
        )

        story.append(payback_table)
        story.append(Spacer(1, 15))

    # ============================================================
    # ROI SUMMARY
    # ============================================================

    roi_summary_data = [
        ["Financial Metric", "Estimated Value"],
        [
            "Total Investment",
            f"₹{total_investment:,.0f}"
        ],
        [
            "Total Annual Benefit",
            f"₹{total_annual_benefit:,.0f}"
        ],
        [
            "Estimated Overall ROI",
            f"{overall_roi:.1f}%"
        ]
    ]

    roi_summary_table = Table(
        roi_summary_data,
        colWidths=[85 * mm, 85 * mm],
        repeatRows=1
    )

    roi_summary_table.setStyle(
        TableStyle([
            # Header
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#1F4E78")
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "NotoSans-Bold"
            ),

            # Metric names
            (
                "FONTNAME",
                (0, 1),
                (0, -1),
                "NotoSans-Bold"
            ),
            
            # Estimated values
            (
                "FONTNAME",
                (1, 1),
                (1, -1),
                "NotoSans"
            ),

            # Borders
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                9
            ),

            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                7
            ),

            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                7
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
        ])
    )

    story.append(roi_summary_table)
    story.append(Spacer(1, 15))

    roi_data = [
        [
            "Use Case",
            "Cost",
            "Benefit",
            "ROI",
            "Payback",
            "Budget Status"
        ]
    ]

    for _, row in roi_analysis.iterrows():

        roi_data.append([
            str(row.get("use_case", "")),
            f"₹{row.get('implementation_cost', 0):,.0f}",
            f"₹{row.get('annual_benefit', 0):,.0f}",
            f"{row.get('roi_percent', 0)}%",
            (
                f"{row.get('payback_months')} months"
                if pd.notna(row.get("payback_months"))
                else "N/A"
            ),
            str(row.get("budget_status", "Not available"))
            
        ])

    roi_table = Table(
        roi_data,
        colWidths=[
            40 * mm,
            25 * mm,
            28 * mm,
            20 * mm,
            25 * mm,
            32 * mm
        ],

        repeatRows=1
    )

    roi_table.setStyle(
        TableStyle([
            (
            "BACKGROUND",
            (0, 0),
            (-1, 0),
            colors.HexColor("#1F4E78")
        ),
        (
            "TEXTCOLOR",
            (0, 0),
            (-1, 0),
            colors.white
        ),
        (
            "FONTNAME",
            (0, 0),
            (-1, 0),
            "NotoSans-Bold"
        ),

        # Table body
        (
            "FONTNAME",
            (0, 1),
            (-1, -1),
            "NotoSans"
        ),

        # Budget Status column
        (
            "FONTNAME",
            (5, 1),
            (5, -1),
            "NotoSans-Bold"
        ),

        (
            "FONTSIZE",
            (5, 0),
            (5, -1),
            7
        ),


        # Borders
        (
            "GRID",
            (0, 0),
            (-1, -1),
            0.5,
            colors.grey
        ),

        # Alignment
        (
            "VALIGN",
            (0, 0),
            (-1, -1),
            "TOP"
        ),

        # Font size
        (
            "FONTSIZE",
            (0, 0),
            (-1, -1),
            7
        ),

        # Padding
        (
            "LEFTPADDING",
            (0, 0),
            (-1, -1),
            5
        ),
        (
            "RIGHTPADDING",
            (0, 0),
            (-1, -1),
            5
        ),
        (
            "TOPPADDING",
            (0, 0),
            (-1, -1),
            5
        ),
        (
            "BOTTOMPADDING",
            (0, 0),
            (-1, -1),
            5
        ),
    ])
)
            

    story.append(roi_table)

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "Note: ROI and cost figures are estimates based on "
            "the assumptions provided in the business profile. "
            "They should be validated with actual business and "
            "implementation data before making investment decisions.",
            normal_style
        )
    )

    # ============================================================
    # FINAL STRATEGIC CONCLUSION
    # ============================================================

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "6. Strategic Conclusion",
            heading_style
        )
    )

    conclusion_text = (
        "The AI strategy assessment provides a structured view of "
        "potential AI opportunities across the business. The "
        "identified opportunities should be evaluated according to "
        "business impact, implementation complexity, available "
        "data, technology readiness, budget, and expected value."
    )

    story.append(
        Paragraph(
            conclusion_text,
            normal_style
        )
    )

    story.append(Spacer(1, 8))

    roadmap_text = (
        "The implementation roadmap provides a phased approach, "
        "beginning with practical AI opportunities and progressing "
        "toward more advanced machine-learning and AI-agent "
        "initiatives as the organization's capabilities mature."
    )

    story.append(
        Paragraph(
            roadmap_text,
            normal_style
        )
    )

    story.append(Spacer(1, 8))

    validation_text = (
        "All cost, benefit, ROI, and payback figures in this report "
        "are estimates generated from the business profile and "
        "project assumptions. Actual results may vary and should "
        "be validated using business-specific financial, technical, "
        "and operational data before implementation."
    )

    story.append(
        Paragraph(
            validation_text,
            normal_style
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "End of Report",
            ParagraphStyle(
                "EndReport",
                parent=normal_style,
                fontName="NotoSans",
                alignment=TA_CENTER,
                fontSize=9,
                leading=14
            )
        )
    )




    # ========================================================
    # BUILD PDF
    # ========================================================
    
    document.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number
    )

    return file_path