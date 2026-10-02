
"""HTTP client for communicating with the FastAPI backend."""

import logging
import os
from typing import Any

import requests


logger = logging.getLogger(__name__)


class APIClient:
    """Client for the Communication Coach FastAPI API."""

    def __init__(
        self,
        base_url: str | None = None,
        timeout: int = 30,
    ) -> None:
        """Initialize the API client.

        Args:
            base_url: Base URL of the FastAPI backend.
            timeout: HTTP request timeout in seconds.
        """
        self.base_url = (
            base_url
            or os.getenv("API_BASE_URL", "http://localhost:8000")
        ).rstrip("/")

        self.timeout = timeout

    def _post(
        self,
        endpoint: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """Send a POST request to the API."""

        url = f"{self.base_url}{endpoint}"

        try:
            logger.info("Sending POST request | endpoint=%s", endpoint)

            response = requests.post(
                url,
                json=payload,
                timeout=self.timeout,
            )

            response.raise_for_status()

            logger.info(
                "POST request successful | endpoint=%s | status=%s",
                endpoint,
                response.status_code,
            )

            return response.json()

        except requests.exceptions.Timeout as exc:
            logger.error(
                "API request timed out | endpoint=%s",
                endpoint,
            )
            raise RuntimeError(
                "The communication coach took too long to respond."
            ) from exc

        except requests.exceptions.ConnectionError as exc:
            logger.error(
                "Unable to connect to API | endpoint=%s",
                endpoint,
            )
            raise RuntimeError(
                "Unable to connect to the Communication Coach API."
            ) from exc

        except requests.exceptions.HTTPError as exc:
            logger.error(
                "API returned HTTP error | endpoint=%s | status=%s",
                endpoint,
                response.status_code,
            )
            raise RuntimeError(
                f"API request failed with status {response.status_code}."
            ) from exc

        except requests.exceptions.RequestException as exc:
            logger.exception(
                "Unexpected API request error | endpoint=%s",
                endpoint,
            )
            raise RuntimeError(
                "An unexpected error occurred while contacting the API."
            ) from exc

        except ValueError as exc:
            logger.error(
                "Invalid JSON response | endpoint=%s",
                endpoint,
            )
            raise RuntimeError(
                "The API returned an invalid response."
            ) from exc

    def analyze(
        self,
        message: str,
        context: str | None = None,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        """Analyze a communication message."""

        return self._post(
            "/api/v1/analyze",
            {
                "message": message,
                "context": context,
                "session_id": session_id,
            },
        )

    def coach(
        self,
        message: str,
        context: str | None = None,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        """Generate a communication coaching response."""

        return self._post(
            "/api/v1/coach",
            {
                "message": message,
                "context": context,
                "session_id": session_id,
            },
        )

    def improve(
        self,
        message: str,
        context: str | None = None,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        """Generate an improved communication response."""

        return self._post(
            "/api/v1/improve",
            {
                "message": message,
                "context": context,
                "session_id": session_id,
            },
        )

    def get_chat_history(
        self,
        session_id: str,
    ) -> dict[str, Any]:
        """Retrieve conversation history for a session."""

        url = (
            f"{self.base_url}"
            f"/api/v1/chat-history/{session_id}"
        )

        try:
            logger.info(
                "Fetching chat history | session_id=%s",
                session_id,
            )

            response = requests.get(
                url,
                timeout=self.timeout,
            )

            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as exc:
            logger.exception(
                "Failed to retrieve chat history | session_id=%s",
                session_id,
            )
            raise RuntimeError(
                "Unable to retrieve conversation history."
            ) from exc

    def health_check(self) -> dict[str, Any]:
        """Check whether the FastAPI backend is available."""

        url = f"{self.base_url}/health"

        try:
            logger.info("Checking API health")

            response = requests.get(
                url,
                timeout=self.timeout,
            )

            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as exc:
            logger.exception("API health check failed")
            raise RuntimeError(
                "Communication Coach API is unavailable."
            ) from exc
