def create_roadmap(scored_opportunities):

    roadmap = {
        "Phase 1 - Quick AI Wins": [],
        "Phase 2 - AI Automation": [],
        "Phase 3 - Advanced ML": [],
        "Phase 4 - AI Agents": []
    }

    for _, row in scored_opportunities.iterrows():

        use_case = str(
            row.get("use_case", "")
        )

        technology = str(
            row.get("technology", "")
        )

        difficulty = str(
            row.get("implementation_difficulty", "")
        )

        score = float(
            row.get("score", 0)
        )


        # ==============================================
        # PHASE 1 — QUICK AI WINS
        # ==============================================

        if (
            difficulty == "Low"
            and score >= 4
        ):

            roadmap[
                "Phase 1 - Quick AI Wins"
            ].append(
                f"{use_case} — {technology}"
            )


        # ==============================================
        # PHASE 2 — AI AUTOMATION
        # ==============================================

        elif (
            technology in [
                "Generative AI",
                "LLM",
                "LLM + RAG",
                "Data Analytics"
            ]
            and score >= 3
        ):

            roadmap[
                "Phase 2 - AI Automation"
            ].append(
                f"{use_case} — {technology}"
            )


        # ==============================================
        # PHASE 3 — ADVANCED ML
        # ==============================================

        elif (
            technology == "Machine Learning"
            and score >= 3
        ):

            roadmap[
                "Phase 3 - Advanced ML"
            ].append(
                f"{use_case} — {technology}"
            )


        # ==============================================
        # PHASE 4 — AI AGENTS
        # ==============================================

        elif (
            "agent" in use_case.lower()
            or "agent" in technology.lower()
        ):

            roadmap[
                "Phase 4 - AI Agents"
            ].append(
                f"{use_case} — {technology}"
            )


    return roadmap