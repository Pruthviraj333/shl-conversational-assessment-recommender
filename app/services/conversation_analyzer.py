from app.models.action import AgentAction
from app.models.conversation_state import ConversationState


class ConversationAnalyzer:

    ROLE_WORDS = [

    "developer",
    "engineer",
    "software engineer",

    "manager",
    "director",
    "executive",
    "cxo",

    "analyst",

    "operator",

    "assistant",
    "administrator",

    "intern",
    "trainee",
    ]

    DOMAINS = {

    # Software

    "java": "software",

    "python": "software",

    "rust": "software",

    "linux": "software",

    "network": "software",

    "cloud": "software",

    # Finance

    "finance": "finance",

    "financial": "finance",

    "accounting": "finance",

    # Sales

    "sales": "sales",

    # Customer Service

    "contact centre": "customer service",

    "contact center": "customer service",

    "customer service": "customer service",

    "call center": "customer service",

    "call centre": "customer service",

    # Manufacturing

    "plant": "manufacturing",

    "industrial": "manufacturing",

    "chemical": "manufacturing",

    # Healthcare

    "healthcare": "healthcare",

    "medical": "healthcare",

    "hipaa": "healthcare",
    }

    SENIORITY = [
        "entry",
        "junior",
        "mid",
        "senior",
        "lead",
        "principal",
        "graduate",
        "experienced",
        "entry level",
        "15 years",
        "10 years",
        "5 years",
    ]

    COMPARE = [
        "difference",
        "compare",
        "vs",
        "versus",
    ]

    REFINE = [
        "actually",
        "add",
        "remove",
        "replace",
        "drop",
        "instead",
        "also",
        "keep",
    ]

    REFUSE = [
        "ignore previous",
        "system prompt",
        "religion",
        "politics",
        "visa",
        "salary",
        "legal",
    ]

    def build_state(self, messages):

        state = ConversationState()

        full_text = " ".join(
            m["content"].lower()
            for m in messages
            if m["role"] == "user"
        )

        state.latest_message = messages[-1]["content"].lower()

        #
        # role
        #

        for role in self.ROLE_WORDS:

            if role in full_text:

                state.role = role

                break
        
        #
        #domain
        #
        for keyword, domain in self.DOMAINS.items():

            if keyword in full_text:

             state.domain = domain

             break


        #
        # seniority
        #

        for level in self.SENIORITY:

            if level in full_text:

                state.seniority = level

                break

        #
        # JD
        #

        if "job description" in full_text:

            state.job_description = True

        #
        # intents
        #

        state.wants_comparison = any(
            x in state.latest_message
            for x in self.COMPARE
        )

        state.wants_refinement = any(
            x in state.latest_message
            for x in self.REFINE
        )

        state.off_topic = any(
            x in state.latest_message
            for x in self.REFUSE
        )

        #
        # recommendation intent
        #

        hiring_words = [

          "hire",
          "hiring",
          "assessment",
          "assessments",
          "screen",
          "screening",
          "candidate",
          "recruit",
          "recommend",
          "recommendation",
          "solution",
          "battery",
          "talent",
          "development",
          "reskill",
          "upskill",
          "evaluate",
          "evaluation",
          "selection",
          "identify",

            ]

        state.wants_recommendation = any(
            x in full_text
            for x in hiring_words
        )

        return state
    
    def analyze(self, messages):

        state = self.build_state(messages)

        if state.off_topic:

            return AgentAction.REFUSE

        if state.wants_comparison:

            return AgentAction.COMPARE

        if state.wants_refinement:

            return AgentAction.REFINE

        #
        # Recommendation only if enough context
        #

        if state.wants_recommendation:

            enough_context = any(
                [
                    state.role,
                    state.domain,
                    state.job_description,
                    state.seniority,
                ]
            )

            if enough_context:

                return AgentAction.RECOMMEND

            return AgentAction.CLARIFY

        return AgentAction.CLARIFY