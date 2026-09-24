"""
Gemini API client with retry logic, timeout, and structured output support.
Never call this directly from route handlers — use the agent layer.
"""
import asyncio
import json
import re
from typing import Any, Optional

import httpx
from tenacity import (
    AsyncRetrying,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.core.config import settings
from app.core.exceptions import AIServiceException
from app.core.logging import get_logger

logger = get_logger(__name__)

_GEMINI_GENERATE_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "{model}:generateContent?key={api_key}"
)


class GeminiClient:
    """
    Async HTTP client for the Gemini API.

    Usage::

        client = GeminiClient()
        text = await client.generate_text("Explain gravity")
        data = await client.generate_json("Return JSON with key 'result'")
    """

    def __init__(self) -> None:
        self._model = settings.GEMINI_MODEL
        self._timeout = settings.GEMINI_TIMEOUT_SECONDS
        self._max_retries = settings.GEMINI_MAX_RETRIES

    def _build_url(self) -> str:
        # API key is injected at call time, not stored in the URL template
        return _GEMINI_GENERATE_URL.format(
            model=self._model,
            api_key=settings.GEMINI_API_KEY,
        )

    def _build_payload(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_output_tokens: int = 8192,
    ) -> dict[str, Any]:
        contents: list[dict[str, Any]] = [
            {"role": "user", "parts": [{"text": prompt}]}
        ]
        payload: dict[str, Any] = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_output_tokens,
                "topP": 0.95,
            },
        }
        if system_prompt:
            payload["systemInstruction"] = {"parts": [{"text": system_prompt}]}
        return payload

    def _extract_text(self, response_data: dict[str, Any]) -> str:
        try:
            candidates = response_data["candidates"]
            if not candidates:
                raise AIServiceException("Gemini returned no candidates")
            parts = candidates[0]["content"]["parts"]
            return "".join(p.get("text", "") for p in parts).strip()
        except (KeyError, IndexError) as e:
            raise AIServiceException(f"Unexpected Gemini response structure: {e}")

    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_output_tokens: int = 8192,
    ) -> str:
        """Generate a text response from Gemini."""
        payload = self._build_payload(prompt, system_prompt, temperature, max_output_tokens)

        try:
            async for attempt in AsyncRetrying(
                stop=stop_after_attempt(self._max_retries),
                wait=wait_exponential(multiplier=1, min=2, max=10),
                retry=retry_if_exception_type(
                    (httpx.TimeoutException, httpx.NetworkError)
                ),
                reraise=True,
            ):
                with attempt:
                    async with httpx.AsyncClient(
                        timeout=self._timeout
                    ) as client:
                        response = await client.post(
                            self._build_url(), json=payload
                        )

            if response.status_code == 429:
                raise AIServiceException(
                    "Gemini rate limit exceeded. Please try again later."
                )
            if response.status_code != 200:
                logger.warning(
                    "Gemini API error",
                    status_code=response.status_code,
                )
                raise AIServiceException(
                    f"Gemini API returned status {response.status_code}"
                )

            return self._extract_text(response.json())

        except AIServiceException:
            raise
        except httpx.TimeoutException:
            logger.error("Gemini API timeout")
            raise AIServiceException("AI service timed out. Please try again.")
        except httpx.NetworkError as e:
            logger.error("Gemini network error", error=str(e))
            raise AIServiceException("Network error connecting to AI service")

    async def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.3,
    ) -> dict[str, Any]:
        """
        Generate a structured JSON response from Gemini.
        Extracts JSON from the response text, even if surrounded by markdown.
        """
        text = await self.generate_text(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            max_output_tokens=16384,
        )

        # Strip markdown code fences if present
        json_text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.MULTILINE)
        json_text = re.sub(r"\s*```$", "", json_text, flags=re.MULTILINE)
        json_text = json_text.strip()

        try:
            return json.loads(json_text)
        except json.JSONDecodeError as e:
            logger.warning(
                "Gemini returned invalid JSON",
                error=str(e),
                response_preview=json_text[:200],
            )
            raise AIServiceException("AI returned malformed JSON output")


# Singleton client instance
gemini_client = GeminiClient()
