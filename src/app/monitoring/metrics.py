from prometheus_client import Counter, Histogram

# Total HTTP requests, labeled by method, path, and status code
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests.",
    ["method", "path", "status"],
)

# Request latency in seconds, labeled by method and path
REQUEST_LATENCY = Histogram(
    "http_request_latency_seconds",
    "HTTP request latency in seconds.",
    ["method", "path"],
)

# Errors (5xx responses) count
ERROR_COUNT = Counter(
    "http_errors_total",
    "Total HTTP 5xx errors.",
    ["method", "path"],
)
