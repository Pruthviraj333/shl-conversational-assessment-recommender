from app.models.conversation_state import ConversationState


class QueryBuilder:

    @staticmethod
    def build(messages, state: ConversationState):

        parts = []

        # ----------------------------
        # Original request
        # ----------------------------

        first_user = next(
            (
                m["content"]
                for m in messages
                if m["role"] == "user"
            ),
            "",
        )

        if first_user:
            parts.append(first_user)

        # ----------------------------
        # Role
        # ----------------------------

        if state.role:
            parts.append(f"Role: {state.role}")

        # ----------------------------
        # Domain
        # ----------------------------

        if state.domain:
            parts.append(f"Domain: {state.domain}")

        # ----------------------------
        # Seniority
        # ----------------------------

        if state.seniority:
            parts.append(f"Seniority: {state.seniority}")

        # ----------------------------
        # Job Description
        # ----------------------------

        if state.job_description:
            parts.append("Job Description Provided")

        # ----------------------------
        # Entire conversation history
        # ----------------------------

        history = " ".join(
            m["content"].lower()
            for m in messages
            if m["role"] == "user"
        )

        # ----------------------------
        # Important hiring keywords
        # ----------------------------

        keywords = [

            # Assessment types
            "personality",
            "behavioral",
            "behavioural",
            "cognitive",
            "ability",
            "aptitude",
            "simulation",
            "coding",
            "technical",
            "leadership",
            "safety",
            "sales",
            "language",

            # Hiring context
            "graduate",
            "entry level",
            "experienced",

            # Customer service
            "customer service",
            "contact centre",
            "contact center",

            # Software
            "java",
            "python",
            "rust",
            "linux",
            "cloud",

            # Finance
            "finance",
            "financial",
            "accounting",

            # Healthcare
            "healthcare",
            "medical",
            "hipaa",

            # Manufacturing
            "manufacturing",
            "industrial",
            "plant",

            # Geography / language
            "english",
            "us",
            "uk",
            "india",

        ]

        seen = set()

        for word in keywords:

            if word in history and word not in seen:

                parts.append(word)
                seen.add(word)

        return "\n".join(parts)