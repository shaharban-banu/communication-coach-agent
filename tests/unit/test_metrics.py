from app.core.metrics import Metrics


def test_metrics_record_successful_request() -> None:
    metrics = Metrics()

    metrics.record_request(
        response_time=2.0,
        success=True,
    )

    result = metrics.get_metrics()

    assert result["total_requests"] == 1
    assert result["successful_requests"] == 1
    assert result["failed_requests"] == 0
    assert result["error_rate"] == 0.0
    assert result["average_response_time"] == 2.0


def test_metrics_record_failed_request() -> None:
    metrics = Metrics()

    metrics.record_request(
        response_time=4.0,
        success=False,
    )

    result = metrics.get_metrics()

    assert result["total_requests"] == 1
    assert result["successful_requests"] == 0
    assert result["failed_requests"] == 1
    assert result["error_rate"] == 100.0
    assert result["average_response_time"] == 4.0


def test_metrics_calculate_average_and_error_rate() -> None:
    metrics = Metrics()

    metrics.record_request(2.0, True)
    metrics.record_request(4.0, True)
    metrics.record_request(6.0, False)

    result = metrics.get_metrics()

    assert result["total_requests"] == 3
    assert result["successful_requests"] == 2
    assert result["failed_requests"] == 1
    assert result["error_rate"] == 33.33
    assert result["average_response_time"] == 4.0