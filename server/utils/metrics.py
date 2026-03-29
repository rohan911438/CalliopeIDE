"""
In-memory metrics tracking for production observability
"""
import time

metrics = {
    "request_count": 0,
    "error_count": 0,
    "execution_count": 0,
    "slow_requests": 0
}

_start_time = time.time()

def increment(metric):
    """Increment a metric by 1"""
    if metric in metrics:
        metrics[metric] += 1

def get_metrics_stats():
    """Return current metrics with uptime"""
    return {
        **metrics,
        "uptime_seconds": round(time.time() - _start_time, 2)
    }
