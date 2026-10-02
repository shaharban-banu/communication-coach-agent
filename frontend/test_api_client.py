"""Manual test for the frontend API client."""

from frontend.api_client import APIClient


def test_api_health():
    """Verify that the backend health endpoint is accessible."""

    client = APIClient()

    result = client.health_check()

    print("Backend health response:", result)

    assert result is not None
    assert isinstance(result, dict)


if __name__ == "__main__":
    test_api_health()