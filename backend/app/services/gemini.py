import httpx

from app.core.config import settings


class GeminiError(Exception):
    """Raised when communication with Gemini fails."""


class GeminiClient:
    def __init__(self):
        self.api_key = settings.gemini_api_key
        self.model = "gemini-2.5-flash"

    async def generate(
        self,
        prompt: str,
        system_instruction: str | None = None,
    ) -> str:
        if not self.api_key:
            raise GeminiError("Gemini API key is not configured.")

        url = (
            "https://generativelanguage.googleapis.com"
            f"/v1beta/models/{self.model}:generateContent"
            f"?key={self.api_key}"
        )

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt,
                        }
                    ]
                }
            ]
        }

        if system_instruction:
            payload["systemInstruction"] = {
                "parts": [
                    {
                        "text": system_instruction,
                    }
                ]
            }

        try:
            async with httpx.AsyncClient(timeout=45) as client:
                response = await client.post(
                    url,
                    json=payload,
                )

            response.raise_for_status()

        except httpx.HTTPStatusError as exc:
            raise GeminiError(
                f"Gemini API returned HTTP {exc.response.status_code}."
            ) from exc

        except httpx.RequestError as exc:
            raise GeminiError(
                "Gemini API request failed."
            ) from exc

        try:
            data = response.json()
        except ValueError as exc:
            raise GeminiError(
                "Gemini returned invalid JSON."
            ) from exc

        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]

        except (KeyError, IndexError, TypeError) as exc:
            raise GeminiError(
                "Gemini returned an unexpected response."
            ) from exc