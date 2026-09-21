"""
Application metrics collection.

This module provides lightweight in-memory metrics for tracking
API usage, successful requests, failed requests, and response time.
"""

from dataclasses import dataclass


@dataclass
class Metrics:
    """
    Store application-level API metrics.
    """

    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_response_time: float = 0.0

    def record_request(
        self,
        response_time: float,
        success: bool,
    ) -> None:
        """
        Record the result of an API request.

        Args:
            response_time: Request processing time in seconds.
            success: Whether the request completed successfully.
        """
        self.total_requests += 1
        self.total_response_time += response_time

        if success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1

    def get_metrics(self) -> dict[str, float | int]:
        """
        Return the current application metrics.

        Returns:
            Dictionary containing request and performance metrics.
        """
        average_response_time = (
            self.total_response_time / self.total_requests
            if self.total_requests > 0
            else 0.0
        )

        error_rate = (
            (self.failed_requests / self.total_requests) * 100
            if self.total_requests > 0
            else 0.0
        )

        return {
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "error_rate": round(error_rate, 2),
            "average_response_time": round(
                average_response_time,
                4,
            ),
        }