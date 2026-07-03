import json

from app.llm.gemini_client import GeminiClient
from app.models.action import AgentAction
from app.prompts.compare_prompt import build_compare_prompt
from app.prompts.recommend_prompt import build_recommend_prompt
from app.prompts.refine_prompt import build_refine_prompt
from app.retrieval.retriever import Retriever
from app.services.conversation_analyzer import ConversationAnalyzer
from app.utils.query_builder import QueryBuilder


class ChatService:

    def __init__(self):
        
        print("Initializing ChatService")
        self.analyzer = ConversationAnalyzer()
        print("ConversationAnalyzer OK")
        
        # Lazy load Retriever
        self.retriever = None

        print("Retriever placeholder OK")

        self.llm = GeminiClient()
        
        print("GeminiClient OK")

    def _generate_json_response(self, prompt):
        """
        Generate a response from Gemini and safely parse JSON.
        """

        try:

            response = self.llm.generate(prompt)

        except Exception as e:

            print(f"[Gemini Error] {e}")

            return {
                "reply": (
                    "The recommendation service is temporarily unavailable. "
                    "Please try again in a few moments."
                ),
                "recommendations": [],
                "end_of_conversation": False,
            }

        response = (
            response
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        try:

            return json.loads(response)

        except Exception:

            return {
                "reply": response,
                "recommendations": [],
                "end_of_conversation": False,
            }

    def chat(self, messages):

        # ---------------------------------------
        # Lazy initialize Retriever
        # ---------------------------------------

        if self.retriever is None:

            print("Loading Retriever...")

            self.retriever = Retriever()

        # ---------------------------------------
        # Analyze conversation
        # ---------------------------------------

        action = self.analyzer.analyze(messages)
        state = self.analyzer.build_state(messages)

        # ---------------------------------------
        # Clarification
        # ---------------------------------------

        if action == AgentAction.CLARIFY:

            return {
                "reply": (
                    "Could you tell me more about the role, "
                    "seniority level, or the skills you're hiring for?"
                ),
                "recommendations": [],
                "end_of_conversation": False,
            }

        # ---------------------------------------
        # Refusal
        # ---------------------------------------

        if action == AgentAction.REFUSE:

            return {
                "reply": (
                    "I can only assist with SHL assessment "
                    "selection, refinement, and comparison."
                ),
                "recommendations": [],
                "end_of_conversation": False,
            }

        # ---------------------------------------
        # Build retrieval query
        # ---------------------------------------

        query = QueryBuilder.build(
            messages,
            state,
        )

        # ---------------------------------------
        # Recommendation
        # ---------------------------------------

        if action == AgentAction.RECOMMEND:

            retrieved = self.retriever.search(
                query=query,
                top_k=5,
            )

            prompt = build_recommend_prompt(
                messages,
                retrieved,
            )

            return self._generate_json_response(prompt)

        # ---------------------------------------
        # Refinement
        # ---------------------------------------

        if action == AgentAction.REFINE:

            retrieved = self.retriever.search(
                query=query,
                top_k=8,
            )

            prompt = build_refine_prompt(
                messages,
                retrieved,
            )

            return self._generate_json_response(prompt)

        # ---------------------------------------
        # Comparison
        # ---------------------------------------

        if action == AgentAction.COMPARE:

            retrieved = self.retriever.search(
                query=query,
                top_k=6,
            )

            prompt = build_compare_prompt(
                messages,
                retrieved,
            )

            return self._generate_json_response(prompt)

        # ---------------------------------------
        # Fallback
        # ---------------------------------------

        return {
            "reply": (
                "I'm not sure how to help with that request. "
                "I can recommend, refine, or compare SHL assessments."
            ),
            "recommendations": [],
            "end_of_conversation": False,
        }