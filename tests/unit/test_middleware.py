from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.middleware import RequestLoggingMiddleware


def create_test_app() -> FastAPI:
    """Create a minimal FastAPI application for middleware testing."""
    test_app = FastAPI()

    test_app.add_middleware(RequestLoggingMiddleware)

    @test_app.get("/test")
    def test_endpoint():
        return {"message": "success"}

    return test_app


def test_request_logging_middleware() -> None:
    """Test request ID generation and response header."""
    test_app = create_test_app()
    client = TestClient(test_app)

    response = client.get("/test")

    assert response.status_code == 200
    assert response.json() == {"message": "success"}

    request_id = response.headers.get("X-Request-ID")

    assert request_id is not None
    assert len(request_id) == 36