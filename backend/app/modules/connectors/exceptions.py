class TransientSyncError(Exception):
    """
    Raised for temporary failures that should trigger a retry with backoff.
    e.g., Network timeouts, 5xx server errors, rate limits (429).
    """
    pass

class TerminalSyncError(Exception):
    """
    Raised for permanent failures that should not be retried.
    e.g., 401 Unauthorized, 403 Forbidden, 400 Bad Request, malformed config.
    """
    pass
