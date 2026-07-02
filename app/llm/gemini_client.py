import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiClient:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found.")

        self.client = genai.Client(api_key=api_key)

        # Model used throughout the project
        self.model = "gemini-2.5-flash"

    def generate(self, prompt: str) -> str:

        max_retries = 3

        for attempt in range(max_retries):

            try:

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                )

                return response.text

            except Exception as e:

                error = str(e)

                # Retry on temporary server overload
                if (
                    "503" in error
                    or "UNAVAILABLE" in error
                ):

                    print(
                        f"[Gemini] Server busy. Retry {attempt + 1}/{max_retries}..."
                    )

                    time.sleep(5)

                    continue

                # Quota exceeded
                if (
                    "429" in error
                    or "RESOURCE_EXHAUSTED" in error
                ):

                    raise RuntimeError(
                        "Gemini API quota exceeded. Please try again later or use another API key."
                    )

                # Unknown error
                raise

        raise RuntimeError(
            "Gemini service unavailable after multiple retries."
        )